"""
Generate a weekly list of high-risk customers and save it in reports/.
Designed to run inside GitHub Actions (Linux) or locally.
"""
import datetime as dt
from pathlib import Path
import pandas as pd
import requests
import sys

# ── CONFIG ───────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent          # repo root
DATA_FILE  = BASE_DIR / "data" / "customers_latest.csv"
REPORT_DIR = BASE_DIR / "reports"
API_URL    = (
    "https://arian401-eshop-churnpredictor.hf.space/predict/"  # << your HF Space
)

# ── 1.  Load latest customer snapshot ────────────────────────────
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    sys.exit(f"❌  {DATA_FILE} not found – aborting")

# ── 2.  Score customers via the API ──────────────────────────────
def score(row: pd.Series) -> int | None:
    try:
        r = requests.post(API_URL, json=row.to_dict(), timeout=15)
        r.raise_for_status()
        return r.json().get("churn_prediction")        # 0 / 1 / None
    except Exception as exc:
        print(f"⚠️  API error for id={row.get('customer_id','?')}: {exc}")
        return None

print(f"⏳  Scoring {len(df)} customers …")
df["churn_prediction"] = df.apply(score, axis=1)

# ── 3.  Filter & save results ────────────────────────────────────
high_risk = df[df["churn_prediction"] == 1]
REPORT_DIR.mkdir(exist_ok=True)

today     = dt.date.today().isoformat()
outfile   = REPORT_DIR / f"high_risk_customers_{today}.csv"
high_risk.to_csv(outfile, index=False)

print(f"✅  Saved {len(high_risk)} high-risk rows to {outfile.relative_to(BASE_DIR)}")
