# main.py
"""
FastAPI endpoint for customer-churn prediction.
Expects 11 numeric features (preferred_device was removed).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, json, pandas as pd

# --------------------------------------------------------------
# Load artefacts
# --------------------------------------------------------------
model   = joblib.load("models/churn_model.pkl")
scaler  = joblib.load("models/scaler.pkl")
numeric = json.load(open("models/numeric_columns.json"))  # 11 numeric columns

# --------------------------------------------------------------
# FastAPI app
# --------------------------------------------------------------
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts churn for e-shop customers using 11 behavioural features",
    version="2.0"
)

# --------------------------------------------------------------
# Input schema
# --------------------------------------------------------------
class CustomerData(BaseModel):
    tenure_months:             float
    total_spent:               float
    avg_purchase_frequency:    float
    avg_order_value:           float
    days_since_last_purchase:  float
    percentage_returns:        float
    complaint_count:           int
    loyalty_program_member:    int   # 0 = No, 1 = Yes
    page_views_last_30d:       int
    cart_abandon_rate:         float
    discount_used_last_6m:     int

# --------------------------------------------------------------
# Prediction endpoint
# --------------------------------------------------------------
@app.post("/predict/")
def predict_churn(data: CustomerData):
    try:
        # 1. to DataFrame
        df = pd.DataFrame([data.dict()])

        # 2. Ensure correct column order
        df = df[numeric]

        # 3. Scale numeric features
        df[numeric] = scaler.transform(df[numeric])

        # 4. Predict
        pred = int(model.predict(df)[0])
        return {"churn_prediction": pred}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
