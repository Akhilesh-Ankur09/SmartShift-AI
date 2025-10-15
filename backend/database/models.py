from sqlalchemy import Column, Integer, String, Text, DateTime
from database.db import Base
import datetime


class MeetingReport(Base):
    __tablename__ = "meeting_reports"

    id = Column(Integer, primary_key=True, index=True)
    meeting_title = Column(String, index=True)
    meeting_date = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, default=None)
    transcript_text = Column(Text)
    final_summary = Column(Text, default=None)
    raw_transcript_path = Column(String, nullable=True)
