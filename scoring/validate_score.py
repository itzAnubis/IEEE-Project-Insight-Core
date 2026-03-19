from scoring.scoring import calculate_final_score
def test_final_score():
    test_cases = [
        (1, 1, 1),
        (0, 0, 0),
        (0.5, 0.5, 0.5),
        (0.7, 0.8, 0.6),
        (0.2, 0.9, 0.3)
    ]
    for engagement, clarity, interaction in test_cases:
        result = calculate_final_score(engagement, clarity, interaction)
        print(f"Inputs: {engagement}, {clarity}, {interaction} => Final Score: {result}")

        assert 0 <= result <= 1, "Error: score out of range!"
if __name__ == "__main__":
    test_final_score()
    print("All tests passed successfully!")