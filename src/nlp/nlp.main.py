import os
import json
import logging
import torch

# Import the team's modules
from arabic_transcription_engine import ArabicTranscriptionEngine
from diarization import run_diarization
from speech_metrics import run_metrics
from qa_extractor import run_qa_extraction
from summarization import run_summarization

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    # CONFIGURATION
    AUDIO_FILE = "TOEFL_Listening_Practice_Test.wav"
    HF_TOKEN = os.environ.get("HF_TOKEN") # Ensure this is set in your environment
    
    # Output filenames for intermediate steps
    OUT_TRANSCRIPT = "step1_transcript.json"
    OUT_DIARIZATION = "step2_diarization.json"
    OUT_METRICS = "step3_metrics.json"
    OUT_QA = "step4_qa.json"
    OUT_SUMMARY = "step5_summary.json"
    FINAL_REPORT = "FINAL_PIPELINE_REPORT.json"

    if not os.path.exists(AUDIO_FILE):
        logger.error(f"Audio file {AUDIO_FILE} not found.")
        return

    report = {
        "audio_file": AUDIO_FILE,
        "steps_completed": []
    }

    # ========================================================================
    # STEP 1: TRANSCRIPTION (Ashraf)
    # ========================================================================
    logger.info("--- STEP 1: TRANSCRIPTION ---")
    try:
        transcriber = ArabicTranscriptionEngine(model_size="small", device="cpu")
        transcription_data = transcriber.transcribe(AUDIO_FILE, output_file=OUT_TRANSCRIPT)
        
        report["transcription"] = transcription_data.to_dict()
        report["steps_completed"].append("Transcription")
        
        transcript_text = transcription_data.full_transcript
        word_count = len(transcript_text.split())
        logger.info(f"Transcription done. Words: {word_count}")
    except Exception as e:
        logger.error(f"Step 1 Failed: {e}")
        return

    # ========================================================================
    # STEP 2: DIARIZATION (Nada)
    # ========================================================================
    logger.info("--- STEP 2: DIARIZATION ---")
    try:
        diarization_data = run_diarization(AUDIO_FILE, HF_TOKEN, output_path=OUT_DIARIZATION)
        report["diarization_stats"] = {
            "total_segments": len(diarization_data),
            "sample_segment": diarization_data[0] if diarization_data else None
        }
        report["steps_completed"].append("Diarization")
    except Exception as e:
        logger.error(f"Step 2 Failed: {e}")
        diarization_data = [] # Continue without diarization if it fails

    # ========================================================================
    # STEP 3: METRICS (Farah)
    # ========================================================================
    logger.info("--- STEP 3: METRICS ---")
    try:
        metrics_data = run_metrics(AUDIO_FILE, word_count, OUT_METRICS)
        report["metrics"] = metrics_data
        report["steps_completed"].append("Metrics")
    except Exception as e:
        logger.error(f"Step 3 Failed: {e}")

    # ========================================================================
    # STEP 4: QA EXTRACTION (Youmna)
    # ========================================================================
    logger.info("--- STEP 4: QA EXTRACTION ---")
    try:
        qa_data = run_qa_extraction(AUDIO_FILE, diarization_data, OUT_QA)
        report["qa_extraction"] = qa_data
        report["steps_completed"].append("QA Extraction")
    except Exception as e:
        logger.error(f"Step 4 Failed: {e}")

    # ========================================================================
    # STEP 5: SUMMARIZATION (Shimaa)
    # ========================================================================
    logger.info("--- STEP 5: SUMMARIZATION ---")
    try:
        summary_data = run_summarization(transcript_text, OUT_SUMMARY)
        report["summary"] = summary_data
        report["steps_completed"].append("Summarization")
    except Exception as e:
        logger.error(f"Step 5 Failed (Likely GPU OOM): {e}")
        report["summary"] = "Skipped due to error."

    # ========================================================================
    # FINAL SAVE
    # ========================================================================
    with open(FINAL_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"PIPELINE FINISHED. Final report saved to {FINAL_REPORT}")

if __name__ == "__main__":
    # Safe globals for PyAnnote
    try:
        from omegaconf.listconfig import ListConfig
        from omegaconf.base import ContainerMetadata
        torch.serialization.add_safe_globals([ListConfig, ContainerMetadata])
    except ImportError:
        pass
        
    main()