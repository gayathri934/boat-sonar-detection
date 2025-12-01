import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_path = "data/sonar_frames/centroid_track.csv"
df = pd.read_csv(csv_path)

# Remove invalid detections
df = df[df["cx"] > 0]

# Harder smoothing
window = 21

df["cx_smooth"] = df["cx"].rolling(window, center=True, min_periods=1).median()
df["cy_smooth"] = df["cy"].rolling(window, center=True, min_periods=1).median()

# Optional: drop weird jumps
df["dx"] = df["cx_smooth"].diff().abs()
df["dy"] = df["cy_smooth"].diff().abs()

# Remove sudden jumps (likely noise)
df.loc[df["dx"] > 120, ["cx_smooth"]] = np.nan
df.loc[df["dy"] > 120, ["cy_smooth"]] = np.nan

df["cx_smooth"] = df["cx_smooth"].interpolate()
df["cy_smooth"] = df["cy_smooth"].interpolate()

df.to_csv("data/sonar_frames/centroid_track_smoothed.csv", index=False)

plt.figure()
plt.plot(df["cx_smooth"], df["cy_smooth"])
plt.title("Boat Smoothed Trajectory in Sonar")
plt.xlabel("X centroid")
plt.ylabel("Y centroid")
plt.gca().invert_yaxis()
plt.savefig("data/sonar_frames/trajectory_plot.png", dpi=300)
plt.close()

print("Smoothed track + refined plot saved.")
