# BROski Crypto Trading Bot

<div align="center">
  <img src="assets/broski_logo.png" alt="BROski Logo" width="200"/>
  <br>
  <h3>Automated Cryptocurrency Trading with Multiple Strategies</h3>
</div>

## 🚀 Features

- **Multiple Trading Strategies** - RSI, MACD, and advanced HyperFocus strategy
- **Real-time Analysis** - Live market data analysis using technical indicators
- **Risk Management** - Configurable stop-loss and take-profit mechanisms
- **User-friendly Interface** - Simple control center and unified launcher
- **Secure API Management** - Safe handling of exchange API credentials
- **Backtesting** - Test strategies against historical data
- **Telegram Integration** - Get notified about trades and bot status
- **Extensible** - Easily add your own custom strategies

## 📋 Requirements

- Python 3.8 or higher
- MEXC Exchange account with API access
- Required packages (installed automatically with setup)

## 🛠️ Installation

### Quick Install

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/broski-bot.git
   cd broski-bot
   ```

2. Run the setup script:
   ```
   python setup.py
   ```

3. Or use the installation batch file:
   ```
   INSTALL.bat  # On Windows
   ```

### Manual Installation

1. Install required packages:
   ```
   pip install ccxt pandas numpy matplotlib colorama requests psutil
   ```

2. Create configuration:
   ```
   cp config.example.json config.json
   ```

3. Edit `config.json` with your API keys and trading preferences.

## ⚙️ Configuration

### MEXC API Setup

1. Create a MEXC account at [mexc.com](https://www.mexc.com)
2. Go to Account → API Management
3. Create API keys with Read and Trade permissions
4. Optional but recommended: Set IP restrictions for your API keys
5. Add your keys to the config.json file

See the [API Setup Guide](api_notes_guide.md) for detailed instructions.

### Trading Configuration

Configure the bot's trading behavior in the `config.json` file:

```json
"trading": {
  "base_symbol": "BTC",
  "quote_symbol": "USDT",
  "auto_trade": false,
  "trade_amount_usdt": 10.0,
  "max_open_trades": 1
}
```

- **base_symbol**: The cryptocurrency to trade (e.g., BTC, ETH)
- **quote_symbol**: The currency to trade against (e.g., USDT)
- **auto_trade**: Set to true for automatic trading, false for simulation/signals only
- **trade_amount_usdt**: Amount of quote currency to use per trade
- **max_open_trades**: Maximum number of simultaneous open trades

### Strategy Selection

BROski includes multiple trading strategies. Select and configure them in the `config.json` file:

```json
"strategies": {
  "active_strategy": "rsi",
  "rsi": {
    "enabled": true,
    "period": 14,
    "overbought": 70,
    "oversold": 30,
    "timeframe": "1h"
  }
}
```

See the [Strategy Configuration Guide](strategy_guide.md) for more details.

## 🚀 Usage

### Starting the Bot

Run the unified launcher to access all bot functions:

```
python unified_launcher.py
```

Or start the control center directly:

```
python BROski_Control_Center.py
```

### Command Line Interface

For terminal users, the CLI provides a text-based interface:

```
python cli.py
```

### Security Recommendations

- Never share your API secret keys
- Enable IP restrictions for your API keys
- Start with auto_trade set to false until you're comfortable with the bot's behavior
- Begin with small trade amounts

## 📊 Strategies

BROski includes several built-in strategies:

### RSI Strategy

Uses the Relative Strength Index to identify overbought and oversold conditions.

### MACD Strategy

Uses Moving Average Convergence Divergence for trend-following.

### HyperFocus Strategy

Advanced multi-timeframe strategy that combines multiple indicators for improved accuracy.

## 🛡️ Risk Management

Configure risk management settings to protect your capital:

```json
"risk_management": {
  "stop_loss_percentage": 2.0,
  "take_profit_percentage": 5.0,
  "max_daily_trades": 10,
  "max_open_positions": 3
}
```

## 📈 Monitoring

Monitor your bot's performance using:

- Command line interface: `python cli.py`
- Bot monitor: `python monitor/bot_monitor.py`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Trading cryptocurrencies involves significant risk. This bot is for educational purposes only. Never trade with money you cannot afford to lose.

## 🙏 Acknowledgements

- MEXC Exchange for their API
- CCXT library for exchange connectivity
- The cryptocurrency trading community for inspiration
