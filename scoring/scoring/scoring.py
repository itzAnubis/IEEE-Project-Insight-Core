def calculate_hand_raise_score(hand_raises, max_expected=5):
    if max_expected <= 0:
        return 0
    return min(hand_raises / max_expected, 1)

def calculate_head_pose_score(attention_ratio):
    return min(max(attention_ratio, 0), 1)

def calculate_qa_participation_score(questions_asked, max_expected=3):
    if max_expected <= 0:
        return 0
    return min(questions_asked / max_expected, 1)

def calculate_interaction(hand_raises, attention_ratio, questions_asked):
    hand_score = calculate_hand_raise_score(hand_raises)
    head_score = calculate_head_pose_score(attention_ratio)
    qa_score = calculate_qa_participation_score(questions_asked)
    return (hand_score + head_score + qa_score) / 3

def calculate_final_score(engagement, clarity, interaction):
    return (0.4 * engagement) + (0.3 * clarity) + (0.3 * interaction)
def generate_insights(engagement, clarity, interaction):
    final_score = calculate_final_score(engagement, clarity, interaction)
    if final_score >= 0.8:
        insight = "Excellent engagement and participation"
    elif final_score >= 0.6:
        insight = "Good lecture but interaction could improve"
    else:
        insight = "Low engagement detected"
    return {
        "engagement": engagement,
        "clarity": clarity,
        "interaction": interaction,
        "final_score": final_score,
        "insight": insight
    }