# Set UTF-8 mode FIRST, before any other imports, so all print() calls
# and Streamlit's internal stdout capture work correctly on Windows.
import os
import sys
os.environ["PYTHONUTF8"] = "1"
reconfigure = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure):
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

import json
import glob
import time
import tempfile
import threading
from datetime import datetime, date
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils import (
    load_models,
    detect_faces,
    detect_single_face,
    get_embedding,
    cosine_similarity,
    load_gallery,
    save_gallery,
    load_image_as_pil,
    opencv_frame_to_pil,
    SUPPORTED_EXTENSIONS,
)
from src.attendance import identify, AttendanceLogger, draw_annotation
from src.lfw_experiment import load_threshold

try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
    import av
    HAS_WEBRTC = True
except Exception:
    HAS_WEBRTC = False

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Smart Attendance System | Ramdeobaba University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS - Modern Premium Dashboard Theme
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #4F46E5;
    --primary-light: #EEF2FF;
    --primary-hover: #4338CA;
    --bg-page: #F8FAFC;
    --bg-card: #FFFFFF;
    --text-main: #0F172A;
    --text-muted: #64748B;
    --border-color: #E2E8F0;
    --success: #10B981;
    --danger: #EF4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg-page);
    color: var(--text-main);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #334155;
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #F8FAFC !important;
}

/* Hero Header */
.hero-banner {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 50%, #818CF8 100%);
    padding: 28px 36px;
    border-radius: 16px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.hero-banner h1 {
    color: #FFFFFF !important;
    font-size: 1.85rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-banner p {
    color: #E0E7FF !important;
    font-size: 0.95rem;
    margin: 6px 0 0 0;
    font-weight: 400;
}
.hero-badge {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
    display: inline-block;
}

/* Stat Cards */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.stat-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.06);
}
.stat-card-title {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 6px;
}
.stat-card-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--text-main);
    line-height: 1.2;
}
.stat-card-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* Sidebar mini cards */
.sidebar-metric {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    text-align: center;
}
.sidebar-metric h2 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    color: #FFFFFF !important;
}
.sidebar-metric p {
    font-size: 0.75rem !important;
    color: #94A3B8 !important;
    margin: 2px 0 0 0 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section Container Cards */
.content-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
.content-card h3 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 0;
    color: var(--text-main);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    padding: 4px 0 16px 0;
    border-bottom: 2px solid var(--border-color);
}
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 10px 10px 0 0;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--text-muted);
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--primary);
    background: #F8FAFC;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border-color: var(--primary) !important;
}

/* Primary Action Buttons */
.stButton > button {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.4rem !important;
    font-size: 0.92rem !important;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--primary-hover) !important;
    box-shadow: 0 6px 14px rgba(79, 70, 229, 0.3) !important;
    transform: translateY(-1px);
}

/* Code & pre */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Table styling */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Constants & Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

GALLERY_DIR    = "gallery"
DATA_ENROLLED  = "data/enrolled"
LOG_DIR        = "data/attendance_logs"
LFW_RESULTS    = "gallery/lfw_results.png"

os.makedirs(GALLERY_DIR, exist_ok=True)
os.makedirs(DATA_ENROLLED, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


@st.cache_resource(show_spinner="Loading Deep Learning models (MTCNN + InceptionResnetV1)...")
def cached_load_models():
    return load_models(device="auto")


def gallery_exists() -> bool:
    return (
        os.path.exists(os.path.join(GALLERY_DIR, "embeddings.npy")) and
        os.path.exists(os.path.join(GALLERY_DIR, "labels.json"))
    )


def gallery_info() -> tuple[int, int]:
    """Returns (n_embeddings, n_students)."""
    if not gallery_exists():
        return 0, 0
    embs, labels = load_gallery(GALLERY_DIR)
    return len(labels), len(set(labels))


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar - Academic & System Profile
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 16px 0;">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🏛️</div>
        <div style="font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; color: #FFFFFF;">Ramdeobaba University</div>
        <div style="font-size: 0.78rem; color: #94A3B8;">Dept. of Electronics Engineering</div>
    </div>
    """, unsafe_allow_html=True)

    n_emb, n_students = gallery_info()
    tau = load_threshold(GALLERY_DIR, default=0.70)

    st.markdown(f"""
    <div class="sidebar-metric">
        <h2>{n_students}</h2>
        <p>Enrolled Participants</p>
    </div>
    <div class="sidebar-metric">
        <h2>{n_emb}</h2>
        <p>Face Embeddings (512-D)</p>
    </div>
    <div class="sidebar-metric">
        <h2>{tau:.2f}</h2>
        <p>Similarity Threshold (τ)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.85rem; line-height: 1.6;">
        <div style="font-weight: 600; color: #F1F5F9; margin-bottom: 6px; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;">Project Team</div>
        <div>👤 <b>Khizra Bushra Raien</b> (Roll: 32)</div>
        <div>👤 <b>Meet Ashish Bajoria</b> (Roll: 36)</div>
        <div>👤 <b>Mohammad Moinuddin</b> (Roll: 38)</div>
        <div>👤 <b>Pratham Singh Thakur</b> (Roll: 44)</div>
        <div style="margin-top: 12px; font-weight: 600; color: #F1F5F9; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;">Course Coordinator</div>
        <div>👨‍🏫 <b>Prof. V. R. Gupta</b></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Top Hero Banner
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
    <div>
        <div class="hero-badge">Deep Learning Lab • Capstone Project • Semester V</div>
        <h1 style="margin-top: 10px;">Smart Face Recognition Attendance System</h1>
        <p>Real-time edge-ready attendance logging powered by MTCNN alignment and InceptionResnetV1 metric learning.</p>
    </div>
    <div style="display: flex; gap: 12px;">
        <div style="text-align: right; background: rgba(0,0,0,0.15); padding: 12px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #E0E7FF;">Backend Engine</div>
            <div style="font-size: 1.1rem; font-weight: 700;">PyTorch + FaceNet</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Organized Main Navigation Tabs
# ─────────────────────────────────────────────────────────────────────────────

tab_live, tab_reports, tab_enroll, tab_lfw, tab_proposal = st.tabs([
    "📹 Live Attendance",
    "📊 Attendance Reports",
    "👥 Participant Enrollment",
    "🧪 Model Benchmark (LFW)",
    "📑 Project Proposal & Architecture"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE ATTENDANCE (PRIMARY WORKFLOW)
# ══════════════════════════════════════════════════════════════════════════════

with tab_live:
    if not gallery_exists():
        st.warning("⚠️ **No participants enrolled yet.** Please enroll volunteers in the **'Participant Enrollment'** tab first.")
    else:
        col_ctrl, col_feed = st.columns([1, 2], gap="large")

        with col_ctrl:
            st.markdown("""
            <div class="content-card">
                <h3>Live Session Controls</h3>
                <p style="font-size: 0.85rem; color: #64748B;">Live camera attendance feed.</p>
            """, unsafe_allow_html=True)

            tau_live = st.slider(
                "Cosine Similarity Threshold (τ)",
                min_value=0.30, max_value=0.99,
                value=0.60,
                step=0.01,
                help="Faces with similarity >= τ are identified; otherwise marked as Unknown."
            )

            frame_skip = st.slider("Process Every Nth Frame", min_value=1, max_value=8, value=3,
                                   help="Optimizes inference speed on CPU.")

            st.markdown("---")
            if "live_running" not in st.session_state:
                st.session_state.live_running = False

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                start_clicked = st.button("▶ Start Session", disabled=st.session_state.live_running)
            with c_btn2:
                stop_clicked = st.button("⏹ Save Attendance", disabled=not st.session_state.live_running)

            if start_clicked:
                st.session_state.live_running = True
                st.rerun()

            if stop_clicked:
                st.session_state.live_running = False
                st.rerun()

            if "last_saved_file" in st.session_state and st.session_state.last_saved_file:
                st.success(f"Session saved: `{os.path.basename(st.session_state.last_saved_file)}`")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_feed:
            st.markdown("""
            <div class="content-card">
                <h3>Live Camera Feed</h3>
            """, unsafe_allow_html=True)

            frame_placeholder = st.empty()

            if st.session_state.get("live_running", False):
                mtcnn, resnet = cached_load_models()
                gallery_embs, gallery_labels = load_gallery(GALLERY_DIR)
                logger = AttendanceLogger(LOG_DIR, gallery_labels)

                # Prioritize Windows DirectShow for primary hardware camera
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(0)

                if not cap.isOpened():
                    st.error(
                        "❌ Could not open webcam at index 0.\n\n"
                        "Live continuous OpenCV video streaming requires running locally on your laptop with the physical webcam directly attached.\n"
                        "Please run `run_app.bat` on your computer to run the live stream."
                    )
                    st.session_state.live_running = False
                else:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                    frame_count = 0
                    last_boxes = []
                    last_identities = []

                    while st.session_state.live_running:
                        ret, frame = cap.read()
                        if not ret:
                            st.error("Webcam feed lost.")
                            break

                        frame_count += 1

                        if frame_count % frame_skip == 0:
                            h, w = frame.shape[:2]
                            scale = 0.5
                            small_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
                            pil_small = opencv_frame_to_pil(small_frame)

                            face_tensors, boxes = detect_faces(pil_small, mtcnn)

                            last_boxes = []
                            last_identities = []
                            if face_tensors is not None and boxes is not None:
                                for face_tensor, sbox in zip(face_tensors, boxes):
                                    orig_box = [coord / scale for coord in sbox]
                                    embedding = get_embedding(face_tensor, resnet)
                                    name, sim = identify(embedding, gallery_embs, gallery_labels, tau_live)
                                    recognised = name != "Unknown"
                                    if recognised:
                                        is_new = logger.mark_present(name)
                                        if is_new:
                                            logger.save()
                                    last_boxes.append(orig_box)
                                    last_identities.append((name, sim, recognised))

                        for box, (name, sim, recognised) in zip(last_boxes, last_identities):
                            draw_annotation(frame, box, name, sim, recognised)

                        cv2.rectangle(frame, (0, 0), (420, 40), (240, 240, 240), -1)
                        cv2.putText(frame, f"Threshold = {tau_live:.2f} | {logger.summary()}", 
                                    (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (20, 20, 20), 1)

                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(frame_rgb, channels="RGB")

                    cap.release()
                    filepath = logger.save()
                    st.session_state.last_saved_file = filepath
            else:
                st.info("Click **'▶ Start Session'** on the left to start the continuous live camera stream.")

            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ATTENDANCE REPORTS
# ══════════════════════════════════════════════════════════════════════════════

with tab_reports:
    log_files = sorted(glob.glob(os.path.join(LOG_DIR, "attendance_*.csv")), reverse=True)

    if not log_files:
        st.info("No attendance sessions saved yet. Start a session in the 'Live Attendance' tab to record logs.")
    else:
        st.markdown("""
        <div class="content-card">
            <h3>Attendance Log History</h3>
        """, unsafe_allow_html=True)

        col_select, col_actions = st.columns([2, 1])
        with col_select:
            selected = st.selectbox(
                "Choose Session Log",
                options=log_files,
                format_func=lambda p: os.path.basename(p),
            )

        if selected:
            df = pd.read_csv(selected)
            n_present = (df["Status"] == "Present").sum()
            n_absent  = (df["Status"] == "Absent").sum()
            total     = len(df)
            pct       = (n_present / total * 100) if total > 0 else 0

            # Metrics row
            st.markdown(f"""
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-card-title">Total Enrolled</div>
                    <div class="stat-card-value">{total}</div>
                    <div class="stat-card-subtitle">Students registered for session</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">Present</div>
                    <div class="stat-card-value" style="color: var(--success);">{n_present}</div>
                    <div class="stat-card-subtitle">{pct:.1f}% Attendance Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">Absent</div>
                    <div class="stat-card-value" style="color: var(--danger);">{n_absent}</div>
                    <div class="stat-card-subtitle">{100 - pct:.1f}% Absence Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with col_actions:
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export Session CSV",
                    data=csv_bytes,
                    file_name=os.path.basename(selected),
                    mime="text/csv",
                )

            st.dataframe(df, width="stretch", hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PARTICIPANT ENROLLMENT
# ══════════════════════════════════════════════════════════════════════════════

with tab_enroll:
    col_en_left, col_en_right = st.columns([1, 1], gap="large")

    with col_en_left:
        st.markdown("""
        <div class="content-card">
            <h3>Enroll New Volunteer</h3>
            <p style="font-size: 0.85rem; color: #64748B;">Upload portrait photos under varied lighting and angles. Faces are aligned via MTCNN and converted into 512-d normalized embeddings.</p>
        """, unsafe_allow_html=True)

        student_name = st.text_input(
            "Volunteer Full Name",
            placeholder="e.g. Meet Bajoria",
            key="enroll_name",
        )
        uploaded_files = st.file_uploader(
            "Upload Face Images",
            type=["jpg", "jpeg", "png", "bmp"],
            accept_multiple_files=True,
            key="enroll_photos",
        )

        if st.button("➕ Register & Extract Embeddings", key="btn_enroll"):
            if not student_name.strip():
                st.error("Please enter a participant name.")
            elif not uploaded_files:
                st.error("Please provide at least one photo.")
            else:
                mtcnn, resnet = cached_load_models()
                formatted_name = student_name.strip().replace(" ", "_")
                student_dir = os.path.join(DATA_ENROLLED, formatted_name)
                os.makedirs(student_dir, exist_ok=True)

                new_embeddings = []
                new_labels     = []
                failed         = []

                progress = st.progress(0)
                for i, uf in enumerate(uploaded_files):
                    img = Image.open(uf).convert("RGB")
                    face_tensor = detect_single_face(img, mtcnn)

                    if face_tensor is None:
                        failed.append(uf.name)
                    else:
                        emb = get_embedding(face_tensor, resnet)
                        new_embeddings.append(emb)
                        new_labels.append(formatted_name)
                        img.save(os.path.join(student_dir, uf.name))

                    progress.progress((i + 1) / len(uploaded_files))

                if new_embeddings:
                    new_emb_arr = np.stack(new_embeddings)
                    if gallery_exists():
                        old_embs, old_labels = load_gallery(GALLERY_DIR)
                        merged_embs   = np.vstack([old_embs, new_emb_arr])
                        merged_labels = old_labels + new_labels
                    else:
                        merged_embs   = new_emb_arr
                        merged_labels = new_labels

                    save_gallery(merged_embs, merged_labels, GALLERY_DIR)
                    st.success(f"Successfully registered **{student_name}** with {len(new_embeddings)} embedding(s)!")
                    st.rerun()

                if failed:
                    st.warning(f"Face not detected in {len(failed)} image(s): {', '.join(failed)}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_en_right:
        st.markdown("""
        <div class="content-card">
            <h3>Enrolled Gallery Roster</h3>
        """, unsafe_allow_html=True)

        if gallery_exists():
            _, labels = load_gallery(GALLERY_DIR)
            unique_students = sorted(set(labels))
            counts = {s: labels.count(s) for s in unique_students}
            df = pd.DataFrame([
                {"Participant Name": s.replace("_", " "), "Total Embeddings": c}
                for s, c in counts.items()
            ])
            st.dataframe(df, width="stretch", hide_index=True)

            if st.button("🗑️ Reset Enrolled Gallery", key="btn_clear_gallery"):
                for f in ["embeddings.npy", "labels.json"]:
                    fp = os.path.join(GALLERY_DIR, f)
                    if os.path.exists(fp):
                        os.remove(fp)
                st.success("Gallery cleared.")
                st.rerun()
        else:
            st.info("Gallery is currently empty. Use the form on the left to add your first volunteer.")

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — LFW BENCHMARK & EXPERIMENTAL VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

with tab_lfw:
    st.markdown("""
    <div class="content-card">
        <h3>Labeled Faces in the Wild (LFW) Verification Benchmark</h3>
        <p style="font-size: 0.9rem; color: #64748B;">
            LFW tests 6,000 face pairs (3,000 matched, 3,000 mismatched) to evaluate model generalizability, 
            ROC curves, AUC, and determine the optimal cosine similarity threshold τ (minimizing False Accept and False Reject rates).
        </p>
    """, unsafe_allow_html=True)

    lfw_dir   = "data/lfw"
    pairs_txt = "data/lfw/pairs.txt"
    lfw_ready = os.path.isdir(lfw_dir) and os.path.exists(pairs_txt)

    if not lfw_ready:
        st.info("LFW dataset folder or `pairs.txt` is not currently present in `data/lfw/`. Using optimal pre-validated threshold τ = 0.70.")
    else:
        if st.button("🚀 Execute LFW Verification Run", key="btn_run_lfw"):
            from src.lfw_experiment import run_experiment
            with st.spinner("Processing LFW pairs..."):
                run_experiment(lfw_dir=lfw_dir, pairs_file=pairs_txt, output_dir=GALLERY_DIR)
            st.success("Evaluation complete!")
            st.rerun()

    if os.path.exists(LFW_RESULTS):
        st.image(LFW_RESULTS, caption="ROC Curve & Cosine Similarity Distribution", width="stretch")
        tau_val = load_threshold(GALLERY_DIR, default=0.70)
        st.metric("Validated Optimal Threshold", f"{tau_val:.4f}")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROJECT PROPOSAL & ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════

with tab_proposal:
    st.markdown("""
    <div class="content-card">
        <h3>1. Problem Statement and Motivation</h3>
        <p>
            Marking attendance manually is slow, repetitive, and often unreliable. In classrooms and labs, it can even 
            lead to proxy attendance. Our project aims to solve this by building a smart attendance prototype 
            powered by face recognition. The system detects faces, generates deep learning based embeddings, 
            and matches them against a small database of volunteers who have given consent. If a face doesn’t match, 
            it is marked as <b>Unknown</b>. This prototype demonstrates how AI makes attendance seamless, 
            accurate, and secure in controlled environments, while keeping privacy at the forefront.
        </p>
    </div>

    <div class="content-card">
        <h3>2. Project Objectives</h3>
        <ol style="line-height: 1.8; color: #334155;">
            <li><b>Real-time Detection:</b> Build a real-time system that detects faces from a live camera feed.</li>
            <li><b>Embedding Extraction:</b> Extract normalized face embeddings using a pretrained Deep Learning model (InceptionResnetV1 / VGGFace2).</li>
            <li><b>Automated Logging:</b> Automatically log attendance with participant name, date, and exact timestamp.</li>
            <li><b>Threshold Recognition:</b> Recognize enrolled participants using cosine similarity while rejecting unknown faces below threshold τ.</li>
        </ol>
    </div>

    <div class="content-card">
        <h3>3. Dataset & Preprocessing</h3>
        <ul style="line-height: 1.8; color: #334155;">
            <li><b>Labeled Faces in the Wild (LFW):</b> Over 13,000 labeled images used for threshold validation and ROC analysis.</li>
            <li><b>Consent-Based Local Dataset:</b> Multiple photos per enrolled volunteer captured under different poses and lighting conditions.</li>
            <li><b>Preprocessing:</b> 5-point facial landmark alignment, margin padding, and normalization to [-1, 1] range.</li>
        </ul>
    </div>

    <div class="content-card">
        <h3>4. Proposed Pipeline Architecture</h3>
        <div style="background: #F1F5F9; border-radius: 10px; padding: 18px; font-family: monospace; font-size: 0.9rem; margin-top: 10px;">
            Webcam Input ──▶ MTCNN Alignment ──▶ InceptionResnetV1 (512-D) ──▶ Cosine Similarity vs Gallery ──▶ CSV Attendance Log
        </div>
    </div>
    """, unsafe_allow_html=True)
