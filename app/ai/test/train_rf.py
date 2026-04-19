import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

from validate_dataset import validate_dataset

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
data_path = os.path.join(BASE_DIR, "data.csv")

df = pd.read_csv(data_path)

df = validate_dataset(df)

print(df.columns.tolist())

# Encode target
encoder = LabelEncoder()
y = encoder.fit_transform(df['Risk_Level'])

# Features
X = df #.drop(['Risk_Score', 'Risk_Score_Noisy', 'Risk_Level'], axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)
rf.fit(X_train, y_train)

# Save artifacts
joblib.dump(rf, os.path.join(BASE_DIR, "rf_model.pkl"))
joblib.dump(list(X.columns), os.path.join(BASE_DIR, "features.pkl"))
joblib.dump(encoder, os.path.join(BASE_DIR, "label_encoder.pkl"))

print("Model, features, and encoder saved successfully.")