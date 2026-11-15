"""
attendance.py - Real-Time Face Recognition Attendance via Webcam
================================================================

WHAT THIS SCRIPT DOES (beginner explanation)
--------------------------------------------
This is the main production part of the system. It:
  1. Opens your webcam
  2. Every frame: detects all faces, embeds each, compares to enrolled gallery
  3. Draws a coloured box around each face with the person's name and similarity
  4. Marks a student Present the FIRST time they are confidently recognised
  5. When you press Q, saves a CSV attendance sheet

THE MATCHING ALGORITHM (simple version)
----------------------------------------
For each face detected in the current frame:

    query_embedding = embed(face)
    similarities = cosine_similarity(query_embedding, gallery_embeddings)
    best_similarity = max(similarities)
    best_name = labels[argmax(similarities)]

    if best_similarity > threshold:
        -> recognised as best_name
    else:
        -> labelled Unknown

THRESHOLD CHOICE
----------------
Default tau = 0.70 (a good starting point).
If you ran lfw_experiment.py, the validated tau is read automatically from
gallery/threshold.json.

USAGE
-----
    python src/attendance.py
    python src/attendance.py --gallery_dir gallery --threshold 0.72
    python src/attendance.py --source data/test_images
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime, date

import cv2
import numpy as np
from PIL import Image

# Force UTF-8 output on Windows (avoids UnicodeEncodeError with arrows/emoji)
reconfigure = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure) and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    load_models,
    detect_faces,
    get_embedding,
    cosine_similarity,
    load_gallery,
    opencv_frame_to_pil,
)
from src.lfw_experiment import load_threshold


# ─────────────────────────────────────────────────────────────────────────────
# Colour palette for bounding boxes
# ─────────────────────────────────────────────────────────────────────────────
COLOR_RECOGNISED = (80, 220, 100)   # green  (BGR)
COLOR_UNKNOWN    = (50,  50, 220)   # red
COLOR_TEXT_BG    = (30,  30,  30)   # dark grey label background


# ─────────────────────────────────────────────────────────────────────────────
# 1. Identify a Single Face Against the Gallery
# ─────────────────────────────────────────────────────────────────────────────

def identify(
    face_embedding: np.ndarray,
    gallery_embeddings: np.ndarray,
    gallery_labels: list[str],
    threshold: float,
) -> tuple[str, float]:
    """
    Compare a query embedding against the gallery and return (name, similarity).

    Strategy: find the gallery entry with the HIGHEST cosine similarity.
              If that similarity < threshold, return ("Unknown", similarity).

    Parameters
    ----------
    face_embedding    : (512,) query vector (L2 normalised)
    gallery_embeddings: (N, 512) enrolled embeddings
    gallery_labels    : list of N student names
    threshold         : float, recognition threshold τ

    Returns
    -------
    name       : recognised student name, or "Unknown"
    best_sim   : cosine similarity to the best gallery match
    """
    sims     = cosine_similarity(face_embedding, gallery_embeddings)  # (N,)
    best_idx = int(np.argmax(sims))
    best_sim = float(sims[best_idx])
    name     = gallery_labels[best_idx] if best_sim >= threshold else "Unknown"
    return name, best_sim


# ─────────────────────────────────────────────────────────────────────────────
# 2. Draw Overlay on OpenCV Frame
# ─────────────────────────────────────────────────────────────────────────────

def draw_annotation(
    frame: np.ndarray,
    box: list,
    name: str,
    similarity: float,
    recognised: bool,
) -> None:
    """
    Draw bounding box + name + similarity score on an OpenCV frame (in-place).

    Parameters
    ----------
    frame      : OpenCV BGR frame (modified in place)
    box        : [x1, y1, x2, y2] bounding box
    name       : "Alice_Smith" or "Unknown"
    similarity : cosine similarity (displayed as %)
    recognised : True → green box; False → red box
    """
    x1, y1, x2, y2 = [int(v) for v in box]
    color = COLOR_RECOGNISED if recognised else COLOR_UNKNOWN

    # Bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Label text
    display_name = name.replace("_", " ")
    label = f"{display_name}  {similarity * 100:.1f}%"

    font       = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    thickness  = 1
    (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)

    # Dark background rectangle behind text for readability
    cv2.rectangle(frame, (x1, y1 - th - baseline - 6), (x1 + tw + 6, y1), COLOR_TEXT_BG, -1)
    cv2.putText(frame, label, (x1 + 3, y1 - baseline - 2), font, font_scale, color, thickness)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Attendance Logger
# ─────────────────────────────────────────────────────────────────────────────

class AttendanceLogger:
    """
    Tracks who has been marked present during a session and saves to CSV.

    Deduplication: each student is marked present only once per session,
    no matter how many times they appear in the video feed.
    """

    def __init__(self, log_dir: str, all_enrolled: list[str]) -> None:
        self.log_dir     = log_dir
        self.session_date = date.today().isoformat()
        self.session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.records: dict[str, dict] = {}

        # Pre-populate all enrolled students as Absent
        for name in set(all_enrolled):
            self.records[name] = {
                "Name":   name.replace("_", " "),
                "Date":   self.session_date,
                "Time":   "--",
                "Status": "Absent",
            }

        os.makedirs(log_dir, exist_ok=True)

    def mark_present(self, name: str) -> bool:
        """
        Mark a student as Present. Returns True if this is a new marking.
        """
        if name == "Unknown" or name not in self.records:
            return False
        if self.records[name]["Status"] == "Present":
            return False  # already marked, don't duplicate

        self.records[name]["Status"] = "Present"
        self.records[name]["Time"]   = datetime.now().strftime("%H:%M:%S")
        print(f"  [PRESENT] {name.replace('_', ' ')} at {self.records[name]['Time']}")
        return True

    def save(self) -> str:
        """Save attendance to a CSV file. Returns the file path."""
        filename = f"attendance_{self.session_timestamp}.csv"
        filepath = os.path.join(self.log_dir, filename)

        fieldnames = ["Name", "Date", "Time", "Status"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in sorted(self.records.values(), key=lambda r: r["Name"]):
                writer.writerow(record)

        # Also maintain latest date-based file for compatibility
        daily_filepath = os.path.join(self.log_dir, f"attendance_{self.session_date}.csv")
        try:
            with open(daily_filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for record in sorted(self.records.values(), key=lambda r: r["Name"]):
                    writer.writerow(record)
        except Exception:
            pass

        print(f"\n[attendance] Attendance saved -> {filepath}")
        return filepath

    def summary(self) -> str:
        total   = len(self.records)
        present = sum(1 for r in self.records.values() if r["Status"] == "Present")
        absent  = total - present
        return f"Present: {present}/{total}  |  Absent: {absent}"


# ─────────────────────────────────────────────────────────────────────────────
# 4. Webcam Attendance Loop
# ─────────────────────────────────────────────────────────────────────────────

def run_webcam_attendance(
    gallery_dir: str,
    threshold: float,
    log_dir: str,
    camera_index: int = 0,
) -> str:
    """
    Open webcam, run face recognition in real-time, save attendance CSV on quit.

    Controls
    --------
    Q or ESC → quit and save attendance CSV.
    S        → manually save attendance mid-session.
    """
    # Load models and gallery
    print("[attendance] Loading models...")
    mtcnn, resnet = load_models(device="auto")

    print("[attendance] Loading gallery...")
    gallery_embeddings, gallery_labels = load_gallery(gallery_dir)

    logger = AttendanceLogger(log_dir, gallery_labels)

    # Open webcam with DirectShow for lower latency on Windows
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open webcam at index {camera_index}. "
            "Try --camera 1 if you have an external webcam."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # Window settings
    cv2.namedWindow("Face Attendance", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Attendance", 960, 600)

    print("\n[attendance] Webcam live. Press Q or ESC to quit and save attendance.\n")

    frame_count = 0
    PROCESS_EVERY_N_FRAMES = 3  # process every 3rd frame for responsive real-time speed
    last_boxes = []
    last_identities = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[attendance] Lost webcam feed.")
            break

        frame_count += 1

        # ── Process faces every N frames ───────────────────────────────────
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            h, w = frame.shape[:2]
            scale = 0.5
            small_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
            pil_img = opencv_frame_to_pil(small_frame)
            face_tensors, boxes = detect_faces(pil_img, mtcnn)

            last_boxes = []
            last_identities = []
            if face_tensors is not None and boxes is not None:
                for i, (face_tensor, sbox) in enumerate(zip(face_tensors, boxes)):
                    orig_box = [coord / scale for coord in sbox]
                    # Embed this face
                    embedding = get_embedding(face_tensor, resnet)

                    # Identify against gallery
                    name, sim = identify(
                        embedding, gallery_embeddings, gallery_labels, threshold
                    )

                    recognised = name != "Unknown"

                    # Mark attendance
                    if recognised:
                        logger.mark_present(name)

                    last_boxes.append(orig_box)
                    last_identities.append((name, sim, recognised))

        # Draw cached or latest annotations smoothly
        for box, (name, sim, recognised) in zip(last_boxes, last_identities):
            draw_annotation(frame, box, name, sim, recognised)

        # ── HUD overlay (top-left info panel) ──────────────────────────────
        cv2.rectangle(frame, (0, 0), (360, 60), (20, 20, 20), -1)
        cv2.putText(frame, f"τ = {threshold:.2f}  |  {logger.summary()}",
                    (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, "Q/ESC: quit & save   S: save now",
                    (10, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

        cv2.imshow("Face Attendance", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), ord("Q"), 27):  # Q or ESC
            break
        elif key in (ord("s"), ord("S")):
            logger.save()

    cap.release()
    cv2.destroyAllWindows()

    filepath = logger.save()
    print(f"\n[attendance] Session ended. {logger.summary()}")
    return filepath


# ─────────────────────────────────────────────────────────────────────────────
# 5. Image-Folder Attendance Mode (for testing without webcam)
# ─────────────────────────────────────────────────────────────────────────────

def run_image_folder_attendance(
    image_dir: str,
    gallery_dir: str,
    threshold: float,
    log_dir: str,
) -> str:
    """
    Run attendance recognition on a folder of images instead of live webcam.
    Useful for testing and for hardware-less demo runs.
    """
    from src.utils import load_image_as_pil, SUPPORTED_EXTENSIONS

    print("[attendance] Loading models...")
    mtcnn, resnet = load_models(device="auto")

    print("[attendance] Loading gallery...")
    gallery_embeddings, gallery_labels = load_gallery(gallery_dir)

    logger = AttendanceLogger(log_dir, gallery_labels)

    image_files = [
        f for f in sorted(os.listdir(image_dir))
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    print(f"\n[attendance] Processing {len(image_files)} images from '{image_dir}'\n")

    for filename in image_files:
        path    = os.path.join(image_dir, filename)
        pil_img = load_image_as_pil(path)
        if pil_img is None:
            continue

        face_tensors, boxes = detect_faces(pil_img, mtcnn)

        print(f"  {filename}:")
        if face_tensors is None:
            print("    -> no faces detected")
            continue

        for face_tensor, box in zip(face_tensors, boxes):
            embedding = get_embedding(face_tensor, resnet)
            name, sim = identify(embedding, gallery_embeddings, gallery_labels, threshold)
            print(f"    -> {name}  (similarity: {sim:.3f})")
            logger.mark_present(name)

    return logger.save()


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time face recognition attendance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/attendance.py                          # webcam, default settings
  python src/attendance.py --threshold 0.72         # custom threshold
  python src/attendance.py --source data/test       # image folder mode
  python src/attendance.py --camera 1               # external webcam
        """,
    )
    parser.add_argument("--gallery_dir", default="gallery",
                        help="Path to gallery/ folder (embeddings.npy + labels.json)")
    parser.add_argument("--threshold", type=float, default=None,
                        help="Recognition threshold τ (default: from gallery/threshold.json or 0.70)")
    parser.add_argument("--log_dir", default="data/attendance_logs",
                        help="Where to save attendance CSV files")
    parser.add_argument("--source", default=None,
                        help="Image folder for offline mode (no webcam). If omitted, uses webcam.")
    parser.add_argument("--camera", type=int, default=0,
                        help="Webcam device index (0 = built-in, 1 = external)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Load threshold: CLI arg → saved JSON → default 0.70
    tau = args.threshold
    if tau is None:
        tau = load_threshold(args.gallery_dir, default=0.70)
    print(f"[attendance] Using recognition threshold τ = {tau:.4f}")

    if args.source:
        run_image_folder_attendance(
            image_dir=args.source,
            gallery_dir=args.gallery_dir,
            threshold=tau,
            log_dir=args.log_dir,
        )
    else:
        run_webcam_attendance(
            gallery_dir=args.gallery_dir,
            threshold=tau,
            log_dir=args.log_dir,
            camera_index=args.camera,
        )
