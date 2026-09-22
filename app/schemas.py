from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import datetime

class CheckInRequest(BaseModel):
    image_base64: Optional[str] = Field(None, description="Base64 encoded JPEG/PNG frame from webcam")
    journal_text: Optional[str] = Field("", description="Micro-journaling user input")
    self_reported_emoji: str = Field("😐", description="Emoji selected during check-in")
    self_reported_mood: str = Field("Neutral", description="Mood name matching emoji")

class FrameAnalysisRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 frame for real-time video evaluation")

class CheckInResponse(BaseModel):
    id: int
    timestamp: datetime.datetime
    visual_emotion: str
    visual_confidence: float
    textual_sentiment: str
    sentiment_score: float
    self_reported_emoji: str
    self_reported_mood: str
    congruence_score: float
    congruence_status: str
    is_emotional_masking: bool
    stability_index: float
    trend_description: str
    wellness_summary: str
    recommended_intervention: str
    intervention_details: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class FrameAnalysisResponse(BaseModel):
    dominant_emotion: str
    confidence: float
    probabilities: Dict[str, float]
    face_detected: bool
    bounding_box: Optional[Dict[str, int]] = None

class ChatRequest(BaseModel):
    message: str = Field(..., description="User query message to the AI Companion Chatbot")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI Companion response")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
