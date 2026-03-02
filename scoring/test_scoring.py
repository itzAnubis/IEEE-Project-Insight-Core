from scoring import calculate_interaction, calculate_final_score


def test_interaction():
    result = calculate_interaction(10, 5, 5)
    expected = (10*0.4) + (5*0.3) + (5*0.3)
    assert result == expected


def test_final_score():
    interaction = calculate_interaction(10, 5, 5)
    result = calculate_final_score(0.8, 0.7, interaction)
    expected = (0.4*0.8) + (0.3*0.7) + (0.3*interaction)
    assert result == expected