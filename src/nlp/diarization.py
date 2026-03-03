import os
import json
import torch
from collections import defaultdict
from pydub import AudioSegment
from pyannote.audio import Pipeline

def run_diarization(audio_path: str, hf_token: str, output_path: str = "diarization_output.json"):
    """
    Identifies speakers and labels the predominant speaker in the first 3 mins as 'Instructor'.
    """
    print(f"Starting Diarization for {audio_path}...")
    
    # Load Pipeline
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=hf_token
    )
    if torch.cuda.is_available(): pipeline.to(torch.device("cuda"))

    # Load Audio
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)

    CHUNK_DURATION = 30
    OVERLAP = 2
    chunk_ms = CHUNK_DURATION * 1000
    overlap_ms = OVERLAP * 1000

    segments = []
    segment_id = 0

    # Process chunks to save memory
    for i in range(0, len(audio), chunk_ms - overlap_ms):
        chunk = audio[i:i + chunk_ms]
        samples = chunk.get_array_of_samples()
        waveform = torch.tensor(samples).float().unsqueeze(0)

        diarization = pipeline({"waveform": waveform, "sample_rate": chunk.frame_rate})

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start = round(turn.start + i / 1000, 2)
            end = round(turn.end + i / 1000, 2)
            if end <= start: continue

            segments.append({
                "start": start,
                "end": end,
                "speaker_id": speaker
            })
            segment_id += 1

    # Identify Instructor (Longest speaker in first 3 mins)
    EARLY_WINDOW = 180
    speaker_durations = defaultdict(float)
    for seg in segments:
        if seg["start"] <= EARLY_WINDOW:
            speaker_durations[seg["speaker_id"]] += (seg["end"] - seg["start"])

    instructor_speaker = max(speaker_durations, key=speaker_durations.get) if speaker_durations else "UNKNOWN"

    # Assign Roles
    for seg in segments:
        seg["role"] = "Instructor" if seg["speaker_id"] == instructor_speaker else "Student"

    # Save Output
    with open(output_path, "w") as f:
        json.dump(segments, f, indent=2)
    
    print(f"Diarization Complete. Instructor Speaker ID: {instructor_speaker}")
    return segments