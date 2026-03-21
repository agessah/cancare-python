def validate_dataset(df):
    REQUIRED_FEATURES = [
        "Age", "Breast_Lump", "Nipple_Discharge", "Skin_Changes",
        "Nipple_Retraction", "Redness_Scaling", "Family_History",
        "Age_Above_50", "Never_Pregnant", "Late_Menopause",
        "Lifestyle_Risk"
    ]

    TARGET = "Risk_Level"
    FORBIDDEN = ["Risk_Score"]

    # 1. Check target column
    if TARGET not in df.columns:
        raise ValueError(f"Missing target column: {TARGET}")

    # 2. Check required features
    missing = [col for col in REQUIRED_FEATURES if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    # 3. Check forbidden columns (data leakage)
    found_forbidden = [col for col in FORBIDDEN if col in df.columns]
    if found_forbidden:
        print(f"⚠️ Warning: Removing forbidden columns: {found_forbidden}")
        df = df.drop(columns=found_forbidden)

    # 4. Check for extra unexpected columns
    allowed = set(REQUIRED_FEATURES + [TARGET])
    extra = [col for col in df.columns if col not in allowed]
    if extra:
        print(f"⚠️ Warning: Unexpected columns will be ignored: {extra}")
        df = df.drop(columns=extra)

    # 5. Check missing values
    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset contains missing values")

    # 6. Validate binary columns (0/1)
    binary_cols = REQUIRED_FEATURES[1:]  # skip Age
    for col in binary_cols:
        if not set(df[col].unique()).issubset({0, 1}):
            raise ValueError(f"Column {col} must contain only 0 or 1")

    # 7. Validate Age
    if df["Age"].min() < 0 or df["Age"].max() > 120:
        raise ValueError("Age values out of realistic range")

    print("✅ Dataset validation passed")
    return df