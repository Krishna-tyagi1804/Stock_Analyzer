import yfinance as yf
from datetime import datetime as dt
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "static" / "data" / "chart_data.db"
conn = sqlite3.connect(db_path)
BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "static" / "data" / "card_data.db"
con = sqlite3.connect(db_path)
tickers = ["GOOGL", "TATASTEEL.NS", "AAPL", "RELIANCE.NS"]

now = dt.now()
current = now.strftime("20%y-%m-%d")
data1 = yf.download(tickers, start="2025-01-01", end=current, group_by="ticker")
data1.columns = [f"{col[0]}_{col[1]}" for col in data1.columns]
data1.to_sql("Chart_data", conn, if_exists="replace", index = True)

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

df = pd.DataFrame(card_data)
df.to_sql("Card_data", con, if_exists="replace", index=False)