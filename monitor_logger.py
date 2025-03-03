import os
import json
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

class MonitorLogger:
    """
    Captures strategic data during monitoring for optimization
    Used to improve HyperFocus strategy performance
    """
    
    def __init__(self):
        """Initialize the monitor logger"""
        # Ensure directories exist
        os.makedirs("data/metrics", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # File paths
        self.metrics_file = "data/metrics/strategy_metrics.csv"
        self.market_data_file = "data/market_data.csv"
        self.log_file = os.path.join("logs", "monitor_logger.log")
        
        # Initialize metrics file if it doesn't exist
        if not os.path.exists(self.metrics_file):
            self._init_metrics_file()
        
        # Load the last price for reference
        self.last_price = 0
        self.last_metrics = {}
        
        # Log initialization
        self.log(f"MonitorLogger initialized. Metrics will be saved to {self.metrics_file}")
    
    def _init_metrics_file(self):
        """Create initial metrics CSV file with headers"""
        columns = [
            'timestamp', 'strategy', 'timeframe', 'price', 'rsi_value',
            'macd_value', 'signal_value', 'macd_histogram', 
            'ma_fast_value', 'ma_slow_value', 'volume', 'avg_volume',
            'signal_generated', 'signal_type', 'confidence_score'
        ]
        
        df = pd.DataFrame(columns=columns)
        df.to_csv(self.metrics_file, index=False)
        
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Created metrics file with columns: {', '.join(columns)}\n")
    
    def log(self, message):
        """Write a log message to the monitor logger log file"""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp} - {message}\n")
    
    def capture_metrics(self, data):
        """
        Capture and save metrics from the bot monitor
        Used for strategy optimization
        
        Args:
            data: Dictionary containing metrics data points
        """
        try:
            # Ensure timestamp is present
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().isoformat()
                
            # Store the metrics
            self.last_metrics = data
            
            # Update last price if available
            if 'price' in data:
                self.last_price = data['price']
            
            # Save to CSV
            df = pd.DataFrame([data])
            if os.path.exists(self.metrics_file):
                df.to_csv(self.metrics_file, mode='a', header=False, index=False)
            else:
                df.to_csv(self.metrics_file, index=False)
                
            self.log(f"Captured metrics - Strategy: {data.get('strategy', 'unknown')}, Signal: {data.get('signal_type', 'none')}")
            return True
            
        except Exception as e:
            self.log(f"Error capturing metrics: {str(e)}")
            return False
    
    def capture_indicator_values(self, strategy_name, indicator_values, timeframe, price, volume=None):
        """
        Capture indicator values for strategy optimization
        
        Args:
            strategy_name: Name of the strategy
            indicator_values: Dictionary of indicator values
            timeframe: Timeframe of the analysis
            price: Current price
            volume: Current volume (optional)
        """
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'strategy': strategy_name,
                'timeframe': timeframe,
                'price': price,
                'volume': volume,
                'signal_generated': False,
                'signal_type': None
            }
            
            # Add indicator values
            data.update(indicator_values)
            
            # Save metrics
            return self.capture_metrics(data)
            
        except Exception as e:
            self.log(f"Error capturing indicator values: {str(e)}")
            return False
    
    def capture_signal(self, strategy_name, signal_type, timeframe, price, confidence=None, indicators=None):
        """
        Capture a trading signal with all relevant data
        
        Args:
            strategy_name: Name of the strategy
            signal_type: Type of signal (BUY/SELL)
            timeframe: Timeframe of the analysis
            price: Current price
            confidence: Signal confidence score (optional)
            indicators: Dictionary of indicator values (optional)
        """
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'strategy': strategy_name,
                'timeframe': timeframe,
                'price': price,
                'signal_generated': True,
                'signal_type': signal_type,
                'confidence_score': confidence
            }
            
            # Add indicator values if provided
            if indicators:
                data.update(indicators)
            
            # Save metrics
            success = self.capture_metrics(data)
            
            # Log the signal
            if success:
                self.log(f"Captured {signal_type} signal for {strategy_name} at price {price}")
                
            return success
            
        except Exception as e:
            self.log(f"Error capturing signal: {str(e)}")
            return False
    
    def save_market_data(self, symbol, dataframe):
        """
        Save market data for backtesting and optimization
        
        Args:
            symbol: Trading pair symbol
            dataframe: Pandas DataFrame with market data
        """
        try:
            # Ensure directory exists
            os.makedirs("data/market", exist_ok=True)
            
            # Filename with symbol
            filename = f"data/market/{symbol.replace('/', '_')}_data.csv"
            
            # Save to CSV
            dataframe.to_csv(filename, index=False)
            self.log(f"Saved market data for {symbol} to {filename}")
            return True
            
        except Exception as e:
            self.log(f"Error saving market data: {str(e)}")
            return False
    
    def get_recent_metrics(self, count=100):
        """
        Get recent metrics for analysis
        
        Args:
            count: Number of recent records to get
            
        Returns:
            Pandas DataFrame with recent metrics
        """
        try:
            if os.path.exists(self.metrics_file):
                df = pd.read_csv(self.metrics_file)
                return df.tail(count)
            return pd.DataFrame()
        except Exception as e:
            self.log(f"Error getting recent metrics: {str(e)}")
            return pd.DataFrame()
    
    def cleanup_old_data(self, days_to_keep=30):
        """
        Clean up old metrics data to prevent excessive file growth
        
        Args:
            days_to_keep: Number of days of data to preserve
        """
        try:
            if os.path.exists(self.metrics_file):
                # Load the metrics data
                df = pd.read_csv(self.metrics_file)
                
                # Convert timestamp to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Calculate cutoff date
                cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days_to_keep)
                
                # Filter data to keep
                recent_data = df[df['timestamp'] > cutoff_date]
                
                # Save only recent data
                recent_data.to_csv(self.metrics_file, index=False)
                
                # Log the cleanup
                removed_count = len(df) - len(recent_data)
                if removed_count > 0:
                    self.log(f"Cleaned up {removed_count} old metrics entries, keeping data from last {days_to_keep} days")
                
                return True
        except Exception as e:
            self.log(f"Error cleaning up old data: {str(e)}")
            return False
    
    def optimize_strategy(self):
        """
        Trigger strategy optimization using collected metrics data
        
        Returns:
            True if optimization was successful, False otherwise
        """
        try:
            # Import the optimizer here to avoid circular imports
            from strategy_optimizer import StrategyOptimizer
            
            # Create optimizer and run optimization
            optimizer = StrategyOptimizer()
            results = optimizer.optimize_hyperfocus()
            
            # Log optimization results
            if 'error' in results:
                self.log(f"Strategy optimization failed: {results['error']}")
                if 'recommendation' in results:
                    self.log(f"Recommendation: {results['recommendation']}")
                return False
            
            # Log success
            if 'optimized_params' in results:
                self.log(f"Strategy optimization successful")
                self.log(f"Optimized parameters: {results['optimized_params']}")
                
                # Apply optimization if significant improvement
                if results.get('improvement', {}).get('pnl_increase', 0) > 5:
                    if optimizer.update_strategy_config(results['optimized_params']):
                        self.log(f"✅ Applied optimized parameters to config")
                        return True
            
            return True
        except Exception as e:
            self.log(f"Error running strategy optimization: {str(e)}")
            return False
    
    def save_current_state(self):
        """Save the current monitoring state for later analysis"""
        try:
            # Create state directory if it doesn't exist
            os.makedirs("data/state", exist_ok=True)
            
            # Create state snapshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            state_file = f"data/state/monitor_state_{timestamp}.json"
            
            # Prepare state data
            state_data = {
                'timestamp': datetime.now().isoformat(),
                'last_price': self.last_price,
                'last_metrics': self.last_metrics,
                'signals_last_hour': len(self.get_recent_metrics(hours=1))
            }
            
            # Save state to file
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
            self.log(f"Saved current monitoring state to {state_file}")
            return True
        except Exception as e:
            self.log(f"Error saving current state: {str(e)}")
            return False
    
    def get_recent_metrics(self, hours=1):
        """Get metrics from the last X hours"""
        try:
            if os.path.exists(self.metrics_file):
                df = pd.read_csv(self.metrics_file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Filter for recent data
                cutoff_time = pd.Timestamp.now() - pd.Timedelta(hours=hours)
                recent_df = df[df['timestamp'] > cutoff_time]
                
                return recent_df
            return pd.DataFrame()
        except Exception as e:
            self.log(f"Error getting recent metrics: {str(e)}")
            return pd.DataFrame()
