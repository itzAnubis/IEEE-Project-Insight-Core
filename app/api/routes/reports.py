import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_db
from app.api.schemas.report import ReportResponse
from app.core.logging import logger
from app.db import queries

router = APIRouter(prefix="/sessions", tags=["Reports"])


@router.get("/{session_id}/report", response_model=ReportResponse)
def get_report(session_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Retrieve insight report for a specific session."""

    logger.info(f"Fetching report for session {session_id}")

    try:
        insights = queries.fetch_insights_by_session(conn, session_id)
    except Exception as e:
        logger.error(f"DB failure fetching report for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve report")

    logger.info(f"Returned {len(insights)} insights for session {session_id}")

    return {
        "status": "success",
        "data": insights,
    }
