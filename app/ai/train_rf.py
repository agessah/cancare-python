import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "data.csv")
#df = pd.read_excel(data_path)
df = pd.read_csv(data_path)

# Features & target
X = df.drop(['Risk_Score', 'Risk_Level'], axis=1)
y = LabelEncoder().fit_transform(df['Risk_Level'])  # Low=0, Medium=1, High=2

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

# Save model and feature names
model_path = os.path.join(BASE_DIR, "rf_model.pkl")
joblib.dump(rf, model_path)
features_path = os.path.join(BASE_DIR, "features.pkl")
joblib.dump(list(X.columns), features_path)

print("Model trained and saved successfully.")