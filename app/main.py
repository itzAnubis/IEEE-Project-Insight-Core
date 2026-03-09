from fastapi import FastAPI
from pydantic import BaseModel
from database.connection import get_connection
from src.insight_engine.engine import generate_insights

# -------------------------------
# FastAPI App
# -------------------------------

app = FastAPI()

# system state
system_running = False


# -------------------------------
# Data Models
# -------------------------------

class VisionData(BaseModel):
    timestamp: str
    engagement: str
    faces_detected: int


class NLPData(BaseModel):
    timestamp: str
    topic: str
    sentiment: str


# -------------------------------
# Basic Routes
# -------------------------------

@app.get("/")
def home():
    return {"message": "Insight Engine API is running"}


# -------------------------------
# System Control
# -------------------------------

@app.post("/start")
def start_system():
    global system_running
    system_running = True
    return {"status": "System started"}


@app.post("/stop")
def stop_system():
    global system_running
    system_running = False
    return {"status": "System stopped"}


# -------------------------------
# Vision Data
# -------------------------------

@app.get("/vision")
def get_vision_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vision_data")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.post("/vision")
def add_vision_data(data: VisionData):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vision_data (timestamp, engagement, faces_detected)
        VALUES (?, ?, ?)
    """, (data.timestamp, data.engagement, data.faces_detected))

    conn.commit()
    conn.close()

    return {"message": "Vision data inserted"}


# -------------------------------
# NLP Data
# -------------------------------

@app.post("/nlp")
def add_nlp_data(data: NLPData):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nlp_data (timestamp, topic, sentiment)
        VALUES (?, ?, ?)
    """, (data.timestamp, data.topic, data.sentiment))

    conn.commit()
    conn.close()

    return {"message": "NLP data inserted"}


# -------------------------------
# Insights
# -------------------------------

@app.get("/get_insights")
def get_insights():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM insights")

        rows = cursor.fetchall()

        conn.close()

        insights = []

        for row in rows:
            insights.append({
                "timestamp": row["timestamp"],
                "insight": row["insight"]
            })

        return {"insights": insights}

    except Exception as e:

        return {
            "error": "Failed to fetch insights",
            "details": str(e)
        }


# -------------------------------
# Metrics
# -------------------------------

@app.get("/get_metrics")
def get_metrics():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM scores")

        rows = cursor.fetchall()

        conn.close()

        metrics = []

        for row in rows:
            metrics.append({
                "engagement_score": row["engagement_score"],
                "clarity_score": row["clarity_score"],
                "interaction_score": row["interaction_score"],
                "total_score": row["total_score"]
            })

        return {"metrics": metrics}

    except Exception as e:

        return {
            "error": "Failed to fetch metrics",
            "details": str(e)
        }


@app.post("/generate_insights")
def run_insight_engine():

    insights = generate_insights()

    return {
        "generated_insights": insights
    }