# Database Queries Documentation

## 1. Get All Scores

SQL Query:
SELECT engagement, clarity, interaction, final_score
FROM scores;

Purpose:
Retrieve engagement, clarity, interaction, and final score from the scores table.

---

## 2. Get Insights with Vision & NLP Data

SQL Query:
SELECT v.timestamp, v.emotion, n.sentiment, i.correlation_score
FROM insights i
JOIN vision_data v ON i.vision_id = v.id
JOIN nlp_data n ON i.nlp_id = n.id;

Purpose:
Combine vision data and NLP sentiment with the correlation score.

---

## 3. Average Scores

SQL Query:
SELECT
AVG(engagement),
AVG(clarity),
AVG(interaction),
AVG(final_score)
FROM scores;

Purpose:
Calculate the average engagement, clarity, interaction, and final score.

---

# Helper Functions

## get_all_scores()

Returns all scoring values.

Example:
from database.db_utils import get_all_scores

scores = get_all_scores()

---

## get_all_insights()

Returns vision and NLP insights with correlation score.

Example:
from database.db_utils import get_all_insights

data = get_all_insights()

---

## get_average_scores()

Returns average values for scoring metrics.

Example:
from database.db_utils import get_average_scores

avg = get_average_scores()