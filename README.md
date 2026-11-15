# 🎓 Face Recognition Smart Attendance System

A deep learning prototype for automated face recognition attendance, built for the Deep Learning Lab.

## Architecture

```
Webcam → MTCNN Detector → InceptionResnetV1 Embedder → Cosine Similarity → Attendance CSV
```

| Component | Technology |
|-----------|-----------|
| Face Detector | MTCNN (facenet-pytorch) |
| Embedding Model | InceptionResnetV1, pretrained on VGGFace2 |
| Similarity Metric | Cosine Similarity |
| Benchmark Dataset | Labeled Faces in the Wild (LFW) |
| UI | Streamlit web dashboard |

---

## Quick Start

### 1. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Enroll Students

Create a folder per student inside `data/enrolled/`:
```
data/enrolled/
    Alice_Smith/
        photo1.jpg
        photo2.jpg
    Bob_Jones/
        photo1.jpg
```

Then run:
```bash
python src/enroll.py
```

Or use the **Enroll tab** in the web UI (easier!).

### 3. Launch Web UI

```bash
streamlit run app.py
```

This opens a browser dashboard where you can:
- Enroll students by uploading photos
- Run LFW verification experiments
- Start live webcam attendance
- View and download attendance reports

### 4. Run Attendance from CLI

```bash
# Live webcam
python src/attendance.py

# With custom threshold
python src/attendance.py --threshold 0.72

# Image folder mode (no webcam needed)
python src/attendance.py --source data/test_images
```

---

## LFW Experiments (Optional but Recommended)

Download LFW:
1. Images: http://vis-www.cs.umass.edu/lfw/lfw.tgz
2. Pairs:  http://vis-www.cs.umass.edu/lfw/pairs.txt
3. Place in `data/lfw/`

Run:
```bash
python src/lfw_experiment.py
```

This produces:
- `gallery/lfw_results.png` — ROC curve + score distribution plot
- `gallery/threshold.json` — optimal threshold τ for attendance

---

## Project Structure

```
Face-Recgnition-attendance/
├── app.py                      # Streamlit web UI
├── requirements.txt
├── data/
│   ├── enrolled/               # Enrollment photos (one folder per student)
│   ├── lfw/                    # LFW dataset
│   └── attendance_logs/        # Output CSV files
├── gallery/
│   ├── embeddings.npy          # Enrolled face embeddings (N × 512)
│   ├── labels.json             # Student names (length N)
│   └── threshold.json          # Validated τ from LFW
└── src/
    ├── utils.py                # Shared: model loading, embedding, similarity
    ├── enroll.py               # Build gallery from enrolled photos
    ├── lfw_experiment.py       # LFW benchmark + ROC + threshold
    └── attendance.py           # Real-time webcam attendance + CSV logging
```

---

## Key Concepts for Beginners

### Face Embedding
A face embedding is a list of 512 numbers that uniquely describes a face — like a fingerprint in math form. The same person always produces similar numbers. Different people produce very different numbers.

### Cosine Similarity
Measures how similar two face embeddings are. Range: -1 to +1.
- **+1** → identical face
- **0** → completely different person
- **Threshold τ** → if similarity > τ, same person; otherwise "Unknown"

### L2 Normalisation
We scale every embedding vector to have length = 1. This makes cosine similarity equal to a simple dot product (fast!).

### LFW Benchmark
6,000 face pairs (same/different person). We use it to measure our model's accuracy and find the optimal threshold τ before using the system for real attendance.

---

## Controls (Webcam Mode)

| Key | Action |
|-----|--------|
| `Q` or `ESC` | Quit and save attendance CSV |
| `S` | Save attendance mid-session |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No face detected` during enrollment | Use a clearer photo, better lighting |
| Too many "Unknown" labels | Lower the threshold (e.g. 0.60) |
| Too many wrong recognitions | Raise the threshold (e.g. 0.80) |
| Webcam not opening | Try `--camera 1` for external webcam |
| Slow on CPU | Normal — MTCNN+ResNet work fine on CPU, just slightly slower |
