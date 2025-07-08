# 🔍 Crypto Trading & Fee Tools – Binance Edition

[![Python](https://img.shields.io/badge/Python-3.9-blue)](#)
[![Data Source](https://img.shields.io/badge/Data%20Source-Binance-yellow)](#)
[![Precision](https://img.shields.io/badge/Price%20Accuracy-To%20the%20Second-green)](#)
[![Input Format](https://img.shields.io/badge/Input-CSV-lightgrey)](#)

A lightweight Python toolkit for crypto traders and record-keepers who value precision. This repo helps you:

- Calculate trade position sizes using ATR and target risk
- Fetch historical price data for any Binance spot symbol (1-minute or 1-second resolution)
- Batch-process multi-symbol pricing data from a simple CSV
- Reconcile Binance trading fees for tax or portfolio reporting
- Enrich crypto transaction CSVs with official USD/COP daily TRM values from Colombia’s Banco de la República for tax reporting
- Works entirely via free public APIs - Binance's REST API (unless specified) — no API keys required

---

## 📁 Repository Structure

- `ATRpositionsize.py`: Calculate trading position size based on ATR.
- `bnb_price_fetcher.py`: Fetch historical BNB/USDT prices (1-minute precision).
- `bnb_price_batch_fetcher.py`: Batch-fetch BNB/USDT prices from a CSV of UTC timestamps (1-second precision).
- `price_batch_fetcher.py`: Batch-fetch second-accurate trade prices for any Binance spot symbol using UTC timestamps from a CSV.
- `price_fetcher.py`: A simple command-line tool to fetch 1-minute historical OHLC data from Binance's public API.
- `README.md`: Project information and usage instructions.
- `timestamp_to_unix.py`: Convert a human-readable timestamp to Unix time in milliseconds.
- `trm_fetcher.py`: Enrich trade logs by fetching official USD/COP TRMs from Colombia’s central bank for each transaction date.

---

## 🚀 Usage

### 🔹 `ATRpositionsize.py`
Calculate trading position size based on your stop loss, ATR, and risk preferences.


```bash
python3 ATRpositionsize.py
```

- **Inputs**: Entry price, Stop loss, ATR, etc.
- **Output**: Position size (units)
- **Dependencies**: requests

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
- **Supported Symbols**: All Binance spot trading pairs 
- **Dependencies**: requests, csv, datetime

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
- **Dependencies**: requests, csv, datetime

---

### 🔹 `price_batch_fetcher.py`
Batch-fetch second-accurate trade prices for any Binance spot symbol using UTC timestamps from a CSV.

```bash
python3 price_batch_fetcher.py
```

- **Input CSV** (`timestamps.csv`):

  ```csv
  Trade ID,Symbol,UTC Time
  001,BNBUSDT,2025-07-01 20:18:30
  002,SOLUSDT,2025-07-01 21:00:02
  003,ETHUSDT,2025-07-01 22:15:45
  ```

- **Output**: priced_multi.csv — includes the last trade price for each timestamp/symbol pair
- **Precision**: 1-second (via Binance's aggTrades API)
- **Supported Symbols**: All Binance spot trading pairs 
- **Dependencies**: requests, csv, datetime

---

### 🔹 `price_fetcher.py`
A simple command-line tool to fetch 1-minute historical OHLC data from Binance's public API.

```bash
python3 price_fetcher.py "YYYY-MM-DD HH:MM:SS" SYMBOL
```
- **Inputs**: Timestamp, symbol (command line arguments)
- **Output**: print to screen
- **Contents**: Unix time (ms), Open, High, Low, Close
- **Precision**: 1-minute candles
- **Dependencies**: requests, csv, datetime

---

### 🔹 `timestamp_to_unix.py`
Convert a human-readable timestamp to Unix time in milliseconds — useful for locating exact rows in Binance’s 1-second .csv historical data.

```bash
python3 timestamp_to_unix.py "YYYY-MM-DD HH:MM:SS"
```
- **Inputs**: Timestamp (command line argument)
- **Output**: print to screen
- **Contents**: Input Timestamp, Unix Time (ms)
- **Precision**: Converts to milliseconds for use with Binance 1-second data files
- **Dependencies**: datetime, sys

---

### 🔹 `trm_fetcher.py`
Batch-fetch official TRMs (USD/COP exchange rates) using Colombia’s open data API.

```bash
python3 trm_fetcher.py
```

- **Input CSV**: Must include a Date/Time column with UTC-5 timestamps (e.g. 2024-05-14 13:04)
- **Output CSV**: Adds a TRM column with the official USD to COP exchange rate from Banco de la República for each date
- **API Source**: https://www.datos.gov.co/resource/32sa-8pi3.json
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