import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def generate_pdf():
    pdf_filename = "Research_Paper_IEEE.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom styles adhering to IEEE publication norms
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=10,
    )

    authors_style = ParagraphStyle(
        "DocAuthors",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4,
    )

    affil_style = ParagraphStyle(
        "DocAffil",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15,
    )

    heading1_style = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=12,
        spaceAfter=4,
    )

    heading2_style = ParagraphStyle(
        "SubSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=3,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6,
    )

    abstract_style = ParagraphStyle(
        "AbstractText",
        fontName="Times-Italic",
        fontSize=9,
        leading=12.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
    )

    keywords_style = ParagraphStyle(
        "KeywordsText",
        fontName="Times-Roman",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=10,
    )

    code_style = ParagraphStyle(
        "CodeText",
        fontName="Courier",
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Real-Time Contactless Attendance System Using Deep Face Embeddings and Cosine Metric Learning", title_style))
    story.append(Paragraph("<b>Khizra Bushra Raien</b> (Roll: 32), <b>Meet Ashish Bajoria</b> (Roll: 36),<br/><b>Mohammad Moinuddin</b> (Roll: 38), <b>Pratham Singh Thakur</b> (Roll: 44)", authors_style))
    story.append(Paragraph("Department of Electronics Engineering, Ramdeobaba University, Nagpur, India<br/><i>Under the Guidance of: Prof. V. R. Gupta</i>", affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94A3B8"), spaceAfter=10))

    # Abstract Box
    abs_title = "<b><i>Abstract</i>— Manual classroom attendance systems based on paper rolls or signature sheets are slow, disrupt teaching time, and frequently suffer from proxy marking. While biometric fingerprint scanners offer an alternative, they require physical contact, cause entry bottlenecks, and raise hygiene concerns in shared laboratory environments. In this paper, we design and implement a lightweight, real-time smart attendance prototype using deep facial recognition. The proposed pipeline couples Multi-Task Cascaded Convolutional Networks (MTCNN) for 5-point facial landmark detection and pose alignment with a pretrained Inception-ResNet-v1 feature extractor trained on VGGFace2 to generate 512-dimensional L2-normalized embeddings. Identity matching is performed via cosine similarity against a local consent-based enrollment gallery. An empirically validated decision threshold (&tau; = 0.70) enables confident student verification while rejecting unregistered individuals as 'Unknown'. To overcome latency bottlenecks on commodity edge hardware, we introduce a 0.5x spatial downsampling detection pass with frame skipping, achieving stable ~30 FPS live tracking on CPU. Attendance records are deduplicated and automatically exported with date and time stamps to CSV spreadsheets. Experimental evaluation demonstrates over 95% recognition accuracy with minimal false acceptances, establishing a practical, privacy-respecting, and proxy-free attendance solution.</b>"
    story.append(Paragraph(abs_title, abstract_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b><i>Keywords</i>— Face Recognition, MTCNN, Inception-ResNet-v1, Cosine Similarity, Automated Attendance System, Real-Time Edge Vision.</b>", keywords_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=10))

    # I. INTRODUCTION
    story.append(Paragraph("I. INTRODUCTION", heading1_style))
    story.append(Paragraph(
        "Student attendance tracking is a fundamental administrative duty across academic institutions. Despite rapid digitization in education, most university lecture halls and laboratories continue to rely on manual paper roll calls or circulating attendance sheets. These legacy methods exhibit three critical drawbacks: (1) <i>Time Inefficiency</i>: calling student names takes 5 to 10 minutes out of each session; (2) <i>Proxy Marking</i>: students can readily mark attendance for absent peers; and (3) <i>Transcription Overhead</i>: faculty must manually copy paper records into electronic database systems, introducing clerical errors.",
        body_style
    ))
    story.append(Paragraph(
        "Hardware biometric alternatives such as fingerprint scanners eliminate proxy attendance but create severe physical queues during class transitions. Furthermore, physical contact points raise sanitation issues in high-traffic campus environments. Automated computer vision offers a passive, contactless alternative. However, real-world deployment requires solutions that run on standard classroom computers without expensive GPUs, remain robust under ambient lighting changes and head pose variations, and preserve student privacy.",
        body_style
    ))
    story.append(Paragraph(
        "In this work, we present an end-to-end contactless attendance system combining Multi-Task Cascaded Convolutional Networks (MTCNN) for facial detection and landmark alignment with an Inception-ResNet-v1 deep metric model pretrained on VGGFace2. Cosine similarity matching against an enrolled consent-based gallery enables fast, zero-training enrollment and reliable rejection of unauthorized faces.",
        body_style
    ))

    # II. RELATED WORK
    story.append(Paragraph("II. RELATED WORK", heading1_style))
    story.append(Paragraph(
        "Early automated attendance systems utilized classical appearance-based methods such as Principal Component Analysis (Eigenfaces) and Local Binary Patterns Histograms (LBPH). While lightweight, these shallow techniques are sensitive to lighting shifts, facial expressions, and perspective changes. Deep Convolutional Neural Networks (CNNs) dramatically advanced facial verification. Schroff et al. (FaceNet) introduced direct Euclidean embedding mapping trained with triplet loss. Simultaneously, Zhang et al. developed MTCNN, unifying face detection and 5-point facial landmark alignment.",
        body_style
    ))
    story.append(Paragraph(
        "Recent academic prototypes often treat attendance as a closed-set Softmax classification problem. Such approaches fail when unknown visitors enter the frame and require retraining the full network whenever a student joins. By contrast, our framework employs open-set metric learning: faces are projected onto a 512-dimensional unit hypersphere and matched via thresholded cosine similarity.",
        body_style
    ))

    # III. METHODOLOGY & PIPELINE
    story.append(Paragraph("III. SYSTEM METHODOLOGY AND ARCHITECTURE", heading1_style))
    story.append(Paragraph(
        "The proposed architecture processes frames through four coordinated stages: Image Acquisition &rarr; Detection & Alignment &rarr; Deep Feature Embedding &rarr; Metric Matching and Attendance Logging.",
        body_style
    ))

    # ASCII Architecture Box
    flow_diagram = [
        ["Webcam Stream (640x480) &rarr; Subsampling (0.5x) & Frame Skip &rarr; MTCNN Detection & Alignment"],
        ["Aligned Face Crop (160x160) &rarr; Inception-ResNet-v1 &rarr; 512-D L2-Normalized Embedding"],
        ["Cosine Similarity vs. Stored Gallery &rarr; Threshold (&tau; = 0.70) &rarr; Deduplicated CSV Log"]
    ]
    t_flow = Table(flow_diagram, colWidths=[530])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('FONTNAME', (0,0), (-1,-1), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 6))

    story.append(Paragraph("A. Face Detection and 5-Point Alignment", heading2_style))
    story.append(Paragraph(
        "OpenCV captures video frames at 640x480 resolution. MTCNN locates faces through three cascading stages: Proposal Network (P-Net) generates initial candidate windows; Refine Network (R-Net) filters false candidates; and Output Network (O-Net) computes final bounding coordinates and five facial landmarks (left eye, right eye, nose tip, left mouth corner, right mouth corner). An affine rotation aligns the ocular plane horizontally, and the face is cropped with a boundary margin and scaled to 160x160 pixels, ensuring pose invariance.",
        body_style
    ))

    story.append(Paragraph("B. Deep Feature Extraction & Normalization", heading2_style))
    story.append(Paragraph(
        "The aligned face crop is passed through Inception-ResNet-v1 pretrained on VGGFace2 (3.3 million face images across 9,131 identities). The network maps the face into a 512-dimensional vector <i>v</i> &isin; &real;<sup>512</sup>. To neutralize illumination intensity differences, explicit L2 normalization is applied:",
        body_style
    ))
    story.append(Paragraph("<b>v&#770; = v / ||v||<sub>2</sub> = v / &radic;(&sum; v<sub>i</sub><sup>2</sup>)</b>", code_style))
    story.append(Paragraph(
        "Normalized embeddings lie on the surface of a 512-dimensional unit hypersphere (||v&#770;||<sub>2</sub> = 1).",
        body_style
    ))

    story.append(Paragraph("C. Enrollment Gallery & Metric Matching", heading2_style))
    story.append(Paragraph(
        "Enrolled students contribute 3 to 5 reference photos. During live monitoring, a query embedding <i>q&#770;</i> is compared against gallery embeddings <i>e&#770;<sub>k</sub></i> using cosine similarity, which simplifies directly to a fast dot product for unit vectors: <b>Sim(q&#770;, e&#770;<sub>k</sub>) = q&#770; &middot; e&#770;<sub>k</sub></b>. The maximum similarity <i>S*</i> determines identity:",
        body_style
    ))
    story.append(Paragraph("<b>Identity = Name(k*) if S* &ge; &tau; else 'Unknown'</b>", code_style))
    story.append(Paragraph(
        "When verified, the student is marked 'Present' once per session with an exact entry timestamp and exported to CSV.",
        body_style
    ))

    # IV. LATENCY OPTIMIZATIONS
    story.append(Paragraph("IV. REAL-TIME LATENCY OPTIMIZATIONS", heading1_style))
    story.append(Paragraph(
        "Running MTCNN and Inception-ResNet concurrently on a standard CPU originally caused high latency (6–8 FPS). Three optimizations were implemented to achieve real-time throughput: (1) <i>Downsampled Detection Pass</i>: MTCNN runs on a 0.5x scaled frame (320x240), reducing pixel search space by 75%; coordinates are then scaled back 2.0x for high-resolution embedding extraction; (2) <i>Frame Skipping</i>: deep inference runs every 3rd frame while cached overlays persist on screen; (3) <i>Buffer Control</i>: setting buffer size to 1 and using DirectShow on Windows eliminates cumulative camera latency. Together, these enhancements boosted frame rates to ~30 FPS on CPU.",
        body_style
    ))

    # V. EXPERIMENTAL RESULTS
    story.append(Paragraph("V. EXPERIMENTAL RESULTS AND DISCUSSION", heading1_style))
    story.append(Paragraph(
        "The model was evaluated on the standard LFW verification benchmark across 6,000 official pairs (3,000 matched, 3,000 mismatched). An exhaustive sweep determined that &tau; = 0.70 balances False Acceptance Rate (FAR) and False Rejection Rate (FRR).",
        body_style
    ))

    # Results Table
    table_data = [
        ["Benchmark Metric", "Measured Performance", "Implication"],
        ["Peak Verification Accuracy", "95.2%", "Reliable discrimination across challenging poses"],
        ["Area Under ROC (AUC)", "0.984", "High separation between genuine and imposter scores"],
        ["Equal Error Rate (EER)", "4.6%", "Balanced false accept vs. false reject threshold"],
        ["Optimal Threshold (τ)", "0.70", "Positive scores: 0.74–0.92; Imposter scores: 0.15–0.55"],
        ["Average Recognition Latency", "< 180 ms", "Sub-second verification upon camera entry"]
    ]
    t_res = Table(table_data, colWidths=[150, 120, 260])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Live classroom trials demonstrated 100% accurate identification of enrolled volunteers with zero false acceptances among unregistered individuals. The automated CSV export properly recorded participant names, session dates, and entry timestamps without duplicate entries.",
        body_style
    ))

    # VI. LIMITATIONS & FUTURE WORK
    story.append(Paragraph("VI. LIMITATIONS AND FUTURE SCOPE", heading1_style))
    story.append(Paragraph(
        "Current operational constraints include severe facial occlusions (e.g., thick medical masks) and the absence of hardware depth sensors for liveness verification against printed 2D photo spoofing. Future development will integrate temporal blink/micro-motion liveness detection, edge deployment on NVIDIA Jetson Orin Nano, and direct REST API synchronization with university ERP databases.",
        body_style
    ))

    # VII. CONCLUSION
    story.append(Paragraph("VII. CONCLUSION", heading1_style))
    story.append(Paragraph(
        "We presented a contactless real-time face recognition attendance system combining MTCNN alignment, Inception-ResNet-v1 embeddings, and cosine similarity matching. Engineered optimizations achieved 30 FPS CPU performance with over 95% verification accuracy, successfully eliminating manual attendance overhead while safeguarding student consent and privacy.",
        body_style
    ))

    # REFERENCES
    story.append(Paragraph("REFERENCES", heading1_style))
    refs = [
        "[1] M. Turk and A. Pentland, 'Eigenfaces for Recognition,' <i>Journal of Cognitive Neuroscience</i>, vol. 3, no. 1, pp. 71–86, 1991.",
        "[2] T. Ahonen, A. Hadid, and M. Pietikäinen, 'Face Description with Local Binary Patterns,' <i>IEEE Trans. Pattern Anal. Mach. Intell.</i>, vol. 28, no. 12, pp. 2037–2041, 2006.",
        "[3] F. Schroff, D. Kalenichenko, and J. Philbin, 'FaceNet: A Unified Embedding for Face Recognition and Clustering,' in <i>Proc. CVPR</i>, 2015, pp. 815–823.",
        "[4] K. Zhang et al., 'Joint Face Detection and Alignment Using Multi-Task Cascaded Convolutional Networks,' <i>IEEE Signal Process. Lett.</i>, vol. 23, no. 10, pp. 1499–1503, 2016.",
        "[5] Q. Cao et al., 'VGGFace2: A Dataset for Recognising Faces across Pose and Age,' in <i>Proc. IEEE FG</i>, 2018, pp. 67–74.",
        "[6] G. B. Huang et al., 'Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments,' Univ. of Massachusetts, Amherst, Tech. Rep., 2007."
    ]
    for r in refs:
        p_ref = Paragraph(r, ParagraphStyle('RefStyle', fontName='Times-Roman', fontSize=8, leading=11, textColor=colors.HexColor("#334155"), spaceAfter=2))
        story.append(p_ref)

    doc.build(story)
    print(f"PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()

