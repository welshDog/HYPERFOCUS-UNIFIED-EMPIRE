# BROski Bot: Quick Start Guide

Get up and running with BROski Crypto Trading Bot in minutes!

## 1. Installation

### Windows
1. Simply double-click `BROSKI_DASHBOARD.bat`
2. The dashboard will open automatically

### Mac/Linux
```bash
# Make the launcher executable
chmod +x ./broski_launcher.sh

# Run the launcher
./broski_launcher.sh
```

## 2. First-Time Setup

1. If this is your first time running BROski, you'll need to:
   - Get your MEXC API keys
   - Configure your trading settings

2. **Easy Setup**: 
   - Click "Setup API Keys" on first launch
   - Follow the on-screen instructions

3. **Manual Setup**:
   - Run `python setup.py`
   - Or use the Configuration tab in the dashboard

## 3. Get MEXC API Keys

1. **Log in** to your [MEXC account](https://www.mexc.com)
2. Go to **Account** → **API Management**
3. Click **Create API**
4. Add a description in the **Notes** field (e.g., "BROski Trading Bot")
5. Enable **Read** and **Trade** permissions (disable withdrawals for security)
6. For enhanced security:
   - Select "Link IP Address"
   - Enter your current public IP address
   - Find your IP at [whatismyip.com](https://whatismyip.com)
7. Save your **API Key** and **Secret Key** securely

## 4. Basic Configuration

Key settings to configure:

1. **Trading Pair**:
   - Base Symbol (e.g., PI, BTC, ETH)
   - Quote Symbol (typically USDT)

2. **Trading Amount**:
   - Start small (5-10 USDT recommended)
   - Can be adjusted later

3. **Strategy Selection**:
   - RSI (beginner-friendly)
   - MACD (good for trends)
   - HyperFocus (advanced multi-indicator)

## 5. Start Trading

### Monitor Mode (Recommended for beginners)
1. Keep "Auto-Trade" disabled initially
2. Start the bot from the Dashboard
3. Open the Monitor to watch for signals
4. Observe bot behavior and strategy performance

### Live Trading
When ready for automated trading:
1. Enable "Auto-Trade" in Configuration
2. Start the bot
3. Use the Monitor to track performance

## 6. Using the Dashboard

The dashboard has four main tabs:

1. **Dashboard Tab**
   - Start/stop the bot
   - Switch strategies
   - Monitor status

2. **Configuration Tab**
   - API settings
   - Trading parameters
   - Strategy configuration

3. **Performance Tab**
   - Trading results
   - Win rates and profits
   - Data export

4. **Help Tab**
   - Access documentation
   - Troubleshooting guides

## 7. Using the Monitor

Launch the enhanced monitor with `MONITOR.bat` to:
- View color-coded trading signals
- See real-time position tracking
- Monitor performance metrics

**Key Commands**:
- `t` - Toggle timestamps
- `f` - Filter log entries
- `h`, `r`, `m` - Switch strategies

## 8. Optimize Your Strategy

1. Let the bot run for some time to collect data
2. Run `OPTIMIZE.bat` to calculate optimal parameters
3. Apply the recommended settings
4. Continue monitoring performance

## 9. Next Steps

Once you're comfortable with the basics:
- Experiment with different strategies
- Try various trading pairs
- Adjust strategy parameters
- Analyze performance reports
- Create your own customized settings

## 10. Shortcut Creation

Run `CREATE_DASHBOARD_SHORTCUT.bat` to create a desktop shortcut for easy access to your BROski Bot dashboard.

---

🚀 That's it! Your bot is ready to start trading. For more detailed information, check the full [README.md](README.md) file.
