import logging
from datetime import datetime, timedelta

logger = logging.getLogger("BROski.RiskManager")

class RiskManager:
    """
    Handles risk management for BROski trading operations.
    Applies risk rules to filter trading signals and manage position sizes.
    """

    def __init__(self, config):
        """
        Initialize risk manager with configuration
        
        Args:
            config (dict): Risk management configuration
        """
        self.config = config
        self.risk_config = config.get("risk_management", {})
        
        # Extract risk management parameters
        self.stop_loss_percentage = self.risk_config.get("stop_loss_percentage", 2.0)
        self.take_profit_percentage = self.risk_config.get("take_profit_percentage", 4.0)
        self.max_daily_trades = self.risk_config.get("max_daily_trades", 10)
        self.max_open_positions = self.risk_config.get("max_open_positions", 3)
        self.max_position_size = config["trading"].get("max_position_size", 100.0)
        
        # Track open positions and daily trades
        self.open_positions = []
        self.daily_trades = []
        
        # Track total account exposure
        self.total_exposure = 0.0
        self.max_exposure_percentage = self.risk_config.get("max_exposure_percentage", 50.0)
        
        logger.info(f"Risk Manager initialized with SL: {self.stop_loss_percentage}%, TP: {self.take_profit_percentage}%")
    
    def update_portfolio(self, positions, account_balance):
        """
        Update the risk manager with current open positions and account balance
        
        Args:
            positions (list): List of current open positions
            account_balance (float): Current account balance
        """
        self.open_positions = positions
        self.account_balance = account_balance
        
        # Calculate total exposure
        self.total_exposure = sum(position["value"] for position in positions)
        self.exposure_percentage = (self.total_exposure / account_balance) * 100 if account_balance > 0 else 0
        
        logger.debug(f"Portfolio updated: {len(positions)} open positions, {self.exposure_percentage:.2f}% exposure")
    
    def clean_daily_trades(self):
        """Remove trades older than 24 hours from daily trades tracking"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=1)
        self.daily_trades = [trade for trade in self.daily_trades if trade["timestamp"] > cutoff_time]
    
    def can_open_new_position(self):
        """Check if a new position can be opened based on risk rules"""
        # Clean old trades first
        self.clean_daily_trades()
        
        # Check number of open positions
        if len(self.open_positions) >= self.max_open_positions:
            logger.warning(f"Maximum open positions reached ({self.max_open_positions})")
            return False
        
        # Check daily trade limit
        if len(self.daily_trades) >= self.max_daily_trades:
            logger.warning(f"Maximum daily trades reached ({self.max_daily_trades})")
            return False
        
        # Check total exposure
        if self.exposure_percentage >= self.max_exposure_percentage:
            logger.warning(f"Maximum exposure reached ({self.exposure_percentage:.2f}%)")
            return False
            
        return True
    
    def calculate_position_size(self, price, signal_type, signal_strength=None):
        """
        Calculate appropriate position size based on risk parameters
        
        Args:
            price (float): Current price
            signal_type (str): Type of signal (buy/sell)
            signal_strength (float): Optional signal strength from HyperFocus (0-1)
            
        Returns:
            float: Appropriate position size
        """
        base_amount = self.config["trading"].get("trade_amount", 10.0)
        
        # Apply position sizing logic based on signal strength if available
        # HyperFocus signals might have strength information
        if signal_strength is not None:
            # Adjust trade amount based on signal strength
            position_size = base_amount * (0.5 + 0.5 * signal_strength)
        else:
            position_size = base_amount
        
        # Make sure we don't exceed max position size
        position_size = min(position_size, self.max_position_size)
        
        return position_size
        
    def filter_signals(self, signals):
        """
        Apply risk management rules to filter trading signals
        
        Args:
            signals (list): List of trading signals
            
        Returns:
            list: Filtered list of signals that pass risk management criteria
        """
        filtered_signals = []
        
        for signal in signals:
            # Skip if we can't open new positions
            if signal["type"] == "buy" and not self.can_open_new_position():
                logger.info(f"Signal rejected due to risk management constraints: {signal}")
                continue
            
            # Get signal strength if available (HyperFocus mode provides this)
            signal_strength = signal.get("strength")
                
            # Calculate appropriate position size
            position_size = self.calculate_position_size(
                signal.get("price", 0), 
                signal["type"],
                signal_strength
            )
            
            # Add position size to signal
            signal["position_size"] = position_size
            
            # Add stop loss and take profit levels
            if signal["type"] == "buy":
                signal["stop_loss"] = signal.get("price", 0) * (1 - self.stop_loss_percentage / 100)
                signal["take_profit"] = signal.get("price", 0) * (1 + self.take_profit_percentage / 100)
            elif signal["type"] == "sell":
                signal["stop_loss"] = signal.get("price", 0) * (1 + self.stop_loss_percentage / 100)
                signal["take_profit"] = signal.get("price", 0) * (1 - self.take_profit_percentage / 100)
            
            # If the signal passes all filters, add it to filtered signals
            filtered_signals.append(signal)
            
            # Track this trade for daily limits
            if signal["type"] in ["buy", "sell"]:
                self.daily_trades.append({
                    "timestamp": datetime.now(),
                    "type": signal["type"],
                    "price": signal.get("price", 0),
                    "size": position_size
                })
        
        logger.debug(f"Risk manager filtered {len(signals)} signals to {len(filtered_signals)}")
        return filtered_signals
    
    def get_risk_metrics(self):
        """
        Get current risk metrics
        
        Returns:
            dict: Dictionary containing risk metrics
        """
        self.clean_daily_trades()
        
        return {
            "open_positions": len(self.open_positions),
            "daily_trades": len(self.daily_trades),
            "exposure_percentage": self.exposure_percentage,
            "max_daily_trades": self.max_daily_trades,
            "max_open_positions": self.max_open_positions,
            "max_exposure_percentage": self.max_exposure_percentage
        }
    
    def should_close_position(self, position, current_price):
        """
        Check if a position should be closed based on risk management rules
        
        Args:
            position (dict): The position to check
            current_price (float): Current price
            
        Returns:
            tuple: (should_close, reason)
        """
        entry_price = position.get("entry_price", 0)
        position_type = position.get("type", "")
        
        # Can't make a decision without price
        if entry_price <= 0 or current_price <= 0:
            return False, "Invalid prices"
        
        # Calculate profit/loss percentage
        if position_type == "buy":
            pnl_percentage = ((current_price - entry_price) / entry_price) * 100
        elif position_type == "sell":
            pnl_percentage = ((entry_price - current_price) / entry_price) * 100
        else:
            return False, "Unknown position type"
        
        # Check stop loss
        if pnl_percentage <= -self.stop_loss_percentage:
            return True, f"Stop loss triggered: {pnl_percentage:.2f}%"
        
        # Check take profit
        if pnl_percentage >= self.take_profit_percentage:
            return True, f"Take profit triggered: {pnl_percentage:.2f}%"
        
        return False, "No exit criteria met"
