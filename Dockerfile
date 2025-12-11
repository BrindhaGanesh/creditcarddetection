# Use a lightweight official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This is done first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all essential application files from the root directory to /app
# 1. app.py (your main FastAPI code)
# 2. fraud_detector_model.joblib (your model file)
# Note: requirements.txt is already copied.
COPY app.py .
COPY fraud_detector_model.joblib .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# 'app:app' refers to the file 'app.py' and the FastAPI instance 'app'
# --host 0.0.0.0 makes the service accessible externally
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]