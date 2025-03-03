# BROski Performance Tracking Guide

BROski's built-in performance tracking system helps you analyze your trading results and optimize your strategies. This guide explains how to use these features and interpret the metrics displayed.

## Accessing Performance Metrics

To view your trade performance metrics:

1. Start the monitor:
   ```bash
   monitor_win.bat
   ```

2. Press the `p` key to display the Performance Panel.

## Performance Panel Overview

The Performance Panel is divided into five main sections:

### 1. Overall Performance
- **Total Trades**: The total number of trades executed
- **Win/Loss**: Number of profitable trades vs losing trades
- **Win Rate**: Percentage of trades that resulted in profit
- **Total P&L**: Overall profit or loss from all trades (in USDT)

### 2. Trade Metrics
- **Average Win**: The average profit from winning trades
- **Average Loss**: The average loss from losing trades
- **Largest Win**: Your biggest profitable trade
- **Largest Loss**: Your biggest losing trade

### 3. Strategy Performance
- Performance breakdown by trading strategy
- Win rate for each strategy
- Total trades per strategy
- Strategy-specific profit/loss

### 4. Recent Trades
- List of your most recent completed trades
- Includes action (BUY/SELL), amount, price, and profit/loss
- Color-coded green for profitable trades, red for losses

### 5. Open Positions
- Currently open trades that haven't been closed
- Shows entry price and position size

## Understanding the Metrics

### Win Rate
The win rate shows the percentage of your trades that end profitably. It's calculated as:
```
Win Rate = (Winning Trades ÷ Total Closed Trades) × 100%
```

**What's a good win rate?**
- 40-50%: Typical for many profitable strategies
- 50-60%: Good performance
- 60%+: Excellent performance

Remember that win rate alone doesn't determine profitability. A strategy with a 40% win rate can be highly profitable if the winning trades are much larger than the losing ones.

### Profit/Loss Metrics
The P&L metrics show your actual trading performance:

- **Total P&L**: Sum of all profits and losses
- **Average Win**: Average profit from winning trades
- **Average Loss**: Average loss from losing trades

The key metric to watch is the ratio between your average win and average loss:

```
Reward-to-Risk Ratio = Average Win ÷ Average Loss
```

A good trading system typically has a ratio of at least 1.5, meaning your average win is 1.5 times larger than your average loss.

### Strategy Comparison

The strategy performance section lets you compare how different strategies perform under current market conditions. Look for:

1. **Which strategy has the highest win rate?**
2. **Which strategy generates the most profit?**
3. **Which strategy has the best reward-to-risk ratio?**

This data helps you decide which strategy to focus on for different market conditions.

## Using Performance Data to Improve

### 1. Strategy Selection
Use the strategy comparison metrics to identify which strategy works best for your trading pair under current market conditions:

- **In ranging markets**: RSI strategy may perform better
- **In trending markets**: MACD strategy might show better results
- **In complex markets**: HyperFocus Mode may provide better signals

### 2. Risk Management
Look at your largest loss compared to your average win:

- If largest loss > 3× average win: Consider tightening stop losses
- If average loss > average win: Adjust your take profit settings

### 3. Performance Optimization

If your win rate is below 40%:
- Try increasing confirmation requirements
- Use larger timeframes to reduce market noise
- Consider switching strategies

If your average profit per trade is low:
- Adjust take profit settings
- Let profitable trades run longer
- Check if you're trading too frequently

### 4. Statistical Significance

For reliable analysis:
- Wait until you have at least 20-30 trades before drawing conclusions
- Compare strategy performance over similar market conditions
- Re-evaluate after significant market changes

## Monitoring Long-Term Performance

For comprehensive performance tracking:

1. Check the Performance Panel weekly
2. Note which strategies perform best in different market conditions
3. Track how changes to your configuration affect results
4. Consider keeping a trading journal alongside the automated metrics

## Example Performance Analysis

Here's how to interpret a sample performance panel:

```
OVERALL PERFORMANCE
Total Trades: 28
Win/Loss: 17/11
Win Rate: 60.7%
Total P&L: +42.5982 USDT

TRADE METRICS
Average Win: 4.8235 USDT
Average Loss: 2.1811 USDT
Largest Win: 12.4500 USDT
Largest Loss: -5.6200 USDT

STRATEGY PERFORMANCE
rsi_strategy: 52.9% win rate (9/17 trades)
hyperfocus_strategy: 72.7% win rate (8/11 trades)
```

Analysis:
1. The overall win rate is good at 60.7%
2. The reward-to-risk ratio is excellent at 2.2 (4.82/2.18)
3. HyperFocus Mode is significantly outperforming RSI strategy
4. The largest loss is manageable (not much larger than average win)

Recommendation: Consider using HyperFocus Mode more frequently based on its superior win rate.

For detailed information on trading strategies, see [STRATEGIES.md](STRATEGIES.md)
