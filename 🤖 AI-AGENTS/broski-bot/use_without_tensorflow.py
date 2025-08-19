import os
import json
import sys
from pathlib import Path
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BROski-Setup")

def update_config_strategy():
    """Update the configuration to use non-ML strategy"""
    config_path = Path("config.json")
    
    if not config_path.exists():
        # Try to create from example if it doesn't exist
        example_config_path = Path("config.example.json")
        if example_config_path.exists():
            shutil.copy(example_config_path, config_path)
            logger.info("Created config.json from example")
        else:
            logger.error("No configuration file found")
            return False
    
    # Load the configuration
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Check if ML strategy is active
        if config["strategies"]["active_strategy"] == "ml_strategy":
            logger.info("Switching from ML strategy to RSI strategy")
            
            # Change to RSI strategy
            config["strategies"]["active_strategy"] = "rsi_strategy"
            config["strategies"]["rsi_strategy"]["enabled"] = True
            config["strategies"]["ml_strategy"]["enabled"] = False
            
            # Save the updated configuration
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            logger.info("Configuration updated successfully")
        else:
            logger.info(f"Already using non-ML strategy: {config['strategies']['active_strategy']}")
            
        return True
        
    except Exception as e:
        logger.error(f"Error updating configuration: {e}")
        return False

def check_dependencies():
    """Check which dependencies are installed"""
    dependencies = {
        "ccxt": False,
        "pandas": False,
        "numpy": False,
        "matplotlib": False,
        "colorama": False,
        "requests": False,
    }
    
    for package in dependencies:
        try:
            __import__(package)
            dependencies[package] = True
        except ImportError:
            pass
    
    return dependencies

def install_core_dependencies():
    """Install core dependencies without TensorFlow"""
    try:
        import subprocess
        
        logger.info("Installing core dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ccxt", "pandas", "numpy", "matplotlib", "colorama", "requests"])
        logger.info("Core dependencies installed successfully")
        return True
    except Exception as e:
        logger.error(f"Error installing core dependencies: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("BROski Bot Setup - Non-TensorFlow Mode".center(60))
    print("=" * 60 + "\n")
    
    print("This will configure BROski to run without TensorFlow/ML features.")
    
    # Check dependencies
    deps = check_dependencies()
    missing = [pkg for pkg, installed in deps.items() if not installed]
    
    if missing:
        print("\nMissing dependencies:", ", ".join(missing))
        install = input("Install missing dependencies now? (y/n): ").lower() == 'y'
        
        if install:
            install_core_dependencies()
    
    # Update strategy configuration
    print("\nUpdating configuration to use RSI strategy instead of ML...")
    update_config_strategy()
    
    print("\n" + "=" * 60)
    print("Setup Complete!".center(60))
    print("=" * 60)
    print("\nYour BROski bot is now configured to use RSI strategy.")
    print("You can run it with: python cli.py")
    
    print("\nAvailable strategies:")
    print("1. RSI Strategy - Relative Strength Index (default)")
    print("2. MACD Strategy - Moving Average Convergence Divergence")
    print("\nTo switch between strategies, use the setup wizard: python wizard.py")

if __name__ == "__main__":
    main()
