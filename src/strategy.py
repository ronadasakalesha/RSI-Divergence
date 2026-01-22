"""
RSI Divergence Strategy Logic
Implements the core divergence detection algorithms
"""

def check_divergence(df):
    """
    Checks for Regular Bullish/Bearish Divergence based on STRICT user rules.
    
    RSI DIVERGENCE RULES:
    =====================
    1. Lower the number of candles = Stronger the divergence
    2. Divergence on closing basis (use closing prices)
    3. Minimum 3 candles required, Maximum 7 candles
    4. Color matching:
       - Bearish (Top): Green to Green candles
       - Bullish (Bottom): Red to Red candles
    5. Candle counting includes Point A and Point B
    6. CONFIRMATION CANDLE (NEW):
       - Bullish: After Point B (red), next candle must be GREEN
       - Bearish: After Point B (green), next candle must be RED
    
    DIVERGENCE DEFINITIONS:
    =======================
    - BEARISH Divergence (Top):
      * Price: Higher High (HH)
      * RSI: Lower High (LH)
      * Signal: Potential downward reversal
      
    - BULLISH Divergence (Bottom):
      * Price: Lower Low (LL)
      * RSI: Higher Low (HL)
      * Signal: Potential upward reversal
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Historical candle data with columns: time, open, high, low, close, volume, rsi
        
    Returns:
    --------
    dict or None
        Signal dictionary with divergence details if found, otherwise None
    """
    if df is None or len(df) < 4:  # Minimum 3 candles + 1 confirmation candle
        return None

    # Import here to avoid circular dependency
    from config.settings import MIN_CANDLES, MAX_CANDLES
    
    # The LAST candle is the CONFIRMATION candle
    # Point B is the SECOND-TO-LAST candle
    confirmation_idx = len(df) - 1
    current_idx = len(df) - 2  # Point B is now second-to-last
    
    if current_idx < 0:
        return None
    
    confirmation_candle = df.iloc[confirmation_idx]
    candle_b = df.iloc[current_idx]
    
    # Determine Color of Confirmation Candle
    confirmation_is_green = confirmation_candle['close'] > confirmation_candle['open']
    confirmation_is_red = confirmation_candle['close'] < confirmation_candle['open']
    
    # Determine Color of Candle B (based on closing prices)
    # Green: Close > Open, Red: Close < Open
    b_is_green = candle_b['close'] > candle_b['open']
    b_is_red = candle_b['close'] < candle_b['open']

    # Iterate backwards for Point A (Pivot)
    # Distance = Index_B - Index_A + 1 (includes both points)
    # Min Distance 3 => A = B - 2
    # Max Distance 7 => A = B - 6
    
    # Check shortest distance first (stronger divergence per Rule 1)
    for dist in range(MIN_CANDLES, MAX_CANDLES + 1):
        offset = dist - 1
        prev_idx = current_idx - offset
        
        if prev_idx < 0:
            continue
        
        candle_a = df.iloc[prev_idx]
        
        # Determine Color of Candle A
        a_is_green = candle_a['close'] > candle_a['open']
        a_is_red = candle_a['close'] < candle_a['open']

        # NEW RULE: Volume at Point A must be greater than Volume at Point B
        # NOTE: For Index symbols (like Nifty 50), volume is often 0.
        # We skip this check if volume data is missing.
        if candle_a['volume'] > 0 and candle_b['volume'] > 0:
            volume_valid = candle_a['volume'] > candle_b['volume']
        else:
            volume_valid = True
        
        # NEW RULE: At least one candle in range [Point A, Point B] must touch BB
        # Bearish (Top): Touch Upper Band (High >= BBU)
        # Bullish (Bottom): Touch Lower Band (Low <= BBL)
        
        # Extract range of candles from A to B (inclusive)
        # Indices in slice: 
        # candle_a is at prev_idx
        # candle_b is at current_idx
        # We need all candles from prev_idx to current_idx
        
        # Check for BB columns existence first (in case not calculated)
        has_bb = 'BBU' in df.columns and 'BBL' in df.columns
        
        bb_touched = False
        if has_bb:
            # Slice from Point A to Point B
            range_sq = df.iloc[prev_idx : current_idx + 1]
            
            if confirmation_is_red: # Bearish Divergence Logic
                    # Check if ANY candle High >= Upper Band
                    bb_touched = (range_sq['high'] >= range_sq['BBU']).any()
            elif confirmation_is_green: # Bullish Divergence Logic
                    # Check if ANY candle Low <= Lower Band
                    bb_touched = (range_sq['low'] <= range_sq['BBL']).any()
        else:
            # If BB not calculated, assume valid (or log warning)
            # For safety, we can default to True if we don't have BB data, 
            # but optimally we should have it.
            bb_touched = True 

        # --- CHECK BEARISH DIVERGENCE (Top) ---
        # Rule 4: Green to Green candles
        # Rule 6: Confirmation candle must be RED
        if b_is_green and a_is_green and confirmation_is_red:
            # Price: Higher High (B > A)
            price_higher = candle_b['close'] > candle_a['close']
            # RSI: Lower High (B < A)
            rsi_lower = candle_b['rsi'] < candle_a['rsi']
            
            if price_higher and rsi_lower and volume_valid and bb_touched:
                return {
                    "type": "BEARISH",
                    "strength": f"{dist} candles",
                    "p1_price": candle_a['close'],
                    "p2_price": candle_b['close'],
                    "p1_rsi": candle_a['rsi'],
                    "p2_rsi": candle_b['rsi'],
                    "time": candle_b['time'],
                    "p1_time": candle_a['time'],
                    "confirmation_time": confirmation_candle['time'],
                    "confirmation_close": confirmation_candle['close'],
                    "confirmation_high": confirmation_candle['high'],
                    "confirmation_low": confirmation_candle['low'],
                    # "entry_price": confirmation_candle['low'],  # SELL at LOW of confirmation (INACTIVE)
                    "pattern": "Green-Green-Red",
                    "bb_touched": bb_touched
                }

        # --- CHECK BULLISH DIVERGENCE (Bottom) ---
        # Rule 4: Red to Red candles
        # Rule 6: Confirmation candle must be GREEN
        if b_is_red and a_is_red and confirmation_is_green:
            # Price: Lower Low (B < A)
            price_lower = candle_b['close'] < candle_a['close']
            # RSI: Higher Low (B > A)
            rsi_higher = candle_b['rsi'] > candle_a['rsi']
            
            if price_lower and rsi_higher and volume_valid and bb_touched:
                    return {
                    "type": "BULLISH",
                    "strength": f"{dist} candles",
                    "p1_price": candle_a['close'],
                    "p2_price": candle_b['close'],
                    "p1_rsi": candle_a['rsi'],
                    "p2_rsi": candle_b['rsi'],
                    "time": candle_b['time'],
                    "p1_time": candle_a['time'],
                    "confirmation_time": confirmation_candle['time'],
                    "confirmation_close": confirmation_candle['close'],
                    "confirmation_high": confirmation_candle['high'],
                    "confirmation_low": confirmation_candle['low'],
                    # "entry_price": confirmation_candle['high'],  # BUY at HIGH of confirmation (INACTIVE)
                    "pattern": "Red-Red-Green",
                    "bb_touched": bb_touched
                }
                
    return None
