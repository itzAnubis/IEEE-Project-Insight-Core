"""
SQLAlchemy ORM models for the Session Management API.

Tables:
  - sessions          (parent)
  - attendance_metrics (FK → sessions)
  - transcripts        (FK → sessions)
  - speech_metrics     (FK → sessions)
  - session_reports    (FK → sessions)
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    instructor_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="idle")  # idle | active | completed

    # Relationships
    attendance_metrics = relationship("AttendanceMetric", back_populates="session", cascade="all, delete-orphan")
    transcripts = relationship("Transcript", back_populates="session", cascade="all, delete-orphan")
    speech_metrics = relationship("SpeechMetric", back_populates="session", cascade="all, delete-orphan")
    reports = relationship("SessionReport", back_populates="session", cascade="all, delete-orphan")


class AttendanceMetric(Base):
    __tablename__ = "attendance_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    count = Column(Integer, nullable=False)
    engagement_score = Column(Float, nullable=False)

    session = relationship("Session", back_populates="attendance_metrics")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    speaker = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    is_question = Column(Boolean, nullable=False, default=False)

    session = relationship("Session", back_populates="transcripts")


class SpeechMetric(Base):
    __tablename__ = "speech_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    wpm = Column(Float, nullable=False)
    silence_gap = Column(Float, nullable=False)
    tone_variance = Column(Float, nullable=False)

    session = relationship("Session", back_populates="speech_metrics")


class SessionReport(Base):
    __tablename__ = "session_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text, nullable=False)
    key_topics = Column(Text, nullable=False)  # Stored as comma-separated or JSON string
    overall_score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    session = relationship("Session", back_populates="reports")
