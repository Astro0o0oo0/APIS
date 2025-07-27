import requests

def get_atr(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["priceChange"])

def get_live_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["price"])

def calculate_unit_size(account_balance, risk_per_unit, atr):
    return (risk_per_unit * account_balance) / atr

def adjust_unit_size(original_unit, actual_dollar_risk, target_dollar_risk):
    return original_unit * (target_dollar_risk / actual_dollar_risk)

def get_historical_atr(symbol, interval="1d", periods=14):
    """
    Fetches historical klines and calculates ATR for the given interval and periods.
    interval: Binance kline interval (e.g., '1h', '4h', '6h', '1d')
    periods: Number of periods for ATR calculation (default 14)
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={periods+1}"
    response = requests.get(url).json()
    trs = []
    for i in range(1, len(response)):
        high = float(response[i][2])
        low = float(response[i][3])
        prev_close = float(response[i-1][4])
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    atr = sum(trs) / periods
    return atr

# User input for symbol
print("Script started! Waiting for your USDT pair input...")
symbol = input("Enter Binance USDT pair symbol (e.g., BNBUSDT): ").strip().upper()

# Trading parameters
account_balance = 120
risk_per_unit = 0.02
target_dollar_risk = 11

# Fetch ATRs for HTF and LTF by default
atr_daily = get_atr(symbol)  # Daily ATR (HTF)
atr_1h = get_historical_atr(symbol, interval="1h")  # 1H ATR (LTF)

# Timeframe selection
print("\nSelect ATR timeframe for position sizing:")
print("1 - Daily (1d) [default]")
print("2 - Hourly (1h)")
print("3 - Custom (e.g., 4h, 6h)")
tf_choice = input("Enter choice (1/2/3): ").strip()

if tf_choice == "2":
    interval = "1h"
    atr_used = atr_1h
elif tf_choice == "3":
    interval = input("Enter custom interval (e.g., 4h, 6h): ").strip()
    atr_used = get_historical_atr(symbol, interval)
else:
    interval = "1d"
    atr_used = atr_daily

price = get_live_price(symbol)

# Calculate unit size and dollar risk
unit = calculate_unit_size(account_balance, risk_per_unit, atr_used)
dollar_risk = unit * price

# Adjust unit size for target dollar risk
unit_adjusted = adjust_unit_size(unit, dollar_risk, target_dollar_risk)

print(f"\nSymbol: {symbol}")
print(f"Daily ATR (HTF): {atr_daily:.6f}")
print(f"1H ATR (LTF): {atr_1h:.6f}")
if tf_choice == "3":
    print(f"Custom ATR ({interval}): {atr_used:.6f}")
print(f"Live Price: {price:.6f} USDT")
print(f"Adjusted Unit Size ({interval}): {unit_adjusted:.6f} {symbol.replace('USDT','')}")