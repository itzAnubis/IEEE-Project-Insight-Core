def calculate_interaction(clicks, comments, shares):
    return (clicks * 0.4) + (comments * 0.3) + (shares * 0.3)


def calculate_final_score(engagement, clarity, interaction):
    return (0.4 * engagement) + (0.3 * clarity) + (0.3 * interaction)