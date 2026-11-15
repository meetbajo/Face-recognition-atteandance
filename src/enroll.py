"""
enroll.py — Build the student face gallery from labeled enrollment photos
=========================================================================

WHAT THIS SCRIPT DOES (beginner explanation)
--------------------------------------------
Imagine you have a folder called "enrolled/" with one sub-folder per student:

    enrolled/
        Alice_Smith/
            photo1.jpg
            photo2.jpg
        Bob_Jones/
            photo1.jpg

This script:
  1. Loops over every student folder
  2. For each photo, detects the face and extracts its 512-d embedding
  3. Stores every embedding together with the student's name
  4. Saves the result to disk as:
       gallery/embeddings.npy  (shape: N_photos × 512)
       gallery/labels.json     (length: N_photos)

WHY MULTIPLE PHOTOS PER STUDENT?
---------------------------------
One photo might capture Alice with glasses. Another without. Another from a
slightly different angle. By storing all of them, the system becomes more
robust — if the webcam sees Alice from a new angle, at least ONE of her
enrolled embeddings will be close enough in vector space.

USAGE
-----
    python src/enroll.py --data_dir data/enrolled --gallery_dir gallery

    # Preview only (don't overwrite existing gallery):
    python src/enroll.py --data_dir data/enrolled --gallery_dir gallery --dry_run
"""

import os
import sys
import argparse

import numpy as np
from tqdm import tqdm

# Make sure src/ is importable when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force UTF-8 output on Windows (avoids UnicodeEncodeError with emoji/arrows)
reconfigure = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure) and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

from src.utils import (
    load_models,
    detect_single_face,
    get_embedding,
    save_gallery,
    load_image_as_pil,
    SUPPORTED_EXTENSIONS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Main Enrollment Logic
# ─────────────────────────────────────────────────────────────────────────────

def enroll_students(data_dir: str, gallery_dir: str, dry_run: bool = False) -> None:
    """
    Scan `data_dir` for student sub-folders, extract face embeddings from each
    photo, and save the gallery to `gallery_dir`.

    Parameters
    ----------
    data_dir    : path to enrolled/ folder (each sub-dir = one student)
    gallery_dir : path where embeddings.npy and labels.json will be saved
    dry_run     : if True, print what would be done without saving
    """
    # ── Step 1: Load models ────────────────────────────────────────────────
    print("\n[enroll] Loading face detection and embedding models...")
    mtcnn, resnet = load_models(device="auto")

    # ── Step 2: Discover student folders ──────────────────────────────────
    if not os.path.isdir(data_dir):
        print(f"[enroll] ERROR: data_dir '{data_dir}' does not exist.")
        print("  Create it and add one sub-folder per student with their photos.")
        sys.exit(1)

    student_folders = [
        d for d in sorted(os.listdir(data_dir))
        if os.path.isdir(os.path.join(data_dir, d))
    ]

    if not student_folders:
        print(f"[enroll] No student folders found in '{data_dir}'.")
        print("  Expected structure: data/enrolled/<StudentName>/<photo.jpg>")
        sys.exit(1)

    print(f"[enroll] Found {len(student_folders)} student(s): {student_folders}\n")

    # ── Step 3: Extract embeddings ─────────────────────────────────────────
    all_embeddings = []
    all_labels     = []
    skipped_photos = []

    for student_name in student_folders:
        student_dir = os.path.join(data_dir, student_name)
        photo_files = [
            f for f in sorted(os.listdir(student_dir))
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        ]

        if not photo_files:
            print(f"  [WARN] No images found for '{student_name}', skipping.")
            continue

        student_embeddings = []

        for photo_file in tqdm(photo_files, desc=f"  Enrolling {student_name}", unit="photo"):
            photo_path = os.path.join(student_dir, photo_file)
            img = load_image_as_pil(photo_path)
            if img is None:
                skipped_photos.append(photo_path)
                continue

            # Detect and align the face
            face_tensor = detect_single_face(img, mtcnn)

            if face_tensor is None:
                print(f"\n    [WARN] No face detected in '{photo_file}', skipping.")
                skipped_photos.append(photo_path)
                continue

            # Extract 512-d embedding
            embedding = get_embedding(face_tensor, resnet)  # shape (512,)
            student_embeddings.append(embedding)
            all_embeddings.append(embedding)
            all_labels.append(student_name)

        n = len(student_embeddings)
        print(f"  [OK] {student_name}: {n} embedding(s) extracted")

        if n == 0:
            print(f"  [WARN] No valid faces for '{student_name}'. "
                  "They will NOT be recognised.")

    # ── Step 4: Summary ────────────────────────────────────────────────────
    print(f"\n[enroll] Summary:")
    print(f"  Total embeddings : {len(all_embeddings)}")
    print(f"  Total students   : {len(set(all_labels))}")
    print(f"  Skipped photos   : {len(skipped_photos)}")

    if skipped_photos:
        print("\n  Skipped files:")
        for f in skipped_photos:
            print(f"    - {f}")

    if not all_embeddings:
        print("[enroll] No embeddings were extracted. Gallery not saved.")
        return

    # ── Step 5: Save gallery ───────────────────────────────────────────────
    embeddings_array = np.stack(all_embeddings, axis=0)  # (N, 512)

    if dry_run:
        print(f"\n[enroll] DRY RUN — would save gallery with shape {embeddings_array.shape}")
    else:
        save_gallery(embeddings_array, all_labels, gallery_dir)
        print(f"\n[enroll] Gallery saved to '{gallery_dir}/'")


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enroll students by building a face embedding gallery.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/enroll.py
  python src/enroll.py --data_dir data/enrolled --gallery_dir gallery
  python src/enroll.py --dry_run
        """,
    )
    parser.add_argument(
        "--data_dir",
        default="data/enrolled",
        help="Path to enrollment photos folder (one sub-dir per student)",
    )
    parser.add_argument(
        "--gallery_dir",
        default="gallery",
        help="Where to save embeddings.npy and labels.json",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Preview what would be enrolled without saving",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    enroll_students(
        data_dir=args.data_dir,
        gallery_dir=args.gallery_dir,
        dry_run=args.dry_run,
    )
