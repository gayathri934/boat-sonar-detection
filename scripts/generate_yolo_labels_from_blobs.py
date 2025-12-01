import cv2
import numpy as np
import os

pre_dir = "data/sonar_frames/preprocessed"
label_out_dir = "data/sonar_frames/yolo_labels_auto"
os.makedirs(label_out_dir, exist_ok=True)

for fname in sorted(os.listdir(pre_dir)):
    if not fname.lower().endswith(".png"):
        continue

    img_path = os.path.join(pre_dir, fname)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    # --- same segmentation logic as before ---
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
        # no detection -> no label file
        continue

    largest = max(contours, key=cv2.contourArea)
    x, y, bw, bh = cv2.boundingRect(largest)

    # YOLO normalized coordinates
    x_c = (x + bw / 2) / w
    y_c = (y + bh / 2) / h
    nw = bw / w
    nh = bh / h

    # class 0 = boat
    label_path = os.path.join(label_out_dir, fname.replace(".png", ".txt"))
    with open(label_path, "w") as f:
        f.write(f"0 {x_c:.6f} {y_c:.6f} {nw:.6f} {nh:.6f}\n")

print("Auto YOLO labels generated in data/sonar_frames/yolo_labels_auto")
