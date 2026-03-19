# Data Format Specification

## Vision Data

| Column | Type | Description |
|---|---|---|
| timestamp | datetime | capture time |
| face_detected | boolean | face presence |
| engagement_level | string | High / Medium / Low |
| emotion | string | detected emotion |

## NLP Data

| Column | Type | Description |
|---|---|---|
| timestamp | datetime | analysis time |
| current_topic | string | active topic |
| sentiment | string | sentiment result |
| keywords | string/list | extracted keywords |

## Insights Table

| Column | Type |
|---|---|
| timestamp | datetime |
| topic | string |
| engagement_level | string |
| insight_text | string |

Unique Constraint:
(timestamp, topic)