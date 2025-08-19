# Getting Started with BROski

This guide will help you start using BROski Crypto Bot in just a few simple steps.

## Step 1: Installation

### System Requirements
- Windows 10/11, macOS, or Linux
- Python 3.7 or higher
- Internet connection
- MEXC Exchange account

### Install BROski
1. Download the BROski files
2. Extract the files to a folder of your choice
3. Open a command prompt or terminal in that folder
4. Install the required packages:

```bash
pip install -r requirements.txt
```

## Step 2: Get MEXC API Keys

You'll need API keys to connect BROski to your MEXC account:

1. **Log in to MEXC**
   - Visit [MEXC Exchange](https://www.mexc.com/)
   - Sign in to your account

2. **Create API Keys**
   - Navigate to Account → API Management
   - Click "Create API"
   - In the "Notes" field, enter "BROski Trading Bot"
   - Set permissions:
     - ✅ Enable "Read"
     - ✅ Enable "Spot & Margin Trading"
     - ❌ DISABLE "Withdrawals" (for security)
   - Set IP restrictions (recommended)
   - Save both your API Key and Secret Key

## Step 3: Set Up BROski

### Run the Setup Wizard
For easy setup, run the setup wizard:

```bash
python setup.py
```

This interactive guide will help you:
1. Enter your MEXC API credentials
2. Set up trading parameters
3. Choose a trading strategy
4. Configure notifications (optional)

### Create Desktop Shortcut
To make future access easier:

```bash
CREATE_SHORTCUT.bat
```

This creates a desktop shortcut that opens the Quick Start Menu.

## Step 4: Start Trading

You have several ways to start BROski:

### Option 1: Quick Start Menu (Recommended)
1. Double-click the desktop shortcut
2. From the Quick Start Menu, select:
   - Option 1 for HyperFocus Mode
   - Option 2 for RSI Strategy
   - Option 3 for MACD Strategy
3. The bot will start in a new window

### Option 2: Command Line
```bash
python broski_launcher.py
```

### Option 3: Single Components
Monitor only:
```bash
python bot_monitor.py
```

## Step 5: Understand the Interface

Once running, you'll see the monitor window with:

1. **Log Messages**
   - Green for INFO messages
   - Yellow for WARNINGS
   - Red for ERRORS

2. **Key Commands**
   - `t` - Toggle timestamps
   - `f` - Filter logs
   - `p` - Show performance metrics
   - `v` - View strategy information
   - `h` - Switch to HyperFocus Mode
   - `?` - Show all commands

## Step 6: Monitor Performance

To track your trading performance:

1. Press `p` in the monitor window
2. Review your trade statistics:
   - Win rate
   - Profit/loss
   - Strategy comparison
   - Recent trades

## Step 7: Optimize Your Strategy

After running for a while:

1. Review your performance metrics
2. Try different strategies:
   - Press `r` for RSI Strategy
   - Press `m` for MACD Strategy
   - Press `h` for HyperFocus Mode
3. Adjust parameters in the config.json file
4. Test in monitoring mode before enabling auto-trading

## Next Steps

- Read [STRATEGIES.md](STRATEGIES.md) to understand trading strategies
- Check [CONFIGURATION.md](CONFIGURATION.md) for detailed settings
- View [TRADE_TRACKING.md](TRADE_TRACKING.md) to interpret performance data
- Read [FAQ.md](FAQ.md) for common questions
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you encounter issues

## Safety Tips

1. **Start small** - Use small trade amounts initially
2. **Monitor before auto-trading** - Set `auto_trade` to `false` until confident
3. **Secure your API keys** - Never enable withdrawal permissions
4. **Set reasonable risk limits** - Configure proper stop-loss values
5. **Regularly check performance** - Monitor your bot's results

Happy trading with BROski! 📈
