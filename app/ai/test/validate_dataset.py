def validate_dataset(df):
    features = [
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
        #"Symptom_Count",
        #"Risk_Factor_Count"
    ]

    target = "Risk_Level"
    forbidden = ["Risk_Score", "Risk_Score_Noisy"]

    # 1. Check target column
    if target not in df.columns:
        raise ValueError(f"Missing target column: {target}")

    # 2. Check required features
    missing = [col for col in features if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    # 3. Check forbidden columns (data leakage)
    found_forbidden = [col for col in forbidden if col in df.columns]
    if found_forbidden:
        print(f"⚠️ Warning: Removing forbidden columns: {found_forbidden}")
        df = df.drop(columns=found_forbidden)

    # 4. Check for extra unexpected columns
    allowed = set(features + [target])
    extra = [col for col in df.columns if col not in allowed]
    if extra:
        print(f"⚠️ Warning: Unexpected columns will be ignored: {extra}")
        df = df.drop(columns=extra)

    # 5. Check missing values
    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset contains missing values")

    # 6. Validate binary columns (0/1)
    binary_cols = features[1:]  # skip Age
    for col in binary_cols:
        if not set(df[col].unique()).issubset({0, 1}):
            raise ValueError(f"Column {col} must contain only 0 or 1")

    # 7. Validate Age
    if df["Age"].min() < 0 or df["Age"].max() > 120:
        raise ValueError("Age values out of realistic range")

    print("✅ Dataset validation passed")
    return df