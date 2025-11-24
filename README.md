# Project Insight-IEEE 👁️🧠

"From Feeling to Knowing": An AI-driven analytics platform that turns workshop engagement into actionable data.

## 📖 About The Project

Project Insight is a cross-disciplinary initiative by the AI, Robotics, and Web committees of IEEE PUA Student Branch. It uses Computer Vision and NLP to analyze workshops in real-time, providing instructors with feedback on audience engagement, speech clarity, and content delivery.

### Key Modules

-   **The Eyes (Vision):** Real-time face tracking, gaze estimation, and crowd counting.
-   **The Ears (NLP):** Local speech-to-text, speaker diarization, and LLM-based summarization.
-   **The Brain (Integration):** Correlates vision/audio data to evaluate instructor performance.
-   **The Body (Robotics):** An autonomous pan/tilt camera pod that tracks the speaker.

## 🛠️ Installation & Setup

We use Python 3.10. Please follow these steps exactly to avoid "it works on my machine" issues.

### 1. Prerequisites

-   Python 3.10 installed.
-   `uv` (Recommended) or standard `pip`.

### 2. Clone & Install

```bash
# 1. Clone the repo
git clone https://github.com/itzAnubis/IEEE-Project-Insight-Core.git
cd IEEE-Project-Insight-Core

# 2. Create Virtual Environment & Install Dependencies

# Option A: Using uv (Recommended & Fastest)
uv venv --python 3.10
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Option B: Standard Python
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the System

To start the "Director" script which launches the Vision, Audio, and Web modules:

```bash
python main.py
```

## 📂 Repository Structure

```
├── data/               # Local database & logs (Ignored by Git)
├── docs/               # Architecture explanations for new members
├── src/
│   ├── vision/         # YOLO & MediaPipe Logic
│   ├── nlp/            # Whisper & Ollama Logic
│   ├── robotics/       # Arduino Serial Comms
│   └── web/            # Dashboard Backend
└── main.py             # System Entry Point
```

## 🤝 Contributing

Please read `CONTRIBUTING.md` before pushing any code.
Direct pushes to `main` are blocked. You must submit a Pull Request.

## 🏗️ The Squads

-   **Vision Squad:** Led by Demiana Said
-   **NLP Squad:** Led by Mohamed Bakr
-   **Integration Squad:** Led by Alaa mohamed elfar
-   **QA Squad:** Led by Team Leads

**Managed by:** Ahmed Sherif

---

Copyright: IEEE PUA Student Branch © 2025
