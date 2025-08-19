import os
import json
import logging
import sys
import time
import random
import traceback
import ccxt
import pandas as pd
from datetime import datetime
from pathlib import Path

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("logs", "broski_bot.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("BROski-Trader")

class DirectBot:
    """Simple direct bot implementation for testing monitor"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.load_config()
        self.setup_exchange()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                
            # Trading settings
            self.base = self.config["trading"]["base_symbol"]
            self.quote = self.config["trading"]["quote_symbol"]
            self.symbol = f"{self.base}/{self.quote}"
            self.auto_trade = self.config["trading"]["auto_trade"]
            
            # Strategy settings
            self.strategy_name = self.config["strategies"]["active_strategy"]
            
            logger.info(f"Configuration loaded successfully")
            logger.info(f"Trading pair: {self.symbol}")
            logger.info(f"Strategy: {self.strategy_name}")
            logger.info(f"Auto-trading: {'Enabled' if self.auto_trade else 'Disabled'}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            sys.exit(1)
    
    def setup_exchange(self):
        """Initialize exchange connection"""
        try:
            self.exchange = ccxt.mexc({
                'apiKey': self.config['exchange']['api_key'],
                'secret': self.config['exchange']['api_secret'],
                'enableRateLimit': True,
            })
            
            # Test connection with a basic call
            self.exchange.load_markets()
            logger.info("Exchange connection successful")
            
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {str(e)}")
            sys.exit(1)
    
    def fetch_price(self):
        """Fetch current price"""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            price = ticker['last']
            logger.info(f"Current price for {self.symbol}: {price}")
            return price
        except Exception as e:
            logger.error(f"Error fetching price: {str(e)}")
            return None
    
    def fetch_candles(self, timeframe='5m', limit=100):
        """Fetch OHLCV candles"""
        try:
            logger.info(f"Fetching {timeframe} candles for {self.symbol}...")
            candles = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            logger.info(f"Fetched {len(df)} candles")
            return df
        except Exception as e:
            logger.error(f"Error fetching candles: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def analyze_rsi(self, df, period=14):
        """Calculate RSI for trading signals"""
        try:
            # Calculate RSI
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            # Get current RSI
            current_rsi = rsi.iloc[-1]
            logger.info(f"Current RSI: {current_rsi:.2f}")
            
            # Check for signals
            if len(rsi) >= 2:
                # RSI Settings
                oversold = self.config["strategies"]["rsi_strategy"]["rsi_oversold"]
                overbought = self.config["strategies"]["rsi_strategy"]["rsi_overbought"]
                
                # Check for buy signal (crossing above oversold)
                if rsi.iloc[-2] < oversold and rsi.iloc[-1] > oversold:
                    logger.info(f"🟢 BUY signal: RSI crossed above {oversold} ({current_rsi:.2f})")
                    return "BUY"
                
                # Check for sell signal (crossing below overbought)
                elif rsi.iloc[-2] > overbought and rsi.iloc[-1] < overbought:
                    logger.info(f"🔴 SELL signal: RSI crossed below {overbought} ({current_rsi:.2f})")
                    return "SELL"
            
            return None
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def run(self):
        """Main bot loop"""
        logger.info(f"Bot initialized for {self.symbol} using {self.strategy_name}")
        logger.info(f"Starting trading loop for {self.symbol}")
        logger.info(f"Auto-trading: {'Enabled' if self.auto_trade else 'Disabled'}")
        
        try:
            while True:
                # Fetch market data
                df = self.fetch_candles()
                
                if df is not None:
                    # Generate trading signal
                    if self.strategy_name == "rsi_strategy":
                        signal = self.analyze_rsi(df)
                    else:
                        # For testing, occasionally generate random signals for other strategies
                        if random.random() < 0.05:  # 5% chance
                            signal = "BUY" if random.random() < 0.5 else "SELL"
                            strat_name = self.strategy_name.replace("_strategy", "").upper()
                            if signal == "BUY":
                                logger.info(f"🟢 BUY signal: {strat_name} strategy")
                            else:
                                logger.info(f"🔴 SELL signal: {strat_name} strategy")
                        else:
                            signal = None
                    
                    # Handle signal
                    if signal and self.auto_trade:
                        logger.info(f"Would execute {signal} order (auto-trade enabled)")
                        # In a real implementation, this would call exchange.create_market_order()
                
                # Generate some additional log messages for monitoring
                current_price = self.fetch_price()
                
                # Sleep before next iteration
                seconds = self.config["trading"]["trade_interval_seconds"]
                time.sleep(seconds)
        
        except KeyboardInterrupt:
            logger.info("Trading bot stopped by user")
        except Exception as e:
            logger.error(f"Error in trading loop: {str(e)}")
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    bot = DirectBot()
    bot.run()
