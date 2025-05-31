import cv2 
import numpy as np
import pandas as pd
import subprocess
import tempfile
import os
import joblib
from tensorflow.keras.models import load_model

# Load your scaler and model
scaler = joblib.load("scaler.pkl")
model = load_model("emotion_model.h5", compile=False)

# Emotion label map
emotion_labels = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']

# Get and clean expected feature names
EXPECTED_FEATURES = [f.strip() for f in scaler.get_feature_names_out().tolist()]
print(f"Scaler expects {len(EXPECTED_FEATURES)} features")

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    with tempfile.TemporaryDirectory() as tmpdir:
        frame_path = os.path.join(tmpdir, "frame.jpg")
        cv2.imwrite(frame_path, frame)
        
        # Run OpenFace FeatureExtraction
        output_prefix = os.path.join(tmpdir, "frame")
        result = subprocess.run([
            "OpenFace_2.2.0_win_x64/FeatureExtraction.exe",
            "-f", frame_path,
            "-out_dir", tmpdir,
            "-of", output_prefix,
            "-2Dfp", "-3Dfp", "-pose", "-aus",
            "-tracked"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output_csv = output_prefix + ".csv"
        
        if os.path.exists(output_csv):
            try:
                df = pd.read_csv(output_csv)
                
                # Clean all column names (remove leading/trailing spaces)
                df.columns = df.columns.str.strip()
                
                # Create a feature vector that matches the scaler's expectations
                feature_vector = np.zeros(len(EXPECTED_FEATURES))
                matched_indices = []
                
                for i, expected_feature in enumerate(EXPECTED_FEATURES):
                    if expected_feature in df.columns:
                        feature_vector[i] = df[expected_feature].values[0]
                        matched_indices.append(i)
                    # Try alternative naming conventions
                    elif expected_feature.replace('_', ' ') in df.columns:
                        feature_vector[i] = df[expected_feature.replace('_', ' ')].values[0]
                        matched_indices.append(i)
                    elif expected_feature.lower() in map(str.lower, df.columns):
                        matching_col = [col for col in df.columns if col.lower() == expected_feature.lower()][0]
                        feature_vector[i] = df[matching_col].values[0]
                        matched_indices.append(i)
                
                matched_count = len(matched_indices)
                print(f"Matched {matched_count} of {len(EXPECTED_FEATURES)} expected features")
                
                if matched_count == 0:
                    emotion = "No Features"
                else:
                    # Print first 5 matched features for debugging
                    print("Sample matched features:")
                    for i in matched_indices[:5]:
                        print(f"{EXPECTED_FEATURES[i]}: {feature_vector[i]}")
                    
                    # Print first 5 available columns for debugging
                    print("Sample available columns:", df.columns.tolist()[:5])
                    
                    # Scale features and predict
                    X_input = scaler.transform(feature_vector.reshape(1, -1))
                    y_pred = model.predict(X_input)
                    emotion = emotion_labels[np.argmax(y_pred[0])]
                    
            except Exception as e:
                print(f"Error processing features: {e}")
                print("Available columns:", df.columns.tolist())
                emotion = "Error"
        else:
            print("OpenFace output not found.")
            emotion = "No Output"

    # Display emotion on frame
    cv2.putText(frame, f'Emotion: {emotion}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Emotion Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()