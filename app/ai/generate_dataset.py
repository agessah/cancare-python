import pandas as pd
import numpy as np

np.random.seed(42)

def calculate_risk_score(row):
    score = 0

    # Age factor
    if row["Age"] > 50:
        score += 2

    # Symptoms
    score += row["Breast_Lump"] * 3
    score += row["Nipple_Discharge"] * 2
    score += row["Skin_Changes"] * 2
    score += row["Nipple_Retraction"] * 2
    score += row["Redness_Scaling"] * 1

    # History
    score += row["Family_History"] * 2

    # Reproductive factors
    score += row["Never_Pregnant"] * 1
    score += row["Late_Menopause"] * 1

    # Lifestyle
    score += row["Lifestyle_Risk"] * 2

    return score


def get_risk_level(score):
    if score <= 4:
        return "Low"
    elif score <= 8:
        return "Medium"
    else:
        return "High"


def generate_data(n=1000):
    data = []

    for _ in range(n):
        age = np.random.randint(20, 80)

        row = {
            "Age": age,
            "Breast_Lump": np.random.binomial(1, 0.3),
            "Nipple_Discharge": np.random.binomial(1, 0.25),
            "Skin_Changes": np.random.binomial(1, 0.3),
            "Nipple_Retraction": np.random.binomial(1, 0.2),
            "Redness_Scaling": np.random.binomial(1, 0.3),
            "Family_History": np.random.binomial(1, 0.2),
            "Age_Above_50": 1 if age > 50 else 0,
            "Never_Pregnant": np.random.binomial(1, 0.3),
            "Late_Menopause": np.random.binomial(1, 0.25),
            "Lifestyle_Risk": np.random.binomial(1, 0.4),
        }

        # Compute score
        score = calculate_risk_score(row)
        level = get_risk_level(score)

        row["Risk_Score"] = score
        row["Risk_Level"] = level

        data.append(row)

    return pd.DataFrame(data)


# Generate dataset
df = generate_data(1000)

# Save
df.to_csv("data.csv", index=False)

print("Dataset generated successfully!")
print(df.head())