import logging
import time
import pandas as pd
import numpy as np
from datetime import datetime
import ccxt
import json
from pathlib import Path

logger = logging.getLogger("BROski.DataFetcher")

class DataFetcher:
    def __init__(self, config=None):
        """Initialize the data fetcher with configuration"""
        if config:
            self.config = config
        else:
            # Load config from file if not provided
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                raise FileNotFoundError("Config file not found")
        
        # Connect to exchange
        self._initialize_exchange()
        
        # Cache for OHLCV data to reduce API calls
        self.ohlcv_cache = {}
        self.last_update_time = {}
        
        logger.info("DataFetcher initialized")
    
    def _initialize_exchange(self):
        """Initialize exchange connection"""
        try:
            self.exchange = ccxt.mexc({
                'apiKey': self.config['exchange']['api_key'],
                'secret': self.config['exchange']['api_secret'],
                'enableRateLimit': True,
            })
            logger.info(f"Connected to {self.exchange.name} exchange")
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {str(e)}")
            self.exchange = None
    
    def get_latest_data(self):
        """
        Fetch the latest market data according to configuration
        
        Returns:
            dict: Market data including prices, volumes, and indicators
        """
        logger.info("Fetching latest market data")
        
        market_data = {
            "pairs": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Get the trading pair from config
        base = self.config["trading"]["base_symbol"]
        quote = self.config["trading"]["quote_symbol"]
        pair = f"{base}/{quote}"
        
        # Get active strategy and timeframe
        active_strategy = self.config["strategies"]["active_strategy"]
        timeframe = self.config["strategies"][active_strategy]["timeframe"]
        
        try:
            market_data["pairs"][pair] = {
                "price": self._get_current_price(pair),
                "ohlcv": self._get_ohlcv_data(pair, timeframe),
                "indicators": self._calculate_indicators(pair, timeframe, active_strategy)
            }
            
            logger.info(f"Fetched data for {pair}")
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            return market_data
    
    def _get_current_price(self, pair):
        """
        Get current price for a trading pair
        
        Args:
            pair (str): Trading pair in format BASE/QUOTE
            
        Returns:
            float: Current price
        """
        try:
            ticker = self.exchange.fetch_ticker(pair)
            price = ticker['last']
            logger.debug(f"Current price for {pair}: {price}")
            return price
        except Exception as e:
            logger.error(f"Error fetching price for {pair}: {str(e)}")
            return None
    
    def _get_ohlcv_data(self, pair, timeframe, limit=100):
        """
        Get OHLCV data for a trading pair
        
        Args:
            pair (str): Trading pair in format BASE/QUOTE
            timeframe (str): Timeframe string like '5m', '1h', etc.
            limit (int): Number of candles to fetch
            
        Returns:
            pd.DataFrame: OHLCV data with columns: open, high, low, close, volume
        """
        cache_key = f"{pair}_{timeframe}"
        current_time = time.time()
        
        # Check if we need to refresh the cache
        # For 1m, refresh every 30 sec; 5m, refresh every 2 min, etc.
        refresh_time = {
            '1m': 30,
            '5m': 120,
            '15m': 300,
            '30m': 600,
            '1h': 1800,
            '4h': 7200,
            '1d': 28800
        }.get(timeframe, 60)
        
        if (cache_key not in self.ohlcv_cache or 
            cache_key not in self.last_update_time or 
            current_time - self.last_update_time.get(cache_key, 0) > refresh_time):
            
            try:
                logger.debug(f"Fetching OHLCV data for {pair} ({timeframe})")
                ohlcv = self.exchange.fetch_ohlcv(pair, timeframe, limit=limit)
                
                # Convert to DataFrame
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                # Update cache
                self.ohlcv_cache[cache_key] = df
                self.last_update_time[cache_key] = current_time
                
                logger.debug(f"Fetched {len(df)} candles for {pair}")
                return df
            
            except Exception as e:
                logger.error(f"Error fetching OHLCV data for {pair}: {str(e)}")
                return pd.DataFrame()
        else:
            logger.debug(f"Using cached OHLCV data for {pair} ({timeframe})")
            return self.ohlcv_cache[cache_key]
    
    def _calculate_indicators(self, pair, timeframe, active_strategy):
        """
        Calculate technical indicators based on the active strategy
        
        Args:
            pair (str): Trading pair
            timeframe (str): Timeframe string
            active_strategy (str): Name of active strategy
            
        Returns:
            dict: Dictionary of calculated indicators
        """
        df = self._get_ohlcv_data(pair, timeframe)
        if df.empty:
            logger.warning(f"No OHLCV data available to calculate indicators for {pair}")
            return {}
        
        indicators = {}
        
        if active_strategy == "rsi_strategy":
            # Calculate RSI
            rsi_period = self.config["strategies"]["rsi_strategy"]["rsi_period"]
            indicators["rsi"] = self._calculate_rsi(df, period=rsi_period)
            
        elif active_strategy == "macd_strategy":
            # Calculate MACD
            fast_period = self.config["strategies"]["macd_strategy"]["fast_period"]
            slow_period = self.config["strategies"]["macd_strategy"]["slow_period"]
            signal_period = self.config["strategies"]["macd_strategy"]["signal_period"]
            
            macd_line, signal_line, histogram = self._calculate_macd(
                df, fast_period=fast_period, slow_period=slow_period, signal_period=signal_period
            )
            
            indicators["macd_line"] = macd_line
            indicators["signal_line"] = signal_line
            indicators["macd_histogram"] = histogram
            
        elif active_strategy == "ml_strategy":
            # For ML strategy, we might want other features
            indicators["rsi"] = self._calculate_rsi(df)
            indicators["ma_5"] = df['close'].rolling(window=5).mean()
            indicators["ma_20"] = df['close'].rolling(window=20).mean()
            indicators["volatility"] = df['close'].pct_change().rolling(window=20).std()
            
        # Always add some basic indicators
        indicators["sma_50"] = df['close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else None
        indicators["sma_200"] = df['close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None
        
        return indicators
    
    def _calculate_rsi(self, df, period=14):
        """
        Calculate RSI (Relative Strength Index)
        
        Args:
            df (pd.DataFrame): OHLCV data
            period (int): RSI period
            
        Returns:
            pd.Series: RSI values
        """
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1] if not rsi.empty else None
        logger.debug(f"Current RSI: {current_rsi}")
        
        return rsi
    
    def _calculate_macd(self, df, fast_period=12, slow_period=26, signal_period=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            df (pd.DataFrame): OHLCV data
            fast_period (int): Fast EMA period
            slow_period (int): Slow EMA period
            signal_period (int): Signal line period
            
        Returns:
            tuple: (MACD line, Signal line, Histogram)
        """
        # Calculate EMAs
        ema_fast = df['close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow_period, adjust=False).mean()
        
        # Calculate MACD line
        macd_line = ema_fast - ema_slow
        
        # Calculate Signal line
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        
        # Calculate Histogram
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def get_historical_prices(self, pair, timeframe='1d', limit=30):
        """
        Get historical price data for charting or analysis
        
        Args:
            pair (str): Trading pair
            timeframe (str): Timeframe string
            limit (int): Number of candles
            
        Returns:
            pd.DataFrame: Historical price data
        """
        return self._get_ohlcv_data(pair, timeframe, limit)
    
    def get_market_info(self, pair):
        """
        Get market information for a trading pair
        
        Args:
            pair (str): Trading pair
            
        Returns:
            dict: Market information including min/max orders, precision, etc.
        """
        try:
            markets = self.exchange.load_markets()
            if pair in markets:
                return markets[pair]
            logger.warning(f"Market info not found for {pair}")
            return None
        except Exception as e:
            logger.error(f"Error fetching market info: {str(e)}")
            return None
    
    def get_order_book(self, pair, limit=10):
        """
        Get order book for a trading pair
        
        Args:
            pair (str): Trading pair
            limit (int): Number of orders to fetch
            
        Returns:
            dict: Order book with bids and asks
        """
        try:
            order_book = self.exchange.fetch_order_book(pair, limit=limit)
            return order_book
        except Exception as e:
            logger.error(f"Error fetching order book: {str(e)}")
            return None
