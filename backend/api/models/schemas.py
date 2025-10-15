from pydantic import BaseModel
from datetime import datetime


class MeetingReportCreate(BaseModel):
    meeting_title: str
    transcript: str


class MeetingReportResponse(BaseModel):
    id: int
    meeting_title: str
    meeting_date: datetime
    started_at: datetime
    final_summary: str | None = None

    class Config:
        orm_mode = True
