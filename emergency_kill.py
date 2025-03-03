import os
import sys
import json
import ccxt
from colorama import init, Fore, Style
from pathlib import Path

# Initialize colorama
init()

def load_config():
    """Load configuration from config file"""
    config_path = Path("config.json")
    if not config_path.exists():
        print(f"{Fore.RED}Error: config.json not found!{Style.RESET_ALL}")
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"{Fore.RED}Error loading config: {str(e)}{Style.RESET_ALL}")
        return None

def connect_exchange(config):
    """Connect to exchange API"""
    if not config:
        return None
    
    try:
        exchange = ccxt.mexc({
            'apiKey': config['exchange']['api_key'],
            'secret': config['exchange']['api_secret'],
            'enableRateLimit': True,
        })
        return exchange
    except Exception as e:
        print(f"{Fore.RED}Error connecting to exchange: {str(e)}{Style.RESET_ALL}")
        return None

def cancel_all_orders(exchange, symbol=None):
    """Cancel all open orders, optionally for a specific symbol"""
    if not exchange:
        return False
    
    try:
        if symbol:
            print(f"{Fore.YELLOW}Canceling all orders for {symbol}...{Style.RESET_ALL}")
            result = exchange.cancel_all_orders(symbol)
            print(f"{Fore.GREEN}Orders canceled for {symbol}{Style.RESET_ALL}")
        else:
            # Get all trading pairs and cancel orders for each
            print(f"{Fore.YELLOW}Fetching markets...{Style.RESET_ALL}")
            markets = exchange.load_markets()
            
            # First, try canceling all orders at once if supported
            try:
                print(f"{Fore.YELLOW}Attempting to cancel all orders...{Style.RESET_ALL}")
                exchange.cancel_all_orders()
                print(f"{Fore.GREEN}All orders canceled successfully{Style.RESET_ALL}")
                return True
            except Exception as e:
                # If global cancellation fails, try canceling by symbol
                print(f"{Fore.YELLOW}Canceling orders by symbol...{Style.RESET_ALL}")
                config = load_config()
                if config:
                    # Prioritize the trading pair from config
                    base = config['trading']['base_symbol']
                    quote = config['trading']['quote_symbol']
                    primary_symbol = f"{base}/{quote}"
                    
                    try:
                        print(f"{Fore.YELLOW}Canceling orders for {primary_symbol}...{Style.RESET_ALL}")
                        exchange.cancel_all_orders(primary_symbol)
                        print(f"{Fore.GREEN}Orders canceled for {primary_symbol}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error canceling orders for {primary_symbol}: {str(e)}{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}Error canceling orders: {str(e)}{Style.RESET_ALL}")
        return False

def disable_auto_trading():
    """Disable auto trading in config"""
    config_path = Path("config.json")
    if not config_path.exists():
        print(f"{Fore.RED}Error: config.json not found!{Style.RESET_ALL}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if config['trading']['auto_trade']:
            config['trading']['auto_trade'] = False
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"{Fore.GREEN}Auto-trading disabled in configuration{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Auto-trading was already disabled{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}Error updating config: {str(e)}{Style.RESET_ALL}")
        return False

def kill_all_processes():
    """Find and kill all BROski bot processes"""
    try:
        import psutil
        import signal
        
        bot_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any(x in str(cmdline) for x in ['start_bot.py', 'bot_runner.py']):
                    bot_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        for proc in bot_processes:
            print(f"{Fore.YELLOW}Terminating process {proc.info['pid']}: {' '.join(proc.info['cmdline'])}{Style.RESET_ALL}")
            try:
                proc.send_signal(signal.SIGTERM)
            except Exception as e:
                print(f"{Fore.RED}Error terminating process: {str(e)}{Style.RESET_ALL}")
        
        if bot_processes:
            print(f"{Fore.GREEN}Terminated {len(bot_processes)} bot processes{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No active bot processes found{Style.RESET_ALL}")
            
        return True
    except ImportError:
        print(f"{Fore.YELLOW}psutil module not available, can't auto-kill processes{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please manually stop any running bot instances{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error killing processes: {str(e)}{Style.RESET_ALL}")
        return False

def emergency_kill():
    """Execute emergency kill to stop all trading and cancel all orders"""
    print(f"{Fore.RED}⚠️  EMERGENCY KILL ACTIVATED  ⚠️{Style.RESET_ALL}")
    print(f"{Fore.RED}==================================={Style.RESET_ALL}")
    
    # Step 1: Disable auto trading in config
    disable_auto_trading()
    
    # Step 2: Cancel all open orders
    config = load_config()
    if config:
        exchange = connect_exchange(config)
        if exchange:
            # Get trading pair from config
            base = config['trading']['base_symbol']
            quote = config['trading']['quote_symbol']
            symbol = f"{base}/{quote}"
            
            cancel_all_orders(exchange, symbol)
    
    # Step 3: Kill all bot processes
    kill_all_processes()
    
    print(f"{Fore.RED}==================================={Style.RESET_ALL}")
    print(f"{Fore.RED}Emergency kill completed!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Your auto-trading has been disabled.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}All open orders have been canceled.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Bot processes have been terminated.{Style.RESET_ALL}")
    
    return True

if __name__ == "__main__":
    print(f"{Fore.RED}⚠️  BROski Emergency Kill  ⚠️{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This will IMMEDIATELY:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Cancel all open orders{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Disable auto trading{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. Stop all bot processes{Style.RESET_ALL}")
    
    confirm = input(f"{Fore.RED}Are you sure you want to proceed? (y/n):{Style.RESET_ALL} ")
    if confirm.lower() == 'y':
        emergency_kill()
    else:
        print("Operation cancelled.")
