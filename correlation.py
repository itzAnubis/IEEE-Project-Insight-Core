import pandas as pd


def correlate_low_engagement(
    vision_df: pd.DataFrame,
    nlp_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Maps low engagement timestamps from Vision data
    to current topics from NLP data.

    Returns:
        DataFrame with columns:
        - timestamp
        - topic
        - engagement_level
    """

    if vision_df.empty or nlp_df.empty:
        raise ValueError("Input DataFrames must not be empty.")

    required_vision_cols = {"timestamp", "engagement_level"}
    required_nlp_cols = {"timestamp", "current_topic"}

    if not required_vision_cols.issubset(vision_df.columns):
        raise ValueError("Vision data missing required columns.")

    if not required_nlp_cols.issubset(nlp_df.columns):
        raise ValueError("NLP data missing required columns.")

    # Work on copies to avoid SettingWithCopyWarning
    vision_df = vision_df.copy()
    nlp_df = nlp_df.copy()

    # Ensure timestamp is datetime
    vision_df["timestamp"] = pd.to_datetime(vision_df["timestamp"])
    nlp_df["timestamp"] = pd.to_datetime(nlp_df["timestamp"])

    # Filter low engagement
    low_engagement = vision_df[
        vision_df["engagement_level"] == "Low"
    ]

    if low_engagement.empty:
        return pd.DataFrame(
            columns=["timestamp", "topic", "engagement_level"]
        )

    # Merge on timestamp
    merged = pd.merge(
        low_engagement,
        nlp_df,
        on="timestamp",
        how="inner"
    )

    result = merged[["timestamp", "current_topic", "engagement_level"]]
    result = result.rename(columns={"current_topic": "topic"})

    # Sort for clean output
    return result.sort_values("timestamp").reset_index(drop=True)