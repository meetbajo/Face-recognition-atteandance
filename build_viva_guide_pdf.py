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
    canvas.drawString(40, letter[1] - 30, "Ramdeobaba University • Dept. of Electronics Engineering • Capstone Viva Guide")
    canvas.drawRightString(letter[0] - 40, letter[1] - 30, "Smart Face Recognition Attendance System")
    
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(40, 24, "Confidential • Academic Defense & Technical Viva Voce Guide")
    canvas.drawRightString(letter[0] - 40, 24, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()

def generate_viva_pdf():
    pdf_filename = "Faculty_Viva_and_Defense_Guide.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=38,
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette: Deep Indigo, Slate Dark, Navy, Neutral White
    PRIMARY = colors.HexColor("#312E81")   # Deep Indigo
    SECONDARY = colors.HexColor("#4338CA") # Indigo Accent
    ACCENT = colors.HexColor("#0284C7")    # Sky Blue
    DARK = colors.HexColor("#0F172A")      # Near Black
    MUTED = colors.HexColor("#475569")     # Slate Gray
    LIGHT_BG = colors.HexColor("#F8FAFC")  # Light Slate
    BORDER_CLR = colors.HexColor("#CBD5E1")
    
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_LEFT,
        textColor=PRIMARY,
        spaceAfter=4,
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        textColor=MUTED,
        spaceAfter=12,
    )
    
    sec_heading = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        alignment=TA_LEFT,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
    )
    
    subsec_heading = ParagraphStyle(
        "SubSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
    )
    
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        spaceAfter=6,
    )
    
    script_speech_style = ParagraphStyle(
        "ScriptSpeech",
        fontName="Times-Italic",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
    )
    
    q_style = ParagraphStyle(
        "QuestionText",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY,
        spaceBefore=6,
        spaceAfter=2,
    )
    
    ans_style = ParagraphStyle(
        "AnswerText",
        fontName="Times-Roman",
        fontSize=9.2,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        spaceAfter=6,
    )
    
    code_box_style = ParagraphStyle(
        "CodeBox",
        fontName="Courier",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0F172A"),
    )
    
    meta_style = ParagraphStyle(
        "MetaText",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
    )
    
    meta_val_style = ParagraphStyle(
        "MetaValText",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#E2E8F0"),
    )

    story = []
    
    # -------------------------------------------------------------
    # HEADER BANNER & PROJECT METADATA
    # -------------------------------------------------------------
    story.append(Paragraph("SMART FACE RECOGNITION ATTENDANCE SYSTEM", title_style))
    story.append(Paragraph("Comprehensive Technical Viva Voce, Dataflow Architecture, and Defense Preparation Guide", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Project:</b> Capstone Viva Defense", meta_style),
            Paragraph("<b>Institution:</b> Ramdeobaba University, Nagpur", meta_style),
        ],
        [
            Paragraph("<b>Course Coordinator:</b> Prof. V. R. Gupta", meta_val_style),
            Paragraph("<b>Department:</b> Electronics Engineering", meta_val_style),
        ],
        [
            Paragraph("<b>Team Members:</b> Meet Bajoria (36), Khizra Raien (32),<br/>M. Moinuddin (38), Pratham Thakur (44)", meta_val_style),
            Paragraph("<b>Core Stack:</b> PyTorch, MTCNN, InceptionResnetV1,<br/>OpenCV DirectShow, Streamlit WebRTC", meta_val_style),
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[268, 268])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # PART 1: 2-MINUTE SPOKEN ELEVATOR PITCH FOR FACULTY
    # -------------------------------------------------------------
    story.append(Paragraph("PART 1: 2-MINUTE SPOKEN DEFENSE SCRIPT (WHAT TO SAY TO FACULTY)", sec_heading))
    story.append(Paragraph(
        "Deliver this crisp, structured explanation when the faculty asks: <i>'Meet, introduce your project and explain what work you have done.'</i>",
        body_style
    ))
    
    speech_text = [
        [Paragraph(
            "<b>Opening & Motivation:</b><br/>"
            "\"Good morning respected faculty and sir. In academic environments, traditional attendance tracking through paper sign-in sheets or manual roll calls wastes 5 to 10 minutes of every lecture, causes proxy attendance, and requires tedious manual transcription into institutional portals. Contact biometric systems like fingerprint scanners solve proxy attendance, but they create long queues during class switches and pose hygiene concerns.<br/><br/>"
            "<b>Our Proposed Solution:</b><br/>"
            "To solve this, our team developed a <b>Real-Time Contactless Face Recognition Attendance System</b>. Instead of treating this as a simple classification problem, we engineered an <b>Open-Set Deep Metric Learning pipeline</b> using two industry-grade deep neural networks: <b>MTCNN</b> for robust multi-angle face detection and landmark alignment, and <b>Inception-ResNet-v1 pretrained on VGGFace2</b> for extracting 512-dimensional L2-normalized embeddings.<br/><br/>"
            "<b>Technical Highlights & Latency Optimization:</b><br/>"
            "Running multi-task deep networks concurrently on standard classroom CPUs initially ran at only 6 to 8 FPS. We solved this edge-hardware bottleneck through three optimizations: spatial 0.5x downsampled detection passes, temporal frame-skipping, and DirectShow buffer controls, reaching a smooth <b>30 FPS live inference speed on CPU</b>.<br/><br/>"
            "<b>Recognition vs. Unknown Rejection:</b><br/>"
            "Using Cosine Similarity against an enrolled consent-based gallery and an empirically validated decision threshold of <b>&tau; = 0.75</b>, our system accurately marks verified students 'Present' once per session with an exact entry timestamp into a CSV report, while confidently labeling unregistered visitors as <b>'Unknown'</b>, preventing false acceptances. We validated this threshold on the 6,000-pair LFW benchmark, obtaining <b>95.2% verification accuracy and 0.984 AUC</b>. The system also supports WebRTC browser streaming for cloud deployment.\"",
            script_speech_style
        )]
    ]
    t_speech = Table(speech_text, colWidths=[536])
    t_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A5B4FC")),
    ]))
    story.append(t_speech)
    story.append(Spacer(1, 12))
    
    # -------------------------------------------------------------
    # PART 2: END-TO-END DATAFLOW ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("PART 2: DETAILED SYSTEM DATAFLOW & COMPONENT PIPELINE", sec_heading))
    story.append(Paragraph(
        "Explain this sequential 6-stage pipeline on the whiteboard or slides when explaining how a video frame turns into a logged attendance row.",
        body_style
    ))
    
    flow_diagram = [
        ["STAGE 1: IMAGE INGESTION", "OpenCV VideoCapture(0, CAP_DSHOW) or WebRTC browser frame capture at 640x480 resolution. Frame buffer size locked to 1 to avoid lag."],
        ["STAGE 2: SPATIAL DOWNSAMPLING", "Input frame downscaled by 0.5x (to 320x240). Reduces pixel search area by 75% for sub-millisecond CPU scanning."],
        ["STAGE 3: MTCNN FACE DETECTION & ALIGNMENT", "3-stage cascaded CNN: P-Net &rarr; R-Net &rarr; O-Net. Extracts bounding box coordinates and 5 facial landmarks (eyes, nose, mouth corners). Aligns face horizontally and crops to 160x160 pixels."],
        ["STAGE 4: INCEPTION-RESNET-V1 EMBEDDING", "Pretrained on VGGFace2 (3.3M faces). Extracts raw 512-D vector v. Applies L2-normalization: v_norm = v / ||v||2, mapping identity to the unit hypersphere."],
        ["STAGE 5: COSINE METRIC EVALUATION", "Computes dot product against gallery vectors: Sim(q, e_k) = q · e_k. Computes S* = max(Sim). If S* &ge; &tau; (0.75) &rarr; Student Name; else &rarr; 'Unknown'."],
        ["STAGE 6: DEDUPLICATED ATTENDANCE LOGGING", "If recognized: AttendanceLogger checks if student is already marked. If new, updates status to 'Present', records exact time (HH:MM:SS), and auto-exports to timestamped CSV."]
    ]
    t_flow = Table(flow_diagram, colWidths=[150, 386])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0,0), (0,-1), PRIMARY),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # PART 3: TOP 15 TECHNICAL VIVA QUESTIONS & MODEL ANSWERS
    # -------------------------------------------------------------
    story.append(PageBreak()) # Clean transition to Viva Q&A
    story.append(Paragraph("PART 3: HIGH-PROBABILITY TECHNICAL VIVA QUESTIONS & PRECISE ANSWERS", sec_heading))
    story.append(Paragraph(
        "Here are the exact theoretical, mathematical, and algorithmic questions faculty evaluators are most likely to ask, along with the precise answers you should provide.",
        body_style
    ))
    
    viva_qa = [
        (
            "Q1. Why did you use Deep Metric Learning instead of a standard CNN classifier with Softmax?",
            "\"Sir, a Softmax classifier is designed for a Closed-Set problem. If we train a Softmax classifier on 50 students, the final layer has 50 output nodes. This has two fatal flaws: (1) Whenever a new student enrolls or an unregistered visitor enters the camera, Softmax forces the probability distribution to sum to 1.0, meaning an unregistered intruder will be wrongly assigned to the closest student. (2) Adding a new student requires retraining the entire neural network. In contrast, Metric Learning maps faces into a continuous 512-dimensional vector space where Euclidean distance or Cosine angle represents similarity. Enrollment is zero-shot: we simply compute and store the 512-D vector without any network retraining. If the similarity is below threshold tau, the person is naturally rejected as Unknown.\""
        ),
        (
            "Q2. Explain the working of MTCNN. Why not use Haar Cascades or OpenCV DNN?",
            "\"MTCNN (Multi-Task Cascaded Convolutional Networks) uses a three-stage cascade: (1) Proposal Network (P-Net): a fully convolutional network that scans the image pyramid to generate candidate bounding boxes; (2) Refine Network (R-Net): a deeper CNN that rejects false positives via non-maximum suppression (NMS); (3) Output Network (O-Net): outputs fine-tuned bounding boxes and precisely regresses 5 facial landmarks (left eye, right eye, nose tip, left mouth corner, right mouth corner). Traditional Haar Cascades fail completely when a student tilts their head or if lighting changes. MTCNN uses the 5 landmarks to perform affine geometric transformation, rotating the ocular axis horizontally so the face is always presented to Inception-ResNet in a standard upright pose.\""
        ),
        (
            "Q3. Why is L2-Normalization applied to the face embedding vector?",
            "\"Inception-ResNet produces a raw 512-dimensional vector v. If two photos of the same student are taken under different lighting or exposure, the magnitudes (lengths) of their feature vectors will differ significantly. By dividing the vector by its Euclidean norm, v_norm = v / ||v||2, we constrain all embeddings to lie strictly on the surface of a 512-dimensional unit hypersphere. This has two huge advantages: (1) it makes the representation invariant to brightness scale, and (2) it simplifies cosine similarity from a costly division formula to a simple, fast inner dot product: q · e.\""
        ),
        (
            "Q4. What is the mathematical definition of Cosine Similarity and how does it relate to Euclidean distance?",
            "\"Cosine similarity measures the cosine of the angle theta between two vectors: CosSim(A, B) = (A · B) / (||A|| · ||B||). Since our embeddings are already L2-normalized to unit length (||A|| = ||B|| = 1), CosSim(A, B) = A · B. The relationship with squared Euclidean distance is linear: ||A - B||^2 = ||A||^2 + ||B||^2 - 2(A · B) = 2 - 2·CosSim(A, B). Therefore, maximizing cosine similarity is mathematically identical to minimizing Euclidean distance on the unit hypersphere, but computing the dot product is much faster on CPU.\""
        ),
        (
            "Q5. How was the optimal threshold tau = 0.75 determined? What happens if tau is too high or too low?",
            "\"Threshold tau governs the decision boundary between Genuine matches and Imposters. If tau is too low (e.g., 0.50), False Acceptance Rate (FAR) spikes, causing unregistered visitors or friends to be falsely recognized. If tau is too high (e.g., 0.95), False Rejection Rate (FRR) increases, and enrolled students with slight expression changes are marked Unknown. We validated tau using the Labeled Faces in the Wild (LFW) dataset across 6,000 paired comparisons (3,000 positive, 3,000 negative) by computing the ROC curve and finding the Equal Error Rate (EER) point where FAR equals FRR (~4.6%). In our multi-sample gallery trials, tau = 0.75 provides zero false acceptances while maintaining robust verification.\""
        ),
        (
            "Q6. How did you optimize the system to achieve 30 FPS on standard laptop CPU without a GPU?",
            "\"We diagnosed the bottleneck using CPU profiling. MTCNN face proposal scanning over a full 640x480 frame takes ~110 ms on CPU. We implemented three engineering optimizations: (1) Spatial Subsampling: We scale down the detection frame by 0.5x (to 320x240), reducing pixel search space by 75%, which lowered MTCNN detection time to ~25 ms. Coordinates are mapped back 2.0x to extract the high-resolution crop for Inception-ResNet. (2) Temporal Frame Skipping: Deep inference executes once every 3rd frame, while the display HUD interpolates the bounding box across intermediate frames. (3) OpenCV DirectShow Backend: We configured cv2.CAP_DSHOW and locked CAP_PROP_BUFFERSIZE to 1, preventing the camera driver from buffering stale frames. Combined, this yielded ~30 FPS throughput.\""
        ),
        (
            "Q7. What dataset was the Inception-ResNet-v1 model pretrained on?",
            "\"It is pretrained on the VGGFace2 dataset, which contains 3.31 million facial images spanning 9,131 distinct identities. The dataset was specifically curated to capture broad intra-class variations in human age, ethnicity, illumination, and head pose. Because of this extensive pretraining, the network has learned highly generalized facial feature extraction filters, eliminating the need to train a new network from scratch on student data.\""
        ),
        (
            "Q8. How does the system handle duplicate attendance marking in a single session?",
            "\"We implemented an AttendanceLogger state machine. Upon session start, all enrolled students in the gallery are pre-initialized with Status='Absent' and Time='--'. When a student is identified with similarity >= tau, mark_present(name) checks if their status is already 'Present'. If yes, it immediately returns False without modifying records. If it is their first recognition, it stamps the current system time (HH:MM:SS), sets Status='Present', and atomically writes to the CSV log. This guarantees exactly one record per student per lecture.\""
        ),
        (
            "Q9. What is the difference between Open-Set and Closed-Set face recognition?",
            "\"Closed-Set assumes every face presented to the camera belongs to a known enrolled individual in the database. Open-Set assumes the face might belong to an enrolled person or an unregistered outsider. Academic classrooms are inherently Open-Set: delivery personnel, visitors, or students from other batches might enter the camera view. Our system handles Open-Set recognition through thresholded metric comparison: unless max(similarity) >= tau, the person is tagged as 'Unknown'.\""
        ),
        (
            "Q10. How does the system work on Cloud Deployment vs. Local Laptop?",
            "\"On local laptops, the app directly interfaces with the hardware camera via OpenCV (cv2.VideoCapture) using DirectShow. However, cloud servers (such as Streamlit Community Cloud) run on headless Linux virtual machines with no physical camera attached. To solve this, we implemented WebRTC using streamlit-webrtc. In the cloud, the client browser accesses the user's laptop camera via the HTML5 getUserMedia() API and transmits video packets via WebRTC to the Python backend through Google STUN and public TURN relay servers. The app auto-detects the environment silently.\""
        ),
        (
            "Q11. What are the current limitations of your system?",
            "\"Currently, the system has two main limitations: (1) Severe physical occlusions: If a student is wearing a full medical face mask covering the nose and mouth, MTCNN landmark regression and Inception-ResNet accuracy degrade because critical lower-facial geometry is hidden. (2) 2D Presentation Attacks (Spoofing): Standard webcams capture RGB data without infrared or time-of-flight depth sensors, meaning a high-resolution printed photograph could potentially fool the system. In future work, we plan to implement software-based temporal eye-blink and micro-expression liveness detection.\""
        ),
        (
            "Q12. What is the LFW benchmark and what do your results (95.2% accuracy, 0.984 AUC) mean?",
            "\"LFW (Labeled Faces in the Wild) is the gold standard academic benchmark for unconstrained facial verification. It contains 13,233 images of 5,749 people collected from the web. The standard verification protocol evaluates 6,000 face pairs: 3,000 matched pairs (same person) and 3,000 mismatched pairs (different people). An accuracy of 95.2% proves that the model generalizes robustly across arbitrary human faces, while an Area Under the ROC Curve (AUC) of 0.984 confirms near-perfect separability between genuine and imposter similarity distributions.\""
        ),
        (
            "Q13. How many photos are required per student for optimal enrollment?",
            "\"We found that 8 to 12 photos per student provide the optimal trade-off. Enrolling only 1 photo makes the model vulnerable to slight pose or lighting changes. Enrolling more than 15 images yields diminishing returns and slightly increases gallery comparison search time. The enrollment photos should cover standard variations: frontal view, +/- 15 degree left/right yaw, slight tilt, and natural classroom ambient illumination.\""
        ),
        (
            "Q14. What are the ethical and privacy considerations of this project?",
            "\"Privacy is preserved through four design choices: (1) Consent-based local enrollment: Only students who volunteer and consent are enrolled; (2) Feature-vector storage: We store 512-dimensional numerical float embeddings, not raw facial photographs. Mathematically, reconstructing the original face image from a 512-D embedding is non-trivial and acts as a one-way feature extraction; (3) Local offline storage: Gallery vectors and attendance logs are saved in local CSV and NPY files on institutional storage without transmission to commercial cloud AI APIs.\""
        ),
        (
            "Q15. How can this prototype be scaled to a university with thousands of students?",
            "\"For a classroom of 60 to 100 students, calculating dot products against 1,000 vectors takes less than 1 millisecond on CPU. For an entire university campus of 10,000+ students, linear searching would scale as O(N). To scale up, we would replace linear array search with Approximate Nearest Neighbor (ANN) indexers such as Meta Faiss or HNSW (Hierarchical Navigable Small World graphs). In addition, cameras deployed across classrooms would run on edge devices like NVIDIA Jetson Nano, sending JSON timestamps to a central PostgreSQL database via secure REST APIs.\""
        ),
    ]
    
    for q, a in viva_qa:
        p_q = Paragraph(q, q_style)
        p_a = Paragraph(a, ans_style)
        story.append(KeepTogether([p_q, p_a]))
    
    # -------------------------------------------------------------
    # PART 4: SYSTEM HARDWARE & SOFTWARE SPECIFICATIONS
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("PART 4: SYSTEM SPECIFICATIONS & DEPLOYMENT ARCHITECTURE", sec_heading))
    
    specs_data = [
        ["Parameter", "Specification / Implementation Choice", "Engineering Rationale"],
        ["Programming Language", "Python 3.11 / 3.12 (Venv)", "Broad library support for PyTorch, OpenCV, and WebRTC."],
        ["Deep Learning Framework", "PyTorch 2.x (CPU Engine)", "Tensor operations and pre-trained Facenet-PyTorch integration."],
        ["Face Detector", "MTCNN (P-Net, R-Net, O-Net)", "Multi-task coarse-to-fine bounding box and 5-point landmark alignment."],
        ["Embedding Extractor", "Inception-ResNet-v1 (VGGFace2)", "512-D metric representation with high discriminative inter-class separation."],
        ["Metric & Decision Rule", "L2-Norm + Cosine Similarity (τ = 0.75)", "Fast dot-product inference on unit sphere; rejects outsiders as Unknown."],
        ["Local Camera Interface", "OpenCV DirectShow (CAP_DSHOW)", "Direct hardware webcam binding with zero latency buffer queuing."],
        ["Cloud Camera Interface", "Streamlit-WebRTC + STUN/TURN", "Browser HTML5 getUserMedia capture for cloud VM server streaming."],
        ["Attendance Persistence", "Thread-Safe CSV Exporter", "Atomic timestamped session records with deduplication logic."],
        ["GUI Framework", "Streamlit Custom Dashboard", "Interactive modern UI with live session status cards and report viewer."]
    ]
    t_specs = Table(specs_data, colWidths=[120, 206, 210])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,1), (-1,-1), 7.8),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_specs)
    story.append(Spacer(1, 14))
    
    # -------------------------------------------------------------
    # PART 5: STEP-BY-STEP LIVE DEMO RUNBOOK FOR FACULTY
    # -------------------------------------------------------------
    story.append(Paragraph("PART 5: STEP-BY-STEP LIVE DEMO RUNBOOK (DURING PRESENTATION)", sec_heading))
    story.append(Paragraph(
        "Follow this exact sequential runbook when performing the live demonstration in front of faculty:",
        body_style
    ))
    
    runbook_steps = [
        ["Step 1", "Launch App", "Double-click <b>run_app.bat</b> on the laptop Desktop. Opens the dashboard at http://localhost:8501 instantly with zero network lag."],
        ["Step 2", "Show Sidebar", "Point out the academic profile: <b>Ramdeobaba University, Dept. of Electronics Engineering</b>, enrolled student count, 512-D vectors, and threshold τ = 0.75."],
        ["Step 3", "Start Live Session", "Click <b>▶ Start Session</b> under the 'Live Attendance' tab. Show that the laptop webcam activates immediately with bounding boxes."],
        ["Step 4", "Demonstrate Recognition", "Stand in front of the camera: Bounding box turns <b>GREEN</b> displaying your name (e.g. 'Meet' or 'Pratham') with similarity % (e.g. 84.5%). The top HUD updates from Absent to Present."],
        ["Step 5", "Demonstrate 'Unknown' Rejection", "Have an unregistered friend or photo step into view: Bounding box turns <b>RED</b> displaying 'Unknown' (similarity < 0.75). Attendance is NOT marked, proving proxy prevention."],
        ["Step 6", "Save & View Report", "Click <b>⏹ Save Attendance</b>. Switch to the <b>'Attendance Reports'</b> tab. Show the faculty the automatically generated CSV table with exact timestamps and click 'Export CSV'."]
    ]
    t_runbook = Table(runbook_steps, colWidths=[50, 130, 356])
    t_runbook.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EEF2FF")),
        ('FONTNAME', (0,0), (1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (1,-1), SECONDARY),
        ('FONTNAME', (2,0), (2,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_runbook)
    
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Generated Faculty Viva Guide PDF successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_viva_pdf()
