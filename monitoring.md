# Monitoring Your BROski Trading Bot

## 4 Easy Ways to Monitor Your Bot

### 1. Live Monitor Tool (Recommended)

The easiest way to see what your bot is doing in real-time:

```bash
python bot_monitor.py
```

Or simply double-click on `monitor.bat`

This tool gives you:
- 🔄 **Real-time updates** - See trading signals as they happen
- 🎨 **Color-coded information** - Easily spot important events
- 🔍 **Filtering options** - Focus on specific activities
- 📜 **Interactive commands** - Control what you see

**Interactive Commands:**
- `t` - Toggle timestamps on/off
- `f keyword` - Filter logs (e.g. `f RSI` or `f price`)
- `c` - Clear filter
- `s` - Toggle auto-scroll
- `h` - Show help
- `q` - Quit monitor

### 2. View Log Files Directly

If you prefer to see the raw logs:

```bash
type logs\broski_bot.log
```

Or open the files in your favorite text editor:
- `logs/broski_bot.log` - Main bot activity log
- `logs/trading_bot.log` - Detailed trading activity

### 3. Check Trading Stats

To see a summary of your trading activity:

```bash
python cli.py
```

Select option 4 ("Show Current Settings") to see your bot configuration and trading parameters.

### 4. Enable Telegram Notifications

For mobile monitoring, set up Telegram notifications:

1. Create a Telegram bot using BotFather
2. Update your `config.json` with:
   ```json
   "notifications": {
     "telegram": {
       "enabled": true,
       "bot_token": "YOUR_BOT_TOKEN",
       "chat_id": "YOUR_CHAT_ID"
     }
   }
   ```
3. Restart the bot to enable notifications

## Understanding Trading Signals

### RSI Strategy Signals

- **Buy Signal** - When RSI crosses above the oversold threshold (default: 30)
- **Sell Signal** - When RSI crosses below the overbought threshold (default: 70)

Example log entry:
```
🟢 BUY signal: RSI crossed above 30 (32.14)
```

### MACD Strategy Signals

- **Buy Signal** - When MACD line crosses above the signal line
- **Sell Signal** - When MACD line crosses below the signal line

Example log entry:
```
🟢 BUY signal: MACD crossed above signal line
```
