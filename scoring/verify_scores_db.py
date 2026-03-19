import sqlite3
conn = sqlite3.connect("scores_database.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM scores")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
required_columns = ["Id", "insight_id", "engagement", "clarity", "interaction", "final_score"]
print("Columns in table:", columns)
if all(col in columns for col in required_columns):
    print("✅ All required columns exist.")
else:
    print("❌ Some required columns are missing.")
insight_ids = [row[1] for row in rows]  
if len(insight_ids) == len(set(insight_ids)):
    print("✅ No duplicate insight_id records.")
else:
    print("❌ Duplicate insight_id records found!")

print("\nAll scores in the database:")
for row in rows:
    print(row)
conn.close()