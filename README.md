# Secured Fraud Detection API

This project is a small fastapi based microservice that exposes a fraud detection model.  
The service takes a set of transaction features as input and returns whether the transaction is fraudulent along with a probability score.  
To keep things safe, the prediction endpoint is protected with a simple API key.

---

## Project overview

The main idea is to  
1 load a trained fraud detection model  
2 create a fastapi service with a single prediction endpoint  
3 secure the endpoint with an API key  
4 accept a JSON transaction and return a prediction  

---

## Tech stack

- Python  
- fastapi  
- uvicorn  
- numpy  
- joblib  
- python dotenv  

---

## Important files and functions

### Main application file
This file contains  
- loading of environment variables  
- reading the secret key from `API_SECRET_KEY`  
- loading the model from `fraud_detector_model.joblib`  
- definition of the pydantic `TransactionFeatures` class  
- the `/predict` endpoint that returns the model output  

### Model file
Place your trained model as  
``fraud_detector_model.joblib``  
in the project directory.  
The model must support `predict` and `predict_proba`.

---

## Security

The API uses a shared key for access control.

1 The key is read from the environment variable `API_SECRET_KEY`.  
2 If the variable is missing a development fallback key is used.  
3 Each request must include the key in the header `X API Key`.  
4 Invalid or missing keys lead to a 401 error.

For real deployment always set the environment variable and avoid the fallback key.

---

## Request format

The endpoint expects a JSON body containing all 30 features.  
Example:

```json
{
  "Time": 1000.0,
  "V1": 0.1,
  "V2": 0.2,
  "V3": 0.3,
  "V4": 0.4,
  "V5": 0.5,
  "V6": 0.6,
  "V7": 0.7,
  "V8": 0.8,
  "V9": 0.9,
  "V10": 1.0,
  "V11": 1.1,
  "V12": 1.2,
  "V13": 1.3,
  "V14": 1.4,
  "V15": 1.5,
  "V16": 1.6,
  "V17": 1.7,
  "V18": 1.8,
  "V19": 1.9,
  "V20": 2.0,
  "V21": 2.1,
  "V22": 2.2,
  "V23": 2.3,
  "V24": 2.4,
  "V25": 2.5,
  "V26": 2.6,
  "V27": 2.7,
  "V28": 2.8,
  "Amount": 123.45
}
