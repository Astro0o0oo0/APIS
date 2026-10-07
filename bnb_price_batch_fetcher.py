import requests
import csv
from datetime import datetime

def parse_timestamp(timestamp_str):
    """Try multiple formats to handle quirks like AM/PM or trailing spaces."""
    ts = timestamp_str.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M:%S %p"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized timestamp format: {ts}")

def fetch_bnb_price(timestamp_str):
    """Fetch the last BNB/USDT price in a given UTC second."""
    dt = parse_timestamp(timestamp_str)
    start_time = int(dt.timestamp() * 1000)
    end_time = start_time + 999

    url = "https://api.binance.com/api/v3/aggTrades"
    params = {
        "symbol": "BNBUSDT",
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        if not data:
            return "No trades"
        return float(data[-1]['p'])
    except Exception as e:
        return f"Error: {e}"

def process_csv(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = reader.fieldnames + ['BNB/USDT Price (UTC)']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            utc_time = row['UTC Time']
            try:
                price = fetch_bnb_price(utc_time)
            except ValueError as e:
                price = f"Error: {e}"
            row['BNB/USDT Price (UTC)'] = price
            writer.writerow(row)

        print(f"✅ Done! Prices saved to {output_file}")

# Run it
process_csv("fee_timestamps.csv", "bnb_fees_priced.csv")
