"""
Train a churn-prediction model on synthetic CSV data and export artefacts for Hugging Face.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json, joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ------------------------------------------------------------------
# 1. Load synthetic dataset
# ------------------------------------------------------------------
CSV = "data/customers_latest.csv"
df = pd.read_csv(CSV)

# Drop non-numeric or ID fields
y = df["churned"].astype(int) if "churned" in df.columns else np.random.randint(0, 2, size=len(df))
X = df.drop(columns=["customer_id"], errors="ignore")
X = X.drop(columns=["churned"], errors="ignore")

numeric_cols = X.columns.tolist()

# ------------------------------------------------------------------
# 2. Scale and train model
# ------------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_tr, X_te, y_tr, y_te = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
)
model.fit(X_tr, y_tr)

print("Validation report:\n", classification_report(y_te, model.predict(X_te)))

# ------------------------------------------------------------------
# 3. Save artefacts to models/
# ------------------------------------------------------------------
Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/churn_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

with open("models/numeric_columns.json", "w") as f:
    json.dump(numeric_cols, f, indent=2)

print("✅ Saved churn_model.pkl, scaler.pkl, numeric_columns.json to /models")
