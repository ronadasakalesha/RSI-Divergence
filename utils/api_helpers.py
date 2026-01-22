"""
API Helpers for Angel One Smart API
"""
import time  # ✅ FIX: required for sleep
import pyotp
import pandas as pd
from datetime import datetime, timedelta
from logzero import logger
from SmartApi import SmartConnect


class AngelOneApiHelper:
    """Helper class for Angel One Smart API interactions"""
    
    def __init__(self, api_key, client_id, password, totp_secret):
        """
        Initialize Angel One API client
        """
        self.api_key = api_key
        self.client_id = client_id
        self.password = password
        self.totp_secret = totp_secret
        self.smart_api = None
        self.auth_token = None
        self.refresh_token = None
        self.feed_token = None
        
    def login(self):
        """
        Login to Angel One and get authentication tokens
        """
        try:
            # Initialize SmartConnect
            self.smart_api = SmartConnect(api_key=self.api_key)
            
            # Generate TOTP
            totp = pyotp.TOTP(self.totp_secret).now()
            
            # Login
            data = self.smart_api.generateSession(
                clientCode=self.client_id,
                password=self.password,
                totp=totp
            )
            
            if data['status']:
                self.auth_token = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token = data['data']['feedToken']
                
                logger.info("[INFO] Successfully logged in to Angel One")
                return True
            else:
                logger.error(f"[ERROR] Login failed: {data.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"[ERROR] Exception during login: {e}")
            return False
    
    def fetch_candles(self, symbol_token, exchange, timeframe, days=5):
        """
        Fetches historical candles from Angel One
        """
        try:
            # Ensure we're logged in
            if not self.smart_api or not self.auth_token:
                logger.warning("[WARN] Not logged in. Attempting login...")
                if not self.login():
                    return None
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)
            
            # Format dates
            from_date_str = from_date.strftime("%Y-%m-%d %H:%M")
            to_date_str = to_date.strftime("%Y-%m-%d %H:%M")
            
            params = {
                "exchange": exchange,
                "symboltoken": symbol_token,
                "interval": timeframe,
                "fromdate": from_date_str,
                "todate": to_date_str
            }
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.smart_api.getCandleData(params)
                    
                    if response is None:
                        logger.warning(
                            f"[WARN] Attempt {attempt+1}/{max_retries}: API returned None"
                        )
                        time.sleep(2)
                        continue
                        
                    if response.get('status') and response.get('data'):
                        data = response['data']
                        
                        cols = ["time", "open", "high", "low", "close", "volume"]
                        df = pd.DataFrame(data, columns=cols)
                        
                        df["time"] = pd.to_datetime(df["time"])
                        
                        for col in ["open", "high", "low", "close", "volume"]:
                            df[col] = pd.to_numeric(df[col])
                        
                        df = df.sort_values("time").reset_index(drop=True)
                        
                        logger.info(f"[INFO] Fetched {len(df)} candles from Angel One")
                        return df
                    else:
                        msg = response.get('message', 'Unknown error')
                        logger.warning(
                            f"[WARN] Attempt {attempt+1}/{max_retries} failed: {msg}"
                        )
                        
                        # Token invalid → re-login
                        if any(x in str(msg).lower() for x in ["token", "auth", "unauthorized"]):
                            logger.info("[INFO] Token issue detected. Re-logging in...")
                            if self.login():
                                continue
                        
                        time.sleep(2 * (attempt + 1))
                        
                except Exception as e:
                    logger.error(
                        f"[ERROR] Exception on attempt {attempt+1}: {e}"
                    )
                    time.sleep(2)
                    
            return None
                
        except Exception as e:
            logger.error(f"[ERROR] Exception fetching candles: {e}")
            return None
    
    def is_market_open(self):
        """
        Check if Indian stock market is currently open.
        Compatible with PythonAnywhere (UTC server).
        """
        from config.settings import (
            MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE,
            MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE,
            TRADING_DAYS
        )
        
        # PythonAnywhere uses UTC time. We need to convert it to IST.
        # IST = UTC + 5:30
        now_utc = datetime.utcnow()
        now_ist = now_utc + timedelta(hours=5, minutes=30)
        
        if now_ist.weekday() not in TRADING_DAYS:
            return False
        
        market_open = now_ist.replace(
            hour=MARKET_OPEN_HOUR,
            minute=MARKET_OPEN_MINUTE,
            second=0,
            microsecond=0
        )
        market_close = now_ist.replace(
            hour=MARKET_CLOSE_HOUR,
            minute=MARKET_CLOSE_MINUTE,
            second=0,
            microsecond=0
        )
        
        return market_open <= now_ist <= market_close
