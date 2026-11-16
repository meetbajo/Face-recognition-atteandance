import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(40, letter[1] - 30, "Ramdeobaba University • Dept. of Electronics Engineering • Capstone Defense")
    canvas.drawRightString(letter[0] - 40, letter[1] - 30, "Team Work Division & Presentation Script")
    
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(40, 24, "Smart Face Recognition Attendance System • Team Role Guide")
    canvas.drawRightString(letter[0] - 40, 24, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()

def generate_team_division_pdf():
    pdf_filename = "Team_Work_Division_and_Defense_Guide.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=38,
    )
    
    PRIMARY = colors.HexColor("#1E1B4B")   # Deep Indigo/Navy
    SECONDARY = colors.HexColor("#4338CA") # Vibrant Indigo
    ACCENT = colors.HexColor("#0284C7")    # Sky Blue
    DARK = colors.HexColor("#0F172A")      # Near Black
    MUTED = colors.HexColor("#475569")     # Slate Gray
    LIGHT_BG = colors.HexColor("#F8FAFC")  # Light Slate
    BORDER_CLR = colors.HexColor("#CBD5E1")
    SUCCESS = colors.HexColor("#059669")
    
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_LEFT,
        textColor=PRIMARY,
        spaceAfter=4,
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_LEFT,
        textColor=MUTED,
        spaceAfter=10,
    )
    
    member_title_style = ParagraphStyle(
        "MemberTitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
    )
    
    member_role_style = ParagraphStyle(
        "MemberRole",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=SECONDARY,
        spaceAfter=6,
    )
    
    sec_heading = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
    )
    
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Times-Roman",
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        spaceAfter=5,
    )
    
    speech_style = ParagraphStyle(
        "SpeechText",
        fontName="Times-Italic",
        fontSize=8.8,
        leading=12.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
    )
    
    bullet_style = ParagraphStyle(
        "BulletText",
        fontName="Times-Roman",
        fontSize=8.8,
        leading=12.2,
        alignment=TA_JUSTIFY,
        leftIndent=12,
        textColor=DARK,
        spaceAfter=3,
    )
    
    qa_title = ParagraphStyle(
        "QATitle",
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=12,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=1,
    )
    
    qa_ans = ParagraphStyle(
        "QAAns",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.8,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        spaceAfter=4,
    )

    story = []
    
    # -------------------------------------------------------------
    # HEADER BANNER & PROJECT METADATA
    # -------------------------------------------------------------
    story.append(Paragraph("SMART FACE RECOGNITION ATTENDANCE SYSTEM", title_style))
    story.append(Paragraph("Official Team Work Division, Presentation Strategy, and Individual Defense Script", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Project:</b> Capstone Viva Voce Defense", ParagraphStyle("M1", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
            Paragraph("<b>Institution:</b> Ramdeobaba University, Nagpur", ParagraphStyle("M2", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
        ],
        [
            Paragraph("<b>Department:</b> Electronics Engineering", ParagraphStyle("M3", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#E2E8F0"))),
            Paragraph("<b>Course Coordinator:</b> Prof. V. R. Gupta", ParagraphStyle("M4", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#E2E8F0"))),
        ],
        [
            Paragraph("<b>Total Presentation Duration:</b> 10 &ndash; 12 Minutes", ParagraphStyle("M5", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#E2E8F0"))),
            Paragraph("<b>Format:</b> 4 Speakers &times; ~2.5 to 3 Minutes Each", ParagraphStyle("M6", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#E2E8F0"))),
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[268, 268])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))
    
    # -------------------------------------------------------------
    # HIGH-LEVEL WORKFLOW SUMMARY TABLE
    # -------------------------------------------------------------
    story.append(Paragraph("EXECUTIVE WORK DIVISION MATRIX", sec_heading))
    matrix_data = [
        [Paragraph("<b>Team Member</b>", ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white)),
         Paragraph("<b>Roll</b>", ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=TA_CENTER)),
         Paragraph("<b>Assigned Module & Technical Domain</b>", ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white)),
         Paragraph("<b>Speaking Window</b>", ParagraphStyle("H4", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=TA_CENTER))],
        
        [Paragraph("<b>Meet Ashish Bajoria</b>", ParagraphStyle("B1", fontName="Helvetica-Bold", fontSize=8, textColor=PRIMARY)),
         Paragraph("36", ParagraphStyle("B2", fontName="Times-Roman", fontSize=8, alignment=TA_CENTER)),
         Paragraph("<b>Speaker 1:</b> Project Motivation, Problem Statement, High-Level Architecture & Pipeline Formulation", ParagraphStyle("B3", fontName="Times-Roman", fontSize=8)),
         Paragraph("Mins 0:00 &ndash; 2:45", ParagraphStyle("B4", fontName="Times-Bold", fontSize=8, alignment=TA_CENTER))],
        
        [Paragraph("<b>Khizra Bushra Raien</b>", ParagraphStyle("B1", fontName="Helvetica-Bold", fontSize=8, textColor=PRIMARY)),
         Paragraph("32", ParagraphStyle("B2", fontName="Times-Roman", fontSize=8, alignment=TA_CENTER)),
         Paragraph("<b>Speaker 2:</b> Face Detection Cascade, MTCNN Mechanics (P-Net, R-Net, O-Net) & 5-Point Alignment", ParagraphStyle("B3", fontName="Times-Roman", fontSize=8)),
         Paragraph("Mins 2:45 &ndash; 5:15", ParagraphStyle("B4", fontName="Times-Bold", fontSize=8, alignment=TA_CENTER))],
         
        [Paragraph("<b>Mohammad Moinuddin</b>", ParagraphStyle("B1", fontName="Helvetica-Bold", fontSize=8, textColor=PRIMARY)),
         Paragraph("38", ParagraphStyle("B2", fontName="Times-Roman", fontSize=8, alignment=TA_CENTER)),
         Paragraph("<b>Speaker 3:</b> Feature Extraction, Inception-ResNet-v1, L2-Normalization, Cosine Metric & Threshold τ", ParagraphStyle("B3", fontName="Times-Roman", fontSize=8)),
         Paragraph("Mins 5:15 &ndash; 8:00", ParagraphStyle("B4", fontName="Times-Bold", fontSize=8, alignment=TA_CENTER))],
         
        [Paragraph("<b>Pratham Singh Thakur</b>", ParagraphStyle("B1", fontName="Helvetica-Bold", fontSize=8, textColor=PRIMARY)),
         Paragraph("44", ParagraphStyle("B2", fontName="Times-Roman", fontSize=8, alignment=TA_CENTER)),
         Paragraph("<b>Speaker 4:</b> Real-Time CPU Latency Optimization (30 FPS), LFW Benchmark, Live Demo & Conclusion", ParagraphStyle("B3", fontName="Times-Roman", fontSize=8)),
         Paragraph("Mins 8:00 &ndash; 11:00", ParagraphStyle("B4", fontName="Times-Bold", fontSize=8, alignment=TA_CENTER))]
    ]
    t_mat = Table(matrix_data, colWidths=[120, 36, 270, 110])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # MEMBER 1 SCRIPT & VIVA
    # -------------------------------------------------------------
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8))
    story.append(Paragraph("MEMBER 1: MEET ASHISH BAJORIA (ROLL: 36)", member_title_style))
    story.append(Paragraph("ROLE: TEAM LEAD • ARCHITECTURE, PROBLEM STATEMENT & HIGH-LEVEL PIPELINE (2.5 &ndash; 3 MINS)", member_role_style))
    
    story.append(Paragraph("<b>Exact Spoken Presentation Script:</b>", ParagraphStyle("HSub", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, spaceAfter=2)))
    m1_speech = [
        [Paragraph(
            "\"Respected faculty members, external examiners, and our course coordinator Prof. V. R. Gupta sir. Good morning. "
            "In modern universities, accurate attendance tracking is vital for internal assessments and accreditation. Yet, most classrooms still rely on paper roll calls or signature sheets. This presents three severe drawbacks: it wastes 5 to 10 minutes of valuable teaching time, it enables rampant proxy marking through buddy sign-ins, and it requires faculty to manually enter records into ERP systems. Contact biometrics like fingerprint scanners solve proxy attendance, but they cause severe queues at classroom doors and raise hygiene concerns.<br/><br/>"
            "To solve this, our capstone project is an <b>Edge-Ready, Contactless Face Recognition Attendance System</b>. Instead of building a closed-set classifier that fails when unregistered visitors enter, we engineered an <b>Open-Set Deep Metric Learning pipeline</b> using two specialized neural networks: MTCNN for geometric face alignment and Inception-ResNet-v1 for generating 512-dimensional face embeddings. The entire pipeline runs smoothly on standard multi-core laptop CPUs at 30 FPS. "
            "<i>I will now hand over to Khizra to explain our face detection cascade and geometric alignment process.</i>\"",
            speech_style
        )]
    ]
    t_m1 = Table(m1_speech, colWidths=[536])
    t_m1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#A5B4FC")),
    ]))
    story.append(t_m1)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Key Viva Questions Member 1 Must Answer:</b>", ParagraphStyle("HViva", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, spaceAfter=2)))
    story.append(Paragraph("<b>Q: Why Metric Learning instead of a standard CNN with Softmax?</b>", qa_title))
    story.append(Paragraph("A: Softmax is restricted to closed sets. If an unregistered person enters, Softmax forces probabilities to sum to 1.0, wrongly assigning the intruder to the nearest student. Also, adding a student requires full network retraining. Metric learning projects faces to vectors; enrollment is instant with zero retraining, and outsiders are rejected as 'Unknown'.", qa_ans))
    story.append(Paragraph("<b>Q: What are the main components of your pipeline?</b>", qa_title))
    story.append(Paragraph("A: Ingestion (OpenCV/WebRTC) &rarr; Subsampling (0.5x) &rarr; MTCNN Alignment &rarr; Inception-ResNet-v1 (512-D) &rarr; L2-Norm &rarr; Cosine Similarity vs Gallery &rarr; Deduplicated CSV Logging.", qa_ans))
    
    # -------------------------------------------------------------
    # MEMBER 2 SCRIPT & VIVA
    # -------------------------------------------------------------
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8))
    story.append(Paragraph("MEMBER 2: KHIZRA BUSHRA RAIEN (ROLL: 32)", member_title_style))
    story.append(Paragraph("ROLE: COMPUTER VISION • FACE DETECTION, MTCNN CASCADE & LANDMARK ALIGNMENT (2.5 MINS)", member_role_style))
    
    m2_speech = [
        [Paragraph(
            "\"Thank you, Meet. The foundation of any robust face recognition system is precise facial localization and alignment. Traditional detectors like Haar Cascades or HOG fail under natural head tilts, yaw angles, and non-uniform classroom illumination. To overcome this, our system employs <b>Multi-Task Cascaded Convolutional Networks (MTCNN)</b>.<br/><br/>"
            "MTCNN operates through three dedicated sub-networks in a coarse-to-fine cascade: First, the <b>Proposal Network (P-Net)</b> scans an image pyramid to generate candidate bounding windows. Second, the <b>Refine Network (R-Net)</b> filters out high-scoring false candidates using Non-Maximum Suppression (NMS). Third, the <b>Output Network (O-Net)</b> computes precise bounding box coordinates and regresses <b>5 key facial landmarks</b>: left eye, right eye, nose tip, left mouth corner, and right mouth corner.<br/><br/>"
            "Detecting landmarks is critical: we perform an affine geometric transformation that rotates the facial crop so that the ocular axis between both eyes is aligned perfectly horizontal. We then crop the face with standard margin padding and resize it to 160x160 pixels. This ensures that when the face reaches the embedding network, it is completely invariant to student head tilts. "
            "<i>Now, Moinuddin will explain how these crops are converted into discriminative deep embeddings.</i>\"",
            speech_style
        )]
    ]
    t_m2 = Table(m2_speech, colWidths=[536])
    t_m2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#86EFAC")),
    ]))
    story.append(t_m2)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Key Viva Questions Member 2 Must Answer:</b>", ParagraphStyle("HViva", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, spaceAfter=2)))
    story.append(Paragraph("<b>Q: Why do we need 5 facial landmarks instead of just bounding boxes?</b>", qa_title))
    story.append(Paragraph("A: Bounding boxes only locate the head. If a student looks sideways or tilts their head, raw pixels change drastically. The 5 landmarks allow affine rotation to align the eyes horizontally, guaranteeing standard pose invariance before feature extraction.", qa_ans))
    story.append(Paragraph("<b>Q: What is the internal architecture of MTCNN?</b>", qa_title))
    story.append(Paragraph("A: A 3-stage cascade: P-Net (shallow FCN for proposal generation), R-Net (CNN for false-positive reduction via NMS), and O-Net (deeper CNN for final bounding box regression and 5-point landmark localization).", qa_ans))
    
    # -------------------------------------------------------------
    # MEMBER 3 SCRIPT & VIVA
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8))
    story.append(Paragraph("MEMBER 3: MOHAMMAD MOINUDDIN (ROLL: 38)", member_title_style))
    story.append(Paragraph("ROLE: DEEP LEARNING & METRICS • INCEPTION-RESNET-V1, L2-NORM & DECISION BOUNDARY (2.5 &ndash; 3 MINS)", member_role_style))
    
    m3_speech = [
        [Paragraph(
            "\"Thank you, Khizra. Once MTCNN delivers the aligned 160x160 face crop, our deep feature extractor takes over. We utilize the <b>Inception-ResNet-v1 architecture pretrained on the VGGFace2 dataset</b>, which spans over 3.3 million facial images across 9,131 distinct subjects. The network maps facial geometry into a compact, highly discriminative <b>512-dimensional vector</b>.<br/><br/>"
            "To make our representation invariant to classroom lighting intensity, we apply explicit <b>L2-normalization</b>: dividing the vector by its Euclidean length. This constrains all student embeddings to lie strictly on the surface of a 512-dimensional unit hypersphere. Because all vectors have unit magnitude, computing <b>Cosine Similarity</b> reduces to a blazing-fast inner dot product: <i>Sim(q, e) = q · e</i>.<br/><br/>"
            "During live video, the system computes similarity between the camera query vector and every enrolled student in our gallery. The maximum similarity score determines identity. We established an optimal decision threshold of <b>τ = 0.75</b>. If similarity is ≥ 0.75, the student is positively identified. If it is below 0.75, the system safely tags the individual as <b>'Unknown'</b>, completely preventing false attendance marks. "
            "<i>Pratham will now explain our speed optimizations, benchmark results, and demonstrate the live system.</i>\"",
            speech_style
        )]
    ]
    t_m3 = Table(m3_speech, colWidths=[536])
    t_m3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FCD34D")),
    ]))
    story.append(t_m3)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Key Viva Questions Member 3 Must Answer:</b>", ParagraphStyle("HViva", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, spaceAfter=2)))
    story.append(Paragraph("<b>Q: Why is L2-normalization mandatory?</b>", qa_title))
    story.append(Paragraph("A: Without L2-norm, vector lengths fluctuate with lighting brightness, distorting distance metrics. Normalizing projects embeddings onto a unit hypersphere, making distance purely an angular measurement and allowing fast dot-product cosine similarity.", qa_ans))
    story.append(Paragraph("<b>Q: How did you select the threshold τ = 0.75?</b>", qa_title))
    story.append(Paragraph("A: We evaluated genuine vs. imposter score distributions. At τ = 0.60, false acceptances occasionally occurred. At τ = 0.75, genuine matches score 0.78–0.92 while imposters score below 0.55, providing a clear margin of separation and zero false acceptances.", qa_ans))
    
    # -------------------------------------------------------------
    # MEMBER 4 SCRIPT & VIVA
    # -------------------------------------------------------------
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8))
    story.append(Paragraph("MEMBER 4: PRATHAM SINGH THAKUR (ROLL: 44)", member_title_style))
    story.append(Paragraph("ROLE: EDGE OPTIMIZATION, EXPERIMENTAL RESULTS, LIVE DEMO & CONCLUSION (3 MINS)", member_role_style))
    
    m4_speech = [
        [Paragraph(
            "\"Thank you, Moinuddin. Running MTCNN and Inception-ResNet simultaneously on standard multi-core laptop CPUs initially resulted in severe latency (only 6 to 8 FPS). To make our prototype truly edge-ready without requiring an expensive dedicated GPU, we engineered three key optimizations:<br/><br/>"
            "1. <b>Spatial Subsampling:</b> The MTCNN face detection pass operates on a 0.5x downsampled frame (320x240), reducing the pixel search space by 75%. Bounding box coordinates are then scaled back 2.0x to extract the high-resolution crop for Inception-ResNet.<br/>"
            "2. <b>Temporal Frame Skipping:</b> Deep inference executes once every 3rd frame, while the display HUD smoothly interpolates bounding boxes across intermediate frames.<br/>"
            "3. <b>DirectShow Hardware Control:</b> We bound OpenCV to DirectShow with buffer size 1, eliminating driver frame lag. Together, these boosted throughput to a stable <b>30 FPS on CPU</b>.<br/><br/>"
            "We validated the model on the official <b>Labeled Faces in the Wild (LFW)</b> benchmark across 6,000 paired comparisons, achieving <b>95.2% verification accuracy and 0.984 AUC</b>. "
            "I will now demonstrate our live system on localhost. As you see on screen, standing before the camera displays a green bounding box with my name and 85% similarity, updating the status to 'Present' with an exact timestamp. When an unregistered face appears, the box turns red and displays 'Unknown'. Clicking 'Save Attendance' immediately exports an audit-ready CSV sheet. "
            "In conclusion, our system provides an automated, hygienic, and proxy-free attendance solution. We thank Prof. V. R. Gupta sir and welcome any questions from the panel.\"",
            speech_style
        )]
    ]
    t_m4 = Table(m4_speech, colWidths=[536])
    t_m4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FDF2F8")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#F472B6")),
    ]))
    story.append(t_m4)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Key Viva Questions Member 4 Must Answer:</b>", ParagraphStyle("HViva", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, spaceAfter=2)))
    story.append(Paragraph("<b>Q: What specific optimizations achieved 30 FPS on CPU?</b>", qa_title))
    story.append(Paragraph("A: (1) 0.5x spatial downsampling (reduces MTCNN scan area by 75%), (2) frame-skipping (deep inference runs every 3rd frame with HUD persistence), and (3) DirectShow backend with buffer size 1 to prevent queue latency.", qa_ans))
    story.append(Paragraph("<b>Q: What does an AUC of 0.984 on LFW signify?</b>", qa_title))
    story.append(Paragraph("A: Area Under the ROC Curve (AUC) measures the probability that the classifier ranks a randomly chosen genuine pair higher than an imposter pair. An AUC of 0.984 proves near-ideal separation between positive and negative distributions.", qa_ans))
    
    # -------------------------------------------------------------
    # DEFENSE COORDINATION & HANDOVER RULES
    # -------------------------------------------------------------
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=6))
    story.append(Paragraph("GOLDEN RULES FOR TEAM COORDINATION DURING VIVA", sec_heading))
    story.append(Paragraph("1. <b>Strict Ownership:</b> When the faculty asks a question, the member responsible for that module must answer first. Other members should only supplement if requested.", bullet_style))
    story.append(Paragraph("2. <b>Smooth Handover Lines:</b> Always use the transition lines at the end of each member's script so the faculty perceives a unified, well-practiced engineering team.", bullet_style))
    story.append(Paragraph("3. <b>Localhost Execution:</b> Always conduct the live demo using <b>run_app.bat (localhost:8501)</b> on the laptop to guarantee zero network drops and instant 30 FPS performance.", bullet_style))
    story.append(Paragraph("4. <b>Confidence on Math & Metrics:</b> Memorize the key numbers: 512-D vectors, VGGFace2 (3.3M images), τ = 0.75, 95.2% LFW accuracy, and 30 FPS CPU throughput.", bullet_style))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Generated Team Work Division PDF successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_team_division_pdf()
