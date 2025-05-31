# train_and_export.py
"""
Connect to an e-shop PostgreSQL database, extract customer records,
train a churn-prediction model (11 features, no preferred_device),
and export artefacts for Hugging Face Spaces.
"""

# --------------------------------------------------------------
# 1. Connect to your database, get the dataset
# --------------------------------------------------------------
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pathlib import Path
import json, joblib

# 🔒 Replace with real credentials
username = "your_username"
password = "your_password"
host     = "localhost"
port     = "5432"
database = "your_database"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

query = """
SELECT
    customer_id,
    tenure_months,
    total_spent,
    avg_purchase_frequency,
    avg_order_value,
    days_since_last_purchase,
    percentage_returns,
    complaint_count,
    loyalty_program_member,
    page_views_last_30d,
    cart_abandon_rate,
    discount_used_last_6m,
    churned
FROM customer_data;
"""

df = pd.read_sql(query, engine)

# --------------------------------------------------------------
# 2. Pre-process
# --------------------------------------------------------------
y = df["churned"].astype(int)
X = df.drop(columns=["customer_id", "churned"])   # 11 numeric features
numeric_cols = X.columns.tolist()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------------------
# 3. Train model
# --------------------------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

X_tr, X_te, y_tr, y_te = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_tr, y_tr)

print("Model report:\n", classification_report(y_te, model.predict(X_te)))

# --------------------------------------------------------------
# 4. Save artefacts
# --------------------------------------------------------------
Path("models").mkdir(exist_ok=True)

joblib.dump(model,  "models/churn_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

with open("models/numeric_columns.json", "w") as f:
    json.dump(numeric_cols, f, indent=2)

print("✅ Artefacts saved to /models  (churn_model.pkl, scaler.pkl, numeric_columns.json)")
