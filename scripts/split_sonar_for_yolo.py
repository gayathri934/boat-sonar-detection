import os
import shutil

img_dir = "data/sonar_frames/preprocessed"
lbl_dir = "data/sonar_frames/yolo_labels_auto"

dst_root = "data/yolo_sonar"

os.makedirs(os.path.join(dst_root, "images/train"), exist_ok=True)
os.makedirs(os.path.join(dst_root, "images/val"), exist_ok=True)
os.makedirs(os.path.join(dst_root, "images/test"), exist_ok=True)
os.makedirs(os.path.join(dst_root, "labels/train"), exist_ok=True)
os.makedirs(os.path.join(dst_root, "labels/val"), exist_ok=True)
os.makedirs(os.path.join(dst_root, "labels/test"), exist_ok=True)

frames = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
n = len(frames)
train_end = int(0.6 * n)
val_end = int(0.8 * n)

for i, fname in enumerate(frames):
    src_img = os.path.join(img_dir, fname)
    src_lbl = os.path.join(lbl_dir, fname.replace(".png", ".txt"))

    if i < train_end:
        split = "train"
    elif i < val_end:
        split = "val"
    else:
        split = "test"

    dst_img = os.path.join(dst_root, "images", split, fname)
    shutil.copy(src_img, dst_img)

    if os.path.exists(src_lbl):
        dst_lbl = os.path.join(dst_root, "labels", split, fname.replace(".png", ".txt"))
        shutil.copy(src_lbl, dst_lbl)

print("Split complete.")
