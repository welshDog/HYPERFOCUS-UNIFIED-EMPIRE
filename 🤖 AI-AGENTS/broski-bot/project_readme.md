# BROski Crypto Trading Bot

## Project Status
We're actively developing BROski, a user-friendly cryptocurrency trading bot with a focus on simplicity and effectiveness.

### Current Features
- Configuration system for easy setup
- CLI interface for interacting with the bot
- Basic MEXC API integration for price fetching
- Signal generation framework
- Telegram notifications
- Docker containerization

### Under Development
- Advanced trading strategies (RSI, MACD)
- AI-powered signal generation
- Risk management system
- Backtesting framework
- Web dashboard

## Development Tools

### Task Tracker
We use a custom task tracking system to monitor progress:

```bash
python task_tracker.py
```

This provides an overview of all components and their completion status.

### Daily Standups
To keep development organized, we use a standup system:

```bash
# Create a new standup entry
python daily_standup.py create --dev YourName

# List recent standups
python daily_standup.py list
```

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (for containerized deployment)
- MEXC API keys
- Telegram API credentials (optional)

### Setup
1. Clone the repository
2. Create your configuration file:
   ```bash
   cp config.example.json config.json
   ```
3. Edit `config.json` with your API keys and preferences
4. Run the CLI:
   ```bash
   python cli.py
   ```

## Development Roadmap

### Phase 1: Core Infrastructure ⏳
- [x] Basic architecture
- [x] Configuration system
- [x] MEXC API integration
- [ ] Trade execution

### Phase 2: Trading Intelligence 🚧
- [ ] Technical indicators
- [ ] Strategy implementation
- [ ] AI model integration
- [ ] Backtesting

### Phase 3: User Experience 🔮
- [ ] Enhanced notifications
- [ ] Performance reporting
- [ ] Web dashboard
- [ ] Mobile app integration

## Contributing
Want to contribute? Great! Check the task tracker for open tasks or suggest new features.

## License
MIT
