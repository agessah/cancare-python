import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import shap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model_path = os.path.join(BASE_DIR, "rf_model.pkl")
rf = joblib.load(model_path)
features_path = os.path.join(BASE_DIR, "features.pkl")
feature_names = joblib.load(features_path)

# SHAP explainer
explainer = shap.TreeExplainer(rf)

# FastAPI app
app = FastAPI(title="Breast Cancer Risk Prediction API")

# Input schema
class InputData(BaseModel):
    Age: int
    Breast_Lump: int
    Nipple_Discharge: int
    Skin_Changes: int
    Nipple_Retraction: int
    Redness_Scaling: int
    Family_History: int
    Age_Above_50: int
    Never_Pregnant: int
    Late_Menopause: int
    Lifestyle_Risk: int

@app.post("/predict")
def predict(data: InputData):
    try:
        arr = np.array([[
            data.Age,
            data.Breast_Lump,
            data.Nipple_Discharge,
            data.Skin_Changes,
            data.Nipple_Retraction,
            data.Redness_Scaling,
            data.Family_History,
            data.Age_Above_50,
            data.Never_Pregnant,
            data.Late_Menopause,
            data.Lifestyle_Risk
        ]])

        # Prediction
        pred_class = rf.predict(arr)[0]

        #probs = rf.predict_proba(arr)[0]
        #class_index = list(rf.classes_).index(pred_class)
        #pred_prob = probs[class_index]

        probs = rf.predict_proba(arr)[0]
        pred_prob = probs[int(pred_class)]

        # SHAP
        shap_values = explainer.shap_values(arr)

        if isinstance(shap_values, list):
            classes = list(rf.classes_)
            if pred_class in classes:
                idx = classes.index(pred_class)
                contributions = shap_values[idx][0]
            else:
                contributions = shap_values[0][0]
        else:
            contributions = shap_values[0]

        # Top features
        top_indices = np.argsort(np.abs(contributions))[-5:]
        top_features = [
            {"feature": feature_names[int(i)], "impact": float(contributions[int(i)])}
            for i in reversed(top_indices)
        ]

        # Decode label
        encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))
        risk_level = encoder.inverse_transform([pred_class])[0]

        return {
            "prediction_class": int(pred_class),
            "risk_level": risk_level,
            "probability": float(pred_prob),
            "top_features": top_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))