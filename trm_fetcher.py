import csv
import requests
from datetime import datetime

INPUT_CSV = 'your_input_file.csv'
OUTPUT_CSV = 'output_with_trm.csv'
FAILED_DATES_LOG = 'missing_trms.log'
TRM_API_URL = 'https://www.datos.gov.co/resource/32sa-8pi3.json'

rows = []
dates_needed = set()

# Step 1: Read the input CSV and normalize dates
with open(INPUT_CSV, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        date_str = row['Date/Time'][:10]  # Trim to YYYY-MM-DD
        try:
            norm_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            row['Date'] = norm_date
            rows.append(row)
            dates_needed.add(norm_date)
        except ValueError:
            print(f"⚠️ Skipping invalid date format: {date_str}")

# Step 2: Fetch TRM for each needed date
trm_by_date = {}
missing_dates = []

for date in sorted(dates_needed):
    try:
        response = requests.get(TRM_API_URL, params={'vigenciadesde': date}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and 'valor' in data[0]:
            trm_by_date[date] = float(data[0]['valor'])
        else:
            trm_by_date[date] = None
            missing_dates.append(date)
            print(f"⚠️ No TRM data found for {date}")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ Error fetching TRM for {date}: {e}")
        trm_by_date[date] = None
        missing_dates.append(date)

# Step 3: Write output with TRM column
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = list(rows[0].keys()) + ['TRM']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        row['TRM'] = trm_by_date.get(row['Date'], 'N/A')
        writer.writerow(row)

# Step 4: Log missing dates
if missing_dates:
    with open(FAILED_DATES_LOG, 'w', encoding='utf-8') as log_file:
        log_file.write("Dates without TRM data:\n")
        for date in missing_dates:
            log_file.write(date + '\n')
    print(f"📝 Missing TRMs logged to {FAILED_DATES_LOG}")
else:
    print("✅ All TRMs fetched successfully!")
