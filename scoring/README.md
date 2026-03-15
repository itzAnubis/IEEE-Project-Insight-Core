# Interaction Scoring Metric

## Overview
The Interaction metric measures active student participation during an online lecture session.

It is designed to be compatible with outputs from both Computer Vision and NLP models.

All factors are normalized between 0 and 1.

---

## Selected Factors

### 1. Hand Raising (Vision-Based)

Measures how many times a student raises their hand during the session.

Calculation:
hand_raise_score = number_of_hand_raises / maximum_expected_hand_raises

Justification:
Hand raising reflects intentional participation and willingness to interact.

---

### 2. Head Pose Attention (Vision-Based)

Measures the percentage of time the student is looking at the screen.

Calculation:
head_pose_score = attention_ratio

Where attention_ratio is between 0 and 1.

Justification:
Head orientation indicates attentiveness and engagement during the lecture.

---

### 3. QA Participation (NLP-Based)

Measures the number of meaningful questions or verbal contributions.

Calculation:
qa_score = questions_asked / maximum_expected_questions

Justification:
Asking questions or participating in discussion reflects cognitive interaction.

---

## Final Interaction Score

The interaction score is calculated as the average of the three normalized factors:

interaction = (hand_raise_score + head_pose_score + qa_score) / 3

This ensures:
- Unified scale (0–1)
- Compatibility with Engagement and Clarity scores
- Fair representation of multimodal interaction