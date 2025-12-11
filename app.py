import os
import numpy as np
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from joblib import load
from dotenv import load_dotenv

load_dotenv()

# --- Configuration & Security ---

# 1. API Key Source: Tries to load the key from a secure environment variable.
#    If the env var is not set, it uses the hardcoded 'DEVELOPMENT_FALLBACK_KEY'.
#    NOTE: Replace 'DEVELOPMENT_FALLBACK_KEY' with a test key you generate 
#          if you don't want to use the full env var logic locally.
API_KEY = os.environ.get("API_SECRET_KEY", "DEVELOPMENT_FALLBACK_KEY_12345") 
print(API_KEY)

# Define where FastAPI should look for the key: a header named 'X-API-Key'
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# Dependency function to validate the key
def get_api_key(api_key: str = Security(api_key_header)):
    """Validates the API key provided in the X-API-Key header."""
    if api_key == API_KEY:
        return api_key
    
    # If the key is invalid, raise a 401 UNAUTHORIZED error
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing X-API-Key header",
    )

# --- Model Loading and Initialization ---

MODEL_FILE = 'fraud_detector_model.joblib' 
try:
    # This must be the trained and saved model file
    model = load(MODEL_FILE)
    print(f"Successfully loaded model from {MODEL_FILE}")
except Exception as e:
    print(f"ERROR: Could not load model file {MODEL_FILE}. Prediction will fail. Error: {e}")
    model = None

app = FastAPI(
    title="Secured Fraud Detection API",
    description="Microservice protected by a single shared API Key.",
    version="1.0.1"
)

# --- Pydantic Data Model (30 Features) ---
# Defines the exact structure of the JSON payload required for prediction
class TransactionFeatures(BaseModel):
    Time: float = Field(..., description="Seconds elapsed since first transaction")
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float = Field(..., description="Transaction amount")

# --- Secured API Endpoint ---

@app.post(
    "/predict", 
    summary="Predict if a transaction is fraudulent",
    # 🌟 Dependency Injection: Requires a valid API Key to proceed
    dependencies=[Depends(get_api_key)] 
)
def predict_fraud(data: TransactionFeatures):
    """
    Accepts 30 transaction features and returns a fraud prediction.
    Requires a valid 'X-API-Key' in the request header.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model service unavailable. Check deployment logs.")
    
    # 1. Prepare data for model
    # The order of features is guaranteed by the Pydantic model definition
    input_data = data.model_dump()
    features = list(input_data.values()) 
    X_predict = np.array([features]) # scikit-learn expects 2D array
    
    # 2. Prediction and Probability
    prediction = int(model.predict(X_predict)[0])
    # Probability of Class 1 (Fraud)
    probability = model.predict_proba(X_predict)[0].tolist()[1]

    # 3. Format result
    result = "Fraudulent" if prediction == 1 else "Not Fraudulent"
    
    return {
        "prediction_status": result,
        "is_fraud": bool(prediction),
        "probability_of_fraud": round(probability, 4)
    }

