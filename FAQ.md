# BROski Frequently Asked Questions

## General Questions

### What is BROski?
BROski is an automated cryptocurrency trading bot designed specifically for MEXC Exchange. It uses technical analysis indicators and advanced strategies like HyperFocus Mode to identify potential trading opportunities.

### Is BROski free to use?
Yes, BROski is completely free and open-source. There are no hidden fees or subscription costs.

### Does BROski work with exchanges other than MEXC?
Currently, BROski is optimized specifically for MEXC Exchange. Support for additional exchanges may be added in future updates.

### How much money do I need to start using BROski?
You can start with any amount you're comfortable with. The bot allows you to set your trade amount in the configuration. We recommend starting with small amounts (5-10 USDT) until you're familiar with how the bot works.

### Does BROski guarantee profits?
No. While BROski is designed to identify potentially profitable trading opportunities, cryptocurrency trading always involves risk. No trading bot can guarantee profits, and market conditions can change rapidly.

## Setup & Configuration

### How do I get MEXC API keys?
1. Log in to your MEXC account
2. Go to Account → API Management
3. Click "Create API"
4. Set permissions (Read + Trade, no withdrawals)
5. Set IP restrictions (recommended)
6. Save your API key and Secret key securely

### Why does my API key keep expiring?
MEXC API keys without IP restrictions expire after 90 days. To prevent this:
1. Add IP restrictions to your API key
2. This makes your key permanent (won't expire)
3. You'll need to update the IP restriction if your IP address changes

### What are the recommended settings for beginners?
- **Strategy**: RSI Strategy
- **Auto-trade**: False (monitor only)
- **Timeframe**: 15m
- **Trading pair**: A major pair like PI/USDT, BTC/USDT, or ETH/USDT
- **Trade amount**: Start small (5-10 USDT)

### How do I enable HyperFocus Mode?
1. Method 1: From the Monitor - Press 'h' in the monitor window
2. Method 2: From the Quick Start Menu - Select option 1
3. Method 3: Manual Configuration - Set `"active_strategy"` to `"hyperfocus_strategy"` in config.json

## Trading Strategies

### How does the RSI strategy work?
The RSI (Relative Strength Index) strategy:
- Buys when RSI crosses above the oversold threshold (default: 30)
- Sells when RSI crosses below the overbought threshold (default: 70)
- Works best in ranging markets with clear support and resistance levels

### How does the MACD strategy work?
The MACD strategy:
- Buys when the MACD line crosses above the signal line
- Sells when the MACD line crosses below the signal line
- Works best in trending markets with sustained directional movements

### What is HyperFocus Mode?
HyperFocus Mode is an advanced strategy that:
- Uses RSI as the primary indicator
- Requires confirmation from secondary indicators (MACD, Moving Averages, Volume)
- Generates fewer but potentially higher-quality signals
- Provides a signal strength metric based on confirmation count

### Which strategy performs best?
Performance varies depending on market conditions:
- RSI works well in ranging, sideways markets
- MACD works well in trending markets
- HyperFocus Mode works well across different conditions but generates fewer signals

Use the Performance Panel (press 'p' in monitor) to compare which strategy works best for your specific trading pair.

## Using the Bot

### How do I start the bot?
The easiest way to start BROski is:
1. Double-click the desktop shortcut (created with CREATE_SHORTCUT.bat)
2. Select option 1, 2, or 3 from the Quick Start Menu to choose your strategy
3. The bot will start in a new window

### How do I know if the bot is working?
When running correctly:
1. You'll see log messages in the monitor window
2. Messages like "Fetched latest candles" indicate data collection
3. "Current RSI: XX.XX" shows indicator calculations
4. "BUY/SELL signal generated" shows trading signals

### What's the difference between monitoring and auto-trading?
- **Monitoring mode** (`auto_trade: false`): The bot identifies signals but doesn't execute trades
- **Auto-trading mode** (`auto_trade: true`): The bot identifies signals AND executes trades automatically

We recommend starting in monitoring mode to test your strategy before enabling auto-trading.

### How do I check my trading performance?
Press 'p' in the monitor window to open the Performance Panel, which shows:
- Win rate and total profit/loss
- Average win and loss sizes
- Performance breakdown by strategy
- Recent trade history
- Open position information

## Troubleshooting

### The bot doesn't connect to MEXC
Check these common issues:
1. Verify your API keys are entered correctly
2. Check if your IP is whitelisted if using IP restrictions
3. Ensure MEXC is accessible from your location
4. Run `python cli.py` and select "Check Balance" to test the connection

### I don't see any trading signals
Possible causes:
1. Market conditions don't meet your strategy criteria
2. Strategy parameters might be too strict
3. Time period is too short (wait longer)
4. HyperFocus Mode has strict confirmation requirements

Try adjusting strategy parameters or switching strategies.

### The performance panel shows no trades
The panel only shows trades when:
1. Auto-trading is enabled and trades were executed, or
2. Trade data was manually added for testing

### My bot crashes on startup
Check these common causes:
1. Missing or incorrect config.json file
2. Missing required Python packages
3. Incorrect API credentials
4. Permission issues with folders/files

Run `python setup.py` to reconfigure your bot.

### How do I update BROski?
1. Make a backup of your config.json
2. Download the latest version
3. Replace all files except your config.json
4. Run `python update_config.py` to add any new config options
5. Restart the bot

## Advanced Questions

### Can I run BROski 24/7?
Yes, BROski is designed to run continuously. For 24/7 operation:
1. Use a VPS (Virtual Private Server)
2. Ensure stable internet connection
3. Set up the bot to start automatically after system reboots

### Does BROski support custom strategies?
Yes, advanced users can create custom strategies by:
1. Creating a new strategy file in the `strategies` folder
2. Updating the strategy_manager.py to load your custom strategy
3. Adding your strategy configuration to config.json

### How do I add more trading pairs?
Currently, BROski trades one pair at a time. To switch pairs:
1. Use the CLI: `python cli.py` then select "Update Trading Settings"
2. Edit config.json directly
3. Use the Quick Start Menu to restart the bot with the new settings

### Can I export my trading data?
Yes, you can export your performance data:
1. As CSV: `python export_data.py --format csv`
2. As JSON: `python export_data.py --format json`
3. All trades are also logged in the logs directory
