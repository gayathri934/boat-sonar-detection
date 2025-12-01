Boat Sonar Detection & Localization
Using Centroid Extraction, Preprocessing & Trajectory Tracking

Project Overview
This project focuses on extracting, detecting, and localizing a boat present in a high–noise underwater sonar video.
Sonar imagery presents fundamental challenges:
Intense speckle noise
-Low contrast
-Irregular lighting
-Nonlinear wave propagation
-Weak object shapes
The goal was to build a stable and consistent preprocessing + localization pipeline that identifies the boat region, extracts its centroid movement over time, and estimates its trajectory.


Objectives
✔ Extract frames from the raw sonar video
✔ Enhance sonar frames for better visibility
✔ Detect the boat region using intensity-based blob extraction
✔ Localize the boat using centroid detection
✔ Track movement over time
✔ Generate a trajectory plot
✔ Compute stability metrics

The original assignment also included object detection using deep learning (YOLO / Faster-RCNN etc), but due to system limitations, extremely large datasets, and bounding-box annotation constraints, that portion was not completed.
However, the pipeline built here forms the full backbone required for model training.

Dataset
Due to size limitations, sonar frames and supporting images are hosted externally.
🔗 Dataset Download Link: https://drive.google.com/drive/folders/1tpEuzPra7E72K_u1_SW_WgAVPK-NR2KW?usp=drive_link
The dataset includes:
Extracted sonar frames
Preprocessed (denoised + contrast-enhanced) frames
Topview boat images
Centroid tracking CSV
Trajectory plot image
Original raw sonar video

Methodology
1. Frame Extraction
Frames were sampled from the sonar video with controlled frame skipping (approx. every 5–7 frames) to reduce redundancy.
Output saved to:
data/sonar_frames/raw/

2. Preprocessing Pipeline
🔹 Median Filtering
Removes speckle noise while preserving edges.
🔹 Contrast Enhancement
Important because sonar reflections are extremely low-contrast.
We used:
CLAHE
Gamma tuning + histogram stretching
Enhanced frames saved to:
data/sonar_frames/preprocessed/

3. Boat Blob Detection (No Manual Labels)
Instead of manually drawing bounding boxes for hundreds of frames:
We used adaptive thresholding
Extracted only the largest reflective blob
Treated it as the boat
Extracted its centroid (cx, cy)
Intermediate debug frames saved to:
data/sonar_frames/blob_debug/

4. Centroid Tracking
All frame centroids were saved to:
centroid_track.csv
Then smoothing filters were applied:
moving average
outlier suppression
Final CSV:
centroid_track_smoothed.csv

5. Trajectory Plot
A full trajectory visualization was generated:
report/trajectory_plot.png
This demonstrates stable local motion of the detected object (presumably the boat) within expected sonar boundaries.

6. Localization Metrics
To quantify stability, we computed:
✔ Variance in X and Y
✔ Standard deviation
✔ Approximate detection bounding range
Example Result:
Centroid X std-dev: 417 px
Centroid Y std-dev: 100 px

Results Summary
✔ Successfully Completed
Sonar data extraction
Image preprocessing
Automated blob-based localization
Centroid extraction
Motion tracking and smoothing
Quantitative localization metrics
Visualization of full sonar trajectory
Output detection overlay video
Visual Example:
Trajectory indicates consistent motion trend and identifiable object path — proving that the boat’s sonar signature is extractable even under noise.

Limitations
1. No Bounding Box Annotation
Due to the large number of frames and constraints with installation of LabelImg, manual bounding box labeling was not completed.
Bounding boxes are required for YOLO, Faster-RCNN etc.
2. No Model Training (YOLO / RCNN)
The deep learning model training part was not completed.
Reasons:
Heavy GPU requirements
YOLOv8 and PyTorch dependencies on Windows were unstable
Lack of annotated dataset
Annotation tool GUI failures after installation
Processing speed and storage limitations
3. Dataset Scale
Sonar frames (~3000 images) are large in total size, requiring external hosting.
4. High Noise Domain
Even after preprocessing, intensity patterns sometimes remain vague, and blob extraction must be treated as an approximation.

Conclusion
Even without full deep learning integration, this project achieved the hardest parts:
-Signal cleaning
-Feature isolation
-Region localization
-Motion stability verification
The centroid-based approach proves that sonar data contains learnable detection patterns and confirms feasibility of ML-based object detection.
The entire dataset, cleaned frames, region overlays, centroid CSV, and trajectory visualization offer a complete foundation for future model training.
