# RSI Divergence Trading Strategy

A professional-grade trading bot that monitors **Nifty 50** on **Angel One Smart API** for RSI divergence patterns, identifying potential reversal signals based on price-RSI divergence.

## 📊 Strategy Overview

This bot implements a **Regular RSI Divergence** strategy based on the following principle:

- **Bearish Divergence (Top)**: Price makes Higher High (HH), RSI makes Lower High (LH) → Potential downward reversal
- **Bullish Divergence (Bottom)**: Price makes Lower Low (LL), RSI makes Higher Low (HL) → Potential upward reversal

## 📏 Trading Rules

The strategy follows these strict rules:

1. **Candle Distance**: Lower number of candles = Stronger divergence
2. **Closing Basis**: All comparisons use closing prices
3. **Distance Requirement**: Minimum 3 candles, Maximum 7 candles between Point A and Point B
4. **Color Matching**:
   - Bearish (Top): Green to Green candles
   - Bullish (Bottom): Red to Red candles
5. **Candle Counting**: Includes both Point A and Point B in the count

## 📁 Folder Structure

```
rsi_divergence/
├── src/                    # Main source code
│   ├── __init__.py
│   ├── main.py            # Bot entry point
│   └── strategy.py        # Divergence detection logic
├── config/                # Configuration
│   ├── __init__.py
│   └── settings.py        # All configuration parameters
├── utils/                 # Utilities
│   ├── __init__.py
│   └── api_helpers.py     # Delta Exchange API client
├── tests/                 # Testing and debugging
│   ├── __init__.py
│   ├── test_rules.py      # Rule validation tests
│   ├── debug_signal.py    # Signal debugging tool
│   └── backtest.py        # Backtesting script
├── scripts/               # Standalone utilities
│   ├── compare_symbols.py # Compare symbols
│   ├── get_price.py       # Get current price
│   └── list_products.py   # List available products
├── docs/                  # Documentation
│   ├── RULES.md          # Detailed trading rules
│   └── SETUP.md          # Setup instructions
├── logs/                  # Log files (gitignored)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd RSI-Divergence

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the environment template
copy .env.example .env

# Edit .env with your Angel One credentials
# REQUIRED: Add your Angel One API key, client ID, password, and TOTP secret
```

### 3. Run the Bot

```bash
# Run from project root
python src/main.py
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:

- **Symbol**: Trading symbol (default: `NIFTY 50`)
- **Timeframe**: Candle timeframe (default: `FIFTEEN_MINUTE`)
- **RSI Period**: RSI calculation period (default: `14`)
- **Min/Max Candles**: Divergence distance (default: `3-7`)
- **Check Interval**: Scan frequency in seconds (default: `60`)
- **Market Hours**: 9:15 AM - 3:30 PM IST (Mon-Fri)

## 📖 Documentation

- [**RULES.md**](docs/RULES.md) - Detailed trading rules and examples
- [**SETUP.md**](docs/SETUP.md) - Complete setup guide

## 🧪 Testing

Run the test suite to validate the strategy:

```bash
# Test rules
python tests/test_rules.py

# Debug a specific signal
python tests/debug_signal.py

# Run backtest
python tests/backtest.py
```

## 📈 Supported Assets

- **Nifty 50** (Default)
- Can be extended to other NSE indices/stocks in `config/settings.py`

## ⏰ Market Hours

- **Trading Hours**: 9:15 AM - 3:30 PM IST
- **Trading Days**: Monday to Friday
- Bot automatically pauses when market is closed

## 🔔 Alerts (Optional)

To enable Telegram alerts, set these in your `.env` file:

```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 📝 Logs

Logs are stored in the `logs/` directory with detailed information about:
- Signal detections
- Price and RSI values
- Divergence patterns
- Errors and warnings

## ⚠️ Disclaimer

This is a trading tool for educational and research purposes. Always do your own research and use proper risk management when trading.

## 📄 License

This project is for personal use.

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
