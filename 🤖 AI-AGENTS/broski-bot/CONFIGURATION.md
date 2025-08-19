# BROski Configuration Guide

This document explains in detail all configuration options available in BROski Crypto Bot.

## Table of Contents
- [Configuration File Overview](#configuration-file-overview)
- [Exchange Configuration](#exchange-configuration)
- [Trading Settings](#trading-settings)
- [Risk Management](#risk-management)
- [Strategy Configuration](#strategy-configuration)
- [Notification Configuration](#notification-configuration)
- [Logging Configuration](#logging-configuration)
- [Advanced Configuration](#advanced-configuration)

## Configuration File Overview

BROski uses a JSON configuration file (`config.json`) to store all settings. This file is created automatically when you run `setup.py` or can be created by copying and editing `config.example.json`.

The configuration is divided into several sections:
- Exchange settings
- Trading parameters
- Risk management rules
- Strategy configurations
- Notification settings
- Logging preferences

## Exchange Configuration

```json
"exchange": {
  "name": "mexc",
  "api_key": "YOUR_MEXC_API_KEY",
  "api_secret": "YOUR_MEXC_API_SECRET",
  "testnet": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Exchange name (currently only "mexc" is supported) |
| `api_key` | string | Your MEXC API key |
| `api_secret` | string | Your MEXC API secret |
| `testnet` | boolean | Whether to use testnet (false for real trading) |

### How to Get API Keys

1. Log in to [MEXC Exchange](https://www.mexc.com/)
2. Navigate to Account → API Management
3. Click "Create API"
4. Set permissions (enable Read and Trade, disable Withdrawals)
5. Add your IP restrictions (recommended)
6. Save your API Key and Secret

## Trading Settings

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

| Parameter | Type | Description |
|-----------|------|-------------|
| `base_symbol` | string | The cryptocurrency you want to trade (e.g., "PI", "BTC") |
| `quote_symbol` | string | The currency used for trading (typically "USDT") |
| `trade_amount` | number | Amount of quote currency to use per trade |
| `max_position_size` | number | Maximum position size in base currency |
| `trade_interval_seconds` | number | Seconds between trading checks |
| `auto_trade` | boolean | Whether to execute trades automatically (true) or just monitor (false) |

### Trade Interval Recommendations

| Timeframe | Recommended Interval |
|-----------|---------------------|
| 1m | 30-60 seconds |
| 5m | 60-120 seconds |
| 15m | 120-300 seconds |
| 1h | 300-600 seconds |
| 4h+ | 600-1200 seconds |

## Risk Management

```json
"risk_management": {
  "stop_loss_percentage": 2.0,
  "take_profit_percentage": 5.0,
  "max_daily_trades": 10,
  "max_open_positions": 3
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `stop_loss_percentage` | number | Percentage loss at which to close a position |
| `take_profit_percentage` | number | Percentage profit at which to close a position |
| `max_daily_trades` | number | Maximum number of trades per day |
| `max_open_positions` | number | Maximum number of open positions at once |

### Risk Management Guidelines

- **Stop Loss**: Typically 1-3% for conservative trading, 3-5% for moderate risk
- **Take Profit**: Usually 2-3x your stop loss value
- **Max Daily Trades**: Limit based on your strategy volatility
- **Max Open Positions**: Depends on your capital allocation strategy

## Strategy Configuration

### RSI Strategy

```json
"rsi_strategy": {
  "enabled": true,
  "timeframe": "5m",
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Whether this strategy is enabled |
| `timeframe` | string | Chart timeframe (1m, 5m, 15m, 1h, etc.) |
| `rsi_period` | number | Number of periods for RSI calculation |
| `rsi_overbought` | number | Level considered overbought |
| `rsi_oversold` | number | Level considered oversold |

### MACD Strategy

```json
"macd_strategy": {
  "enabled": false,
  "timeframe": "15m",
  "fast_period": 12,
  "slow_period": 26,
  "signal_period": 9
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Whether this strategy is enabled |
| `timeframe` | string | Chart timeframe |
| `fast_period` | number | Fast EMA period |
| `slow_period` | number | Slow EMA period |
| `signal_period` | number | Signal line EMA period |

### ML Strategy

```json
"ml_strategy": {
  "enabled": false,
  "model_path": "models/prediction_model.h5",
  "confidence_threshold": 0.75
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Whether this strategy is enabled |
| `model_path` | string | Path to the trained model file |
| `confidence_threshold` | number | Minimum confidence level for signals (0.5-1.0) |

### Active Strategy Selection

```json
"strategies": {
  "active_strategy": "rsi_strategy",
  // Strategy configurations...
}
```

The `active_strategy` parameter determines which strategy will be used. It should match one of the strategy names: `rsi_strategy`, `macd_strategy`, or `ml_strategy`.

## Notification Configuration

### Telegram Notifications

```json
"notifications": {
  "telegram": {
    "enabled": true,
    "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "chat_id": "YOUR_TELEGRAM_CHAT_ID"
  }
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Whether Telegram notifications are enabled |
| `bot_token` | string | Your Telegram bot token (from BotFather) |
| `chat_id` | string | Your Telegram chat ID |

### Email Notifications

```json
"email": {
  "enabled": false,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your_email@gmail.com",
  "password": "your_app_password",
  "receiver_email": "your_email@gmail.com"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Whether email notifications are enabled |
| `smtp_server` | string | SMTP server address |
| `smtp_port` | number | SMTP server port |
| `sender_email` | string | Email address to send from |
| `password` | string | Email account password or app password |
| `receiver_email` | string | Email address to send to |

### Email Security Note

For Gmail and many other providers, you'll need to use an "app password" rather than your regular email password. This is a special password that allows applications to access your email account.

To create an app password for Gmail:
1. Go to your Google Account settings
2. Navigate to Security → App passwords
3. Generate a new app password for BROski
4. Use this password in your config file

## Logging Configuration

```json
"logging": {
  "level": "INFO",
  "save_to_file": true,
  "log_directory": "logs"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | string | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `save_to_file` | boolean | Whether to save logs to files |
| `log_directory` | string | Directory for log files |

### Logging Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General operational information
- **WARNING**: Concerning but non-critical issues
- **ERROR**: Errors that prevent specific operations
- **CRITICAL**: Critical errors that may prevent the bot from running

## Advanced Configuration

These settings are for advanced users and may not be required for typical usage.

### API Configuration

```json
"api": {
  "timeout_seconds": 30,
  "max_retries": 3,
  "retry_delay_seconds": 5
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `timeout_seconds` | number | API request timeout |
| `max_retries` | number | Maximum number of retry attempts |
| `retry_delay_seconds` | number | Delay between retries |

### Performance Settings

```json
"performance": {
  "cache_duration_seconds": 300,
  "use_websocket": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `cache_duration_seconds` | number | How long to cache market data |
| `use_websocket` | boolean | Whether to use WebSocket connections |

## Sample Complete Configuration

Here's a sample configuration file with recommended settings for beginners:

```json
{
  "exchange": {
    "name": "mexc",
    "api_key": "YOUR_MEXC_API_KEY",
    "api_secret": "YOUR_MEXC_API_SECRET",
    "testnet": false
  },
  
  "trading": {
    "base_symbol": "PI",
    "quote_symbol": "USDT",
    "trade_amount": 10,
    "max_position_size": 100,
    "trade_interval_seconds": 60,
    "auto_trade": false
  },
  
  "risk_management": {
    "stop_loss_percentage": 2.0,
    "take_profit_percentage": 5.0,
    "max_daily_trades": 10,
    "max_open_positions": 3
  },
  
  "strategies": {
    "active_strategy": "rsi_strategy",
    "rsi_strategy": {
      "enabled": true,
      "timeframe": "5m",
      "rsi_period": 14,
      "rsi_overbought": 70,
      "rsi_oversold": 30
    },
    "macd_strategy": {
      "enabled": false,
      "timeframe": "15m",
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9
    },
    "ml_strategy": {
      "enabled": false,
      "model_path": "models/prediction_model.h5",
      "confidence_threshold": 0.75
    }
  },
  
  "notifications": {
    "telegram": {
      "enabled": true,
      "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
      "chat_id": "YOUR_TELEGRAM_CHAT_ID"
    },
    "email": {
      "enabled": false,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "sender_email": "your_email@gmail.com",
      "password": "your_app_password",
      "receiver_email": "your_email@gmail.com"
    }
  },
  
  "logging": {
    "level": "INFO",
    "save_to_file": true,
    "log_directory": "logs"
  },
  
  "api": {
    "timeout_seconds": 30,
    "max_retries": 3,
    "retry_delay_seconds": 5
  },
  
  "performance": {
    "cache_duration_seconds": 300,
    "use_websocket": false
  }
}
```

## Configuration Best Practices

1. **Security**:
   - Never commit your config file with API keys to public repositories
   - Consider encrypting sensitive parts of your configuration
   - Regularly rotate API keys

2. **Strategy Parameters**:
   - Start with default values before optimizing
   - Change one parameter at a time to evaluate impact
   - Document which settings work best for different market conditions

3. **Performance Optimization**:
   - Use longer intervals for less active trading
   - Limit the number of trading pairs for better performance
   - Adjust cache duration based on your strategy's needs

4. **Risk Management**:
   - Always set reasonable stop-loss and take-profit values
   - Limit maximum open positions to manage exposure
   - Start with smaller trade amounts until you're confident

## Configuration Templates

### Conservative Setup (Beginners)

```json
{
  "trading": {
    "trade_amount": 5,
    "max_position_size": 50,
    "trade_interval_seconds": 120,
    "auto_trade": false
  },
  "risk_management": {
    "stop_loss_percentage": 1.5,
    "take_profit_percentage": 3.0,
    "max_daily_trades": 5,
    "max_open_positions": 2
  },
  "strategies": {
    "active_strategy": "rsi_strategy",
    "rsi_strategy": {
      "enabled": true,
      "timeframe": "15m",
      "rsi_period": 14,
      "rsi_overbought": 70,
      "rsi_oversold": 30
    }
  }
}
```

### Moderate Setup (Intermediate)

```json
{
  "trading": {
    "trade_amount": 10,
    "max_position_size": 100,
    "trade_interval_seconds": 60,
    "auto_trade": true
  },
  "risk_management": {
    "stop_loss_percentage": 2.0,
    "take_profit_percentage": 5.0,
    "max_daily_trades": 10,
    "max_open_positions": 3
  },
  "strategies": {
    "active_strategy": "macd_strategy",
    "macd_strategy": {
      "enabled": true,
      "timeframe": "15m",
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9
    }
  }
}
```

### Aggressive Setup (Advanced)

```json
{
  "trading": {
    "trade_amount": 20,
    "max_position_size": 200,
    "trade_interval_seconds": 30,
    "auto_trade": true
  },
  "risk_management": {
    "stop_loss_percentage": 3.0,
    "take_profit_percentage": 7.0,
    "max_daily_trades": 20,
    "max_open_positions": 5
  },
  "strategies": {
    "active_strategy": "ml_strategy",
    "ml_strategy": {
      "enabled": true,
      "model_path": "models/prediction_model.h5",
      "confidence_threshold": 0.65
    }
  }
}
```

## Updating Configuration

You can update your configuration in several ways:

1. **Directly edit** `config.json` with a text editor
2. Use the **setup wizard**: `python setup.py`
3. Use the **CLI interface**: `python cli.py` then select "Update Trading Settings"

After updating your configuration, you'll need to restart the bot for changes to take effect.
