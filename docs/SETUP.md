# Setup Guide - RSI Divergence Bot

Complete setup instructions for running the RSI Divergence trading bot.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for fetching market data)

## 🚀 Installation Steps

### Step 1: Install Python

If you don't have Python installed:

**Windows**:
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

**Verify installation**:
```bash
python --version
```

### Step 2: Install Dependencies

Navigate to the project directory and install required packages:

```bash
cd RSI-Divergence
pip install -r requirements.txt
```

**Required packages**:
- `requests` - For API calls to Delta Exchange
- `pandas` - For data manipulation
- `pandas_ta` - For RSI calculation
- `logzero` - For logging
- `python-dotenv` - For environment variables

### Step 3: Configure Environment (Optional)

For basic usage, **no configuration is needed**. The bot works with public Delta Exchange data.

**Optional configurations**:

1. Copy the environment template:
```bash
copy .env.example .env
```

2. Edit `.env` file for Telegram alerts:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Step 4: Customize Settings (Optional)

Edit `config/settings.py` to change:

```python
# Trading pair
SYMBOL = "BTCUSD"  # Options: "BTCUSD", "ETHUSD", etc.

# Timeframe
TIMEFRAME = "15m"  # Options: "5m", "15m", "1h", "4h", "1d"

# RSI Period
RSI_PERIOD = 14  # Standard is 14

# Divergence distance
MIN_CANDLES = 3  # Minimum distance
MAX_CANDLES = 7  # Maximum distance

# Check interval (seconds)
CHECK_INTERVAL = 60  # How often to check for signals
```

## ▶️ Running the Bot

### Basic Usage

From the project root directory:

```bash
python src/main.py
```

### Expected Output

```
🚀 Starting RSI Divergence Bot (Delta Exchange)
📊 Symbol: BTCUSD | Timeframe: 15m
📏 Rules: 3-7 candles, Closing Basis, Color Match
📐 RSI Period: 14
────────────────────────────────────────────────────────────
🔍 Scanning BTCUSD: Price=45000.00, RSI=54.32
🔍 Scanning BTCUSD: Price=45050.00, RSI=55.10
...
```

### When a Signal is Detected

```
============================================================
✅ BULLISH DIVERGENCE DETECTED!
   📊 Strength: 3 candles
   💰 Price: 45000.00 → 44800.00
   📈 RSI:   28.50 → 31.20
   🎨 Pattern: Red-Red
   🕐 Point A Time: 2026-01-22 10:00:00+00:00
   🕑 Point B Time: 2026-01-22 10:30:00+00:00
============================================================
```

## 🧪 Testing

### 1. Test the Strategy Rules

```bash
python tests/test_rules.py
```

### 2. Debug a Specific Signal

```bash
python tests/debug_signal.py
```

### 3. Run Backtests

```bash
python tests/backtest.py
```

## 🔔 Setting Up Telegram Alerts (Optional)

### Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **bot token** provided

### Step 2: Get Your Chat ID

1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{"id":YOUR_CHAT_ID}`
4. Copy the **chat ID**

### Step 3: Configure .env

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

### Step 4: Restart the Bot

The bot will now send alerts to your Telegram when divergence signals are detected.

## 📁 Folder Structure Overview

```
RSI-Divergence/
├── src/               # Core bot code
│   ├── main.py       # Run this file
│   └── strategy.py   # Divergence logic
├── config/           # Settings
│   └── settings.py   # Edit this to customize
├── utils/            # Helper functions
├── tests/            # Testing tools
├── scripts/          # Utility scripts
├── docs/             # Documentation
└── logs/             # Log files (auto-created)
```

## 🛠️ Utility Scripts

### Compare Symbols
```bash
python scripts/compare_symbols.py
```

### Get Current Price
```bash
python scripts/get_price.py
```

### List Available Products
```bash
python scripts/list_products.py
```

## 🔧 Troubleshooting

### Issue: "Module not found" error

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "No data fetched" error

**Solution**: 
- Check internet connection
- Verify Delta Exchange API is accessible
- Try a different symbol in `config/settings.py`

### Issue: Bot not detecting signals

**Solution**:
- Divergences are rare - be patient
- Try backtesting to verify bot works: `python tests/backtest.py`
- Check that RSI values are being calculated (visible in logs)

### Issue: Import errors

**Solution**: Make sure you're running from the project root:
```bash
cd RSI-Divergence
python src/main.py
```

## 📊 Monitoring Logs

Logs are stored in `logs/rsi_divergence.log` with detailed information:
- Every scan shows current price and RSI
- Signal detections are highlighted
- Errors are logged for debugging

## 🔄 Updating the Bot

To update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## ⚙️ Advanced Configuration

### Multiple Symbols

Edit `src/main.py` to loop through multiple symbols:

```python
SYMBOLS = ["BTCUSD", "ETHUSD"]
for symbol in SYMBOLS:
    # ... scanning logic
```

### Different Timeframes

Change in `config/settings.py`:
```python
TIMEFRAME = "1h"  # For hourly divergence scanning
```

## 📈 Performance Tips

1. **Check Interval**: Shorter intervals (60s) for active monitoring, longer intervals (300s) for passive scanning
2. **Timeframe**: Lower timeframes (5m, 15m) for day trading, higher timeframes (1h, 4h) for swing trading
3. **Logs**: Monitor logs regularly to understand bot behavior

## ⚠️ Important Reminders

- This bot identifies **signals**, not guaranteed trades
- Always use proper risk management
- Test thoroughly before using in live trading
- Keep your `.env` file private (never share or commit to git)

---

**Need Help?** Check `docs/RULES.md` for detailed strategy rules and examples.

**Status**: ✅ Ready to run
