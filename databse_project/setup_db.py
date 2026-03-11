import sqlite3
from pathlib import Path

# Get project root (مكان ملف setup_db.py نفسه)
BASE_DIR = Path(__file__).resolve().parent

# Define paths safely
DB_PATH = BASE_DIR / "database" / "project.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def setup_database():
    # Create database folder if not exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()

    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    conn.close()

    print("✅ Database created successfully")
    print("✅ Tables created:", tables)
    print(f"📁 Database location: {DB_PATH}")


if __name__ == "__main__":
    setup_database()