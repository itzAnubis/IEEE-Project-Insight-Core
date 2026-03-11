"""
Database schema initialization script.

Creates all tables required by the Insight Engine.
Run this script directly to initialize or reset the database:

    python database/db.py

Tables:
    - sessions       : Tracks session state
    - vision_data    : Raw vision pipeline output (per-session)
    - nlp_data       : Raw NLP pipeline output (per-session)
    - insights       : Generated insight entries (per-session)
    - scores         : Computed scoring metrics (per-session)
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "project.db")


def init_db():
    """Create all tables if they do not already exist."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        state TEXT NOT NULL DEFAULT 'stopped',
        created_at TEXT DEFAULT (datetime('now'))
    )
    """)

    # Vision data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vision_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER REFERENCES sessions(id),
        timestamp TEXT,
        engagement TEXT,
        faces_detected INTEGER
    )
    """)

    # NLP data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nlp_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER REFERENCES sessions(id),
        timestamp TEXT,
        topic TEXT,
        sentiment TEXT
    )
    """)

    # Insights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER REFERENCES sessions(id),
        timestamp TEXT,
        insight TEXT
    )
    """)

    # Scores table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER REFERENCES sessions(id),
        engagement_score REAL,
        clarity_score REAL,
        interaction_score REAL,
        total_score REAL
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully")