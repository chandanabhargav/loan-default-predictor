
# 🚀 Loan Default Prediction API

A FastAPI-powered machine learning service for predicting loan default risk, trained on Lending Club data.  
Supports real-time predictions, monitoring, and integration with MLflow for model versioning.

---

## 📦 Features

| Feature                        | Description                                      |
|-------------------------------|--------------------------------------------------|
| 🧠 Model                      | XGBoost, trained on Lending Club loan data       |
| ⚙️ API                        | Built with FastAPI for real-time scoring         |
| 🔍 Monitoring                 | Logs prediction, confidence score, model version |
| 📦 Model Versioning           | Uses MLflow Registry to load production models   |
| 🧪 Sample Payload             | Included in `/docs` for easy testing             |
| 🛠️ Docker Support             | Lightweight containerized deployment             |
| 🏗️ Airflow                    | Scheduled batch inference                        |
                                 
---

## 🚀 Quick Start (Local)

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/loan-default-api.git
cd loan-default-api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn app:app --reload
```

### 4. Open Swagger UI

Go to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Sample Request

```json
{
  "loan_amnt": 12000,
  "funded_amnt": 12000,
  "term": " 36 months",
  "int_rate": 14.32,
  "emp_length": "10+ years",
  "home_ownership": "RENT",
  "annual_inc": 60000,
  "verification_status": "Verified",
  "purpose": "credit_card",
  "dti": 15.7,
  "delinq_2yrs": 0
}
```

---

## 📤 Sample Response

```json
{
  "default_probability": 0.71,
  "prediction": 1,
  "confidence_label": "High Risk",
  "model_version": "1.0.0"
}
```

---

## 🧠 Monitoring

| Field              | Logged           |
|-------------------|------------------|
| Timestamp          | ✅               |
| Input features     | ✅               |
| Prediction         | ✅               |
| Probability score  | ✅               |
| Risk label         | ✅               |
| Model version      | ✅               |

All logs are stored in `inference.log`.

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t loan-default-api .
```

### Run the Container

```bash
docker run -d -p 8000:8000 loan-default-api
```

Then visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 MLflow Integration

This project uses MLflow for **experiment tracking** and **model logging** during training.

- Metrics (e.g. AUC, F1)
- Parameters (e.g. model type, learning rate)

---

## 📁 Project Structure

```
.
├── app.py                    # FastAPI app
├── inference.log             # Logs predictions
├── requirements.txt
├── Dockerfile
└── xgboost_random_search.pkl # (or use MLflow registry)
```

---

## 🛡️ Health Check

```bash
GET /health
Response: {"status": "ok"}
```

---

## ✨ License

MIT — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Chandana**  
[https://github.com/chandanabhargav](https://github.com/chandanabhargav)

---

## 🏗️ Batch Scoring with Airflow

This project supports scheduled batch inference using Apache Airflow.  

### 📂 Structure

```
airflow_dags/
└── loan_default_dag.py    # DAG to run batch_predict.py
batch/
├── batch_predict.py       # Reads input CSV, scores, saves output
└── input/
    └── new_loans.csv      # Sample input data
```

### 🛠️ How It Works

1. Pulls daily loan applications (e.g., from `new_loans.csv` or S3)
2. Runs batch scoring using your trained model
3. Writes predictions to a CSV or target system
4. Scheduled via Airflow DAG

### 🧪 Run DAG Locally

1. Install Airflow (suggested in a virtualenv):
    ```bash
    pip install apache-airflow
    ```

2. Set up airflow directories:
    ```bash
    export AIRFLOW_HOME=~/airflow
    airflow db init
    ```

3. Copy `loan_default_dag.py` into `~/airflow/dags/`

4. Start the Airflow scheduler and web UI:
    ```bash
    airflow scheduler
    airflow webserver --port 8080
    ```

5. Visit the UI: [http://localhost:8080](http://localhost:8080)

6. Enable and trigger the DAG: `loan_default_batch_prediction`

---

## 📌 Example Batch Command

```bash
python batch/batch_predict.py
```

Outputs predictions to: `predictions.csv`

---

## 📅 Schedule

The DAG is configured to run **nightly**:
```python
schedule_interval="@daily"
start_date=datetime(2025, 1, 1)
```

Update to your desired schedule in `loan_default_dag.py`.