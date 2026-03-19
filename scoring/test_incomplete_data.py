from scoring.scoring import calculate_final_score
def safe_score(engagement, clarity, interaction):
    engagement = engagement if engagement is not None else 0
    clarity = clarity if clarity is not None else 0
    interaction = interaction if interaction is not None else 0
    return calculate_final_score(engagement, clarity, interaction)
def test_incomplete_data():
    test_cases = [
        (None, 0.8, 0.6),
        (0.7, None, 0.6),
        (0.7, 0.8, None),
        (None, None, 0.5),
        (None, None, None)
    ]
    for engagement, clarity, interaction in test_cases:
        result = safe_score(engagement, clarity, interaction)
        print(f"Inputs: {engagement}, {clarity}, {interaction} => Final Score: {result}")
if __name__ == "__main__":
    test_incomplete_data()