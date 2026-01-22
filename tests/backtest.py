"""
Backtest Runner - Saves results to file
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from logzero import logger

from config.settings import (
    SYMBOL, SYMBOL_TOKEN, EXCHANGE, TIMEFRAME, RSI_PERIOD,
    ANGEL_API_KEY, ANGEL_CLIENT_ID, ANGEL_PASSWORD, ANGEL_TOTP_SECRET,
    BB_PERIOD, BB_STD_DEV
)
from utils.api_helpers import AngelOneApiHelper
from src.strategy import check_divergence

BACKTEST_DAYS = 2

def run_backtest():
    output = []
    output.append("=" * 100)
    output.append(f"🔄 RSI Divergence Backtest - {SYMBOL}")
    output.append(f"📅 Period: Last {BACKTEST_DAYS} days")
    output.append(f"⏰ Timeframe: {TIMEFRAME}")
    output.append("=" * 100)
    
    # Login
    output.append("\n🔐 Logging in to Angel One...")
    api = AngelOneApiHelper(ANGEL_API_KEY, ANGEL_CLIENT_ID, ANGEL_PASSWORD, ANGEL_TOTP_SECRET)
    
    if not api.login():
        output.append("❌ Failed to login to Angel One")
        return "\n".join(output)
    
    output.append("✅ Login successful!")
    
    # Fetch data
    output.append(f"\n📊 Fetching {BACKTEST_DAYS} days of historical data...")
    df = api.fetch_candles(SYMBOL_TOKEN, EXCHANGE, TIMEFRAME, days=BACKTEST_DAYS + 2)
    
    if df is None or df.empty:
        output.append("❌ Failed to fetch historical data")
        return "\n".join(output)
    
    # Calculate RSI
    df['rsi'] = ta.rsi(df['close'], length=RSI_PERIOD)

    # Calculate Bollinger Bands
    bb = ta.bbands(df['close'], length=BB_PERIOD, std=BB_STD_DEV)
    
    # Dynamically find the correct column names
    # Expected pattern: BBL_length_std, but sometimes version specific
    bbl_col = [c for c in bb.columns if c.startswith('BBL')][0]
    bbu_col = [c for c in bb.columns if c.startswith('BBU')][0]
    
    # Assign specific columns
    df['BBL'] = bb[bbl_col]
    df['BBU'] = bb[bbu_col]
    
    # Filter for last BACKTEST_DAYS
    from datetime import timezone
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=BACKTEST_DAYS)
    df = df[df['time'] >= start_time].reset_index(drop=True)
    
    output.append(f"\n📊 Loaded {len(df)} candles")
    output.append(f"🕐 Start: {df['time'].iloc[0]}")
    output.append(f"🕑 End:   {df['time'].iloc[-1]}")
    output.append(f"💰 Price Range: {df['close'].min():.2f} - {df['close'].max():.2f}")
    output.append(f"📈 RSI Range: {df['rsi'].min():.2f} - {df['rsi'].max():.2f}")
    
    # Run backtest
    output.append(f"\n🔍 Scanning for divergence signals...")
    signals = []
    start_index = RSI_PERIOD + 7
    
    for i in range(start_index, len(df)):
        current_slice = df.iloc[:i+1].copy()
        signal = check_divergence(current_slice)
        
        if signal:
            signal['index'] = i
            signal['candle_time'] = df.iloc[i]['time']
            signals.append(signal)
    
    # Report results
    output.append("\n" + "=" * 100)
    output.append(f"✅ Backtest Complete! Found {len(signals)} Divergence Signal(s)")
    output.append("=" * 100)
    
    if len(signals) == 0:
        output.append("\n⚠️  No divergence signals found in the last 2 days.")
        output.append("💡 This is normal - divergence signals are relatively rare.")
    else:
        output.append(f"\n{'#':<3} | {'TIME':<20} | {'TYPE':<8} | {'STRENGTH':<10} | {'PATTERN':<12} | {'PRICE':<25} | {'RSI':<20}")
        output.append("-" * 110)
        
        for idx, s in enumerate(signals, 1):
            time_str = s['candle_time'].strftime('%Y-%m-%d %H:%M')
            price_str = f"{s['p1_price']:.2f} → {s['p2_price']:.2f}"
            rsi_str = f"{s['p1_rsi']:.2f} → {s['p2_rsi']:.2f}"
            
            output.append(f"{idx:<3} | {time_str:<20} | {s['type']:<8} | {s['strength']:<10} | {s['pattern']:<12} | {price_str:<25} | {rsi_str:<20}")
        
        # Detailed breakdown
        output.append("\n" + "=" * 100)
        output.append("📋 DETAILED SIGNAL BREAKDOWN")
        output.append("=" * 100)
        
        for idx, s in enumerate(signals, 1):
            output.append(f"\n🔔 Signal #{idx}: {s['type']} DIVERGENCE")
            output.append(f"   ⏰ Detected at: {s['candle_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"   📊 Strength: {s['strength']}")
            output.append(f"   🎨 Pattern: {s['pattern']}")
            output.append(f"   📍 Point A Time: {s['p1_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"   📍 Point B Time: {s['time'].strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"   💰 Price Movement: {s['p1_price']:.2f} → {s['p2_price']:.2f}")
            output.append(f"   📈 RSI Movement: {s['p1_rsi']:.2f} → {s['p2_rsi']:.2f}")
            
            if s.get('bb_touched'):
                 output.append(f"   🌊 Bollinger Band: Touched ({'Upper' if s['type'] == 'BEARISH' else 'Lower'})")
            
            if s['type'] == 'BULLISH':
                output.append(f"   💡 Interpretation: Price made lower low but RSI made higher low → Potential upward reversal")
            else:
                output.append(f"   💡 Interpretation: Price made higher high but RSI made lower high → Potential downward reversal")
    
    output.append("\n" + "=" * 100)
    output.append("✅ Backtest Completed Successfully!")
    output.append("=" * 100)
    
    return "\n".join(output)

if __name__ == "__main__":
    result = run_backtest()
    print(result)
    
    # Save to file
    with open("logs/backtest_results.txt", "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"\n📄 Results saved to: logs/backtest_results.txt")
