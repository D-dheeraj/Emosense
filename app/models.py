import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from app.database import Base

class UserCheckIn(Base):
    __tablename__ = "user_checkins"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Input signals
    visual_emotion = Column(String(50), nullable=False)        # Top predicted visual expression
    visual_confidence = Column(Float, nullable=False)          # 0.0 to 1.0
    textual_sentiment = Column(String(50), nullable=False)       # Positive / Negative / Neutral
    sentiment_score = Column(Float, nullable=False)            # Compound score (-1.0 to +1.0)
    journal_text = Column(Text, nullable=True)                 # User's micro-journaling input
    self_reported_emoji = Column(String(20), nullable=False)    # e.g., "😊", "😔", "😐"
    self_reported_mood = Column(String(50), nullable=False)     # e.g., "Happy", "Sad", "Neutral"

    # Multi-Agent Reasoning Outputs
    congruence_score = Column(Float, nullable=False)           # 0.0 to 100.0%
    congruence_status = Column(String(50), nullable=False)      # "Congruent", "Mild Discrepancy", "Masked Distress"
    is_emotional_masking = Column(Boolean, default=False)      # True if facial expression masks true text/mood distress
    
    # Historical Trend & Baseline Metrics
    stability_index = Column(Float, default=100.0)             # Emotional stability score
    trend_description = Column(String(100), default="Stable")   # e.g. "Improving", "Declining", "Stable"

    # Report & Micro-Intervention
    wellness_summary = Column(Text, nullable=True)             # Plain language synthesis from Gemini Agent
    recommended_intervention = Column(String(100), nullable=True) # e.g. "4-7-8 Breathing", "Ambient Audio", "Reflective Journaling"
    intervention_details = Column(JSON, nullable=True)          # Structured details for frontend visualizer

class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    id = Column(Integer, primary_key=True, index=True)
    checkin_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Detailed 7-class emotion probabilities
    probabilities = Column(JSON, nullable=False) # {'Angry': 0.05, 'Happy': 0.85, ...}
    dominant_emotion = Column(String(50), nullable=False)

class InterventionLog(Base):
    __tablename__ = "intervention_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    intervention_type = Column(String(100), nullable=False)
    duration_seconds = Column(Integer, default=60)
    completed = Column(Boolean, default=True)
