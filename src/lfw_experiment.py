"""
lfw_experiment.py — Validate the embedding model on Labeled Faces in the Wild
==============================================================================

WHAT IS LFW? (beginner explanation)
------------------------------------
"Labeled Faces in the Wild" is a standard academic benchmark dataset.
It contains 13,233 face images of 5,749 celebrities, collected from the web.

For face *verification* experiments, LFW provides 6,000 pre-defined pairs:
  • 3,000 "same person" pairs  → the two photos show the same celebrity
  • 3,000 "different person" pairs → two different celebrities

Your job: decide, for each pair, whether the two photos show the same person.
You do this by computing the cosine similarity of their embeddings and comparing
to a threshold τ.

WHY RUN LFW EXPERIMENTS?
--------------------------
Before trusting our system with real student attendance, we want to know:
  "How accurate is the InceptionResnetV1 model at telling people apart?"
LFW gives us a standard, reproducible answer.

HOW TO DOWNLOAD LFW
--------------------
1. Download: http://vis-www.cs.umass.edu/lfw/lfw.tgz       (~177 MB)
2. Download: http://vis-www.cs.umass.edu/lfw/pairs.txt
3. Extract lfw.tgz → should create a folder called "lfw/" with sub-folders
   named by person (e.g. lfw/George_W_Bush/George_W_Bush_0001.jpg)
4. Place the lfw/ folder inside data/ and pairs.txt inside data/lfw/

USAGE
-----
    python src/lfw_experiment.py
    python src/lfw_experiment.py --lfw_dir data/lfw --pairs data/lfw/pairs.txt
"""

import os
import sys
import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend (works without a display)
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.metrics import roc_curve, auc

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
    detect_single_face,
    get_embedding,
    cosine_similarity,
    load_image_as_pil,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Parse the LFW pairs.txt File
# ─────────────────────────────────────────────────────────────────────────────

def parse_lfw_pairs(pairs_file: str, lfw_dir: str) -> list[dict]:
    """
    Read the official LFW pairs.txt and return a list of pair records.

    pairs.txt format (skip the first header line):
      • Matched (same) pair:    <name> <img1_num> <img2_num>
      • Mismatched pair:        <name1> <img1_num> <name2> <img2_num>

    Returns
    -------
    pairs : list of dicts, each with keys:
        path1   : absolute path to image 1
        path2   : absolute path to image 2
        label   : 1 (same person) or 0 (different person)
    """
    def img_path(name: str, num: int) -> str:
        filename = f"{name}_{num:04d}.jpg"
        return os.path.join(lfw_dir, name, filename)

    pairs = []

    with open(pairs_file, "r") as f:
        lines = f.read().strip().split("\n")

    # First line: "<n_pairs_same>\t<n_pairs_diff>"  or just a count
    # Skip header
    header = lines[0].split()
    data_lines = lines[1:]

    for line in data_lines:
        parts = line.strip().split()
        if not parts:
            continue

        if len(parts) == 3:
            # Same-person pair: name  img1_num  img2_num
            name, n1, n2 = parts[0], int(parts[1]), int(parts[2])
            pairs.append({
                "path1": img_path(name, n1),
                "path2": img_path(name, n2),
                "label": 1,
            })
        elif len(parts) == 4:
            # Different-person pair: name1  img1_num  name2  img2_num
            name1, n1, name2, n2 = parts[0], int(parts[1]), parts[2], int(parts[3])
            pairs.append({
                "path1": img_path(name1, n1),
                "path2": img_path(name2, n2),
                "label": 0,
            })

    return pairs


# ─────────────────────────────────────────────────────────────────────────────
# 2. Compute Similarities for All Pairs
# ─────────────────────────────────────────────────────────────────────────────

def compute_pair_similarities(
    pairs: list[dict], mtcnn, resnet
) -> tuple[np.ndarray, np.ndarray]:
    """
    For each pair, embed both images and compute cosine similarity.

    Returns
    -------
    similarities : np.ndarray, shape (N,) — cosine similarity for each pair
    labels       : np.ndarray, shape (N,) — 1=same, 0=different
    """
    similarities = []
    labels       = []
    skipped      = 0

    for pair in tqdm(pairs, desc="Computing similarities", unit="pair"):
        img1 = load_image_as_pil(pair["path1"])
        img2 = load_image_as_pil(pair["path2"])

        if img1 is None or img2 is None:
            skipped += 1
            continue

        face1 = detect_single_face(img1, mtcnn)
        face2 = detect_single_face(img2, mtcnn)

        if face1 is None or face2 is None:
            skipped += 1
            continue

        emb1 = get_embedding(face1, resnet)  # (512,)
        emb2 = get_embedding(face2, resnet)  # (512,)

        sim = cosine_similarity(emb1, emb2)  # scalar in [-1, 1]
        similarities.append(sim)
        labels.append(pair["label"])

    print(f"\n[lfw] Processed {len(similarities)} pairs, skipped {skipped}")
    return np.array(similarities), np.array(labels)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Find Best Threshold (minimise classification error)
# ─────────────────────────────────────────────────────────────────────────────

def find_best_threshold(
    similarities: np.ndarray, labels: np.ndarray
) -> tuple[float, float]:
    """
    Sweep thresholds and find the one with highest accuracy.

    At each threshold τ:
        predict 1 (same person) if similarity >= τ
        predict 0 (different)   if similarity <  τ

    Returns
    -------
    best_threshold : float
    best_accuracy  : float (0–1)
    """
    thresholds = np.linspace(-1.0, 1.0, 500)
    best_acc   = 0.0
    best_tau   = 0.5

    for tau in thresholds:
        preds   = (similarities >= tau).astype(int)
        acc     = np.mean(preds == labels)
        if acc > best_acc:
            best_acc = acc
            best_tau = tau

    return float(best_tau), float(best_acc)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Plot ROC Curve
# ─────────────────────────────────────────────────────────────────────────────

def plot_roc_and_distribution(
    similarities: np.ndarray,
    labels: np.ndarray,
    best_tau: float,
    output_dir: str,
) -> None:
    """
    Generate and save:
      1. ROC curve with AUC annotation
      2. Similarity score distribution (same vs. different)
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── ROC Curve ──────────────────────────────────────────────────────────
    fpr, tpr, thresholds_roc = roc_curve(labels, similarities)
    roc_auc = auc(fpr, tpr)

    # Find EER (Equal Error Rate) — point where FPR ≈ FNR
    fnr = 1 - tpr
    eer_idx = np.argmin(np.abs(fpr - fnr))
    eer = (fpr[eer_idx] + fnr[eer_idx]) / 2

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("LFW Face Verification Experiment", fontsize=14, fontweight="bold")

    # ROC
    ax = axes[0]
    ax.plot(fpr, tpr, color="#6C63FF", linewidth=2.5,
            label=f"AUC = {roc_auc:.4f}")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random classifier")
    ax.scatter(fpr[eer_idx], tpr[eer_idx], color="red", zorder=5,
               label=f"EER = {eer:.4f}")
    ax.set_xlabel("False Positive Rate (FAR)", fontsize=11)
    ax.set_ylabel("True Positive Rate (TAR)", fontsize=11)
    ax.set_title("ROC Curve", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # Score distribution
    ax = axes[1]
    same_sims = similarities[labels == 1]
    diff_sims = similarities[labels == 0]
    ax.hist(same_sims, bins=60, alpha=0.65, color="#4CAF50",
            label=f"Same person (n={len(same_sims)})", density=True)
    ax.hist(diff_sims, bins=60, alpha=0.65, color="#F44336",
            label=f"Different person (n={len(diff_sims)})", density=True)
    ax.axvline(best_tau, color="#6C63FF", linewidth=2, linestyle="--",
               label=f"Best threshold τ = {best_tau:.3f}")
    ax.set_xlabel("Cosine Similarity", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.set_title("Score Distribution", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out_path = os.path.join(output_dir, "lfw_results.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[lfw] Plot saved -> {out_path}")

    return roc_auc, eer


# ─────────────────────────────────────────────────────────────────────────────
# 5. Save Threshold for Attendance
# ─────────────────────────────────────────────────────────────────────────────

def save_threshold(tau: float, output_dir: str) -> None:
    """Save the best threshold to a file so attendance.py can read it."""
    import json
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "threshold.json")
    with open(path, "w") as f:
        json.dump({"threshold": tau}, f, indent=2)
    print(f"[lfw] Threshold tau = {tau:.4f} saved -> {path}")


def load_threshold(gallery_dir: str, default: float = 0.70) -> float:
    """Load threshold from gallery_dir/threshold.json, fallback to default."""
    import json
    path = os.path.join(gallery_dir, "threshold.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return float(json.load(f)["threshold"])
    return default


# ─────────────────────────────────────────────────────────────────────────────
# 6. Main
# ─────────────────────────────────────────────────────────────────────────────

def run_experiment(lfw_dir: str, pairs_file: str, output_dir: str) -> None:
    print("\n[lfw] Loading models...")
    mtcnn, resnet = load_models(device="auto")

    print(f"\n[lfw] Parsing pairs from: {pairs_file}")
    pairs = parse_lfw_pairs(pairs_file, lfw_dir)
    print(f"[lfw] Total pairs: {len(pairs)} "
          f"({sum(p['label']==1 for p in pairs)} same, "
          f"{sum(p['label']==0 for p in pairs)} different)")

    print("\n[lfw] Embedding all face pairs (this may take 10-30 minutes on CPU)...")
    similarities, labels = compute_pair_similarities(pairs, mtcnn, resnet)

    print("\n[lfw] Finding best classification threshold...")
    best_tau, best_acc = find_best_threshold(similarities, labels)

    print("\n" + "=" * 50)
    print("  LFW VERIFICATION RESULTS")
    print("=" * 50)
    print(f"  Best threshold (τ)  : {best_tau:.4f}")
    print(f"  Accuracy at τ       : {best_acc * 100:.2f}%")

    roc_auc, eer = plot_roc_and_distribution(similarities, labels, best_tau, output_dir)
    print(f"  AUC                 : {roc_auc:.4f}")
    print(f"  EER                 : {eer * 100:.2f}%")
    print("=" * 50)

    # Save threshold so attendance.py uses the validated value
    save_threshold(best_tau, output_dir)
    print(f"\n[lfw] ✅ Experiment complete! Use τ = {best_tau:.4f} in attendance.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run LFW face verification experiments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lfw_dir",   default="data/lfw",
                        help="Path to lfw/ image folder")
    parser.add_argument("--pairs",     default="data/lfw/pairs.txt",
                        help="Path to pairs.txt")
    parser.add_argument("--output_dir", default="gallery",
                        help="Where to save plots and threshold.json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_experiment(
        lfw_dir=args.lfw_dir,
        pairs_file=args.pairs,
        output_dir=args.output_dir,
    )
