import cv2
import os
import numpy as np

raw_dir = "data/sonar_frames/raw"
out_dir = "data/sonar_frames/preprocessed"
os.makedirs(out_dir, exist_ok=True)

for fname in sorted(os.listdir(raw_dir)):
    if not fname.lower().endswith((".png", ".jpg")):
        continue
    
    img_path = os.path.join(raw_dir, fname)
    img = cv2.imread(img_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Median filtering to reduce speckle
    denoised = cv2.medianBlur(gray, 7)

    # CLAHE to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)

    # OPTIONAL: remove central sonar beam
    h, w = enhanced.shape
    center_line = w // 2
    enhanced[:, center_line-2:center_line+2] = np.median(enhanced)

    out_path = os.path.join(out_dir, fname)
    cv2.imwrite(out_path, enhanced)

print("Preprocessing complete.")
