import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class LectureSummarizer:
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if self.model: return
        print("Loading Summarization Model...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def summarize(self, transcript: str) -> str:
        self.load_model()
        
        prompt = f"""
You are an AI assistant that produces a clear Executive Summary.
Output Format:
EXECUTIVE SUMMARY:
- 5–10 bullet points.
KEY CONCEPTS:
- List main concepts.
Transcript:
{transcript}
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096).to("cuda")
        output = self.model.generate(**inputs, max_new_tokens=400, temperature=0.3)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

def run_summarization(transcript_text: str, output_file: str):
    summarizer = LectureSummarizer()
    summary_text = summarizer.summarize(transcript_text)
    
    result = {"summary": summary_text}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Summary saved to {output_file}")
    return result