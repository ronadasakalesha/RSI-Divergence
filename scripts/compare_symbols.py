from delta_api_helper import DeltaApiHelper
import pandas as pd

api = DeltaApiHelper()

target_time = "2026-01-21 06:45:00+00:00"

for sym in ["BTCUSD", "BTC-USDT", "BTC_USDT", "BTC-PERP"]:
    print(f"\nScanning {sym}...")
    df = api.fetch_candles(sym, "15m")
    if df is not None:
        row = df[df['time'].astype(str) == target_time]
        if not row.empty:
            print(f"Data for {target_time}:")
            print(row[['time', 'open', 'high', 'low', 'close']].to_string(index=False))
        else:
            print("Time not found.")
    else:
        print("Failed to fetch.")
