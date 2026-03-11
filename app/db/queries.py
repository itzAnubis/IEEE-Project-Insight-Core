"""
Database query abstraction layer.

ALL SQL statements live here.
The API layer MUST NOT write raw SQL inline.
"""

import sqlite3
from typing import Any, Dict, List, Optional


# ───────────────────────────────────────────
# Session Queries
# ───────────────────────────────────────────

def get_session_state(conn: sqlite3.Connection, session_id: int) -> Optional[str]:
    """Return the state of a session, or None if it does not exist."""

    row = conn.execute(
        "SELECT state FROM sessions WHERE id = ?",
        (session_id,),
    ).fetchone()
    return row["state"] if row else None


def create_session(conn: sqlite3.Connection, session_id: int) -> None:
    """Insert a new session record with state 'stopped'."""

    conn.execute(
        "INSERT OR IGNORE INTO sessions (id, state) VALUES (?, ?)",
        (session_id, "stopped"),
    )
    conn.commit()


def update_session_state(conn: sqlite3.Connection, session_id: int, state: str) -> None:
    """Update the state of an existing session."""

    conn.execute(
        "UPDATE sessions SET state = ? WHERE id = ?",
        (state, session_id),
    )
    conn.commit()


# ───────────────────────────────────────────
# Metrics Queries
# ───────────────────────────────────────────

def fetch_metrics_by_session(conn: sqlite3.Connection, session_id: int) -> List[Dict[str, Any]]:
    """Return all score rows for a given session."""

    rows = conn.execute(
        "SELECT engagement_score, clarity_score, interaction_score, total_score "
        "FROM scores WHERE session_id = ?",
        (session_id,),
    ).fetchall()

    return [
        {
            "engagement": row["engagement_score"],
            "clarity": row["clarity_score"],
            "interaction": row["interaction_score"],
            "final_score": row["total_score"],
        }
        for row in rows
    ]


# ───────────────────────────────────────────
# Insights / Report Queries
# ───────────────────────────────────────────

def fetch_insights_by_session(conn: sqlite3.Connection, session_id: int) -> List[Dict[str, Any]]:
    """Return all insight rows for a given session."""

    rows = conn.execute(
        "SELECT timestamp, insight FROM insights WHERE session_id = ?",
        (session_id,),
    ).fetchall()

    return [
        {
            "timestamp": row["timestamp"],
            "insight": row["insight"],
        }
        for row in rows
    ]
