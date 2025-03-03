import os
import json
import sys
import platform
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init()

def check_python_version():
    """Check Python version compatibility with TensorFlow"""
    version = platform.python_version().split('.')
    major, minor = int(version[0]), int(version[1])
    
    print(f"Detected Python version: {major}.{minor}")
    
    if (major == 3 and 7 <= minor <= 11):
        print(f"{Fore.GREEN}✓ Python version {major}.{minor} is compatible with TensorFlow{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ Python version {major}.{minor} is NOT compatible with TensorFlow{Style.RESET_ALL}")
        print("TensorFlow requires Python 3.7-3.11")
        return False

def check_system_compatibility():
    """Check system compatibility with TensorFlow"""
    system = platform.system()
    machine = platform.machine()
    
    print(f"System detected: {system} on {machine} architecture")
    
    if system == "Windows" and "64" not in machine:
        print(f"{Fore.RED}✗ TensorFlow requires 64-bit Windows{Style.RESET_ALL}")
        return False
    
    if "arm" in machine.lower() or "aarch" in machine.lower():
        print(f"{Fore.YELLOW}⚠ ARM architecture detected - TensorFlow has limited ARM support{Style.RESET_ALL}")
        return False
        
    return True

def update_config_to_rsi():
    """Update configuration to use RSI strategy instead of ML"""
    config_path = Path("config.json")
    
    if not config_path.exists():
        print(f"{Fore.RED}Configuration file not found!{Style.RESET_ALL}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check if ML strategy is active
        current_strategy = config["strategies"]["active_strategy"]
        
        if current_strategy == "ml_strategy":
            print(f"Current strategy: {Fore.YELLOW}{current_strategy}{Style.RESET_ALL}")
            print(f"Switching to {Fore.GREEN}rsi_strategy{Style.RESET_ALL} (doesn't require TensorFlow)")
            
            # Switch to RSI strategy
            config["strategies"]["active_strategy"] = "rsi_strategy"
            config["strategies"]["rsi_strategy"]["enabled"] = True
            config["strategies"]["ml_strategy"]["enabled"] = False
            
            # Save updated configuration
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            print(f"{Fore.GREEN}✓ Configuration updated to use RSI strategy{Style.RESET_ALL}")
            return True
        else:
            print(f"Current strategy: {Fore.GREEN}{current_strategy}{Style.RESET_ALL}")
            print("No changes needed - you're already using a strategy that doesn't require TensorFlow")
            return True
            
    except Exception as e:
        print(f"{Fore.RED}Error updating configuration: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function"""
    print(f"{Fore.CYAN}=" * 60)
    print("BROski Bot - TensorFlow Alternative Setup".center(60))
    print("=" * 60 + Style.RESET_ALL)
    
    print("\nSince TensorFlow installation failed, we'll configure your bot to use")
    print("traditional technical indicators (RSI/MACD) instead of ML.\n")
    
    print(f"{Fore.YELLOW}Checking your system compatibility for future reference:{Style.RESET_ALL}")
    python_ok = check_python_version()
    system_ok = check_system_compatibility()
    
    if not python_ok or not system_ok:
        print("\nYour system may not be compatible with TensorFlow.")
        print("This is fine - BROski works great with traditional strategies too!")
    
    print(f"\n{Fore.CYAN}Updating your configuration to use RSI strategy instead...{Style.RESET_ALL}")
    update_config_to_rsi()
    
    print(f"\n{Fore.GREEN}Setup complete! You can now run BROski without TensorFlow.{Style.RESET_ALL}")
    print("\nTo start the bot, run:")
    print(f"{Fore.CYAN}python cli.py{Style.RESET_ALL}")
    
    print("\nNext steps:")
    print("1. Select option to check your balance")
    print("2. Update trading settings if needed")
    print("3. Start the trading bot")
    
    print(f"\n{Fore.YELLOW}Note: The bot will use the RSI strategy which works very well for trading{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}cryptocurrency and doesn't require any ML libraries.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
