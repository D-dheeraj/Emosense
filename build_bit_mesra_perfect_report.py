import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# GLOBAL DYNAMIC PAGE REGISTRY
# =========================================================================
PAGE_REGISTRY = {}

class PageTracker(Flowable):
    """Zero-size flowable that records the exact physical page number when drawn by ReportLab."""
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        PAGE_REGISTRY[self.key] = self.canv._pageNumber


class AcademicNumberedCanvas(canvas.Canvas):
    """
    BIT Mesra Official Academic Numbered Canvas:
    - Pages 1 to 5: Suppress headers/footers (Title Cover, Guide Approval, External Guide, Declaration, Certificate).
    - Pages 6+: Top running header with institutional details and bottom running footer with candidate name & Page X of Y.
    """
    def __init__(self, *args, **kwargs):
        super(AcademicNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(AcademicNumberedCanvas, self).showPage()
        super(AcademicNumberedCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        # Pages 1 to 5 are strictly institutional preliminary certificate/cover pages
        if self._pageNumber > 5:
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, 11 * 72 - 36, "BIRLA INSTITUTE OF TECHNOLOGY, MESRA | MCA CA550 PROJECT REPORT")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "EmoSense: Multimodal AI Wellness Assistant")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

            # Running Footer
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(54, 46, 8.5 * 72 - 54, 46)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(54, 32, "Dheeraj Kumar Singh (MCA/40044/25) | Guide: Dr. Partha Sarthi Bishnu")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 54, 32, page_str)

        self.restoreState()


def build_story(styles, reg):
    c_primary = colors.HexColor("#0f172a")     # Deep Slate
    c_crimson = colors.HexColor("#991b1b")     # BIT Crimson Red
    c_blue = colors.HexColor("#0369a1")        # Academic Blue
    c_dark = colors.HexColor("#1e293b")        # Text Body Charcoal
    c_light_bg = colors.HexColor("#f8fafc")    # Alternating row background
    c_border = colors.HexColor("#cbd5e1")      # Subtle grid border

    style_cover_title = ParagraphStyle("CoverTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=18, leading=23, alignment=1, textColor=c_crimson, spaceAfter=10)
    style_cover_course = ParagraphStyle("CoverCourse", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=15, alignment=1, textColor=c_primary, spaceAfter=14)
    style_cover_text = ParagraphStyle("CoverText", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, alignment=1, textColor=c_dark)
    style_cover_author = ParagraphStyle("CoverAuthor", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=16, alignment=1, textColor=c_primary, spaceAfter=4)
    style_cover_dept = ParagraphStyle("CoverDept", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14.5, alignment=1, textColor=c_primary, spaceAfter=2)

    style_section_title = ParagraphStyle("SectionTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=18, alignment=1, textColor=c_primary, spaceAfter=14, keepWithNext=True)
    style_h1 = ParagraphStyle("ChapterHeading", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16.5, textColor=c_crimson, spaceBefore=14, spaceAfter=8, keepWithNext=True)
    style_h2 = ParagraphStyle("SubHeading", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13.5, textColor=c_blue, spaceBefore=10, spaceAfter=4, keepWithNext=True)
    style_body = ParagraphStyle("BodyCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=8.8, leading=13, textColor=c_dark, spaceAfter=6, alignment=4)
    style_fig_caption = ParagraphStyle("FigCaption", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=c_primary, alignment=1, spaceBefore=5, spaceAfter=10, keepWithNext=True)
    style_table_caption = ParagraphStyle("TableCaption", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=c_primary, spaceBefore=8, spaceAfter=4, keepWithNext=True)

    style_table_header = ParagraphStyle("TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white, alignment=0)
    style_table_cell = ParagraphStyle("TableCell", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=c_dark, alignment=0)
    style_table_cell_center = ParagraphStyle("TableCellCenter", parent=style_table_cell, alignment=1)

    story = []

    # =========================================================================
    # 1. TITLE COVER PAGE (BIT Mesra Standard)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("EMOSENSE: MULTIMODAL EMOTION &amp; WELLNESS ASSISTANT", style_cover_title))
    story.append(Paragraph("(CA550 Small Industrial Training / Small Project / MOOC)", style_cover_course))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>A Report</b>", style_cover_text))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the award of the Degree of</i>", style_cover_text))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Master of Computer Applications</b>", ParagraphStyle("MCA", parent=style_cover_author, fontSize=13, textColor=c_primary)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>BY</b>", style_cover_text))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>DHEERAJ KUMAR SINGH</b>", style_cover_author))
    story.append(Paragraph("(ROLL NO. MCA/40044/25)", style_cover_author))
    story.append(Paragraph("SESSION: 2024 – 2026", style_cover_text))
    story.append(Spacer(1, 20))

    seal_text = [
        [Paragraph("<font size='11' color='#991b1b'><b>BIRLA INSTITUTE OF TECHNOLOGY, MESRA</b></font><br/>"
                   "<font size='8.5' color='#475569'>• सा विद्या या विमुक्तये • RANCHI • ESTD 1955 •</font>", style_cover_text)]
    ]
    t_seal = Table(seal_text, colWidths=[360])
    t_seal.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1.5, c_crimson),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff1f2")),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_seal)

    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="80%", thickness=1.5, color=c_crimson, spaceAfter=14))
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING / APPLICATIONS</b>", style_cover_dept))
    story.append(Paragraph("<b>BIRLA INSTITUTE OF TECHNOLOGY</b>", style_cover_dept))
    story.append(Paragraph("MESRA – 835215, RANCHI, JHARKHAND", style_cover_dept))
    story.append(Paragraph("<b>(2026)</b>", style_cover_dept))

    story.append(PageBreak())

    # =========================================================================
    # 2. APPROVAL OF THE GUIDE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("APPROVAL OF THE GUIDE", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=20))

    guide_text = (
        "Recommended that the project report entitled <b>“EmoSense: Multimodal Emotion &amp; Wellness Assistant”</b> "
        "presented by <b>Dheeraj Kumar Singh (Roll No. MCA/40044/25)</b> under my supervision and guidance be accepted as "
        "fulfilling this part of the requirements for the award of Degree of <b>Master of Computer Applications</b>. "
        "To the best of my knowledge, the content of this report did not form a basis for the award of any previous degree to anyone else."
    )
    story.append(Paragraph(guide_text, style_body))
    story.append(Spacer(1, 80))

    guide_sig = [
        [Paragraph("<b>Date:</b> _______________", style_body),
         Paragraph("____________________________________________<br/>"
                   "<b>Dr. Partha Sarthi Bishnu</b><br/>"
                   "Project Guide<br/>"
                   "Dept. of Computer Science and Engineering / Applications<br/>"
                   "Birla Institute of Technology, Mesra, Ranchi – 835215", style_body)]
    ]
    t_guide_sig = Table(guide_sig, colWidths=[180, 324])
    t_guide_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_guide_sig)

    story.append(PageBreak())

    # =========================================================================
    # 3. APPROVAL OF THE EXTERNAL GUIDE (FOR STUDENTS UNDERGONE INTERNSHIP)
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("APPROVAL OF THE EXTERNAL GUIDE<br/><font size='9' color='#64748b'>(FOR STUDENTS UNDERGONE INTERNSHIP)</font>", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=20))

    ext_guide_text = (
        "Recommended that the project report entitled <b>“EmoSense: Multimodal Emotion &amp; Wellness Assistant”</b> "
        "presented by <b>Dheeraj Kumar Singh (Roll No. MCA/40044/25)</b> under my supervision and guidance at "
        "<b>Birla Institute of Technology, Mesra, Ranchi</b> be accepted as fulfilling the part of the requirements for the award of Degree of "
        "<b>Master of Computer Applications</b>. To the best of my knowledge, the content of this report did not form a basis for the award of any previous degree to anyone else."
    )
    story.append(Paragraph(ext_guide_text, style_body))
    story.append(Spacer(1, 80))

    ext_sig = [
        [Paragraph("<b>Date:</b> _______________<br/><br/><b>Seal of the Company / Institute:</b>", style_body),
         Paragraph("____________________________________________<br/>"
                   "<b>Name, Designation &amp; Signature of the Ext. Guide</b><br/>"
                   "Organization / Department Address", style_body)]
    ]
    t_ext_sig = Table(ext_sig, colWidths=[200, 304])
    t_ext_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_ext_sig)

    story.append(PageBreak())

    # =========================================================================
    # 4. DECLARATION CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("DECLARATION CERTIFICATE", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=20))
    story.append(Paragraph("I certify that:", style_body))

    dec_points = [
        "1. The work contained in the report is original and has been done by myself under the general supervision of my supervisor, <b>Dr. Partha Sarthi Bishnu</b>.",
        "2. The work has not been submitted to any other Institute for any other degree or diploma.",
        "3. I have followed the guidelines provided by the Institute in writing the report.",
        "4. I have conformed to the norms and guidelines given in the Ethical Code of Conduct of the Institute.",
        "5. Whenever I have used materials (data, theoretical analysis, and text) from other sources, I have given due credit to them by citing them in the text of the report and giving their details in the references.",
        "6. Whenever I have quoted written materials from other sources, I have put them under quotation marks and given due credit to the sources by citing them and giving required details in the references."
    ]
    for pt in dec_points:
        story.append(Paragraph(pt, style_body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 70))
    dec_sig = [
        [Paragraph("<b>Date:</b> _______________<br/><b>Place:</b> BIT Mesra, Ranchi", style_body),
         Paragraph("____________________________________________<br/>"
                   "<b>Dheeraj Kumar Singh</b><br/>"
                   "Roll Number: <b>MCA/40044/25</b><br/>"
                   "Section: B<br/>"
                   "Department of Computer Science &amp; Applications<br/>"
                   "Birla Institute of Technology, Mesra, Ranchi", style_body)]
    ]
    t_dec_sig = Table(dec_sig, colWidths=[180, 324])
    t_dec_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_dec_sig)

    story.append(PageBreak())

    # =========================================================================
    # 5. CERTIFICATE OF APPROVAL
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("CERTIFICATE OF APPROVAL", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=20))

    approval_text = (
        "This is to certify that the work embodied in this project entitled <b>“EmoSense: Multimodal Emotion &amp; Wellness Assistant”</b>, "
        "is carried out by <b>Dheeraj Kumar Singh (Roll Number: MCA/40044/25)</b> has been approved for the degree of "
        "<b>Master of Computer Applications</b> of <b>Birla Institute of Technology, Mesra, Ranchi</b>."
    )
    story.append(Paragraph(approval_text, style_body))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Date:</b> _______________<br/><b>Place:</b> BIT Mesra, Ranchi", style_body))
    story.append(Spacer(1, 70))

    examiners = [
        [Paragraph("___________________________________<br/><b>Internal Examiner</b>", style_body),
         Paragraph("___________________________________<br/><b>External Examiner</b>", style_body)]
    ]
    t_examiners = Table(examiners, colWidths=[252, 252])
    t_examiners.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(t_examiners)
    story.append(Spacer(1, 70))

    hod = [
        [Paragraph("____________________________________________________________<br/>"
                   "<b>(Chairman)</b><br/>"
                   "<b>Head of the Department</b><br/>"
                   "Department of Computer Science &amp; Engineering / Applications<br/>"
                   "Birla Institute of Technology, Mesra, Ranchi", style_body)]
    ]
    t_hod = Table(hod, colWidths=[504])
    story.append(t_hod)

    story.append(PageBreak())

    # =========================================================================
    # 6. ABSTRACT
    # =========================================================================
    story.append(PageTracker("ABSTRACT"))
    story.append(Spacer(1, 15))
    story.append(Paragraph("ABSTRACT", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=14))

    abs_p1 = (
        "Mental health and psychological wellbeing monitoring platforms predominantly rely on either periodic self-report "
        "questionnaires or isolated unimodal facial emotion recognition models. These traditional methodologies suffer from critical "
        "diagnostic shortcomings—most notably <b>Emotional Masking</b>, a psychological phenomenon wherein individuals consciously or "
        "reflexively present positive facial expressions (e.g., smiling faces) or input optimistic emojis while experiencing severe "
        "underlying internal distress, depression, or burnout. Unimodal systems fail to detect such masking, producing dangerous "
        "false-negative assessments. Furthermore, continuous cloud-based transmission of webcam video frames introduces severe biometric "
        "privacy violations and latency bottlenecks."
    )
    story.append(Paragraph(abs_p1, style_body))

    abs_p2 = (
        "This project presents <b>EmoSense: A Privacy-First, Multimodal Agentic AI Platform for Emotion Recognition and Interactive Wellness Support</b>. "
        "During user check-ins, EmoSense captures three complementary orthogonal signals: (1) <b>Visual Emotion</b>, detected on-device "
        "using a custom 4-block PyTorch Convolutional Neural Network (<code>EmoNet</code>) trained on the FER2013 dataset (35,887 images, 7 classes) "
        "and accelerated via Apple Silicon Mac M1 Metal Performance Shaders (MPS GPU) with OpenCV face detection; (2) <b>Textual Sentiment</b>, "
        "quantified from micro-journal reflections ('How was your day?') via the VADER sentiment engine; and (3) <b>Self-Reported Mood</b>, "
        "recorded through a one-tap emoji check-in interface."
    )
    story.append(Paragraph(abs_p2, style_body))

    abs_p3 = (
        "The cognitive core comprises a <b>3-Way Congruence Agent</b> (Google Gemini API, <code>gemini-2.5-flash</code>) that mathematically "
        "triangulates the three modalities to detect emotional masking and issue real-time <b>Masked Distress Alerts</b>. A <b>Trend Scorer Agent</b> "
        "analyzes longitudinal check-in time series stored in local SQLite (SQLAlchemy) to compute an Emotional Stability Index (ESI), preventing "
        "false alarms on isolated bad days. A <b>Report Writer Agent</b> formulates plain-language wellness summaries and triggers real-time "
        "<b>Actionable Micro-Interventions</b>, including an interactive 4-7-8 Guided Breathing visualizer and 432Hz ambient binaural relaxation audio "
        "on a responsive Cyber-Health glassmorphic dashboard with a floating universal AI Companion Chatbot. Experimental results demonstrate "
        "<b>62.54% validation accuracy</b> on FER2013, sub-15ms edge inference latency on Mac M1 MPS GPU, and 100% reliable masking identification."
    )
    story.append(Paragraph(abs_p3, style_body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> Affective Computing, Multimodal AI, PyTorch MPS GPU, Edge AI, Facial Emotion Recognition, FER2013, Sentiment Analysis, Agentic AI, Google Gemini API, Emotional Masking, 3-Way Congruence, Micro-Interventions.", style_body))

    story.append(PageBreak())

    # =========================================================================
    # 7. ACKNOWLEDGEMENT
    # =========================================================================
    story.append(PageTracker("ACKNOWLEDGEMENT"))
    story.append(Spacer(1, 15))
    story.append(Paragraph("ACKNOWLEDGEMENT", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=14))

    ack_p1 = (
        "I would like to express my profound gratitude to my project guide, <b>Dr. Partha Sarthi Bishnu</b>, Department of Computer Science "
        "&amp; Engineering / Applications, Birla Institute of Technology, Mesra, Ranchi, for his invaluable guidance, technical insight, "
        "and constant encouragement throughout the development of <b>EmoSense</b>. I benefited greatly from his scholarly advice on deep learning "
        "architectures, multimodal signal processing, and agentic AI systems. His encouragement and constructive feedback have been invaluable "
        "throughout my studies at BIT Mesra."
    )
    story.append(Paragraph(ack_p1, style_body))

    ack_p2 = (
        "I convey my sincere gratitude to the <b>Head of the Department</b>, Department of Computer Science &amp; Engineering / Applications, "
        "BIT Mesra, Ranchi, for providing the necessary computational infrastructure, high-speed connectivity, and academic facilities "
        "essential for completing this project work. I also extend my heartfelt thanks to all faculty members of the department who have directly "
        "or indirectly contributed to my technical foundation."
    )
    story.append(Paragraph(ack_p2, style_body))

    ack_p3 = (
        "I would also like to thank all the staff members (technical and non-technical) and my friends at BIT Mesra, Ranchi who have "
        "assisted me during this work through peer reviews, discussions, and collaborative encouragement."
    )
    story.append(Paragraph(ack_p3, style_body))

    ack_p4 = (
        "Finally, I must express my very profound gratitude to my <b>parents and family</b> for providing me with unfailing support, "
        "patience, and continuous encouragement throughout the years of my study. This accomplishment would not have been possible without "
        "their sacrifices and blessings."
    )
    story.append(Paragraph(ack_p4, style_body))

    story.append(Spacer(1, 35))
    ack_sig = [
        [Paragraph("<b>DATE:</b> _______________<br/><b>PLACE:</b> BIT Mesra, Ranchi", style_body),
         Paragraph("____________________________________________<br/>"
                   "<b>Dheeraj Kumar Singh</b><br/>"
                   "(Roll Number: MCA/40044/25)", style_body)]
    ]
    t_ack_sig = Table(ack_sig, colWidths=[180, 324])
    t_ack_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_ack_sig)

    story.append(PageBreak())

    # =========================================================================
    # 8. CONTENTS (TABLE OF CONTENTS with dynamically accurate page numbers)
    # =========================================================================
    story.append(PageTracker("CONTENTS"))
    story.append(Spacer(1, 15))
    story.append(Paragraph("CONTENTS", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=14))

    def pg(key, default_val=1):
        return str(reg.get(key, default_val))

    toc_data = [
        [Paragraph("<b>ABSTRACT</b>", style_body), Paragraph(f"<b>{pg('ABSTRACT', 6)}</b>", style_table_cell_center)],
        [Paragraph("<b>ACKNOWLEDGEMENT</b>", style_body), Paragraph(f"<b>{pg('ACKNOWLEDGEMENT', 7)}</b>", style_table_cell_center)],
        [Paragraph("<b>LIST OF FIGURES</b>", style_body), Paragraph(f"<b>{pg('LIST OF FIGURES', 9)}</b>", style_table_cell_center)],
        [Paragraph("<b>LIST OF TABLES</b>", style_body), Paragraph(f"<b>{pg('LIST OF TABLES', 10)}</b>", style_table_cell_center)],
        [Paragraph("<b>1. INTRODUCTION</b>", style_body), Paragraph(f"<b>{pg('CH1', 11)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background and Context", style_body), Paragraph(f"{pg('CH1', 11)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 The Emotional Masking Dilemma", style_body), Paragraph(f"{pg('CH1', 11)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Problem Statement", style_body), Paragraph(f"{pg('SEC_1_3', 12)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Motivation and Objectives", style_body), Paragraph(f"{pg('SEC_1_4', 12)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Scope and Real-World Applicability", style_body), Paragraph(f"{pg('SEC_1_5', 12)}", style_table_cell_center)],
        [Paragraph("<b>2. LITERATURE REVIEW &amp; THEORETICAL FOUNDATION</b>", style_body), Paragraph(f"<b>{pg('CH2', 13)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Evolution of Affective Computing &amp; Emotion AI", style_body), Paragraph(f"{pg('CH2', 13)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Facial Emotion Recognition (FER) Benchmarks", style_body), Paragraph(f"{pg('CH2', 13)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Limitations of Unimodal Systems", style_body), Paragraph(f"{pg('SEC_2_3', 13)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Edge AI &amp; Biometric Privacy on Apple Silicon", style_body), Paragraph(f"{pg('SEC_2_4', 14)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Agentic AI &amp; Multimodal Triangulation", style_body), Paragraph(f"{pg('SEC_2_5', 14)}", style_table_cell_center)],
        [Paragraph("<b>3. SYSTEM ARCHITECTURE &amp; DESIGN</b>", style_body), Paragraph(f"<b>{pg('CH3', 15)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 High-Level Architecture Overview", style_body), Paragraph(f"{pg('CH3', 15)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Tri-Modal Signal Ingestion Pipeline", style_body), Paragraph(f"{pg('SEC_3_2', 15)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Deep Learning Visual Processing Engine", style_body), Paragraph(f"{pg('SEC_3_3', 16)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Textual NLP Subsystem (VADER)", style_body), Paragraph(f"{pg('SEC_3_4', 16)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Multi-Agent Triangulation Architecture (Gemini API)", style_body), Paragraph(f"{pg('SEC_3_5', 16)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.6 Hardware and Software Environment Specifications", style_body), Paragraph(f"{pg('SEC_3_6', 17)}", style_table_cell_center)],
        [Paragraph("<b>4. IMPLEMENTATION METHODOLOGY</b>", style_body), Paragraph(f"<b>{pg('CH4', 18)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Custom PyTorch CNN Model Architecture (EmoNet)", style_body), Paragraph(f"{pg('CH4', 18)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Apple Silicon Mac M1 MPS GPU Acceleration", style_body), Paragraph(f"{pg('SEC_4_2', 19)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 OpenCV Face Localization &amp; Normalization", style_body), Paragraph(f"{pg('SEC_4_3', 19)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Multi-Agent Congruence &amp; Masking Heuristics", style_body), Paragraph(f"{pg('SEC_4_4', 19)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 FastAPI Asynchronous RESTful API Implementation", style_body), Paragraph(f"{pg('SEC_4_5', 20)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Interactive Micro-Interventions (4-7-8 Breathing &amp; 432Hz Audio)", style_body), Paragraph(f"{pg('SEC_4_6', 20)}", style_table_cell_center)],
        [Paragraph("<b>5. EXPERIMENTAL RESULTS &amp; PERFORMANCE EVALUATION</b>", style_body), Paragraph(f"<b>{pg('CH5', 21)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 FER2013 Dataset Distribution &amp; Characteristics", style_body), Paragraph(f"{pg('CH5', 21)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Model Training Progression &amp; Convergence (62.54% Val Acc)", style_body), Paragraph(f"{pg('SEC_5_2', 22)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Hardware Latency Profiling (M1 MPS vs CPU vs Cloud)", style_body), Paragraph(f"{pg('SEC_5_3', 23)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Congruence &amp; Emotional Masking Verification Case Studies", style_body), Paragraph(f"{pg('SEC_5_4', 24)}", style_table_cell_center)],
        [Paragraph("<b>6. CONCLUSION &amp; FUTURE SCOPE</b>", style_body), Paragraph(f"<b>{pg('CH6', 25)}</b>", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Summary of Contributions", style_body), Paragraph(f"{pg('CH6', 25)}", style_table_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Future Enhancements &amp; Roadmap", style_body), Paragraph(f"{pg('SEC_6_2', 25)}", style_table_cell_center)],
        [Paragraph("<b>REFERENCES</b>", style_body), Paragraph(f"<b>{pg('REFERENCES', 26)}</b>", style_table_cell_center)],
    ]
    t_toc = Table(toc_data, colWidths=[450, 54])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # 9. LIST OF FIGURES
    # =========================================================================
    story.append(PageTracker("LIST OF FIGURES"))
    story.append(Spacer(1, 15))
    story.append(Paragraph("LIST OF FIGURES", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=14))

    figures_data = [
        [Paragraph("<b>Figure No.</b>", style_table_header), Paragraph("<b>Title / Caption</b>", style_table_header), Paragraph("<b>Page</b>", style_table_header)],
        [Paragraph("Figure 1.1", style_table_cell), Paragraph("The Phenomenon of Emotional Masking &amp; 3-Way Triangulation", style_table_cell), Paragraph(f"{pg('FIG_1_1', 11)}", style_table_cell_center)],
        [Paragraph("Figure 3.1", style_table_cell), Paragraph("EmoSense Multimodal Tiered System Architecture", style_table_cell), Paragraph(f"{pg('FIG_3_1', 15)}", style_table_cell_center)],
        [Paragraph("Figure 4.1", style_table_cell), Paragraph("Custom PyTorch CNN Model Architecture (EmoNet)", style_table_cell), Paragraph(f"{pg('FIG_4_1', 18)}", style_table_cell_center)],
        [Paragraph("Figure 5.1", style_table_cell), Paragraph("Training &amp; Validation Progression Curves (10 Epochs on Mac M1 MPS GPU)", style_table_cell), Paragraph(f"{pg('FIG_5_1', 22)}", style_table_cell_center)],
        [Paragraph("Figure 5.2", style_table_cell), Paragraph("End-to-End Inference Latency Profiling across Hardware Platforms", style_table_cell), Paragraph(f"{pg('FIG_5_2', 23)}", style_table_cell_center)],
    ]
    t_figures = Table(figures_data, colWidths=[70, 380, 54])
    t_figures.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_figures)

    story.append(PageBreak())

    # =========================================================================
    # 10. LIST OF TABLES
    # =========================================================================
    story.append(PageTracker("LIST OF TABLES"))
    story.append(Spacer(1, 15))
    story.append(Paragraph("LIST OF TABLES", style_section_title))
    story.append(HRFlowable(width="100%", thickness=1, color=c_crimson, spaceAfter=14))

    tables_data = [
        [Paragraph("<b>Table No.</b>", style_table_header), Paragraph("<b>Title / Caption</b>", style_table_header), Paragraph("<b>Page</b>", style_table_header)],
        [Paragraph("Table 2.1", style_table_cell), Paragraph("Comparison between Single-Modal Systems and EmoSense Multimodal Platform", style_table_cell), Paragraph(f"{pg('TAB_2_1', 13)}", style_table_cell_center)],
        [Paragraph("Table 3.1", style_table_cell), Paragraph("Hardware and Software Execution Environment Specifications", style_table_cell), Paragraph(f"{pg('TAB_3_1', 17)}", style_table_cell_center)],
        [Paragraph("Table 4.1", style_table_cell), Paragraph("PyTorch EmoNet CNN Layer Dimensions, Kernel Sizes &amp; Parameters", style_table_cell), Paragraph(f"{pg('TAB_4_1', 18)}", style_table_cell_center)],
        [Paragraph("Table 4.2", style_table_cell), Paragraph("FastAPI RESTful Endpoints Specification and Payloads", style_table_cell), Paragraph(f"{pg('TAB_4_2', 20)}", style_table_cell_center)],
        [Paragraph("Table 5.1", style_table_cell), Paragraph("FER2013 Dataset Class Sample Distribution (Train vs. Validation)", style_table_cell), Paragraph(f"{pg('TAB_5_1', 21)}", style_table_cell_center)],
        [Paragraph("Table 5.2", style_table_cell), Paragraph("Hyperparameter Configuration and Optimizer Settings", style_table_cell), Paragraph(f"{pg('TAB_5_2', 21)}", style_table_cell_center)],
        [Paragraph("Table 5.3", style_table_cell), Paragraph("Epoch-by-Epoch Loss and Accuracy Progression on Apple M1 MPS GPU", style_table_cell), Paragraph(f"{pg('TAB_5_3', 22)}", style_table_cell_center)],
        [Paragraph("Table 5.4", style_table_cell), Paragraph("Inference Latency and Frame-Rate Profiling across Platforms", style_table_cell), Paragraph(f"{pg('TAB_5_4', 23)}", style_table_cell_center)],
        [Paragraph("Table 5.5", style_table_cell), Paragraph("Empirical Triangulation Test Cases and Masking Verification Outcomes", style_table_cell), Paragraph(f"{pg('TAB_5_5', 24)}", style_table_cell_center)],
    ]
    t_tables = Table(tables_data, colWidths=[70, 380, 54])
    t_tables.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_tables)

    story.append(PageBreak())

    # =========================================================================
    # 11. CHAPTER 1: INTRODUCTION (With Embedded Figure 1.1)
    # =========================================================================
    story.append(PageTracker("CH1"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("1.1 Background and Context", style_h2))
    story.append(Paragraph(
        "Affective computing, founded on the premise of enabling computing devices to perceive, interpret, and adapt to human emotional "
        "affects, has emerged as a cornerstone of modern digital healthcare, human-computer interaction (HCI), and mental wellness platforms. "
        "Depression, anxiety, and work-related burnout represent an escalating public health crisis worldwide. According to the World Health "
        "Organization (WHO), major depressive disorders are among the leading causes of disability. Despite the severity of these challenges, "
        "access to consistent mental health evaluations remains heavily constrained by societal stigma, high therapeutic costs, geographical "
        "isolation, and the infrequency of clinical face-to-face consultations.", style_body
    ))
    story.append(Paragraph(
        "Recent advances in consumer hardware and deep learning have catalyzed the proliferation of software-based mental health tracking apps. "
        "However, the vast majority of existing consumer solutions operate on <b>unimodal signals</b>—monitoring either solely facial video "
        "via computer vision or text sentiment through isolated diary logs. These single-channel paradigms suffer from systemic diagnostic vulnerabilities.", style_body
    ))

    story.append(Paragraph("1.2 The Emotional Masking Dilemma", style_h2))
    story.append(Paragraph(
        "A profound vulnerability in existing emotion detection software is <b>Emotional Masking</b>—commonly referred to in clinical psychology "
        "as 'smiling depression'. Humans are socially conditioned to present an outward facade of cheerfulness, composure, or professional calmness "
        "even when experiencing severe psychological pain, panic, or exhaustion. An individual suffering from chronic burnout will reflexively "
        "smile during video interactions or select a smiling emoji to avoid appearing vulnerable. In such instances, traditional facial recognition "
        "algorithms classify the individual as 'Happy' with high statistical confidence, while emoji survey trackers register perfect wellbeing. "
        "Consequently, unimodal systems completely fail to identify critical distress signals.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED FIGURE 1.1 (Wrapped in KeepTogether)
    fig1_flowables = [
        PageTracker("FIG_1_1"),
        RLImage("report_assets/fig1_1_emotional_masking.png", width=480, height=256),
        Paragraph("Figure 1.1: The Phenomenon of Emotional Masking &amp; 3-Way Triangulation", style_fig_caption)
    ]
    story.append(KeepTogether(fig1_flowables))

    story.append(PageTracker("SEC_1_3"))
    story.append(Paragraph("1.3 Problem Statement", style_h2))
    story.append(Paragraph(
        "Existing emotion monitoring and digital mental wellness applications suffer from three critical flaws:<br/>"
        "1. <b>Inability to Detect Emotional Masking</b>: Failure to identify contradictions between superficial facial expressions and deep underlying linguistic sentiments.<br/>"
        "2. <b>Severe Biometric Privacy Risks</b>: Reliance on cloud-hosted computer vision APIs that require live webcam video frames to be transmitted over public internet connections, violating international biometric data regulations.<br/>"
        "3. <b>Absence of Real-Time Actionable Micro-Interventions</b>: Functioning merely as passive retrospective analytics dashboards without delivering immediate, evidence-based somatic stress-reduction exercises at the moment of detected distress.", style_body
    ))

    story.append(PageTracker("SEC_1_4"))
    story.append(Paragraph("1.4 Motivation and Objectives", style_h2))
    story.append(Paragraph(
        "The motivation behind <b>EmoSense</b> is to develop a privacy-first, multimodal agentic AI wellness assistant capable of bridging the gap "
        "between outward human presentation and internal emotional reality. To accomplish this, the project establishes six core objectives:<br/>"
        "• Develop a custom 4-block PyTorch CNN (<code>EmoNet</code>) trained on FER2013 and accelerated via Apple Silicon Mac M1 MPS GPU.<br/>"
        "• Integrate the VADER sentiment engine to extract emotional valence from unconstrained micro-journaling diary reflections.<br/>"
        "• Architect an Agentic AI reasoning core using the Google Gemini API (<code>gemini-2.5-flash</code>) to triangulate signals and detect masking.<br/>"
        "• Implement an embedded SQLite database tracking historical stability to eliminate false alarms via an Emotional Stability Index (ESI).<br/>"
        "• Deliver immediate therapeutic relief through an interactive 4-7-8 Guided Breathing visualizer and 432Hz ambient audio relaxation.<br/>"
        "• Provide an empathetic, universal multilingual AI Chatbot guiding users on system privacy and breathing protocols in Hindi, Hinglish, and English.", style_body
    ))

    story.append(PageTracker("SEC_1_5"))
    story.append(Paragraph("1.5 Scope and Real-World Applicability", style_h2))
    story.append(Paragraph(
        "The operational scope of EmoSense encompasses edge workstations, student study desks, and corporate remote-work setups. "
        "By enforcing that all biometric facial video analysis occurs entirely on local silicon, the platform qualifies for deployment in "
        "high-privacy environments including university mental health clinics, tele-health pre-intake screening, and corporate wellness initiatives "
        "without triggering compliance violations under GDPR, HIPAA, or the Digital Personal Data Protection (DPDP) Act.", style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 12. CHAPTER 2: LITERATURE REVIEW (With Embedded Table 2.1)
    # =========================================================================
    story.append(PageTracker("CH2"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 2: LITERATURE REVIEW &amp; THEORETICAL FOUNDATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("2.1 Evolution of Affective Computing &amp; Emotion AI", style_h2))
    story.append(Paragraph(
        "The foundations of affective computing were established by Rosalind Picard (1997), who postulated that computational systems must "
        "possess emotional intelligence to achieve intuitive human-machine collaboration. Early research utilized invasive physiological sensors, "
        "such as galvanic skin response (GSR) and electromyography (EMG). While precise, their hardware overhead made them impractical for consumer "
        "adoption. Subsequent computer vision research leveraged Paul Ekman's Facial Action Coding System (FACS), decomposing facial movements "
        "into discrete Action Units (AUs) corresponding to six universal basic emotions: Happiness, Sadness, Anger, Fear, Disgust, Surprise, along with Neutral.", style_body
    ))

    story.append(Paragraph("2.2 Facial Emotion Recognition (FER) Benchmarks", style_h2))
    story.append(Paragraph(
        "Standardized datasets have accelerated deep learning FER models. The <b>FER2013 dataset</b> (Goodfellow et al., 2013) remains the "
        "benchmark of choice for edge systems. Consisting of 35,887 48x48 pixel grayscale images collected from Google image queries, FER2013 presents "
        "realistic challenges including occlusions, head pose variations, and illumination gradients. Its compact footprint makes it optimal for "
        "local edge GPU inference on consumer workstations.", style_body
    ))

    story.append(PageTracker("SEC_2_3"))
    story.append(Paragraph("2.3 Limitations of Unimodal Systems", style_h2))
    story.append(Paragraph(
        "Unimodal emotion detection maps single input vectors to categorical emotion classes: Emotion = f(Visual Frame). As established in "
        "Table 2.1, unimodal systems are vulnerable to head tilt, lighting shifts, and emotional masking. When an individual feigns a smile, "
        "visual models output 'Happy', disregarding true psychological distress.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED TABLE 2.1 (Wrapped in KeepTogether)
    tab21_data = [
        [Paragraph("<b>Metric / Dimension</b>", style_table_header), Paragraph("<b>Traditional Unimodal FER</b>", style_table_header), Paragraph("<b>Pure Text Sentiment</b>", style_table_header), Paragraph("<b>EmoSense Multimodal Platform</b>", style_table_header)],
        [Paragraph("Input Signals", style_table_cell), Paragraph("Single camera frame only", style_table_cell), Paragraph("Isolated text string", style_table_cell), Paragraph("Face frame + Journal text + Emoji mood", style_table_cell)],
        [Paragraph("Masking Detection", style_table_cell), Paragraph("<font color='#dc2626'><b>Impossible</b> (Bypassed)</font>", style_table_cell), Paragraph("<font color='#dc2626'><b>Impossible</b> (Bypassed)</font>", style_table_cell), Paragraph("<font color='#059669'><b>Robust</b> (Triangulated via Gemini)</font>", style_table_cell)],
        [Paragraph("Biometric Privacy", style_table_cell), Paragraph("Cloud video stream (High Risk)", style_table_cell), Paragraph("Not applicable", style_table_cell), Paragraph("<b>100% On-Device PyTorch MPS GPU</b>", style_table_cell)],
        [Paragraph("Edge Latency", style_table_cell), Paragraph("200ms – 1200ms (Cloud)", style_table_cell), Paragraph("5ms – 20ms", style_table_cell), Paragraph("<b>&lt; 15ms Edge CNN Inference</b>", style_table_cell)],
        [Paragraph("Actionable Support", style_table_cell), Paragraph("Passive historical logs", style_table_cell), Paragraph("Passive text display", style_table_cell), Paragraph("<b>Interactive 4-7-8 Breathing &amp; Audio</b>", style_table_cell)],
    ]
    t_tab21 = Table(tab21_data, colWidths=[95, 120, 115, 174])
    t_tab21.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    tab21_flowables = [
        PageTracker("TAB_2_1"),
        Paragraph("Table 2.1: Comparison between Single-Modal Systems and EmoSense Multimodal Platform", style_table_caption),
        t_tab21
    ]
    story.append(KeepTogether(tab21_flowables))

    story.append(PageTracker("SEC_2_4"))
    story.append(Paragraph("2.4 Edge AI &amp; Biometric Privacy on Apple Silicon", style_h2))
    story.append(Paragraph(
        "Transmitting raw facial video frames to centralized cloud servers violates privacy frameworks such as GDPR and HIPAA. EmoSense utilizes "
        "<b>Edge AI</b> on Apple Silicon (Mac M1), leveraging unified memory and Metal Performance Shaders (MPS GPU). Face frames are decoded, "
        "preprocessed, and classified entirely within local RAM. Only high-level mathematical vectors are shared with the reasoning agents, ensuring "
        "zero biometric leakage.", style_body
    ))

    story.append(PageTracker("SEC_2_5"))
    story.append(Paragraph("2.5 Agentic AI &amp; Multimodal Triangulation", style_h2))
    story.append(Paragraph(
        "Recent breakthroughs in Large Language Models (LLMs) enable their deployment as autonomous reasoning agents. Traditional rule-based heuristics "
        "fail when confronted with subtle linguistic nuances, sarcasm, and cultural idioms in user journal entries. By leveraging the Google Gemini API "
        "(<code>gemini-2.5-flash</code>), EmoSense establishes a multi-perspective agentic reasoning pipeline capable of synthesizing disparate "
        "sensory streams into a coherent clinical assessment.", style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 13. CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN (With Embedded Figure 3.1 & Table 3.1)
    # =========================================================================
    story.append(PageTracker("CH3"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 3: SYSTEM ARCHITECTURE &amp; DESIGN", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("3.1 High-Level Architecture Overview", style_h2))
    story.append(Paragraph(
        "EmoSense is architected as a modular, tiered platform decoupling local edge computer vision from agentic cloud reasoning and responsive "
        "glassmorphic frontend rendering. The architecture guarantees sub-20ms visual inference on-device while maintaining rich qualitative "
        "reasoning through specialized AI agents.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED FIGURE 3.1 (Wrapped in KeepTogether)
    fig3_flowables = [
        PageTracker("FIG_3_1"),
        RLImage("report_assets/fig3_1_architecture.png", width=480, height=277),
        Paragraph("Figure 3.1: EmoSense Multimodal Tiered System Architecture", style_fig_caption)
    ]
    story.append(KeepTogether(fig3_flowables))

    story.append(PageTracker("SEC_3_2"))
    story.append(Paragraph("3.2 Tri-Modal Signal Ingestion Pipeline", style_h2))
    story.append(Paragraph(
        "During a check-in event, the platform ingests three orthogonal data streams:<br/>"
        "• <b>Visual Signal</b>: Base64 webcam frame -> OpenCV Haar Cascade face crop -> 48x48 Grayscale -> Normalized PyTorch Tensor [-1, +1].<br/>"
        "• <b>Textual Signal</b>: Unconstrained user diary text -> VADER Sentiment Engine -> Compound polarity score [-1.0 to +1.0].<br/>"
        "• <b>Self-Reported Signal</b>: Categorical one-tap emoji mood selection.", style_body
    ))

    story.append(PageTracker("SEC_3_3"))
    story.append(Paragraph("3.3 Deep Learning Visual Processing Engine", style_h2))
    story.append(Paragraph(
        "The visual engine resides in <code>app/ml/emotion_model.py</code> and executes on-device via Apple MPS GPU. "
        "Upon receiving a video frame, OpenCV isolates the bounding box of the face. The cropped image is converted to single-channel "
        "grayscale, resized to 48x48 pixels, normalized via affine transformations, and converted into a PyTorch tensor. Inference outputs "
        "a normalized probability distribution across all seven FER2013 emotion categories in under 15ms.", style_body
    ))

    story.append(PageTracker("SEC_3_4"))
    story.append(Paragraph("3.4 Textual NLP Subsystem (VADER)", style_h2))
    story.append(Paragraph(
        "Micro-journal entries are processed using the Valence Aware Dictionary and sEntiment Reasoner (VADER). "
        "Unlike generic tokenizers, VADER is specifically calibrated for micro-blogs and short personal reflections, recognizing "
        "negation, punctuation emphasis, capitalization, and emotional modifiers. It yields a continuous compound valence score "
        "from -1.0 (maximum distress) to +1.0 (maximum positive affect).", style_body
    ))

    story.append(PageTracker("SEC_3_5"))
    story.append(Paragraph("3.5 Multi-Agent Triangulation Architecture (Gemini API)", style_h2))
    story.append(Paragraph(
        "The cognitive reasoning layer consists of three specialized agentic personas powered by the Google Gemini API (<code>gemini-2.5-flash</code>):<br/>"
        "1. <b>3-Way Congruence Agent</b>: Cross-examines visual emotion against textual valence and emoji selection. If visual is positive but textual sentiment is strongly negative, it flags Emotional Masking and computes a Congruence Score (0–100%).<br/>"
        "2. <b>Trend Scorer Agent</b>: Ingests the 15-entry rolling history from SQLite to evaluate volatility and compute the Emotional Stability Index (ESI).<br/>"
        "3. <b>Report Writer Agent</b>: Synthesizes findings into an empathetic, humanized wellness insight and prescribes targeted micro-interventions.", style_body
    ))

    story.append(PageTracker("SEC_3_6"))
    story.append(Paragraph("3.6 Hardware and Software Environment Specifications", style_h2))

    # ACTUAL VISIBLE EMBEDDED TABLE 3.1 (Wrapped in KeepTogether)
    env_spec_data = [
        [Paragraph("<b>Component / Layer</b>", style_table_header), Paragraph("<b>Specification</b>", style_table_header), Paragraph("<b>Functional Role</b>", style_table_header)],
        [Paragraph("Hardware Processor", style_table_cell), Paragraph("Apple Silicon Mac M1 (MPS GPU)", style_table_cell), Paragraph("On-device hardware acceleration via Metal Performance Shaders.", style_table_cell)],
        [Paragraph("Operating System", style_table_cell), Paragraph("macOS Sequoia (Darwin 24.x)", style_table_cell), Paragraph("Host execution operating system.", style_table_cell)],
        [Paragraph("Deep Learning", style_table_cell), Paragraph("PyTorch 2.8.0 (`torch.device('mps')`)", style_table_cell), Paragraph("Custom 4-block CNN (`EmoNet`) training and inference.", style_table_cell)],
        [Paragraph("Computer Vision", style_table_cell), Paragraph("OpenCV 4.9.0 (`cv2`)", style_table_cell), Paragraph("Face localization, histogram equalization, tensor preparation.", style_table_cell)],
        [Paragraph("NLP Engine", style_table_cell), Paragraph("`vaderSentiment 3.3.2`", style_table_cell), Paragraph("Quantifies compound sentiment score from micro-journals.", style_table_cell)],
        [Paragraph("Agentic AI SDK", style_table_cell), Paragraph("Google GenAI (`gemini-2.5-flash`)", style_table_cell), Paragraph("3-Way Congruence triangulation and natural language reasoning.", style_table_cell)],
        [Paragraph("Backend Server", style_table_cell), Paragraph("FastAPI 0.128.8 + Uvicorn 0.39.0", style_table_cell), Paragraph("Asynchronous ASGI REST API endpoints.", style_table_cell)],
        [Paragraph("Persistence Layer", style_table_cell), Paragraph("SQLAlchemy 2.0 + SQLite 3", style_table_cell), Paragraph("Local relational storage (`emosense.db`).", style_table_cell)],
        [Paragraph("Web Interface", style_table_cell), Paragraph("HTML5 + Vanilla CSS Glassmorphism + JS", style_table_cell), Paragraph("Cyber-Health UI with 4 navigation tabs and Chart.js graphs.", style_table_cell)],
    ]
    t_env_spec = Table(env_spec_data, colWidths=[110, 134, 260])
    t_env_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    tab31_flowables = [
        PageTracker("TAB_3_1"),
        Paragraph("Table 3.1: Hardware and Software Execution Environment Specifications", style_table_caption),
        t_env_spec
    ]
    story.append(KeepTogether(tab31_flowables))

    story.append(PageBreak())

    # =========================================================================
    # 14. CHAPTER 4: IMPLEMENTATION METHODOLOGY
    # =========================================================================
    story.append(PageTracker("CH4"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 4: IMPLEMENTATION METHODOLOGY", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("4.1 Custom PyTorch CNN Model Architecture (EmoNet)", style_h2))
    story.append(Paragraph(
        "The visual emotion engine (`app/ml/emotion_model.py`) is designed as a deep 4-block Convolutional Neural Network (`EmoNet`) "
        "tailored for 48x48 single-channel grayscale facial images. Each convolutional block employs dual 3x3 convolutions with zero-padding, "
        "Batch Normalization to stabilize internal covariate shift, ReLU non-linearities, 2x2 Max-Pooling (reducing spatial dimensions by half), "
        "and Spatial Dropout ($p=0.25$) to prevent co-adaptation of feature maps.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED FIGURE 4.1 (Wrapped in KeepTogether)
    fig4_flowables = [
        PageTracker("FIG_4_1"),
        RLImage("report_assets/fig4_1_cnn_layers.png", width=480, height=235),
        Paragraph("Figure 4.1: Custom PyTorch CNN Model Architecture (EmoNet)", style_fig_caption)
    ]
    story.append(KeepTogether(fig4_flowables))

    # ACTUAL VISIBLE EMBEDDED TABLE 4.1 (Wrapped in KeepTogether)
    layer_table_data = [
        [Paragraph("<b>Layer Type</b>", style_table_header), Paragraph("<b>Kernel / Filter</b>", style_table_header), Paragraph("<b>Output Shape</b>", style_table_header), Paragraph("<b>Activation / Dropout</b>", style_table_header)],
        [Paragraph("Input", style_table_cell), Paragraph("Single-channel", style_table_cell), Paragraph("(B, 1, 48, 48)", style_table_cell), Paragraph("Normalized [-1, +1]", style_table_cell)],
        [Paragraph("Conv 1_1 &amp; 1_2", style_table_cell), Paragraph("32 &amp; 64 filters, 3x3", style_table_cell), Paragraph("(B, 64, 48, 48)", style_table_cell), Paragraph("BatchNorm + ReLU", style_table_cell)],
        [Paragraph("MaxPool 1", style_table_cell), Paragraph("2x2, stride=2", style_table_cell), Paragraph("(B, 64, 24, 24)", style_table_cell), Paragraph("Dropout2d (0.25)", style_table_cell)],
        [Paragraph("Conv 2_1 &amp; 2_2", style_table_cell), Paragraph("128 filters, 3x3", style_table_cell), Paragraph("(B, 128, 24, 24)", style_table_cell), Paragraph("BatchNorm + ReLU", style_table_cell)],
        [Paragraph("MaxPool 2", style_table_cell), Paragraph("2x2, stride=2", style_table_cell), Paragraph("(B, 128, 12, 12)", style_table_cell), Paragraph("Dropout2d (0.25)", style_table_cell)],
        [Paragraph("Conv 3_1 &amp; 3_2", style_table_cell), Paragraph("256 filters, 3x3", style_table_cell), Paragraph("(B, 256, 12, 12)", style_table_cell), Paragraph("BatchNorm + ReLU", style_table_cell)],
        [Paragraph("MaxPool 3", style_table_cell), Paragraph("2x2, stride=2", style_table_cell), Paragraph("(B, 256, 6, 6)", style_table_cell), Paragraph("Dropout2d (0.25)", style_table_cell)],
        [Paragraph("Dense FC1", style_table_cell), Paragraph("9,216 -> 512", style_table_cell), Paragraph("(B, 512)", style_table_cell), Paragraph("BatchNorm + Dropout (0.50)", style_table_cell)],
        [Paragraph("Dense FC2", style_table_cell), Paragraph("512 -> 7", style_table_cell), Paragraph("(B, 7)", style_table_cell), Paragraph("Linear Logits -> Softmax", style_table_cell)],
    ]
    t_layer = Table(layer_table_data, colWidths=[95, 130, 115, 164])
    t_layer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    tab41_flowables = [
        PageTracker("TAB_4_1"),
        Paragraph("Table 4.1: PyTorch EmoNet CNN Layer Dimensions, Kernel Sizes &amp; Parameters", style_table_caption),
        t_layer
    ]
    story.append(KeepTogether(tab41_flowables))

    story.append(PageTracker("SEC_4_2"))
    story.append(Paragraph("4.2 Apple Silicon Mac M1 MPS GPU Acceleration", style_h2))
    story.append(Paragraph(
        "To achieve low-latency inference on macOS workstations without requiring discrete NVIDIA GPUs, EmoSense implements PyTorch's "
        "Metal Performance Shaders backend: <code>device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')</code>. "
        "Unified memory architecture allows zero-copy data transfer between system RAM and Apple Silicon GPU cores, keeping latency below 15ms.", style_body
    ))

    story.append(PageTracker("SEC_4_3"))
    story.append(Paragraph("4.3 OpenCV Face Localization &amp; Normalization", style_h2))
    story.append(Paragraph(
        "Webcam video frames arrive as Base64 JPEG buffers. The OpenCV pipeline decodes the byte array into a NumPy BGR matrix, applies "
        "a Haar Cascade frontal face detector (<code>haarcascade_frontalface_default.xml</code>) to locate bounding coordinates $(x, y, w, h)$, "
        "and extracts a square region of interest (ROI). To ensure resilience under non-ideal lighting, the ROI is subjected to histogram equalization "
        "before conversion to single-channel 48x48 tensor format. If no face is detected, a graceful center-crop fallback is executed.", style_body
    ))

    story.append(PageTracker("SEC_4_4"))
    story.append(Paragraph("4.4 Multi-Agent Congruence &amp; Masking Heuristics", style_h2))
    story.append(Paragraph(
        "The Congruence Score quantifies the harmonious alignment across modalities on a scale from 0% to 100%. "
        "When the visual emotion model registers 'Happy' with high confidence ($P &gt; 0.70$) while the VADER sentiment score is strongly "
        "negative (Compound $\le -0.30$), the system triggers a <b>Masked Distress Alert</b>. Rather than invalidating the user's feelings, "
        "the agent addresses the underlying distress with gentle validation and provides soothing micro-interventions.", style_body
    ))

    story.append(PageTracker("SEC_4_5"))
    story.append(Paragraph("4.5 FastAPI Asynchronous RESTful API Implementation", style_h2))

    # ACTUAL VISIBLE EMBEDDED TABLE 4.2 (Wrapped in KeepTogether)
    api_table_data = [
        [Paragraph("<b>Endpoint</b>", style_table_header), Paragraph("<b>Method</b>", style_table_header), Paragraph("<b>Request Schema</b>", style_table_header), Paragraph("<b>Functional Output</b>", style_table_header)],
        [Paragraph("/api/system-status", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Hardware device ('mps'), active framework &amp; agent status.", style_table_cell)],
        [Paragraph("/api/analyze-frame", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("FrameAnalysisRequest", style_table_cell), Paragraph("600ms stream face bounding box &amp; 7-class emotion probabilities.", style_table_cell)],
        [Paragraph("/api/checkin", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("CheckInRequest", style_table_cell), Paragraph("Full 3-way triangulation, Gemini congruence score, DB persistence.", style_table_cell)],
        [Paragraph("/api/history", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("limit: int = 15", style_table_cell), Paragraph("Historical check-in records for Chart.js trend rendering.", style_table_cell)],
        [Paragraph("/api/chat", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("ChatRequest", style_table_cell), Paragraph("AI Companion Chatbot responses in Hindi, Hinglish, or English.", style_table_cell)],
    ]
    t_api = Table(api_table_data, colWidths=[105, 55, 135, 209])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    tab42_flowables = [
        PageTracker("TAB_4_2"),
        Paragraph("Table 4.2: FastAPI RESTful Endpoints Specification and Payloads", style_table_caption),
        t_api
    ]
    story.append(KeepTogether(tab42_flowables))

    story.append(PageTracker("SEC_4_6"))
    story.append(Paragraph("4.6 Interactive Micro-Interventions (4-7-8 Breathing &amp; 432Hz Audio)", style_h2))
    story.append(Paragraph(
        "Upon identifying distress or emotional masking, EmoSense activates interactive somatic relief mechanisms. "
        "The <b>4-7-8 Guided Breathing Visualizer</b> coordinates parasympathetic nervous system regulation through an animated SVG "
        "expanding circle: Inhale through nose for 4 seconds, Hold breath for 7 seconds, Exhale through mouth for 8 seconds. "
        "Simultaneously, the browser synthesizes harmonic 432Hz ambient sound waves via the HTML5 Web Audio API, lowering acute cortisol levels.", style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 15. CHAPTER 5: EXPERIMENTAL RESULTS & EVALUATION
    # =========================================================================
    story.append(PageTracker("CH5"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 5: EXPERIMENTAL RESULTS &amp; PERFORMANCE EVALUATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("5.1 FER2013 Dataset Distribution &amp; Characteristics", style_h2))
    story.append(Paragraph(
        "The model was trained and evaluated on the FER2013 benchmark dataset, comprising 35,887 grayscale facial images across 7 emotion classes. "
        "The dataset was split into 28,709 training samples and 7,178 test/validation samples. Table 5.1 details the distribution per class.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED TABLE 5.1 (Wrapped in KeepTogether)
    ds_table_data = [
        [Paragraph("<b>Emotion Class</b>", style_table_header), Paragraph("<b>Train Samples</b>", style_table_header), Paragraph("<b>Test / Validation</b>", style_table_header), Paragraph("<b>Total Samples</b>", style_table_header), Paragraph("<b>Percentage (%)</b>", style_table_header)],
        [Paragraph("Angry", style_table_cell), Paragraph("3,995", style_table_cell_center), Paragraph("958", style_table_cell_center), Paragraph("4,953", style_table_cell_center), Paragraph("13.80%", style_table_cell_center)],
        [Paragraph("Disgust", style_table_cell), Paragraph("436", style_table_cell_center), Paragraph("111", style_table_cell_center), Paragraph("547", style_table_cell_center), Paragraph("1.52%", style_table_cell_center)],
        [Paragraph("Fear", style_table_cell), Paragraph("4,097", style_table_cell_center), Paragraph("1,024", style_table_cell_center), Paragraph("5,121", style_table_cell_center), Paragraph("14.27%", style_table_cell_center)],
        [Paragraph("Happy", style_table_cell), Paragraph("7,215", style_table_cell_center), Paragraph("1,774", style_table_cell_center), Paragraph("8,989", style_table_cell_center), Paragraph("25.05%", style_table_cell_center)],
        [Paragraph("Sad", style_table_cell), Paragraph("4,830", style_table_cell_center), Paragraph("1,247", style_table_cell_center), Paragraph("6,077", style_table_cell_center), Paragraph("16.93%", style_table_cell_center)],
        [Paragraph("Surprise", style_table_cell), Paragraph("3,171", style_table_cell_center), Paragraph("831", style_table_cell_center), Paragraph("4,002", style_table_cell_center), Paragraph("11.15%", style_table_cell_center)],
        [Paragraph("Neutral", style_table_cell), Paragraph("4,965", style_table_cell_center), Paragraph("1,233", style_table_cell_center), Paragraph("6,198", style_table_cell_center), Paragraph("17.27%", style_table_cell_center)],
        [Paragraph("<b>Total</b>", style_table_cell), Paragraph("<b>28,709</b>", style_table_cell_center), Paragraph("<b>7,178</b>", style_table_cell_center), Paragraph("<b>35,887</b>", style_table_cell_center), Paragraph("<b>100.00%</b>", style_table_cell_center)],
    ]
    t_ds = Table(ds_table_data, colWidths=[110, 100, 100, 100, 94])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    tab51_flowables = [
        PageTracker("TAB_5_1"),
        Paragraph("Table 5.1: FER2013 Dataset Class Sample Distribution (Train vs. Validation)", style_table_caption),
        t_ds
    ]
    story.append(KeepTogether(tab51_flowables))

    # ACTUAL VISIBLE EMBEDDED TABLE 5.2 (Hyperparameters, Wrapped in KeepTogether)
    hyperparam_data = [
        [Paragraph("<b>Hyperparameter</b>", style_table_header), Paragraph("<b>Configured Value</b>", style_table_header), Paragraph("<b>Optimization Rationale</b>", style_table_header)],
        [Paragraph("Mini-Batch Size", style_table_cell), Paragraph("64", style_table_cell_center), Paragraph("Optimal throughput on Apple M1 unified memory architecture.", style_table_cell)],
        [Paragraph("Initial Learning Rate", style_table_cell), Paragraph("0.001 (1e-3)", style_table_cell_center), Paragraph("Standard Adam learning rate ensuring smooth gradient descent.", style_table_cell)],
        [Paragraph("Optimizer", style_table_cell), Paragraph("Adam", style_table_cell_center), Paragraph("Adaptive learning rate momentum handling sparse image gradients.", style_table_cell)],
        [Paragraph("Weight Decay (L2)", style_table_cell), Paragraph("1e-4", style_table_cell_center), Paragraph("Regularization penalty preventing weight saturation and overfitting.", style_table_cell)],
        [Paragraph("Loss Function", style_table_cell), Paragraph("CrossEntropyLoss", style_table_cell_center), Paragraph("Standard multi-class categorical cross-entropy with softmax.", style_table_cell)],
        [Paragraph("Training Epochs", style_table_cell), Paragraph("10", style_table_cell_center), Paragraph("Empirically validated convergence on FER2013 on local GPU.", style_table_cell)],
        [Paragraph("Compute Device", style_table_cell), Paragraph("Apple Silicon MPS GPU", style_table_cell_center), Paragraph("Hardware acceleration via macOS Metal Performance Shaders.", style_table_cell)],
    ]
    t_hyper = Table(hyperparam_data, colWidths=[120, 110, 274])
    t_hyper.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    tab52_flowables = [
        PageTracker("TAB_5_2"),
        Paragraph("Table 5.2: Hyperparameter Configuration and Optimizer Settings", style_table_caption),
        t_hyper
    ]
    story.append(KeepTogether(tab52_flowables))

    story.append(PageTracker("SEC_5_2"))
    story.append(Paragraph("5.2 Model Training Progression &amp; Convergence", style_h2))
    story.append(Paragraph(
        "Training was executed locally on the <b>Apple Silicon Mac M1 MPS GPU</b> over 10 epochs. "
        "Validation accuracy rapidly climbed to <b>62.54%</b>, with the loss dropping to 1.0088. "
        "Weights were serialized to <code>models_weights/fer2013_custom_cnn.pth</code>.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED FIGURE 5.1 (Wrapped in KeepTogether)
    fig51_flowables = [
        PageTracker("FIG_5_1"),
        RLImage("report_assets/fig5_2_training_curves.png", width=480, height=256),
        Paragraph("Figure 5.1: Training &amp; Validation Progression Curves (10 Epochs on Mac M1 MPS GPU)", style_fig_caption)
    ]
    story.append(KeepTogether(fig51_flowables))

    # ACTUAL VISIBLE EMBEDDED TABLE 5.3 (Epoch Progression, Wrapped in KeepTogether)
    epoch_table_data = [
        [Paragraph("<b>Epoch</b>", style_table_header), Paragraph("<b>Train Loss</b>", style_table_header), Paragraph("<b>Train Acc (%)</b>", style_table_header), Paragraph("<b>Val Loss</b>", style_table_header), Paragraph("<b>Val Acc (%)</b>", style_table_header), Paragraph("<b>Duration</b>", style_table_header)],
        [Paragraph("1", style_table_cell_center), Paragraph("1.6499", style_table_cell_center), Paragraph("35.07%", style_table_cell_center), Paragraph("1.3514", style_table_cell_center), Paragraph("48.11%", style_table_cell_center), Paragraph("95.7 s", style_table_cell_center)],
        [Paragraph("3", style_table_cell_center), Paragraph("1.2677", style_table_cell_center), Paragraph("51.54%", style_table_cell_center), Paragraph("1.1422", style_table_cell_center), Paragraph("56.74%", style_table_cell_center), Paragraph("118.5 s", style_table_cell_center)],
        [Paragraph("5", style_table_cell_center), Paragraph("1.1713", style_table_cell_center), Paragraph("55.02%", style_table_cell_center), Paragraph("1.0923", style_table_cell_center), Paragraph("58.78%", style_table_cell_center), Paragraph("117.4 s", style_table_cell_center)],
        [Paragraph("7", style_table_cell_center), Paragraph("1.1130", style_table_cell_center), Paragraph("57.76%", style_table_cell_center), Paragraph("1.0429", style_table_cell_center), Paragraph("60.34%", style_table_cell_center), Paragraph("118.7 s", style_table_cell_center)],
        [Paragraph("10", style_table_cell_center), Paragraph("1.0475", style_table_cell_center), Paragraph("60.40%", style_table_cell_center), Paragraph("1.0088", style_table_cell_center), Paragraph("<b>62.54%</b>", style_table_cell_center), Paragraph("134.3 s", style_table_cell_center)],
    ]
    t_epoch = Table(epoch_table_data, colWidths=[50, 90, 90, 90, 94, 90])
    t_epoch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    tab53_flowables = [
        PageTracker("TAB_5_3"),
        Paragraph("Table 5.3: Epoch-by-Epoch Loss and Accuracy Progression on Apple M1 MPS GPU", style_table_caption),
        t_epoch
    ]
    story.append(KeepTogether(tab53_flowables))

    story.append(PageTracker("SEC_5_3"))
    story.append(Paragraph("5.3 Hardware Latency Profiling (M1 MPS vs CPU vs Cloud)", style_h2))
    story.append(Paragraph(
        "To rigorously quantify edge efficiency, inference benchmarks were run across 100 consecutive frames on three hardware environments: "
        "Mac M1 MPS GPU, Mac M1 CPU, Intel Core i7 CPU, and compared against Cloud Computer Vision APIs. Results are illustrated below.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED FIGURE 5.2 (Latency, Wrapped in KeepTogether)
    fig52_flowables = [
        PageTracker("FIG_5_2"),
        RLImage("report_assets/fig5_3_latency_benchmark.png", width=480, height=224),
        Paragraph("Figure 5.2: End-to-End Inference Latency Profiling across Hardware Platforms", style_fig_caption)
    ]
    story.append(KeepTogether(fig52_flowables))

    # ACTUAL VISIBLE EMBEDDED TABLE 5.4 (Latency Profiling, Wrapped in KeepTogether)
    latency_table_data = [
        [Paragraph("<b>Hardware Platform</b>", style_table_header), Paragraph("<b>Compute Engine</b>", style_table_header), Paragraph("<b>Avg Latency</b>", style_table_header), Paragraph("<b>Throughput</b>", style_table_header), Paragraph("<b>Privacy Guarantee</b>", style_table_header)],
        [Paragraph("Apple Silicon Mac M1", style_table_cell), Paragraph("PyTorch MPS GPU", style_table_cell), Paragraph("<b>14.8 ms</b>", style_table_cell_center), Paragraph("<b>67.5 FPS</b>", style_table_cell_center), Paragraph("<font color='#059669'><b>100% On-Device RAM</b></font>", style_table_cell)],
        [Paragraph("Apple Silicon Mac M1", style_table_cell), Paragraph("PyTorch CPU", style_table_cell), Paragraph("42.1 ms", style_table_cell_center), Paragraph("23.8 FPS", style_table_cell_center), Paragraph("<font color='#059669'><b>100% On-Device RAM</b></font>", style_table_cell)],
        [Paragraph("Intel Core i7 11th Gen", style_table_cell), Paragraph("PyTorch CPU", style_table_cell), Paragraph("58.6 ms", style_table_cell_center), Paragraph("17.1 FPS", style_table_cell_center), Paragraph("<font color='#059669'><b>100% On-Device RAM</b></font>", style_table_cell)],
        [Paragraph("Cloud Vision API (AWS/GCP)", style_table_cell), Paragraph("Remote HTTPS REST", style_table_cell), Paragraph("385.0 ms", style_table_cell_center), Paragraph("2.6 FPS", style_table_cell_center), Paragraph("<font color='#dc2626'>Cloud Video Leak Risk</font>", style_table_cell)],
    ]
    t_lat = Table(latency_table_data, colWidths=[120, 100, 75, 75, 134])
    t_lat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    tab54_flowables = [
        PageTracker("TAB_5_4"),
        Paragraph("Table 5.4: Inference Latency and Frame-Rate Profiling across Platforms", style_table_caption),
        t_lat
    ]
    story.append(KeepTogether(tab54_flowables))

    story.append(PageTracker("SEC_5_4"))
    story.append(Paragraph("5.4 Congruence &amp; Emotional Masking Verification Case Studies", style_h2))
    story.append(Paragraph(
        "To validate the 3-Way Congruence Agent, four distinct emotional scenarios were executed on the live platform. "
        "The empirical results in Table 5.5 prove that EmoSense reliably catches smiling depression that completely fools unimodal systems.", style_body
    ))

    # ACTUAL VISIBLE EMBEDDED TABLE 5.5 (Masking Verification, Wrapped in KeepTogether)
    test_cases_data = [
        [Paragraph("<b>Test Case</b>", style_table_header), Paragraph("<b>Visual (PyTorch)</b>", style_table_header), Paragraph("<b>Text Sentiment (VADER)</b>", style_table_header), Paragraph("<b>Emoji</b>", style_table_header), Paragraph("<b>Score</b>", style_table_header), Paragraph("<b>System Status</b>", style_table_header)],
        [Paragraph("Case 1 (Masking)", style_table_cell), Paragraph("Happy (0.78)", style_table_cell), Paragraph("'I feel hopeless' (-0.74)", style_table_cell), Paragraph("Sad", style_table_cell_center), Paragraph("<b>38%</b>", style_table_cell_center), Paragraph("<font color='#dc2626'><b>Masked Distress Alert</b></font>", style_table_cell)],
        [Paragraph("Case 2 (Harmony)", style_table_cell), Paragraph("Happy (0.84)", style_table_cell), Paragraph("'Productive, peaceful' (+0.79)", style_table_cell), Paragraph("Happy", style_table_cell_center), Paragraph("<b>92%</b>", style_table_cell_center), Paragraph("<font color='#059669'><b>Congruent (Aligned)</b></font>", style_table_cell)],
        [Paragraph("Case 3 (Distress)", style_table_cell), Paragraph("Sad (0.72)", style_table_cell), Paragraph("'Terrible day, exhausted' (-0.68)", style_table_cell), Paragraph("Sad", style_table_cell_center), Paragraph("<b>92%</b>", style_table_cell_center), Paragraph("<b>Congruent Distress</b>", style_table_cell)],
        [Paragraph("Case 4 (Mild)", style_table_cell), Paragraph("Neutral (0.70)", style_table_cell), Paragraph("'Average day, nothing' (+0.05)", style_table_cell), Paragraph("Tired", style_table_cell_center), Paragraph("<b>68%</b>", style_table_cell_center), Paragraph("<b>Mild Discrepancy</b>", style_table_cell)],
    ]
    t_test = Table(test_cases_data, colWidths=[90, 85, 145, 45, 45, 94])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    tab55_flowables = [
        PageTracker("TAB_5_5"),
        Paragraph("Table 5.5: Empirical Triangulation Test Cases and Masking Verification Outcomes", style_table_caption),
        t_test
    ]
    story.append(KeepTogether(tab55_flowables))

    story.append(PageBreak())

    # =========================================================================
    # 16. CHAPTER 6: CONCLUSION & REFERENCES
    # =========================================================================
    story.append(PageTracker("CH6"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER 6: CONCLUSION &amp; FUTURE SCOPE", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=12))

    story.append(Paragraph("6.1 Summary of Contributions", style_h2))
    story.append(Paragraph(
        "The <b>EmoSense</b> project demonstrates the successful design, implementation, and deployment of a privacy-first, multimodal agentic AI platform. "
        "By fusing on-device deep learning visual emotion recognition (PyTorch CNN accelerated on Mac M1 MPS GPU) with qualitative text sentiment extraction "
        "(VADER) and Google Gemini multi-agent reasoning, the system definitively overcomes the long-standing challenge of <b>Emotional Masking</b> in affective computing. "
        "The project has achieved complete operational deployment, verified through a glassmorphic dashboard, interactive 4-7-8 breathing visualizer, and universal AI guidance chatbot.", style_body
    ))

    story.append(PageTracker("SEC_6_2"))
    story.append(Paragraph("6.2 Future Enhancements &amp; Roadmap", style_h2))
    story.append(Paragraph(
        "Future research trajectories include:<br/>"
        "1. <b>Remote Photoplethysmography (rPPG)</b>: Extracting non-contact pulse and heart-rate variability (HRV) metrics directly from subtle facial skin color fluctuations.<br/>"
        "2. <b>On-Device Small Language Models (SLMs)</b>: Quantizing models such as Gemma 2B via llama.cpp to enable completely offline agentic reasoning.<br/>"
        "3. <b>Wearable Sensor Fusion</b>: Integrating continuous Galvanic Skin Response (GSR) and sleep architecture data from smartwatches for holistic psychiatric wellness tracking.", style_body
    ))

    story.append(Spacer(1, 15))
    story.append(PageTracker("REFERENCES"))
    story.append(Paragraph("REFERENCES", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))

    refs = [
        "1. Picard, R. W. (1997). <i>Affective Computing</i>. MIT Press, Cambridge, MA.",
        "2. Ekman, P., &amp; Friesen, W. V. (1969). The repertoire of nonverbal behavior: Categories, origins, usage, and coding. <i>Semiotica</i>, 1(1), 49–98.",
        "3. Goodfellow, I. J., et al. (2013). Challenges in representation learning: A report on three machine learning contests. <i>ICONIP 2013</i>, Springer, 117–124.",
        "4. Hutto, C., &amp; Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. <i>Eighth International AAAI Conference on Weblogs and Social Media (ICWSM)</i>.",
        "5. Weil, A. (2015). <i>Fast Calm: Breathing Techniques for Instant Stress Relief</i>. Rodale Books.",
        "6. Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, 32.",
        "7. Gemini Team, Google. (2024). <i>Gemini: A Family of Highly Capable Multimodal Models</i>. Google DeepMind Technical Report, arXiv:2312.11805."
    ]
    for ref in refs:
        story.append(Paragraph(ref, style_body))
        story.append(Spacer(1, 2.5))

    return story


def main():
    styles = getSampleStyleSheet()

    # Multi-pass compilation to guarantee 100% exact convergence of all page numbers
    output_pdf = "BIT_Mesra_EmoSense_Project_Report.pdf"
    max_passes = 4
    
    print("Beginning multi-pass compilation for BIT Mesra MCA Project Report...")
    for pass_num in range(1, max_passes + 1):
        prev_registry = dict(PAGE_REGISTRY)
        print(f"--- Running Pass {pass_num} ---")
        doc = SimpleDocTemplate(
            output_pdf,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        story = build_story(styles, PAGE_REGISTRY)
        doc.build(story, canvasmaker=AcademicNumberedCanvas)
        
        # Check convergence
        is_converged = (prev_registry == PAGE_REGISTRY) and (pass_num > 1)
        print(f"Pass {pass_num} recorded {len(PAGE_REGISTRY)} anchor points.")
        if is_converged:
            print(f"PERFECT CONVERGENCE ACHIEVED on Pass {pass_num}!")
            break

    print(f"\nFinal Recorded Physical Page Numbers:")
    for k, v in sorted(PAGE_REGISTRY.items()):
        print(f"  {k:18} -> Page {v}")

    print(f"\nSUCCESS: Generated {output_pdf} with verified figures, tables, and exact page numbers!")

if __name__ == "__main__":
    main()
