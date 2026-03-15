from scoring.scoring import calculate_interaction, calculate_final_score

def score_from_json(json_data, max_people=30):
    """
    Compute scoring metrics from system JSON output.
    Interaction is based only on head pose since hand raises and QA are not available.
    """
    instructor_data = json_data.get("instructor", {})
    env_data = json_data.get("environment", {})

    head_pitch = instructor_data.get("head_pitch", 0)
    total_people_count = env_data.get("total_people_count", 0)
    status = instructor_data.get("status", "Unknown")

    # Convert head_pitch to attention_ratio
    attention_ratio = max(0, 1 - abs(head_pitch)/30)

    # Interaction based only on attention_ratio
    interaction = calculate_interaction(attention_ratio)

    # Engagement based on number of people (normalized)
    engagement = min(total_people_count / max_people, 1)

    # Clarity (default until NLP is available)
    clarity = 0.8

    # Final score
    final_score = calculate_final_score(engagement, clarity, interaction)

    scoring_result = {
        "engagement": engagement,
        "clarity": clarity,
        "interaction": interaction,
        "final_score": final_score,
        "attention_ratio": attention_ratio,
        "status": status
    }

    return scoring_result


# Example usage
if __name__ == "__main__":
    json_example = {
        "timestamp": 1234567890,
        "instructor": {"head_pitch": 10, "status": "Active"},
        "environment": {"total_people_count": 18, "crowd_history_length": 5}
    }

    scores = score_from_json(json_example)
    print(scores)