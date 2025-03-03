# BROski Bot - Master Guide

## Quick Start

1. **Install BROski**:
   ```
   python master_install.py
   ```

2. **Configure API Keys**:
   - Edit `config.json` to add your MEXC API keys
   - Or use the Configuration tab in the Control Center

3. **Launch BROski**:
   - Windows: Double-click `START_BROSKI.bat`
   - All platforms: Run `python launch_broski.py`
   - Advanced: Run `python BROski_Control_Center.py`

## Files and Structure

- **BROski_Control_Center.py** - Main dashboard application
- **start_bot.py** - Trading bot core functionality 
- **launch_broski.py** - Quick launcher with environment checks
- **master_install.py** - Comprehensive installation script

## Configuration Guide

The main configuration file is `config.json`. Key settings:

```json
{
  "exchange": {
    "name": "mexc",
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET"
  },
  "trading": {
    "base_symbol": "PI",
    "quote_symbol": "USDT",
    "auto_trade": false,
    "trade_amount": 10
  },
  "strategies": {
    "active_strategy": "rsi_strategy",
    ...
  }
}
```

## Directory Structure

- **logs/** - Contains bot activity logs
- **backups/** - Stores configuration backups
- **data/** - Stores trading history and market data
- **strategies/** - Contains trading strategy implementations

## Troubleshooting

1. **Missing dependencies**: Run `python master_install.py`
2. **API connection issues**: Check your API keys and internet connection
3. **Bot crashes**: Check logs at `logs/broski_bot.log`
4. **Incorrect strategy behavior**: Verify strategy parameters in configuration

## Security Notes

- Always set IP restrictions on your MEXC API keys
- Never enable withdrawal permissions for trading bots
- Use auto-trade mode only after thorough testing
- Start with small trade amounts until you're confident

## Support

If you encounter problems:
1. Check the logs folder for detailed error information
2. Review this guide and the README file
3. Run the built-in diagnostics from the Health tab
