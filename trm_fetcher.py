import csv
import requests
from datetime import datetime, timedelta

INPUT_CSV = 'your_input_file.csv'
OUTPUT_CSV = 'output_with_trm.csv'
FAILED_DATES_LOG = 'missing_trms.log'
TRM_API_URL = 'https://www.datos.gov.co/resource/32sa-8pi3.json'

rows = []
dates_needed = set()

# Step 1: Read the input CSV and normalize dates
with open(INPUT_CSV, 'r', newline='', encoding='utf-8-sig') as infile:
    reader = csv.DictReader(infile)

    # Preview the first few rows before processing
    print("🔍 Previewing first 10 rows of input CSV:")
    for i, row in enumerate(reader):
        print(row)
        if i >= 9:
            break
    infile.seek(0)  # Reset reader to beginning
    reader = csv.DictReader(infile)  # Reinitialize after preview

    for row in reader:
        date_str = row['Date/Time'][:10]  # Trim to YYYY-MM-DD
        try:
            norm_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            row['Date'] = norm_date
            rows.append(row)
            dates_needed.add(norm_date)
        except ValueError:
            print(f"⚠️ Skipping invalid date format: {date_str}")

# Step 2: Define fallback function to fetch TRM
# Step 2: Define fallback function to fetch TRM using vigenciahasta
def fetch_trm_for_date(date_str):
    """
    Fetch TRM for a given date.
    If no TRM is published exactly on that date, look backwards until
    you find a TRM whose 'vigenciahasta' covers the target date.
    """
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    for offset in range(0, 6):  # try today, then up to 5 days back
        check_date = (base_date - timedelta(days=offset)).strftime("%Y-%m-%d")
        try:
            response = requests.get(
                TRM_API_URL,
                params={'vigenciahasta': check_date},  # key change: use vigenciahasta
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                continue

            # TRM entries have 'vigenciadesde' and 'vigenciahasta' fields
            for entry in data:
                desde = entry.get('vigenciadesde')
                hasta = entry.get('vigenciahasta')
                raw_val = entry.get('valor') or entry.get('value')

                if hasta and datetime.strptime(hasta[:10], "%Y-%m-%d") >= base_date:
                    try:
                        return float(raw_val)
                    except (TypeError, ValueError):
                        continue
        except requests.exceptions.RequestException:
            continue
    return None

# Step 3: Fetch TRM for each needed date
trm_by_date = {}
missing_dates = []

for date in sorted(dates_needed):
    trm_val = fetch_trm_for_date(date)
    if trm_val is None:
        print(f"⚠️ No TRM found for {date} (even after fallback)")
        missing_dates.append(date)
    else:
        trm_by_date[date] = trm_val

# Step 4: Write output with TRM column
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = list(rows[0].keys()) + ['TRM']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        row['TRM'] = trm_by_date.get(row['Date'], 'N/A')
        writer.writerow(row)

# Step 5: Log missing dates
if missing_dates:
    with open(FAILED_DATES_LOG, 'w', encoding='utf-8') as log_file:
        log_file.write("Dates without TRM data:\n")
        for date in missing_dates:
            log_file.write(date + '\n')
    print(f"📝 Missing TRMs logged to {FAILED_DATES_LOG}")
else:
    print("✅ All TRMs fetched successfully!")

