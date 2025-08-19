# BROski Bot Trading Strategies

This document explains each trading strategy included in BROski Bot, how they work, and how to configure them for best results.

## Strategy Overview

BROski includes multiple trading strategies:

| Strategy | Complexity | Good For | Risk Level |
|----------|------------|----------|------------|
| RSI | Beginner | Range-bound markets | Low-Medium |
| MACD | Intermediate | Trending markets | Medium |
| HyperFocus | Advanced | All market conditions | Medium-High |

## RSI Strategy

### Overview
The Relative Strength Index (RSI) strategy is built on a momentum oscillator that measures the speed and change of price movements. It generates buy signals in oversold conditions and sell signals in overbought conditions.

### How It Works
1. Calculates RSI over a specified period (typically 14 candles)
2. Generates **BUY signal** when RSI crosses above the oversold threshold
3. Generates **SELL signal** when RSI crosses below the overbought threshold

### Configuration
```json
"rsi_strategy": {
  "enabled": true,
  "timeframe": "5m",
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30
}
```

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| timeframe | Chart interval | 1m, 5m, 15m, 1h |
| rsi_period | Periods for RSI calculation | 9-21 (14 standard) |
| rsi_overbought | Threshold for sell signals | 65-80 |
| rsi_oversold | Threshold for buy signals | 20-35 |

### Best For
- Sideways/ranging markets
- Short-term trading
- Markets with clear support/resistance

### Not Ideal For
- Strong trending markets
- Low volatility periods

## MACD Strategy

### Overview
The Moving Average Convergence Divergence (MACD) strategy uses the relationship between moving averages to identify trend direction, momentum changes, and potential reversals.

### How It Works
1. Calculates the MACD line (difference between fast and slow EMAs)
2. Calculates the signal line (EMA of the MACD line)
3. Generates **BUY signal** when MACD line crosses above signal line
4. Generates **SELL signal** when MACD line crosses below signal line

### Configuration
```json
"macd_strategy": {
  "enabled": true,
  "timeframe": "15m",
  "fast_period": 12,
  "slow_period": 26,
  "signal_period": 9
}
```

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| timeframe | Chart interval | 15m, 1h, 4h |
| fast_period | Fast EMA period | 8-16 |
| slow_period | Slow EMA period | 20-30 |
| signal_period | Signal line period | 7-12 |

### Best For
- Trending markets
- Medium-term trading
- Capturing momentum

### Not Ideal For
- Choppy/sideways markets
- Very low timeframes

## HyperFocus Strategy

### Overview
HyperFocus is BROski's advanced multi-indicator strategy that combines several technical indicators for higher accuracy. It uses cross-confirmation from multiple signals and timeframes to filter out poor trades.

### How It Works
1. Analyzes multiple indicators: RSI, MACD, Moving Averages, Volume
2. Requires confirmation from multiple indicators before generating signals
3. Uses volume confirmation for stronger signals
4. Applies smart exit tactics to lock in profits

### Configuration
```json
"hyperfocus_strategy": {
  "enabled": true,
  "timeframe": "15m",
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30,
  "fast_period": 12,
  "slow_period": 26,
  "signal_period": 9,
  "ma_fast": 20,
  "ma_slow": 50,
  "volume_factor": 1.5,
  "volume_lookback": 20,
  "require_confirmation": true,
  "smart_exit": true
}
```

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| timeframe | Chart interval | 15m or 1h |
| rsi_* | RSI settings | Same as RSI strategy |
| fast/slow/signal_period | MACD settings | Same as MACD strategy |
| ma_fast | Fast moving average | 20 |
| ma_slow | Slow moving average | 50 |
| volume_factor | Volume increase required for signals | 1.3-2.0 |
| volume_lookback | Periods to compare volume against | 20-30 |
| require_confirmation | Require multiple indicators to confirm | true |
| smart_exit | Use trailing stops and partial exits | true |

### Best For
- All market conditions
- Higher accuracy trading
- Filtering out false signals

### Not Ideal For
- Users seeking simplicity
- Very short-term trading

## Strategy Optimization

BROski includes a strategy optimizer that can fine-tune the parameters for any strategy based on historical performance. To optimize your strategy:

1. Run `OPTIMIZE.bat`
2. Select the strategy to optimize
3. Choose whether to apply the optimized parameters
4. View the performance report for results

The optimizer uses machine learning to find the best parameters for current market conditions.

## Choosing the Right Strategy

### For Beginners
Start with the **RSI Strategy** and default settings. It's simple to understand and provides good results in many market conditions.

### For Intermediate Users
Try the **MACD Strategy** for trending markets. It's particularly effective when the market is showing a clear direction.

### For Advanced Users
Use the **HyperFocus Strategy** for the highest signal accuracy. Take time to understand all the settings and how they interact.

## Strategy Switching

You can switch strategies at any time:

1. From the Dashboard tab, use the Strategy Selection buttons
2. From the Monitor, use keyboard shortcuts (h, r, m)
3. From the Configuration tab, change the active_strategy setting

## Custom Strategy Development

Advanced users can develop custom strategies by:

1. Creating a new strategy file in the strategies directory
2. Implementing the required interface methods
3. Adding the strategy to the config.json file

See the developer documentation for more details on creating custom strategies.
