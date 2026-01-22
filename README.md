
# 🤖 RSI Divergence Trading Bot

This `README.md` details exactly what the **RSI Divergence Bot** does in its current configuration.

## 1. 🕒 Timing & Schedule
*   **Operating Hours:** 09:15 AM to 03:30 PM IST (Monday - Friday).
*   **Timezone Handling:** Automatically syncs with IST (UTC +5:30), allowing accurate operation on international servers like PythonAnywhere.
*   **Execution Cycle:** The bot runs on a **5-minute cycle**:
    1.  It calculates exactly when the next 5-minute candle will close (e.g., 09:20, 09:25).
    2.  It waits until that time **plus a 15-second buffer** (e.g., 09:20:15) to ensure data is finalized by the broker.
*   **Market Status:** If the market is closed, the bot pauses and checks again every 5 minutes.

## 2. 📊 Data Processing
*   **Asset:** NIFTY 50 Index.
*   **Source:** Angel One Smart API.
*   **Data Frame:** Fetches the last 5 days of 5-minute candles to ensure enough history for calculations.
*   **Technical Indicators:**
    *   **RSI (Relative Strength Index):** Period 14.
    *   **Bollinger Bands:** Period 20, Standard Deviation 2.

## 3. 🧠 The Strategy Logic
Every 5 minutes, the bot scans **closed candles** for a valid signal. A signal is only generated if **ALL** the following strict conditions are met:

### A. The Setup (Point A ➔ Point B)
*   **Bearish Divergence (Top Reversal):**
    *   Price Close at B is **Higher** than at A (Higher High).
    *   RSI at B is **Lower** than at A (Lower High).
*   **Bullish Divergence (Bottom Reversal):**
    *   Price Close at B is **Lower** than at A (Lower Low).
    *   RSI at B is **Higher** than at A (Higher Low).

### B. Strict Filtering Rules
1.  **Candle Distance:** Point A and Point B must be **3 to 7 candles** apart.
2.  **Color Matching:**
    *   **Bearish:** Candle A and Candle B must both be **GREEN**.
    *   **Bullish:** Candle A and Candle B must both be **RED**.
3.  **Volume Validation:** Volume at Point A must be > Volume at Point B (Skipped if volume is 0).
4.  **🌊 Bollinger Band Filter:**
    *   **Bearish:** At least one candle between A and B (inclusive) must have touched the **Upper Bollinger Band**.
    *   **Bullish:** At least one candle between A and B (inclusive) must have touched the **Lower Bollinger Band**.

### C. The Confirmation Trigger
The bot does **not** signal immediately at Point B. It waits for one additional candle (the Confirmation Candle).
*   **Bearish Signal Trigger:** Requires a **RED** candle immediately following Point B.
*   **Bullish Signal Trigger:** Requires a **GREEN** candle immediately following Point B.

## 4. 📢 Output & Alerts
When a Valid Signal is Detected:

1.  **Telegram Alert:** Sends a formatted message to your channel.
    *   *Includes:* Signal Type (Bullish/Bearish), Time, Pattern (e.g., Green-Green-Red), and Confirmation of BB Touch.
2.  **Console Logging:** Logs detailed trade data to the terminal/server logs.

### 🚫 Inactive Features (Current State)
*   **Entry Instructions:** The bot currently **does not** suggest specific "Buy Above/Sell Below" prices (Disabled).
*   **Auto-Trading:** The bot is a **Scanner Only**. It does not place live orders.

---
**Summary:** The bot is a high-precision scanner that filters out noise by enforcing strict structural rules, Bollinger Band interactions, and confirmation candles before flagging a potential Nifty 50 reversal.

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
│   └── api_helpers.py     # API Helper (Angel One)
├── tests/                 # Testing and debugging
│   ├── __init__.py
│   └── backtest.py        # Backtesting script
├── docs/                  # Documentation
│   ├── RULES.md          # Detailed trading rules
│   └── SETUP.md          # Setup instructions
├── logs/                  # Log files (gitignored)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start & Deployment

See [docs/PYTHONANYWHERE_SETUP.md](docs/PYTHONANYWHERE_SETUP.md) for deployment instructions.
