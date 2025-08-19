import os
import json
import logging
import sys
from colorama import init, Fore, Style
import ccxt
from pathlib import Path

# Initialize colorama
init()

# Create necessary directories
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/broski_cli.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("BROski-CLI")

class BroskiCLI:
    """Command Line Interface for BROski Crypto Bot"""
    
    def __init__(self):
        self.config_file = Path("config.json")
        if not self.config_file.exists():
            print(f"{Fore.RED}Error: config.json not found!{Style.RESET_ALL}")
            print(f"Please run {Fore.CYAN}python setup.py{Style.RESET_ALL} first to create your configuration.")
            sys.exit(1)
            
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
            
        # Initialize exchange connection
        self._setup_exchange()
        
    def _setup_exchange(self):
        """Setup the exchange connection"""
        try:
            self.exchange = ccxt.mexc({
                'apiKey': self.config['exchange']['api_key'],
                'secret': self.config['exchange']['api_secret'],
                'enableRateLimit': True,
            })
            logger.info("Exchange connection initialized")
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {str(e)}")
            self.exchange = None
    
    def check_balance(self):
        """Check account balance"""
        if not self.exchange:
            print(f"{Fore.RED}Error: Exchange connection not available{Style.RESET_ALL}")
            return
            
        try:
            print(f"{Fore.CYAN}Fetching balance from MEXC...{Style.RESET_ALL}")
            balance = self.exchange.fetch_balance()
            
            # Get base and quote currencies
            base = self.config["trading"]["base_symbol"]
            quote = self.config["trading"]["quote_symbol"]
            
            # Display balances
            print("\n=== Account Balance ===")
            
            # Show quote currency (usually USDT)
            quote_balance = balance.get('total', {}).get(quote, 0)
            print(f"{Fore.GREEN}{quote}{Style.RESET_ALL}: {quote_balance}")
            
            # Show base currency (e.g., PI)
            base_balance = balance.get('total', {}).get(base, 0)
            print(f"{Fore.GREEN}{base}{Style.RESET_ALL}: {base_balance}")
            
            # Show some other common currencies
            for currency in ['BTC', 'ETH', 'USDT']:
                if currency != quote and currency != base:
                    curr_balance = balance.get('total', {}).get(currency, 0)
                    if curr_balance > 0:
                        print(f"{currency}: {curr_balance}")
                        
        except Exception as e:
            logger.error(f"Error fetching balance: {str(e)}")
            error_msg = str(e)
            print(f"{Fore.RED}Failed to fetch balance: {str(e)}{Style.RESET_ALL}")
            
            # Check for IP whitelist error specifically
            if "IP" in error_msg and "white list" in error_msg:
                print(f"\n{Fore.YELLOW}This is an IP whitelist error. Your current IP is not authorized.{Style.RESET_ALL}")
                
                try:
                    # Extract IP from error message
                    import re
                    ip_match = re.search(r'IP \[([0-9\.]+)\]', error_msg)
                    current_ip = ip_match.group(1) if ip_match else "unknown"
                    
                    print(f"\n{Fore.CYAN}Your current IP address: {current_ip}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}To fix this issue, you need to add this IP to your MEXC API whitelist.{Style.RESET_ALL}")
                    print(f"\nWould you like to run the IP whitelist helper tool?")
                    
                    run_helper = input("Run IP whitelist helper? (y/n): ").lower() == 'y'
                    if run_helper:
                        import subprocess
                        subprocess.run([sys.executable, "ip_whitelist_helper.py"])
                except Exception as helper_error:
                    print(f"{Fore.RED}Error starting helper: {str(helper_error)}{Style.RESET_ALL}")
                    print(f"Please run 'python ip_whitelist_helper.py' manually to fix this issue.")
    
    def update_trading_settings(self):
        """Update trading settings"""
        print(f"\n{Fore.CYAN}Trading Settings{Style.RESET_ALL}\n")
        
        # Trading pair
        base = self.config["trading"]["base_symbol"]
        quote = self.config["trading"]["quote_symbol"]
        print(f"Current trading pair: {base}/{quote}")
        
        change_pair = input("Change trading pair? (y/n): ").lower() == 'y'
        if change_pair:
            print("\nPopular trading pairs on MEXC:")
            print("- BTC/USDT (Bitcoin)")
            print("- ETH/USDT (Ethereum)")
            print("- BNB/USDT (Binance Coin)")
            print("- DOGE/USDT (Dogecoin)")
            print("- SHIB/USDT (Shiba Inu)")
            print("- SOL/USDT (Solana)")
            
            base = input(f"Enter base symbol [{base}]: ") or base
            quote = input(f"Enter quote symbol [{quote}]: ") or quote
            self.config["trading"]["base_symbol"] = base
            self.config["trading"]["quote_symbol"] = quote
            print(f"Trading pair updated to {base}/{quote}")
            
            # Verify trading pair exists
            try:
                print(f"Verifying {base}/{quote} exists on MEXC...")
                symbol = f"{base}/{quote}"
                ticker = self.exchange.fetch_ticker(symbol)
                print(f"{Fore.GREEN}Trading pair verified! Current price: {ticker['last']}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Warning: Could not verify trading pair: {str(e)}{Style.RESET_ALL}")
                print(f"Please make sure {base}/{quote} exists on MEXC")
        
        # Trade amount
        amount = self.config["trading"]["trade_amount"]
        new_amount = input(f"Enter trade amount [{amount}]: ") or str(amount)
        try:
            self.config["trading"]["trade_amount"] = float(new_amount)
            print(f"Trade amount set to {new_amount}")
        except ValueError:
            print(f"{Fore.RED}Invalid amount. Keeping previous value: {amount}{Style.RESET_ALL}")
        
        # Auto trading
        auto_trade = "yes" if self.config["trading"]["auto_trade"] else "no"
        auto_input = input(f"Enable auto trading? (yes/no) [{auto_trade}]: ").lower() or auto_trade
        self.config["trading"]["auto_trade"] = auto_input in ["yes", "y", "true"]
        print(f"Auto trading {'enabled' if self.config['trading']['auto_trade'] else 'disabled'}")
        
        # Save changes
        save_changes = input("\nSave changes? (y/n): ").lower() == 'y'
        if save_changes:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"{Fore.GREEN}Trading settings saved!{Style.RESET_ALL}")
    
    def start_bot(self):
        """Start the trading bot"""
        print(f"\n{Fore.YELLOW}Starting BROski Crypto Bot...{Style.RESET_ALL}")
        
        try:
            from subprocess import Popen
            Popen(["python", "start_bot.py"])
            print(f"{Fore.GREEN}Bot started in background!{Style.RESET_ALL}")
            print("Check logs/broski_bot.log for activity")
            print(f"Use {Fore.CYAN}python cli.py{Style.RESET_ALL} to interact with the bot")
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            print(f"{Fore.RED}Failed to start bot: {str(e)}{Style.RESET_ALL}")
    
    def show_menu(self):
        """Show the main menu"""
        while True:
            print(f"\n{Fore.CYAN}======= BROski Crypto Bot CLI ======={Style.RESET_ALL}")
            print(f"1. Check Balance")
            print(f"2. Update Trading Settings")
            print(f"3. Start Trading Bot")
            print(f"4. Show Current Settings")
            print(f"{Fore.RED}5. EMERGENCY KILL - Cancel All Orders{Style.RESET_ALL}")
            print(f"6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.update_trading_settings()
            elif choice == '3':
                self.start_bot()
            elif choice == '4':
                self.show_settings()
            elif choice == '5':
                self.emergency_kill()
            elif choice == '6':
                print(f"\n{Fore.GREEN}Exiting BROski CLI. Happy trading!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1-6.{Style.RESET_ALL}")

    def emergency_kill(self):
        """Execute emergency kill to cancel all orders and stop bot"""
        print(f"\n{Fore.RED}⚠️  EMERGENCY KILL - Cancel All Orders  ⚠️{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}This will immediately:{Style.RESET_ALL}")
        print(f"• Cancel all open orders")
        print(f"• Disable auto-trading")
        print(f"• Stop all running bot processes")
        
        confirm = input(f"\n{Fore.RED}Are you sure you want to proceed? (y/n):{Style.RESET_ALL} ")
        if confirm.lower() == 'y':
            try:
                # Import and run the emergency kill function
                from emergency_kill import emergency_kill
                emergency_kill()
            except Exception as e:
                print(f"{Fore.RED}Error executing emergency kill: {str(e)}{Style.RESET_ALL}")
        else:
            print("Emergency kill aborted.")

    def show_settings(self):
        """Show current bot settings"""
        print(f"\n{Fore.CYAN}Current Bot Settings{Style.RESET_ALL}")
        
        # Exchange
        print(f"\n{Fore.YELLOW}Exchange:{Style.RESET_ALL} {self.config['exchange']['name']}")
        
        # Trading pair
        base = self.config["trading"]["base_symbol"]
        quote = self.config["trading"]["quote_symbol"]
        print(f"{Fore.YELLOW}Trading Pair:{Style.RESET_ALL} {base}/{quote}")
        
        # Trading settings
        print(f"{Fore.YELLOW}Trade Amount:{Style.RESET_ALL} {self.config['trading']['trade_amount']} {quote}")
        print(f"{Fore.YELLOW}Max Position Size:{Style.RESET_ALL} {self.config['trading']['max_position_size']} {base}")
        print(f"{Fore.YELLOW}Trading Interval:{Style.RESET_ALL} {self.config['trading']['trade_interval_seconds']} seconds")
        print(f"{Fore.YELLOW}Auto Trading:{Style.RESET_ALL} {'Enabled' if self.config['trading']['auto_trade'] else 'Disabled'}")
        
        # Active strategy
        active_strat = self.config["strategies"]["active_strategy"]
        print(f"{Fore.YELLOW}Active Strategy:{Style.RESET_ALL} {active_strat}")
        
        # Strategy details
        if active_strat == "rsi_strategy":
            strat = self.config["strategies"]["rsi_strategy"]
            print(f"  - Timeframe: {strat['timeframe']}")
            print(f"  - RSI Period: {strat['rsi_period']}")
            print(f"  - Overbought Level: {strat['rsi_overbought']}")
            print(f"  - Oversold Level: {strat['rsi_oversold']}")
        elif active_strat == "macd_strategy":
            strat = self.config["strategies"]["macd_strategy"]
            print(f"  - Timeframe: {strat['timeframe']}")
            print(f"  - Fast Period: {strat['fast_period']}")
            print(f"  - Slow Period: {strat['slow_period']}")
            print(f"  - Signal Period: {strat['signal_period']}")
        
        # Risk management
        risk = self.config["risk_management"]
        print(f"\n{Fore.YELLOW}Risk Management:{Style.RESET_ALL}")
        print(f"  - Stop Loss: {risk['stop_loss_percentage']}%")
        print(f"  - Take Profit: {risk['take_profit_percentage']}%")
        print(f"  - Max Daily Trades: {risk['max_daily_trades']}")
        print(f"  - Max Open Positions: {risk['max_open_positions']}")
        
        # Notifications
        telegram = self.config["notifications"]["telegram"]
        print(f"\n{Fore.YELLOW}Telegram Notifications:{Style.RESET_ALL} {'Enabled' if telegram['enabled'] else 'Disabled'}")

if __name__ == "__main__":
    cli = BroskiCLI()
    cli.show_menu()
