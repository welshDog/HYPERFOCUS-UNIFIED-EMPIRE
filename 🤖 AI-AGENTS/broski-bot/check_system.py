import os
import sys
import json
import importlib
import platform
from pathlib import Path
import traceback
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

def print_header(text):
    """Print a colored header"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text.center(50)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def print_success(text):
    """Print a success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print an error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Fore.YELLOW}! {text}{Style.RESET_ALL}")

def print_info(text):
    """Print an info message"""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")

def check_python_version():
    """Check Python version"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version >= required_version:
        print_success(f"Python version: {platform.python_version()}")
        return True
    else:
        print_error(f"Python version: {platform.python_version()}. Required: 3.6+")
        return False

def check_required_packages():
    """Check required packages"""
    required_packages = ['ccxt', 'pandas', 'colorama', 'matplotlib']
    missing_packages = []
    
    print_info("Checking required packages:")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print_success(f"  {package} ✓")
        except ImportError:
            missing_packages.append(package)
            print_error(f"  {package} ✗")
    
    if missing_packages:
        print_error(f"\nMissing packages: {', '.join(missing_packages)}")
        print_info("Run: pip install " + " ".join(missing_packages))
        return False
    return True

def check_core_files():
    """Check core files exist"""
    required_files = [
        'start_bot.py',
        'direct_bot.py',
        'cli.py',
        'BROSKI_DASHBOARD.bat',
        'MONITOR_DIRECT.bat',
        'START_BOT.bat',
        'BACKUP_BOT.bat'
    ]
    
    missing_files = []
    
    print_info("Checking core files:")
    for filename in required_files:
        if os.path.exists(filename):
            print_success(f"  {filename} ✓")
        else:
            missing_files.append(filename)
            print_error(f"  {filename} ✗")
    
    if missing_files:
        print_error(f"\nMissing files: {', '.join(missing_files)}")
        return False
    return True

def check_config():
    """Check configuration file"""
    config_path = Path("config.json")
    example_path = Path("config.example.json")
    
    if not config_path.exists():
        if example_path.exists():
            print_warning("config.json not found, but example exists")
            print_info("Run setup.py to create configuration")
            return False
        else:
            print_error("Both config.json and config.example.json are missing!")
            return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for essential fields
        if not all(k in config for k in ["exchange", "trading", "strategies"]):
            print_error("config.json is missing essential sections")
            return False
            
        # Check API keys
        api_key = config["exchange"]["api_key"]
        api_secret = config["exchange"]["api_secret"]
        
        if api_key == "YOUR_MEXC_API_KEY_HERE" or not api_key:
            print_warning("API key not configured in config.json")
            print_info("Run setup.py to configure your API keys")
            return False
            
        if api_secret == "YOUR_MEXC_API_SECRET_HERE" or not api_secret:
            print_warning("API secret not configured in config.json")
            return False
        
        print_success("Configuration file (config.json) exists and contains API keys")
        
        # Check trading settings
        print_info("Trading configuration:")
        print_info(f"  Trading pair: {config['trading']['base_symbol']}/{config['trading']['quote_symbol']}")
        print_info(f"  Active strategy: {config['strategies']['active_strategy']}")
        if config['trading']['auto_trade']:
            print_warning("  Auto-trading is ENABLED")
        else:
            print_info("  Auto-trading is disabled (monitor mode)")
        
        return True
        
    except json.JSONDecodeError:
        print_error("config.json is not a valid JSON file")
        return False
    except Exception as e:
        print_error(f"Error checking config: {str(e)}")
        return False

def test_api_connection():
    """Test the API connection"""
    print_info("Testing API connection to MEXC...")
    
    try:
        import ccxt
        
        # Load config
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        # Initialize exchange
        exchange = ccxt.mexc({
            'apiKey': config['exchange']['api_key'],
            'secret': config['exchange']['api_secret'],
            'enableRateLimit': True,
        })
        
        # Test API connection by fetching ticker
        base = config['trading']['base_symbol']
        quote = config['trading']['quote_symbol']
        symbol = f"{base}/{quote}"
        
        try:
            ticker = exchange.fetch_ticker(symbol)
            print_success(f"API connection successful! Current {symbol} price: {ticker['last']}")
            return True
        except Exception as e:
            if "IP" in str(e) and "whitelist" in str(e).lower():
                print_error(f"IP whitelist error: Your current IP is not authorized")
                print_info("Run ip_whitelist_helper.py to fix this issue")
            else:
                print_error(f"Error fetching ticker: {str(e)}")
            return False
            
    except ImportError:
        print_error("ccxt package is not installed")
        return False
    except Exception as e:
        print_error(f"Error testing API: {str(e)}")
        return False

def check_directories():
    """Check required directories"""
    required_dirs = ['logs', 'strategies']
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print_warning(f"Directory '{dir_name}' does not exist, creating it...")
            try:
                os.makedirs(dir_name, exist_ok=True)
                print_success(f"Created '{dir_name}' directory")
            except Exception as e:
                print_error(f"Failed to create '{dir_name}' directory: {str(e)}")
                return False
        else:
            print_success(f"Directory '{dir_name}' exists")
    
    return True

def main():
    print_header("BROski Bot Health Check")
    
    # Track overall health status
    all_checks_passed = True
    
    # Check Python version
    print_header("System Check")
    if not check_python_version():
        all_checks_passed = False
    
    # Check required packages
    if not check_required_packages():
        all_checks_passed = False
    
    # Check core files 
    print_header("Files Check")
    if not check_core_files():
        all_checks_passed = False
    
    # Check directories
    if not check_directories():
        all_checks_passed = False
    
    # Check configuration
    print_header("Configuration Check")
    config_ok = check_config()
    if not config_ok:
        all_checks_passed = False
    
    # Test API connection only if config is OK
    if config_ok:
        print_header("API Connection Test")
        if not test_api_connection():
            all_checks_passed = False
    
    # Print final summary
    print_header("SUMMARY")
    if all_checks_passed:
        print_success("BROski Bot is READY TO RUN!")
        print_info("Start the bot with one of these commands:")
        print_info("  - START_BOT.bat           (Direct bot)")
        print_info("  - BROSKI_DASHBOARD.bat    (Dashboard interface)")
        print_info("  - python start_bot.py     (Command line)")
    else:
        print_error("BROski Bot needs some fixes before it can run properly.")
        print_info("Please address the issues mentioned above.")
    
    print("")
    return all_checks_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        print_error(traceback.format_exc())
        sys.exit(1)
