from typing import Dict, Any

class ReportWriterAgent:
    """
    Agent 3: Report Writer & Micro-Intervention Agent.
    Generates plain-language wellness summaries and assigns real-time micro-interventions:
      - 4-7-8 Guided Breathing
      - Ambient Music & Relaxation Audio
      - Reflective Journaling Prompts
    """
    def generate_report_and_intervention(
        self,
        visual_emotion: str,
        textual_sentiment: str,
        self_reported_mood: str,
        congruence_score: float,
        congruence_status: str,
        is_masking: bool,
        stability_index: float
    ) -> Dict[str, Any]:
        """
        Synthesizes summary and selects micro-intervention payload.
        """
        if is_masking:
            summary = (
                f"Your check-in highlights a difference between your outward expression ({visual_emotion}) "
                f"and inner journal sentiment ({textual_sentiment}). Suppressing distress can cause subtle tension. "
                "Taking a brief moment to reset through guided breathing can help relieve internal strain."
            )
            recommended_intervention = "4-7-8 Guided Breathing"
            details = {
                "type": "breathing",
                "title": "4-7-8 Reset Breathing",
                "description": "Inhale for 4s, Hold for 7s, Exhale for 8s to calm the nervous system.",
                "duration_seconds": 120,
                "cycles": 4
            }
        elif visual_emotion in ['Sad', 'Fear', 'Angry'] or textual_sentiment == "Negative":
            summary = (
                f"We noticed signs of stress or low mood today ({visual_emotion} visual expression, {textual_sentiment} text tone). "
                "Unwinding with gentle audio frequencies can soothe mental fatigue."
            )
            recommended_intervention = "Ambient Soundscape"
            details = {
                "type": "music",
                "title": "Deep Relaxation Ambient Audio",
                "description": "Soothing nature soundscape designed for emotional grounding.",
                "audio_url": "/static/assets/ambient_relaxation.mp3",
                "duration_seconds": 180
            }
        elif congruence_score < 70.0:
            summary = (
                f"Your signals show mild variation (Congruence: {congruence_score:.0f}%). "
                "Reflective micro-journaling can bring clarity to conflicting thoughts."
            )
            recommended_intervention = "Reflective Journaling"
            details = {
                "type": "journal_prompt",
                "title": "Guided Reflective Prompt",
                "prompt": "What is one small thing that gave you comfort today, and what is one thought you'd like to let go of?",
                "duration_seconds": 300
            }
        else:
            summary = (
                f"Great alignment across all signals ({congruence_status}, {congruence_score:.0f}% congruence). "
                f"Your visual expression ({visual_emotion}) and mood reflect emotional harmony!"
            )
            recommended_intervention = "Mindful Affirmation"
            details = {
                "type": "affirmation",
                "title": "Mindful Affirmation",
                "affirmation": "I honor my emotions and give myself permission to rest and grow at my own pace.",
                "duration_seconds": 60
            }

        return {
            "wellness_summary": summary,
            "recommended_intervention": recommended_intervention,
            "intervention_details": details
        }


_report_writer_agent = None

def get_report_writer_agent() -> ReportWriterAgent:
    global _report_writer_agent
    if _report_writer_agent is None:
        _report_writer_agent = ReportWriterAgent()
    return _report_writer_agent
