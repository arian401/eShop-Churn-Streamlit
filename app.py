# app.py
import os
os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"      # disable telemetry

import streamlit as st
import requests, pandas as pd

API_URL = "https://arian401-eshop-churnpredictor.hf.space/predict/"

st.set_page_config(page_title="eShop Churn Lab", page_icon="🛒")
st.title("🛒 Customer Churn Predictor")
st.write("Enter a single customer **or** upload a CSV to score many customers.")

# ─────────────────────────── Single-customer form ──────────────────────────
with st.form("single_customer"):
    st.subheader("Manual input")
    tenure   = st.number_input("Tenure (months)", 0.0, value=10.0)
    spent    = st.number_input("Total lifetime spend", 0.0, value=500.0)
    freq     = st.number_input("Avg purchases / month", 0.0, value=2.0)
    aov      = st.number_input("Avg order value", 0.0, value=60.0)
    recency  = st.number_input("Days since last purchase", 0.0, value=30.0)
    returns  = st.slider("Return / refund rate", 0.0, 0.5, 0.05, 0.01)
    tickets  = st.number_input("Complaint count", 0, value=0, step=1)
    loyalty  = st.selectbox("Loyalty-programme member", [0, 1])
    views    = st.number_input("Page views (30 d)", 0, value=20, step=1)
    abandon  = st.slider("Cart-abandon rate", 0.0, 1.0, 0.30, 0.01)
    coupons  = st.number_input("Discount codes used (6 m)", 0, value=1, step=1)

    if st.form_submit_button("Predict ⏩"):
        payload = {
            "tenure_months": tenure,
            "total_spent": spent,
            "avg_purchase_frequency": freq,
            "avg_order_value": aov,
            "days_since_last_purchase": recency,
            "percentage_returns": returns,
            "complaint_count": tickets,
            "loyalty_program_member": loyalty,
            "page_views_last_30d": views,
            "cart_abandon_rate": abandon,
            "discount_used_last_6m": coupons
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=15)
            if r.status_code != 200:
                st.warning(f"API error {r.status_code}: {r.text}")
            else:
                pred = r.json().get("churn_prediction")
                if pred == 1:
                    st.error("⚠️ High churn risk – suggest retention offer.")
                else:
                    st.success("✅ Low churn risk – customer likely to stay.")
        except Exception as e:
            st.warning(f"Request failed: {e}")

# ─────────────────────────── Batch CSV upload ──────────────────────────────
st.subheader("Batch scoring (CSV)")
csv = st.file_uploader("Upload CSV with the same 11 columns", type="csv")

if csv and st.button("Score batch"):
    df = pd.read_csv(csv)
    st.write("Preview:", df.head())

    preds = []
    progress = st.progress(0, text="Scoring customers...")
    for i, row in df.iterrows():
        r = requests.post(API_URL, json=row.to_dict())
        preds.append(r.json().get("churn_prediction", None))
        progress.progress((i + 1) / len(df))
    df["churn_prediction"] = preds
    progress.empty()

    st.success("Batch scoring complete")
    st.dataframe(df)
    st.download_button("Download results as CSV",
                       df.to_csv(index=False).encode(),
                       file_name="churn_predictions.csv")
