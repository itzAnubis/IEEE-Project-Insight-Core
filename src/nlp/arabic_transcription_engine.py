import os
import json
import logging
import gc
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Generator, Tuple
from pathlib import Path

import numpy as np
import soundfile as sf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ArabicTranscriptionOutput:
    audio_file: str
    language: str
    chunk_duration_sec: int
    chunks: List[Dict[str, Any]]
    full_transcript: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio_file": self.audio_file,
            "language": self.language,
            "chunk_duration_sec": self.chunk_duration_sec,
            "chunks": self.chunks,
            "full_transcript": self.full_transcript
        }

class ArabicTranscriptionEngine:
    MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    
    def __init__(self, model_size: str = "medium", device: str = "cpu", chunk_duration_sec: int = 20):
        self.model_size = model_size
        self.device = device
        self.chunk_duration_sec = chunk_duration_sec
        self.model = None
        self.backend = "unknown"

    def load_model(self):
        if self.model is not None: return
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(self.model_size, device=self.device, compute_type="int8")
            self.backend = "faster-whisper"
            logger.info(f"Loaded Faster-Whisper {self.model_size}")
        except ImportError:
            import whisper
            self.model = whisper.load_model(self.model_size, device=self.device)
            self.backend = "openai-whisper"
            logger.info(f"Loaded OpenAI Whisper {self.model_size}")

    def transcribe(self, audio_path: str, output_file: Optional[str] = None) -> ArabicTranscriptionOutput:
        self.load_model()
        
        # Load & Preprocess
        audio_data, sr = sf.read(audio_path)
        if len(audio_data.shape) > 1: audio_data = np.mean(audio_data, axis=1)
        
        # Chunking
        chunk_samples = int(self.chunk_duration_sec * sr)
        chunks_data = []
        full_text_parts = []
        
        for i, chunk_id in enumerate(range(0, len(audio_data), chunk_samples)):
            chunk = audio_data[chunk_id : chunk_id + chunk_samples]
            start_time = chunk_id / sr
            end_time = (chunk_id + len(chunk)) / sr
            
            # Transcribe
            segments, info = self.model.transcribe(
                chunk, language="ar", vad_filter=True, beam_size=5
            )
            
            text = " ".join([s.text.strip() for s in segments if s.text.strip()])
            chunks_data.append({
                "chunk_id": i,
                "start_time": round(start_time, 2),
                "end_time": round(end_time, 2),
                "text": text
            })
            if text: full_text_parts.append(text)

        result = ArabicTranscriptionOutput(
            audio_file=os.path.basename(audio_path),
            language="ar",
            chunk_duration_sec=self.chunk_duration_sec,
            chunks=chunks_data,
            full_transcript=" ".join(full_text_parts)
        )

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"Saved transcription to {output_file}")

        return result