import pandas as pd
import unittest
from bot import check_divergence

class TestRSIDivergence(unittest.TestCase):
    
    def create_candle(self, open_p, close_p, rsi, time="2024-01-01 12:00:00"):
        return {
            "time": time,
            "open": open_p, 
            "close": close_p, 
            "rsi": rsi, 
            "high": max(open_p, close_p) + 10, 
            "low": min(open_p, close_p) - 10,
            "volume": 100
        }

    def test_bullish_divergence_valid(self):
        """
        Valid 3-candle Shortest Distance Bullish Divergence (Red to Red)
        """
        data = [
            # A (Red, Low Price, Low RSI)
            self.create_candle(100, 90, 30), 
            self.create_candle(92, 95, 35), # Noise
            # B (Red, Lower Price, Higher RSI)
            self.create_candle(88, 85, 32)  
        ]
        df = pd.DataFrame(data)
        result = check_divergence(df)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], "BULLISH")
        self.assertEqual(result['strength'], "3 candles")
        print("✅ test_bullish_divergence_valid Passed")

    def test_bearish_divergence_valid(self):
        """
        Valid 3-candle Bearish Divergence (Green to Green)
        """
        data = [
            # A (Green, High Price, High RSI)
            self.create_candle(100, 110, 70), 
            self.create_candle(108, 105, 65), # Noise
            # B (Green, Higher Price, Lower RSI)
            self.create_candle(112, 115, 68)  
        ]
        df = pd.DataFrame(data)
        result = check_divergence(df)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], "BEARISH")
        self.assertEqual(result['strength'], "3 candles")
        print("✅ test_bearish_divergence_valid Passed")

    def test_invalid_color_bullish(self):
        """
        Found Price/RSI Divergence but Candle colors Mismatch (Green to Red)
        Should be Ignored.
        """
        data = [
            # A (Green! - Should be Red for Bullish)
            self.create_candle(90, 100, 30), 
            self.create_candle(95, 92, 35), 
            # B (Red, Lower Close than A, Higher RSI than A)
            self.create_candle(98, 95, 32)
            # wait, Close A=100, Close B=95. Higher RSI check: 32 > 30.
            # Divergence exists mathematically, but Color Rule checks A/B match.
        ]
        df = pd.DataFrame(data)
        result = check_divergence(df)
        self.assertIsNone(result, "Should fail because A is Green")
        print("✅ test_invalid_color_bullish Passed")

    def test_distance_too_long(self):
        """
        Divergence valid but 8 candles apart (Max is 7)
        """
        data = [self.create_candle(100, 90, 30)] # A
        # 6 candles in between (Total distance 8)
        for _ in range(6):
            data.append(self.create_candle(90, 90, 35))
        # B
        data.append(self.create_candle(88, 85, 32))

        df = pd.DataFrame(data)
        # Total len = 1 + 6 + 1 = 8
        
        result = check_divergence(df)
        self.assertIsNone(result)
        print("✅ test_distance_too_long Passed")

if __name__ == '__main__':
    unittest.main()
