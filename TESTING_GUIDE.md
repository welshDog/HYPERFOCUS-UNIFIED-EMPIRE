# BROski Bot Testing Guide

This guide provides a step-by-step approach to test if your BROski bot is set up correctly and functioning as expected.

## Step 1: Check Configuration

First, let's make sure your configuration is properly set up:

```bash
python setup.py
```

This will verify that your configuration file is valid and properly structured.

## Step 2: Test API Connection

Let's verify that your MEXC API connection is working:

```bash
python cli.py
```

Select option 1 "Check Balance" from the menu. If you see your account balances, your API connection is working correctly.

## Step 3: Test Signal Generation

Let's check if the trading strategy can generate signals:

```bash
python test_signals.py
```

This will fetch market data and show recent trading signals for your configured strategy. If you see buy/sell signals, your strategy is working correctly.

## Step 4: Test Monitoring

Start the monitoring tool to see real-time updates:

```bash
python bot_monitor.py
```

Try using some of the interactive commands:
- Type `t` to toggle timestamps
- Type `f rsi` to filter for RSI-related logs
- Type `c` to clear the filter
- Type `h` to show help

## Step 5: Test Combined Launcher

Try the one-click launcher:

```bash
python broski_launcher.py
```

This should start both the bot and monitor together. Verify that both components are running.

## Step 6: Test Emergency Kill

**Important:** Make sure you're not in the middle of important trades before testing this.

From the monitor, press `k` to test the emergency kill function. Confirm by entering `y` when prompted.

Alternatively, run:
```bash
python emergency_kill.py
```

Verify that auto-trading is disabled after the emergency kill process.

## Step 7: Check Log Files

Examine the log files to ensure they're being created and updated correctly:

```bash
type logs\broski_bot.log
```

## Step 8: Update Settings Test

Try updating a setting to see if the changes are saved:

1. Run the CLI: `python cli.py`
2. Select option 2 "Update Trading Settings"
3. Change the trade amount or trading pair
4. Save the changes
5. Exit and restart the CLI to verify the changes persisted

## Step 9: Strategy Test

If you want to test a different strategy:

1. Edit `config.json` and change the `active_strategy` value
2. Restart the bot
3. Check the logs to see if the new strategy is generating different signals

## Step 10: Full End-to-End Test

For a complete test, run the bot in monitoring mode (set `auto_trade` to `false` in config) for a few hours and observe:

1. Are signals being generated?
2. Is the data being retrieved correctly?
3. Are logs updating as expected?

## Troubleshooting Common Issues

- **No balance showing**: Check your API keys and IP whitelist
- **No signals generating**: Verify your strategy configuration and trading pair
- **Monitor not showing updates**: Check if the bot is actually running
- **API errors**: Ensure your API key has the correct permissions

If all tests pass, your BROski Bot is ready for trading! Start with small amounts and monitoring mode until you're confident in the system.
