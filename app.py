MODEL_VERSION = '1.0.0'

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    filename='inference.log',
    level=logging.INFO,   
    format="%(asctime)s %(levelname)s %(message)s"    
)

# Load model and columns
model = joblib.load("xgboost_random_search.pkl")

# Define expected input features (based on training data)
expected_columns = model.feature_names_in_.tolist()

# Pydantic schema for incoming requests
class LoanInput(BaseModel):
    loan_amnt: float
    funded_amnt: float
    term: str
    int_rate: float
    emp_length: str
    home_ownership: str
    annual_inc: float
    verification_status: str
    purpose: str
    dti: float
    delinq_2yrs: int

# Initialize FastAPI app
app = FastAPI()

def log_prediction(input_data, prediction, proba, label, version):
    logging.info(
       f'Prediction: {prediction} | Probability: {proba} | '
       f'Input: {input_data} | {label} | V{version}'
    )


# Root endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Prediction endpoint
@app.post("/predict")
def predict_default(data: LoanInput):
    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # Apply the same transformations as training
    df = pd.get_dummies(df, drop_first=True)
    df.columns = (
        df.columns
        .str.replace('<', 'less than', regex=False)
        .str.replace('+', 'plus', regex=False)
        .str.replace(' ', '_', regex=False)
        .str.replace('__', '_', regex=False)
    )

    # Align columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0  # Add missing columns
    df = df[expected_columns]  # Ensure correct order

    # Predict
    proba = model.predict_proba(df)[:, 1][0]
    prediction = int(proba >= 0.5)

    # Add human-readable confidence label
    if proba >= 0.8:
        label = "Very High Risk"
    elif proba >= 0.6:
        label = "High Risk"
    elif proba >= 0.4:
        label = "Moderate Risk"
    else:
        label = "Low Risk"

    log_prediction(
        data.dict(),
        prediction,
        proba,
        label,
        MODEL_VERSION
    )

    return {
        "default_probability": round(float(proba), 2),
        "prediction": prediction,
        "confidence_label": label,
        "model_version": MODEL_VERSION
    }