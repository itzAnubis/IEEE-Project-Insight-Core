import sqlite3
from pathlib import Path

# path to database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "project.db"


def get_all_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT engagement, clarity, interaction, final_score
        FROM scores
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def get_all_insights():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.timestamp, v.emotion, n.sentiment, i.correlation_score
        FROM insights i
        JOIN vision_data v ON i.vision_id = v.id
        JOIN nlp_data n ON i.nlp_id = n.id
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def get_average_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            AVG(engagement),
            AVG(clarity),
            AVG(interaction),
            AVG(final_score)
        FROM scores
    """)

    result = cursor.fetchone()

    conn.close()

    return result