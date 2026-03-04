from alerts.health_check import run_health_check
dummy_report = {
    "transcription": {"full_transcript": ""},
    "diarization_stats": {"total_segments": 0},
    "summary": "Skipped due to error."
}

status = run_health_check("unavailable", dummy_report)

print("System Healthy?" , status)