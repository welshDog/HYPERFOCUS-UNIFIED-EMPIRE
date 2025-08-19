import os
import sys
import json
import time
import logging
import traceback
from pathlib import Path
import ccxt
import numpy as np
import pandas as pd
from datetime import datetime

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/trading_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BROski-Trader")

class TradingBot:
    """BROski Trading Bot with RSI and MACD strategies"""
    
    def __init__(self):
        """Initialize the trading bot with configuration"""
        self.config_file = Path("config.json")
        if not self.config_file.exists():
            logger.error("Config file not found!")
            sys.exit(1)
            
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        
        # Exchange setup
        self.exchange = ccxt.mexc({
            'apiKey': self.config['exchange']['api_key'],
            'secret': self.config['exchange']['api_secret'],
            'enableRateLimit': True,
        })
        
        # Trading parameters
        self.base = self.config["trading"]["base_symbol"]
        self.quote = self.config["trading"]["quote_symbol"]
        self.symbol = f"{self.base}/{self.quote}"
        self.trade_amount = self.config["trading"]["trade_amount"]
        self.max_position = self.config["trading"]["max_position_size"]
        self.auto_trade = self.config["trading"]["auto_trade"]
        
        # Strategy parameters
        self.active_strategy = self.config["strategies"]["active_strategy"]
        self.strategy_config = self.config["strategies"][self.active_strategy]
        self.timeframe = self.strategy_config["timeframe"]
        
        # Risk management
        self.risk = self.config["risk_management"]
        
        # Trading state
        self.trades_today = 0
        self.last_trade_time = None
        self.open_positions = 0
        self.last_signal = None
        
        logger.info(f"Bot initialized for {self.symbol} using {self.active_strategy}")
    
    def fetch_historical_data(self, limit=100):
        """Fetch historical OHLCV data"""
        try:
            logger.info(f"Fetching {self.timeframe} candles for {self.symbol}...")
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"Fetched {len(df)} candles")
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return None
    
    def calculate_indicators(self, df):
        """Calculate technical indicators based on strategy"""
        try:
            if self.active_strategy == "rsi_strategy":
                # Calculate RSI
                rsi_period = self.strategy_config["rsi_period"]
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                
                avg_gain = gain.rolling(window=rsi_period).mean()
                avg_loss = loss.rolling(window=rsi_period).mean()
                
                rs = avg_gain / avg_loss
                df['rsi'] = 100 - (100 / (1 + rs))
                
                logger.info(f"Current RSI: {df['rsi'].iloc[-1]:.2f}")
                
            elif self.active_strategy == "macd_strategy":
                # Calculate MACD
                fast = self.strategy_config["fast_period"]
                slow = self.strategy_config["slow_period"]
                signal_period = self.strategy_config["signal_period"]
                
                df['ema_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
                df['ema_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
                df['macd_line'] = df['ema_fast'] - df['ema_slow']
                df['signal_line'] = df['macd_line'].ewm(span=signal_period, adjust=False).mean()
                df['macd_histogram'] = df['macd_line'] - df['signal_line']
                
                logger.info(f"Current MACD Line: {df['macd_line'].iloc[-1]:.6f}, Signal Line: {df['signal_line'].iloc[-1]:.6f}")
            
            return df
        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}")
            return df
    
    def check_signal(self, df):
        """Check for buy/sell signals based on strategy"""
        if len(df) < 2:
            logger.warning("Not enough data to generate signals")
            return None
        
        try:
            signal = None
            
            if self.active_strategy == "rsi_strategy":
                current_rsi = df['rsi'].iloc[-1]
                previous_rsi = df['rsi'].iloc[-2]
                overbought = self.strategy_config["rsi_overbought"]
                oversold = self.strategy_config["rsi_oversold"]
                
                # Buy signal - RSI crosses above oversold
                if previous_rsi < oversold and current_rsi >= oversold:
                    signal = "BUY"
                    logger.info(f"🟢 BUY signal: RSI crossed above {oversold} ({current_rsi:.2f})")
                
                # Sell signal - RSI crosses below overbought
                elif previous_rsi > overbought and current_rsi <= overbought:
                    signal = "SELL"
                    logger.info(f"🔴 SELL signal: RSI crossed below {overbought} ({current_rsi:.2f})")
            
            elif self.active_strategy == "macd_strategy":
                current_macd = df['macd_line'].iloc[-1]
                current_signal = df['signal_line'].iloc[-1]
                prev_macd = df['macd_line'].iloc[-2]
                prev_signal = df['signal_line'].iloc[-2]
                
                # Buy signal - MACD crosses above signal line
                if prev_macd < prev_signal and current_macd > current_signal:
                    signal = "BUY"
                    logger.info(f"🟢 BUY signal: MACD crossed above signal line")
                
                # Sell signal - MACD crosses below signal line
                elif prev_macd > prev_signal and current_macd < current_signal:
                    signal = "SELL"
                    logger.info(f"🔴 SELL signal: MACD crossed below signal line")
            
            return signal
        except Exception as e:
            logger.error(f"Error checking signals: {str(e)}")
            return None
    
    def check_balance(self):
        """Check account balance for trading pair"""
        try:
            balance = self.exchange.fetch_balance()
            base_balance = balance['total'][self.base] if self.base in balance['total'] else 0
            quote_balance = balance['total'][self.quote] if self.quote in balance['total'] else 0
            
            logger.info(f"Balance: {base_balance} {self.base}, {quote_balance} {self.quote}")
            return base_balance, quote_balance
        except Exception as e:
            logger.error(f"Error checking balance: {str(e)}")
            return 0, 0
    
    def execute_trade(self, signal):
        """Execute a buy or sell order based on signal"""
        if not self.auto_trade:
            logger.info(f"Auto-trading disabled. Signal received: {signal}")
            self.send_notification(f"{signal} signal generated but auto-trading is disabled")
            return False
        
        # Check daily trade limit
        if self.trades_today >= self.risk["max_daily_trades"]:
            logger.info(f"Daily trade limit reached ({self.trades_today}/{self.risk['max_daily_trades']})")
            return False
        
        # Check open position limit for buys
        if signal == "BUY" and self.open_positions >= self.risk["max_open_positions"]:
            logger.info(f"Max open positions reached ({self.open_positions}/{self.risk['max_open_positions']})")
            return False
        
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            base_balance, quote_balance = self.check_balance()
            
            if signal == "BUY":
                # Check if we have enough quote currency
                if quote_balance < self.trade_amount:
                    logger.warning(f"Insufficient {self.quote} balance for trade")
                    return False
                
                # Calculate quantity based on trade amount
                quantity = self.trade_amount / current_price
                
                # Execute buy order
                logger.info(f"Placing buy order: {quantity} {self.base} @ {current_price} {self.quote}")
                order = self.exchange.create_market_buy_order(self.symbol, quantity)
                
                logger.info(f"Buy order executed: {order}")
                self.trades_today += 1
                self.open_positions += 1
                self.last_trade_time = datetime.now()
                
                self.send_notification(f"🟢 BUY order executed: {quantity:.6f} {self.base} @ {current_price} {self.quote}")
                return True
                
            elif signal == "SELL":
                # Check if we have any of the base currency to sell
                if base_balance <= 0:
                    logger.warning(f"No {self.base} balance to sell")
                    return False
                
                # Calculate sell quantity - either what we have or max position size
                quantity = min(base_balance, self.max_position)
                
                # Execute sell order
                logger.info(f"Placing sell order: {quantity} {self.base} @ {current_price} {self.quote}")
                order = self.exchange.create_market_sell_order(self.symbol, quantity)
                
                logger.info(f"Sell order executed: {order}")
                self.trades_today += 1
                self.open_positions = max(0, self.open_positions - 1)  # Decrease open positions
                self.last_trade_time = datetime.now()
                
                self.send_notification(f"🔴 SELL order executed: {quantity:.6f} {self.base} @ {current_price} {self.quote}")
                return True
                
            return False
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}")
            self.send_notification(f"⚠️ Error executing {signal} trade: {str(e)}")
            return False
    
    def send_notification(self, message):
        """Send notification via configured channels"""
        logger.info(f"Notification: {message}")
        
        # TODO: Implement Telegram notifications
        # This would use the Telegram bot token and chat ID from config
    
    def run_trading_loop(self):
        """Main trading loop"""
        logger.info(f"Starting trading loop for {self.symbol}")
        logger.info(f"Auto-trading: {'Enabled' if self.auto_trade else 'Disabled (monitoring only)'}")
        
        # Reset daily trades at midnight
        last_date = datetime.now().date()
        
        try:
            while True:
                # Check if date changed (reset daily counters)
                current_date = datetime.now().date()
                if current_date != last_date:
                    logger.info("New day - resetting trade counters")
                    self.trades_today = 0
                    last_date = current_date
                
                # Fetch and process data
                df = self.fetch_historical_data()
                if df is not None and not df.empty:
                    df = self.calculate_indicators(df)
                    signal = self.check_signal(df)
                    
                    # Execute trade if signal exists and different from last signal
                    if signal and signal != self.last_signal:
                        self.execute_trade(signal)
                        self.last_signal = signal
                
                # Sleep for the configured interval
                interval = self.config["trading"]["trade_interval_seconds"]
                logger.debug(f"Sleeping for {interval} seconds")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Trading bot stopped by user")
        except Exception as e:
            logger.error(f"Error in trading loop: {str(e)}")
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    bot = TradingBot()
    bot.run_trading_loop()
