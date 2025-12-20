import yfinance as yf
from datetime import datetime as dt
import json

tickers = ["GOOGL", "TATASTEEL.NS"]
now = dt.now()
current = now.strftime("20%y-%m-%d")
data1 = yf.download(tickers, start="2025-01-01", end=current, group_by="ticker")

data1.to_csv("backend\data\chart_data.csv", index=True)
card_data = []

for ticker in tickers:
    ticker_obj = yf.Ticker(ticker) 
    info = ticker_obj.info
    cur_data = {
        # 1. Header Data
        "symbol": info.get("symbol"),
        "shortName": info.get("shortName"),
        "currentPrice": info.get("currentPrice"),
        
        # Calculate Change (Current - Previous Close)
        "previousClose": info.get("previousClose"),
        # Use .get() with defaults to avoid errors if data is missing
        "change_percent": (info.get("currentPrice", 0) - info.get("previousClose", 1)) / info.get("previousClose", 1) * 100,

        # 2. Body Data
        "marketCap": info.get("marketCap"),  # You will need to format this (e.g., 20000000 -> 20M)
        "trailingPE": info.get("trailingPE"), # Price-to-Earnings Ratio
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "sector": info.get("sector")
    }
    card_data.append(cur_data)

with open("backend/data/card_data.json", "w") as jdata:
    json.dump(card_data, jdata, indent=4)