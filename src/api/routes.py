"""
API route definitions — all 11 endpoints under /api prefix.

Session Management:
  GET  /api/sessions             — list all sessions
  GET  /api/sessions/active      — get currently active sessions
  GET  /api/sessions/{id}        — get session by ID
  POST /api/sessions/{id}/start  — start session + background worker
  POST /api/sessions/{id}/stop   — stop session + background worker

Metrics & Data:
  GET /api/sessions/{id}/metrics     — aggregated metrics from DB
  GET /api/sessions/{id}/attendance  — attendance timeline
  GET /api/sessions/{id}/engagement  — engagement scores over time
  GET /api/sessions/{id}/transcript  — full transcript
  GET /api/sessions/{id}/report      — session report
  GET /api/sessions/{id}/scores      — computed scores only
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.db import get_db, SessionLocal
from src.api.models import Session, AttendanceMetric, Transcript, SpeechMetric, SessionReport
from src.api.schemas import (
    APIResponse, SessionSchema, AttendanceItem, TranscriptItem,
    ReportSchema, MetricsResponse, MetricsScores,
)
from src.api.service import worker, compute_metrics, compute_scores

logger = logging.getLogger("api.routes")

router = APIRouter(prefix="/api")


# ===========================================================================
# Helper
# ===========================================================================

def _get_session_or_404(session_id: int, db: DBSession) -> Session:
    """Fetch session by ID or raise 404."""
    session = db.query(Session).filter(Session.id == session_id).first()
    if session is None:
        logger.warning(f"Session {session_id} not found")
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Session with id {session_id} not found",
                "data": None,
            },
        )
    return session


# ===========================================================================
# Session Management
# ===========================================================================

@router.get("/sessions/active", response_model=APIResponse)
def get_active_sessions(db: DBSession = Depends(get_db)):
    """Return all sessions with status 'active'."""
    logger.info("GET /api/sessions/active")
    sessions = db.query(Session).filter(Session.status == "active").all()
    return APIResponse(
        status="success",
        message=f"Found {len(sessions)} active session(s)",
        data=[SessionSchema.model_validate(s).model_dump() for s in sessions],
    )


@router.get("/sessions", response_model=APIResponse)
def list_sessions(db: DBSession = Depends(get_db)):
    """Return all sessions."""
    logger.info("GET /api/sessions")
    sessions = db.query(Session).all()
    return APIResponse(
        status="success",
        message=f"Retrieved {len(sessions)} session(s)",
        data=[SessionSchema.model_validate(s).model_dump() for s in sessions],
    )


@router.get("/sessions/{session_id}", response_model=APIResponse)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    """Return a single session by ID."""
    logger.info(f"GET /api/sessions/{session_id}")
    session = _get_session_or_404(session_id, db)
    return APIResponse(
        status="success",
        message=f"Session {session_id} retrieved",
        data=SessionSchema.model_validate(session).model_dump(),
    )


@router.post("/sessions/{session_id}/start", response_model=APIResponse)
async def start_session(session_id: int, db: DBSession = Depends(get_db)):
    """
    Start a session:
      1. Validate session exists
      2. Check it is not already running
      3. Set status to 'active' and start_time
      4. Launch background worker that generates real data
    """
    logger.info(f"POST /api/sessions/{session_id}/start")
    session = _get_session_or_404(session_id, db)

    if session.status == "active" or worker.is_running(session_id):
        logger.warning(f"Session {session_id} is already running — rejecting duplicate start")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"Session {session_id} is already running",
                "data": None,
            },
        )

    # Activate session
    session.status = "active"
    session.start_time = datetime.utcnow()
    session.end_time = None  # Clear any previous end_time
    db.commit()
    db.refresh(session)
    logger.info(f"Session {session_id} status set to 'active'")

    # Start background worker (pass the SessionLocal factory, NOT the request-scoped db)
    await worker.start(session_id, SessionLocal)

    return APIResponse(
        status="success",
        message=f"Session {session_id} started — background data generation is running",
        data=SessionSchema.model_validate(session).model_dump(),
    )


@router.post("/sessions/{session_id}/stop", response_model=APIResponse)
async def stop_session(session_id: int, db: DBSession = Depends(get_db)):
    """
    Stop a session:
      1. Validate session exists
      2. Stop background worker
      3. Set status to 'completed', set end_time
      4. Generate session report
    """
    logger.info(f"POST /api/sessions/{session_id}/stop")
    session = _get_session_or_404(session_id, db)

    if session.status != "active" and not worker.is_running(session_id):
        logger.warning(f"Session {session_id} is not currently running")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"Session {session_id} is not currently running",
                "data": None,
            },
        )

    # Stop background worker (handles finalization + report generation internally)
    await worker.stop(session_id, SessionLocal)

    # Re-read the session to get updated state
    db.refresh(session)
    logger.info(f"Session {session_id} stopped and finalized")

    return APIResponse(
        status="success",
        message=f"Session {session_id} stopped — report generated",
        data=SessionSchema.model_validate(session).model_dump(),
    )


# ===========================================================================
# Metrics & Data
# ===========================================================================

@router.get("/sessions/{session_id}/metrics", response_model=APIResponse)
def get_metrics(session_id: int, db: DBSession = Depends(get_db)):
    """Return aggregated metrics computed from real DB data."""
    logger.info(f"GET /api/sessions/{session_id}/metrics")
    _get_session_or_404(session_id, db)

    result = compute_metrics(session_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": f"Session {session_id} not found",
            "data": None,
        })

    return APIResponse(
        status="success",
        message=f"Metrics for session {session_id} computed from database",
        data=result.model_dump(),
    )


@router.get("/sessions/{session_id}/attendance", response_model=APIResponse)
def get_attendance(session_id: int, db: DBSession = Depends(get_db)):
    """Return the attendance timeline for a session."""
    logger.info(f"GET /api/sessions/{session_id}/attendance")
    _get_session_or_404(session_id, db)

    rows = db.query(AttendanceMetric).filter(
        AttendanceMetric.session_id == session_id
    ).order_by(AttendanceMetric.timestamp).all()

    return APIResponse(
        status="success",
        message=f"Retrieved {len(rows)} attendance record(s) for session {session_id}",
        data=[AttendanceItem.model_validate(r).model_dump() for r in rows],
    )


@router.get("/sessions/{session_id}/engagement", response_model=APIResponse)
def get_engagement(session_id: int, db: DBSession = Depends(get_db)):
    """Return engagement scores over time for a session."""
    logger.info(f"GET /api/sessions/{session_id}/engagement")
    _get_session_or_404(session_id, db)

    rows = db.query(AttendanceMetric).filter(
        AttendanceMetric.session_id == session_id
    ).order_by(AttendanceMetric.timestamp).all()

    engagement_data = [
        {
            "timestamp": r.timestamp.isoformat(),
            "engagement_score": r.engagement_score,
            "attendance_count": r.count,
        }
        for r in rows
    ]

    return APIResponse(
        status="success",
        message=f"Retrieved {len(engagement_data)} engagement data point(s) for session {session_id}",
        data=engagement_data,
    )


@router.get("/sessions/{session_id}/transcript", response_model=APIResponse)
def get_transcript(session_id: int, db: DBSession = Depends(get_db)):
    """Return the full transcript for a session."""
    logger.info(f"GET /api/sessions/{session_id}/transcript")
    _get_session_or_404(session_id, db)

    rows = db.query(Transcript).filter(
        Transcript.session_id == session_id
    ).order_by(Transcript.timestamp).all()

    return APIResponse(
        status="success",
        message=f"Retrieved {len(rows)} transcript entry/entries for session {session_id}",
        data=[TranscriptItem.model_validate(r).model_dump() for r in rows],
    )


@router.get("/sessions/{session_id}/report", response_model=APIResponse)
def get_report(session_id: int, db: DBSession = Depends(get_db)):
    """Return the session report (generated on stop)."""
    logger.info(f"GET /api/sessions/{session_id}/report")
    _get_session_or_404(session_id, db)

    report = db.query(SessionReport).filter(
        SessionReport.session_id == session_id
    ).order_by(SessionReport.created_at.desc()).first()

    if report is None:
        return APIResponse(
            status="success",
            message=f"No report available for session {session_id} — session may not have been stopped yet",
            data=None,
        )

    return APIResponse(
        status="success",
        message=f"Report for session {session_id} retrieved",
        data=ReportSchema.model_validate(report).model_dump(),
    )


@router.get("/sessions/{session_id}/scores", response_model=APIResponse)
def get_scores(session_id: int, db: DBSession = Depends(get_db)):
    """Return computed scores for a session."""
    logger.info(f"GET /api/sessions/{session_id}/scores")
    _get_session_or_404(session_id, db)

    scores = compute_scores(session_id, db)
    if scores is None:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": f"Session {session_id} not found",
            "data": None,
        })

    return APIResponse(
        status="success",
        message=f"Scores for session {session_id} computed from database",
        data=scores.model_dump(),
    )
