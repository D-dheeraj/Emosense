import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.config import BASE_DIR, DEVICE
from app.database import engine, Base, get_db
from app.models import UserCheckIn, EmotionLog
from app.schemas import CheckInRequest, CheckInResponse, FrameAnalysisRequest, FrameAnalysisResponse, ChatRequest, ChatResponse

from app.ml.emotion_model import get_emotion_classifier
from app.ml.face_detector import get_face_detector
from app.ml.sentiment_analyzer import get_sentiment_analyzer

from app.agents.congruence_agent import get_congruence_agent
from app.agents.trend_scorer_agent import get_trend_scorer_agent
from app.agents.report_writer_agent import get_report_writer_agent
from app.agents.chatbot_agent import get_chatbot_agent

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EmoSense Production API",
    description="Multimodal Emotion & Wellness Assistant with PyTorch MPS Edge AI, Gemini 3-Way Congruence Agent, and AI Companion Chatbot",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files & HTML templates
static_dir = BASE_DIR / "app" / "static"
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = BASE_DIR / "app" / "templates"
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/")
def read_root(request: Request):
    """
    Renders the EmoSense Production Dashboard.
    """
    return templates.TemplateResponse("index.html", {"request": request, "device": str(DEVICE)})


@app.get("/api/system-status")
def get_system_status():
    """
    Returns edge AI hardware acceleration, database status, and multi-agent systems.
    """
    return {
        "status": "online",
        "device": str(DEVICE),
        "is_mps": str(DEVICE) == "mps",
        "framework": "PyTorch + FastAPI + OpenCV",
        "agents": [
            "3-Way Congruence Agent (Gemini API)",
            "Trend Scorer Agent",
            "Report Writer Agent",
            "AI Guidance Companion Chatbot"
        ]
    }


@app.post("/api/analyze-frame", response_model=FrameAnalysisResponse)
def analyze_frame(req: FrameAnalysisRequest):
    """
    Real-time webcam video stream evaluator.
    Decodes Base64 frame -> detects face via OpenCV -> PyTorch MPS CNN inference.
    """
    detector = get_face_detector()
    classifier = get_emotion_classifier()

    bgr_img = detector.decode_base64_image(req.image_base64)
    if bgr_img is None:
        raise HTTPException(status_code=400, detail="Invalid Base64 frame payload")

    cropped_face, bbox = detector.detect_and_crop_face(bgr_img)
    if cropped_face is None:
        return FrameAnalysisResponse(
            dominant_emotion="Neutral",
            confidence=0.5,
            probabilities={"Neutral": 1.0},
            face_detected=False,
            bounding_box=None
        )

    dominant_emotion, confidence, probabilities = classifier.predict(cropped_face)

    return FrameAnalysisResponse(
        dominant_emotion=dominant_emotion,
        confidence=round(confidence, 4),
        probabilities={k: round(v, 4) for k, v in probabilities.items()},
        face_detected=True,
        bounding_box=bbox
    )


@app.post("/api/checkin", response_model=CheckInResponse)
def create_checkin(req: CheckInRequest, db: Session = Depends(get_db)):
    """
    Full Multimodal Check-in Pipeline:
      1. Edge AI Visual Emotion Detection (PyTorch CNN)
      2. Micro-Journaling Text Sentiment Analysis (VADER)
      3. Self-Reported Emoji Integration
      4. Agent 1: 3-Way Congruence Triangulation (Gemini API)
      5. Agent 2: Trend Scorer (Historical Baseline)
      6. Agent 3: Report Writer & Micro-Intervention Selector
      7. Persistence in SQLite
    """
    detector = get_face_detector()
    classifier = get_emotion_classifier()
    sentiment_engine = get_sentiment_analyzer()

    congruence_agent = get_congruence_agent()
    trend_agent = get_trend_scorer_agent()
    report_agent = get_report_writer_agent()

    # 1. Visual Signal
    if req.image_base64:
        bgr_img = detector.decode_base64_image(req.image_base64)
        cropped_face, _ = detector.detect_and_crop_face(bgr_img)
        if cropped_face is not None:
            visual_emotion, visual_conf, probabilities = classifier.predict(cropped_face)
        else:
            visual_emotion, visual_conf, probabilities = "Neutral", 0.70, {"Neutral": 1.0}
    else:
        visual_emotion, visual_conf, probabilities = "Neutral", 0.70, {"Neutral": 1.0}

    # 2. Textual Signal
    text_sentiment, sentiment_score, _ = sentiment_engine.analyze(req.journal_text)

    # 3. Agent 1: 3-Way Congruence Reasoning
    congruence_res = congruence_agent.evaluate_congruence(
        visual_emotion=visual_emotion,
        visual_confidence=visual_conf,
        textual_sentiment=text_sentiment,
        sentiment_score=sentiment_score,
        journal_text=req.journal_text,
        self_reported_emoji=req.self_reported_emoji,
        self_reported_mood=req.self_reported_mood
    )

    congruence_score = congruence_res["congruence_score"]
    congruence_status = congruence_res["status"]
    is_masking = congruence_res["is_masking"]

    # 4. Agent 2: Trend Scoring
    trend_res = trend_agent.calculate_trend_metrics(
        db=db,
        current_congruence=congruence_score,
        current_sentiment=sentiment_score
    )

    stability_index = trend_res["stability_index"]
    trend_description = trend_res["trend_description"]

    # 5. Agent 3: Report & Intervention Synthesis
    report_res = report_agent.generate_report_and_intervention(
        visual_emotion=visual_emotion,
        textual_sentiment=text_sentiment,
        self_reported_mood=req.self_reported_mood,
        congruence_score=congruence_score,
        congruence_status=congruence_status,
        is_masking=is_masking,
        stability_index=stability_index
    )

    # 6. Database Persistence
    db_checkin = UserCheckIn(
        visual_emotion=visual_emotion,
        visual_confidence=round(visual_conf, 3),
        textual_sentiment=text_sentiment,
        sentiment_score=round(sentiment_score, 3),
        journal_text=req.journal_text,
        self_reported_emoji=req.self_reported_emoji,
        self_reported_mood=req.self_reported_mood,
        congruence_score=round(congruence_score, 1),
        congruence_status=congruence_status,
        is_emotional_masking=is_masking,
        stability_index=stability_index,
        trend_description=trend_description,
        wellness_summary=report_res["wellness_summary"],
        recommended_intervention=report_res["recommended_intervention"],
        intervention_details=report_res["intervention_details"]
    )

    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)

    db_log = EmotionLog(
        checkin_id=db_checkin.id,
        probabilities=probabilities,
        dominant_emotion=visual_emotion
    )
    db.add(db_log)
    db.commit()

    return db_checkin


@app.get("/api/history", response_model=List[CheckInResponse])
def get_history(limit: int = 15, db: Session = Depends(get_db)):
    """
    Returns historical check-in records for Chart.js trend visualization.
    """
    checkins = db.query(UserCheckIn)\
        .order_by(UserCheckIn.timestamp.asc())\
        .limit(limit)\
        .all()
    return checkins


@app.post("/api/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest):
    """
    AI Companion Chatbot Endpoint.
    Provides conversational guidance on check-ins, data privacy, and 4-7-8 breathing.
    """
    chatbot = get_chatbot_agent()
    reply = chatbot.respond(req.message)
    return ChatResponse(reply=reply)
