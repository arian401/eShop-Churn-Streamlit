"""
Local stub backend that simulates an e-shop server.
• Builds synthetic customer data (11 numeric features)
• Sends it to your HF predictor API
• If churn risk == 1, sends a retention e-mail
"""

from flask import Flask, jsonify, Response
import requests, os, random, smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.utils import formataddr

# ── Load ENV ───────────────────────────────────────────
load_dotenv()                                      # looks for .env
EMAIL_USER  = os.getenv("EMAIL_USER")
EMAIL_PASS  = os.getenv("EMAIL_PASS")
API_URL     = os.getenv("CHURN_API")

# 🔸 fixed test address so you can confirm delivery
TEST_EMAIL  = os.getenv("TEST_EMAIL", "am.s401@yahoo.com")

# ── Flask app ─────────────────────────────────────────
app = Flask(__name__)

@app.post("/simulate-login")
def simulate_login():
    """Pretend the user just logged in – build features & score"""
    
    # 11-feature payload (same order as in your model)
    customer = {
        "tenure_months":          random.randint(1, 48),
        "total_spent":            round(random.uniform(100, 2000), 2),
        "avg_purchase_frequency": round(random.uniform(0.5, 5), 2),
        "avg_order_value":        round(random.uniform(20, 120), 2),
        "days_since_last_purchase": random.randint(1, 180),
        "percentage_returns":     round(random.uniform(0, 0.4), 2),
        "complaint_count":        random.randint(0, 3),
        "loyalty_program_member": random.choice([0, 1]),
        "page_views_last_30d":    random.randint(1, 60),
        "cart_abandon_rate":      round(random.uniform(0.1, 0.9), 2),
        "discount_used_last_6m":  random.randint(0, 5)
    }

    # ── Call the predictor API ─────────────────────────
    try:
        r = requests.post(API_URL, json=customer, timeout=15)
        r.raise_for_status()
        churn_flag = r.json()["churn_prediction"]
        print(f"✅ Predictor responded: {churn_flag}")
    except Exception as exc:
        return jsonify({"error": f"API error: {exc}"}), 500

    # ── Act on result ─────────────────────────────────
    if churn_flag == 1:
        try:
            send_email(TEST_EMAIL)
            message = "High risk; Email sent"
        except Exception as exc:
            return jsonify({"error": f"Email failed: {exc}"}), 500
    else:
        message = "Low risk; No action"

    # jsonify already returns UTF-8; some clients will escape the dash
    return jsonify({"action": message}), 200


# ── Helper: send SMTP mail ────────────────────────────
def send_email(recipient):
    smtp_server = "smtp.gmail.com"
    smtp_port   = 587

    sender_email = EMAIL_USER
    display_name = "E-Shop"

    msg = MIMEText(
        "Here’s 10 % off your next order. Code: WELCOME10"
    )
    msg["Subject"] = "🛒 A Little Gift to Welcome You Back!"
    msg["From"] = formataddr((display_name, sender_email))
    msg["To"]      = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, recipient, msg.as_string())

    print(f"📧  Email sent to {recipient}")


# ── Entry-point for `flask run` is still `app` ────────
