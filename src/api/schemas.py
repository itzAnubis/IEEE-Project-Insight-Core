"""
Pydantic schemas for all API request/response models.

Every endpoint returns an APIResponse envelope:
  { "status": "success"|"error", "message": "...", "data": ... }
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Optional, List
from datetime import datetime


# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------

class APIResponse(BaseModel):
    """Standard API response wrapper."""
    status: str = Field(..., examples=["success", "error"])
    message: str
    data: Optional[Any] = None


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

class SessionSchema(BaseModel):
    id: int
    title: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    instructor_name: str
    status: str

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Attendance
# ---------------------------------------------------------------------------

class AttendanceItem(BaseModel):
    id: int
    session_id: int
    timestamp: datetime
    count: int
    engagement_score: float

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Transcript
# ---------------------------------------------------------------------------

class TranscriptItem(BaseModel):
    id: int
    session_id: int
    timestamp: datetime
    speaker: str
    text: str
    is_question: bool

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Speech Metrics
# ---------------------------------------------------------------------------

class SpeechMetricItem(BaseModel):
    id: int
    session_id: int
    timestamp: datetime
    wpm: float
    silence_gap: float
    tone_variance: float

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Scores (computed)
# ---------------------------------------------------------------------------

class MetricsScores(BaseModel):
    engagement: float
    clarity: float
    interaction: float
    overall: float


# ---------------------------------------------------------------------------
# Aggregated Metrics
# ---------------------------------------------------------------------------

class MetricsSummary(BaseModel):
    avg_engagement: float
    peak_attendance: int
    final_attendance: int
    dropoff_rate: float
    avg_wpm: float
    silence_ratio: float


class MetricsResponse(BaseModel):
    session_id: int
    title: str
    start_time: Optional[datetime] = None
    metrics: MetricsSummary
    scores: MetricsScores


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

class ReportSchema(BaseModel):
    id: int
    session_id: int
    summary: str
    key_topics: str
    overall_score: float
    created_at: datetime

    class Config:
        from_attributes = True
