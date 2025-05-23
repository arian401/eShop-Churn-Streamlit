# 🛒 eShop Churn Lab – Streamlit Front-End

A lightweight **Streamlit** interface that lets non-technical users interact with the e-shop churn prediction API.

- **Live API (FastAPI + Hugging Face):** https://arian401-eshop-churnpredictor.hf.space/docs
- **Why this UI?** No JSON, no Swagger—just a form or CSV upload and instant churn scores.

---

## ✨ Features
| Feature              | Description                                                  |
|----------------------|--------------------------------------------------------------|
| 🧑‍💻 Single-customer form | Enter 11 customer features and get a churn risk result        |
| 📄 Batch scoring     | Upload a CSV and get churn predictions with downloadable CSV |
| ✅ Simple deployment | Works locally or online on Streamlit Cloud                   |

---

## 🛠 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/arian401/eShop-Churn-Streamlit.git
cd eShop-Churn-Streamlit

# 2. Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 🗂 File Structure

| File/Folder              | Description                             |
|--------------------------|-----------------------------------------|
| `app.py`                 | Streamlit UI code                       |
| `requirements.txt`       | Lists `streamlit`, `requests`, `pandas` |
| `.streamlit/config.toml` | Disables telemetry to avoid HF crash    |
| `README.md`              | You’re reading it                       |

---

## 📑 CSV Format for Batch Scoring

CSV must include these columns:

```
tenure_months,total_spent,avg_purchase_frequency,avg_order_value,
days_since_last_purchase,percentage_returns,complaint_count,
loyalty_program_member,page_views_last_30d,cart_abandon_rate,
discount_used_last_6m
```

Sample row:

```
12,350.5,3.2,58.4,45,0.04,1,1,30,0.25,2
```

---

## 🌐 Online Deployment

1. **Streamlit Cloud:**  
   Deploy from this GitHub repo in seconds.

2. **Hugging Face Spaces:**  
   Create a new Space (SDK = Streamlit), upload the same files, or sync with GitHub.

Both will call your existing FastAPI backend on HF.

---

## 📬 Contact

For questions or ideas, reach out via GitHub Issues or connect on [LinkedIn](https://www.linkedin.com/in/your-profile).

---

© 2025 Arian401 – for educational & portfolio use only
