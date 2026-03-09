from database.connection import get_connection


def generate_insights():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vision_data")
    vision_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM nlp_data")
    nlp_rows = cursor.fetchall()

    insights = []

    for v in vision_rows:
        for n in nlp_rows:

            if v["timestamp"] == n["timestamp"]:

                if v["engagement"] == "low":

                    insight_text = f"Low engagement detected during topic {n['topic']}"

                    cursor.execute("""
                    INSERT INTO insights (timestamp, insight)
                    VALUES (?, ?)
                    """, (v["timestamp"], insight_text))

                    insights.append(insight_text)

    conn.commit()
    conn.close()

    return insights