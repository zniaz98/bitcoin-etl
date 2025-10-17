#BTC ETL Pipeline

import requests # Allows for API calls
import pandas as pd # Importing pandas for easier data manipulation
from datetime import datetime # To work with dates in the raw data

# Here I am defining the first of 3 functions as Extract
# This calls the API from the coingecko link and retrieves the relevant data from the last 30 days, specifying which parameters I want
# Then I convert the API data into a pandas dataframe, specifying column names and what data I want exactly
# Finally, I change the timestamp to date format from ms


def extract():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30"}
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices'] 
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
    return df

# Next I define the Transform function which drops duplicate dates
# I also add a useful column that shows the daily change in price
# Finally I select only the relevant columns to keep the dataframe clean


def transform(df):
    df = df.drop_duplicates(subset='date')
    df['daily_change'] = df['price'].diff() 
    df = df[['date', 'price', 'daily_change']] 
    return df

# Lastly I define the Load function which just saves the dataframe as a csv file in a data folder

def load(df): 
    df.to_csv('data/bitcoin_prices.csv', index=False)
              
if __name__ == "__main__":
    print("Starting ETL process for BTC price data...")

    raw_data = extract()
    cleaned_data = transform(raw_data)
    print(cleaned_data.head())

    load(cleaned_data)

    print("ETL process successful!") 

