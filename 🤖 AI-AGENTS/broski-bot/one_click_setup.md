# BROski One-Click Launch Guide

## Start Everything with a Single Command

For maximum convenience, you can now start both the trading bot and monitoring system together with one click!

### How to Use the One-Click Launcher

Simply double-click the `START_BROSKI.bat` file in your BROski directory.

Or, from the command line:
```bash
python broski_launcher.py
```

### What the Launcher Does

The launcher provides these benefits:

1. **Complete Trading Experience** - Starts both the bot and monitoring tool together
2. **Configuration Summary** - Shows your current settings before launching
3. **Clean Shutdown** - Properly terminates all components when you exit
4. **Error Handling** - Ensures all processes are managed correctly

### Features

- **Trading Bot** runs in the background, executing your selected strategy
- **Monitor** shows real-time logs in a color-coded format
- **Single Control Point** - Just press Ctrl+C in the launcher window to stop everything

### Monitoring Commands

While the system is running, you can use these commands in the monitor window:

- `t` - Toggle timestamps on/off
- `f <keyword>` - Filter logs (e.g., `f RSI` or `f price`)
- `c` - Clear filter
- `s` - Toggle auto-scroll
- `h` - Show help information

## Advanced Usage

### Customizing Launch Options

If you want to customize how the launcher behaves, edit `broski_launcher.py`:

```python
# Change time between bot and monitor start (seconds)
time.sleep(2)  # Adjust this value if needed
```

### Running Components Separately

If you prefer to run the bot and monitor separately:

1. For just the bot: `python start_bot.py`
2. For just the monitor: `python bot_monitor.py`

Enjoy your streamlined BROski trading experience!
