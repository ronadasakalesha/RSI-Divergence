"""
RSI Divergence Trading Bot - Main Entry Point
Angel One / Nifty 50 Edition

This bot monitors Nifty 50 on Angel One Smart API for RSI divergence patterns.
It identifies potential reversal signals based on price-RSI divergence.
"""
import sys
import os

# Add parent directory to path to allow imports from any location
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import pandas_ta as ta
from logzero import logger
from datetime import datetime, timedelta

# Import configuration
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
    BB_STD_DEV
)

# Import utilities and strategy
from utils.api_helpers import AngelOneApiHelper
from src.strategy import check_divergence

# Buffer time after candle close (in seconds) to ensure data is complete
CANDLE_BUFFER_SECONDS = 15

# Timeframe in minutes
TIMEFRAME_MINUTES = {
    "ONE_MINUTE": 1,
    "FIVE_MINUTE": 5,
    "FIFTEEN_MINUTE": 15,
    "ONE_HOUR": 60,
    "ONE_DAY": 1440
}


def get_next_candle_close_time():
    """
    Calculate the next candle close time based on timeframe.
    For 5-minute candles: closes at :00, :05, :10, :15, etc.
    
    Returns:
        datetime: The next candle close time (IST-aware if possible, or naive IST)
    """
    # Use UTC + 5:30 for IST consistency across environments (Local Windows vs PythonAnywhere UTC)
    from datetime import timezone
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    
    interval_minutes = TIMEFRAME_MINUTES.get(TIMEFRAME, 5)
    
    # Calculate minutes since start of hour
    current_minute = now_ist.minute
    
    # Find the next candle close minute
    next_close_minute = ((current_minute // interval_minutes) + 1) * interval_minutes
    
    # Handle hour rollover
    if next_close_minute >= 60:
        next_close_minute = next_close_minute % 60
        next_close_time = now_ist.replace(minute=next_close_minute, second=0, microsecond=0) + timedelta(hours=1)
    else:
        next_close_time = now_ist.replace(minute=next_close_minute, second=0, microsecond=0)
    
    return next_close_time


def wait_for_candle_close():
    """
    Wait until the next candle closes + buffer time.
    This ensures we fetch complete candle data, not running candle.
    
    Returns:
        bool: True if waited successfully, False if interrupted
    """
    next_close = get_next_candle_close_time()
    wait_until = next_close + timedelta(seconds=CANDLE_BUFFER_SECONDS)
    
    # Use IST for "now" to match "next_close" timezone
    from datetime import timezone
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    
    wait_seconds = (wait_until - now_ist).total_seconds()
    
    if wait_seconds > 0:
        logger.info(f"[WAIT] Next candle closes at {next_close.strftime('%H:%M:%S')}")
        logger.info(f"[WAIT] Waiting {wait_seconds:.0f} seconds (including {CANDLE_BUFFER_SECONDS}s buffer)...")
        time.sleep(wait_seconds)
    
    return True


def main():
    """Main bot loop"""
    logger.info("=" * 80)
    logger.info("RSI Divergence Bot - Angel One / Nifty 50")
    logger.info("=" * 80)
    logger.info(f"Symbol: {SYMBOL}")
    logger.info(f"Timeframe: {TIMEFRAME} ({TIMEFRAME_MINUTES.get(TIMEFRAME, 5)} minutes)")
    logger.info(f"Rules: {MIN_CANDLES}-{MAX_CANDLES} candles, Closing Basis, Color Match")
    logger.info(f"RSI Period: {RSI_PERIOD}")
    logger.info(f"Buffer: {CANDLE_BUFFER_SECONDS} seconds after candle close")
    logger.info(f"Market Hours: 9:15 AM - 3:30 PM IST (Mon-Fri)")
    logger.info("=" * 80)
    
    # Initialize Angel One API
    api = AngelOneApiHelper(
        api_key=ANGEL_API_KEY,
        client_id=ANGEL_CLIENT_ID,
        password=ANGEL_PASSWORD,
        totp_secret=ANGEL_TOTP_SECRET
    )
    
    # Login to Angel One
    logger.info("[LOGIN] Logging in to Angel One...")
    if not api.login():
        logger.error("[ERROR] Failed to login. Please check your credentials.")
        return
    
    logger.info("[SUCCESS] Login successful! Starting monitoring...")
    logger.info("-" * 80)
    
    while True:
        try:
            # Check if market is open
            if not api.is_market_open():
                current_time = datetime.now().strftime("%H:%M:%S")
                logger.info(f"[MARKET] Market closed at {current_time}. Waiting 5 minutes...")
                time.sleep(300)  # Wait 5 minutes if market closed
                continue
            
            # Wait for candle close + buffer time
            wait_for_candle_close()
            
            # Fetch candle data (now fetching closed candle data)
            logger.info("[FETCH] Fetching candle data...")
            df = api.fetch_candles(
                symbol_token=SYMBOL_TOKEN,
                exchange=EXCHANGE,
                timeframe=TIMEFRAME,
                days=5
            )
            
            if df is not None and len(df) > 0:
                # Calculate RSI indicator
                df['rsi'] = ta.rsi(df['close'], length=RSI_PERIOD)
                
                # Calculate Bollinger Bands (Required for Strategy)
                bb = ta.bbands(df['close'], length=BB_PERIOD, std=BB_STD_DEV)
                
                if bb is not None:
                     # Dynamically find the correct column names
                    bbl_col = [c for c in bb.columns if c.startswith('BBL')][0]
                    bbu_col = [c for c in bb.columns if c.startswith('BBU')][0]
                    
                    df['BBL'] = bb[bbl_col]
                    df['BBU'] = bb[bbu_col]
                
                # Check for divergence signal
                signal = check_divergence(df)
                
                # Get current market status (last CLOSED candle)
                last_price = df['close'].iloc[-1]
                last_rsi = df['rsi'].iloc[-1]
                last_time = df['time'].iloc[-1]
                
                logger.info(
                    f"[SCAN] {SYMBOL}: Price={last_price:.2f}, RSI={last_rsi:.2f} "
                    f"[Candle: {last_time.strftime('%H:%M')}]"
                )
                
                if signal:
                    # Signal found - log details
                    logger.info("=" * 80)
                    logger.info(f"[SIGNAL] {signal['type']} DIVERGENCE DETECTED!")
                    logger.info(f"   Strength: {signal['strength']}")
                    logger.info(f"   Pattern: {signal['pattern']}")
                    logger.info(f"   Price: {signal['p1_price']:.2f} -> {signal['p2_price']:.2f}")
                    logger.info(f"   RSI:   {signal['p1_rsi']:.2f} -> {signal['p2_rsi']:.2f}")
                    logger.info(f"   Point A: {signal['p1_time'].strftime('%Y-%m-%d %H:%M:%S')}")
                    logger.info(f"   Point B: {signal['time'].strftime('%Y-%m-%d %H:%M:%S')}")
                    logger.info(f"   Confirmation: {signal['confirmation_time'].strftime('%Y-%m-%d %H:%M:%S')}")
                    logger.info("-" * 40)
                    if signal['type'] == 'BULLISH':
                        # logger.info(f"   ENTRY: BUY above {signal['entry_price']:.2f} (High of confirmation)")
                        pass
                    else:
                        # logger.info(f"   ENTRY: SELL below {signal['entry_price']:.2f} (Low of confirmation)")
                        pass
                    logger.info("=" * 80)
                    
                    # Send Telegram Alert
                    from utils.telegram_helper import send_telegram_alert
                    from config.settings import ENABLE_TELEGRAM_ALERTS
                    
                    if ENABLE_TELEGRAM_ALERTS:
                        # Construct message
                        trend_emoji = "🟢" if signal['type'] == "BULLISH" else "🔴"
                        # entry_msg = (f"BUY above {signal['entry_price']:.2f}" 
                        #            if signal['type'] == "BULLISH" 
                        #            else f"SELL below {signal['entry_price']:.2f}")
                        
                        bb_msg = ""
                        if signal.get('bb_touched'):
                             bb_msg = f"\n🌊 <b>Bollinger Band Touched</b>"
                        
                        msg = (
                            f"{trend_emoji} <b>{signal['type']} DIVERGENCE DETECTED</b> {trend_emoji}\n\n"
                            f"<b>Symbol:</b> {SYMBOL}\n"
                            f"<b>Timeframe:</b> {TIMEFRAME}\n"
                            f"<b>Time:</b> {signal['confirmation_time'].strftime('%Y-%m-%d %H:%M')}\n\n"
                            f"<b>Strength:</b> {signal['strength']}\n"
                            f"<b>Pattern:</b> {signal['pattern']}\n"
                            f"<b>Price:</b> {signal['p1_price']:.2f} → {signal['p2_price']:.2f}\n"
                            f"<b>RSI:</b> {signal['p1_rsi']:.2f} → {signal['p2_rsi']:.2f}\n"
                            f"{bb_msg}\n"
                            f"--------------------------------"
                            # f"\n<b>ENTRY:</b> {entry_msg}"
                        )
                        
                        logger.info(f"[TELEGRAM] Sending alert...")
                        send_telegram_alert(msg)
                    
            else:
                logger.warning("[WARNING] Failed to fetch data from Angel One")
                # Try to re-login
                logger.info("[RETRY] Attempting to re-login...")
                api.login()
                time.sleep(10)  # Wait before retry
                
        except KeyboardInterrupt:
            logger.info("[STOP] Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"[ERROR] Error in main loop: {e}")
            logger.info("[WAIT] Waiting 30 seconds before retry...")
            time.sleep(30)


if __name__ == "__main__":
    main()
