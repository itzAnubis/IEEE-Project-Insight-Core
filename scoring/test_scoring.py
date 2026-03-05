from scoring import (
    calculate_hand_raise_score,
    calculate_head_pose_score,
    calculate_qa_participation_score,
    calculate_interaction,
    calculate_final_score
)

def test_hand_raise():
    result = calculate_hand_raise_score(3, 5)
    assert result == 0.6

def test_interaction():
    result = calculate_interaction(5, 1.0, 2)
    assert 0 <= result <= 1

def test_final_score():
    interaction = calculate_interaction(5, 1.0, 2)
    result = calculate_final_score(0.8, 0.7, interaction)
    assert 0 <= result <= 1

print("All tests passed successfully!")