import logging
import time
import ccxt
import json
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger("BROski.ExchangeConnector")

class ExchangeConnector:
    """
    Class responsible for connecting to and executing trades on cryptocurrency exchanges.
    Primary implementation for MEXC exchange with ccxt library.
    """
    
    def __init__(self, config):
        """
        Initialize the exchange connector with configuration.
        
        Args:
            config: Configuration object containing exchange settings
        """
        self.config = config
        self.exchange_client = None
        self.exchange_info = {}
        self.markets = {}
        self.last_api_call_time = 0
        self.min_time_between_calls = 0.1  # 100ms minimum between API calls to avoid rate limits
        self._initialize_exchange_client()
        self._load_market_info()
        logger.info(f"Exchange connector initialized for {self.config['exchange']['name']}")
    
    def _initialize_exchange_client(self):
        """
        Set up the connection to the exchange API based on configuration.
        """
        try:
            exchange_name = self.config['exchange']['name'].lower()
            api_key = self.config['exchange']['api_key']
            api_secret = self.config['exchange']['api_secret']
            
            # Verify we have the necessary credentials
            if not api_key or not api_secret:
                logger.error("API key or secret is missing in configuration")
                raise ValueError("API key or secret is missing")
            
            # Initialize exchange-specific client
            if exchange_name == "mexc":
                self.exchange_client = ccxt.mexc({
                    'apiKey': api_key,
                    'secret': api_secret,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot'
                    }
                })
                
                # Check if using testnet
                if self.config['exchange'].get('testnet', False):
                    if hasattr(self.exchange_client, 'set_sandbox_mode'):
                        self.exchange_client.set_sandbox_mode(True)
                        logger.info("Exchange client set to testnet/sandbox mode")
            else:
                raise ValueError(f"Unsupported exchange: {exchange_name}")
            
            # Test connection
            self._respect_rate_limit()
            server_time = self.exchange_client.fetch_time()
            time_diff = abs(server_time - int(time.time() * 1000))
            
            logger.info(f"Connected to {exchange_name.upper()}. Server time diff: {time_diff}ms")
            
        except ccxt.AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            raise
        except ccxt.NetworkError as e:
            logger.error(f"Network error when connecting to exchange: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize exchange client: {e}")
            raise
    
    def _load_market_info(self):
        """
        Load market information from the exchange
        """
        try:
            self._respect_rate_limit()
            self.markets = self.exchange_client.load_markets()
            
            # Get trading pair from config
            base = self.config['trading']['base_symbol']
            quote = self.config['trading']['quote_symbol']
            symbol = f"{base}/{quote}"
            
            if symbol in self.markets:
                self.exchange_info = self.markets[symbol]
                logger.info(f"Loaded market info for {symbol}")
                
                # Log trading limits
                min_amount = self.exchange_info.get('limits', {}).get('amount', {}).get('min', 'unknown')
                min_price = self.exchange_info.get('limits', {}).get('price', {}).get('min', 'unknown')
                min_cost = self.exchange_info.get('limits', {}).get('cost', {}).get('min', 'unknown')
                
                logger.info(f"Trading limits for {symbol}: min amount: {min_amount}, min price: {min_price}, min cost: {min_cost}")
            else:
                available_symbols = list(self.markets.keys())[:10]  # Show first 10 for brevity
                logger.error(f"Symbol {symbol} not found in exchange. Available symbols include: {available_symbols}...")
                raise ValueError(f"Trading pair {symbol} not found on exchange")
                
        except Exception as e:
            logger.error(f"Error loading market info: {e}")
            raise
    
    def _respect_rate_limit(self):
        """
        Ensure we don't exceed API rate limits by adding delays between calls
        """
        current_time = time.time()
        elapsed = current_time - self.last_api_call_time
        
        if elapsed < self.min_time_between_calls:
            sleep_time = self.min_time_between_calls - elapsed
            time.sleep(sleep_time)
            
        self.last_api_call_time = time.time()
    
    def get_trading_symbol(self) -> str:
        """
        Get the trading symbol in exchange format
        
        Returns:
            str: Trading symbol (e.g. "BTC/USDT")
        """
        base = self.config['trading']['base_symbol']
        quote = self.config['trading']['quote_symbol']
        return f"{base}/{quote}"
    
    def get_balance(self) -> Dict[str, float]:
        """
        Get account balance for trading pair
        
        Returns:
            Dict[str, float]: Balance information for base and quote currencies
        """
        try:
            self._respect_rate_limit()
            balance = self.exchange_client.fetch_balance()
            
            base = self.config['trading']['base_symbol']
            quote = self.config['trading']['quote_symbol']
            
            result = {
                'base': {
                    'symbol': base,
                    'free': float(balance.get('free', {}).get(base, 0)),
                    'used': float(balance.get('used', {}).get(base, 0)),
                    'total': float(balance.get('total', {}).get(base, 0))
                },
                'quote': {
                    'symbol': quote,
                    'free': float(balance.get('free', {}).get(quote, 0)),
                    'used': float(balance.get('used', {}).get(quote, 0)),
                    'total': float(balance.get('total', {}).get(quote, 0))
                }
            }
            
            logger.info(f"Account balance - {base}: {result['base']['total']}, {quote}: {result['quote']['total']}")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return {
                'base': {'symbol': self.config['trading']['base_symbol'], 'free': 0, 'used': 0, 'total': 0},
                'quote': {'symbol': self.config['trading']['quote_symbol'], 'free': 0, 'used': 0, 'total': 0}
            }
    
    def get_ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current ticker information for a symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "BTC/USDT")
            
        Returns:
            Dict[str, Any]: Ticker information
        """
        try:
            if not symbol:
                symbol = self.get_trading_symbol()
                
            self._respect_rate_limit()
            ticker = self.exchange_client.fetch_ticker(symbol)
            
            logger.debug(f"Fetched ticker for {symbol}: Last price: {ticker['last']}")
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return {}
    
    def get_price(self, symbol: Optional[str] = None) -> float:
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            float: Current price
        """
        ticker = self.get_ticker(symbol)
        if ticker and 'last' in ticker:
            return float(ticker['last'])
        return 0.0
    
    def execute_trade(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a trade on the exchange based on the given signal.
        
        Args:
            signal: Trading signal dictionary
            
        Returns:
            Dict[str, Any]: Execution result
        """
        try:
            # Extract signal details
            symbol = signal.get('symbol', self.get_trading_symbol())
            trade_type = signal.get('type', '')  # 'buy' or 'sell'
            price = signal.get('price', 0)
            position_size = signal.get('position_size')
            
            # If no position size in signal, use config trade amount
            if position_size is None:
                position_size = self.config['trading']['trade_amount']
                
            # Calculate amount in base currency
            if trade_type.lower() == 'buy' and price > 0:
                # For buy orders, we're spending quote currency (e.g. USDT)
                # Calculate how much base currency (e.g. BTC) we can get
                amount = position_size / price
            else:
                # For sell orders, amount is directly in base currency
                amount = position_size
                
            # Apply exchange-specific precision rules
            if symbol in self.markets:
                # Get precision for amount from exchange info
                precision = self.markets[symbol].get('precision', {}).get('amount')
                if precision:
                    # Round amount to exchange precision
                    amount = round(amount, precision) if isinstance(precision, int) else amount
                    
            logger.info(f"Executing {trade_type} order for {amount} {symbol} at {price}")
            
            # Check if auto_trade is enabled
            if not self.config['trading'].get('auto_trade', False):
                logger.info("Auto-trading disabled. Simulating trade execution.")
                
                # Simulated execution
                execution_result = {
                    'success': True,
                    'order_id': f"simulated_{int(time.time())}",
                    'symbol': symbol,
                    'type': trade_type,
                    'side': trade_type.lower(),
                    'amount': amount,
                    'price': price,
                    'value': price * amount,
                    'timestamp': int(time.time() * 1000),
                    'datetime': datetime.now().isoformat(),
                    'status': 'closed',
                    'simulated': True,
                    'exchange': self.config['exchange']['name']
                }
                
                logger.info(f"Simulated trade: {execution_result}")
                return execution_result
            
            # Execute actual trade on exchange
            self._respect_rate_limit()
            
            # Prepare order parameters
            order_type = 'market'  # or 'limit'
            params = {}
            
            # Place order
            response = self.exchange_client.create_order(
                symbol=symbol,
                type=order_type,
                side=trade_type.lower(),
                amount=amount,
                price=price if order_type == 'limit' else None,
                params=params
            )
            
            # Format execution result
            execution_result = {
                'success': True,
                'order_id': response.get('id', ''),
                'symbol': symbol,
                'type': trade_type,
                'side': trade_type.lower(),
                'amount': amount,
                'price': price,
                'value': price * amount,
                'timestamp': int(time.time() * 1000),
                'datetime': datetime.now().isoformat(),
                'status': response.get('status', ''),
                'exchange': self.config['exchange']['name']
            }
            
            logger.info(f"Trade executed successfully: {execution_result['order_id']}")
            
            # Save trade to history
            self._save_trade_history(execution_result)
            
            return execution_result
            
        except ccxt.InsufficientFunds as e:
            logger.error(f"Insufficient funds for trade execution: {e}")
            return self._create_error_result(signal, "Insufficient funds", e)
        except ccxt.InvalidOrder as e:
            logger.error(f"Invalid order: {e}")
            return self._create_error_result(signal, "Invalid order", e)
        except Exception as e:
            logger.error(f"Failed to execute trade: {e}")
            return self._create_error_result(signal, "Execution failed", e)
    
    def _create_error_result(self, signal, error_type, exception) -> Dict[str, Any]:
        """Create standardized error result"""
        return {
            'success': False,
            'error_type': error_type,
            'error': str(exception),
            'symbol': signal.get('symbol', self.get_trading_symbol()),
            'type': signal.get('type', ''),
            'side': signal.get('type', '').lower(),
            'amount': signal.get('position_size', self.config['trading']['trade_amount']),
            'price': signal.get('price', 0),
            'timestamp': int(time.time() * 1000),
            'datetime': datetime.now().isoformat(),
            'exchange': self.config['exchange']['name']
        }
    
    def _save_trade_history(self, trade: Dict[str, Any]) -> None:
        """
        Save trade to history file
        
        Args:
            trade: Trade execution result
        """
        try:
            history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
            os.makedirs(history_dir, exist_ok=True)
            history_file = os.path.join(history_dir, 'trade_history.json')
            
            # Load existing history
            trades = []
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    try:
                        trades = json.load(f)
                    except json.JSONDecodeError:
                        trades = []
            
            # Add new trade
            trades.append(trade)
            
            # Save updated history
            with open(history_file, 'w') as f:
                json.dump(trades, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving trade history: {e}")
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of open orders
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            List[Dict[str, Any]]: List of open orders
        """
        try:
            if not symbol:
                symbol = self.get_trading_symbol()
                
            self._respect_rate_limit()
            orders = self.exchange_client.fetch_open_orders(symbol=symbol)
            
            logger.debug(f"Fetched {len(orders)} open orders for {symbol}")
            return orders
        except Exception as e:
            logger.error(f"Error fetching open orders: {e}")
            return []
    
    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        """
        Cancel an open order
        
        Args:
            order_id: ID of the order to cancel
            symbol: Trading pair symbol
            
        Returns:
            bool: True if cancelled successfully
        """
        try:
            if not symbol:
                symbol = self.get_trading_symbol()
                
            self._respect_rate_limit()
            self.exchange_client.cancel_order(order_id, symbol)
            logger.info(f"Order {order_id} cancelled successfully")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    def cancel_all_orders(self, symbol: Optional[str] = None) -> bool:
        """
        Cancel all open orders for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            bool: True if all orders cancelled successfully
        """
        try:
            if not symbol:
                symbol = self.get_trading_symbol()
                
            open_orders = self.get_open_orders(symbol)
            success = True
            
            for order in open_orders:
                if not self.cancel_order(order['id'], symbol):
                    success = False
            
            logger.info(f"Cancelled all orders for {symbol}")
            return success
        except Exception as e:
            logger.error(f"Error cancelling all orders: {e}")
            return False
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test connection to the exchange
        
        Returns:
            Tuple[bool, str]: Success status and message
        """
        try:
            self._respect_rate_limit()
            # Fetch exchange time
            exchange_time = self.exchange_client.fetch_time()
            local_time = int(time.time() * 1000)
            time_diff = abs(exchange_time - local_time)
            
            # Fetch balance to test authentication
            balance = self.exchange_client.fetch_balance()
            
            return True, f"Connection successful! Time difference: {time_diff}ms"
        except ccxt.AuthenticationError:
            return False, "Authentication failed. Check your API keys."
        except ccxt.NetworkError:
            return False, "Network error. Check your internet connection."
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_historical_data(self, symbol: Optional[str] = None, timeframe: str = '1h', limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get historical OHLCV data
        
        Args:
            symbol: Trading pair symbol
            timeframe: Candle timeframe (1m, 5m, 15m, 1h, etc)
            limit: Number of candles to retrieve
            
        Returns:
            List[Dict[str, Any]]: Historical candle data
        """
        try:
            if not symbol:
                symbol = self.get_trading_symbol()
                
            self._respect_rate_limit()
            ohlcv = self.exchange_client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            
            # Convert to readable format
            candles = []
            for candle in ohlcv:
                candles.append({
                    'timestamp': candle[0],
                    'datetime': datetime.fromtimestamp(candle[0] / 1000).isoformat(),
                    'open': candle[1],
                    'high': candle[2],
                    'low': candle[3],
                    'close': candle[4],
                    'volume': candle[5]
                })
            
            logger.debug(f"Fetched {len(candles)} {timeframe} candles for {symbol}")
            return candles
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return []
