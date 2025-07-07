import sys
import requests
from datetime import datetime

# ✅ Check for proper usage
if len(sys.argv) != 3:
    print("Usage: python3 price_fetcher.py 'YYYY-MM-DD HH:MM:SS' SYMBOL")
    sys.exit(1)

timestamp = sys.argv[1]
symbol = sys.argv[2].upper()  # Auto-uppercase (e.g. solusdt → SOLUSDT)
interval = "1m"

# Convert time to milliseconds
start_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

# Check if we need to snap to the start of the minute
if start_dt.second != 0 or start_dt.microsecond != 0:
    print(f"🧭 Snapped timestamp to candle start: {start_dt.replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')} UTC")

start_dt = start_dt.replace(second=0, microsecond=0)

# Convert to Unix time in milliseconds
start_ms = int(start_dt.timestamp() * 1000)
end_ms = start_ms + 60_000  # 1-minute window

print(f"Unix time (ms): {start_ms}")


# 🔗 API call setup
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": symbol,
    "interval": interval,
    "startTime": start_ms,
    "endTime": end_ms,
    "limit": 1
}

response = requests.get(url, params=params)
data = response.json()

# Display results
if data and isinstance(data, list):
    candle = data[0]
    print(f"\n📅 Trade Time: {timestamp} UTC")
    print(f"🟢 Open:  {candle[1]}")
    print(f"🔼 High:  {candle[2]}")
    print(f"🔽 Low:   {candle[3]}")
    print(f"🔴 Close: {candle[4]}")
else:
    print(f"No data returned for {symbol} at {timestamp}")
