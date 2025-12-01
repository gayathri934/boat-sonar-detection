import cv2
import numpy as np
import os
import csv

pre_dir = "data/sonar_frames/preprocessed"
csv_out = "data/sonar_frames/centroid_track.csv"

records = []

for fname in sorted(os.listdir(pre_dir)):
    if not fname.lower().endswith(".png"):
        continue
    
    img_path = os.path.join(pre_dir, fname)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # threshold
    thresh = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        35, -5
    )
    
    kernel = np.ones((5,5), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        records.append([fname, -1, -1])
        continue

    largest = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest)

    if M["m00"] == 0:
        cx, cy = -1, -1
    else:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

    records.append([fname, cx, cy])

# save CSV
with open(csv_out, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "cx", "cy"])
    writer.writerows(records)

print("Centroid tracking CSV saved.")
