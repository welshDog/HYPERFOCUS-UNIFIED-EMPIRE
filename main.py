import logging
import time
import os
from config import Config
from data_fetcher import DataFetcher
from strategy_manager import StrategyManager
from risk_manager import RiskManager
from exchange_connector import ExchangeConnector
from performance_tracker import PerformanceTracker
from notification_service import NotificationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("broski_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BROski")

class BroskiBot:
    def __init__(self):
        logger.info("Initializing BROski Crypto Bot...")
        self.config = Config()
        self.data_fetcher = DataFetcher(self.config)
        self.exchange = ExchangeConnector(self.config)
        self.risk_manager = RiskManager(self.config)
        self.strategy_manager = StrategyManager(self.config, self.data_fetcher)
        self.performance_tracker = PerformanceTracker(self.config)
        self.notification_service = NotificationService(self.config)
        logger.info("BROski Crypto Bot initialized successfully!")

    def run(self):
        logger.info("BROski Crypto Bot starting...")
        
        while True:
            try:
                # Fetch latest market data
                market_data = self.data_fetcher.get_latest_data()
                
                # Generate trading signals
                signals = self.strategy_manager.generate_signals(market_data)
                
                # Apply risk management rules
                filtered_signals = self.risk_manager.filter_signals(signals)
                
                # Execute trades
                for signal in filtered_signals:
                    execution_result = self.exchange.execute_trade(signal)
                    self.performance_tracker.record_trade(execution_result)
                    self.notification_service.send_trade_notification(execution_result)
                
                # Update performance metrics
                self.performance_tracker.update_metrics()
                
                # Sleep until next cycle
                time.sleep(self.config.cycle_interval)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.notification_service.send_error_notification(str(e))
                time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    bot = BroskiBot()
    bot.run()
