import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_db
from app.api.schemas.metrics import MetricsResponse
from app.core.logging import logger
from app.db import queries

router = APIRouter(prefix="/sessions", tags=["Metrics"])


@router.get("/{session_id}/metrics", response_model=MetricsResponse)
def get_metrics(session_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Retrieve scoring metrics for a specific session."""

    logger.info(f"Fetching metrics for session {session_id}")

    try:
        metrics = queries.fetch_metrics_by_session(conn, session_id)
    except Exception as e:
        logger.error(f"DB failure fetching metrics for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")

    logger.info(f"Returned {len(metrics)} metric entries for session {session_id}")

    return {
        "status": "success",
        "data": metrics,
    }
