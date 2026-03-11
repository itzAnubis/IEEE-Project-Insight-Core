"""
API endpoint tests for the Insight Engine.

Tests cover:
    - Health check
    - Session start / stop (success + error cases)
    - Metrics retrieval
    - Report retrieval
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ───────────────────────────────────────────
# Health Check
# ───────────────────────────────────────────

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Insight Core API running"


# ───────────────────────────────────────────
# Session Start
# ───────────────────────────────────────────

def test_start_session():
    response = client.post("/api/sessions/1/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["session_id"] == 1
    assert data["data"]["state"] == "started"


def test_start_session_already_running():
    # Ensure session 99 is started
    client.post("/api/sessions/99/start")
    # Attempting to start again should return 400
    response = client.post("/api/sessions/99/start")
    assert response.status_code == 400


# ───────────────────────────────────────────
# Session Stop
# ───────────────────────────────────────────

def test_stop_session():
    # Start then stop session 2
    client.post("/api/sessions/2/start")
    response = client.post("/api/sessions/2/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["session_id"] == 2
    assert data["data"]["state"] == "stopped"


def test_stop_session_not_running():
    response = client.post("/api/sessions/999/stop")
    assert response.status_code == 400


# ───────────────────────────────────────────
# Metrics
# ───────────────────────────────────────────

def test_get_metrics():
    response = client.get("/api/sessions/1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


# ───────────────────────────────────────────
# Report
# ───────────────────────────────────────────

def test_get_report():
    response = client.get("/api/sessions/1/report")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)