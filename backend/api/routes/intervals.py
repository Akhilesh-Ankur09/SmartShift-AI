from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database import models
from utils.audio_utils import split_audio_to_chunks
from utils.summarizer import summarize_text
import whisper, tempfile, os
from datetime import datetime, timedelta

router = APIRouter()
model = whisper.load_model("small")  # reuse the same Whisper model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _process_chunks_and_save(meeting_id: int, chunks, meeting_start_dt, session_factory):
    """
    Background worker: transcribe each chunk, summarize, save to DB.
    """
    db = session_factory()
    try:
        for idx, (chunk_path, start_ms, end_ms) in enumerate(chunks):
            # 1) transcribe
            result = model.transcribe(chunk_path)
            text = result.get("text", "")

            # 2) summarize chunk
            summary = summarize_text(text, max_length=120)

            # 3) convert offsets (ms) to datetimes relative to meeting_start_dt
            start_dt = meeting_start_dt + timedelta(milliseconds=int(start_ms))
            end_dt = meeting_start_dt + timedelta(milliseconds=int(end_ms))

            # 4) save interval
            row = models.IntervalSummary(
                meeting_id=meeting_id,
                interval_index=idx,
                start_time=start_dt,
                end_time=end_dt,
                transcript_text=text,
                interval_summary=summary
            )
            db.add(row); db.commit()

            # 5) cleanup
            try: os.remove(chunk_path)
            except OSError: pass
    finally:
        db.close()


@router.post("/transcribe/intervals")
async def transcribe_intervals(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    meeting_title: str = "Untitled Meeting",
    interval_minutes: int = 5,
    db: Session = Depends(get_db)
):
    """
    Upload audio, create meeting record, then chunk/transcribe/summarize in background.
    Returns meeting_id immediately.
    """
    # save upload temporarily
    suffix = ".wav" if file.filename.endswith(".wav") else ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # create meeting
    meeting = models.MeetingReport(
        meeting_title=meeting_title,
        meeting_date=datetime.utcnow(),
        started_at=datetime.utcnow(),
        transcript_text=""
    )
    db.add(meeting); db.commit(); db.refresh(meeting)

    # split into chunks
    chunks = split_audio_to_chunks(tmp_path, chunk_minutes=interval_minutes)
    meeting_start_dt = datetime.utcnow()

    # process in background
    background_tasks.add_task(_process_chunks_and_save, meeting.id, chunks, meeting_start_dt, SessionLocal)

    # remove original file
    try: os.remove(tmp_path)
    except OSError: pass

    return {"message": "interval processing started", "meeting_id": meeting.id, "interval_minutes": interval_minutes}


@router.get("/intervals/{meeting_id}")
def get_intervals(meeting_id: int, db: Session = Depends(get_db)):
    rows = (db.query(models.IntervalSummary)
              .filter(models.IntervalSummary.meeting_id == meeting_id)
              .order_by(models.IntervalSummary.interval_index)
              .all())
    return [
        {
            "id": r.id,
            "interval_index": r.interval_index,
            "start_time": r.start_time.isoformat() if r.start_time else None,
            "end_time": r.end_time.isoformat() if r.end_time else None,
            "interval_summary": r.interval_summary
        } for r in rows
    ]
