# Bitcoin ETL Pipeline

This project demonstrates a simple ETL process built in Python. It fetches Bitcoin price data from the CoinGecko API, cleans and transforms the data using pandas, calculates daily price changes and saves the final dataset as a CSV file for analysis.

## Tech stack

Python 3

Libraries: pandas, requests

Tools: Git & GitHub for version control

## How it works

Extract: Gets 30 days of Bitcoin price data from CoinGecko’s public API.

Transform: Cleans duplicates, aggregates hourly prices into daily values and adds a daily-change column.

Load: Saves the cleaned dataset to /data/bitcoin_prices.csv.

## Run the project

pip3 install pandas requests
python3 etl.py

The output CSV appears in the data/ folder.

## Key learning

While building this project I fixed an issue where CoinGecko returned multiple hourly entries per day. I solved it by grouping by date and keeping the last entry for each day, which gave one clean record per date.

## Project structure

bitcoin-etl/
├── data/
│   └── bitcoin_prices.csv
└── etl.py

Author
Zubair Niaz – github.com/zniaz98