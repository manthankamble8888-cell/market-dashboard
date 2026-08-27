import yfinance as yf
import feedparser
import json
from datetime import datetime

tickers = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Sensex": "^BSESN",
    "India VIX": "^INDIAVIX",
    "Nifty IT": "^CNXIT",
    "Nifty Midcap": "^CNXMIDCAP",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "S&P 500": "^GSPC",
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "Crude Oil (Brent)": "BZ=F",
    "Crude Oil (WTI)": "CL=F",
    "Gold": "GC=F",
    "Silver": "SI=F",
    "USD/INR": "INR=X",
    "Dollar Index": "DX-Y.NYB",
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

# Live news headlines (Google News RSS - free, no key needed)
news_items = []
try:
    feed = feedparser.parse("https://news.google.com/rss/search?q=indian+stock+market+OR+nifty+OR+sensex+OR+RBI&hl=en-IN&gl=IN&ceid=IN:en")
    for entry in feed.entries[:8]:
        news_items.append({"title": entry.title, "link": entry.link, "published": entry.get("published","")})
except Exception as e:
    news_items = [{"title": f"News unavailable: {e}", "link":"", "published":""}]

data["news"] = news_items
data["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
