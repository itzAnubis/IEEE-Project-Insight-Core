import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_get_insights():
    response = client.get("/get_insights")
    assert response.status_code == 200


def test_get_metrics():
    response = client.get("/get_metrics")
    assert response.status_code == 200