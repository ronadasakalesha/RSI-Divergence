from delta_api_helper import DeltaApiHelper
import pandas as pd

api = DeltaApiHelper()
df = api.fetch_candles("BTCUSD", "15m")

# Target Time
target = "2026-01-21 06:45:00+00:00"

row = df[df['time'].astype(str) == target]

if not row.empty:
    print(f"✅ Found Data for {target}:")
    print(f"Close Price: {row['close'].values[0]}")
    print(row[['time', 'open', 'high', 'low', 'close', 'volume']])
else:
    print(f"❌ No data found for {target}. Data range: {df['time'].min()} to {df['time'].max()}")
