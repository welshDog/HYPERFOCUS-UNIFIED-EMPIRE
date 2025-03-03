import logging
import numpy as np
import pandas as pd

logger = logging.getLogger("BROski.RSIStrategy")

class RSIStrategy:
    """
    Strategy based on Relative Strength Index (RSI)
    Generates buy signals when RSI is below oversold threshold
    Generates sell signals when RSI is above overbought threshold
    """
    
    def __init__(self, config):
        self.config = config
        self.timeframe = config.get("timeframe", "5m")
        self.rsi_period = config.get("rsi_period", 14)
        self.rsi_overbought = config.get("rsi_overbought", 70)
        self.rsi_oversold = config.get("rsi_oversold", 30)
        
    def calculate_rsi(self, prices):
        """Calculate RSI indicator"""
        deltas = np.diff(prices)
        seed = deltas[:self.rsi_period+1]
        
        # Calculate gains and losses
        up = seed[seed >= 0].sum() / self.rsi_period
        down = -seed[seed < 0].sum() / self.rsi_period
        
        if down == 0:
            rs = float('inf')
        else:
            rs = up / down
            
        rsi = np.zeros_like(prices)
        rsi[:self.rsi_period+1] = 100. - (100. / (1. + rs))
        
        # Calculate RSI for the rest of the data
        for i in range(self.rsi_period+1, len(prices)):
            delta = deltas[i-1]
            
            if delta > 0:
                upval = delta
                downval = 0
            else:
                upval = 0
                downval = -delta
                
            # Use exponential moving average
            up = (up * (self.rsi_period-1) + upval) / self.rsi_period
            down = (down * (self.rsi_period-1) + downval) / self.rsi_period
            
            if down == 0:
                rs = float('inf')
            else:
                rs = up / down
                
            rsi[i] = 100. - (100. / (1. + rs))
            
        return rsi
    
    def generate_signals(self, df):
        """Generate trading signals based on RSI values"""
        signals = []
        
        if len(df) < self.rsi_period + 10:
            logger.warning(f"Not enough data for RSI calculation. Need at least {self.rsi_period + 10} candles.")
            return signals
            
        try:
            # Calculate RSI if not already in the dataframe
            if 'rsi' not in df.columns:
                prices = df['close'].values
                rsi_values = self.calculate_rsi(prices)
                df['rsi'] = rsi_values
            
            # Get the latest RSI value
            latest_rsi = df['rsi'].iloc[-1]
            previous_rsi = df['rsi'].iloc[-2]
            
            logger.info(f"Current RSI: {latest_rsi:.2f}, Previous RSI: {previous_rsi:.2f}")
            
            # Generate buy signal if RSI crosses below oversold threshold
            if latest_rsi < self.rsi_oversold and previous_rsi >= self.rsi_oversold:
                signals.append({
                    'type': 'buy',
                    'price': df['close'].iloc[-1],
                    'rsi': latest_rsi,
                    'timestamp': df.index[-1]
                })
                logger.info(f"🟢 BUY signal generated (RSI: {latest_rsi:.2f} < {self.rsi_oversold})")
                
            # Generate sell signal if RSI crosses above overbought threshold
            elif latest_rsi > self.rsi_overbought and previous_rsi <= self.rsi_overbought:
                signals.append({
                    'type': 'sell',
                    'price': df['close'].iloc[-1],
                    'rsi': latest_rsi,
                    'timestamp': df.index[-1]
                })
                logger.info(f"🔴 SELL signal generated (RSI: {latest_rsi:.2f} > {self.rsi_overbought})")
                
            return signals
            
        except Exception as e:
            logger.error(f"Error generating RSI signals: {str(e)}")
            return []
