import pandas as pd
import numpy as np


def calculate_engagement(active_faces, total_faces, distraction_score):

    if total_faces == 0:
        return 0

    focus_ratio = active_faces / total_faces
    score = (focus_ratio * 0.8) - (distraction_score * 0.2)
    return max(0, min(round(score, 2), 1))


def calculate_clarity(gestures_score, stability_score):
    score = (gestures_score * 0.6) + (stability_score * 0.4)
    return max(0, min(round(score, 2), 1))


def integrate_scoring_logic(insights_df):

    df = insights_df.fillna(0)

    df['engagement'] = df.apply(lambda x: calculate_engagement(
        x['active_faces'], x['total_faces'], x['distract']
    ), axis=1)

    df['clarity'] = df.apply(lambda x: calculate_clarity(
        x['gestures'], x['stability']
    ), axis=1)

    return df[['insight_id', 'engagement', 'clarity']]


if __name__ == "__main__":
    sample_data = {
        'insight_id': [101, 102, 103],
        'active_faces': [8, 5, 2],
        'total_faces': [10, 10, 10],
        'distract': [0.1, 0.4, 0.6],
        'gestures': [0.8, 0.5, 0.2],
        'stability': [0.9, 0.7, 0.4]
    }
    df_test = pd.DataFrame(sample_data)
    results = integrate_scoring_logic(df_test)
    print("Integration Results:")
    print(results)
