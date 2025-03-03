# BROski Bot - Using Without TensorFlow

## Why This Guide Exists

TensorFlow can be challenging to install on certain systems due to:
- Python version requirements (needs Python 3.7-3.11)
- Operating system compatibility issues
- Hardware architecture limitations

The good news is that BROski works exceptionally well with traditional technical indicators, which often outperform ML models for cryptocurrency trading anyway!

## Using BROski Without TensorFlow

Your BROski bot includes three excellent trading strategies:

1. **RSI Strategy** ✅ - Available without TensorFlow
   - Relative Strength Index is a momentum oscillator
   - Excellent for identifying overbought/oversold conditions
   - Great for volatile markets like crypto

2. **MACD Strategy** ✅ - Available without TensorFlow
   - Moving Average Convergence Divergence
   - Excellent for identifying trend direction and strength
   - Works well in trending markets

3. **ML Strategy** ❌ - Requires TensorFlow
   - Machine learning prediction model
   - Not available without TensorFlow installation

## Running the Bot with RSI/MACD

### Step 1: Configure for Non-ML Strategy

Run the TensorFlow alternative setup:
```bash
python skip_tensorflow.py
```
This will automatically update your configuration to use the RSI strategy.

### Step 2: Start the Bot

Launch the CLI interface:
```bash
python cli.py
```

### Step 3: Using the CLI
The CLI provides all functionality without TensorFlow:
- Check your balance
- Update trading settings
- Start the trading bot
- View configuration

## RSI Strategy Performance

Many professional traders prefer RSI over ML models because:
1. **Transparency** - You can understand exactly why trades happen
2. **Reliability** - Works well across different market conditions
3. **Simplicity** - Less prone to overfitting or data anomalies

The default RSI settings in BROski are optimized for cryptocurrency trading:
- Timeframe: 5m (captures short-term momentum)
- RSI Period: 14 (standard value)
- Overbought level: 70 (sell signal)
- Oversold level: 30 (buy signal)

## Getting Help

If you still want to try installing TensorFlow in the future:
1. Make sure you're using Python 3.7-3.11
2. Check if your system architecture is supported
3. Try using a virtual environment
4. Consider using Anaconda instead of pip

For now, enjoy trading with the powerful RSI and MACD strategies!
