# EmoSense: Multimodal Emotion & Wellness Assistant

EmoSense is a privacy-first, multimodal agentic AI platform combining deep learning visual emotion recognition (PyTorch CNN accelerated via Apple Silicon Mac M1 MPS GPU), text sentiment analysis, and multi-agent reasoning for wellness tracking and immediate interactive support.

---

## Key Features

- **Visual Emotion Recognition**: Custom PyTorch CNN (`EmoNet`) trained on FER2013 and accelerated locally on Mac M1 MPS GPU (`torch.device("mps")`) with OpenCV face detection.
- **Textual Sentiment Analysis**: Micro-journaling input analyzed for emotional tone via VADER sentiment scoring engine.
- **Self-Reported Mood Check-in**: One-tap emoji mood selector.
- **3-Way Congruence Agent (Google Gemini API)**: Triangulates visual, textual, and self-reported signals to detect **Emotional Masking** (e.g. smiling face with negative journal text).
- **Trend Scorer Agent**: Evaluates historical check-in time series (SQLAlchemy + SQLite) to calculate Emotional Stability Index (ESI) and prevent false alarms.
- **Report Writer & Micro-Intervention Agent**: Synthesizes plain-language wellness summaries and triggers real-time **Actionable Micro-Interventions** (4-7-8 Guided Breathing visualizer, ambient relaxation audio, reflective journaling prompts).
- **Glassmorphic Web Dashboard**: Modern cyber-health UI built with HTML5, CSS3 glassmorphism, Vanilla JS, and Chart.js.

---

## Hardware & Software Requirements

- Apple Mac M1 / M2 / M3 (macOS)
- Python 3.9+ / Python 3.10+
- PyTorch with MPS GPU acceleration
- OpenCV (`opencv-python`)
- FastAPI & Uvicorn
- SQLAlchemy & SQLite
- Google Gemini API (`google-genai` SDK)

---

## Quick Start Guide

### 1. Activate Virtual Environment
```bash
cd /Users/macbook/Desktop/Emosense
source venv/bin/activate
```

### 2. Configure Environment Variables (Optional for Gemini API)
```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_actual_key
```

### 3. Run FastAPI Development Server
```bash
./venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Open Dashboard in Web Browser
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in Safari or Chrome.

---

## Project Structure

```
Emosense/
├── app/
│   ├── main.py                  # FastAPI web server & API routes
│   ├── config.py                # Environment & Apple MPS device configuration
│   ├── database.py              # SQLAlchemy database setup & session
│   ├── models.py                # Database tables (UserCheckIn, EmotionLog)
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── ml/                      # Edge AI Machine Learning Engine
│   │   ├── emotion_model.py     # Custom PyTorch EmoNet CNN architecture
│   │   ├── face_detector.py     # OpenCV face detection & Base64 decoding
│   │   └── sentiment_analyzer.py# VADER micro-journal sentiment engine
│   ├── agents/                  # Multi-Agent Reasoning Core
│   │   ├── congruence_agent.py  # 3-Way Congruence Agent (Gemini API)
│   │   ├── trend_scorer_agent.py# Historical baseline & trend scoring agent
│   │   └── report_writer_agent.py# Wellness report & micro-intervention agent
│   ├── static/                  # Glassmorphic Frontend Assets
│   │   ├── css/styles.css       # Custom Glassmorphism design system
│   │   └── js/
│   │       ├── app.js           # Main UI logic & webcam frame evaluator
│   │       ├── breathing.js     # 4-7-8 Guided breathing visualizer
│   │       └── charts.js        # Chart.js historical trend rendering
│   └── templates/
│       └── index.html           # Main web dashboard template
├── models_weights/
│   └── fer2013_custom_cnn.pth   # Model weights file
├── requirements.txt
└── README.md
```

---

## 50% Milestone Demonstration Setup (Sept 24)

For the Sept 24 presentation:
1. Start server: `./venv/bin/uvicorn app.main:app --reload`.
2. Demonstrate Live Webcam feed with real-time face bounding box & PyTorch MPS emotion classification.
3. Show **Emotional Masking Detection**: Smile at the camera while typing "I feel completely hopeless and exhausted today."
4. Watch the 3-Way Congruence Agent flag **Masked Distress Alert!** in red, update the congruence gauge, and trigger the 4-7-8 Guided Breathing visualizer.
