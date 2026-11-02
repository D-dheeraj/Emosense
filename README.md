# EmoSense: Multimodal Emotion & Wellness Assistant

<p align="center">
  <img src="report_assets/fig3_1_architecture.png" alt="EmoSense Architecture Banner" width="850"/>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.8_MPS_GPU-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch MPS"/></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini"/></a>
  <a href="https://www.bitmesra.ac.in/"><img src="https://img.shields.io/badge/BIT_Mesra-MCA_CA550-991b1b?style=for-the-badge" alt="BIT Mesra"/></a>
  <img src="https://img.shields.io/badge/Status-Completed_%26_Deployed-success?style=for-the-badge" alt="Status"/>
</p>

---

## 📌 Executive Summary

**EmoSense** is a privacy-first, multimodal agentic AI platform designed to overcome the critical diagnostic vulnerability of **Emotional Masking** (commonly known in clinical psychology as *"smiling depression"*). 

Traditional affective computing systems rely on single-channel (unimodal) computer vision or isolated survey trackers. When an individual masks severe internal burnout or depression behind a reflexive smile or positive emoji, unimodal systems output false-negative "Happy" assessments. 

EmoSense solves this by capturing three orthogonal, complementary sensory streams during every check-in:
1. **Visual Facial Affect**: 100% on-device edge computer vision using a custom 4-block PyTorch CNN (`EmoNet`) accelerated via Apple Silicon Metal Performance Shaders (MPS GPU).
2. **Textual Sentiment & Linguistic Tone**: Unconstrained micro-journaling diary reflections scored via the VADER sentiment engine.
3. **Self-Reported Mood State**: Categorical one-tap emoji check-in interface.

These streams are triangulated in real time by an **Agentic AI Core (Google Gemini 2.5 Flash)** to identify contradictions, compute a quantitative **Congruence Score (0–100%)**, evaluate longitudinal stability against historical baselines, and deliver immediate evidence-based somatic relief (interactive **4-7-8 Guided Breathing** visualizer and **432Hz Ambient Harmonic Soundscapes**).

---

## 🧠 The Emotional Masking Dilemma & 3-Way Triangulation

<p align="center">
  <img src="report_assets/fig1_1_emotional_masking.png" alt="Emotional Masking Triangulation" width="750"/>
</p>

In professional or high-stress environments, individuals routinely conceal emotional exhaustion behind outward cheerfulness. As illustrated above:
- **Visual Stream**: Facial feature geometry registers a smiling mouth curve $\rightarrow$ traditional FER classifies as `Happy` ($P = 0.78$).
- **Linguistic Stream**: Micro-journal entry *"I feel completely hopeless and exhausted today"* $\rightarrow$ VADER sentiment scores strongly negative ($-0.74$).
- **Self-Reported Mood**: User selects `Sad` emoji.
- **The Triangulation Outcome**: Rather than averaging contradictory signals or trusting the superficial smile, the **3-Way Congruence Agent** identifies the divergence, generates an urgent **Masked Distress Alert (Congruence Score: 38%)**, and immediately initiates calming micro-interventions.

---

## ✨ Core Features & Architectural Highlights

### 🛡️ 1. Privacy-First Edge AI (Zero Biometric Leakage)
- Raw webcam frames are processed **100% locally in workstation memory** using PyTorch and OpenCV.
- No video feeds or biometric facial coordinates are ever transmitted over the network or uploaded to cloud storage, strictly complying with **GDPR**, **HIPAA**, and **DPDP** regulations.
- Hardware auto-detection dynamically leverages Apple Silicon Mac M1/M2/M3 **MPS GPU**, NVIDIA **CUDA**, or optimized **CPU fallback**.

### 🤖 2. Multi-Agent Cognitive Orchestration
- **3-Way Congruence Agent**: Evaluates visual probabilities, VADER sentiment polarity, and emoji selection via Google Gemini API (`gemini-2.5-flash`) with structured JSON schema outputs. Includes an offline rule-based heuristic fallback.
- **Trend Scorer Agent**: Ingests rolling 15-entry historical check-in time series stored in local SQLite (`emosense.db`) to compute an **Emotional Stability Index (ESI)**, distinguishing chronic distress from transient bad days.
- **Report Writer Agent**: Formulates compassionate, clinical-grade wellness summaries and prescribes actionable recovery micro-interventions.
- **Universal Multilingual AI Companion Chatbot**: Floating conversational assistant providing real-time guidance on app usage, data privacy, mental wellness, and breathing protocols in **Hindi**, **Hinglish**, and **English**.

### 🫁 3. Real-Time Actionable Somatic Interventions
- **4-7-8 Guided Breathing Visualizer**: Interactive SVG animated expanding/contracting sphere synchronizing parasympathetic nervous system regulation:
  - *Inhale*: 4 seconds (Nasal)
  - *Hold*: 7 seconds (Vagal nerve activation)
  - *Exhale*: 8 seconds (Oral release)
- **432Hz Ambient Harmonic Generator**: Synthesizes calming binaural harmonic sound waves directly in-browser using the HTML5 Web Audio API to reduce acute cortisol levels.

### 📊 4. Cyber-Health Glassmorphic Web Dashboard
- Multi-tab cyber-health interface built with modern Glassmorphism, CSS backdrop filters, and responsive design:
  - 🖥️ **Live Check-In**: Real-time webcam preview, emotion distribution bars, journal pad, and instant congruence scanner.
  - 📈 **Trend Analytics**: Interactive Chart.js graphs mapping Emotional Stability Index and check-in timeline.
  - 🧘 **Micro-Interventions**: Standalone 4-7-8 breathing pacer, ambient relaxation audio, and self-reflection prompts.
  - 🔒 **Data Privacy Center**: Transparent audit of edge processing, local database status, and active hardware compute device.

---

## 🔬 Deep Learning Model: `EmoNet`

The visual engine employs a custom deep Convolutional Neural Network (`EmoNet`) tailored for 48×48 single-channel facial grayscale inputs, trained and evaluated on the **FER2013 benchmark dataset** (35,887 images across 7 classes).

<p align="center">
  <img src="report_assets/fig4_1_cnn_layers.png" alt="PyTorch EmoNet CNN Layer Architecture" width="750"/>
</p>

### CNN Layer Dimensions & Hyperparameters

| Block / Layer | Type | Kernel / Filters | Output Dimension | Regularization & Activation |
|:---|:---|:---|:---:|:---|
| **Input** | Grayscale Tensor | 1 channel | $(B, 1, 48, 48)$ | Min-Max Normalized $[-1, +1]$ |
| **Block 1** | Dual Conv2D + Pool | $32 \rightarrow 64$ filters ($3\times3$) | $(B, 64, 24, 24)$ | BatchNorm, ReLU, MaxPool ($2\times2$), Dropout ($p=0.25$) |
| **Block 2** | Dual Conv2D + Pool | $128$ filters ($3\times3$) | $(B, 128, 12, 12)$ | BatchNorm, ReLU, MaxPool ($2\times2$), Dropout ($p=0.25$) |
| **Block 3** | Dual Conv2D + Pool | $256$ filters ($3\times3$) | $(B, 256, 6, 6)$ | BatchNorm, ReLU, MaxPool ($2\times2$), Dropout ($p=0.25$) |
| **Dense FC1** | Fully Connected | $9,216 \rightarrow 512$ | $(B, 512)$ | BatchNorm, ReLU, Dropout ($p=0.50$) |
| **Dense FC2** | Output Classification | $512 \rightarrow 7$ | $(B, 7)$ | Linear Logits $\rightarrow$ Softmax |

---

## 📈 Experimental Results & Performance Benchmarks

### Training Progression on Apple Silicon Mac M1 MPS GPU
Trained over 10 epochs using Adam optimizer ($\text{lr} = 10^{-3}$, batch size $= 64$, L2 weight decay $= 10^{-4}$), achieving **62.54% validation accuracy** and loss convergence to $1.0088$.

<p align="center">
  <img src="report_assets/fig5_2_training_curves.png" alt="Training and Validation Progression Curves" width="750"/>
</p>

### Hardware Inference Latency Benchmark

<p align="center">
  <img src="report_assets/fig5_3_latency_benchmark.png" alt="Inference Latency Benchmark" width="750"/>
</p>

| Platform | Compute Device | Inference Latency | Frame Rate (FPS) | Biometric Privacy Guarantee |
|:---|:---|:---:|:---:|:---|
| **Apple Silicon Mac M1** | **PyTorch MPS GPU** | **14.8 ms** | **67.5 FPS** | 🟢 **100% On-Device RAM (Zero Cloud Leakage)** |
| **Apple Silicon Mac M1** | PyTorch CPU | 42.1 ms | 23.8 FPS | 🟢 100% On-Device RAM |
| **Intel Core i7 11th Gen** | PyTorch CPU | 58.6 ms | 17.1 FPS | 🟢 100% On-Device RAM |
| **Cloud Computer Vision APIs** | Remote HTTPS REST | 385.0 ms | 2.6 FPS | 🔴 High Risk (Webcam frames sent to cloud) |

---

## 📂 Repository Directory Structure

```
Emosense/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI server, REST API endpoints & lifecycle hooks
│   ├── config.py                # Hardware detection, paths, & environment settings
│   ├── database.py              # SQLAlchemy engine & session dependency injection
│   ├── models.py                # Relational ORM models (UserCheckIn, EmotionLog, InterventionLog)
│   ├── schemas.py               # Pydantic validation schemas (CheckIn, FrameAnalysis, Chat)
│   ├── ml/                      # Edge AI Computer Vision & NLP Subsystem
│   │   ├── __init__.py
│   │   ├── emotion_model.py     # Custom PyTorch EmoNet CNN architecture & inference
│   │   ├── train_fer2013.py     # FER2013 training script (Mac M1 MPS GPU accelerated)
│   │   ├── face_detector.py     # OpenCV Haar Cascade localization & Base64 decoding
│   │   └── sentiment_analyzer.py# VADER micro-journal sentiment engine
│   ├── agents/                  # Cognitive Multi-Agent AI Subsystem
│   │   ├── __init__.py
│   │   ├── congruence_agent.py  # 3-Way Congruence Agent (Gemini API & heuristics)
│   │   ├── trend_scorer_agent.py# ESI baseline calculation & historical trend scoring
│   │   ├── report_writer_agent.py# Wellness report generator & micro-interventions
│   │   └── chatbot_agent.py     # Multilingual conversational AI companion (Hindi/Hinglish/Eng)
│   ├── static/                  # Glassmorphic Frontend Client
│   │   ├── css/
│   │   │   └── styles.css       # Custom Glassmorphism cyber-health design system
│   │   └── js/
│   │       ├── app.js           # Core UI controller, webcam stream, & tab manager
│   │       ├── breathing.js     # 4-7-8 Guided breathing animated visualizer
│   │       └── charts.js        # Chart.js historical trend rendering
│   └── templates/
│       └── index.html           # Multi-tab responsive single-page web application
├── models_weights/
│   └── fer2013_custom_cnn.pth   # Pre-trained PyTorch CNN model weights (62.54% Val Acc)
├── report_assets/               # High-resolution architectural diagrams & benchmark charts
│   ├── fig1_1_emotional_masking.png
│   ├── fig3_1_architecture.png
│   ├── fig4_1_cnn_layers.png
│   ├── fig5_2_training_curves.png
│   └── fig5_3_latency_benchmark.png
├── BIT_Mesra_EmoSense_Project_Report.md  # Official BIT Mesra Academic Report source
├── BIT_Mesra_EmoSense_Project_Report.pdf # Final publication-grade 22-page academic report
├── build_bit_mesra_perfect_report.py    # ReportLab multi-pass PDF compiler with exact TOC mapping
├── generate_report_figures.py           # Offline PIL generator for high-res diagrams
├── generate_pdf_doc.py                  # Standalone technical documentation generator
├── requirements.txt                     # Pinned project dependencies
├── .env.example                         # Environment variable configuration template
├── .gitignore                           # Git exclusion rules
└── README.md                            # Comprehensive project documentation
```

---

## 📡 RESTful API Endpoints

| Endpoint | Method | Request Payload | Description |
|:---|:---:|:---|:---|
| `/api/system-status` | `GET` | *None* | Returns active hardware compute engine (`mps`, `cuda`, or `cpu`). |
| `/api/analyze-frame` | `POST` | `{"frame": "<Base64 JPEG>"}` | Performs real-time face detection & returns 7-class emotion probabilities. |
| `/api/checkin` | `POST` | `{"image_data": "...", "journal_text": "...", "self_reported_mood": "..."}` | Executes 3-way triangulation, triggers Gemini Congruence Agent, and logs check-in. |
| `/api/history` | `GET` | Query param `limit` (default: 15) | Retrieves longitudinal check-in records for Chart.js trend rendering. |
| `/api/chat` | `POST` | `{"message": "<User Query>"}` | Conversational AI companion endpoint with bilingual conversational routing. |

---

## 🚀 Quick Start & Installation Guide

### Prerequisites
- Python 3.9, 3.10, or 3.11 installed.
- macOS (Apple Silicon M1/M2/M3 recommended for MPS acceleration) or Linux/Windows with CUDA/CPU.
- Google Gemini API key (Free tier available at [Google AI Studio](https://aistudio.google.com/)).

### 1. Clone the Repository
```bash
git clone https://github.com/D-dheeraj/Emosense.git
cd Emosense
```

### 2. Create and Activate Virtual Environment
```bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file from the provided template:
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_gemini_api_key_here"
DATABASE_URL="sqlite:///./emosense.db"
```
*(Note: If no API key is provided, EmoSense seamlessly falls back to its built-in rule-based heuristic triangulation engine and local conversational synthesizer).*

### 5. Launch the Application
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Access the Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🎓 Academic Credentials & Institutional Attribution

This project was developed as a Capstone Final Project in partial fulfillment of the requirements for the award of the Degree of **Master of Computer Applications (MCA)** at **Birla Institute of Technology (BIT), Mesra, Ranchi**.

- **Candidate**: **Dheeraj Kumar Singh**
- **Roll Number**: **MCA/40044/25** (Section B)
- **Academic Session**: 2024 – 2026
- **Project Supervisor / Guide**: **Dr. Partha Sarthi Bishnu**
- **Department**: Department of Computer Science & Engineering / Computer Applications
- **Institution**: Birla Institute of Technology, Mesra – 835215, Ranchi, Jharkhand, India
- **Course Code**: CA550 Small Industrial Training / Small Project / MOOC

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free for educational, academic, and non-commercial research use.
