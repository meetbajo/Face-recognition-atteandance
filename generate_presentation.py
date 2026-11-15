import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Modern color palette
    NAVY = RGBColor(15, 23, 42)        # #0F172A
    INDIGO = RGBColor(79, 70, 229)     # #4F46E5
    SLATE = RGBColor(100, 116, 139)    # #64748B
    DARK = RGBColor(30, 41, 59)        # #1E293B
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    ACCENT_GREEN = RGBColor(16, 185, 129)

    def set_slide_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="RAMDEOBABA UNIVERSITY • DEEP LEARNING LAB"):
        # Top banner category
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = INDIGO
        p_cat.font.name = "Segoe UI"

        # Main slide title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 1: Title & Team Members
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, NAVY)

    # Decorative shape/card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card.line.color.rgb = RGBColor(51, 65, 85)
    card.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "RAMDEOBABA UNIVERSITY, NAGPUR • DEPARTMENT OF ELECTRONICS ENGINEERING"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(129, 140, 248)
    p0.font.name = "Segoe UI"

    p1 = tf1.add_paragraph()
    p1.text = "Smart Face Recognition Attendance System"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Segoe UI"
    p1.space_before = Pt(8)
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Course: Deep Learning Lab  |  Session: 2026–27  |  Semester: V"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.font.name = "Segoe UI"
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "PROJECT TEAM MEMBERS:"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(129, 140, 248)
    p3.font.name = "Segoe UI"
    p3.space_after = Pt(6)

    members = [
        "• Khizra Bushra Raien (Roll No: 32)",
        "• Meet Ashish Bajoria (Roll No: 36)",
        "• Mohammad Moinuddin (Roll No: 38)",
        "• Pratham Singh Thakur (Roll No: 44)",
    ]
    for m in members:
        pm = tf1.add_paragraph()
        pm.text = m
        pm.font.size = Pt(14)
        pm.font.color.rgb = WHITE
        pm.font.name = "Segoe UI"

    p_guide = tf1.add_paragraph()
    p_guide.text = "Under the guidance of: Prof. V. R. Gupta"
    p_guide.font.size = Pt(13)
    p_guide.font.bold = True
    p_guide.font.color.rgb = RGBColor(148, 163, 184)
    p_guide.font.name = "Segoe UI"
    p_guide.space_before = Pt(16)

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, LIGHT_BG)
    add_header(s2, "1. Problem Statement & Motivation")

    # 2 Box Columns
    boxes_s2 = [
        ("The Problem with Traditional Attendance", [
            "Manual paper attendance is slow and wastes valuable lab & class time.",
            "Paper sheets can easily lead to proxy attendance and false records.",
            "Manual data entry into computer spreadsheets is repetitive and prone to human errors.",
            "Physical roll calls cause disruptions during lectures."
        ], Inches(0.8), Inches(1.8), Inches(5.6)),
        ("Our Solution & Core Motivation", [
            "An automated AI prototype powered by real-time Face Recognition.",
            "Contactless & Fast: Students are marked present within milliseconds via camera.",
            "Consent & Privacy First: Only enrolled volunteers are recognized; unknown faces are rejected.",
            "Automatic Logging: Logs participant name, date, and exact entry time directly to CSV."
        ], Inches(6.8), Inches(1.8), Inches(5.7))
    ]

    for title, points, left, top, width in boxes_s2:
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s2.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.font.name = "Segoe UI"
        pt.space_after = Pt(14)

        for pt_text in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_text
            p.font.size = Pt(14)
            p.font.color.rgb = DARK
            p.font.name = "Segoe UI"
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: Dataset
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, LIGHT_BG)
    add_header(s3, "2. Datasets Used")

    boxes_s3 = [
        ("Labeled Faces in the Wild (LFW)", [
            "Purpose: Used to rigorously test and evaluate our face recognition accuracy.",
            "Size: Contains over 13,000 labeled face photos of thousands of people.",
            "Benchmark: Tested on standard 6,000 pairs (3,000 same person, 3,000 different person).",
            "Why LFW: Standard benchmark in deep learning literature to test real-world variations."
        ], Inches(0.8), Inches(1.8), Inches(5.6)),
        ("Local Consent-Based Gallery", [
            "Purpose: Enrolled volunteers database used for live classroom attendance.",
            "Consent-Driven: Only registered students who provided consent photos are stored.",
            "Image Variety: Photos captured under varied poses, lighting, and expressions.",
            "Preprocessing: Automated face detection, landmark alignment, and 512-D vector extraction."
        ], Inches(6.8), Inches(1.8), Inches(5.7))
    ]

    for title, points, left, top, width in boxes_s3:
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s3.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.font.name = "Segoe UI"
        pt.space_after = Pt(14)

        for pt_text in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_text
            p.font.size = Pt(14)
            p.font.color.rgb = DARK
            p.font.name = "Segoe UI"
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 4: Methodology & Model Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, LIGHT_BG)
    add_header(s4, "3. System Architecture & Methodology")

    steps = [
        ("Step 1: Face Detection & Alignment", "MTCNN Detector", "Scans webcam frame, locates face, and aligns using 5 facial landmarks (eyes, nose, mouth corners)."),
        ("Step 2: Deep Learning Embeddings", "InceptionResnetV1", "Pretrained on VGGFace2. Converts face into a compact 512-number vector (unique math fingerprint)."),
        ("Step 3: Cosine Similarity Matching", "Metric Matching", "Measures angle between live face vector and enrolled vectors. Range is -1 to +1 (dot product of L2 vectors)."),
        ("Step 4: Decision & Automated Logging", "Smart Threshold (τ)", "If similarity >= τ: student is recognized and marked Present with timestamp. Otherwise labeled 'Unknown'.")
    ]

    step_w = Inches(2.7)
    gap = Inches(0.25)
    for i, (stitle, sbadge, sdesc) in enumerate(steps):
        left = Inches(0.8) + i * (step_w + gap)
        top = Inches(1.8)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, step_w, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.25), step_w - Inches(0.4), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = INDIGO
        p_num.font.name = "Segoe UI"

        p_t = tf.add_paragraph()
        p_t.text = stitle
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        p_t.font.name = "Segoe UI"
        p_t.space_before = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = f"[{sbadge}]"
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_GREEN
        p_b.font.name = "Segoe UI"
        p_b.space_before = Pt(4)
        p_b.space_after = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = sdesc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = DARK
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 5: Experiments & Hyperparameters
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, LIGHT_BG)
    add_header(s5, "4. Experiments & Hyperparameter Tuning")

    boxes_s5 = [
        ("Hyperparameter Configurations", [
            "Input Image Size: 160 × 160 pixels (standard input for InceptionResnetV1).",
            "Embedding Dimensions: 512-dimensional L2-normalized vector.",
            "Recognition Threshold (τ): Swept from 0.30 to 0.99; optimal threshold found at τ = 0.70.",
            "Detector Confidence: MTCNN confidence threshold set to 0.70 to filter false detections.",
            "Frame Optimization: Every 3rd frame processed with 0.5x downscaled detection pass for CPU speed."
        ], Inches(0.8), Inches(1.8), Inches(5.6)),
        ("Evaluation Experiments Conducted", [
            "Threshold Sweep: Evaluated cosine similarity distribution of positive vs. negative pairs.",
            "FAR & FRR Trade-off: Balanced False Acceptance Rate (imposters accepted) vs. False Rejection Rate (valid users rejected).",
            "Unknown Face Rejection Test: Verified that unregistered visitors are reliably classified as 'Unknown'.",
            "Latency Profiling: Benchmarked inference time per frame on standard laptop CPU."
        ], Inches(6.8), Inches(1.8), Inches(5.7))
    ]

    for title, points, left, top, width in boxes_s5:
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s5.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.font.name = "Segoe UI"
        pt.space_after = Pt(14)

        for pt_text in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_text
            p.font.size = Pt(14)
            p.font.color.rgb = DARK
            p.font.name = "Segoe UI"
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 6: Results
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, LIGHT_BG)
    add_header(s6, "5. Project Results & Performance")

    # 3 Stat Cards on Top
    res_stats = [
        ("RECOGNITION ACCURACY", "> 95%", "High verification on clear faces"),
        ("OPTIMAL THRESHOLD (τ)", "0.70", "Balances FAR & FRR perfectly"),
        ("INFERENCE SPEED", "~ 30 FPS", "Real-time smooth stream on CPU")
    ]
    stat_w = Inches(3.7)
    stat_gap = Inches(0.3)
    for i, (stitle, sval, ssub) in enumerate(res_stats):
        left = Inches(0.8) + i * (stat_w + stat_gap)
        top = Inches(1.8)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, stat_w, Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), stat_w - Inches(0.4), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = SLATE
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = sval
        p2.font.size = Pt(28)
        p2.font.bold = True
        p2.font.color.rgb = INDIGO
        p2.font.name = "Segoe UI"

        p3 = tf.add_paragraph()
        p3.text = ssub
        p3.font.size = Pt(11)
        p3.font.color.rgb = DARK
        p3.font.name = "Segoe UI"

    # Bottom summary box
    card_bot = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.7), Inches(11.7), Inches(3.0))
    card_bot.fill.solid()
    card_bot.fill.fore_color.rgb = WHITE
    card_bot.line.color.rgb = CARD_BORDER
    card_bot.line.width = Pt(1)

    tb_bot = s6.shapes.add_textbox(Inches(1.1), Inches(3.9), Inches(11.1), Inches(2.6))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    pt = tf_bot.paragraphs[0]
    pt.text = "Key Functional Achievements:"
    pt.font.size = Pt(17)
    pt.font.bold = True
    pt.font.color.rgb = NAVY
    pt.font.name = "Segoe UI"
    pt.space_after = Pt(10)

    achievements = [
        "Real-Time Tracking: Successfully draws green bounding boxes for recognized students and red boxes for unknown faces.",
        "Zero-Duplication Attendance: Each student is marked 'Present' only once per session with an exact entry timestamp.",
        "Automatic CSV Generation: Immediately writes date, time, and roll names to CSV reports with instant download support.",
        "Interactive Web Dashboard: User-friendly Streamlit web interface with dedicated tabs for live feed, reports, and enrollment."
    ]
    for ach in achievements:
        p = tf_bot.add_paragraph()
        p.text = "✔ " + ach
        p.font.size = Pt(13)
        p.font.color.rgb = DARK
        p.font.name = "Segoe UI"
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 7: Challenges & Learnings
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, LIGHT_BG)
    add_header(s7, "6. Practical Challenges & Key Learnings")

    boxes_s7 = [
        ("Challenges Faced", [
            "CPU Inference Lag: Deep learning models (MTCNN + ResNet) originally caused stutter on CPU.",
            "Lighting & Angle Variations: Extreme side-profiles or dim room lighting occasionally degraded detection.",
            "Webcam Buffer Delays: OpenCV frame buffering initially caused delayed video feeds.",
            "False Acceptance vs. Rejection: Finding the single threshold number that never accepts strangers while never rejecting students."
        ], Inches(0.8), Inches(1.8), Inches(5.6)),
        ("How We Solved Them & Learnings", [
            "Downsampling Optimization: Running MTCNN on a 0.5x scaled frame increased frame rate by 3x with zero loss in recognition accuracy.",
            "Landmark Alignment: Using MTCNN 5-point alignment fixed face tilt issues before passing to InceptionResnet.",
            "Buffer Management: Setting OpenCV buffer size to 1 and using DirectShow eliminated camera lag completely.",
            "Metric Learning Power: Learned that cosine similarity on normalized vectors is vastly faster and more flexible than retraining a classifier."
        ], Inches(6.8), Inches(1.8), Inches(5.7))
    ]

    for title, points, left, top, width in boxes_s7:
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s7.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.font.name = "Segoe UI"
        pt.space_after = Pt(14)

        for pt_text in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_text
            p.font.size = Pt(14)
            p.font.color.rgb = DARK
            p.font.name = "Segoe UI"
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 8: Conclusion & Future Work
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, LIGHT_BG)
    add_header(s8, "7. Conclusion & Future Roadmap")

    boxes_s8 = [
        ("Conclusion", [
            "Built a working real-time contactless attendance system for Deep Learning Lab.",
            "Combines MTCNN face detection with InceptionResnetV1 deep embeddings.",
            "Demonstrated automated CSV logging and high-accuracy volunteer verification.",
            "Eliminates proxy attendance while maintaining student consent and privacy."
        ], Inches(0.8), Inches(1.8), Inches(5.6)),
        ("Future Roadmap", [
            "Liveness Detection: Anti-spoofing algorithms (blink detection / texture analysis) to prevent photo spoofing.",
            "Edge Hardware Deployment: Porting the pipeline to NVIDIA Jetson Nano / Orin Nano for standalone embedded deployment.",
            "Multi-Camera Support: Synchronizing multiple classroom cameras into a central attendance database.",
            "Cloud Database Integration: Direct sync with university ERP / Student Information Management System."
        ], Inches(6.8), Inches(1.8), Inches(5.7))
    ]

    for title, points, left, top, width in boxes_s8:
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s8.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.font.name = "Segoe UI"
        pt.space_after = Pt(14)

        for pt_text in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_text
            p.font.size = Pt(14)
            p.font.color.rgb = DARK
            p.font.name = "Segoe UI"
            p.space_after = Pt(10)

    out_path = "Face_Recognition_Attendance_Final_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    create_deck()

