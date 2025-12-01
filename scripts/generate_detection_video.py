import cv2
import pandas as pd
import os

csv = pd.read_csv("data/sonar_frames/centroid_track_smoothed.csv")
pre_dir = "data/sonar_frames/preprocessed"
out_vid = "data/sonar_frames/sonar_detection_output.mp4"

frames = sorted(os.listdir(pre_dir))

# Use MJPG codec (super compatible)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# Initialize after reading first frame
first = cv2.imread(os.path.join(pre_dir, frames[0]))
h, w = first.shape[:2]
writer = cv2.VideoWriter(out_vid, fourcc, 10.0, (w, h))

# Iterate by matching csv order
for _, row in csv.iterrows():
    fname = row["frame"]
    cx = row["cx_smooth"]
    cy = row["cy_smooth"]

    img_path = os.path.join(pre_dir, fname)
    img = cv2.imread(img_path)

    if img is None:
        continue

    if cx > 0:
        cv2.circle(img, (int(cx), int(cy)), 10, (0,255,0), -1)

    writer.write(img)

writer.release()
print("\nVideo regenerated successfully using MJPG codec!")
print("Saved at:", out_vid)
