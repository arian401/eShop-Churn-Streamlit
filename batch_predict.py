"""
Fetch customer data, call the HF API, save a dated CSV with high-risk customers.
Meant to run locally *or* inside GitHub Actions.
"""
import datetime as dt
from pathlib import Path
import pandas as pd
import requests

# ── CONSTANTS ───────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
DATA_FILE  = BASE_DIR / "data" / "customers_latest.csv"
REPORT_DIR = BASE_DIR / "reports"
API_URL    = "https://arian401-eshop-churnpredictor.hf.space/predict/"

# ── 1.  Load the latest customer snapshot ───────────────────────
df = pd.read_csv(DATA_FILE)

# ── 2.  Score customers via the model API ───────────────────────
def predict(row):
    try:
        r = requests.post(API_URL, json=row.to_dict(), timeout=20)
        r.raise_for_status()
        return r.json().get("churn_prediction")
    except Exception as e:
        print(f"⚠️  API error for id={row.get('customer_id', 'NA')}: {e}")
        return None

df["churn_prediction"] = df.apply(predict, axis=1)

# ── 3.  Filter & save high-risk customers ───────────────────────
high_risk = df[df["churn_prediction"] == 1]

REPORT_DIR.mkdir(exist_ok=True)
today     = dt.date.today().isoformat()
outfile   = REPORT_DIR / f"high_risk_customers_{today}.csv"
high_risk.to_csv(outfile, index=False)

print(f"✅  Wrote {len(high_risk)} high-risk rows to {outfile.relative_to(BASE_DIR)}")
