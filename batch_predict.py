"""
Fetch customer data, call the Hugging-Face API, save a CSV of high-risk customers.
Run locally or via GitHub Actions.
"""
import pandas as pd, requests, pathlib, datetime as dt

API_URL = "https://arian401-eshop-churnpredictor.hf.space/predict/"

# 1. ── FETCH DATA ───────────────────────────────────────────────
# Practise with a dummy CSV until you get a real DB.
df = pd.read_csv("data/customers_latest.csv")        # 11 feature columns

# 2. ── CALL API FOR EACH CUSTOMER ───────────────────────────────
preds = []
for _, row in df.iterrows():
    r = requests.post(API_URL, json=row.to_dict(), timeout=20)
    preds.append(r.json().get("churn_prediction", None))

df["churn_prediction"] = preds

# 3. ── FILTER HIGH-RISK & SAVE RESULTS ──────────────────────────
high_risk = df[df["churn_prediction"] == 1]
today = dt.date.today().isoformat()
pathlib.Path("reports").mkdir(exist_ok=True)
outfile = f"reports/high_risk_customers_{today}.csv"
high_risk.to_csv(outfile, index=False)
print(f"✅  Saved {len(high_risk)} high-risk rows to {outfile}")
