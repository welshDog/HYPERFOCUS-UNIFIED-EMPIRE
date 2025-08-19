"""
Complete installer script for BROski Bot.
This script will:
1. Set up required directories
2. Install all dependencies
3. Create necessary configuration files
4. Test the installation
"""

import os
import sys
import subprocess
import json
import time
import platform
from pathlib import Path

# ANSI colors for better output formatting
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== {text} ==={Colors.END}\n")

def print_step(step_number, text):
    """Print a step with number"""
    print(f"{Colors.BOLD}Step {step_number}: {text}{Colors.END}")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def run_command(command, description=None):
    """Run a command and display output"""
    if description:
        print(f"{description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {e}")
        print(e.stderr)
        return False, e.stderr

def ensure_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print_success(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def create_default_config():
    """Create a default configuration file"""
    config = {
        "exchange": {
            "name": "mexc",
            "api_key": "",
            "api_secret": ""
        },
        "trading": {
            "base_symbol": "BTC",
            "quote_symbol": "USDT",
            "auto_trade": False,
            "trade_amount_usdt": 10.0,
            "max_open_trades": 1
        },
        "strategies": {
            "active_strategy": "rsi",
            "rsi": {
                "enabled": True,
                "period": 14,
                "overbought": 70,
                "oversold": 30,
                "timeframe": "1h"
            },
            "macd": {
                "enabled": False,
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9,
                "timeframe": "1h"
            },
            "hyperfocus": {
                "enabled": False,
                "rsi_period": 14,
                "volume_threshold": 1.5,
                "timeframes": ["15m", "1h", "4h"]
            }
        },
        "system": {
            "log_level": "INFO",
            "update_interval": 60,
            "data_retention_days": 30,
            "timezone": "UTC"
        }
    }
    
    # Create config.example.json
    with open('config.example.json', 'w') as f:
        json.dump(config, f, indent=2)
    print_success("Created config.example.json template")
    
    # Create config.json if it doesn't exist
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print_success("Created initial config.json")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python version {sys.version.split()[0]} is compatible")
        return True
    else:
        print_error(f"Python version {sys.version.split()[0]} is not compatible. Please use Python 3.8+")
        return False

def install_dependencies():
    """Install all required dependencies"""
    # Core dependencies for trading and data processing
    core_deps = [
        "ccxt",         # Cryptocurrency exchange API
        "pandas",       # Data analysis library
        "numpy",        # Numerical computing library
        "matplotlib",   # Plotting library
        "colorama",     # Terminal colors
        "requests",     # HTTP library
    ]
    
    # Optional dependencies for advanced features
    optional_deps = [
        "scikit-learn", # Machine learning library
        "ta",           # Technical analysis library
    ]
    
    # Install core dependencies
    print_step(2, "Installing core dependencies")
    success, _ = run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    if success:
        success, _ = run_command(
            f"{sys.executable} -m pip install {' '.join(core_deps)}",
            "Installing core packages"
        )
        if success:
            print_success("Core dependencies installed successfully")
        
    # Ask about optional dependencies
    print("\nDo you want to install optional dependencies?")
    print("These provide additional functionality but are not required:")
    for dep in optional_deps:
        print(f"- {dep}")
    
    install_optional = input("Install optional dependencies? (y/n): ").lower() == 'y'
    
    if install_optional:
        success, _ = run_command(
            f"{sys.executable} -m pip install {' '.join(optional_deps)}",
            "Installing optional packages"
        )
        if success:
            print_success("Optional dependencies installed successfully")

def test_installation():
    """Test critical components of the installation"""
    print_step(4, "Testing installation")
    
    # Test importing core packages
    try:
        import pandas
        import ccxt
        import matplotlib
        print_success("Core packages imported successfully")
    except ImportError as e:
        print_error(f"Failed importing packages: {str(e)}")
        return False
    
    # Test MEXC API connection
    try:
        import ccxt
        print("Testing MEXC API (public endpoints only)...")
        mexc = ccxt.mexc()
        tickers = mexc.fetch_tickers(['BTC/USDT'])
        print_success("Successfully connected to MEXC exchange API")
    except Exception as e:
        print_warning(f"Could not connect to MEXC: {str(e)}")
        print("This is not critical but you'll need to configure your API keys later.")
    
    # Test directories
    if (os.path.exists('config.json') and 
        os.path.exists('logs') and 
        os.path.exists('data') and
        os.path.exists('backups')):
        print_success("All required directories are present")
    else:
        print_warning("Some directories may be missing")
    
    return True

def main():
    """Main installation function"""
    print_header("BROski Bot Installation")
    print("This script will install all dependencies and set up BROski Bot")
    
    # Check Python version
    if not check_python_version():
        print_error("Installation cannot continue with incompatible Python version")
        sys.exit(1)
    
    # Create directories
    print_step(1, "Creating required directories")
    ensure_directory("logs")
    ensure_directory("data")
    ensure_directory("backups")
    ensure_directory("strategies")
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration files
    print_step(3, "Creating configuration files")
    create_default_config()
    
    # Test installation
    test_installation()
    
    # Final instructions
    print_header("Installation Complete")
    print("BROski Bot has been successfully installed!")
    print("\nTo start the bot control center, run:")
    print(f"{Colors.BOLD}python BROski_Control_Center.py{Colors.END}")
    print("\nAdditional steps:")
    print("1. Update your API keys in the config.json file")
    print("2. Adjust trading parameters in the configuration tab")
    print("3. Start with monitoring mode before enabling auto-trading")
    
    print("\nThank you for installing BROski Bot!")

if __name__ == "__main__":
    main()
