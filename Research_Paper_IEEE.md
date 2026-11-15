# Real-Time Contactless Attendance System Using Deep Face Embeddings and Cosine Metric Learning

**Khizra Bushra Raien**$^1$ (Roll No: 32), **Meet Ashish Bajoria**$^2$ (Roll No: 36), **Mohammad Moinuddin**$^3$ (Roll No: 38), **Pratham Singh Thakur**$^4$ (Roll No: 44)  
*Department of Electronics Engineering, Ramdeobaba University, Nagpur, India*  
*Under the Guidance of: Prof. V. R. Gupta*

---

### Abstract
Manual classroom attendance systems based on paper rolls or signature sheets are slow, disrupt teaching time, and frequently suffer from proxy marking. While biometric fingerprint scanners offer an alternative, they require physical contact, cause entry bottlenecks, and raise hygiene concerns in shared laboratory environments. In this paper, we design and implement a lightweight, real-time smart attendance prototype using deep facial recognition. The proposed pipeline couples Multi-Task Cascaded Convolutional Networks (MTCNN) for 5-point facial landmark detection and pose alignment with a pretrained Inception-ResNet-v1 feature extractor trained on VGGFace2 to generate 512-dimensional $L_2$-normalized embeddings. Identity matching is performed via cosine similarity against a local consent-based enrollment gallery. An empirically validated decision threshold ($\tau = 0.70$) enables confident student verification while rejecting unregistered individuals as "Unknown". To overcome latency bottlenecks on commodity edge hardware, we introduce a $0.5\times$ spatial downsampling detection pass with frame skipping, achieving stable ~30 FPS live tracking on CPU. Attendance records are deduplicated and automatically exported with date and time stamps to CSV spreadsheets. Experimental evaluation shows $>95\%$ recognition accuracy with minimal false acceptances, establishing a practical, privacy-respecting, and proxy-free attendance solution.

**Keywords**—Face Recognition, MTCNN, Inception-ResNet-v1, Cosine Similarity, Automated Attendance System, Real-Time Edge Vision.

---

### I. Introduction
Student attendance tracking is a routine operational requirement across academic institutions. Despite rapid digitization, most university classrooms still rely on paper roll calls or circulating attendance sheets. These manual approaches suffer from three well-documented drawbacks:
1. **Time Consumption:** Calling roll numbers for 50–70 students typically occupies 5 to 10 minutes of valuable laboratory or lecture time.
2. **Proxy Attendance:** Physical signature sheets allow students to sign on behalf of absent peers with minimal accountability.
3. **Transcription Overhead:** Transferring handwritten marks into institutional management portals requires repetitive manual labor and introduces clerical errors.

Biometric alternatives such as fingerprint scanners eliminate proxy attendance but create long queues at classroom doors. Additionally, shared physical touchpoints present hygiene issues in high-traffic campus settings. 

Computer vision offers a contactless, automated solution. By leveraging existing webcams or classroom cameras, students can be identified naturally as they enter. However, building an automated face attendance system for practical deployment introduces distinct engineering challenges:
- Real-time video processing must run smoothly on standard classroom computers without requiring high-end dedicated GPUs.
- Variations in student head pose, lighting changes throughout the day, and camera distance must not cause identification failures.
- The system must respect user privacy by strictly relying on voluntary opt-in enrollment and reliably rejecting unauthorized faces.

In this work, we present a practical attendance prototype tailored to laboratory and classroom environments. Instead of training a classification model from scratch—which requires thousands of images per student and necessitates full retraining whenever a student joins the class—we adopt a deep metric learning approach. Faces are aligned via MTCNN, mapped into a compact 512-dimensional latent feature space using a pretrained Inception-ResNet-v1 network, and matched against enrolled gallery embeddings using cosine distance. 

The primary contributions of this work are:
- A complete, end-to-end contactless attendance system with automatic, deduplicated timestamp logging and a Streamlit dashboard.
- An optimization strategy combining half-resolution detection, frame skipping, and camera buffer management to enable real-time CPU execution (~30 FPS).
- Empirical validation of the recognition threshold using Labeled Faces in the Wild (LFW) benchmark pairs and real-world student trials.

---

### II. Related Work
Early automated attendance systems relied heavily on traditional handcrafted visual features, including Principal Component Analysis (Eigenfaces) [1] and Local Binary Patterns Histograms (LBPH) [2]. While computationally lightweight, these shallow representations degrade significantly under ambient illumination changes, mild facial rotations, and varying camera angles.

The introduction of Deep Convolutional Neural Networks (CNNs) fundamentally transformed facial recognition. Schroff et al. [3] introduced FaceNet, demonstrating that mapping face images directly into a Euclidean embedding space using triplet loss produces discriminative feature vectors where distances directly correspond to facial similarity. Concurrently, Multi-Task Cascaded Convolutional Networks (MTCNN) developed by Zhang et al. [4] established a robust standard for joint face detection and five-point landmark alignment (left eye, right eye, nose, left mouth corner, right mouth corner). 

Recent academic prototypes often frame attendance as an $N$-class closed-set classification problem using Softmax classifiers or Support Vector Machines (SVM). While functional for static groups, such architectures cannot handle open-set scenarios—where unregistered visitors enter the camera frame—and require full model retraining whenever new participants are enrolled. In contrast, our pipeline relies on direct geometric metric learning and thresholded vector comparison, enabling instantaneous enrollment and explicit "Unknown" classification.

---

### III. Proposed System Methodology

The complete attendance pipeline follows a modular four-stage architecture: **Image Acquisition $\rightarrow$ Face Detection & Alignment $\rightarrow$ Feature Embedding $\rightarrow$ Cosine Metric Identification & Logging**.

```
[Webcam Stream (640x480)]
           │
           ▼
[Frame Subsampling (0.5x) & Frame Skipping]
           │
           ▼
[MTCNN Detection & 5-Point Landmark Alignment]
           │
           ▼
[Aligned Face Crop (160x160 RGB)]
           │
           ▼
[Inception-ResNet-v1 (VGGFace2 Pretrained)]
           │
           ▼
[512-Dimensional L2-Normalized Embedding Vector]
           │
           ▼
[Cosine Similarity Matching vs. Stored Gallery]
           │
   ┌───────┴───────┐
   ▼               ▼
Sim >= tau      Sim < tau
[Recognized]   [Unknown]
   │
   ▼
[AttendanceLogger: CSV Output (Name, Date, Time)]
```

#### A. Face Detection and 5-Point Alignment (MTCNN)
Video frames are read via OpenCV from the active camera sensor. To accurately isolate faces, we employ MTCNN, which operates across three cascaded stages:
1. **Proposal Network (P-Net):** A shallow fully convolutional network that parses an image pyramid to generate candidate bounding bounding boxes.
2. **Refine Network (R-Net):** A CNN that rejects false positive candidates and performs bounding box regression.
3. **Output Network (O-Net):** A deeper network that determines final bounding coordinates and predicts five facial landmarks: left eye, right eye, nose tip, left mouth corner, and right mouth corner.

Using the detected eye coordinates, an affine rotation is applied to horizontally align the facial plane. The aligned face is cropped with a boundary margin and scaled to $160 \times 160 \times 3$ pixels. Normalizing facial orientation ensures that subsequent embedding extraction is invariant to minor head tilt.

#### B. Deep Feature Representation (Inception-ResNet-v1)
Feature extraction is performed by an Inception-ResNet-v1 deep architecture pretrained on the VGGFace2 dataset (comprising 3.3 million face images across 9,131 identities). The network blends the computational efficiency of Inception factorization blocks with residual skip connections, mitigating vanishing gradients while capturing multi-scale facial patterns.

The forward pass transforms the aligned $160 \times 160$ crop into a continuous 512-dimensional vector $v \in \mathbb{R}^{512}$. To eliminate distortions caused by variations in lighting intensity, the vector is explicitly $L_2$-normalized:

$$\hat{v} = \frac{v}{\|v\|_2} = \frac{v}{\sqrt{\sum_{i=1}^{512} v_i^2}}$$

Following $L_2$ normalization, all face embeddings reside on the surface of a 512-dimensional unit hypersphere ($\|\hat{v}\|_2 = 1$).

#### C. Gallery Construction and Enrollment
During volunteer enrollment, participating students provide 3 to 5 portrait photographs captured under different angles and lighting conditions. For each image, the pipeline detects the face, computes its normalized embedding, and records the student's name:

$$\mathcal{G} = \{(\hat{e}_k, y_k)\}_{k=1}^M$$

where $\hat{e}_k$ is the $k$-th enrolled embedding, $y_k$ is the associated student identity label, and $M$ is the total number of gallery vectors. Storing multiple feature vectors per student accounts for natural intra-class facial variation without requiring data augmentation or artificial image synthesis.

#### D. Metric Matching and Unknown Face Rejection
During live attendance monitoring, a query face detected in frame $t$ generates a normalized embedding $\hat{q}_t$. The system computes the cosine similarity between $\hat{q}_t$ and every stored gallery embedding $\hat{e}_k \in \mathcal{G}$. Because all vectors are unit-normalized, cosine similarity reduces to an efficient vector dot product:

$$\text{Sim}(\hat{q}_t, \hat{e}_k) = \hat{q}_t \cdot \hat{e}_k = \sum_{j=1}^{512} \hat{q}_{t,j} \cdot \hat{e}_{k,j}$$

The maximum similarity score and the corresponding identity candidate are determined via:

$$k^* = \arg\max_{k \in \{1, \dots, M\}} \text{Sim}(\hat{q}_t, \hat{e}_k), \quad S^* = \text{Sim}(\hat{q}_t, \hat{e}_{k^*})$$

The final identification decision is governed by an operating threshold $\tau$:

$$\text{Identity}(\hat{q}_t) = \begin{cases} y_{k^*}, & \text{if } S^* \ge \tau \\ \text{"Unknown"}, & \text{if } S^* < \tau \end{cases}$$

If $S^* < \tau$, the person is marked as an unrecognized visitor, preserving privacy and preventing false positive matches.

#### E. Deduplicated Attendance Logging
When a student is recognized ($S^* \ge \tau$), their identity is passed to the `AttendanceLogger` module. The system initializes all registered students as "Absent" at the start of a session. Upon the first valid recognition event, the student's status is toggled to "Present", and the exact entry timestamp is recorded. Subsequent detections within the same session do not duplicate the record. The session log is saved to disk in CSV format:

$$\text{Record} = \{\text{Student Name}, \text{Date}, \text{Time}, \text{Status}\}$$

---

### IV. Real-Time Latency Optimizations
Running MTCNN face detection and Inception-ResNet feature extraction concurrently on standard consumer-grade CPUs typically introduces severe processing latency (5–8 FPS), resulting in video lag. To achieve responsive performance on edge devices without GPU acceleration, three optimizations were implemented:

1. **Downsampled Detection Pass:** Live webcam frames are captured at $640 \times 480$. MTCNN detection is executed on a half-resolution frame ($320 \times 240$, $0.5\times$ scale), reducing the pixel volume by $75\%$. Once bounding boxes are detected, coordinates are scaled back by $2.0\times$ to crop the face from the original high-resolution frame for embedding.
2. **Inference Frame Skipping:** Face detection and embedding computation are executed every $N$-th frame ($N=3$). For intermediate frames, existing bounding boxes and identity labels persist on screen, maintaining smooth video playback while reducing CPU load by $66\%$.
3. **Buffer Management:** OpenCV's default multi-frame video buffer introduces cumulative frame latency. Setting `cv2.CAP_PROP_BUFFERSIZE = 1` and using the DirectShow (`cv2.CAP_DSHOW`) backend on Windows ensures the video pipeline processes strictly the most recent sensor frame.

Together, these adjustments improved CPU inference performance from 7 FPS to approximately 28–30 FPS, providing a responsive experience.

---

### V. Experimental Results and Discussion

#### A. Benchmark Evaluation on Labeled Faces in the Wild (LFW)
To evaluate the discriminative capability of the feature extractor and determine the optimal decision threshold $\tau$, the pipeline was evaluated on the standard LFW verification benchmark across 6,000 image pairs (3,000 matched same-identity pairs, 3,000 mismatched different-identity pairs).

Cosine similarities were calculated across all pairs. A threshold sweep was conducted over the range $[-1.0, 1.0]$ to identify the operating point that minimizes False Acceptance Rate (FAR) and False Rejection Rate (FRR).

| Metric | Measured Value |
|---|---|
| Peak Verification Accuracy | **95.2%** |
| Area Under the ROC Curve (AUC) | **0.984** |
| Equal Error Rate (EER) | **4.6%** |
| Optimal Threshold ($\tau$) | **0.70** |

At $\tau = 0.70$, the distribution of positive (same person) and negative (different person) similarity scores shows minimal overlap. Scores for identical individuals typically range between $0.74$ and $0.92$, whereas pairs of different individuals concentrate between $0.15$ and $0.55$.

#### B. Live Classroom Evaluation
The complete prototype was deployed in a laboratory environment with volunteer students enrolled under varied lighting conditions and head orientations.

```
       SAMPLE ATTENDANCE SESSION LOG (CSV EXPORT)
=========================================================
Name                    Date         Time       Status
---------------------------------------------------------
Khizra Bushra Raien     2026-11-15   11:58:12   Present
Meet Ashish Bajoria     2026-11-15   11:58:04   Present
Mohammad Moinuddin      2026-11-15   11:58:20   Present
Pratham Singh Thakur    2026-11-15   11:58:16   Present
=========================================================
Total Enrolled: 4  |  Present: 4 (100.0%)  |  Absent: 0
```

1. **Recognition Speed:** The average recognition latency from the moment a student entered the camera frame to CSV logging was under 180 milliseconds.
2. **Imposter and Unknown Handling:** Unregistered individuals standing in front of the camera achieved maximum similarity scores between $0.32$ and $0.58$, well below $\tau = 0.70$, and were labeled "Unknown" with red bounding boxes. No false positive identifications occurred.
3. **Pose and Lighting Robustness:** Thanks to MTCNN 5-point landmark alignment, facial rotations up to $\pm 30^\circ$ were identified reliably. Moderate ambient lighting variations caused minor score fluctuations ($\pm 0.05$) without dipping below the classification threshold.

---

### VI. Practical Limitations
While the system performs robustly under normal operating conditions, two main limitations remain:
1. **Extreme Occlusion:** Heavy facial obstructions (such as opaque medical masks or dense sunglasses) reduce MTCNN detection confidence and distort embedding vectors, causing valid students to be classified as Unknown.
2. **Spoofing Vulnerability:** As with any standard RGB camera pipeline, the current setup does not incorporate infrared depth sensing or dynamic liveness detection. A printed high-resolution photograph or a smartphone screen display could potentially be accepted if held steadily before the lens.

---

### VII. Conclusion and Future Scope
In this paper, we presented a real-time, contactless face recognition attendance system designed for university classrooms and laboratories. By integrating MTCNN facial detection and alignment with Inception-ResNet-v1 feature embeddings and cosine metric learning, the system provides accurate identification while preserving privacy through thresholded unknown rejection. Engineered optimizations—including spatial downsampling, frame skipping, and buffer control—enable smooth 30 FPS execution on standard CPU hardware without costly GPU infrastructure. The interactive Streamlit dashboard streamlines enrollment, live monitoring, and attendance export.

Future work will focus on:
- **Liveness Detection:** Integrating temporal micro-motion analysis (eye blink and head movement tracking) to prevent 2D presentation attacks.
- **Embedded Edge Deployment:** Porting the neural inference pipeline to dedicated low-power edge accelerators such as the NVIDIA Jetson Orin Nano.
- **Enterprise Integration:** Connecting the attendance logger directly to institutional SQL databases and student ERP portals via authenticated REST APIs.

---

### References
[1] M. Turk and A. Pentland, "Eigenfaces for Recognition," *Journal of Cognitive Neuroscience*, vol. 3, no. 1, pp. 71–86, 1991.  
[2] T. Ahonen, A. Hadid, and M. Pietikäinen, "Face Description with Local Binary Patterns: Application to Face Recognition," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 28, no. 12, pp. 2037–2041, Dec. 2006.  
[3] F. Schroff, D. Kalenichenko, and J. Philbin, "FaceNet: A Unified Embedding for Face Recognition and Clustering," in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Boston, MA, USA, 2015, pp. 815–823.  
[4] K. Zhang, Z. Zhang, Z. Li, and Y. Qiao, "Joint Face Detection and Alignment Using Multi-Task Cascaded Convolutional Networks," *IEEE Signal Processing Letters*, vol. 23, no. 10, pp. 1499–1503, Oct. 2016.  
[5] Q. Cao, L. Shen, W. Xie, O. M. Parkhi, and A. Zisserman, "VGGFace2: A Dataset for Recognising Faces across Pose and Age," in *Proc. 13th IEEE International Conference on Automatic Face & Gesture Recognition (FG)*, Xi'an, China, 2018, pp. 67–74.  
[6] G. B. Huang, M. Ramesh, T. Berg, and E. Learned-Miller, "Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments," University of Massachusetts, Amherst, Tech. Rep. 07-49, Oct. 2007.

