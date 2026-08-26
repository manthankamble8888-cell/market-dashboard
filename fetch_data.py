import yfinance as yf
import json
from datetime import datetime

tickers = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Sensex": "^BSESN",
    "India VIX": "^INDIAVIX",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "S&P 500": "^GSPC",
    "Crude Oil (Brent)": "BZ=F",
    "Crude Oil (WTI)": "CL=F",
    "Gold": "GC=F",
    "USD/INR": "INR=X",
    "US 10Y Yield": "^TNX",
}

data = {}
for name, symbol in tickers.items():
    try:
        hist = yf.Ticker(symbol).history(period="2d")
        prev_close = hist["Close"].iloc[-2]
        last = hist["Close"].iloc[-1]
        change = last - prev_close
        pct = (change / prev_close) * 100
        data[name] = {"price": round(float(last),2), "change": round(float(change),2), "pct": round(float(pct),2)}
    except Exception as e:
        data[name] = {"error": str(e)}

data["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
