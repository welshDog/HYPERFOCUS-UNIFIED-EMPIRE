# BROski Integration Guide

This guide explains how to integrate BROski with other tools and services for an enhanced trading experience.

## Table of Contents
- [Telegram Notifications](#telegram-notifications)
- [Email Alerts](#email-alerts)
- [Data Export](#data-export)
- [Third-Party Tools](#third-party-tools)
- [API Integration](#api-integration)

## Telegram Notifications

### Setting Up Telegram Bot

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Save the bot token provided

2. **Get Your Chat ID**:
   - Send a message to `@userinfobot`
   - Note the "Id" number provided
   - This is your personal chat ID

3. **Configure BROski**:
   - Open your `config.json` file
   - Add your Telegram settings:
   ```json
   "notifications": {
     "telegram": {
       "enabled": true,
       "bot_token": "YOUR_BOT_TOKEN",
       "chat_id": "YOUR_CHAT_ID"
     }
   }
   ```

4. **Test Notifications**:
   - Restart BROski
   - Notifications will now be sent to your Telegram

### Customizing Notifications

You can customize which events trigger notifications in the `notifications.py` file:

- Trading signals
- Executed trades
- Performance statistics
- Error alerts

## Email Alerts

### Setting Up Email Notifications

1. **Configure Email Settings**:
   ```json
   "notifications": {
     "email": {
       "enabled": true,
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "your_email@gmail.com",
       "password": "your_app_password",
       "receiver_email": "your_email@gmail.com"
     }
   }
   ```

2. **Gmail App Password**:
   - For Gmail, you'll need to create an "App Password"
   - Go to your Google Account → Security → App passwords
   - Generate a new app password for "Mail" and "Other (Custom name)"
   - Use this password in your config, not your regular Gmail password

3. **Test Email Alerts**:
   - Restart BROski
   - Check that you receive test email

## Data Export

BROski can export your trading data for analysis in other tools:

### CSV Export

1. **Enable Export**:
   ```bash
   python data_export.py --format csv
   ```

2. **Available Data**:
   - Trading signals
   - Executed trades
   - Performance metrics
   - Raw market data

### JSON Export

For integration with other applications:

```bash
python data_export.py --format json
```

## Third-Party Tools

### TradingView Integration

You can use TradingView alerts with BROski by:

1. Setting up a webhook server (instructions in `tradingview_webhook.py`)
2. Creating TradingView alerts that send to your webhook
3. Configuring BROski to process these alerts

### Excel Integration

For Excel analysis:
1. Export data as CSV
2. Import to Excel
3. Use provided Excel templates for visualization

## API Integration

BROski provides a simple API for integration with other tools:

1. **Enable API Server**:
   ```bash
   python api_server.py
   ```

2. **Available Endpoints**:
   - `/status` - Current bot status
   - `/trades` - Recent trades
   - `/signals` - Recent signals
   - `/performance` - Performance metrics

3. **Security**:
   - Set up API keys in `config.json`
   - Use HTTPS for secure connections
   - Restrict access by IP address

For detailed API documentation, see the comments in `api_server.py`.
