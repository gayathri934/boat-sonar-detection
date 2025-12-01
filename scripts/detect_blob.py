import cv2
import numpy as np
import os

pre_dir = "data/sonar_frames/preprocessed"
out_dir = "data/sonar_frames/preprocessed"
debug_dir = "data/sonar_frames/blob_debug"

os.makedirs(debug_dir, exist_ok=True)

for fname in sorted(os.listdir(pre_dir)):
    if not fname.lower().endswith(".png"):
        continue

    img_path = os.path.join(pre_dir, fname)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        35,
        -5
    )

    # Morphological cleaning
    kernel = np.ones((5,5), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Find blobs
    contours, _ = cv2.findContours(
        clean,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:
        continue

    # Find largest blob
    areas = [cv2.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    largest = contours[idx]

    # Bounding region
    x, y, w, h = cv2.boundingRect(largest)

    # Visual overlay on original
    overlay = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    cv2.rectangle(overlay, (x,y), (x+w, y+h), (0,255,0), 2)

    # Compute centroid
    M = cv2.moments(largest)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(overlay, (cx, cy), 5, (255,255,255), -1)
    else:
        cx, cy = -1, -1

    out_file = os.path.join(debug_dir, fname)
    cv2.imwrite(out_file, overlay)

print("Blob extraction complete. Check blob_debug outputs.")
