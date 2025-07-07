import requests
import csv
from datetime import datetime

# Parameters
symbol = "BNBUSDT"
interval = "1m"

# 🔢 List of trade times (UTC)
timestamps = [
    "2025-07-01 20:18:00",
    "2025-07-02 14:33:00",
    "2025-07-03 09:05:00"
    # Add more timestamps as needed
]

# Prepare CSV output
with open("bnbusdt_historical_prices.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Trade Time (UTC)", "Open", "High", "Low", "Close", "Volume"])

    # Loop through timestamps
    for ts in timestamps:
        start_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        start_ms = int(start_dt.timestamp() * 1000)
        end_ms = start_ms + 60_000  # 1-minute window

        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_ms}&endTime={end_ms}"
        response = requests.get(url)
        data = response.json()

        if data:
            candle = data[0]
            writer.writerow([
                ts,
                candle[1],  # Open
                candle[2],  # High
                candle[3],  # Low
                candle[4],  # Close
                candle[5]   # Volume
            ])
        else:
            writer.writerow([ts, "No data", "", "", "", ""])

print("✅ Historical prices saved to bnbusdt_historical_prices.csv")
