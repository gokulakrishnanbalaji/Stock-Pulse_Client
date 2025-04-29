from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
import yaml
from datetime import datetime, timedelta
from pydantic import BaseModel
import torch.nn as nn
import os
import joblib
from prometheus_fastapi_instrumentator import Instrumentator
from model import TimeSeriesTransformer
import logging

# Set up logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="Stock Price Movement Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Load ticker symbols from YAML
try:
    with open('/app/stocks.yaml', 'r') as file:
        NSE_TICKERS = yaml.safe_load(file)
    logging.info("Successfully loaded stocks.yaml: %s", NSE_TICKERS)
except FileNotFoundError:
    logging.error("stocks.yaml not found")
    raise Exception("stocks.yaml not found")
except Exception as e:
    logging.error("Error loading stocks.yaml: %s", str(e))
    raise Exception(f"Error loading stocks.yaml: {str(e)}")

# Load the trained model
try:
    torch.serialization.add_safe_globals([torch.nn.modules.linear.Linear])
    model_path = '/app/model.pth'
    model = torch.load(model_path, weights_only=False)
    model.eval()
    logging.info("Successfully loaded model.pth")
except FileNotFoundError:
    logging.error("model.pth not found")
    raise Exception("model.pth not found")
except Exception as e:
    logging.error("Error loading model: %s", str(e))
    raise Exception(f"Error loading model: {str(e)}")

# Define request model
class CompanyRequest(BaseModel):
    company_name: str

# Compute technical indicators
def compute_technical_indicators(df):
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26

    logging.info('Computed technical indicators')
    return df

# Process stock data for prediction
def process_stock_for_prediction(df):
    df = compute_technical_indicators(df)

    feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_5', 'SMA_10', 'RSI', 'MACD']
    df = df[feature_columns]
    df = df.dropna().reset_index(drop=True)
    
    scaler = joblib.load('/app/scaler.pkl')
    X = scaler.transform(df)

    # Return the most recent feature set
    X_last = X[-1]

    logging.info('Processed stock data for prediction')
    return X_last

# Fetch minimal stock data
def fetch_company_data(company_name):
    if company_name not in NSE_TICKERS:
        raise HTTPException(status_code=404, detail=f"Company {company_name} not found in stocks.yaml")

    ticker = NSE_TICKERS[company_name]
    days = 30
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    logging.info(f"Downloading {company_name} from {start_date.date()} to {end_date.date()}...")
    df = yf.download(
        ticker,
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        interval='1d',
        group_by='ticker',
        auto_adjust=False
    )
    
    if not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)

        df = df.reset_index()
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df['Date'] = pd.to_datetime(df['Date'])  

    logging.info('Fetched company data')
    return df

# FastAPI endpoint
@app.post("/predict/", response_model=dict)
async def predict_stock_movement(request: CompanyRequest):
    try:
        # Step 1: Fetch minimal data
        df = fetch_company_data(request.company_name)
        
        # Step 2: Preprocess data
        X_last = process_stock_for_prediction(df)
                
        X_tensor = torch.tensor(X_last, dtype=torch.float32)

        if X_tensor.dim() == 1:
            X_tensor = X_tensor.unsqueeze(0)

        X_tensor = X_tensor.unsqueeze(1)

        with torch.no_grad():
            output = model(X_tensor)
            prediction = torch.argmax(output, dim=1).item()

        logging.info('Completed making prediction')

        return {"company_name": request.company_name, "prediction": prediction}

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    return {"message": "FastAPI backend is running"}