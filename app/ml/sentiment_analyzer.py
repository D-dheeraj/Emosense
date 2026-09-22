from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any, Tuple

class TextSentimentAnalyzer:
    """
    Micro-journaling Text Sentiment Analysis Engine using VADER Lexicon.
    Computes compound sentiment score, emotional valence, and confidence metrics.
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Analyzes micro-journaling text.
        Returns: (sentiment_label, compound_score, score_breakdown)
        """
        if not text or not text.strip():
            return "Neutral", 0.0, {"pos": 0.0, "neu": 1.0, "neg": 0.0, "compound": 0.0}

        scores = self.analyzer.polarity_scores(text)
        compound = float(scores["compound"])

        if compound >= 0.15:
            label = "Positive"
        elif compound <= -0.15:
            label = "Negative"
        else:
            label = "Neutral"

        return label, compound, scores


_sentiment_analyzer = None

def get_sentiment_analyzer() -> TextSentimentAnalyzer:
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = TextSentimentAnalyzer()
    return _sentiment_analyzer
