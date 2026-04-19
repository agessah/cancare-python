import os

import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def calculate_risk_score(row):
    score = 0

    # --- Age ---
    if row["Age"] > 60:
        score += 3
    elif row["Age"] > 50:
        score += 2

    # --- Symptoms ---
    score += row["Breast_Lump"] * 3
    score += row["Nipple_Discharge"] * 2
    score += row["Skin_Changes"] * 2
    score += row["Nipple_Retraction"] * 2
    score += row["Redness_Scaling"] * 1
    score += row["Breast_Pain"] * 0.5
    score += row["Swollen_Lymph_Nodes"] * 2
    score += row["Self_Exam_Irregularity"] * 2

    # --- Interaction ---
    if row["Breast_Lump"] and row["Swollen_Lymph_Nodes"]:
        score += 2

    # --- History ---
    score += row["Family_History"] * 3

    # --- Reproductive ---
    score += row["Never_Pregnant"] * 1
    score += row["Late_Menopause"] * 1

    # --- Lifestyle ---
    score += row["BMI_Risk"] * 1
    score += row["Alcohol_Risk"] * 1
    score += row["Smoker"] * 2
    score += row["Low_Physical_Activity"] * 1
    score += row["Prior_Benign_Breast_Disease"] * 2

    # --- Screening ---
    if row["Prior_Screening"] == 0 and row["Age"] > 50:
        score += 2

    return score


def get_risk_level(score):
    if score <= 6:
        return "Low"
    elif score <= 11:
        return "Medium"
    return "High"


def generate_data(size, seed):
    rng = np.random.default_rng(seed)
    data = []

    for _ in range(size):
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

        #lifestyle_risk = int(any([bmi_risk, alcohol_risk, smoker, low_physical_activity]))

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
            "Prior_Benign_Breast_Disease": prior_benign_breast_disease,
            "Prior_Screening": prior_screening,
            "Self_Exam_Irregularity": self_exam_irregularity,
            "Symptom_Count": symptom_count,
            "Risk_Factor_Count": risk_factor_count
        }

        # Compute score
        risk_score = calculate_risk_score(row)
        noisy_score = risk_score + rng.choice([-1, 0, 1], p=[0.01, 0.97, 0.02])
        risk_level = get_risk_level(noisy_score)

        row["Risk_Score"] = risk_score
        row["Risk_Score_Noisy"] = noisy_score
        row["Risk_Level"] = risk_level

        data.append(row)

    return pd.DataFrame(data)


# Generate dataset
df = generate_data(1250, 42)

# Save
data_path = os.path.join(BASE_DIR, "data.csv")
df.to_csv(data_path, index=False)

print("Dataset generated successfully!")
print(df.head())