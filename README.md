---
title: Customer Churn Prediction API
emoji: 🔁
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🛒 Customer Churn Prediction System

A full-stack machine learning project that predicts e-commerce customer churn, powered by:

- ✅ FastAPI + Hugging Face Spaces (for real-time scoring)
- ✅ Streamlit (for interactive frontend)
- ✅ GitHub Actions (for scheduled batch predictions)
- ✅ Flask (for local backend simulation)
- ✅ Email alerts (for retention campaigns)

## 🌐 Live Demos

- **API**: https://arian401-eshop-churnpredictor.hf.space/predict/
- **Streamlit UI**: https://eshop-churn.streamlit.app/
- **GitHub Repo**: https://github.com/arian401/eShop-Churn-Streamlit

---

## 🔧 Project Structure

```
eShop-Churn-Streamlit/
├── app.py                 # Streamlit app (single + batch input)
├── batch_predict.py       # GitHub Actions batch prediction script
├── stub_backend.py        # Local simulation using Flask + SMTP
├── .env.example           # Template for local credentials
├── data/
│   └── customers_latest.csv
├── reports/
│   └── (output CSVs from GitHub workflow)
├── models/
│   └── churn_model.pkl, scaler.pkl, numeric_columns.json
├── .github/workflows/
│   └── batch.yml          # Scheduled job (daily or weekly)
```

---

## 🧪 Local Testing (Flask Backend)

You can simulate a customer login event and trigger a real API call + email:

```bash
cd /path/to/API-Backend
export FLASK_APP=stub_backend
flask run
```

Then in another terminal:

```bash
curl -X POST http://127.0.0.1:5000/simulate-login
```

Expected output: `{"action":"High risk; Email sent"}` or `{"action":"Low risk; No action"}`  
Emails are sent to the address configured in `.env`.

---

## 🖥️ Streamlit Frontend

Supports:

- 📥 Manual entry for one customer
- 📤 CSV upload for batch predictions
- ✅ Hosted on Streamlit Cloud

---

## 🔁 GitHub Actions

This project includes a scheduled workflow that:

- Pulls the latest customer dataset
- Scores all rows using your HF API
- Saves a report of high-risk customers
- Emails the CSV to your marketing team

To configure your own email alerts, create GitHub repo secrets:

```
SMTP_USERNAME=youremail@gmail.com
SMTP_PASSWORD=your_app_password
```

---

## 🧠 Model Details

- **Features used (11)**: tenure, spend, frequency, recency, return rate, complaints, loyalty status, engagement, cart abandon rate, discount usage.
- **Model**: RandomForestClassifier
- **Scaler**: StandardScaler
- **Training script**: `train_and_export.py`
- **Deployment**: Docker runtime on Hugging Face Spaces

---

## 🔄 Weekly Retraining (optional)

Automate model refresh via:

- `train_and_export.py` script
- Push updated `.pkl` files to HF repo or GitHub (Render will auto-deploy)

---

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

For the Flask backend:

```bash
pip install Flask python-dotenv requests
flask run
```

---

## 📬 Contact

Created by **Amin Sokhanvar**  
Email: [am.s401@yahoo.com](mailto:am.s401@yahoo.com)

Portfolio: https://github.com/arian401
