import os
import json
from typing import Dict, Any
from app.config import GEMINI_API_KEY

class ThreeWayCongruenceAgent:
    """
    Agent 1: 3-Way Congruence Agent (Google Gemini API).
    Triangulates 3 complementary signals:
      1. Visual Emotion (PyTorch CNN on face frame)
      2. Textual Sentiment (Micro-journaling text)
      3. Self-Reported Mood (Selected Emoji)

    Detects Emotional Masking (e.g. smiling face masking negative internal state).
    Includes failsafe heuristic engine so network/API errors never break check-in.
    """
    def __init__(self):
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[CongruenceAgent] Gemini API Client initialized successfully.")
            except Exception as e:
                print(f"[CongruenceAgent] Failed to init Gemini API client: {e}")

    def evaluate_congruence(
        self,
        visual_emotion: str,
        visual_confidence: float,
        textual_sentiment: str,
        sentiment_score: float,
        journal_text: str,
        self_reported_emoji: str,
        self_reported_mood: str
    ) -> Dict[str, Any]:
        """
        Runs Gemini API 3-Way Congruence Check.
        Returns dict containing:
          - congruence_score: float (0.0 to 100.0)
          - status: "Congruent" | "Mild Discrepancy" | "Masked Distress"
          - is_masking: bool
          - explanation: str
        """
        # Attempt Gemini LLM reasoning if client is available
        if self.client:
            try:
                prompt = f"""
You are the 3-Way Congruence Agent for EmoSense wellness assistant.
Analyze these 3 user check-in signals for alignment and emotional masking:

1. Visual Facial Emotion (from PyTorch CNN): {visual_emotion} (confidence: {visual_confidence:.2f})
2. Textual Journal Sentiment: {textual_sentiment} (compound score: {sentiment_score:.2f})
   Journal Text: "{journal_text}"
3. Self-Reported Mood: {self_reported_emoji} ({self_reported_mood})

Instructions:
- Evaluate whether the facial expression, journal text tone, and self-reported mood match.
- Emotional Masking occurs when the user exhibits a positive facial expression (e.g. Happy/Smiling) or positive emoji, but their journal text reveals distress, sadness, anxiety, or helplessness.
- Output ONLY valid JSON in this exact structure:
{{
  "congruence_score": <number between 0 and 100>,
  "status": "<Congruent | Mild Discrepancy | Masked Distress>",
  "is_masking": <true or false>,
  "explanation": "<2-sentence explanation of signal alignment>"
}}
"""
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                text_out = response.text.strip()
                if "```json" in text_out:
                    text_out = text_out.split("```json")[1].split("```")[0].strip()
                elif "```" in text_out:
                    text_out = text_out.split("```")[1].split("```")[0].strip()

                result = json.loads(text_out)
                return {
                    "congruence_score": float(result.get("congruence_score", 85.0)),
                    "status": str(result.get("status", "Congruent")),
                    "is_masking": bool(result.get("is_masking", False)),
                    "explanation": str(result.get("explanation", "Signals analyzed via Gemini API."))
                }
            except Exception as e:
                print(f"[CongruenceAgent] Gemini API call exception ({e}), activating heuristic fallback.")

        # Guaranteed Heuristic Engine Fallback
        return self._heuristic_congruence(
            visual_emotion, textual_sentiment, sentiment_score, self_reported_mood, journal_text
        )

    def _classify_signal(self, kind: str, value: str, sentiment_score: float = None, journal_lower: str = "") -> str:
        """
        Buckets any one of the 3 signals into 'positive' | 'negative' | 'neutral'
        so all three can be compared on the same scale.
        """
        if kind == "visual":
            if value in ['Happy', 'Surprise']:
                return "positive"
            if value in ['Sad', 'Angry', 'Fear', 'Disgust']:
                return "negative"
            return "neutral"  # Neutral

        if kind == "text":
            negative_kw = any(w in journal_lower for w in [
                'sad', 'hopeless', 'tired', 'depressed', 'overwhelmed', 'bad', 'hate', 'pain', 'fail', 'upset'
            ])
            if (sentiment_score is not None and sentiment_score <= -0.15) or value == "Negative" or negative_kw:
                return "negative"
            if (sentiment_score is not None and sentiment_score >= 0.15) or value == "Positive":
                return "positive"
            return "neutral"

        if kind == "mood":
            if value in ['Happy', 'Joyful', 'Excited', 'Good', 'Calm']:
                return "positive"
            if value in ['Sad', 'Angry', 'Anxious', 'Stressed', 'Overwhelmed', 'Tired']:
                return "negative"
            return "neutral"  # Neutral

        return "neutral"

    def _heuristic_congruence(
        self,
        visual_emotion: str,
        textual_sentiment: str,
        sentiment_score: float,
        self_reported_mood: str,
        journal_text: str
    ) -> Dict[str, Any]:
        """
        Rule-based fallback calculation when offline or without Gemini API key.
        Compares all THREE signals (visual, text, self-reported mood) against each
        other, rather than only visual+text, so a mismatched emoji is never silently
        ignored.
        """
        journal_lower = (journal_text or "").lower()

        vis_bucket = self._classify_signal("visual", visual_emotion)
        text_bucket = self._classify_signal("text", textual_sentiment, sentiment_score, journal_lower)
        mood_bucket = self._classify_signal("mood", self_reported_mood)

        # 1. Emotional Masking: text reveals distress while an OUTWARD signal
        #    (face or self-reported mood) looks positive. This check has priority
        #    over the general agreement check below, because masking is the
        #    specific pattern this app exists to catch.
        if text_bucket == "negative" and (vis_bucket == "positive" or mood_bucket == "positive"):
            score = 35.0
            status = "Masked Distress"
            is_masking = True
            explanation = (
                "Detected Emotional Masking: an outward signal (facial expression or self-reported mood) "
                "appears positive, but the journal entry reveals underlying emotional distress."
            )
            return {"congruence_score": score, "status": status, "is_masking": is_masking, "explanation": explanation}

        buckets = [vis_bucket, text_bucket, mood_bucket]
        distinct = set(buckets)

        # 2. All three signals agree -> genuinely congruent
        if len(distinct) == 1:
            score = 92.0
            status = "Congruent"
            explanation = "High congruence: visual expression, journal tone, and self-reported mood all align."

        # 3. Exactly two of three agree -> mild discrepancy
        elif len(distinct) == 2:
            score = 65.0
            status = "Mild Discrepancy"
            explanation = (
                f"Mild variance observed: one signal (visual={visual_emotion}, "
                f"text={textual_sentiment}, mood={self_reported_mood}) doesn't match the other two."
            )

        # 4. All three signals disagree -> stronger discrepancy, but not masking
        #    (masking case was already handled above)
        else:
            score = 48.0
            status = "Mild Discrepancy"
            explanation = (
                f"Notable discrepancy: visual ({visual_emotion}), text ({textual_sentiment}), and "
                f"self-reported mood ({self_reported_mood}) all point in different directions."
            )

        return {"congruence_score": score, "status": status, "is_masking": False, "explanation": explanation}


_congruence_agent = None

def get_congruence_agent() -> ThreeWayCongruenceAgent:
    global _congruence_agent
    if _congruence_agent is None:
        _congruence_agent = ThreeWayCongruenceAgent()
    return _congruence_agent