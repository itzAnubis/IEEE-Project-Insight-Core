import sqlite3
from pathlib import Path

# Get project root
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "project.db"


def test_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = ["vision_data", "nlp_data", "insights", "scores"]

    for table in tables:
        cursor.execute(f"SELECT * FROM {table} LIMIT 1;")

    conn.close()
    print("✅ All tables accessible. Database connection successful.")


if __name__ == "__main__":
    test_connection()