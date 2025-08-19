# BROski Bot: Troubleshooting Guide

This guide covers common issues encountered when using BROski Bot and their solutions.

## Table of Contents
- [API Connection Issues](#api-connection-issues)
- [Dashboard Problems](#dashboard-problems)
- [Trading Issues](#trading-issues)
- [Monitor Problems](#monitor-problems)
- [Strategy Issues](#strategy-issues)
- [Error Messages](#error-messages)

## API Connection Issues

### "API key or secret incorrect" / Authentication Failed

**Possible causes:**
- API key or secret incorrectly entered
- API keys expired
- IP restrictions preventing connection

**Solutions:**
1. Verify your API keys in config.json match exactly what MEXC provided
2. Check if your keys have IP restrictions and if your current IP is allowed
3. Regenerate new API keys on MEXC and update your configuration

### "IP not in whitelist"

**Cause:** Your current IP address is not in the allowed list for your API key.

**Solutions:**
1. Add your current IP to your API whitelist on MEXC
   - Go to MEXC → Account → API Management → Edit API → Add IP
2. Find your current IP by visiting [whatismyip.com](https://whatismyip.com)
3. If your IP changes frequently, consider using API keys without IP restrictions (less secure, requires renewal every 90 days)

## Dashboard Problems

### Dashboard Won't Start

**Possible causes:**
- Missing Python dependencies
- Incorrect Python version
- File permissions issues

**Solutions:**
1. Ensure Python 3.9+ is installed
2. Run: `pip install -r requirements.txt`
3. Check logs/broski_dashboard.log for specific errors
4. Try running directly: `python broski_dashboard.py`

### Dashboard Missing Components

**Possible cause:** Incomplete installation or missing files

**Solutions:**
1. Verify all required files exist
2. Re-download or clone the entire repository
3. Check file permissions

## Trading Issues

### Bot Not Executing Trades

**Possible causes:**
- Auto-trade disabled
- Insufficient balance
- API keys missing trading permissions
- Trade amount too small for minimum order size

**Solutions:**
1. Check "Auto-Trade" setting (Configuration tab or config.json)
2. Verify trading permissions in your MEXC API settings
3. Check your MEXC balance for sufficient funds
4. Increase trade amount to meet minimum order size

### Orders Being Rejected

**Possible causes:**
- Insufficient funds
- Invalid price (outside price limits)
- Symbol trading restrictions on exchange

**Solutions:**
1. Check balance for the quote currency (usually USDT)
2. Verify the trading pair exists and is active
3. Ensure your trade amount meets minimum requirements

## Monitor Problems

### Empty Window in Monitor

**Solutions:**
1. Use MONITOR.bat to launch the monitor
2. Ensure logs/broski_bot.log exists
3. Check if the bot is running

### Missing Information in Monitor

**Possible causes:**
- Bot not running
- Log file access issues

**Solutions:**
1. Start the bot first with BROSKI_DASHBOARD.bat
2. Check file permissions for logs folder
3. View the bot's log file directly to verify logging is working

## Strategy Issues

### No Trading Signals Generated

**Possible causes:**
- Strategy parameters need adjustment
- Market conditions not triggering signals
- Strategy disabled

**Solutions:**
1. Verify the correct strategy is enabled in Configuration
2. Adjust strategy parameters (e.g., RSI thresholds)
3. Try a different strategy more suitable for current market conditions

### Poor Strategy Performance

**Solutions:**
1. Run OPTIMIZE.bat to optimize strategy parameters
2. Switch to a different strategy (Dashboard tab → Strategy Selection)
3. Adjust timeframes for the current market conditions

## Error Messages

### "Configuration file not found"

**Solutions:**
1. Run setup.py to create configuration
2. Check if config.json exists in the main directory
3. Copy config.example.json to config.json and edit manually

### "No module named X"

**Solution:** Run `pip install -r requirements.txt`

### "Failed to fetch market data"

**Possible causes:**
- Internet connection issue
- MEXC API temporarily unavailable
- Rate limiting

**Solutions:**
1. Check your internet connection
2. Wait a few minutes and retry
3. Reduce the frequency of API calls (increase trade_interval_seconds)

## Log Files

Important log files to check when troubleshooting:

- `logs/broski_bot.log` - Main bot activity log
- `logs/broski_dashboard.log` - Dashboard application log
- `logs/monitor_logger.log` - Monitor activity log

To view a log file:
```
type logs\broski_bot.log
```

## Still Having Issues?

If none of these solutions work, try these steps:

1. **Restart Everything**
   - Close all BROski windows and scripts
   - Restart your computer
   - Try the bot again

2. **Reset Configuration**
   - Rename or delete config.json
   - Run setup.py to create a new configuration
   - Enter your API keys and settings again

3. **Check System Requirements**
   - Python 3.9 or newer
   - Sufficient disk space
   - Active internet connection
   - Valid MEXC account with API access
