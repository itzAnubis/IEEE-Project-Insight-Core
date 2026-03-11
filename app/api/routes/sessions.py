import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_db
from app.api.schemas.session import SessionResponse
from app.core.logging import logger
from app.db import queries

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/{session_id}/start", response_model=SessionResponse)
def start_session(session_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Start a session. Returns 400 if the session is already running."""

    state = queries.get_session_state(conn, session_id)

    if state == "started":
        logger.warning(f"Attempted to start session {session_id} but it is already running")
        raise HTTPException(status_code=400, detail=f"Session {session_id} already running")

    # Create the session record if it does not exist yet
    if state is None:
        queries.create_session(conn, session_id)

    queries.update_session_state(conn, session_id, "started")
    logger.info(f"Session {session_id} started")

    return {
        "status": "success",
        "data": {
            "session_id": session_id,
            "state": "started",
        },
    }


@router.post("/{session_id}/stop", response_model=SessionResponse)
def stop_session(session_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Stop a running session. Returns 400 if the session is not running."""

    state = queries.get_session_state(conn, session_id)

    if state != "started":
        logger.warning(f"Attempted to stop session {session_id} but it is not running")
        raise HTTPException(status_code=400, detail=f"Session {session_id} is not running")

    queries.update_session_state(conn, session_id, "stopped")
    logger.info(f"Session {session_id} stopped")

    return {
        "status": "success",
        "data": {
            "session_id": session_id,
            "state": "stopped",
        },
    }
