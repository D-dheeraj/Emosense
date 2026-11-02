import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Try system fonts, fall back to default
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNSText.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_figure_1_1():
    """Figure 1.1: Emotional Masking Conceptual Triangulation"""
    w, h = 900, 480
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, True)
    f_sub = get_font(13)
    f_box_title = get_font(15, True)
    f_box_text = get_font(12)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    draw.text((30, 24), "Figure 1.1: The Phenomenon of Emotional Masking & 3-Way Triangulation", fill=(15, 23, 42), font=f_title)
    draw.text((30, 52), "Contrasting superficial outward presentation against deep internal qualitative reflections", fill=(100, 116, 139), font=f_sub)

    # Box 1: Visual Presentation (Smiling / False Positive)
    draw.rounded_rectangle([40, 95, 290, 260], radius=10, fill=(240, 253, 250), outline=(13, 148, 136), width=2)
    draw.text((55, 110), "1. VISUAL MODALITY", fill=(13, 148, 136), font=f_box_title)
    draw.text((55, 135), "• Face: Smiling / Composed", fill=(30, 41, 59), font=f_box_text)
    draw.text((55, 155), "• PyTorch CNN: EmoNet (MPS)", fill=(30, 41, 59), font=f_box_text)
    draw.text((55, 175), "• Dominant: 'Happy' (88%)", fill=(30, 41, 59), font=f_box_text)
    draw.text((55, 205), "[!] Social Smile Facade", fill=(180, 83, 9), font=f_box_title)
    draw.text((55, 230), "Deceptive Unimodal Output", fill=(100, 116, 139), font=f_box_text)

    # Box 2: Textual Journal (True Distress)
    draw.rounded_rectangle([320, 95, 580, 260], radius=10, fill=(254, 242, 242), outline=(225, 29, 72), width=2)
    draw.text((335, 110), "2. TEXTUAL MODALITY", fill=(225, 29, 72), font=f_box_title)
    draw.text((335, 135), "• Journal: 'Feeling hopeless'", fill=(30, 41, 59), font=f_box_text)
    draw.text((335, 155), "• VADER Compound: -0.74", fill=(30, 41, 59), font=f_box_text)
    draw.text((335, 175), "• Text Polarity: Negative", fill=(30, 41, 59), font=f_box_text)
    draw.text((335, 205), "[*] True Somatic Distress", fill=(190, 18, 60), font=f_box_title)
    draw.text((335, 230), "Internal Exhaustion & Anxiety", fill=(100, 116, 139), font=f_box_text)

    # Box 3: Emoji Check-in
    draw.rounded_rectangle([610, 95, 860, 260], radius=10, fill=(248, 250, 252), outline=(100, 116, 139), width=2)
    draw.text((625, 110), "3. SELF-REPORT MOOD", fill=(71, 85, 105), font=f_box_title)
    draw.text((625, 135), "• Selected: Sad Emoji", fill=(30, 41, 59), font=f_box_text)
    draw.text((625, 155), "• Mood Tag: 'Sad / Tired'", fill=(30, 41, 59), font=f_box_text)
    draw.text((625, 175), "• User Consciousness: Low", fill=(30, 41, 59), font=f_box_text)
    draw.text((625, 205), "[i] Confirmatory Signal", fill=(71, 85, 105), font=f_box_title)
    draw.text((625, 230), "Validates Inner Sentiment", fill=(100, 116, 139), font=f_box_text)

    # Arrows pointing down to Triangulation Engine
    draw.line([(165, 260), (165, 305), (450, 305), (450, 320)], fill=(13, 148, 136), width=3)
    draw.line([(450, 260), (450, 320)], fill=(225, 29, 72), width=3)
    draw.line([(735, 260), (735, 305), (450, 305), (450, 320)], fill=(100, 116, 139), width=3)

    # Triangulation Result Box
    draw.rounded_rectangle([120, 320, 780, 450], radius=12, fill=(255, 241, 242), outline=(153, 27, 27), width=3)
    draw.text((145, 335), "3-WAY CONGRUENCE AGENT EVALUATION (GOOGLE GEMINI API)", fill=(153, 27, 27), font=f_box_title)
    draw.text((145, 362), "• Discrepancy Detected: Visual Expression (Happy) contradicts Qualitative Text (Distress).", fill=(30, 41, 59), font=f_box_text)
    draw.text((145, 385), "• Congruence Score: 38% (Low Alignment) | Status: EMOTIONAL MASKING DETECTED", fill=(180, 83, 9), font=f_box_title)
    draw.text((145, 412), "• Action Triggered: Immediate Red Glowing Warning + Interactive 4-7-8 Breathing Reset", fill=(5, 150, 105), font=f_box_text)

    os.makedirs("report_assets", exist_ok=True)
    img.save("report_assets/fig1_1_emotional_masking.png")
    print("Generated: fig1_1_emotional_masking.png")

def create_figure_3_1():
    """Figure 3.1: High-Level System Architecture Diagram"""
    w, h = 900, 520
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, True)
    f_sub = get_font(13)
    f_box_title = get_font(14, True)
    f_box_text = get_font(11.5)

    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    draw.text((30, 22), "Figure 3.1: EmoSense Multimodal Tiered System Architecture", fill=(15, 23, 42), font=f_title)
    draw.text((30, 48), "Decoupled edge AI inference, cloud agentic reasoning, and local encrypted SQLite persistence", fill=(100, 116, 139), font=f_sub)

    # Tier 1: Client Layer
    draw.rounded_rectangle([40, 85, 220, 485], radius=10, fill=(241, 245, 249), outline=(148, 163, 184), width=2)
    draw.text((55, 100), "TIER 1: CLIENT UI", fill=(15, 23, 42), font=f_box_title)
    draw.text((55, 130), "• Live Video Feed", fill=(51, 65, 85), font=f_box_text)
    draw.text((55, 155), "• Canvas Face HUD", fill=(51, 65, 85), font=f_box_text)
    draw.text((55, 180), "• Emoji Mood Grid", fill=(51, 65, 85), font=f_box_text)
    draw.text((55, 205), "• Micro-Journal Box", fill=(51, 65, 85), font=f_box_text)
    draw.text((55, 235), "INTERVENTIONS:", fill=(15, 23, 42), font=f_box_title)
    draw.text((55, 260), "• 4-7-8 Breathing", fill=(13, 148, 136), font=f_box_text)
    draw.text((55, 285), "• 432Hz Audio Player", fill=(13, 148, 136), font=f_box_text)
    draw.text((55, 315), "CHATBOT DRAWER:", fill=(15, 23, 42), font=f_box_title)
    draw.text((55, 340), "• Multilingual UI", fill=(2, 132, 199), font=f_box_text)
    draw.text((55, 365), "• Privacy Center", fill=(2, 132, 199), font=f_box_text)
    draw.text((55, 410), "Cyber-Health Glass", fill=(100, 116, 139), font=f_box_text)
    draw.text((55, 435), "HTML5/CSS3/Chart.js", fill=(100, 116, 139), font=f_box_text)

    # Arrow 1 -> 2
    draw.line([(220, 200), (260, 200)], fill=(2, 132, 199), width=3)
    draw.line([(220, 350), (260, 350)], fill=(2, 132, 199), width=3)

    # Tier 2: Edge ML & Fast API
    draw.rounded_rectangle([260, 85, 470, 485], radius=10, fill=(240, 249, 255), outline=(2, 132, 199), width=2)
    draw.text((275, 100), "TIER 2: EDGE AI & API", fill=(2, 132, 199), font=f_box_title)
    draw.text((275, 130), "FASTAPI ASYNC BACKEND", fill=(15, 23, 42), font=f_box_title)
    draw.text((275, 155), "• /api/checkin", fill=(51, 65, 85), font=f_box_text)
    draw.text((275, 180), "• /api/analyze-frame", fill=(51, 65, 85), font=f_box_text)
    draw.text((275, 205), "• /api/chat", fill=(51, 65, 85), font=f_box_text)
    draw.text((275, 240), "OPENCV VISION PIPELINE", fill=(15, 23, 42), font=f_box_title)
    draw.text((275, 265), "• Haar Face Cascade", fill=(51, 65, 85), font=f_box_text)
    draw.text((275, 290), "• 48x48 Grayscale Crop", fill=(51, 65, 85), font=f_box_text)
    draw.text((275, 325), "PYTORCH EMONET CNN", fill=(15, 23, 42), font=f_box_title)
    draw.text((275, 350), "• Mac M1 MPS GPU (torch)", fill=(5, 150, 105), font=f_box_text)
    draw.text((275, 375), "• 14.8ms Edge Latency", fill=(5, 150, 105), font=f_box_text)
    draw.text((275, 410), "VADER NLP SENTIMENT", fill=(15, 23, 42), font=f_box_title)
    draw.text((275, 435), "• Compound Polarity Score", fill=(51, 65, 85), font=f_box_text)

    # Arrow 2 -> 3
    draw.line([(470, 200), (510, 200)], fill=(124, 58, 237), width=3)

    # Tier 3: Agentic Reasoning Core
    draw.rounded_rectangle([510, 85, 700, 485], radius=10, fill=(245, 243, 255), outline=(124, 58, 237), width=2)
    draw.text((525, 100), "TIER 3: AGENTIC CORE", fill=(124, 58, 237), font=f_box_title)
    draw.text((525, 130), "GOOGLE GEMINI API", fill=(15, 23, 42), font=f_box_title)
    draw.text((525, 155), "3-WAY CONGRUENCE", fill=(124, 58, 237), font=f_box_title)
    draw.text((525, 180), "• Cross-modal Triangulation", fill=(51, 65, 85), font=f_box_text)
    draw.text((525, 205), "• Detects Emotional Masking", fill=(225, 29, 72), font=f_box_text)
    draw.text((525, 240), "TREND SCORER AGENT", fill=(124, 58, 237), font=f_box_title)
    draw.text((525, 265), "• Evaluates History (ESI)", fill=(51, 65, 85), font=f_box_text)
    draw.text((525, 290), "• Prevents False Alarms", fill=(51, 65, 85), font=f_box_text)
    draw.text((525, 325), "REPORT WRITER AGENT", fill=(124, 58, 237), font=f_box_title)
    draw.text((525, 350), "• Wellness Synthesis", fill=(51, 65, 85), font=f_box_text)
    draw.text((525, 375), "• Micro-Interventions", fill=(51, 65, 85), font=f_box_text)
    draw.text((525, 410), "AI COMPANION CHATBOT", fill=(124, 58, 237), font=f_box_title)
    draw.text((525, 435), "• Multilingual QA Engine", fill=(51, 65, 85), font=f_box_text)

    # Arrow 3 -> 4
    draw.line([(700, 280), (740, 280)], fill=(5, 150, 105), width=3)

    # Tier 4: Local Storage
    draw.rounded_rectangle([740, 85, 860, 485], radius=10, fill=(240, 253, 244), outline=(5, 150, 105), width=2)
    draw.text((755, 100), "TIER 4: DB", fill=(5, 150, 105), font=f_box_title)
    draw.text((755, 130), "SQLITE 3", fill=(15, 23, 42), font=f_box_title)
    draw.text((755, 155), "LOCAL STORAGE", fill=(100, 116, 139), font=f_box_text)
    draw.text((755, 185), "• UserCheckIns", fill=(51, 65, 85), font=f_box_text)
    draw.text((755, 210), "• EmotionLogs", fill=(51, 65, 85), font=f_box_text)
    draw.text((755, 235), "• Interventions", fill=(51, 65, 85), font=f_box_text)
    draw.text((755, 280), "ORM LAYER:", fill=(15, 23, 42), font=f_box_title)
    draw.text((755, 305), "• SQLAlchemy 2.0", fill=(51, 65, 85), font=f_box_text)
    draw.text((755, 360), "100% PRIVATE", fill=(5, 150, 105), font=f_box_title)
    draw.text((755, 385), "Zero Cloud DB", fill=(100, 116, 139), font=f_box_text)
    draw.text((755, 410), "emosense.db", fill=(100, 116, 139), font=f_box_text)

    img.save("report_assets/fig3_1_architecture.png")
    print("Generated: fig3_1_architecture.png")

def create_figure_4_1():
    """Figure 4.1: PyTorch EmoNet CNN Layer Architecture"""
    w, h = 900, 440
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, True)
    f_sub = get_font(13)
    f_box_title = get_font(13, True)
    f_box_text = get_font(11)

    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    draw.text((30, 22), "Figure 4.1: Custom PyTorch CNN Model Architecture (EmoNet)", fill=(15, 23, 42), font=f_title)
    draw.text((30, 48), "4-Block Convolutional Feature Extractor with Batch Normalization, MaxPool, Dropout and Dense Head", fill=(100, 116, 139), font=f_sub)

    blocks = [
        ("INPUT IMAGE", ["48 x 48 Grayscale", "1 Channel [-1, +1]", "Tensor (B,1,48,48)"], (241, 245, 249), (148, 163, 184)),
        ("BLOCK 1", ["Conv2d (1->32, 3x3)", "Conv2d (32->64, 3x3)", "MaxPool2d (2x2)", "Dropout2d (0.25)", "Output: 64x24x24"], (238, 242, 255), (99, 102, 241)),
        ("BLOCK 2", ["Conv2d (64->128, 3x3)", "Conv2d (128->128, 3x3)", "MaxPool2d (2x2)", "Dropout2d (0.25)", "Output: 128x12x12"], (240, 253, 250), (13, 148, 136)),
        ("BLOCK 3", ["Conv2d (128->256, 3x3)", "Conv2d (256->256, 3x3)", "MaxPool2d (2x2)", "Dropout2d (0.25)", "Output: 256x6x6"], (254, 243, 199), (217, 119, 6)),
        ("DENSE HEAD", ["Flatten (9,216)", "Linear (9216->512)", "BatchNorm1d + ReLU", "Dropout (0.50)", "Linear (512->7)"], (255, 241, 242), (225, 29, 72)),
        ("7 EMOTIONS", ["Angry, Disgust", "Fear, Happy", "Neutral, Sad", "Surprise", "Softmax Probs"], (240, 253, 244), (5, 150, 105)),
    ]

    x = 30
    for idx, (b_title, lines, bg_col, border_col) in enumerate(blocks):
        bx_w = 125
        draw.rounded_rectangle([x, 95, x + bx_w, 400], radius=8, fill=bg_col, outline=border_col, width=2)
        draw.text((x + 8, 110), b_title, fill=border_col, font=f_box_title)
        draw.line([(x + 8, 130), (x + bx_w - 8, 130)], fill=border_col, width=1)
        y = 145
        for line in lines:
            draw.text((x + 8, y), line, fill=(30, 41, 59), font=f_box_text)
            y += 24
        if idx < len(blocks) - 1:
            draw.polygon([(x + bx_w + 4, 245), (x + bx_w + 14, 250), (x + bx_w + 4, 255)], fill=(100, 116, 139))
        x += bx_w + 18

    img.save("report_assets/fig4_1_cnn_layers.png")
    print("Generated: fig4_1_cnn_layers.png")

def create_figure_5_2():
    """Figure 5.2: Training & Validation Progression Curve"""
    w, h = 900, 480
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, True)
    f_sub = get_font(13)
    f_axis = get_font(12, True)
    f_num = get_font(11)

    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    draw.text((30, 22), "Figure 5.2: Training & Validation Progression Curves (10 Epochs on Mac M1 MPS GPU)", fill=(15, 23, 42), font=f_title)
    draw.text((30, 48), "Validation accuracy steadily converges to 62.54% while validation loss descends to 1.0088", fill=(100, 116, 139), font=f_sub)

    # Plot coordinates: [80, 100] to [820, 420]
    origin_x, origin_y = 90, 410
    plot_w, plot_h = 730, 300

    # Draw Grid & Axes
    draw.line([(origin_x, origin_y), (origin_x + plot_w, origin_y)], fill=(71, 85, 105), width=2)
    draw.line([(origin_x, origin_y), (origin_x, origin_y - plot_h)], fill=(71, 85, 105), width=2)
    draw.line([(origin_x + plot_w, origin_y), (origin_x + plot_w, origin_y - plot_h)], fill=(71, 85, 105), width=2)

    # Horizontal grid lines (30% to 70% accuracy on left axis)
    for acc in [30, 40, 50, 60, 70]:
        y = origin_y - int(((acc - 30) / 40) * plot_h)
        draw.line([(origin_x, y), (origin_x + plot_w, y)], fill=(226, 232, 240), width=1)
        draw.text((origin_x - 45, y - 7), f"{acc}%", fill=(71, 85, 105), font=f_num)

    # Right axis labels (Loss: 1.8 to 0.8)
    for l_val in [1.8, 1.6, 1.4, 1.2, 1.0]:
        y = origin_y - int(((1.8 - l_val) / 1.0) * plot_h)
        draw.text((origin_x + plot_w + 10, y - 7), f"{l_val:.1f}", fill=(225, 29, 72), font=f_num)

    # Epoch points
    epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    val_accs = [48.11, 53.26, 56.74, 57.01, 58.78, 59.64, 60.34, 60.77, 62.20, 62.54]
    train_accs = [35.07, 47.71, 51.54, 53.54, 55.02, 56.49, 57.76, 58.72, 59.32, 60.40]
    val_losses = [1.3514, 1.2243, 1.1422, 1.1148, 1.0923, 1.0757, 1.0429, 1.0419, 1.0155, 1.0088]

    def get_acc_pt(idx, acc):
        x = origin_x + int((idx / 9) * plot_w)
        y = origin_y - int(((acc - 30) / 40) * plot_h)
        return (x, y)

    def get_loss_pt(idx, l_val):
        x = origin_x + int((idx / 9) * plot_w)
        y = origin_y - int(((1.8 - l_val) / 1.0) * plot_h)
        return (x, y)

    # Plot Validation Accuracy (Cyan / Teal)
    val_pts = [get_acc_pt(i, val_accs[i]) for i in range(10)]
    for i in range(9):
        draw.line([val_pts[i], val_pts[i+1]], fill=(13, 148, 136), width=3)
        draw.ellipse([val_pts[i][0]-4, val_pts[i][1]-4, val_pts[i][0]+4, val_pts[i][1]+4], fill=(13, 148, 136))
    draw.ellipse([val_pts[9][0]-5, val_pts[9][1]-5, val_pts[9][0]+5, val_pts[9][1]+5], fill=(13, 148, 136))
    draw.text((val_pts[9][0]-70, val_pts[9][1]-20), "Best Val Acc: 62.54%", fill=(13, 148, 136), font=get_font(12, True))

    # Plot Training Accuracy (Indigo)
    train_pts = [get_acc_pt(i, train_accs[i]) for i in range(10)]
    for i in range(9):
        draw.line([train_pts[i], train_pts[i+1]], fill=(99, 102, 241), width=2)
        draw.ellipse([train_pts[i][0]-3, train_pts[i][1]-3, train_pts[i][0]+3, train_pts[i][1]+3], fill=(99, 102, 241))

    # Plot Validation Loss (Rose Red)
    loss_pts = [get_loss_pt(i, val_losses[i]) for i in range(10)]
    for i in range(9):
        draw.line([loss_pts[i], loss_pts[i+1]], fill=(225, 29, 72), width=2)
        draw.ellipse([loss_pts[i][0]-3, loss_pts[i][1]-3, loss_pts[i][0]+3, loss_pts[i][1]+3], fill=(225, 29, 72))

    # X-axis labels
    for i in range(10):
        x = origin_x + int((i / 9) * plot_w)
        draw.text((x - 8, origin_y + 10), f"Ep {i+1}", fill=(71, 85, 105), font=f_num)

    # Legend
    draw.rectangle([origin_x + 30, origin_y - 280, origin_x + 380, origin_y - 200], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.line([(origin_x + 45, origin_y - 260), (origin_x + 75, origin_y - 260)], fill=(13, 148, 136), width=3)
    draw.text((origin_x + 85, origin_y - 268), "Validation Accuracy (%) - Left Axis", fill=(13, 148, 136), font=f_num)
    draw.line([(origin_x + 45, origin_y - 240), (origin_x + 75, origin_y - 240)], fill=(99, 102, 241), width=2)
    draw.text((origin_x + 85, origin_y - 248), "Training Accuracy (%) - Left Axis", fill=(99, 102, 241), font=f_num)
    draw.line([(origin_x + 45, origin_y - 220), (origin_x + 75, origin_y - 220)], fill=(225, 29, 72), width=2)
    draw.text((origin_x + 85, origin_y - 228), "Validation Loss - Right Axis", fill=(225, 29, 72), font=f_num)

    img.save("report_assets/fig5_2_training_curves.png")
    print("Generated: fig5_2_training_curves.png")

def create_figure_5_3():
    """Figure 5.3: Latency Benchmark Bar Chart"""
    w, h = 900, 420
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, True)
    f_sub = get_font(13)
    f_axis = get_font(13, True)
    f_num = get_font(12)

    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    draw.text((30, 22), "Figure 5.3: End-to-End Inference Latency Profiling (Lower is Faster)", fill=(15, 23, 42), font=f_title)
    draw.text((30, 48), "Apple Silicon Mac M1 MPS GPU achieves 14.8ms (< 20ms target), 25x faster than Cloud Vision APIs", fill=(100, 116, 139), font=f_sub)

    data = [
        ("Apple M1 MPS GPU\n(EmoSense Local)", 14.8, (13, 148, 136), "14.8 ms (67.5 FPS)\n[Zero Cloud Transmission]"),
        ("Apple M1 CPU\n(PyTorch CPU Mode)", 42.1, (99, 102, 241), "42.1 ms (23.7 FPS)\n[Local On-Device]"),
        ("Intel Core i7 CPU\n(Legacy Laptop)", 84.6, (217, 119, 6), "84.6 ms (11.8 FPS)\n[Local On-Device]"),
        ("Commercial Cloud Vision API\n(AWS / GCP Network Roundtrip)", 385.0, (225, 29, 72), "385.0 ms (2.6 FPS)\n[High Biometric Privacy Risk]"),
    ]

    max_lat = 400.0
    bar_y = 100
    bar_h = 55

    for label, lat, color, note in data:
        draw.text((40, bar_y + 12), label, fill=(15, 23, 42), font=f_axis)
        bar_len = int((lat / max_lat) * 440)
        draw.rounded_rectangle([290, bar_y, 290 + bar_len, bar_y + bar_h], radius=6, fill=color)
        draw.text((290 + bar_len + 15, bar_y + 10), note, fill=color, font=f_num)
        bar_y += 75

    img.save("report_assets/fig5_3_latency_benchmark.png")
    print("Generated: fig5_3_latency_benchmark.png")

if __name__ == "__main__":
    create_figure_1_1()
    create_figure_3_1()
    create_figure_4_1()
    create_figure_5_2()
    create_figure_5_3()
    print("All report figures successfully generated in report_assets/!")
