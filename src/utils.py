# -*- coding: utf-8 -*-
"""
utils.py -- Shared helpers for the Face Recognition Attendance System
======================================================================
This module is the backbone of the entire system. It handles:
  1. Loading the MTCNN face detector and InceptionResnetV1 embedding model
  2. Detecting and aligning faces from images / webcam frames
  3. Extracting L2-normalised face embeddings (512-d vectors)
  4. Computing cosine similarity between two embeddings
  5. Loading and saving the enrolled-student gallery from disk

WHY THESE CHOICES?
  - MTCNN: detects face bounding boxes AND 5 landmarks (eyes, nose, corners
    of mouth). We use landmarks to geometrically align the face so the
    embedding model always sees the face in the same standard pose.
  - InceptionResnetV1 (pretrained='vggface2'): trained on 3.3M faces; produces
    a 512-d vector where same-person faces cluster together and different-
    person faces are far apart in vector space.
  - L2 normalisation: scales every vector to unit length (length=1).
    This lets cosine similarity reduce to a simple dot product, which is
    fast and numerically stable.
"""

import os
import sys
import json
import numpy as np
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

# Force UTF-8 for the terminal process (belt-and-suspenders alongside PYTHONUTF8)
reconfigure = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure):
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


# ---------------------------------------------------------------------------
# 1. Model Loading
# ---------------------------------------------------------------------------

def load_models(device="auto"):
    """
    Load and return (mtcnn, resnet) models on the chosen device.

    Parameters
    ----------
    device : str
        'auto' -- use GPU if available, else CPU.
        'cpu'  -- force CPU.
        'cuda' -- force GPU.

    Returns
    -------
    mtcnn   : MTCNN
        Face detector. Accepts an image, returns aligned face tensor.
    resnet  : InceptionResnetV1
        Face embedding model. Accepts an aligned face tensor, returns
        a 512-d float vector.

    Beginner note
    -------------
    We call model.eval() to put the model in inference mode -- this disables
    things like Dropout that are only used during training.
    """
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[utils] Using device: {device}")

    # MTCNN: returns aligned 160x160 RGB tensors, keeps only the best face.
    # image_size=160 matches InceptionResnetV1's expected input.
    mtcnn = MTCNN(
        image_size=160,
        margin=14,           # reduced margin for cleaner crop
        min_face_size=50,    # skip micro noise/distant heads for speed
        thresholds=[0.7, 0.8, 0.8],  # faster rejection of false positives
        factor=0.709,        # scale factor for image pyramid
        post_process=True,   # normalise pixel values to [-1, 1]
        keep_all=True,       # return ALL detected faces (not just the largest)
        device=device,
    )

    # InceptionResnetV1 pretrained on VGGFace2 (3.3M face images, 9k identities)
    resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

    return mtcnn, resnet


# ---------------------------------------------------------------------------
# 2. Face Detection and Alignment
# ---------------------------------------------------------------------------

def detect_faces(img, mtcnn):
    """
    Detect all faces in a PIL image.

    Returns
    -------
    face_tensors : torch.Tensor of shape (N, 3, 160, 160) or None
        One aligned face tensor per detected face.
    boxes : list of [x1, y1, x2, y2] or None
        Bounding boxes in pixel coordinates.

    Beginner note
    -------------
    MTCNN is a cascade detector: it runs three tiny networks (P-Net, R-Net,
    O-Net) in sequence, each refining the candidate face regions from the
    previous stage. This makes it fast yet accurate.
    """
    with torch.no_grad():
        # facenet-pytorch >= 2.5.3: mtcnn.detect() returns (boxes, probs)
        # and mtcnn() returns aligned face tensors separately.
        boxes, probs = mtcnn.detect(img)      # boxes: ndarray (N,4) or None
        face_tensors = mtcnn(img)             # Tensor (N,3,160,160) or None

    if face_tensors is None or boxes is None:
        return None, None

    # Add batch dim if only one face was returned
    if face_tensors.dim() == 3:
        face_tensors = face_tensors.unsqueeze(0)

    # Filter out low-confidence detections (threshold: 0.90)
    if probs is not None:
        confident = [p is not None and float(p) > 0.90 for p in probs]
        if not any(confident):
            return None, None
        face_tensors = face_tensors[confident]
        boxes = [b.tolist() for b, c in zip(boxes, confident) if c]
    else:
        boxes = [b.tolist() for b in boxes]

    return face_tensors, boxes


def detect_single_face(img, mtcnn):
    """
    Detect the best (largest / most confident) face in an image.
    Useful during enrollment where we expect exactly one face per photo.

    Returns
    -------
    face_tensor : torch.Tensor of shape (3, 160, 160) or None
    """
    mtcnn_single = MTCNN(
        image_size=160, margin=20, min_face_size=40,
        post_process=True, keep_all=False, device=mtcnn.device,
    )
    with torch.no_grad():
        face_tensor = mtcnn_single(img)
    return face_tensor


# ---------------------------------------------------------------------------
# 3. Face Embedding
# ---------------------------------------------------------------------------

def get_embedding(face_tensor, resnet):
    """
    Convert an aligned face tensor to an L2-normalised 512-d embedding vector.

    Parameters
    ----------
    face_tensor : torch.Tensor, shape (3, 160, 160) or (N, 3, 160, 160)
        Pixel values in [-1, 1] (output of MTCNN with post_process=True).
    resnet : InceptionResnetV1
        The embedding model.

    Returns
    -------
    embedding : np.ndarray, shape (512,) or (N, 512)
        L2-normalised embedding vector(s).

    Beginner note
    -------------
    L2 normalisation: divide a vector by its own length so the result has
    length=1. After this, cosine_similarity(a, b) = dot(a, b).
    """
    device = next(resnet.parameters()).device

    # Add batch dimension if single face
    if face_tensor.dim() == 3:
        face_tensor = face_tensor.unsqueeze(0)  # (1, 3, 160, 160)

    face_tensor = face_tensor.to(device)

    with torch.no_grad():
        embedding = resnet(face_tensor)  # shape (N, 512)

    # L2 normalise (already done inside InceptionResnetV1, but we be explicit)
    embedding = embedding / embedding.norm(dim=1, keepdim=True)

    embedding_np = embedding.cpu().numpy()
    return embedding_np.squeeze() if embedding_np.shape[0] == 1 else embedding_np


# ---------------------------------------------------------------------------
# 4. Cosine Similarity
# ---------------------------------------------------------------------------

def cosine_similarity(a, b):
    """
    Compute cosine similarity between vector a and vector/matrix b.

    Because both vectors are L2-normalised (length=1), this equals dot(a, b).
    Result is in [-1, 1]:
        +1 = identical direction (same person)
         0 = orthogonal (unrelated)
        -1 = opposite direction (very different)

    Parameters
    ----------
    a : np.ndarray, shape (512,)
        Query embedding.
    b : np.ndarray, shape (512,) or (N, 512)
        Gallery embedding(s).

    Returns
    -------
    similarity : float or np.ndarray of shape (N,)
    """
    a = a / (np.linalg.norm(a) + 1e-10)
    if b.ndim == 1:
        b = b / (np.linalg.norm(b) + 1e-10)
        return float(np.dot(a, b))
    else:
        norms = np.linalg.norm(b, axis=1, keepdims=True) + 1e-10
        b_norm = b / norms
        return b_norm @ a  # shape (N,)


# ---------------------------------------------------------------------------
# 5. Gallery I/O
# ---------------------------------------------------------------------------

def save_gallery(embeddings, labels, gallery_dir):
    """
    Save the enrolled gallery to disk.

    Files written
    -------------
    gallery/embeddings.npy  -- float32 array of shape (N, 512)
    gallery/labels.json     -- list of N student name strings

    Beginner note
    -------------
    We keep the two files in sync: embeddings[i] belongs to labels[i].
    """
    os.makedirs(gallery_dir, exist_ok=True)
    np.save(os.path.join(gallery_dir, "embeddings.npy"), embeddings.astype(np.float32))
    with open(os.path.join(gallery_dir, "labels.json"), "w") as f:
        json.dump(labels, f, indent=2)
    print(f"[utils] Gallery saved: {len(labels)} embeddings -> {gallery_dir}")


def load_gallery(gallery_dir):
    """
    Load the enrolled gallery from disk.

    Returns
    -------
    embeddings : np.ndarray, shape (N, 512)
    labels     : list of str, length N
    """
    emb_path   = os.path.join(gallery_dir, "embeddings.npy")
    label_path = os.path.join(gallery_dir, "labels.json")

    if not os.path.exists(emb_path) or not os.path.exists(label_path):
        raise FileNotFoundError(
            f"Gallery not found in {gallery_dir}. "
            "Run enroll.py first to build the gallery."
        )

    embeddings = np.load(emb_path)
    with open(label_path, "r") as f:
        labels = json.load(f)

    print(f"[utils] Gallery loaded: {len(labels)} embeddings from {gallery_dir}")
    return embeddings, labels


# ---------------------------------------------------------------------------
# 6. Image Loading Helpers
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def load_image_as_pil(path):
    """Load an image file as a PIL RGB image. Returns None on failure."""
    try:
        img = Image.open(path).convert("RGB")
        return img
    except Exception as e:
        print(f"[utils] Could not load image {path}: {e}")
        return None


def opencv_frame_to_pil(frame):
    """Convert an OpenCV BGR frame (numpy array) to a PIL RGB image."""
    import cv2
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)
