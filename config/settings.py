"""
RSI Divergence Strategy Configuration
Centralized settings for the trading bot - Angel One / Nifty 50
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== SYMBOL CONFIGURATION ====================
# Primary symbol for Angel One
SYMBOL = "NIFTY 50"
SYMBOL_TOKEN = "99926000"  # Angel One symbol token for Nifty 50 index
EXCHANGE = "NSE"

# ==================== TIMEFRAME CONFIGURATION ====================
TIMEFRAME = "FIVE_MINUTE"  # Angel One format - 5 minute candles

# Supported timeframes for Angel One
SUPPORTED_TIMEFRAMES = {
    "1m": "ONE_MINUTE",
    "5m": "FIVE_MINUTE",
    "15m": "FIFTEEN_MINUTE",
    "1h": "ONE_HOUR",
    "1d": "ONE_DAY"
}

# ==================== RSI CONFIGURATION ====================
# ==================== RSI CONFIGURATION ====================
RSI_PERIOD = 14  # Standard RSI period

# ==================== BOLLINGER BANDS CONFIGURATION ====================
BB_PERIOD = 20
BB_STD_DEV = 2.0

# ==================== STRATEGY RULES ====================
# Rule 1: Lower the number of candles = stronger the divergence
# Rule 2: Divergence on closing basis
# Rule 3: Minimum and maximum candle distance
# Rule 3: Minimum and maximum candle distance
MIN_CANDLES = 3  # Minimum distance between Point A and Point B
MAX_CANDLES = 7  # Maximum distance between Point A and Point B

# Rule 4: Color matching rules
# - Bearish (Top): Green to Green candles
# - Bullish (Bottom): Red to Red candles

# Rule 5: Candle counting includes Point A and Point B

# ==================== BOT CONFIGURATION ====================
CHECK_INTERVAL = 60  # Check every 60 seconds (1 minute)

# ==================== MARKET HOURS CONFIGURATION ====================
# Indian market trading hours (IST)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 15
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# Trading days
TRADING_DAYS = [0, 1, 2, 3, 4]  # Monday to Friday (0=Monday, 6=Sunday)

# ==================== ANGEL ONE API CONFIGURATION ====================
ANGEL_API_KEY = os.getenv("ANGEL_API_KEY", "")
ANGEL_CLIENT_ID = os.getenv("ANGEL_CLIENT_ID", "")
ANGEL_PASSWORD = os.getenv("ANGEL_PASSWORD", "")
ANGEL_TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET", "")

# Validate required credentials
if not all([ANGEL_API_KEY, ANGEL_CLIENT_ID, ANGEL_PASSWORD]):
    raise ValueError("Missing Angel One credentials. Please check your .env file.")

# ==================== TELEGRAM CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ENABLE_TELEGRAM_ALERTS = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

# ==================== LOGGING CONFIGURATION ====================
LOG_LEVEL = "INFO"  # INFO, DEBUG, WARNING, ERROR
LOG_FILE = "logs/rsi_divergence.log"

# ==================== DISPLAY SETTINGS ====================
SHOW_DETAILED_LOGS = True  # Show detailed signal information
