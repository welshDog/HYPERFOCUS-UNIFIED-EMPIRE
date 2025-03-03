# BROski Bot Strategy Guide

This guide explains the trading strategies available in BROski Bot and how to configure them for optimal performance.

## Strategy Overview

BROski Bot offers multiple trading strategies with different approaches to market analysis:

| Strategy | Best For | Complexity | Risk Level |
|----------|----------|------------|------------|
| RSI | Range-bound markets | Beginner | Low-Medium |
| MACD | Trending markets | Intermediate | Medium |
| HyperFocus | All market conditions | Advanced | Medium-High |

## 📊 RSI Strategy

### Description
The Relative Strength Index (RSI) strategy is a momentum oscillator that measures the speed and change of price movements. RSI oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions.

### Configuration
```json
"rsi_strategy": {
  "enabled": true,
  "timeframe": "1h",
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30
}
```

### Parameters
- **timeframe**: The chart timeframe to analyze (e.g., "5m", "15m", "1h", "4h")
- **rsi_period**: Number of periods used to calculate RSI (typical: 14)
- **rsi_overbought**: Level considered overbought, triggering sell signals (typical: 70)
- **rsi_oversold**: Level considered oversold, triggering buy signals (typical: 30)

### Recommended Settings
- **Conservative**: rsi_period: 14, rsi_overbought: 75, rsi_oversold: 25
- **Moderate**: rsi_period: 14, rsi_overbought: 70, rsi_oversold: 30
- **Aggressive**: rsi_period: 10, rsi_overbought: 65, rsi_oversold: 35

## 📉 MACD Strategy

### Description
Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. It's calculated by subtracting the 26-period Exponential Moving Average (EMA) from the 12-period EMA.

### Configuration
```json
"macd_strategy": {
  "enabled": true,
  "timeframe": "1h",
  "fast_period": 12,
  "slow_period": 26,
  "signal_period": 9
}
```

### Parameters
- **timeframe**: The chart timeframe to analyze
- **fast_period**: Short-term EMA period (typical: 12)
- **slow_period**: Long-term EMA period (typical: 26)
- **signal_period**: Signal line smoothing period (typical: 9)

### Recommended Settings
- **Standard**: fast_period: 12, slow_period: 26, signal_period: 9
- **Fast-Response**: fast_period: 8, slow_period: 17, signal_period: 9
- **Trend-Focused**: fast_period: 19, slow_period: 39, signal_period: 9

## 🔍 HyperFocus Strategy

### Description
HyperFocus is an advanced multi-timeframe strategy exclusive to BROski Bot. It combines multiple indicators including RSI, MACD, and volume analysis across different timeframes to confirm signals and filter out market noise.

### Configuration
```json
"hyperfocus_strategy": {
  "enabled": true,
  "rsi_period": 14,
  "volume_threshold": 1.5,
  "timeframes": ["15m", "1h", "4h"],
  "sensitivity": "medium"
}
```

### Parameters
- **rsi_period**: Period for RSI calculation within HyperFocus
- **volume_threshold**: Volume increase factor to confirm signals (1.0 = no increase)
- **timeframes**: Array of timeframes to analyze (multi-timeframe confirmation)
- **sensitivity**: Affects how easily signals are generated ("low", "medium", "high")

### Recommended Settings
- **Conservative**: volume_threshold: 2.0, sensitivity: "low", timeframes: ["1h", "4h", "1d"]
- **Balanced**: volume_threshold: 1.5, sensitivity: "medium", timeframes: ["15m", "1h", "4h"]
- **Aggressive**: volume_threshold: 1.2, sensitivity: "high", timeframes: ["5m", "15m", "1h"]

## 📈 Strategy Selection

### How to Choose the Right Strategy

1. **Market Condition Assessment**:
   - Range-bound markets (sideways): Use RSI
   - Strong trends: Use MACD
   - Mixed or uncertain: Use HyperFocus

2. **Timeframe Selection**:
   - Longer timeframes (1h+) for less noise but slower signals
   - Shorter timeframes (5m, 15m) for more signals but more false positives

3. **Risk Tolerance**:
   - Lower risk: Use longer timeframes with conservative settings
   - Higher risk/reward: Use shorter timeframes with aggressive settings

### Enabling a Strategy

To enable a strategy, set it as the active strategy in your configuration:

```json
"strategies": {
  "active_strategy": "rsi_strategy",
  // Strategy configurations...
}
```

## 📚 Backtesting Strategies

BROski Bot includes a backtesting feature to evaluate strategy performance:

```
python backtest.py --strategy rsi --days 30
```

This helps you determine which strategy and settings work best for your trading pair before risking real funds.

## 🔄 Multiple Timeframe Analysis

For the best results, analyze multiple timeframes:

1. Use longer timeframes (4h, 1d) to identify overall market direction
2. Use medium timeframes (1h, 2h) for your primary signals
3. Use shorter timeframes (5m, 15m) for entry/exit timing

This approach is built into the HyperFocus strategy but can also be applied manually with other strategies.

## ⚠️ Risk Management

Always pair your strategy with proper risk management:

- Set appropriate stop-loss and take-profit levels
- Limit position sizes to a small percentage of your portfolio
- Don't trade with funds you cannot afford to lose
- Test strategies with paper trading before using real funds

Remember, no strategy works in all market conditions. Monitor performance and be ready to adjust as needed.
