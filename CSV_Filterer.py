# filter_csv.py

import pandas as pd
import argparse
import os

# Argument parsing
parser = argparse.ArgumentParser(description='Filter CSV files for emotion recognition')
parser.add_argument('filename', type=str, help='Full path to the input CSV file')
parser.add_argument('relative_path', type=str, help='Base path to remove from filename for output')
parser.add_argument('end_directory', type=str, help='Directory where filtered files will be saved')

args = parser.parse_args()

# Normalize paths
filename = os.path.normpath(args.filename)
relative_path = os.path.normpath(args.relative_path)
end_directory = os.path.normpath(args.end_directory)

# Load the dataset
df = pd.read_csv(filename)

# Step 1: Keep only relevant columns
keep_columns = []

for col in df.columns:
    if len(col) > 1 and col[1] in ['X', 'Y', 'Z']:  # 3D landmarks
        keep_columns.append(col)
    if col.lower() in [' pose_rx', ' pose_ry', ' pose_rz', ' pose_tx', ' pose_ty', ' pose_tz']:  # Head pose
        keep_columns.append(col)
    if col.startswith(' AU') and (col.endswith('_r') or col.endswith('_c')):  # Action Units
        keep_columns.append(col)

df_filtered = df[keep_columns].copy()

# Step 2: Extract emotion from filename
def extract_emotion(filename):
    parts = os.path.basename(filename).split('-')
    if len(parts) >= 3:
        return parts[2]
    return None

df_filtered['emotion'] = extract_emotion(filename)

# Step 3: Save cleaned data
output_filename = os.path.join(end_directory, filename.replace(relative_path, "").strip("\\/"))
os.makedirs(os.path.dirname(output_filename), exist_ok=True)
df_filtered.to_csv(output_filename, index=False)
print(f"Filtered dataset saved to {output_filename}")
