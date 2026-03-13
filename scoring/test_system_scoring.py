from scoring.scoring import calculate_hand_raise_score, calculate_head_pose_score, calculate_qa_participation_score, calculate_interaction, calculate_final_score, generate_insights
import sqlite3
conn = sqlite3.connect("scores_database.db")
cursor = conn.cursor()
def test_system_data():
    system_data = [
        {"insight_id": 101, "hand_raises": 3, "attention_ratio": 0.9, "questions_asked": 2, "engagement": 0.7, "clarity": 0.8},
        {"insight_id": 102, "hand_raises": 1, "attention_ratio": 0.6, "questions_asked": 1, "engagement": 0.5, "clarity": 0.6},
        {"insight_id": 103, "hand_raises": 4, "attention_ratio": 1.0, "questions_asked": 3, "engagement": 0.9, "clarity": 0.9}
    ]
    for data in system_data:
        interaction = calculate_interaction(data["hand_raises"], data["attention_ratio"], data["questions_asked"])
        final_score = calculate_final_score(data["engagement"], data["clarity"], interaction)
        cursor.execute("""
            INSERT INTO scores (insight_id, engagement, clarity, interaction, final_score)
            VALUES (?, ?, ?, ?, ?)
        """, (data["insight_id"], data["engagement"], data["clarity"], interaction, final_score))
    conn.commit()
    print("System data tested and scores inserted successfully!")
if __name__ == "__main__":
    test_system_data()
    conn.close()