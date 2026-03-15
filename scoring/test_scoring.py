from scoring.scoring import (
    calculate_hand_raise_score,
    calculate_head_pose_score,
    calculate_qa_participation_score,
    calculate_interaction,
    calculate_final_score
)

def test_hand_raise():
    result = calculate_hand_raise_score(3, 5)
    expected = 3 / 5
    assert result == expected

def test_head_pose():
    result = calculate_head_pose_score(0.8)
    assert 0 <= result <= 1

def test_qa_participation():
    result = calculate_qa_participation_score(2, 4)
    expected = 2 / 4
    assert result == expected

def test_interaction():
    result = calculate_interaction(3, 0.8, 2)
    assert 0 <= result <= 1

def test_final_score():
    interaction = calculate_interaction(3, 0.8, 2)
    result = calculate_final_score(0.7, 0.6, interaction)
    assert 0 <= result <= 1

print("All tests passed successfully!")