import sys
import requests
from datetime import datetime

# ✅ Usage check
if len(sys.argv) != 3:
    print("Usage: python price_fetcher.py 'YYYY-MM-DD HH:MM:SS' SYMBOL")
    sys.exit(1)

timestamp = sys.argv[1]
symbol = sys.argv[2].upper()  # e.g. suiUSDT → SUIUSDT

# Parse timestamp
dt = datetime.strptime(timestamp.strip(), "%Y-%m-%d %H:%M:%S")

# Convert to milliseconds
start_time = int(dt.timestamp() * 1000)
end_time = start_time + 999  # full second window

# 🔗 API call
url = "https://api.binance.com/api/v3/aggTrades"
params = {
    "symbol": symbol,
    "startTime": start_time,
    "endTime": end_time,
    "limit": 1000
}

try:
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    if not data:
        print(f"No trades found for {symbol} at {timestamp} UTC")
    else:
        last_trade = data[-1]
        print(f"\n📅 Trade Time: {timestamp} UTC")
        print(f"💰 Last Trade Price: {last_trade['p']}")
        print(f"🔢 Trade ID: {last_trade['a']}")

except Exception as e:
    print(f"Error: {e}")
