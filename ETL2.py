# ----------------------------------------
# BTC ETL Pipeline
# Extract → Transform → Load
# Beginner-friendly version
# ----------------------------------------

import requests          # To get data from the CoinGecko API
import pandas as pd      # To work with tables (DataFrames)
from datetime import datetime  # To handle dates
import os                # To handle folders/files

# -------------------------------
# STEP 1: EXTRACT
# -------------------------------
def extract():
    """
    Fetch Bitcoin prices from CoinGecko API for the last 30 days.
    Returns a pandas DataFrame with timestamp, price, and date.
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30"}

    print("Fetching data from CoinGecko API...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching data! Status code:", response.status_code)
        return pd.DataFrame()  # return empty DataFrame

    data = response.json()
    prices = data.get("prices", [])
    
    if not prices:
        print("No price data returned from API!")
        return pd.DataFrame()  # return empty DataFrame

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date

    print("Extracted sample data:")
    print(df.head())

    return df

# -------------------------------
# STEP 2: TRANSFORM
# -------------------------------
def transform(df):
    """
    Clean the DataFrame:
    - Remove duplicate dates
    - Add a column showing daily price change
    """
    if df.empty:
        print("No data to transform!")
        return df

    df = df.drop_duplicates(subset="date")
    df["daily_change"] = df["price"].diff()
    df = df[["date", "price", "daily_change"]]

    print("Transformed data sample:")
    print(df.head())

    return df

# -------------------------------
# STEP 3: LOAD
# -------------------------------
def load(df):
    """
    Save the cleaned DataFrame as a CSV inside the 'data' folder.
    Creates the folder if it doesn't exist.
    """
    if df.empty:
        print("No data to save!")
        return

    os.makedirs("data", exist_ok=True)  # Create folder if missing
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/bitcoin_prices_{today}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved successfully to {filename}")

# -------------------------------
# STEP 4: MAIN FUNCTION / START BUTTON
# -------------------------------
if __name__ == "__main__":
    print("Starting ETL process for BTC price data...")

    raw_data = extract()
    cleaned_data = transform(raw_data)
    load(cleaned_data)

    print("ETL process completed successfully!")
