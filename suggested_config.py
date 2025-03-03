import json
from pathlib import Path
import os

def update_config_with_pi():
    """Update the configuration file with PI/USDT trading pair"""
    config_path = Path("config.json")
    
    if not config_path.exists():
        print("Config file not found. Please run setup.py first.")
        return False
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Update with PI/USDT pair
    config["trading"]["base_symbol"] = "PI"
    config["trading"]["quote_symbol"] = "USDT"
    
    # Set reasonable trading parameters for PI
    config["trading"]["trade_amount"] = 10  # Amount in USDT
    config["trading"]["max_position_size"] = 50  # Maximum PI to hold
    
    # Configure strategy parameters more suitable for PI
    if config["strategies"]["active_strategy"] == "rsi_strategy":
        config["strategies"]["rsi_strategy"]["timeframe"] = "15m"  # Slightly longer timeframe
    
    # Save the updated configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration updated for PI/USDT trading!")
    return True

if __name__ == "__main__":
    update_config_with_pi()
    print("Run 'python cli.py' to start trading PI/USDT")
