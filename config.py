import os
import yaml
import json
from pathlib import Path

class Config:
    def __init__(self, config_file="config.yaml"):
        self.config_path = Path(os.path.dirname(os.path.abspath(__file__))) / config_file
        self._load_config()
        
    def _load_config(self):
        """Load configuration from file"""
        if not self.config_path.exists():
            self._create_default_config()
            
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # General settings
        self.debug_mode = config.get('general', {}).get('debug_mode', False)
        self.cycle_interval = config.get('general', {}).get('cycle_interval', 60)
        
        # Exchange settings
        exchange_config = config.get('exchange', {})
        self.exchange_name = exchange_config.get('name', 'binance')
        self.api_key = exchange_config.get('api_key', '')
        self.api_secret = exchange_config.get('api_secret', '')
        
        # Trading pairs
        self.trading_pairs = config.get('trading_pairs', ['BTC/USDT', 'ETH/USDT'])
        
        # Strategy settings
        self.strategies = config.get('strategies', {})
        
        # Risk management
        risk_config = config.get('risk_management', {})
        self.max_position_size = risk_config.get('max_position_size', 0.1)
        self.stop_loss_pct = risk_config.get('stop_loss_pct', 0.02)
        self.take_profit_pct = risk_config.get('take_profit_pct', 0.05)
        
        # Notification settings
        self.notification_channels = config.get('notifications', {})
    
    def _create_default_config(self):
        """Create default configuration file"""
        default_config = {
            'general': {
                'debug_mode': True,
                'cycle_interval': 60  # seconds
            },
            'exchange': {
                'name': 'binance',
                'api_key': '',
                'api_secret': ''
            },
            'trading_pairs': ['BTC/USDT', 'ETH/USDT'],
            'strategies': {
                'rsi_strategy': {
                    'enabled': True,
                    'timeframe': '1h',
                    'rsi_period': 14,
                    'rsi_overbought': 70,
                    'rsi_oversold': 30
                },
                'macd_strategy': {
                    'enabled': False,
                    'timeframe': '4h',
                    'fast_period': 12,
                    'slow_period': 26,
                    'signal_period': 9
                }
            },
            'risk_management': {
                'max_position_size': 0.1,  # 10% of portfolio
                'stop_loss_pct': 0.02,     # 2% stop loss
                'take_profit_pct': 0.05    # 5% take profit
            },
            'notifications': {
                'telegram': {
                    'enabled': False,
                    'bot_token': '',
                    'chat_id': ''
                },
                'email': {
                    'enabled': False,
                    'smtp_server': '',
                    'smtp_port': 587,
                    'sender_email': '',
                    'receiver_email': '',
                    'password': ''
                }
            }
        }
        
        with open(self.config_path, 'w') as file:
            yaml.dump(default_config, file, default_flow_style=False)

