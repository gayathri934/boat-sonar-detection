import pandas as pd
import numpy as np

df = pd.read_csv("data/sonar_frames/centroid_track_smoothed.csv")

valid = df[(df["cx_smooth"] > 0) & (df["cy_smooth"] > 0)]

vari_x = np.var(valid["cx_smooth"])
vari_y = np.var(valid["cy_smooth"])
std_x = np.std(valid["cx_smooth"])
std_y = np.std(valid["cy_smooth"])

print("\n--- Localization Stability Metrics ---")
print(f"Centroid X variance: {vari_x:.2f}")
print(f"Centroid Y variance: {vari_y:.2f}")
print(f"Centroid X std-dev: {std_x:.2f} pixels")
print(f"Centroid Y std-dev: {std_y:.2f} pixels")

print("\nApprox detection region:")
print(f" X-range: {valid['cx_smooth'].min():.1f} to {valid['cx_smooth'].max():.1f}")
print(f" Y-range: {valid['cy_smooth'].min():.1f} to {valid['cy_smooth'].max():.1f}")
