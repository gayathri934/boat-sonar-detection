import cv2
import os

video_path = "data/sonar_raw_video.mp4"
out_dir = "data/sonar_frames/raw"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise ValueError(f"Could not open video file at {video_path}")

frame_idx = 0

# Start conservative. We will inspect and then adjust.
SAVE_EVERY = 5  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_idx % SAVE_EVERY == 0:
        out_path = os.path.join(out_dir, f"frame_{frame_idx:05d}.png")
        cv2.imwrite(out_path, frame)

    frame_idx += 1

cap.release()

print("Extraction complete.")
print(f"Total frames read: {frame_idx}")
print(f"Frames saved (~): {frame_idx // SAVE_EVERY}")
