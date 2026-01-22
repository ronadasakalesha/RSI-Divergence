"""
RSI Divergence Trading Bot - Main Entry Point
Angel One / Nifty 50 Edition
"""

import sys
import os
import time
import pandas as pd
import pandas_ta as ta
from logzero import logger
from datetime import datetime, timedelta, timezone

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================= CONFIG =================

from config.settings import (
    SYMBOL,
    SYMBOL_TOKEN,
    EXCHANGE,
    TIMEFRAME,
    RSI_PERIOD,
    MIN_CANDLES,
    MAX_CANDLES,
    ANGEL_API_KEY,
    ANGEL_CLIENT_ID,
    ANGEL_PASSWORD,
    ANGEL_TOTP_SECRET,
    BB_PERIOD,
    BB_STD_DEV,
    ENABLE_TELEGRAM_ALERTS
)

from utils.api_helpers import AngelOneApiHelper
from src.strategy import check_divergence
from utils.telegram_helper import send_telegram_alert

# ================= CONSTANTS =================

CANDLE_BUFFER_SECONDS = 15

TIMEFRAME_MINUTES = {
    "ONE_MINUTE": 1,
    "FIVE_MINUTE": 5,
    "FIFTEEN_MINUTE": 15,
    "ONE_HOUR": 60,
    "ONE_DAY": 1440
}

# ================= TIME HELPERS =================

def now_ist():
    return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)


def next_market_open_ist():
    now = now_ist()

    # Weekend handling
    if now.weekday() >= 5:
        days_ahead = 7 - now.weekday()
        now += timedelta(days=days_ahead)

    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)

    # If past market close today → next day
    if now.time() >= datetime.strptime("15:30", "%H:%M").time():
        market_open += timedelta(days=1)

    # Skip weekends
    while market_open.weekday() >= 5:
        market_open += timedelta(days=1)

    return market_open


def get_next_candle_close_time():
    now = now_ist()
    interval = TIMEFRAME_MINUTES.get(TIMEFRAME, 5)

    next_minute = ((now.minute // interval) + 1) * interval

    if next_minute >= 60:
        next_minute %= 60
        return now.replace(minute=next_minute, second=0, microsecond=0) + timedelta(hours=1)

    return now.replace(minute=next_minute, second=0, microsecond=0)


def wait_for_candle_close():
    next_close = get_next_candle_close_time()
    wait_until = next_close + timedelta(seconds=CANDLE_BUFFER_SECONDS)
    wait_seconds = (wait_until - now_ist()).total_seconds()

    if wait_seconds <= 0:
        return True

    # Safety guard
    if wait_seconds > 300:
        logger.warning("[WAIT] Abnormal candle wait skipped")
        return False

    logger.info(
        f"[WAIT] Next candle close at {next_close.strftime('%H:%M:%S')} | "
        f"Sleeping {int(wait_seconds)}s"
    )
    time.sleep(wait_seconds)
    return True


# ================= MAIN =================

def main():
    logger.info("=" * 80)
    logger.info("RSI Divergence Bot - Angel One / Nifty 50")
    logger.info("=" * 80)

    api = AngelOneApiHelper(
        api_key=ANGEL_API_KEY,
        client_id=ANGEL_CLIENT_ID,
        password=ANGEL_PASSWORD,
        totp_secret=ANGEL_TOTP_SECRET
    )

    logger.info("[LOGIN] Logging in...")
    if not api.login():
        logger.error("[ERROR] Login failed")
        return

    logger.info("[SUCCESS] Logged in successfully")
    logger.info("-" * 80)

    last_signal_time = None

    while True:
        try:
            # ===== MARKET CLOSED → WAIT TILL OPEN =====
            if not api.is_market_open():
                next_open = next_market_open_ist()
                sleep_seconds = (next_open - now_ist()).total_seconds()
                sleep_seconds = max(sleep_seconds, 60)

                logger.info(
                    f"[MARKET] Closed. Sleeping until "
                    f"{next_open.strftime('%Y-%m-%d %H:%M')} IST"
                )
                time.sleep(sleep_seconds)
                continue

            # ===== WAIT FOR CANDLE CLOSE =====
            if not wait_for_candle_close():
                continue

            logger.info("[FETCH] Fetching candle data...")

            df = api.fetch_candles(
                symbol_token=SYMBOL_TOKEN,
                exchange=EXCHANGE,
                timeframe=TIMEFRAME,
                days=5
            )

            if df is None or df.empty:
                logger.warning("[WARNING] No candle data received")
                continue

            # ===== UTC → IST =====
            df['time'] = pd.to_datetime(df['time']) + timedelta(hours=5, minutes=30)

            # ===== INDICATORS =====
            df['rsi'] = ta.rsi(df['close'], length=RSI_PERIOD)

            bb = ta.bbands(df['close'], length=BB_PERIOD, std=BB_STD_DEV)
            if bb is not None:
                df['BBL'] = bb[[c for c in bb.columns if c.startswith("BBL")][0]]
                df['BBU'] = bb[[c for c in bb.columns if c.startswith("BBU")][0]]

            # ===== STRATEGY =====
            signal = check_divergence(df)

            last_price = df['close'].iloc[-1]
            last_rsi = df['rsi'].iloc[-1]
            last_time = df['time'].iloc[-1]

            logger.info(
                f"[SCAN] {SYMBOL} | Price={last_price:.2f} | "
                f"RSI={last_rsi:.2f} | Candle={last_time.strftime('%H:%M')}"
            )

            if signal:
                if last_signal_time == signal['confirmation_time']:
                    logger.info("[SKIP] Duplicate signal ignored")
                    continue

                last_signal_time = signal['confirmation_time']

                logger.info("=" * 80)
                logger.info(f"[SIGNAL] {signal['type']} DIVERGENCE")
                logger.info(f"Strength : {signal['strength']}")
                logger.info(f"Pattern  : {signal['pattern']}")
                logger.info(
                    f"Price    : {signal['p1_price']:.2f} → {signal['p2_price']:.2f}"
                )
                logger.info(
                    f"RSI      : {signal['p1_rsi']:.2f} → {signal['p2_rsi']:.2f}"
                )
                logger.info(
                    f"Time     : {signal['confirmation_time'].strftime('%Y-%m-%d %H:%M')}"
                )
                logger.info("=" * 80)

                if ENABLE_TELEGRAM_ALERTS:
                    emoji = "🟢" if signal['type'] == "BULLISH" else "🔴"
                    msg = (
                        f"{emoji} <b>{signal['type']} RSI DIVERGENCE</b>\n\n"
                        f"<b>Symbol:</b> {SYMBOL}\n"
                        f"<b>TF:</b> {TIMEFRAME}\n"
                        f"<b>Time:</b> {signal['confirmation_time'].strftime('%H:%M')}\n"
                        f"<b>Strength:</b> {signal['strength']}\n"
                        f"<b>Pattern:</b> {signal['pattern']}\n"
                        f"<b>Price:</b> {signal['p1_price']:.2f} → {signal['p2_price']:.2f}\n"
                        f"<b>RSI:</b> {signal['p1_rsi']:.2f} → {signal['p2_rsi']:.2f}"
                    )
                    send_telegram_alert(msg)

        except KeyboardInterrupt:
            logger.info("[STOP] Bot stopped manually")
            break
        except Exception as e:
            logger.error(f"[ERROR] {e}")
            time.sleep(30)


if __name__ == "__main__":
    main()
