from sqlalchemy.orm import Session
from database import models
import datetime


def create_meeting_report(db: Session, meeting_title: str, transcript_text: str):
    rec = models.MeetingReport(
        meeting_title=meeting_title,
        meeting_date=datetime.datetime.utcnow(),
        started_at=datetime.datetime.utcnow(),
        transcript_text=transcript_text,
    )
    db.add(rec); db.commit(); db.refresh(rec)
    return rec


def get_all_reports(db: Session):
    return db.query(models.MeetingReport).all()
