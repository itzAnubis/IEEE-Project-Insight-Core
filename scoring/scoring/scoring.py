def calculate_head_pose_score(attention_ratio):
    """Compute score based on head pose attention ratio (0-1)."""
    return min(max(attention_ratio, 0), 1)

def calculate_interaction(attention_ratio):
    """Interaction score based only on head pose."""
    return calculate_head_pose_score(attention_ratio)

def calculate_final_score(engagement, clarity, interaction):
    """Final score = 0.4*engagement + 0.3*clarity + 0.3*interaction"""
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