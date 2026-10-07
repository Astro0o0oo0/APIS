import csv
from datetime import datetime
import os

def closest_prior_trade(csv_file, target_unix):
    closest_row = None
    closest_diff = float("inf")
    
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            try:
                # Convert microseconds → milliseconds
                trade_time = int(row[5]) // 1000
                if trade_time <= target_unix:
                    diff = target_unix - trade_time
                    if diff < closest_diff:
                        closest_diff = diff
                        closest_row = row
            except ValueError:
                # Skip malformed rows
                print("Skipping row:", row)
    
    return closest_row, closest_diff

def batch_process(timestamps_csv, output_csv):
    results = []
    
    # Your timestamps.csv is semicolon-delimited (Latin American Excel)
    with open(timestamps_csv, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        # normalize headers (strip spaces)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        for row in reader:
            timestamp_str = row["Timestamp"]
            pair = row.get("Pair", "").strip()   # e.g. BNBUSDT, LINKUSDT
            case_type = row.get("Type", "").strip()  # "NoTrade" or "Check"
            
            # Convert timestamp to UNIX ms
            target_unix = int(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
            
            # Build expected filename for the aggTrades CSV
            # Assumes files are named like "BNBUSDT-aggTrades-2025-12-31.csv"
            date_part = timestamp_str.split(" ")[0]  # YYYY-MM-DD
            trades_csv = f"{pair}-aggTrades-{date_part}.csv"
            
            if not os.path.exists(trades_csv):
                print(f"⚠️ File not found: {trades_csv} → skipping {timestamp_str} ({pair})")
                result = {
                    "Timestamp": timestamp_str,
                    "Pair": pair,
                    "Type": case_type,
                    "Price": "File not found",
                    "MillisecondsBefore": "",
                    "ClosestUnix": ""
                }
                results.append(result)
                continue
            
            closest_row, diff = closest_prior_trade(trades_csv, target_unix)
            
            if closest_row:
                result = {
                    "Timestamp": timestamp_str,
                    "Pair": pair,
                    "Type": case_type,
                    "Price": closest_row[1],  # price column
                    "MillisecondsBefore": diff,
                    "ClosestUnix": closest_row[5]  # trade time column
                }
                results.append(result)
                # Log message per row
                print(f"Processing {timestamp_str} ({pair}, {case_type}) → Price {result['Price']}, ClosestUnix {result['ClosestUnix']}, {diff} ms before")
            else:
                result = {
                    "Timestamp": timestamp_str,
                    "Pair": pair,
                    "Type": case_type,
                    "Price": "No prior trade",
                    "MillisecondsBefore": "",
                    "ClosestUnix": ""
                }
                results.append(result)
                print(f"Processing {timestamp_str} ({pair}, {case_type}) → No prior trade found")
    
    # Write results to output CSV (comma-delimited for consistency)
    with open(output_csv, "w", newline='') as f:
        fieldnames = ["Timestamp", "Pair", "Type", "Price", "MillisecondsBefore", "ClosestUnix"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(results)

# Define file names
TIMESTAMPS_CSV = "timestamps.csv"   # input list of timestamps + pair + type
OUTPUT_CSV = "results.csv"          # output with prices + closest unix

# Run batch process
batch_process(TIMESTAMPS_CSV, OUTPUT_CSV)
print(f"Processed {TIMESTAMPS_CSV} → wrote results to {OUTPUT_CSV}")
