# BROski Monitor Commands Guide

The BROski monitor provides a real-time interface to track bot activity and manage your trading with simple keyboard commands. This guide explains all available commands and their functions.

## Starting the Monitor

To start the monitor:

```bash
monitor_win.bat
```

Or use option 4 in the Quick Start Menu:

```bash
BROSKI_QUICK_START.bat
```

## Available Commands

| Command | Description |
|---------|-------------|
| `t` | Toggle timestamps on/off in log display |
| `f` | Filter logs (you'll be prompted for keyword) |
| `c` | Clear current filter |
| `s` | Toggle auto-scroll on/off |
| `v` | Show/hide strategy information panel |
| `p` | Show/hide performance metrics panel |
| `h` | Enable HyperFocus Mode |
| `r` | Enable RSI Strategy |
| `m` | Enable MACD Strategy |
| `k` | EMERGENCY KILL - Stops bot and cancels open orders |
| `?` | Show help screen |
| `q` | Quit monitor |

## Strategy Switching

Use these commands to change strategies on-the-fly:

- **h** - Switch to HyperFocus Mode
  - Multi-indicator strategy with confirmations
  - More selective with higher-quality signals
  - Best for important trading decisions

- **r** - Switch to RSI Strategy
  - Relative Strength Index based signals
  - Good for ranging markets
  - Detects overbought/oversold conditions

- **m** - Switch to MACD Strategy
  - Moving Average Convergence Divergence
  - Good for trending markets
  - Identifies trend changes and momentum

After changing strategies, you'll need to restart the bot for changes to take effect.

## Information Panels

### Strategy Information Panel (Press `v`)

Shows details about your active trading strategy:

- **For HyperFocus Mode**:
  - Signal strength (confirmations)
  - Primary and confirmation indicators
  - Strategy description

- **For RSI Strategy**:
  - Current RSI value
  - Buy/sell thresholds
  - Strategy description

- **For MACD Strategy**:
  - MACD line and signal line values
  - Histogram values
  - Strategy description

### Performance Panel (Press `p`)

Shows comprehensive trade performance metrics:

- **Overall Performance**:
  - Total trades, win/loss ratio
  - Win rate percentage
  - Total profit/loss

- **Trade Metrics**:
  - Average win and loss amounts
  - Largest win and loss
  - Return metrics

- **Strategy Performance**:
  - Win rates by strategy
  - Profit/loss by strategy
  - Trade counts by strategy

- **Recent Trades & Open Positions**:
  - List of recent trade results
  - Currently open positions

## Filtering Logs

The filter function helps you focus on specific information:

1. Press `f` to activate filtering
2. Enter your keyword when prompted
3. Only log entries containing your keyword will be shown
4. Press `c` to clear the filter and see all logs again

### Useful Filter Keywords

- `signal` - Show only trading signals
- `RSI` - Show only RSI-related entries
- `MACD` - Show only MACD-related entries
- `price` - Show price updates
- `buy` or `sell` - Show only buy or sell signals
- `error` - Show only error messages

## Emergency Kill Button

If something goes wrong:

1. Press `k` to activate the emergency kill
2. Confirm with `y` when prompted
3. This will:
   - Cancel all open orders
   - Stop the trading bot
   - Disable auto-trading in your config

Use this only in emergencies when you need to immediately stop all trading activity.

## Tips for Effective Monitoring

1. Use the Performance Panel (`p`) regularly to track your trading success
2. Switch between strategies (`h`, `r`, `m`) to compare performance
3. Use filters (`f`) when troubleshooting specific issues
4. Clear the screen occasionally to avoid clutter
5. Toggle timestamps (`t`) off for cleaner display when needed

For more information about BROski's features, see [README.md](README.md)
