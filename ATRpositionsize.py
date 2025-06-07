import requests

# Function to fetch ATR (approximating ATR using 24hr price change for simplicity)
def get_atr(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["priceChange"])  # Approximate ATR using daily price change

# Function to calculate initial unit size based on ATR
def calculate_unit_size(account_balance, risk_per_unit, atr):
    return (risk_per_unit * account_balance) / atr

# Function to apply scaling adjustments for equal dollar risk
def adjust_unit_size(original_unit, actual_dollar_risk, target_dollar_risk):
    return original_unit * (target_dollar_risk / actual_dollar_risk)

# Define trading parameters
account_balance = 120  # Your total account size
risk_per_unit = 0.02  # 2% risk per trade
target_dollar_risk = 11  # Desired dollar risk per trade

# Fetch ATR for assets
btc_atr = get_atr("BTCUSDT")
eth_atr = get_atr("ETHUSDT")
sol_atr = get_atr("SOLUSDT")

# Calculate initial unit sizes
btc_unit = calculate_unit_size(account_balance, risk_per_unit, btc_atr)
eth_unit = calculate_unit_size(account_balance, risk_per_unit, eth_atr)
sol_unit = calculate_unit_size(account_balance, risk_per_unit, sol_atr)

# Approximate current prices (You can replace this with live price fetching)
btc_price = 110000
eth_price = 2500
sol_price = 160

# Convert unit sizes to dollar risk
btc_dollar_risk = btc_unit * btc_price
eth_dollar_risk = eth_unit * eth_price
sol_dollar_risk = sol_unit * sol_price

# Adjust unit sizes for equal dollar risk
btc_unit_adjusted = adjust_unit_size(btc_unit, btc_dollar_risk, target_dollar_risk)
eth_unit_adjusted = adjust_unit_size(eth_unit, eth_dollar_risk, target_dollar_risk)
sol_unit_adjusted = adjust_unit_size(sol_unit, sol_dollar_risk, target_dollar_risk)

# Display final adjusted unit sizes
print(f"Adjusted BTC Unit Size: {btc_unit_adjusted:.6f} BTC")
print(f"Adjusted ETH Unit Size: {eth_unit_adjusted:.6f} ETH")
print(f"Adjusted SOL Unit Size: {sol_unit_adjusted:.6f} SOL")
import requests