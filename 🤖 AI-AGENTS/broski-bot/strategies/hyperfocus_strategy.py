import logging
import numpy as np
import pandas as pd
from datetime import datetime

logger = logging.getLogger("BROski.HyperFocus")

class HyperFocusStrategy:
    """
    HyperFocus Strategy - Advanced multi-indicator trading strategy
    Combines RSI, MACD, Volume, and Moving Averages for high-precision signals
    """
    
    def __init__(self, config):
        """Initialize HyperFocus strategy with configuration"""
        self.config = config.get("hyperfocus_strategy", {})
        
        # Primary indicator settings (RSI)
        self.timeframe = self.config.get("timeframe", "15m")
        self.rsi_period = self.config.get("rsi_period", 14)
        self.rsi_overbought = self.config.get("rsi_overbought", 70)
        self.rsi_oversold = self.config.get("rsi_oversold", 30)
        
        # Secondary indicator settings (MACD)
        self.fast_period = self.config.get("fast_period", 12)
        self.slow_period = self.config.get("slow_period", 26)
        self.signal_period = self.config.get("signal_period", 9)
        
        # Moving Average settings
        self.ma_fast = self.config.get("ma_fast", 20)
        self.ma_slow = self.config.get("ma_slow", 50)
        
        # Volume threshold settings
        self.volume_factor = self.config.get("volume_factor", 1.5)
        self.volume_lookback = self.config.get("volume_lookback", 20)
        
        # Signal strengthening options
        self.require_confirmation = self.config.get("require_confirmation", True)
        self.smart_exit = self.config.get("smart_exit", True)
        
        logger.info("HyperFocus strategy initialized")
    
    def calculate_indicators(self, df):
        """Calculate all indicators needed for the strategy"""
        # Make sure we have enough data
        if len(df) < max(self.rsi_period, self.slow_period, self.ma_slow) + 10:
            logger.warning("Not enough data for HyperFocus strategy indicators")
            return df
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Calculate MACD
        ema_fast = df['close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.slow_period, adjust=False).mean()
        df['macd_line'] = ema_fast - ema_slow
        df['signal_line'] = df['macd_line'].ewm(span=self.signal_period, adjust=False).mean()
        df['macd_histogram'] = df['macd_line'] - df['signal_line']
        
        # Calculate Moving Averages
        df['ma_fast'] = df['close'].rolling(window=self.ma_fast).mean()
        df['ma_slow'] = df['close'].rolling(window=self.ma_slow).mean()
        
        # Calculate Volume indicators
        df['volume_sma'] = df['volume'].rolling(window=self.volume_lookback).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # Calculate Price Action indicators
        df['high_low_range'] = df['high'] - df['low']
        df['range_sma'] = df['high_low_range'].rolling(window=14).mean()
        df['volatility'] = df['high_low_range'] / df['range_sma']
        
        # Additional trend strength indicator
        df['trend_strength'] = (df['close'] - df['close'].rolling(window=20).mean()) / df['close'].rolling(window=20).std()
        
        return df
    
    def check_rsi_signal(self, df, index):
        """Check for RSI signals"""
        current_rsi = df['rsi'].iloc[index]
        previous_rsi = df['rsi'].iloc[index-1]
        
        # Buy signal - RSI crossing above oversold threshold
        if previous_rsi < self.rsi_oversold and current_rsi >= self.rsi_oversold:
            return "buy", f"RSI crossed above oversold ({current_rsi:.2f})"
            
        # Sell signal - RSI crossing below overbought threshold
        elif previous_rsi > self.rsi_overbought and current_rsi <= self.rsi_overbought:
            return "sell", f"RSI crossed below overbought ({current_rsi:.2f})"
            
        return None, None
    
    def check_macd_signal(self, df, index):
        """Check for MACD signals"""
        current_macd = df['macd_line'].iloc[index]
        current_signal = df['signal_line'].iloc[index]
        previous_macd = df['macd_line'].iloc[index-1]
        previous_signal = df['signal_line'].iloc[index-1]
        
        # Buy signal - MACD crossing above signal line
        if previous_macd < previous_signal and current_macd > current_signal:
            return "buy", "MACD crossed above signal line"
            
        # Sell signal - MACD crossing below signal line
        elif previous_macd > previous_signal and current_macd < current_signal:
            return "sell", "MACD crossed below signal line"
            
        return None, None
    
    def check_ma_signal(self, df, index):
        """Check for Moving Average signals"""
        current_ma_fast = df['ma_fast'].iloc[index]
        current_ma_slow = df['ma_slow'].iloc[index]
        previous_ma_fast = df['ma_fast'].iloc[index-1]
        previous_ma_slow = df['ma_slow'].iloc[index-1]
        
        # Buy signal - Fast MA crossing above Slow MA
        if previous_ma_fast < previous_ma_slow and current_ma_fast > current_ma_slow:
            return "buy", f"MA{self.ma_fast} crossed above MA{self.ma_slow}"
            
        # Sell signal - Fast MA crossing below Slow MA
        elif previous_ma_fast > previous_ma_slow and current_ma_fast < current_ma_slow:
            return "sell", f"MA{self.ma_fast} crossed below MA{self.ma_slow}"
            
        return None, None
    
    def check_volume_confirmation(self, df, index, signal_type):
        """Check if volume confirms the signal"""
        volume_ratio = df['volume_ratio'].iloc[index]
        
        # High volume confirms the signal
        if volume_ratio > self.volume_factor:
            return True, f"Volume {volume_ratio:.2f}x above average"
        
        return False, f"Volume insufficient ({volume_ratio:.2f}x)"
    
    def generate_signals(self, df):
        """Generate trading signals using the HyperFocus strategy"""
        signals = []
        
        if df is None or df.empty:
            logger.warning("No data available for signal generation")
            return signals
            
        # Ensure we have calculated all necessary indicators
        df = self.calculate_indicators(df)
        
        # We need at least one previous candle to compare
        if len(df) < 2:
            logger.warning("Not enough data for signal generation")
            return signals
        
        # Get the current candle index (last row)
        index = len(df) - 1
        
        # Check primary signal (RSI)
        primary_signal, primary_reason = self.check_rsi_signal(df, index)
        
        if primary_signal:
            # Check for confirmation signals
            macd_signal, macd_reason = self.check_macd_signal(df, index)
            ma_signal, ma_reason = self.check_ma_signal(df, index)
            volume_confirmed, volume_reason = self.check_volume_confirmation(df, index, primary_signal)
            
            # Determine confirmation strength
            confirmations = 0
            confirmation_text = []
            
            if macd_signal == primary_signal:
                confirmations += 1
                confirmation_text.append(macd_reason)
                
            if ma_signal == primary_signal:
                confirmations += 1
                confirmation_text.append(ma_reason)
                
            if volume_confirmed:
                confirmations += 1
                confirmation_text.append(volume_reason)
            
            # Generate signal if we have enough confirmations
            if (not self.require_confirmation) or (confirmations >= 1):
                confirmation_str = ", ".join(confirmation_text) if confirmation_text else "No confirmations"
                
                signal = {
                    'type': primary_signal,
                    'price': df['close'].iloc[index],
                    'timestamp': df.index[index],
                    'primary_reason': primary_reason,
                    'confirmations': confirmations,
                    'confirmation_details': confirmation_str,
                    'strength': min(confirmations / 3.0, 1.0)  # Signal strength 0-1
                }
                
                if primary_signal == "buy":
                    logger.info(f"🟢 BUY signal: {primary_reason}, Confirmations: {confirmations}/3")
                else:
                    logger.info(f"🔴 SELL signal: {primary_reason}, Confirmations: {confirmations}/3")
                
                signals.append(signal)
        
        return signals
