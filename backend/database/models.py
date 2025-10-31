from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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

    intervals = relationship("IntervalSummary", back_populates="meeting", cascade="all, delete-orphan")


class IntervalSummary(Base):
    __tablename__ = "interval_summaries"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting_reports.id", ondelete="CASCADE"), nullable=False)
    interval_index = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=None)
    end_time = Column(DateTime, default=None)
    transcript_text = Column(Text)
    interval_summary = Column(Text)

    meeting = relationship("MeetingReport", back_populates="intervals")
