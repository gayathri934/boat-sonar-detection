# Boat Detection and Localization in Sonar Imagery  
**Author:** Gayathri P K  
**Repository Name:** boat-sonar-detection  

---

##  Project Overview

This project builds a complete pipeline for detecting and localizing a boat in noisy underwater sonar imagery.  
It processes a raw sonar video, extracts frames, enhances sonar data to improve signal-to-noise ratio, detects the acoustic signature of the boat, tracks its centroid over time, and computes movement stability metrics.  

Because sonar returns are often amorphous and lack clear edges (unlike optical images), a classical image-processing + blob-segmentation + centroid-tracking approach was adopted for a robust baseline solution.  

The deep-learning detection phase (e.g., YOLO) was *planned* but not executed, due to dataset size and resource constraints. However, the code and dataset structure have been fully prepared so that training can be carried out with minimal additional effort.

---

##  Repository Structure


**scripts/** contains:
- `extract_frames.py` — extract frames from video  
- `preprocess_frames.py` — speckle reduction & contrast enhancement  
- `detect_blob.py` — intensity-based segmentation & blob detection  
- `track_centroid.py`, `smooth_track.py` — centroid extraction, smoothing & tracking  
- `localization_stats.py` — compute variance and spatial stability metrics  
- `generate_detection_video.py` — overlay detections + produce inference video  

**results/** includes:  
- `sonar_detection_output.mp4` — full sonar video with detection overlay  
- `centroid_track.csv`, `centroid_track_smoothed.csv` — raw and smoothed centroid tracks  
- `trajectory_plot.png` — 2D trajectory plot (boat path in sonar image coordinates)  

**samples/** contains a handful of example images to illustrate preprocessing, detection, and blob localization results.  

---

## 📥 Dataset Access

Raw data (sonar frames, raw video, and top-view boat images) are too large to store directly in this repository.  
They are hosted externally on Google Drive:

**Dataset Download Link:**  
[https://drive.google.com/drive/folders/1tpEuzPra7E72K_u1_SW_WgAVPK-NR2KW?usp=sharing](https://drive.google.com/drive/folders/1tpEuzPra7E72K_u1_SW_WgAVPK-NR2KW?usp=sharing)

**To run locally:**

1. Download the entire dataset from the link.  
2. Place it in your local clone under the folder structure:
data/
sonar_raw_video.mp4
sonar_frames/
raw/
topview_raw/
images/

3. Run the preprocessing + detection scripts according to the instructions below.

---

## 🧪 How to Run the Pipeline

```bash
# 1. Extract frames from raw sonar video
python scripts/extract_frames.py

# 2. Preprocess frames (speckle suppression + contrast enhancement)
python scripts/preprocess_frames.py

# 3. Detect boat region via blob segmentation
python scripts/detect_blob.py

# 4. Track centroid across frames
python scripts/track_centroid.py
python scripts/smooth_track.py

# 5. Compute localization metrics
python scripts/localization_stats.py

# 6. (Optional) Generate detection overlay video
python scripts/generate_detection_video.py

Results Summary

Preprocessing: Significant speckle noise reduction and contrast enhancement allowed stable region detection where raw sonar frames were too noisy for reliable detection.

Blob-based detection successfully identified the boat’s acoustic return as the largest intensity cluster in each usable frame.

Centroid tracking + smoothing produced a coherent boat trajectory over time.

Localization stability metrics:

Centroid X-axis standard deviation: ~ 417 px

Centroid Y-axis standard deviation: ~ 100 px
These indicate that the detection remains spatially bounded despite sonar noise and vehicle motion.

Inference video (in results/) shows consistent detection overlays — validating the method qualitatively.

This baseline demonstrates that classical signal-processing + segmentation + tracking is viable for sonar boat localization.

Limitations & Why Deep-Learning Was Not Completed

No bounding-box annotations: Manual bounding-box annotation for hundreds of sonar frames was prohibitive given time and hardware constraints.

Ambiguous appearance in sonar: The boat appears as a diffuse acoustic blob, lacking clear structural edges. This undermines bounding-box detection reliability.

Hardware & dataset size issues: Full-frame sonar data and optical top-view images consume substantial storage and compute resources; training a deep model (YOLO or similar) would exceed available local GPU capacity.

Domain gap risk: Mixing optical top-view images with sonar data for training may cause false positives, because visual features differ drastically between domains.

Although not executed, the DL phase is fully planned and prepared:

Model

YOLOv8 (Nano or Small)

Single-class detector: boat

Dataset plan

Two experiments:

Train on sonar frames only

Train on combined sonar + top-view images

Evaluate:

mAP

Precision, Recall, F1

False positives

Inference latency

Label strategy

Use blob bounding boxes as pseudo-labels for sonar

Manual annotation for top-view images

Expected Observations

Sonar-only training performs better on sonar inference

Adding optical images may hurt until domain gap is reduced

Conclusion

This project successfully:

extracted reliable localization from noisy sonar footage

demonstrated consistent target reflectance

quantified spatial stability

produced visual detection results

While the deep-learning phase was not executed due to hardware & annotation constraints, the preparation for it has been completed logically and structurally.

The classical pipeline outcomes confirm:

Sonar data does contain stable, learnable signatures for boat detection
and provide a solid foundation for future model-based work.
