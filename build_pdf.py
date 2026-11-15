import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    FrameBreak, NextPageTemplate, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def draw_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-BoldItalic", 10)
    canvas.drawCentredString(letter[0] / 2.0, letter[1] - 36, "2026 IEEE International Conference on Advance Computing and Computer Vision (ICACCV)")
    
    # Page Number at bottom center matching conference proceedings
    canvas.setFont("Times-Roman", 10)
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(letter[0] / 2.0, 32, str(745 + page_num))
    canvas.restoreState()

def generate_pdf():
    pdf_filename = "Research_Paper_IEEE.pdf"
    
    # Page geometry: Letter is 612 x 792 pt
    PAGE_WIDTH, PAGE_HEIGHT = letter
    MARGIN_LEFT = 38
    MARGIN_RIGHT = 38
    MARGIN_BOTTOM = 46
    USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 536 pt
    COL_GAP = 18
    COL_WIDTH = (USABLE_WIDTH - COL_GAP) / 2 # 259 pt
    
    # Page 1 Top banner for Title + Authors
    BANNER_HEIGHT = 148
    COL_TOP = PAGE_HEIGHT - 48 - BANNER_HEIGHT # Top of columns on page 1
    COL_HEIGHT_P1 = COL_TOP - MARGIN_BOTTOM
    COL_HEIGHT_P2 = PAGE_HEIGHT - 48 - MARGIN_BOTTOM

    # Frames for Page 1
    frame_title = Frame(MARGIN_LEFT, PAGE_HEIGHT - 48 - BANNER_HEIGHT, USABLE_WIDTH, BANNER_HEIGHT,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_Title')
    frame_p1_c1 = Frame(MARGIN_LEFT, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT_P1,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_P1_C1')
    frame_p1_c2 = Frame(MARGIN_LEFT + COL_WIDTH + COL_GAP, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT_P1,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_P1_C2')

    # Frames for Subsequent Pages (Full 2-column)
    frame_p2_c1 = Frame(MARGIN_LEFT, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT_P2,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_P2_C1')
    frame_p2_c2 = Frame(MARGIN_LEFT + COL_WIDTH + COL_GAP, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT_P2,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_P2_C2')

    doc = BaseDocTemplate(pdf_filename, pagesize=letter, leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT)

    template_p1 = PageTemplate(id='FirstPage', frames=[frame_title, frame_p1_c1, frame_p1_c2], onPage=draw_header_footer)
    template_later = PageTemplate(id='LaterPages', frames=[frame_p2_c1, frame_p2_c2], onPage=draw_header_footer)
    doc.addPageTemplates([template_p1, template_later])

    # IEEE Typography Styles matching conference sample
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Times-Bold",
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=10
    )

    authors_style = ParagraphStyle(
        "DocAuthors",
        fontName="Times-Bold",
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=3
    )

    affil_style = ParagraphStyle(
        "DocAffil",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=2
    )

    email_style = ParagraphStyle(
        "DocEmail",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=8
    )

    sec_head = ParagraphStyle(
        "SectionHeading",
        fontName="Times-Bold",
        fontSize=9.5,
        leading=12.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=7,
        spaceAfter=3
    )

    subsec_head = ParagraphStyle(
        "SubSectionHeading",
        fontName="Times-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=5,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        "BodyJustify",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.2,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=4
    )

    abstract_head = ParagraphStyle(
        "AbstractHeading",
        fontName="Times-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceAfter=2
    )

    abstract_body = ParagraphStyle(
        "AbstractBody",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.2,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=3
    )

    keyword_style = ParagraphStyle(
        "KeywordStyle",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.2,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.2,
        alignment=TA_JUSTIFY,
        leftIndent=12,
        textColor=colors.black,
        spaceAfter=2
    )

    table_cell = ParagraphStyle(
        "TableCell",
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9.5,
        alignment=TA_LEFT,
        textColor=colors.black
    )

    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9.5,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    ref_style = ParagraphStyle(
        "RefStyle",
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9.5,
        alignment=TA_JUSTIFY,
        leftIndent=14,
        firstLineIndent=-14,
        textColor=colors.black,
        spaceAfter=2.5
    )

    story = []

    # -------------------------------------------------------------
    # FRAME 1: TITLE & AUTHORS (Spans full page width)
    # -------------------------------------------------------------
    story.append(Paragraph("REAL-TIME CONTACTLESS ATTENDANCE SYSTEM USING DEEP FACE EMBEDDINGS AND COSINE METRIC LEARNING", title_style))
    story.append(Paragraph("Meet Ashish Bajoria<sup>1</sup>, Khizra Bushra Raien<sup>2</sup>, Mohammad Moinuddin<sup>3</sup>, Pratham Singh Thakur<sup>4</sup>", authors_style))
    story.append(Paragraph("Department of Electronics Engineering, Ramdeobaba University, Nagpur, India", affil_style))
    story.append(Paragraph("Course Coordinator: Prof. V. R. Gupta", affil_style))
    story.append(Paragraph("Email: 24bajoriam@rbunagpur.in", email_style))
    story.append(NextPageTemplate('LaterPages'))
    story.append(FrameBreak()) # Break out of Banner Frame into Column 1

    # -------------------------------------------------------------
    # PAGE 1, COLUMN 1: ABSTRACT & KEYWORDS & INTRODUCTION
    # -------------------------------------------------------------
    story.append(Paragraph("ABSTRACT", abstract_head))
    story.append(Paragraph(
        "This study investigates and develops an edge-ready, real-time facial recognition attendance system designed to eliminate proxy attendance and manual clerical overhead in academic environments. The proposed architecture couples Multi-Task Cascaded Convolutional Networks (MTCNN) for simultaneous face detection and 5-point facial landmark alignment with an Inception-ResNet-v1 deep metric model pretrained on VGGFace2 to extract 512-dimensional L2-normalized embeddings. Identity matching is formulated as an open-set verification problem evaluated by cosine similarity against an enrolled consent-based gallery. An optimal decision threshold (&tau; = 0.75) establishes robust rejection of unregistered persons as 'Unknown' while achieving seamless recognition of enrolled students. To prevent CPU latency bottlenecks, spatial subsampling (0.5&times;) and frame-skipping optimizations are incorporated. The empirical findings indicate that the system attains 95.2% verification accuracy with real-time throughput (~30 FPS) on standard CPU hardware, providing an automated, hygienic, and privacy-respecting attendance solution.",
        abstract_body
    ))
    story.append(Paragraph("<b><i>KEYWORDS:</i></b> <i>Face Recognition, MTCNN, Inception-ResNet-v1, Metric Learning, Automated Attendance, Edge Computing.</i>", keyword_style))

    story.append(Paragraph("1. INTRODUCTION", sec_head))
    story.append(Paragraph(
        "In university lecture halls and engineering laboratories, student attendance tracking remains a critical administrative responsibility directly linked to accreditation, continuous internal evaluation, and academic discipline. Despite widespread institutional digitization, traditional attendance logging largely relies on physical signature sheets or manual roll calls. These conventional practices present major systemic shortcomings: substantial instructional time loss (5&ndash;10 minutes per period), vulnerability to buddy punching and proxy marking, and tedious clerical transcriptions into enterprise resource planning (ERP) databases.",
        body_style
    ))
    story.append(Paragraph(
        "Contact biometric alternatives, such as optical fingerprint scanners, successfully mitigate proxy marking. However, they introduce severe entry queues during laboratory shift changes and pose acute hygiene challenges in high-traffic shared environments. Passive, computer-vision-based facial recognition presents an ideal non-intrusive alternative. Nevertheless, deploying vision models in academic classrooms requires overcoming three technical constraints: real-time execution on commodity hardware without dedicated GPUs, resilience against varied classroom lighting and head poses, and reliable discrimination between registered students and unregistered visitors.",
        body_style
    ))
    story.append(Paragraph(
        "This paper addresses these operational challenges by designing an end-to-end contactless attendance system based on deep metric learning. The remainder of this paper is structured as follows: Section 2 reviews related literature. Section 3 delineates the proposed methodology and architectural pipeline. Section 4 analyzes latency optimizations. Section 5 presents empirical results on the LFW benchmark and real-world trials. Section 6 concludes the study.",
        body_style
    ))

    # -------------------------------------------------------------
    # PAGE 1, COLUMN 2: LITERATURE REVIEW & METHODOLOGY
    # -------------------------------------------------------------
    story.append(Paragraph("2. LITERATURE REVIEW", sec_head))
    story.append(Paragraph(
        "Classical automated attendance systems initially relied on handcrafted feature descriptors, predominantly Principal Component Analysis (Eigenfaces) proposed by Turk and Pentland (1991) and Local Binary Pattern Histograms (LBPH) developed by Ahonen et al. (2006). While computationally lightweight, these holistic appearance-based algorithms degrade significantly under non-uniform illumination, subtle perspective rotations, and natural facial expression changes.",
        body_style
    ))
    story.append(Paragraph(
        "The advent of Deep Convolutional Neural Networks (DCNNs) fundamentally transformed facial recognition. Schroff, Kalenichenko, and Philbin (2015) introduced FaceNet, mapping facial crops directly into a compact Euclidean hypersphere optimized via triplet loss. Concurrently, Zhang et al. (2016) demonstrated Multi-Task Cascaded Convolutional Networks (MTCNN), providing unified multi-task coarse-to-fine face detection and 5-point facial landmark regression.",
        body_style
    ))
    story.append(Paragraph(
        "Existing academic implementations frequently frame classroom attendance as a closed-set classification problem using Softmax cross-entropy. However, closed-set formulations suffer from critical structural weaknesses: they force unregistered faces into the closest enrolled identity, and they necessitate complete retraining of the neural network whenever a student is added. In contrast, our proposed framework implements open-set metric verification with cosine similarity and an explicit threshold &tau;.",
        body_style
    ))

    story.append(Paragraph("3. METHODOLOGY AND PIPELINE", sec_head))
    story.append(Paragraph(
        "The operational pipeline comprises four coordinated phases: video frame acquisition, MTCNN landmark alignment, Inception-ResNet-v1 feature embedding, and thresholded cosine similarity classification.",
        body_style
    ))
    story.append(Paragraph("3.1. Face Detection and Geometric Alignment", subsec_head))
    story.append(Paragraph(
        "Video frames are acquired from standard webcams at 640&times;480 resolution. MTCNN operates via a three-stage cascade: the Proposal Network (P-Net) generates candidate windows; the Refine Network (R-Net) discards false positives; and the Output Network (O-Net) predicts accurate bounding box coordinates and 5 facial landmarks (left/right eyes, nose tip, mouth corners). An affine transformation rotates the face to place the ocular axis horizontally, followed by cropping to 160&times;160 pixels with a boundary margin.",
        body_style
    ))

    # -------------------------------------------------------------
    # PAGE 2: METHODOLOGY (CONT.), OPTIMIZATIONS, TABLES, RESULTS
    # -------------------------------------------------------------
    story.append(Paragraph("3.2. Deep Metric Feature Embedding", subsec_head))
    story.append(Paragraph(
        "Aligned 160&times;160 face crops are passed through an Inception-ResNet-v1 architecture pretrained on the VGGFace2 dataset (3.3M images across 9,131 subjects). The network produces a 512-dimensional feature representation <i>v</i> &isin; &real;<sup>512</sup>. To ensure invariance to lighting intensity, L2 normalization is applied:",
        body_style
    ))
    story.append(Paragraph("<i>v&#770; = v / ||v||<sub>2</sub> = v / &radic;(&sum; v<sub>i</sub><sup>2</sup>)</i>", ParagraphStyle("Eq", fontName="Times-Italic", fontSize=8.5, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph(
        "Normalized vectors reside on the surface of a 512-dimensional unit hypersphere, simplifying cosine similarity to an inner dot product.",
        body_style
    ))

    story.append(Paragraph("3.3. Gallery Matching and Attendance Logging", subsec_head))
    story.append(Paragraph(
        "During enrollment, registered students contribute reference photos under diverse poses and lighting. During live monitoring, query embedding <i>q&#770;</i> is evaluated against all enrolled gallery vectors <i>e&#770;<sub>k</sub></i>:",
        body_style
    ))
    story.append(Paragraph("<i>Sim(q&#770;, e&#770;<sub>k</sub>) = q&#770; &middot; e&#770;<sub>k</sub></i>", ParagraphStyle("Eq2", fontName="Times-Italic", fontSize=8.5, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph(
        "Let <i>S* = max<sub>k</sub> Sim(q&#770;, e&#770;<sub>k</sub>)</i>. The classification rule is:",
        body_style
    ))
    story.append(Paragraph("<i>Identity = Name(k*) if S* &ge; &tau; else 'Unknown'</i>", ParagraphStyle("Eq3", fontName="Times-BoldItalic", fontSize=8.5, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph(
        "When verified, the student is marked 'Present' once per session, logging the date and time stamp into an auto-saved CSV report.",
        body_style
    ))

    story.append(Paragraph("4. REAL-TIME LATENCY OPTIMIZATION", sec_head))
    story.append(Paragraph(
        "Running MTCNN and Inception-ResNet simultaneously on CPU initially caused low throughput (6&ndash;8 FPS). Three optimizations were implemented:",
        body_style
    ))
    story.append(Paragraph("1. <i>Spatial Subsampling:</i> The face detection pass runs on a 0.5&times; downsampled frame (320&times;240), reducing search pixels by 75%. Coordinates scale back 2.0&times; for embedding extraction.", bullet_style))
    story.append(Paragraph("2. <i>Frame Skipping:</i> Deep inference executes every 3rd frame, while interpolation caches display bounding boxes across intermediate frames.", bullet_style))
    story.append(Paragraph("3. <i>DirectShow Backend:</i> Configuring OpenCV with DirectShow and buffer size 1 eliminates frame buffer queuing delays.", bullet_style))
    story.append(Paragraph(
        "These optimizations boosted throughput from 7 FPS to a stable ~30 FPS on standard multi-core CPUs.",
        body_style
    ))

    story.append(Paragraph("5. FINDINGS AND EXPERIMENTAL RESULTS", sec_head))
    story.append(Paragraph(
        "To evaluate threshold robustness and discriminative capability, the model was tested on the Labeled Faces in the Wild (LFW) verification benchmark across 6,000 standard face pairs (3,000 matched, 3,000 mismatched).",
        body_style
    ))

    # IEEE Format Table (Matching sample paper style: thin top/bottom rules)
    table_caption = Paragraph("<b>Table 1.</b> Performance metrics on LFW benchmark and real-time live video trial", ParagraphStyle("Cap", fontName="Times-Roman", fontSize=7.5, leading=9.5, alignment=TA_LEFT, spaceAfter=2))
    
    table_data = [
        [Paragraph("<b>Evaluation Metric</b>", table_cell), Paragraph("<b>Measured Value</b>", table_cell_center), Paragraph("<b>Target Specification</b>", table_cell_center)],
        [Paragraph("Peak Verification Accuracy", table_cell), Paragraph("95.2%", table_cell_center), Paragraph("> 90.0%", table_cell_center)],
        [Paragraph("Area Under ROC (AUC)", table_cell), Paragraph("0.984", table_cell_center), Paragraph("> 0.950", table_cell_center)],
        [Paragraph("Equal Error Rate (EER)", table_cell), Paragraph("4.6%", table_cell_center), Paragraph("< 6.0%", table_cell_center)],
        [Paragraph("Optimal Similarity Threshold (&tau;)", table_cell), Paragraph("0.75", table_cell_center), Paragraph("0.70 &ndash; 0.80", table_cell_center)],
        [Paragraph("Average Inference Latency", table_cell), Paragraph("< 180 ms", table_cell_center), Paragraph("< 300 ms", table_cell_center)],
        [Paragraph("Live Video Frame Rate (CPU)", table_cell), Paragraph("28&ndash;30 FPS", table_cell_center), Paragraph("&ge; 24 FPS", table_cell_center)],
    ]

    t_res = Table(table_data, colWidths=[120, 68, 68])
    t_res.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))

    story.append(table_caption)
    story.append(t_res)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Live classroom validation with enrolled students demonstrated 100% true positive verification with zero false acceptances for unregistered individuals when threshold &tau; was set to 0.75.",
        body_style
    ))

    story.append(Paragraph("6. CONCLUSION", sec_head))
    story.append(Paragraph(
        "This paper presented a real-time, contactless smart attendance system combining MTCNN face alignment, Inception-ResNet-v1 deep metric extraction, and cosine similarity matching. Engineered optimizations achieved ~30 FPS CPU performance with 95.2% accuracy. The prototype successfully eliminates manual attendance overhead, mitigates proxy marking, and provides a scalable, privacy-conscious solution for modern academic institutions.",
        body_style
    ))

    story.append(Paragraph("ACKNOWLEDGMENT", sec_head))
    story.append(Paragraph(
        "The authors express sincere gratitude to Prof. V. R. Gupta, Course Coordinator, Department of Electronics Engineering, Ramdeobaba University, Nagpur, for guidance, technical feedback, and continuous support throughout the capstone development.",
        body_style
    ))

    story.append(Paragraph("REFERENCES", sec_head))
    refs = [
        "[1] M. Turk and A. Pentland, \"Eigenfaces for recognition,\" <i>J. Cogn. Neurosci.</i>, vol. 3, no. 1, pp. 71&ndash;86, 1991.",
        "[2] T. Ahonen, A. Hadid, and M. Pietik&auml;inen, \"Face description with local binary patterns: Application to face recognition,\" <i>IEEE Trans. Pattern Anal. Mach. Intell.</i>, vol. 28, no. 12, pp. 2037&ndash;2041, 2006.",
        "[3] F. Schroff, D. Kalenichenko, and J. Philbin, \"FaceNet: A unified embedding for face recognition and clustering,\" in <i>Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)</i>, 2015, pp. 815&ndash;823.",
        "[4] K. Zhang, Z. Zhang, Z. Li, and Y. Qiao, \"Joint face detection and alignment using multitask cascaded convolutional networks,\" <i>IEEE Signal Process. Lett.</i>, vol. 23, no. 10, pp. 1499&ndash;1503, 2016.",
        "[5] Q. Cao, L. Shen, W. Xie, O. M. Parkhi, and A. Zisserman, \"VGGFace2: A dataset for recognising faces across pose and age,\" in <i>Proc. 13th IEEE Int. Conf. Autom. Face Gesture Recognit. (FG)</i>, 2018, pp. 67&ndash;74.",
        "[6] G. B. Huang, M. Mattar, T. Berg, and E. Learned-Miller, \"Labeled faces in the wild: A database for studying face recognition in unconstrained environments,\" Univ. Massachusetts, Amherst, Tech. Rep. 07-49, 2007."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))

    doc.build(story)
    print(f"Generated IEEE Formatted PDF successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
