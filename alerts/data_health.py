import logging

def check_data(report: dict) -> bool:
    """
    Checks NLP pipeline output integrity.
    Returns True if data looks valid, False otherwise.
    """

    system_ok = True

    # Check transcription
    if "transcription" not in report:
        logging.error("Data Issue: Missing Transcription Output")
        system_ok = False
    else:
        transcript = report["transcription"].get("full_transcript", "")
        if not transcript:
            logging.error("Data Issue: Empty Transcript")
            system_ok = False

    # Check diarization
    diar_stats = report.get("diarization_stats", {})
    if diar_stats.get("total_segments", 0) == 0:
        logging.warning("Data Issue: No Speaker Segments Detected")

    # Check summary
    if report.get("summary") == "Skipped due to error.":
        logging.warning("Data Issue: Summarization Failed")

    return system_ok