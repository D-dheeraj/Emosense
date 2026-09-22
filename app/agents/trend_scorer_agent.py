from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import UserCheckIn

class TrendScorerAgent:
    """
    Agent 2: Historical Trend Scorer Agent.
    Evaluates past check-ins from SQLite database to calculate Emotional Stability Index (ESI),
    prevent false alarms on isolated bad days, and detect long-term emotional trajectories.
    """

    def calculate_trend_metrics(self, db: Session, current_congruence: float, current_sentiment: float) -> Dict[str, Any]:
        """
        Queries recent check-ins and returns stability index and trend description.
        """
        recent_checkins: List[UserCheckIn] = db.query(UserCheckIn)\
            .order_by(UserCheckIn.timestamp.desc())\
            .limit(10)\
            .all()

        if not recent_checkins:
            return {
                "stability_index": 90.0,
                "trend_description": "Initial Baseline Established",
                "historical_count": 1
            }

        congruence_scores = [c.congruence_score for c in recent_checkins]
        sentiment_scores = [c.sentiment_score for c in recent_checkins]

        avg_congruence = sum(congruence_scores) / len(congruence_scores)
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

        # Base stability starts at 100
        stability = 100.0

        # Deduct if chronic masking or negative sentiment observed
        masking_count = sum(1 for c in recent_checkins if c.is_emotional_masking)
        stability -= (masking_count * 12.0)

        if avg_sentiment < -0.2:
            stability -= 15.0

        stability = max(10.0, min(100.0, stability))

        if len(recent_checkins) >= 3:
            recent_sentiments = [c.sentiment_score for c in recent_checkins[:3]]
            if recent_sentiments[0] > recent_sentiments[-1] + 0.2:
                trend = "Improving Trajectory"
            elif recent_sentiments[0] < recent_sentiments[-1] - 0.2:
                trend = "Declining Trajectory"
            else:
                trend = "Stable Balance"
        else:
            trend = "Establishing Pattern"

        return {
            "stability_index": round(stability, 1),
            "trend_description": trend,
            "historical_count": len(recent_checkins) + 1
        }


_trend_scorer_agent = None

def get_trend_scorer_agent() -> TrendScorerAgent:
    global _trend_scorer_agent
    if _trend_scorer_agent is None:
        _trend_scorer_agent = TrendScorerAgent()
    return _trend_scorer_agent
