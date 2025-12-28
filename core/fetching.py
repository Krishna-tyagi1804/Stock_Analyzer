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
tickers = ["GOOGL", "TATASTEEL.NS", "AAPL", "RELIANCE.NS", "^NSEI", "^BSESN", "GOLDBEES.NS"]

now = dt.now()
current = now.strftime("20%y-%m-%d")
data1 = yf.download(tickers, start="2025-01-01", end=current, group_by="ticker")
data1.columns = [f"{col[0]}_{col[1]}" for col in data1.columns]
data1.to_sql("Chart_data", conn, if_exists="replace", index = True)
CURRENCY_SYMBOLS = {
    'USD': '$', 'EUR': '€', 'JPY': '¥', 'GBP': '£', 'CNY': '¥',
    'INR': '₹', 'CAD': 'C$', 'AUD': 'A$', 'KRW': '₩', 'BRL': 'R$',
    'RUB': '₽', 'MXN': 'Mex$', 'SGD': 'S$', 'HKD': 'HK$'
}

card_data = []
for ticker in tickers:
    ticker_obj = yf.Ticker(ticker) 
    info1 = ticker_obj.info
    currency = info1.get('currency')
    cur_symbol = CURRENCY_SYMBOLS.get(currency)
    cur_price = info1.get('currentPrice') or info1.get('regularMarketPrice')
    prev_close = info1.get('previousClose') or info1.get('regularMarketPreviousClose')
    if info1.get("symbol") == "GOLDBEES.NS":
        cur_price = 1000*cur_price
        prev_close = 1000*prev_close
    cur_data = {
        # 1. Header Data
        "symbol": info1.get("symbol"),
        "shortName": info1.get("shortName"),
        "currentPrice": f"{cur_symbol}{cur_price}",
        
        # Calculate Change (Current - Previous Close)
        "previousClose": info1.get("previousClose"),
        # Use .get() with defaults to avoid errors if data is missing
        "change_percent": (info1.get("currentPrice", 0) - info1.get("previousClose", 1)) / info1.get("previousClose", 1) * 100,

        # 2. Body Data
        "marketCap": info1.get("marketCap"),  # You will need to format this (e.g., 20000000 -> 20M)
        "trailingPE": info1.get("trailingPE"), # Price-to-Earnings Ratio
        "fiftyTwoWeekHigh": info1.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info1.get("fiftyTwoWeekLow"),
        "sector": info1.get("sector")
    }
    if currency != "INR":
        ticker_symbol = f"{currency}INR=X"
        data = yf.Ticker(ticker_symbol)
        price = data.info.get('currentPrice') or data.info.get('regularMarketPreviousClose')
        price = price * info1.get("currentPrice")
        cur_data["currentPrice"] = f"{cur_symbol}{cur_price}(₹{price:.2f})"
    card_data.append(cur_data)

df = pd.DataFrame(card_data)
df.to_sql("Card_data", con, if_exists="replace", index=False)