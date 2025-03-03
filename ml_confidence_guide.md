# ML Strategy Confidence Threshold Guide

## What is the Confidence Threshold?

The confidence threshold is a value between 0 and 1 that determines how certain the ML model must be before generating a trading signal.

When the ML model makes a prediction, it outputs a probability value:
- A value close to 1.0 means high confidence in an upward price movement (buy signal)
- A value close to 0.0 means high confidence in a downward price movement (sell signal)
- A value around 0.5 means uncertainty (no clear signal)

## How the Threshold Works

Given your threshold setting (default 0.75):

- **For BUY signals**: The model's prediction must be ≥ 0.75 to generate a buy signal
- **For SELL signals**: The model's prediction must be ≤ 0.25 (calculated as 1 - threshold) to generate a sell signal
- **No signal** is generated when the prediction falls between these values

## Choosing Your Threshold Value

### Higher Threshold (0.80-0.95)
- **Pros**: More selective signals, potentially higher accuracy, fewer false positives
- **Cons**: Fewer trading opportunities, might miss profitable trades
- **Best for**: Conservative traders who prefer quality over quantity

### Medium Threshold (0.70-0.80)
- **Pros**: Balanced approach, reasonable number of signals with decent reliability
- **Cons**: Some false signals will still occur
- **Best for**: Balanced trading approach, moderate risk tolerance

### Lower Threshold (0.60-0.70)
- **Pros**: More trading opportunities, won't miss many potential moves
- **Cons**: Lower signal quality, more false positives
- **Best for**: Aggressive traders who can manage false signals and prefer quantity

## Recommendations

1. **For beginners**: Start with the default value of 0.75 for balance
2. **For conservative trading**: Use 0.85 to minimize false signals
3. **For aggressive trading**: Use 0.65 to capture more opportunities
4. **For testing**: Run the bot in monitoring mode (auto_trade: false) and test different thresholds

## Adjusting Over Time

It's good practice to:
1. Start with a moderate threshold (0.75)
2. Monitor performance for a few weeks
3. Adjust based on results:
   - If too many false signals, increase the threshold
   - If too few signals, decrease the threshold

Remember that market conditions change, so the optimal threshold may need periodic adjustment.
