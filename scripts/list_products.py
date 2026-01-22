import requests
import json

url = "https://api.india.delta.exchange/v2/products"
response = requests.get(url)
data = response.json()

if "result" in data:
    for p in data["result"]:
        # Filter for relevant symbols
        c_type = p.get('contract_type')
        if "BTC" in p["symbol"] and c_type in ["perpetual_futures", "futures"]:
             print(f"Symbol: {p['symbol']}, Type: {c_type}, Quote: {p.get('quote_currency')}")
else:
    print("Failed to fetch products.")
