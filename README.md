# EmoSense: Multimodal Emotion & Wellness Assistant

**EmoSense** is a privacy-first, multimodal agentic AI platform combining deep learning visual emotion recognition (PyTorch CNN accelerated via Apple Silicon Mac M1 MPS GPU), text sentiment analysis, and multi-agent reasoning for wellness tracking, emotional masking detection, and real-time interactive support.

---

## 🌟 Key Features

- **Visual Emotion Recognition**: Custom PyTorch CNN (`EmoNet`) trained on FER2013 and accelerated locally on Mac M1 MPS GPU (`torch.device("mps")`) with OpenCV face detection.
- **Textual Sentiment Analysis**: Micro-journaling input analyzed for emotional tone via VADER sentiment scoring engine.
- **Self-Reported Mood Check-in**: One-tap emoji mood selector.
- **3-Way Congruence Agent (Google Gemini API)**: Triangulates visual, textual, and self-reported signals to detect **Emotional Masking** (e.g. smiling face with negative journal text).
- **Trend Scorer Agent**: Evaluates historical check-in time series (SQLAlchemy + SQLite) to calculate Emotional Stability Index (ESI) and prevent false alarms.
- **Report Writer Agent**: Synthesizes plain-language wellness summaries and triggers real-time **Actionable Micro-Interventions** (4-7-8 Guided Breathing visualizer, 432Hz Ambient Relaxation Audio, reflective journaling prompts).
- **Universal Multilingual AI Companion Chatbot**: Floating AI Assistant Widget powered by Google Gemini API for instant conversational guidance on app usage, data privacy, and 4-7-8 breathing techniques in Hindi, Hinglish, English, or any language.
- **Glassmorphic Multi-Tab Dashboard**: Modern cyber-health UI with tabbed navigation (**Live Check-In**, **Trend Analytics**, **Micro-Interventions**, **Data Privacy Center**).

---

## 📂 Updated Project Structure

```
Emosense/
├── app/
│   ├── main.py                  # FastAPI web server, REST routes & API endpoints
│   ├── config.py                # Environment & Apple MPS device configuration
│   ├── database.py              # SQLAlchemy database setup & session generator
│   ├── models.py                # Database models (UserCheckIn, EmotionLog, InterventionLog)
│   ├── schemas.py               # Pydantic request/response validation schemas
│   ├── ml/                      # Edge AI Machine Learning Engine
│   │   ├── __init__.py
│   │   ├── emotion_model.py     # Custom PyTorch EmoNet CNN architecture
│   │   ├── train_fer2013.py     # PyTorch FER2013 dataset training script (Mac M1 MPS)
│   │   ├── face_detector.py     # OpenCV face detection & Base64 image decoding
│   │   └── sentiment_analyzer.py# VADER micro-journal sentiment engine
│   ├── agents/                  # Multimodal Agentic AI Core
│   │   ├── __init__.py
│   │   ├── congruence_agent.py  # 3-Way Congruence Agent (Gemini API)
│   │   ├── trend_scorer_agent.py# Historical baseline & trend scoring agent
│   │   ├── report_writer_agent.py# Wellness report & micro-intervention agent
│   │   └── chatbot_agent.py     # Universal Multilingual AI Assistant Chatbot (Gemini API)
│   ├── static/                  # Glassmorphic Frontend Assets
│   │   ├── css/
│   │   │   └── styles.css       # Custom Glassmorphism design system & widget styles
│   │   └── js/
│   │       ├── app.js           # Main UI logic, tab manager & AI chatbot controller
│   │       ├── breathing.js     # 4-7-8 Guided breathing interactive visualizer
│   │       └── charts.js        # Chart.js historical trend analytics
│   └── templates/
│       └── index.html           # Multi-tab web dashboard & AI chatbot template
├── models_weights/
│   └── fer2013_custom_cnn.pth   # Trained PyTorch CNN model weights (62.54% Val Acc)
├── dataset/                     # FER2013 Dataset directory (train & test folders)
│   ├── train/
│   └── test/
├── requirements.txt             # Python project dependencies
├── .env.example                 # Environment variables configuration template
├── .gitignore                   # Git exclusion rules
└── README.md                    # Project documentation & execution guide
```

---

## 🛠️ Hardware & Software Requirements

- Apple Mac M1 / M2 / M3 (macOS)
- Python 3.9+ / Python 3.10+
- PyTorch with MPS GPU acceleration
- OpenCV (`opencv-python`)
- FastAPI & Uvicorn
- SQLAlchemy & SQLite
- Google Gemini API (`google-genai` SDK)

---

## 🚀 Quick Start & Manual Execution

### 1. Activate Virtual Environment
```bash
cd /Users/macbook/Desktop/Emosense
source venv/bin/activate
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
# Set your GEMINI_API_KEY in .env
```

### 3. Run PyTorch Model Training (Optional - Pre-trained weights included)
```bash
python app/ml/train_fer2013.py
```

### 4. Run FastAPI Web Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Open Dashboard in Web Browser
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in Safari or Chrome.

---

## 👥 Student & Guide Details

- **Student Name**: Dheeraj Kumar Singh (Roll No: MCA/40044/25, Section B)
- **Guide Name**: Dr. Partha Sarthi Bishnu
- **Course**: MCA III CA550-Project (MO 2026)
