import sqlite3

# connect to database
conn = sqlite3.connect("database/project.db")

cursor = conn.cursor()

# vision table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vision_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    engagement TEXT,
    faces_detected INTEGER
)
""")

# nlp table
cursor.execute("""
CREATE TABLE IF NOT EXISTS nlp_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    topic TEXT,
    sentiment TEXT
)
""")

# insights table
cursor.execute("""
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    insight TEXT
)
""")

# scores table
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    engagement_score REAL,
    clarity_score REAL,
    interaction_score REAL,
    total_score REAL
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully")