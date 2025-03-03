# BROski Crypto Bot Setup Guide

## Getting and Adding Your MEXC API Keys

### How to Get MEXC API Keys
1. **Create a MEXC Account**
   - Sign up at [MEXC Global](https://www.mexc.com/)
   - Complete identity verification if required

2. **Generate API Keys**
   - Log in to your MEXC account
   - Navigate to "Account" → "API Management"
   - Click "Create API Key"
   - Enter a description in the "Notes" field (Required)
   - Set permissions (recommended: Read & Trade permissions only, no withdrawal)
Before installing BROski, ensure your system meets these minimum requirements:
   - Save both your **API Key** and **Secret Key** securely

3. **IP Address Restriction (IMPORTANT)**
   - When creating your API key, you'll see "Link IP Address (optional)"
   - **Recommended**: Enter your public IP address
   - Keys without IP restriction expire after 90 days
   - Keys with IP restriction don't expire and are more secure
   - Find your IP at [whatismyip.com](https://www.whatismyip.com)
   - If your IP changes frequently, you may need to update this setting

4. **Security Tips**
   - Never share your API Secret with anyone
   - Consider setting IP restrictions in MEXC
   - Use keys with minimal permissions needed

### Adding API Keys to BROski Bot
You have two options to add your API keys:

#### Option 1: Using the Setup Script
Run the setup script and follow the prompts:
```bash
python setup.py
```

When prompted, paste your MEXC API Key and API Secret.

#### Option 2: Editing Config File Directly
1. Copy the example config: `cp config.example.json config.json`
2. Open `config.json` in a text editor
3. Find the exchange section and add your keys:
```json
"exchange": {
  "name": "mexc",
  "api_key": "YOUR_MEXC_API_KEY_HERE",
  "api_secret": "YOUR_MEXC_API_SECRET_HERE",
  "testnet": false
}
```

## Configuring Trading Settings

### Key Trading Parameters
The trading section of your config controls how the bot trades:

```json
"trading": {
  "base_symbol": "PI",
  "quote_symbol": "USDT",
  "trade_amount": 10,
  "max_position_size": 100,
  "trade_interval_seconds": 60,
  "auto_trade": false
}
```

* **base_symbol**: The cryptocurrency you want to trade (e.g., PI, BTC, ETH)
* **quote_symbol**: The currency used to buy/sell (usually USDT)
* **trade_amount**: Amount of quote currency (USDT) used per trade
* **max_position_size**: Maximum position size in base currency
* **trade_interval_seconds**: How often the bot checks for trading opportunities
* **auto_trade**: Whether to execute trades automatically (false = just alerts)

### Recommended Setup for Beginners

1. Start with a small **trade_amount** (5-10 USDT)
2. Set **auto_trade** to `false` initially to just get signals
3. Use standard timeframes (5m, 15m) for best liquidity
4. Keep **trade_interval_seconds** at 60 for adequate market monitoring

### Advanced Trading Settings

Risk management settings control how the bot manages your trades:

```json
"risk_management": {
  "stop_loss_percentage": 2.0,
  "take_profit_percentage": 5.0,
  "max_daily_trades": 10,
  "max_open_positions": 3
}
```

* **stop_loss_percentage**: Closes trade if loss reaches this percentage
* **take_profit_percentage**: Closes trade when profit reaches this percentage
* **max_daily_trades**: Limits number of trades per day
* **max_open_positions**: Maximum number of concurrent trades

## Selecting and Configuring Trading Strategies

BROski comes with several built-in strategies:

### Available Strategies
1. **RSI Strategy** - Based on Relative Strength Index
2. **MACD Strategy** - Moving Average Convergence Divergence
3. **ML Strategy** - Machine Learning prediction model

### How to Select a Strategy

#### Option 1: Using the Setup Script
Run `python setup.py` and when prompted:
```
🤖 Strategy settings:
Choose strategy (rsi, macd, ml) [default: rsi]:
```
Type the name of your preferred strategy.

#### Option 2: Editing Config File
Set your active strategy in the config.json:
```json
"strategies": {
  "active_strategy": "rsi_strategy",
  ...
}
```

### Strategy Configuration

#### RSI Strategy
```json
"rsi_strategy": {
  "enabled": true,
  "timeframe": "5m",
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30
}
```

* **timeframe**: Chart timeframe (1m, 5m, 15m, 1h, etc.)
* **rsi_period**: Length of RSI calculation period
* **rsi_overbought**: Level considered overbought (sell signal)
* **rsi_oversold**: Level considered oversold (buy signal)

#### MACD Strategy
```json
"macd_strategy": {
  "enabled": false,
  "timeframe": "15m",
  "fast_period": 12,
  "slow_period": 26,
  "signal_period": 9
}
```

* **timeframe**: Chart timeframe
* **fast_period**: Fast EMA period
* **slow_period**: Slow EMA period
* **signal_period**: Signal line period

#### ML Strategy
```json
"ml_strategy": {
  "enabled": false,
  "model_path": "models/prediction_model.h5",
  "confidence_threshold": 0.75
}
```

* **model_path**: Path to trained model file
* **confidence_threshold**: Minimum confidence level for signals

### Strategy Recommendations

1. **Beginners**: Start with RSI strategy with standard settings
2. **Intermediate**: Try MACD strategy on 15m or 1h timeframe
3. **Advanced**: Experiment with the ML strategy after understanding basics

## Testing Your Setup

After configuring your settings:

1. Run the CLI: `python cli.py`
2. Select option to check your balance
3. Start with bot in monitoring mode (auto_trade: false)
4. Review signals before enabling automatic trading

## Troubleshooting Common Issues

* **API Key Errors**: Double-check your API key and secret are correct
* **Trading Errors**: Ensure you have sufficient balance for trades
* **Strategy Not Working**: Verify your strategy configuration parameters
