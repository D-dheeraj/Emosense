import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to add 'Page X of Y' footers and top running headers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Suppress running header on cover/first page
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "EmoSense: Multimodal Emotion & Wellness Assistant — Technical Documentation")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * 72 - 54, 48)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, page_str)
        self.drawString(54, 34, "Dheeraj Kumar Singh | MCA III CA550-Project (MO 2026) | Guide: Dr. Partha Sarthi Bishnu")
        self.restoreState()

def generate_pdf():
    pdf_path = Path("/Users/macbook/Desktop/Emosense/EmoSense_Project_Documentation.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0f172a")     # Deep Slate
    c_secondary = colors.HexColor("#0284c7")   # Electric Blue
    c_accent = colors.HexColor("#059669")      # Emerald
    c_dark = colors.HexColor("#1e293b")        # Dark Slate Text
    c_light_bg = colors.HexColor("#f8fafc")    # Light Neutral
    c_border = colors.HexColor("#e2e8f0")

    # Typography Styles
    style_doc_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )
    
    style_doc_subtitle = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=8
    )

    style_body_bold = ParagraphStyle(
        "Body_Bold_Custom",
        parent=style_body,
        fontName="Helvetica-Bold"
    )

    style_callout = ParagraphStyle(
        "Callout_Text",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0f172a")
    )

    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )

    style_code = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title Block
    story.append(Paragraph("EmoSense: Multimodal Emotion & Wellness Assistant", style_doc_title))
    story.append(Paragraph("COMPREHENSIVE PROJECT DOCUMENTATION & TECHNICAL ARCHITECTURE REPORT", style_doc_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceAfter=12))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Project Title:</b>", style_table_cell), Paragraph("EmoSense: Multimodal Emotion & Wellness Assistant", style_table_cell),
         Paragraph("<b>Course / Code:</b>", style_table_cell), Paragraph("MCA III CA550-Project (MO 2026)", style_table_cell)],
        [Paragraph("<b>Student Name:</b>", style_table_cell), Paragraph("Dheeraj Kumar Singh", style_table_cell),
         Paragraph("<b>Roll No / Sec:</b>", style_table_cell), Paragraph("MCA/40044/25 (Section B)", style_table_cell)],
        [Paragraph("<b>Guide Name:</b>", style_table_cell), Paragraph("Dr. Partha Sarthi Bishnu", style_table_cell),
         Paragraph("<b>Institution:</b>", style_table_cell), Paragraph("Dept. of Computer Science & Applications", style_table_cell)],
        [Paragraph("<b>Execution Status:</b>", style_table_cell), Paragraph("<font color='#059669'><b>100% Fully Built & Deployed</b></font>", style_table_cell),
         Paragraph("<b>Repository:</b>", style_table_cell), Paragraph("github.com/D-dheeraj/Emosense", style_table_cell)]
    ]

    t_meta = Table(meta_data, colWidths=[90, 160, 90, 164])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    story.append(Paragraph("1. Executive Summary & Problem Statement", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))
    
    p1_text = (
        "Mental health monitoring applications traditionally rely on single-modal inputs, such as self-reported text surveys "
        "or standalone facial expression analysis. These conventional approaches suffer from critical flaws, most notably "
        "<b>Emotional Masking</b> — a psychological phenomenon where individuals exhibit outward positive facial expressions "
        "(e.g., forced smiles) or select 'Happy' emojis while experiencing severe underlying distress, depression, or burnout."
    )
    story.append(Paragraph(p1_text, style_body))

    p2_text = (
        "<b>EmoSense</b> solves this challenge by implementing a privacy-first, multimodal agentic AI platform. "
        "The system captures three complementary signals during a user check-in: <b>Visual Emotion</b> (on-device PyTorch CNN), "
        "<b>Textual Sentiment</b> (VADER micro-journaling engine), and <b>Self-Reported Mood</b> (emoji picker). "
        "A <b>3-Way Congruence Agent</b> (Google Gemini API) triangulates these signals to detect emotional masking, "
        "a <b>Trend Scorer Agent</b> tracks baseline stability in SQLite, and a <b>Report Writer Agent</b> triggers real-time "
        "actionable micro-interventions (such as 4-7-8 guided breathing visualizers and 432Hz ambient audio relaxation)."
    )
    story.append(Paragraph(p2_text, style_body))

    # Callout Box for Key Innovation
    callout_data = [[
        Paragraph(
            "<b>Key Innovation:</b> Privacy-preserving Edge AI face recognition running locally on Apple Silicon Mac M1 MPS GPU "
            "combined with Google Gemini multi-agent reasoning to catch hidden psychological distress without uploading raw video to external servers.",
            style_callout
        )
    ]]
    t_callout = Table(callout_data, colWidths=[504])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0f2fe")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (0,0), 4, c_secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#bae6fd"))
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 12))

    # SECTION 2: COMPLETE TECH STACK & ARCHITECTURE
    story.append(Paragraph("2. Complete Technology Stack & Specifications", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))

    tech_table_data = [
        [Paragraph("Layer / Subsystem", style_table_header), Paragraph("Technology Used", style_table_header), Paragraph("Technical Specification & Purpose", style_table_header)],
        [Paragraph("Edge AI Hardware", style_table_cell), Paragraph("Apple Silicon Mac M1 (MPS GPU)", style_table_cell), Paragraph("On-device hardware acceleration via PyTorch Metal Performance Shaders (`torch.device('mps')`) for < 20ms face inference.", style_table_cell)],
        [Paragraph("Deep Learning CNN", style_table_cell), Paragraph("PyTorch 2.8.0 (`EmoNet`)", style_table_cell), Paragraph("Custom 4-Block CNN trained on FER2013 dataset (35,887 images, 48x48 grayscale). Achieved <b>62.54% Validation Accuracy</b>.", style_table_cell)],
        [Paragraph("Computer Vision", style_table_cell), Paragraph("OpenCV 4.9.0 (`cv2`)", style_table_cell), Paragraph("Decodes Base64 webcam frames, performs Haar Cascade face detection with auto center-crop fallback.", style_table_cell)],
        [Paragraph("Text Sentiment Engine", style_table_cell), Paragraph("VADER (`vaderSentiment`)", style_table_cell), Paragraph("Rule-based lexicon analyzer returning compound sentiment score (-1.0 to +1.0) for micro-journaling entries.", style_table_cell)],
        [Paragraph("Multi-Agent AI Core", style_table_cell), Paragraph("Google Gemini API (`gemini-2.5-flash`)", style_table_cell), Paragraph("Drives 3-Way Congruence Agent, Trend Scorer Agent, Report Writer Agent, and Universal Multilingual Guidance Chatbot.", style_table_cell)],
        [Paragraph("Backend Framework", style_table_cell), Paragraph("FastAPI + Uvicorn", style_table_cell), Paragraph("Asynchronous REST API backend supporting `/api/checkin`, `/api/analyze-frame`, `/api/chat`, and `/api/history`.", style_table_cell)],
        [Paragraph("Database & ORM", style_table_cell), Paragraph("SQLite 3 + SQLAlchemy 2.0", style_table_cell), Paragraph("Persistent storage for `UserCheckIn`, `EmotionLog`, and `InterventionLog` tables (`emosense.db`).", style_table_cell)],
        [Paragraph("Frontend UI", style_table_cell), Paragraph("HTML5 + Vanilla CSS + JS + Chart.js", style_table_cell), Paragraph("Cyber-Health Dark Glassmorphic Dashboard with Tabbed Navigation, 4-7-8 Breathing visualizer, 432Hz Soundscape, and Chatbot Drawer.", style_table_cell)]
    ]

    t_tech = Table(tech_table_data, colWidths=[110, 134, 260])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 14))

    # SECTION 3: STEP-BY-STEP IMPLEMENTATION METHODOLOGY
    story.append(Paragraph("3. Step-by-Step Implementation Methodology", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))

    m_text = (
        "The project was engineered systematically following a prototype-to-production lifecycle across 7 distinct phases:"
    )
    story.append(Paragraph(m_text, style_body))

    steps_data = [
        [Paragraph("Phase", style_table_header), Paragraph("Milestone Target", style_table_header), Paragraph("Key Work Completed & Deliverables", style_table_header)],
        [Paragraph("Phase 1", style_table_cell), Paragraph("Environment Setup", style_table_cell), Paragraph("Created virtual environment (`venv`), configured Apple Silicon PyTorch MPS device recognition, and initialized directory structure.", style_table_cell)],
        [Paragraph("Phase 2", style_table_cell), Paragraph("PyTorch CNN Model Training", style_table_cell), Paragraph("Downloaded Kaggle FER2013 dataset (35k images). Wrote `app/ml/train_fer2013.py` and trained custom `EmoNet` CNN for 10 epochs on Mac M1 MPS GPU, achieving <b>62.54% accuracy</b>. Saved weights to `models_weights/fer2013_custom_cnn.pth`.", style_table_cell)],
        [Paragraph("Phase 3", style_table_cell), Paragraph("Edge Vision & NLP Engines", style_table_cell), Paragraph("Built `face_detector.py` using OpenCV Base64 frame decoding with center-crop fallback, and `sentiment_analyzer.py` using VADER lexicon.", style_table_cell)],
        [Paragraph("Phase 4", style_table_cell), Paragraph("Multi-Agent AI Core", style_table_cell), Paragraph("Implemented `congruence_agent.py` (Gemini API 3-Way Triangulation), `trend_scorer_agent.py` (ESI stability index), `report_writer_agent.py`, and `chatbot_agent.py` (Universal Multilingual Guidance Chatbot).", style_table_cell)],
        [Paragraph("Phase 5", style_table_cell), Paragraph("FastAPI Server & DB", style_table_cell), Paragraph("Built `app/main.py` REST API routes (`/api/checkin`, `/api/analyze-frame`, `/api/chat`, `/api/history`) and SQLAlchemy SQLite models (`models.py`).", style_table_cell)],
        [Paragraph("Phase 6", style_table_cell), Paragraph("Glassmorphic Dashboard UI", style_table_cell), Paragraph("Designed single-page dark Cyber-Health glassmorphic web dashboard with Tab Navigation, Webcam HUD, 4-7-8 Breathing visualizer, 432Hz Ambient Audio Player, and floating AI Chatbot drawer.", style_table_cell)],
        [Paragraph("Phase 7", style_table_cell), Paragraph("Git & GitHub Deployment", style_table_cell), Paragraph("Configured `.gitignore` to protect datasets/keys, committed codebase, and pushed repository to <b>github.com/D-dheeraj/Emosense.git</b>.", style_table_cell)]
    ]

    t_steps = Table(steps_data, colWidths=[54, 120, 330])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 14))

    # SECTION 4: SYSTEM MODULES & FUNCTIONALITIES
    story.append(Paragraph("4. System Modules & Core Functionalities", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))

    story.append(Paragraph("4.1 Multimodal Input Triangulation", style_h2))
    mod1_text = (
        "• <b>Visual Signal</b>: Captures webcam video frame -> OpenCV crops face -> PyTorch MPS CNN classifies 7 facial emotions.<br/>"
        "• <b>Textual Signal</b>: User enters micro-journal ('How was your day?') -> VADER computes sentiment score (-1.0 to +1.0).<br/>"
        "• <b>Self-Reported Signal</b>: User taps an emoji (e.g. 😀, 😔, 😠) to indicate subjective feeling."
    )
    story.append(Paragraph(mod1_text, style_body))

    story.append(Paragraph("4.2 Agentic AI Multimodal Triangulation Pipeline", style_h2))
    mod2_text = (
        "• <b>Agent 1 (3-Way Congruence Agent)</b>: Sends signal triplet to Google Gemini API. Detects <b>Emotional Masking</b> "
        "(e.g., smiling face on camera + negative journal text like 'I feel helpless'). Computes Congruence Index (0-100%).<br/>"
        "• <b>Agent 2 (Trend Scorer Agent)</b>: Queries historical check-in timeline from SQLite to calculate Emotional Stability Index (ESI) "
        "and prevent false alarms on isolated bad days.<br/>"
        "• <b>Agent 3 (Report Writer & Micro-Intervention Agent)</b>: Generates plain-language wellness synthesis and assigns micro-interventions.<br/>"
        "• <b>Agent 4 (Universal AI Companion Chatbot)</b>: Floating AI widget answering user questions in Hindi, Hinglish, or English about "
        "app usage, data privacy, tech stack, and breathing techniques."
    )
    story.append(Paragraph(mod2_text, style_body))

    story.append(Paragraph("4.3 Interactive Actionable Micro-Interventions Deck", style_h2))
    mod3_text = (
        "• <b>4-7-8 Guided Breathing Visualizer</b>: Animated pulsating visual ring (Inhale 4s -> Hold 7s -> Exhale 8s) with timer countdown.<br/>"
        "• <b>Ambient Soundscape Player</b>: Built-in 432Hz harmonic binaural relaxation sound generator to soothe nervous tension.<br/>"
        "• <b>Data Privacy Center</b>: Interactive tab detailing on-device PyTorch MPS face detection and local SQLite database security."
    )
    story.append(Paragraph(mod3_text, style_body))
    story.append(Spacer(1, 10))

    # SECTION 5: CURRENT PROJECT STATUS & MILESTONE VERIFICATION
    story.append(Paragraph("5. Current Project Status & Milestone Verification", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))

    status_data = [
        [Paragraph("Project Component", style_table_header), Paragraph("Status", style_table_header), Paragraph("Empirical Verification Results", style_table_header)],
        [Paragraph("PyTorch Edge AI Model", style_table_cell), Paragraph("<font color='#059669'><b>Trained & Verified</b></font>", style_table_cell), Paragraph("Trained 10 Epochs on FER2013 dataset using Mac M1 MPS GPU. Saved at `models_weights/fer2013_custom_cnn.pth` with <b>62.54% Validation Accuracy</b>.", style_table_cell)],
        [Paragraph("FastAPI Server & Endpoints", style_table_cell), Paragraph("<font color='#059669'><b>Active & Verified</b></font>", style_table_cell), Paragraph("All routes (`/api/checkin`, `/api/analyze-frame`, `/api/chat`, `/api/history`) tested and returning <b>HTTP 200 OK</b>.", style_table_cell)],
        [Paragraph("Gemini Multi-Agent Core", style_table_cell), Paragraph("<font color='#059669'><b>Active + Failsafe</b></font>", style_table_cell), Paragraph("Google Gemini API integration verified with rule-based heuristic fallback for offline execution.", style_table_cell)],
        [Paragraph("Glassmorphic Web Dashboard", style_table_cell), Paragraph("<font color='#059669'><b>100% Deployed</b></font>", style_table_cell), Paragraph("Live web dashboard running at <b>http://127.0.0.1:8000</b> with 4 Navigation Tabs, Floating AI Chatbot, and 4-7-8 Breathing Visualizer.", style_table_cell)],
        [Paragraph("Git & GitHub Repository", style_table_cell), Paragraph("<font color='#059669'><b>Committed & Pushed</b></font>", style_table_cell), Paragraph("Codebase committed with clean `.gitignore` and pushed to <b>https://github.com/D-dheeraj/Emosense.git</b>.", style_table_cell)]
    ]

    t_status = Table(status_data, colWidths=[120, 110, 274])
    t_status.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_status)
    story.append(Spacer(1, 14))

    # SECTION 6: REAL-WORLD UTILITY & FUTURE SCOPE
    story.append(Paragraph("6. Real-World Utility & Future Scope", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8))

    future_text = (
        "1. <b>University & College Student Wellness Portals</b>: Pre-screens academic burnout, exam stress, and student depression prior to severe crises while preserving student biometric privacy.<br/>"
        "2. <b>Corporate HR Employee Assistance Programs (EAPs)</b>: Integrated into IT company portals (TCS, Infosys, Accenture) to prevent tech worker burnout and prompt micro-breathing breaks.<br/>"
        "3. <b>Tele-Psychiatry & Digital Therapeutics</b>: Provides psychiatrists with an empirical 30-day Emotional Stability Index graph between patient therapy sessions.<br/>"
        "4. <b>Privacy-First Smart Home Health Kiosks</b>: Runs on edge AI hardware (Apple Silicon / Smart Mirrors) without sending raw camera video to cloud servers."
    )
    story.append(Paragraph(future_text, style_body))
    story.append(Spacer(1, 14))

    # Signature Block
    sig_data = [
        [Paragraph("<b>Student Signature:</b>", style_table_cell), Paragraph("_______________________<br/>Dheeraj Kumar Singh<br/>(MCA/40044/25)", style_table_cell),
         Paragraph("<b>Guide Signature:</b>", style_table_cell), Paragraph("_______________________<br/>Dr. Partha Sarthi Bishnu<br/>Project Guide", style_table_cell)]
    ]
    t_sig = Table(sig_data, colWidths=[110, 142, 110, 142])
    t_sig.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(KeepTogether([t_sig]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated documentation PDF at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
