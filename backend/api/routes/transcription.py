from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import tempfile
import whisper
from sqlalchemy.orm import Session
from database.db import SessionLocal
from api.routes import crud
from utils.summarizer import summarize_text
from database import models

router = APIRouter()

# Load Whisper model once globally (reuse for all requests)
model = whisper.load_model("small")


# Dependency - open a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    meeting_title: str = "Untitled Meeting",
    db: Session = Depends(get_db)
):
    """
    Upload an audio/video file, transcribe it, and save to DB.
    """
    suffix = ".wav" if file.filename.endswith(".wav") else ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Run Whisper transcription
    result = model.transcribe(tmp_path)
    text = result.get("text", "")

    # Save transcript in the database
    report = crud.create_meeting_report(
        db, meeting_title=meeting_title, transcript_text=text
    )

    return {
        "message": "Transcription saved successfully!",
        "meeting_id": report.id,
        "meeting_title": report.meeting_title,
        "meeting_date": report.meeting_date,
        "transcript_preview": text[:200] + "..." if len(text) > 200 else text,
    }


@router.get("/reports")
def list_reports(db: Session = Depends(get_db)):
    """
    List all stored meeting reports from the database.
    """
    reports = crud.get_all_reports(db)
    return reports


@router.post("/summarize/{meeting_id}")
def summarize_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """
    Generate or regenerate a summary for a stored meeting report.
    """
    report = db.query(models.MeetingReport).filter(models.MeetingReport.id == meeting_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Meeting not found")

    summary = summarize_text(report.transcript_text)
    report.final_summary = summary
    db.commit()
    db.refresh(report)

    return {
        "meeting_id": report.id,
        "meeting_title": report.meeting_title,
        "summary": summary,
    }
