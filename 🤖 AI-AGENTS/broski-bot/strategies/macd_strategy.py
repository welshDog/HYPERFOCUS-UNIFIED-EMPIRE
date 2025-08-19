import logging
import numpy as np
import pandas as pd

logger = logging.getLogger("BROski.MACDStrategy")

class MACDStrategy:
    """
    Strategy based on Moving Average Convergence Divergence (MACD)
    Generates buy signals when MACD line crosses above signal line
    Generates sell signals when MACD line crosses below signal line
    """
    
    def __init__(self, config):
        self.config = config
        self.timeframe = config.get("timeframe", "15m")
        self.fast_period = config.get("fast_period", 12)
        self.slow_period = config.get("slow_period", 26)
        self.signal_period = config.get("signal_period", 9)
        
    def calculate_macd(self, prices):
        """Calculate MACD indicator"""
        # Calculate EMA with fast period
        ema_fast = self._calculate_ema(prices, self.fast_period)
        
        # Calculate EMA with slow period
        ema_slow = self._calculate_ema(prices, self.slow_period)
        
        # Calculate MACD line (fast EMA - slow EMA)
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line (EMA of MACD line)
        signal_line = self._calculate_ema(macd_line, self.signal_period)
        
        # Calculate histogram (MACD line - signal line)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def _calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        ema = np.zeros_like(prices)
        
        # Start with SMA for the first period
        ema[:period] = np.mean(prices[:period])
        
        # Calculate EMA using the formula: EMA_today = (Price_today * k) + (EMA_yesterday * (1-k))
        # where k = 2 / (period + 1)
        k = 2.0 / (period + 1)
        
        for i in range(period, len(prices)):
            ema[i] = prices[i] * k + ema[i-1] * (1-k)
            
        return ema
    
    def generate_signals(self, df):
        """Generate trading signals based on MACD crossovers"""
        signals = []
        
        if len(df) < self.slow_period + self.signal_period:
            logger.warning(f"Not enough data for MACD calculation. Need at least {self.slow_period + self.signal_period} candles.")
            return signals
            
        try:
            # Calculate MACD indicators if not already in the dataframe
            if 'macd_line' not in df.columns or 'signal_line' not in df.columns:
                prices = df['close'].values
                macd_line, signal_line, histogram = self.calculate_macd(prices)
                
                df['macd_line'] = macd_line
                df['signal_line'] = signal_line
                df['macd_histogram'] = histogram
            
            # Get the latest values
            current_macd = df['macd_line'].iloc[-1]
            current_signal = df['signal_line'].iloc[-1]
            previous_macd = df['macd_line'].iloc[-2]
            previous_signal = df['signal_line'].iloc[-2]
            
            logger.info(f"Current MACD: {current_macd:.6f}, Signal: {current_signal:.6f}")
            
            # Check for bullish crossover (MACD crosses above signal line)
            if current_macd > current_signal and previous_macd <= previous_signal:
                signals.append({
                    'type': 'buy',
                    'price': df['close'].iloc[-1],
                    'macd': current_macd,
                    'signal': current_signal,
                    'timestamp': df.index[-1]
                })
                logger.info(f"🟢 BUY signal generated (MACD: {current_macd:.6f} crossed above Signal: {current_signal:.6f})")
                
            # Check for bearish crossover (MACD crosses below signal line)
            elif current_macd < current_signal and previous_macd >= previous_signal:
                signals.append({
                    'type': 'sell',
                    'price': df['close'].iloc[-1],
                    'macd': current_macd,
                    'signal': current_signal,
                    'timestamp': df.index[-1]
                })
                logger.info(f"🔴 SELL signal generated (MACD: {current_macd:.6f} crossed below Signal: {current_signal:.6f})")
                
            return signals
            
        except Exception as e:
            logger.error(f"Error generating MACD signals: {str(e)}")
            return []
