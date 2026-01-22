# RSI Divergence Trading Rules

Complete documentation of the RSI Divergence strategy rules and patterns.

## 📊 Core Concept

**Divergence** occurs when price action and the RSI indicator move in opposite directions, signaling a potential trend reversal.

## 🎯 Divergence Types

### Bearish Divergence (Top)

**Signal**: Potential **downward reversal**

**Pattern**:
- **Price**: Makes a **Higher High (HH)** - New peak above previous peak
- **RSI**: Makes a **Lower High (LH)** - RSI peak below previous RSI peak
- **Candle Color**: Green to Green (both candles have Close > Open)

**Visual Example**:
```
Price Chart:
    Point B (HH) 📈📈
   /
  /  Point A (H) 📈
 /

RSI Chart:
 Point A (H) 📊
  \
   \  Point B (LH) 📉
    \
```

**Interpretation**: Price is making new highs but RSI is weakening → Momentum is declining → Potential sell signal

---

### Bullish Divergence (Bottom)

**Signal**: Potential **upward reversal**

**Pattern**:
- **Price**: Makes a **Lower Low (LL)** - New trough below previous trough
- **RSI**: Makes a **Higher Low (HL)** - RSI trough above previous RSI trough
- **Candle Color**: Red to Red (both candles have Close < Open)

**Visual Example**:
```
Price Chart:
  \
   \  Point A (L) 📉
    \
     Point B (LL) 📉📉

RSI Chart:
    \
     \  Point B (HL) 📈
      \
   Point A (L) 📊
```

**Interpretation**: Price is making new lows but RSI is strengthening → Momentum is increasing → Potential buy signal

---

## 📏 Strategy Rules

### Rule 1: Divergence Strength
**Lower number of candles = Stronger divergence**

- 3-candle divergence → **Strongest** 💪
- 4-candle divergence → Very Strong
- 5-candle divergence → Strong
- 6-candle divergence → Moderate
- 7-candle divergence → **Weakest** (but still valid)

### Rule 2: Closing Basis
**All comparisons use CLOSING prices**

- Price comparison: Compare candle **close** values
- Candle color: Determined by **close vs open**
  - Green candle: Close > Open
  - Red candle: Close < Open
- RSI values: Calculated from **closing prices**

### Rule 3: Distance Requirement
**Minimum: 3 candles | Maximum: 7 candles**

- **Minimum 3 candles**: At least 2 candles between Point A and Point B
- **Maximum 7 candles**: No more than 6 candles between Point A and Point B
- **Counting**: Includes both Point A (start) and Point B (end)

**Example**:
```
Point A → Candle → Candle → Point B = 4-candle divergence
```

### Rule 4: Color Matching
**Candle colors must match the divergence type**

| Divergence Type | Point A Color | Point B Color |
|----------------|---------------|---------------|
| **Bearish** (Top) | Green ✅ | Green ✅ |
| **Bullish** (Bottom) | Red 🔴 | Red 🔴 |

**Why?**
- Bearish divergence occurs at **tops** → Look for green (bullish) candles
- Bullish divergence occurs at **bottoms** → Look for red (bearish) candles

### Rule 5: Candle Counting
**Both Point A and Point B are included in the count**

Distance calculation:
```
Distance = Index_B - Index_A + 1
```

**Example**:
- Point A at index 10
- Point B at index 12
- Distance = 12 - 10 + 1 = **3 candles** ✅

---

## ✅ Valid Divergence Examples

### Example 1: Bullish Divergence (3 candles)

| Candle | Time | Close | Color | RSI |
|--------|------|-------|-------|-----|
| Point A | 10:00 | 45,000 | Red | 28.5 |
| Candle | 10:15 | 45,200 | Green | 32.0 |
| **Point B** | **10:30** | **44,800** | **Red** | **31.2** |

**Analysis**:
- ✅ Distance: 3 candles
- ✅ Color: Red to Red
- ✅ Price: Lower Low (44,800 < 45,000)
- ✅ RSI: Higher Low (31.2 > 28.5)
- **Result**: Valid Bullish Divergence - Potential buy signal

---

### Example 2: Bearish Divergence (5 candles)

| Candle | Time | Close | Color | RSI |
|--------|------|-------|-------|-----|
| Point A | 14:00 | 48,000 | Green | 72.3 |
| Candle | 14:15 | 47,800 | Red | 68.5 |
| Candle | 14:30 | 48,200 | Green | 70.1 |
| Candle | 14:45 | 47,900 | Red | 66.8 |
| **Point B** | **15:00** | **48,500** | **Green** | **69.5** |

**Analysis**:
- ✅ Distance: 5 candles
- ✅ Color: Green to Green
- ✅ Price: Higher High (48,500 > 48,000)
- ✅ RSI: Lower High (69.5 < 72.3)
- **Result**: Valid Bearish Divergence - Potential sell signal

---

## ❌ Invalid Divergence Examples

### Example 1: Wrong Color Pattern

| Candle | Time | Close | Color | RSI |
|--------|------|-------|-------|-----|
| Point A | 10:00 | 45,000 | **Green** | 28.5 |
| Point B | 10:15 | 44,800 | **Red** | 31.2 |

**Analysis**:
- ❌ Color mismatch: Green to Red (should be Red to Red for bullish)
- **Result**: **NOT** a valid divergence

---

### Example 2: Distance Too Short

| Candle | Time | Close | Color | RSI |
|--------|------|-------|-------|-----|
| Point A | 10:00 | 45,000 | Red | 28.5 |
| **Point B** | **10:15** | **44,800** | **Red** | **31.2** |

**Analysis**:
- ❌ Distance: Only 2 candles (minimum is 3)
- **Result**: **NOT** a valid divergence

---

### Example 3: Distance Too Long

| Candle | Time | Close | Color | RSI |
|--------|------|-------|-------|-----|
| Point A | 10:00 | 45,000 | Red | 28.5 |
| ...8+ candles... | ... | ... | ... | ... |
| Point B | 12:00 | 44,800 | Red | 31.2 |

**Analysis**:
- ❌ Distance: More than 7 candles
- **Result**: **NOT** a valid divergence

---

## 🎨 Pattern Recognition Tips

1. **Look for extremes**: Divergences typically form at market tops (bearish) or bottoms (bullish)

2. **Confirm with candle color**: Color matching ensures you're comparing like-to-like patterns

3. **Prefer shorter distances**: 3-4 candle divergences are typically more reliable than 6-7 candle divergences

4. **Wait for confirmation**: The divergence signal appears when Point B candle **closes**

5. **Use with other indicators**: Divergence works best when combined with support/resistance, volume, or other technical indicators

---

## 📐 RSI Settings

- **RSI Period**: 14 (standard)
- **Overbought**: 70 (bearish divergence often occurs here)
- **Oversold**: 30 (bullish divergence often occurs here)

---

## ⚠️ Important Notes

- **False signals**: Not all divergences lead to reversals. Use proper risk management.
- **Timeframes**: Strategy works on any timeframe (5m, 15m, 1h, etc.)
- **Confirmation**: Consider waiting for price action confirmation before entering trades
- **Stop loss**: Always use stop losses to manage risk

---

**Remember**: Divergence indicates **potential** reversal, not guaranteed reversal. Always use proper risk management and confirm with other technical analysis tools.
