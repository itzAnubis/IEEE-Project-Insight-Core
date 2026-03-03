import librosa
import numpy as np
import json
from typing import Dict

class SpeechMetricsAnalyzer:
    def __init__(self, silence_threshold_db: float = -40, min_silence_duration: float = 0.5):
        self.silence_threshold_db = silence_threshold_db
        self.min_silence_duration = min_silence_duration

    def analyze_audio_chunk(self, audio_path: str, word_count: int = None) -> Dict:
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        wpm = self._calculate_wpm(duration, word_count) if word_count else None
        silence_metrics = self._detect_silence_gaps(y, sr)
        tone_metrics = self._analyze_tone_variance(y, sr)
        
        return {
            "duration_seconds": round(duration, 2),
            "wpm": wpm,
            "silence_analysis": silence_metrics,
            "tone_analysis": tone_metrics,
            "monotone_detected": tone_metrics["is_monotone"]
        }

    def _calculate_wpm(self, duration_seconds: float, word_count: int) -> float:
        if duration_seconds == 0: return 0.0
        return round((word_count / (duration_seconds / 60)), 2)

    def _detect_silence_gaps(self, y: np.ndarray, sr: int) -> Dict:
        hop_length = 512
        S = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        db = librosa.amplitude_to_db(S, ref=np.max)
        silent_frames = db < self.silence_threshold_db
        frame_duration = librosa.frames_to_time(1, sr=sr, hop_length=hop_length)
        
        silence_gaps = []
        in_silence = False
        silence_start = 0
        
        for i, is_silent in enumerate(silent_frames):
            if is_silent and not in_silence:
                silence_start = i * frame_duration
                in_silence = True
            elif not is_silent and in_silence:
                silence_duration = (i * frame_duration) - silence_start
                if silence_duration >= self.min_silence_duration:
                    silence_gaps.append({"start": round(silence_start, 2), "duration": round(silence_duration, 2)})
                in_silence = False
        
        total_silence = sum(gap["duration"] for gap in silence_gaps)
        silence_percentage = (total_silence / librosa.get_duration(y=y, sr=sr)) * 100
        
        return {
            "total_gaps": len(silence_gaps),
            "total_silence_seconds": round(total_silence, 2),
            "silence_percentage": round(silence_percentage, 2),
            "gaps": silence_gaps[:10]
        }

    def _analyze_tone_variance(self, y: np.ndarray, sr: int) -> Dict:
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=75, fmax=400)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0: pitch_values.append(pitch)
            
        if len(pitch_values) == 0:
            return {"pitch_mean_hz": 0, "pitch_std_hz": 0, "is_monotone": True}

        pitch_values = np.array(pitch_values)
        cv = (np.std(pitch_values) / np.mean(pitch_values)) if np.mean(pitch_values) > 0 else 0
        return {
            "pitch_mean_hz": round(float(np.mean(pitch_values)), 2),
            "pitch_std_hz": round(float(np.std(pitch_values)), 2),
            "coefficient_of_variation": round(float(cv), 3),
            "is_monotone": bool(cv < 0.15)
        }

def run_metrics(audio_path: str, word_count: int, output_file: str):
    analyzer = SpeechMetricsAnalyzer()
    results = analyzer.analyze_audio_chunk(audio_path, word_count)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Metrics saved to {output_file}")
    return results