import sqlite3
from scoring.scoring import calculate_final_score
conn = sqlite3.connect("scores_database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight_id INTEGER,
    engagement REAL,
    clarity REAL,
    interaction REAL,
    final_score REAL
)
""")
conn.commit()
def insert_score(insight_id, engagement, clarity, interaction):
    final_score = calculate_final_score(engagement, clarity, interaction)
    cursor.execute("""
    INSERT INTO scores (insight_id, engagement, clarity, interaction, final_score)
    VALUES (?, ?, ?, ?, ?)
    """, (insight_id, engagement, clarity, interaction, final_score))
    conn.commit()
    print("Score inserted successfully!")
if __name__ == "__main__":
    insert_score(1,0.7,0.8,0.6)
    conn.close()