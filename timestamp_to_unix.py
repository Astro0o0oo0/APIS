import sys
from datetime import datetime

# Check for timestamp argument
if len(sys.argv) != 2:
    print("Usage: python3 timestamp_to_unix.py 'YYYY-MM-DD HH:MM:SS'")
    sys.exit(1)

# Parse and convert
timestamp_str = sys.argv[1]

try:
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    unix_ms = int(dt.timestamp() * 1000)
    print(f"📅 Input Timestamp: {timestamp_str} UTC")
    print(f"🧮 Unix Time (ms): {unix_ms}")
except ValueError:
    print("❌ Invalid format. Use: 'YYYY-MM-DD HH:MM:SS'")
