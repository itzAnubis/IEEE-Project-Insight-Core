# scoring/test_scoring.py
from scoring.scoring import calculate_head_pose_score, calculate_interaction, calculate_final_score

def test_head_pose_score():
    result = calculate_head_pose_score(0.8)
    assert 0 <= result <= 1

def test_interaction_score():
    result = calculate_interaction(0.75)
    assert 0 <= result <= 1

def test_final_score():
    interaction = calculate_interaction(0.75)
    result = calculate_final_score(0.7, 0.8, interaction)
    assert 0 <= result <= 1

if __name__ == "__main__":
    test_head_pose_score()
    test_interaction_score()
    test_final_score()
    print("All tests passed successfully!")