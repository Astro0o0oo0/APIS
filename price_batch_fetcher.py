import requests
import csv
from datetime import datetime

def fetch_price(symbol, timestamp_str):
    """Fetch the last trade price for a symbol within a specific UTC second."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        start_time = int(dt.timestamp() * 1000)
        end_time = start_time + 999  # full second window

        url = "https://api.binance.com/api/v3/aggTrades"
        params = {
            "symbol": symbol.upper(),
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        if not data:
            return "No trades"
        return float(data[-1]['p'])
    except Exception as e:
        return f"Error: {e}"

def process_csv(input_file="timestamps.csv", output_file="priced_multi.csv"):
    """Read a CSV of symbol + UTC time, append price, write to new CSV."""
    try:
        with open(input_file, newline='') as infile, open(output_file, mode='w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['Last Trade Price (UTC)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                symbol = row['Symbol']
                timestamp = row['UTC Time']
                price = fetch_price(symbol, timestamp)
                row['Last Trade Price (UTC)'] = price
                writer.writerow(row)

            print(f"✅ Done! Prices saved to {output_file}")
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    process_csv()  # uses default filenames unless called with custom ones
