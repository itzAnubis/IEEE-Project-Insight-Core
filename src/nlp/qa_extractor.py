import json
import re
import os
from dataclasses import dataclass, asdict
from typing import List, Optional
import numpy as np
import soundfile as sf
import librosa

try:
    from faster_whisper import WhisperModel
except Exception:
    print("faster-whisper not installed. pip install faster-whisper")

QUESTION_RE = re.compile(r"\b(who|what|when|where|why|how|which|whom|whose|do|does|did)\b", flags=re.IGNORECASE)

@dataclass
class QuestionHit:
    text: str
    start: float
    end: float
    speaker: Optional[str] # "Instructor" or "Student"
    confidence: float

def align_speaker(start, end, diarization_segments):
    """Finds who is speaking based on Nada's output."""
    if not diarization_segments: return None
    best_speaker = None
    max_overlap = 0.0
    
    for d in diarization_segments:
        overlap_start = max(start, d["start"])
        overlap_end = min(end, d["end"])
        overlap = max(0, overlap_end - overlap_start)
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_speaker = d.get("role") # Use the role (Instructor/Student) assigned by Nada
            
    return best_speaker

def run_qa_extraction(audio_path: str, diarization_data: List[dict], output_file: str):
    """
    Extracts questions and tags speakers using pre-calculated diarization.
    """
    print(f"Running QA Extraction for {audio_path}...")
    model = WhisperModel("small", device="cpu", compute_type="float32")
    segments, _ = model.transcribe(audio_path, beam_size=5, word_timestamps=True)
    
    hits = []
    # Load audio for pitch analysis
    y, sr = librosa.load(audio_path, sr=16000)

    for seg in segments:
        text = seg.text.strip()
        if not text: continue
        
        # Heuristics
        is_question = ("?" in text) or (QUESTION_RE.search(text))
        
        if is_question:
            # Pitch Check
            s_idx = int(max(0, (seg.start - 0.15) * sr))
            e_idx = int(min(len(y), (seg.end + 0.15) * sr))
            # Simplified pitch check (omitted full logic for brevity, assuming text heuristic is primary)
            
            # Speaker Alignment
            speaker_role = align_speaker(seg.start, seg.end, diarization_data)
            
            hits.append(asdict(QuestionHit(
                text=text,
                start=round(seg.start, 2),
                end=round(seg.end, 2),
                speaker=speaker_role,
                confidence=0.8
            )))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hits, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(hits)} questions.")
    return hits