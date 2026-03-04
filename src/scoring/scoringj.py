import pandas as pd
import numpy as np


def calculate_engagement(focus_ratio, distraction_score):
    score = (focus_ratio * 0.8) - (distraction_score * 0.2)
    return max(0, min(round(score, 2), 1))


def calculate_clarity(gestures_score, stability_score):
    score = (gestures_score * 0.6) + (stability_score * 0.4)
    return max(0, min(round(score, 2), 1))


def get_partial_scores(df):
    df['focus_ratio'] = df['focus'].apply(
        lambda x: 1 - (min(x, 90) / 90)).fillna(0.5)
    df['gestures_scaled'] = df['gestures'] / 10

    df['engagement'] = df.apply(lambda x: calculate_engagement(
        x['focus_ratio'], x['distract']), axis=1)
    df['clarity'] = df.apply(lambda x: calculate_clarity(
        x['gestures_scaled'], x['stability']), axis=1)

    return df[['engagement', 'clarity']]


if __name__ == "__main__":
    raw_data = {
        'student_id': [202200441, 202200442, 202200443, 202200444],
        'focus': [15.5, 85.0, np.nan, 12.0],
        'distract': [0.1, 0.8, 0.5, 0.2],
        'gestures': [5, 2, 0, 10],
        'stability': [0.9, 0.4, 0.7, 0.8]
    }

    test_df = pd.DataFrame(raw_data)
    results = get_partial_scores(test_df)
    print(results)
