from __future__ import annotations

import json
import os
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, label_binarize

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False


# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "model_outputs_eda")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_SEED = 42
DATASET_SIZE = 1250
TARGET_COLUMN = "Risk_Level"

FEATURE_COLUMNS = [
    "Age",
    "Age_Above_50",
    "Breast_Lump",
    "Nipple_Discharge",
    "Skin_Changes",
    "Nipple_Retraction",
    "Redness_Scaling",
    "Breast_Pain",
    "Swollen_Lymph_Nodes",
    "Family_History",
    "Never_Pregnant",
    "Late_Menopause",
    "BMI_Risk",
    "Alcohol_Risk",
    "Smoker",
    "Low_Physical_Activity",
    "Prior_Screening",
    "Prior_Benign_Breast_Disease",
    "Self_Exam_Irregularity",
    "Symptom_Count",
    "Risk_Factor_Count",
]

NOISY_COLUMNS_TO_DROP = [
    "Symptom_Duration_Weeks",
    "Lifestyle_Risk",
]


# ============================================================
# DATA GENERATION
# ============================================================
def calculate_risk_score(row: Dict[str, int]) -> int:
    score = 0

    if row["Age"] > 50:
        score += 2
    if row["Age"] > 60:
        score += 1

    score += row["Breast_Lump"] * 3
    score += row["Nipple_Discharge"] * 2
    score += row["Skin_Changes"] * 2
    score += row["Nipple_Retraction"] * 2
    score += row["Redness_Scaling"] * 1
    score += row["Breast_Pain"] * 1
    score += row["Swollen_Lymph_Nodes"] * 2
    score += row["Self_Exam_Irregularity"] * 2

    score += row["Family_History"] * 2
    score += row["Never_Pregnant"] * 1
    score += row["Late_Menopause"] * 1
    score += row["BMI_Risk"] * 1
    score += row["Alcohol_Risk"] * 1
    score += row["Smoker"] * 1
    score += row["Low_Physical_Activity"] * 1
    score += row["Prior_Benign_Breast_Disease"] * 1

    if row["Prior_Screening"] == 0:
        score += 1

    return score


def get_risk_level(score: int) -> str:
    if score <= 6:
        return "Low"
    elif score <= 11:
        return "Medium"
    return "High"


def generate_synthetic_dataset(n: int = DATASET_SIZE, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    records: List[Dict[str, int]] = []

    for _ in range(n):
        age = int(rng.integers(20, 81))
        age_above_50 = int(age > 50)

        family_history = rng.binomial(1, 0.18 if age < 40 else 0.25)
        never_pregnant = rng.binomial(1, 0.24 if age < 35 else 0.12)
        late_menopause = int(age >= 55 and rng.random() < 0.35)
        bmi_risk = rng.binomial(1, 0.26 if age < 45 else 0.43)
        alcohol_risk = rng.binomial(1, 0.14)
        smoker = rng.binomial(1, 0.07)
        low_physical_activity = rng.binomial(1, 0.34)
        prior_screening = rng.binomial(1, 0.28 if age < 40 else 0.50)
        prior_benign_breast_disease = rng.binomial(1, 0.07 if age < 45 else 0.16)

        latent_risk = (
            age_above_50 * 1.8
            + (age > 60) * 1.0
            + family_history * 1.6
            + never_pregnant * 0.7
            + late_menopause * 0.8
            + bmi_risk * 0.7
            + alcohol_risk * 0.4
            + smoker * 0.35
            + low_physical_activity * 0.3
            + prior_benign_breast_disease * 0.9
            + (1 - prior_screening) * 0.35
        )

        breast_lump = rng.binomial(1, min(0.04 + 0.14 * latent_risk, 0.96))
        nipple_discharge = rng.binomial(1, min(0.03 + 0.09 * latent_risk, 0.82))
        skin_changes = rng.binomial(1, min(0.03 + 0.10 * latent_risk, 0.84))
        nipple_retraction = rng.binomial(1, min(0.02 + 0.08 * latent_risk, 0.72))
        redness_scaling = rng.binomial(1, min(0.02 + 0.06 * latent_risk, 0.74))
        breast_pain = rng.binomial(1, min(0.05 + 0.05 * latent_risk, 0.70))
        swollen_lymph_nodes = rng.binomial(1, min(0.01 + 0.07 * latent_risk, 0.62))
        self_exam_irregularity = rng.binomial(
            1,
            min(0.05 + 0.08 * latent_risk + 0.14 * breast_lump + 0.05 * skin_changes, 0.93),
        )

        symptom_duration_weeks = int(
            np.clip(
                rng.normal(
                    loc=2.0 + latent_risk * 1.2 + breast_lump * 1.3 + skin_changes * 0.8,
                    scale=1.4,
                ),
                0,
                12,
            )
        )

        lifestyle_risk = int(any([bmi_risk, alcohol_risk, smoker, low_physical_activity]))

        symptom_count = int(
            breast_lump
            + nipple_discharge
            + skin_changes
            + nipple_retraction
            + redness_scaling
            + breast_pain
            + swollen_lymph_nodes
            + self_exam_irregularity
        )

        risk_factor_count = int(
            age_above_50
            + family_history
            + never_pregnant
            + late_menopause
            + bmi_risk
            + alcohol_risk
            + smoker
            + low_physical_activity
            + prior_benign_breast_disease
            + (1 - prior_screening)
        )

        row = {
            "Age": age,
            "Age_Above_50": age_above_50,
            "Breast_Lump": breast_lump,
            "Nipple_Discharge": nipple_discharge,
            "Skin_Changes": skin_changes,
            "Nipple_Retraction": nipple_retraction,
            "Redness_Scaling": redness_scaling,
            "Breast_Pain": breast_pain,
            "Swollen_Lymph_Nodes": swollen_lymph_nodes,
            "Family_History": family_history,
            "Never_Pregnant": never_pregnant,
            "Late_Menopause": late_menopause,
            "BMI_Risk": bmi_risk,
            "Alcohol_Risk": alcohol_risk,
            "Smoker": smoker,
            "Low_Physical_Activity": low_physical_activity,
            "Lifestyle_Risk": lifestyle_risk,
            "Prior_Screening": prior_screening,
            "Prior_Benign_Breast_Disease": prior_benign_breast_disease,
            "Self_Exam_Irregularity": self_exam_irregularity,
            "Symptom_Duration_Weeks": symptom_duration_weeks,
            "Symptom_Count": symptom_count,
            "Risk_Factor_Count": risk_factor_count,
        }

        risk_score = calculate_risk_score(row)
        noisy_score = risk_score + rng.choice([-1, 0, 1], p=[0.01, 0.97, 0.02])
        risk_level = get_risk_level(noisy_score)

        row["Risk_Score"] = risk_score
        row["Risk_Score_Noisy"] = noisy_score
        row["Risk_Level"] = risk_level
        records.append(row)

    return pd.DataFrame(records)


# ============================================================
# PREPROCESSING
# ============================================================
def drop_noisy_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [col for col in NOISY_COLUMNS_TO_DROP if col in df.columns]
    return df.drop(columns=cols, errors="ignore")


# ============================================================
# EDA PLOTS
# ============================================================
def generate_eda_plots(df: pd.DataFrame):
    # Univariate
    plt.figure(figsize=(8, 5))
    df["Age"].hist(bins=15)
    plt.title("Univariate Analysis: Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    uni_path = os.path.join(OUTPUT_DIR, "univariate_age_distribution.png")
    plt.tight_layout()
    plt.savefig(uni_path, dpi=150)
    plt.close()

    # Bivariate
    mean_symptoms = df.groupby("Risk_Level")["Symptom_Count"].mean().reindex(["Low", "Medium", "High"])
    plt.figure(figsize=(8, 5))
    mean_symptoms.plot(kind="bar")
    plt.title("Bivariate Analysis: Mean Symptom Count by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Mean Symptom Count")
    plt.xticks(rotation=0)
    bi_path = os.path.join(OUTPUT_DIR, "bivariate_symptom_count_by_risk.png")
    plt.tight_layout()
    plt.savefig(bi_path, dpi=150)
    plt.close()

    # Correlation Heatmap
    corr_cols = FEATURE_COLUMNS + ["Risk_Score"]
    corr = df[corr_cols].corr(numeric_only=True)

    plt.figure(figsize=(12, 10))
    plt.imshow(corr, aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index)
    plt.title("Correlation Heatmap")
    heatmap_path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(heatmap_path, dpi=150)
    plt.close()

    corr.to_csv(os.path.join(OUTPUT_DIR, "correlation_matrix.csv"))

    return uni_path, bi_path, heatmap_path


# ============================================================
# MODEL EVALUATION
# ============================================================
def evaluate_one_model(model_name, model, X_train, X_test, y_train, y_test, encoder):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        target_names=list(encoder.classes_),
        digits=4,
        zero_division=0,
    )

    y_test_bin = label_binarize(y_test, classes=np.arange(len(encoder.classes_)))
    roc_auc = roc_auc_score(y_test_bin, y_proba, multi_class="ovr")

    print("\n" + "=" * 80)
    print(f"{model_name} RESULTS")
    print("=" * 80)
    print(f"Accuracy score: {accuracy:.4f}")
    print("confusion_matrix:")
    print(conf)
    print("\nclassification_report")
    print(report)
    print(f"roc_auc_score: {roc_auc:.6f}")

    return {
        "model": model,
        "accuracy": accuracy,
        "confusion_matrix": conf,
        "classification_report": report,
        "roc_auc_score": roc_auc,
    }


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 80)
    print("BREAST CANCER SCREENING MODEL WITH EDA + MODEL COMPARISON")
    print("=" * 80)

    df = generate_synthetic_dataset(n=DATASET_SIZE, seed=RANDOM_SEED)
    df_model = drop_noisy_columns(df)

    print(f"\nDataset shape: {df.shape}")
    print("\nRisk level distribution:")
    print(df["Risk_Level"].value_counts())

    uni_path, bi_path, heatmap_path = generate_eda_plots(df)
    print("\nEDA plots saved:")
    print(uni_path)
    print(bi_path)
    print(heatmap_path)

    X = df_model[FEATURE_COLUMNS].copy()
    y_raw = df_model[TARGET_COLUMN].copy()

    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_SEED, stratify=y
    )

    results = {}

    rf_model = RandomForestClassifier(
        n_estimators=400,
        max_depth=14,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features="sqrt",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    results["RandomForest"] = evaluate_one_model(
        "RandomForest", rf_model, X_train, X_test, y_train, y_test, encoder
    )

    if XGBOOST_AVAILABLE:
        xgb_model = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state=RANDOM_SEED,
            n_jobs=1,
        )
        results["XGBoost"] = evaluate_one_model(
            "XGBoost", xgb_model, X_train, X_test, y_train, y_test, encoder
        )
    else:
        print("\nXGBoost is not installed. Run: pip install xgboost")

    best_model_name = max(results, key=lambda k: results[k]["accuracy"])
    best_model = results[best_model_name]["model"]

    joblib.dump(best_model, os.path.join(OUTPUT_DIR, f"best_model_{best_model_name.lower()}.pkl"))
    joblib.dump(encoder, os.path.join(OUTPUT_DIR, "label_encoder.pkl"))
    joblib.dump(FEATURE_COLUMNS, os.path.join(OUTPUT_DIR, "feature_columns.pkl"))

    print("\n" + "=" * 80)
    print("BEST MODEL SUMMARY")
    print("=" * 80)
    print(f"Best model: {best_model_name}")
    print(f"Best accuracy: {results[best_model_name]['accuracy']:.4f}")

    summary = {
        "best_model": best_model_name,
        "accuracies": {k: round(float(v["accuracy"]), 4) for k, v in results.items()},
        "roc_auc_scores": {k: round(float(v["roc_auc_score"]), 6) for k, v in results.items()},
        "plots": {
            "univariate": uni_path,
            "bivariate": bi_path,
            "heatmap": heatmap_path,
        },
    }

    with open(os.path.join(OUTPUT_DIR, "summary_results.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # Open saved images automatically on Windows
    if os.name == "nt":
        try:
            os.startfile(uni_path)
            os.startfile(bi_path)
            os.startfile(heatmap_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()