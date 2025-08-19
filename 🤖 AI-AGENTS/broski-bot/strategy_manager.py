import logging
import importlib
import os
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger("BROski.StrategyManager")

class StrategyManager:
    """
    Manages trading strategies for BROski Bot
    """
    
    def __init__(self, config):
        """Initialize strategy manager with config"""
        self.config = config
        self.active_strategy_name = config["strategies"]["active_strategy"]
        self.active_strategy = None
        self.load_active_strategy()
        
    def load_active_strategy(self):
        """Load the active strategy based on configuration"""
        try:
            logger.info(f"Loading strategy: {self.active_strategy_name}")
            
            # Map strategy names to module paths
            strategy_map = {
                "rsi_strategy": ("strategies.rsi_strategy", "RSIStrategy"),
                "macd_strategy": ("strategies.macd_strategy", "MACDStrategy"),
                "ml_strategy": ("strategies.lite_ml_strategy", "LiteMLStrategy"),
                "hyperfocus_strategy": ("strategies.hyperfocus_strategy", "HyperFocusStrategy")
            }
            
            if self.active_strategy_name not in strategy_map:
                logger.error(f"Unknown strategy: {self.active_strategy_name}")
                return False
            
            # Get module and class name
            module_path, class_name = strategy_map[self.active_strategy_name]
            
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the strategy class
            strategy_class = getattr(module, class_name)
            
            # Instantiate the strategy
            self.active_strategy = strategy_class(self.config["strategies"][self.active_strategy_name])
            
            logger.info(f"Successfully loaded {self.active_strategy_name}")
            return True
            
        except ImportError as e:
            logger.error(f"Failed to import strategy module: {str(e)}")
            return False
        except AttributeError as e:
            logger.error(f"Strategy class not found: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error loading strategy: {str(e)}")
            return False
    
    def generate_signals(self, df):
        """Generate signals using the active strategy"""
        if self.active_strategy is None:
            logger.error("No active strategy loaded")
            return []
        
        try:
            return self.active_strategy.generate_signals(df)
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
            return []
    
    def get_strategy_info(self):
        """Get information about the active strategy"""
        return {
            "name": self.active_strategy_name,
            "config": self.config["strategies"][self.active_strategy_name],
            "status": "active" if self.active_strategy is not None else "error"
        }
    
    def set_strategy(self, strategy_name):
        """Change the active strategy"""
        if strategy_name in self.config["strategies"]:
            self.active_strategy_name = strategy_name
            self.load_active_strategy()
            return True
        else:
            logger.error(f"Unknown strategy: {strategy_name}")
            return False
