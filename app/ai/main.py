import os
import numpy as np
import joblib
import shap
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load artifacts
rf = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "features.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))

# SHAP explainer (initialize once)
explainer = shap.TreeExplainer(rf)

# App
app = FastAPI(title="Breast Cancer Risk Prediction API")

# -------------------------
# Input Schema (validated)
# -------------------------
class InputData(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    Age_Above_50: int = Field(..., ge=0, le=1)
    Breast_Lump: int = Field(..., ge=0, le=1)
    Nipple_Discharge: int = Field(..., ge=0, le=1)
    Skin_Changes: int = Field(..., ge=0, le=1)
    Nipple_Retraction: int = Field(..., ge=0, le=1)
    Redness_Scaling: int = Field(..., ge=0, le=1)
    Breast_Pain: int = Field(..., ge=0, le=1)
    Swollen_Lymph_Nodes: int = Field(..., ge=0, le=1)
    Family_History: int = Field(..., ge=0, le=1)
    Never_Pregnant: int = Field(..., ge=0, le=1)
    Late_Menopause: int = Field(..., ge=0, le=1)
    BMI_Risk: int = Field(..., ge=0, le=1)
    Alcohol_Risk: int = Field(..., ge=0, le=1)
    Smoker: int = Field(..., ge=0, le=1)
    Low_Physical_Activity: int = Field(..., ge=0, le=1)
    Prior_Screening: int = Field(..., ge=0, le=1)
    Prior_Benign_Breast_Disease: int = Field(..., ge=0, le=1)
    Self_Exam_Irregularity: int = Field(..., ge=0, le=1)

    Symptom_Count: int = Field(..., ge=0, le=10)
    Risk_Factor_Count: int = Field(..., ge=0, le=10)


# -------------------------
# Helper: Build input array
# -------------------------
def build_input_array(data: InputData):
    return np.array([[
        data.Age,
        data.Age_Above_50,
        data.Breast_Lump,
        data.Nipple_Discharge,
        data.Skin_Changes,
        data.Nipple_Retraction,
        data.Redness_Scaling,
        data.Breast_Pain,
        data.Swollen_Lymph_Nodes,
        data.Family_History,
        data.Never_Pregnant,
        data.Late_Menopause,
        data.BMI_Risk,
        data.Alcohol_Risk,
        data.Smoker,
        data.Low_Physical_Activity,
        data.Prior_Screening,
        data.Prior_Benign_Breast_Disease,
        data.Self_Exam_Irregularity,
    ]], dtype=float)

# -------------------------
# Helper: SHAP extraction
# -------------------------
def get_contributions(shap_values, pred_class):
    if isinstance(shap_values, list):
        contributions = shap_values[int(pred_class)][0]
    elif hasattr(shap_values, "shape") and len(shap_values.shape) == 3:
        contributions = shap_values[0, int(pred_class), :]
    else:
        contributions = shap_values[0]

    return np.array(contributions).flatten()

# -------------------------
# Helper: Top features
# -------------------------
def get_top_features(contributions):
    top_indices = np.argsort(np.abs(contributions))[-5:]

    return [
        {
            "feature": feature_names[int(i)],
            "impact": float(contributions[int(i)])
        }
        for i in reversed(top_indices)
    ]

# -------------------------
# Helper: Risk interpretation
# -------------------------
def interpret_risk(prob):
    if prob > 0.75:
        return "High confidence ⚠️"
    elif prob > 0.5:
        return "Moderate confidence"
    else:
        return "Low confidence"

# -------------------------
# Prediction Endpoint
# -------------------------
@app.post("/predict")
def predict(data: InputData):
    try:
        arr = build_input_array(data)

        # Prediction
        pred_class = int(rf.predict(arr)[0])

        probs = rf.predict_proba(arr)[0]
        pred_prob = float(probs[pred_class])

        # Decode label
        risk_level = encoder.inverse_transform([pred_class])[0]

        # SHAP
        shap_values = explainer.shap_values(arr)
        contributions = get_contributions(shap_values, pred_class)

        # Top features
        top_features = get_top_features(contributions)

        return {
            "prediction_class": pred_class,
            "risk_level": risk_level,
            "probability": pred_prob,
            "confidence": interpret_risk(pred_prob),
            "top_features": top_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))