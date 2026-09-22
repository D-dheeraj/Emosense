import os
import re
from typing import Dict, Any, List
from app.config import GEMINI_API_KEY

class EmoSenseChatbotAgent:
    """
    Universal Multilingual AI Assistant & Guidance Chatbot for EmoSense.
    Handles ANY unlimited, open-ended question in Hindi, Hinglish, English, or any language.
    """
    def __init__(self):
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[ChatbotAgent] Gemini API Client active for Universal Open-Ended Chatbot.")
            except Exception as e:
                print(f"[ChatbotAgent] Gemini Client init note: {e}")

    def respond(self, user_query: str) -> str:
        """
        Universal response generator for any open-ended question.
        """
        if not user_query or not user_query.strip():
            return "👋 Namaste! Main aapka **EmoSense AI Companion** hoon. Aap app ke kisi bhi feature, technical architecture, data privacy, ya mental wellness ke baare mein pooch sakte hain!"

        query_text = user_query.strip()

        # 1. Primary Engine: Google Gemini LLM for Unlimited Open-Ended Queries
        if self.client:
            try:
                system_prompt = """
You are the official EmoSense AI Companion & Project Assistant.
EmoSense is a Privacy-First Multimodal AI Wellness Assistant designed by Dheeraj Kumar Singh under the guidance of Dr. Partha Sarthi Bishnu.

Complete Knowledge Context:
- Project Purpose: Detects emotional masking (e.g. smiling face masking negative inner feelings) and provides real-time micro-interventions.
- Multimodal Signals: (1) Visual Face Emotion via custom PyTorch CNN (EmoNet) on Mac M1 MPS GPU, (2) Textual Sentiment via VADER, (3) Self-reported Emoji Mood.
- Agentic Core: 3-Way Congruence Agent (Gemini API) + Trend Scorer Agent (SQLite ESI baseline) + Report Writer Agent (4-7-8 Breathing & 432Hz Ambient Music).
- Privacy & Biometrics: Facial expressions are processed locally on the user's Mac M1 GPU. Raw video is NEVER uploaded to cloud servers. History is saved in local SQLite (emosense.db).
- Navigation: Live Check-In tab, Trend Analytics tab, Micro-Interventions tab, Data Privacy Center tab.

Instructions for Responding:
1. Answer ANY question asked by the user intelligently and specifically (whether related to the app, features, privacy, tech stack, mental health, breathing, or project viva).
2. Match the user's input language exactly (Hindi, Hinglish, English, Spanish, etc.).
3. Format output cleanly using Markdown bullet points or short paragraphs.
"""
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\nUser Question: {query_text}"
                )
                return response.text.strip()
            except Exception as e:
                print(f"[ChatbotAgent] Gemini API call note ({e}), switching to Dynamic Semantic Parser.")

        # 2. Secondary Engine: Dynamic Semantic NLP Tokenizer & Synthesizer for Offline Mode
        return self._dynamic_semantic_synthesizer(query_text)

    def _dynamic_semantic_synthesizer(self, query: str) -> str:
        q_lower = query.lower()
        words = set(re.findall(r'\w+', q_lower))

        is_hindi = any(w in words for w in ['kya', 'kaise', 'kahan', 'kaun', 'kyun', 'batao', 'bataiye', 'hai', 'hain', 'ho', 'main', 'aap', 'mera', 'meri', 'karo', 'suno', 'ye', 'is', 'ko', 'se'])

        # Concept Maps
        privacy_terms = {'privacy', 'secure', 'safe', 'security', 'data', 'store', 'storage', 'database', 'sqlite', 'camera', 'video', 'saved', 'suraksha', 'chori', 'leak', 'cloud', 'biometric', 'emosense.db'}
        congruence_terms = {'mask', 'masking', 'congruence', '3way', 'triangulat', 'triangulation', 'score', 'discrepancy', 'alignment', 'fake', 'smile', 'distress', 'agent', 'reasoning'}
        usage_terms = {'use', 'run', 'start', 'step', 'guide', 'working', 'help', 'chalaen', 'tarika', 'feature', 'kaam', 'button', 'tab', 'checkin', 'process'}
        breathing_terms = {'breath', 'breathing', '478', 'relax', 'exercise', 'intervention', 'music', 'audio', 'sound', 'reset', 'stress', 'anxiety', 'mindfulness'}
        tech_terms = {'tech', 'stack', 'pytorch', 'fastapi', 'developer', 'dheeraj', 'guide', 'm1', 'mps', 'synopsis', 'viva', 'dr', 'bishnu', 'python', 'opencv', 'cnn', 'emonet', 'model', 'dataset', 'fer2013', 'kaggle'}

        # Calculate Intersections
        scores = {
            'privacy': len(words & privacy_terms),
            'congruence': len(words & congruence_terms),
            'usage': len(words & usage_terms),
            'breathing': len(words & breathing_terms),
            'tech': len(words & tech_terms)
        }

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]

        # Synthesize Dynamic Answer Based on Detected Intent & Entities
        if best_intent == 'privacy' and max_score > 0:
            if is_hindi:
                return (
                    "🔒 **Aapki Data Privacy & Security Full Safe Hai!**\n\n"
                    "• **Edge AI Processing**: Aapke webcam ki face video kabi kisi cloud server par nahi bheji jaati. Yeh aapke Mac M1 GPU par PyTorch (MPS) se **locally process** hoti hai.\n"
                    "• **Local SQLite Storage**: Aapka sabhi check-in history data local database file `emosense.db` mein aapke computer par hi safe rehta hai."
                )
            else:
                return (
                    "🔒 **Data Privacy & Security Guarantee**\n\n"
                    "• **On-Device Edge AI**: Facial analysis runs 100% locally on your Mac M1 GPU using PyTorch MPS acceleration. Raw video is NEVER uploaded to cloud servers.\n"
                    "• **Local Storage**: Your history is saved safely inside your local SQLite database (`emosense.db`)."
                )

        elif best_intent == 'congruence' and max_score > 0:
            if is_hindi:
                return (
                    "🛡️ **3-Way Congruence & Emotional Masking Explanation:**\n\n"
                    "• EmoSense aapke 3 signals ko triangulate karta hai: (1) Face Expression (PyTorch CNN), (2) Journal Text Sentiment (VADER), aur (3) Emoji Mood.\n"
                    "• **Emotional Masking**: Agar koi bahar se smile kar raha hai par andar se distressed feel kar raha hai, toh 3-Way Congruence Agent **Masked Distress Alert** trigger karta hai."
                )
            else:
                return (
                    "🛡️ **3-Way Congruence & Emotional Masking:**\n\n"
                    "• Triangulates 3 signals: Visual Expression, Micro-Journal Text Sentiment, and Self-Reported Emoji Mood.\n"
                    "• Flags **Masked Distress** whenever there is a conflict between outward facial expression and inner text sentiment."
                )

        elif best_intent == 'breathing' and max_score > 0:
            if is_hindi:
                return (
                    "🫁 **4-7-8 Guided Breathing & Micro-Interventions:**\n\n"
                    "• **Inhale**: Naak se 4s tak saans lein.\n"
                    "• **Hold**: Saans ko 7s tak rokein.\n"
                    "• **Exhale**: 8s mein mooh se saans chhodein.\n\n"
                    "💡 **Micro-Interventions Tab** par animated breathing visualizer aur 432Hz ambient relaxation soundscape player active hai!"
                )
            else:
                return (
                    "🫁 **4-7-8 Breathing & Micro-Interventions:**\n\n"
                    "• **Inhale**: 4 seconds through your nose.\n"
                    "• **Hold**: 7 seconds hold.\n"
                    "• **Exhale**: 8 seconds through your mouth.\n\n"
                    "Navigate to the **Micro-Interventions** tab for the interactive visualizer and 432Hz ambient relaxation audio!"
                )

        elif best_intent == 'tech' and max_score > 0:
            if is_hindi:
                return (
                    "💻 **EmoSense Project & Technical Overview:**\n\n"
                    "• **Project Title**: EmoSense: Multimodal Emotion & Wellness Assistant\n"
                    "• **Developer**: Dheeraj Kumar Singh | **Guide**: Dr. Partha Sarthi Bishnu\n"
                    "• **Tech Stack**: PyTorch CNN (EmoNet trained on FER2013), Mac M1 MPS GPU, OpenCV, FastAPI, SQLite, Google Gemini API."
                )
            else:
                return (
                    "💻 **EmoSense Technical Overview:**\n\n"
                    "• **Title**: EmoSense - Multimodal Emotion & Wellness Assistant\n"
                    "• **Developer**: Dheeraj Kumar Singh | **Guide**: Dr. Partha Sarthi Bishnu\n"
                    "• **Tech Stack**: PyTorch (Mac M1 MPS GPU), OpenCV, FastAPI, SQLite, Google Gemini API, Chart.js."
                )

        elif best_intent == 'usage' and max_score > 0:
            if is_hindi:
                return (
                    "📱 **EmoSense Guide & Usage:**\n\n"
                    "1. **Live Check-In**: Camera ke samne aayein -> Real-time Edge PyTorch CNN facial emotion detect karega.\n"
                    "2. **Emoji & Text**: Emoji select karein aur journal text likhein.\n"
                    "3. **Analyze**: 'Run 3-Way Congruence Check-In' click karke Gemini Agent analysis aur 4-7-8 Breathing reset dekhein."
                )
            else:
                return (
                    "📱 **How to Use EmoSense:**\n\n"
                    "1. **Live Check-In**: Position in front of webcam for real-time PyTorch MPS detection.\n"
                    "2. **Emoji & Text**: Select your mood emoji and enter a micro-journal entry.\n"
                    "3. **Check-In**: Click **Run 3-Way Congruence Check-In** to view agent reasoning and interventions."
                )

        else:
            # Universal Dynamic Synthesizer for any other open-ended question
            if is_hindi:
                return (
                    f"🤖 **EmoSense AI Companion Response:**\n\n"
                    f"Aapne '{query}' ke baare mein poocha hai.\n\n"
                    "EmoSense ek privacy-first multimodal AI platform hai jo PyTorch MPS Edge AI face detection, micro-journal sentiment analysis, aur Google Gemini 3-Way Congruence Agent ko combine karke emotional masking detect karta hai.\n\n"
                    "Aap app ke kisi bhi specific feature, data privacy, 4-7-8 breathing, ya project tech stack ke baare mein kuch bhi pooch sakte hain!"
                )
            else:
                return (
                    f"🤖 **EmoSense AI Assistant Response:**\n\n"
                    f"Regarding '{query}': EmoSense is a multimodal AI wellness assistant combining PyTorch MPS edge face recognition, text sentiment, and Gemini Agent triangulation.\n\n"
                    "Feel free to ask any open-ended question about Data Privacy, 3-Way Congruence, 4-7-8 Breathing, or Tech Architecture!"
                )


_chatbot_agent = None

def get_chatbot_agent() -> EmoSenseChatbotAgent:
    global _chatbot_agent
    if _chatbot_agent is None:
        _chatbot_agent = EmoSenseChatbotAgent()
    return _chatbot_agent
