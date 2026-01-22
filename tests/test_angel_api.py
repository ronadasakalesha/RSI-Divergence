"""
Simple test script to check Angel One candle fetching
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.api_helpers import AngelOneApiHelper
from config.settings import *

print("Testing Angel One API...")
print(f"Symbol: {SYMBOL}")
print(f"Token: {SYMBOL_TOKEN}")
print(f"Exchange: {EXCHANGE}")
print(f"Timeframe: {TIMEFRAME}")
print()

api = AngelOneApiHelper(ANGEL_API_KEY, ANGEL_CLIENT_ID, ANGEL_PASSWORD, ANGEL_TOTP_SECRET)

print("1. Logging in...")
if api.login():
    print("✅ Login successful!")
else:
    print("❌ Login failed!")
    exit(1)

print("\n2. Fetching candles for last 2 days...")
df = api.fetch_candles(SYMBOL_TOKEN, EXCHANGE, TIMEFRAME, days=2)

if df is not None:
    print(f"✅ Fetched {len(df)} candles successfully!")
    print(f"\nFirst candle: {df.iloc[0]['time']}")
    print(f"Last candle: {df.iloc[-1]['time']}")
    print(f"\nSample data:")
    print(df.tail())
else:
    print("❌ Failed to fetch candles")
