from scoring.scoring_from_json import score_from_json
import sqlite3

conn = sqlite3.connect("scores_database.db")
cursor = conn.cursor()

def test_system_json():
    system_data = [
        {"insight_id": 101, "instructor": {"head_pitch": 10, "status": "Active"}, "environment": {"total_people_count": 18}},
        {"insight_id": 102, "instructor": {"head_pitch": 20, "status": "Active"}, "environment": {"total_people_count": 25}},
        {"insight_id": 103, "instructor": {"head_pitch": 5, "status": "Active"}, "environment": {"total_people_count": 10}},
    ]

    for data in system_data:
        scores = score_from_json(data)
        cursor.execute("""
            INSERT INTO scores (insight_id, engagement, clarity, interaction, final_score)
            VALUES (?, ?, ?, ?, ?)
        """, (data["insight_id"], scores["engagement"], scores["clarity"], scores["interaction"], scores["final_score"]))

    conn.commit()
    print("System JSON tested and scores inserted successfully!")

if __name__ == "__main__":
    test_system_json()
    conn.close()