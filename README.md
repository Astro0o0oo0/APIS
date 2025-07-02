# 🔍 Crypto Fee Tools – Binance Edition

[![Python](https://img.shields.io/badge/Python-3.9-blue)](#)
[![Data Source](https://img.shields.io/badge/Data%20Source-Binance-yellow)](#)
[![Precision](https://img.shields.io/badge/Price%20Accuracy-To%20the%20Second-green)](#)
[![Input Format](https://img.shields.io/badge/Input-CSV-lightgrey)](#)

A lightweight Python toolkit for crypto traders and record-keepers who value precision. This repo helps you:

- Calculate trade position sizes using ATR
- Fetch historical BNB prices (1-minute or 1-second accuracy)
- Reconcile Binance trading fees for tax or portfolio reporting

---

## 📁 Repository Structure

- `ATRpositionsize.py`: Calculate trading position size based on ATR.
- `bnb_price_fetcher.py`: Fetch historical BNB/USDT prices (1-minute precision).
- `bnb_price_batch_fetcher.py`: Batch-fetch BNB/USDT prices from a CSV of UTC timestamps (1-second precision).
- `README.md`: Project information and usage instructions.

---

## 🚀 Usage

### 🔹 `ATRpositionsize.py`
Calculate trading position size based on your stop loss, ATR, and risk preferences.


```bash
python3 ATRpositionsize.py
```

- **Inputs**: Entry price, Stop loss, ATR, etc.
- **Output**: Position size (units)
- **Dependencies**: None

---

### 🔹 `bnb_price_fetcher.py`
Fetch 1-minute BNB/USDT candlestick data and export to CSV.

```bash
python3 bnb_price_fetcher.py
```

- **Inputs**: Symbol, interval, and time range (edit inside script)
- **Output**: bnbusdt_historical_prices.csv
- **Contents**: Time, Open, High, Low, Close, Volume
- **Precision**: 1-minute candles
- **Dependencies**: requests, csv, datetime, time

---

### 🔹 `bnb_price_batch_fetcher.py`
Batch-fetch second-accurate BNB/USDT prices using UTC timestamps from a CSV.

```bash
python3 bnb_price_batch_fetcher.py
```

- **Input CSV** (`fee_timestamps.csv`):

  ```csv
  Trade ID,UTC Time
  001,2025-07-01 20:18:30
  002,2025-07-01 21:00:02
  ```

- **Output**: bnb_fees_priced.csv — includes price for each timestamp
- **Precision**: 1-second (via Binance's aggTrades API)
- **Dependencies**: requests, csv, datetime

---

## 🛠️ Notes
All price data and timestamps are UTC-based for accuracy and consistency with Binance records.
No authentication is required for these scripts—they use Binance’s free public API endpoints.
Data is pulled from Binance at runtime; results may vary slightly depending on trade activity and network timing.

## 📫 Contributions
Ideas, improvements, and precision-obsessed collaborators welcome. Feel free to fork, customize, or submit a pull request.

## 🪙 License
MIT License — free to use, fork, and remix. Attribution appreciated, but not required.