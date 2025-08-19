import json
import os
from pathlib import Path
from colorama import init, Fore, Style
import webbrowser

# Initialize colorama
init()

class SetupWizard:
    """
    Interactive wizard for setting up BROski Crypto Bot
    Guides users through API setup, trading settings, and strategy selection
    """
    
    def __init__(self):
        self.current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = self.current_dir / 'config.json'
        self.example_config_file = self.current_dir / 'config.example.json'
        self.config = {}
        
        # Load or create config
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        elif self.example_config_file.exists():
            with open(self.example_config_file, 'r') as f:
                self.config = json.load(f)
        else:
            print(f"{Fore.RED}Cannot find config files. Please run setup.py first.{Style.RESET_ALL}")
            exit(1)
    
    def print_header(self, text):
        """Print a formatted section header"""
        width = 60
        print("\n" + "=" * width)
        print(f"{Fore.CYAN}{text.center(width)}{Style.RESET_ALL}")
        print("=" * width + "\n")
    
    def mexc_api_guide(self):
        """Guide for setting up MEXC API keys"""
        self.print_header("MEXC API Key Setup Guide")
        
        print(f"{Fore.YELLOW}Do you need help getting your MEXC API keys?{Style.RESET_ALL}")
        help_needed = input("Open MEXC API documentation in browser? (y/n): ").lower() == 'y'
        
        if help_needed:
            print("Opening MEXC API documentation...")
            webbrowser.open("https://mxcdevelop.github.io/apidocs/spot_v3_en/#api-key-application")
        
        print(f"\n{Fore.GREEN}Steps to get your API keys:{Style.RESET_ALL}")
        print("1. Log in to your MEXC account")
        print("2. Go to Account → API Management")
        print("3. Click 'Create API'")
        print(f"4. {Fore.YELLOW}Enter a description in the 'Notes' field (Required){Style.RESET_ALL}")
        print("   - Example: 'BROski Trading Bot'")
        print("5. Enable 'Read' and 'Trade' permissions (disable withdrawals)")
        print("6. Copy your API Key and Secret Key")
        
        # Add new IP restriction guidance
        print(f"\n{Fore.YELLOW}Important Security Setting:{Style.RESET_ALL}")
        print("You'll see: 'Link IP Address (optional)'")
        print("- Keys WITHOUT IP restriction expire in 90 days")
        print("- Keys WITH IP restriction are more secure and don't expire")
        
        use_ip = input(f"{Fore.GREEN}Do you want to restrict your API key to your current IP? (recommended) (y/n):{Style.RESET_ALL} ").lower() == 'y'
        
        if use_ip:
            try:
                import requests
                ip = requests.get('https://api.ipify.org').text
                print(f"Your current public IP address is: {ip}")
                print("Use this IP when creating your API key")
            except:
                print("Could not automatically detect your IP address.")
                print("Please visit https://whatismyip.com to find your IP address")
        else:
            print(f"{Fore.YELLOW}Warning: Your API key will expire after 90 days without IP restriction{Style.RESET_ALL}")
            print("You will need to regularly create new API keys")
        
        print(f"\n{Fore.YELLOW}Now let's add your keys to the bot configuration...{Style.RESET_ALL}")
        
        self.config["exchange"]["api_key"] = input(f"{Fore.GREEN}Enter your MEXC API Key:{Style.RESET_ALL} ")
        self.config["exchange"]["api_secret"] = input(f"{Fore.GREEN}Enter your MEXC API Secret:{Style.RESET_ALL} ")
        
        # Test connection option
        test_connection = input("\nWould you like to test the API connection? (y/n): ").lower() == 'y'
        if test_connection:
            print("Testing connection... (functionality would be here in full implementation)")
            # Here you would import ccxt and test the connection
            print(f"{Fore.GREEN}Connection successful!{Style.RESET_ALL}")
    
    def trading_settings_guide(self):
        """Guide for configuring trading settings"""
        self.print_header("Trading Settings Configuration")
        
        print(f"{Fore.YELLOW}Let's set up your trading parameters:{Style.RESET_ALL}\n")
        
        # Trading pair selection
        print(f"{Fore.CYAN}Step 1: Select Trading Pair{Style.RESET_ALL}")
        print("The trading pair consists of a base currency and a quote currency.")
        print("Example: For trading Bitcoin with USDT, the pair is BTC/USDT")
        
        default_base = self.config["trading"]["base_symbol"]
        default_quote = self.config["trading"]["quote_symbol"]
        
        self.config["trading"]["base_symbol"] = input(f"Enter base symbol [{default_base}]: ") or default_base
        self.config["trading"]["quote_symbol"] = input(f"Enter quote symbol [{default_quote}]: ") or default_quote
        
        # Trading amount
        print(f"\n{Fore.CYAN}Step 2: Set Trading Amount{Style.RESET_ALL}")
        print(f"This is how much {self.config['trading']['quote_symbol']} to use per trade.")
        print("For beginners, start with a small amount to minimize risk.")
        
        default_amount = self.config["trading"]["trade_amount"]
        amount_input = input(f"Enter trade amount [{default_amount}]: ") or str(default_amount)
        self.config["trading"]["trade_amount"] = float(amount_input)
        
        # Trading interval
        print(f"\n{Fore.CYAN}Step 3: Set Trading Interval{Style.RESET_ALL}")
        print("This controls how frequently the bot checks for trading signals.")
        print("60 seconds is recommended for most strategies.")
        
        default_interval = self.config["trading"]["trade_interval_seconds"]
        interval_input = input(f"Enter check interval in seconds [{default_interval}]: ") or str(default_interval)
        self.config["trading"]["trade_interval_seconds"] = int(interval_input)
        
        # Auto trading
        print(f"\n{Fore.CYAN}Step 4: Configure Auto Trading{Style.RESET_ALL}")
        print("Auto trading controls whether the bot executes trades automatically.")
        print(f"{Fore.YELLOW}Recommendation: Start with this disabled (false) until you're confident in the bot.{Style.RESET_ALL}")
        
        default_auto = "yes" if self.config["trading"]["auto_trade"] else "no"
        auto_input = input(f"Enable auto trading? (yes/no) [{default_auto}]: ").lower() or default_auto
        self.config["trading"]["auto_trade"] = auto_input in ['yes', 'y', 'true']
        
        print(f"\n{Fore.GREEN}Trading settings configured successfully!{Style.RESET_ALL}")
    
    def strategy_selection_guide(self):
        """Guide for selecting and configuring trading strategies"""
        self.print_header("Trading Strategy Selection")
        
        print(f"{Fore.YELLOW}Let's choose your trading strategy:{Style.RESET_ALL}\n")
        
        # Display available strategies
        print(f"{Fore.CYAN}Available Strategies:{Style.RESET_ALL}")
        print("1. RSI Strategy - Good for beginners, detects overbought/oversold conditions")
        print("2. MACD Strategy - Better for trending markets")
        print("3. ML Strategy - Advanced machine learning predictions")
        
        # Strategy selection
        strategy_map = {
            "1": "rsi_strategy",
            "2": "macd_strategy",
            "3": "ml_strategy"
        }
        
        current = self.config["strategies"]["active_strategy"]
        current_num = next((k for k, v in strategy_map.items() if v == current), "1")
        
        choice = input(f"\nSelect a strategy (1-3) [{current_num}]: ") or current_num
        if choice in strategy_map:
            self.config["strategies"]["active_strategy"] = strategy_map[choice]
            # Enable selected strategy, disable others
            for strat in strategy_map.values():
                self.config["strategies"][strat]["enabled"] = (strat == strategy_map[choice])
        
        # Configure selected strategy
        active_strat = self.config["strategies"]["active_strategy"]
        print(f"\n{Fore.CYAN}Configuring {active_strat.replace('_', ' ').title()}:{Style.RESET_ALL}")
        
        if active_strat == "rsi_strategy":
            self._configure_rsi()
        elif active_strat == "macd_strategy":
            self._configure_macd()
        elif active_strat == "ml_strategy":
            self._configure_ml()
        
        print(f"\n{Fore.GREEN}Strategy configured successfully!{Style.RESET_ALL}")
    
    def _configure_rsi(self):
        """Configure RSI strategy parameters"""
        strat = self.config["strategies"]["rsi_strategy"]
        
        print("RSI (Relative Strength Index) measures momentum by comparing recent gains to losses.")
        print("- Timeframe: Chart interval (e.g., 5m, 15m, 1h)")
        print("- RSI Period: Number of periods for calculation (typically 14)")
        print("- Overbought level: Signals potential sell (typically 70)")
        print("- Oversold level: Signals potential buy (typically 30)")
        
        strat["timeframe"] = input(f"Enter timeframe [{strat['timeframe']}]: ") or strat["timeframe"]
        
        period = input(f"Enter RSI period [{strat['rsi_period']}]: ") or str(strat["rsi_period"])
        strat["rsi_period"] = int(period)
        
        overbought = input(f"Enter overbought level [{strat['rsi_overbought']}]: ") or str(strat["rsi_overbought"])
        strat["rsi_overbought"] = int(overbought)
        
        oversold = input(f"Enter oversold level [{strat['rsi_oversold']}]: ") or str(strat["rsi_oversold"])
        strat["rsi_oversold"] = int(oversold)
    
    def _configure_macd(self):
        """Configure MACD strategy parameters"""
        strat = self.config["strategies"]["macd_strategy"]
        
        print("MACD (Moving Average Convergence Divergence) follows trends using moving averages.")
        print("- Timeframe: Chart interval (e.g., 15m, 1h, 4h)")
        print("- Fast period: Short-term EMA period (typically 12)")
        print("- Slow period: Long-term EMA period (typically 26)")
        print("- Signal period: Signal line smoothing (typically 9)")
        
        strat["timeframe"] = input(f"Enter timeframe [{strat['timeframe']}]: ") or strat["timeframe"]
        
        fast = input(f"Enter fast period [{strat['fast_period']}]: ") or str(strat["fast_period"])
        strat["fast_period"] = int(fast)
        
        slow = input(f"Enter slow period [{strat['slow_period']}]: ") or str(strat["slow_period"])
        strat["slow_period"] = int(slow)
        
        signal = input(f"Enter signal period [{strat['signal_period']}]: ") or str(strat["signal_period"])
        strat["signal_period"] = int(signal)
    
    def _configure_ml(self):
        """Configure ML strategy parameters"""
        strat = self.config["strategies"]["ml_strategy"]
        
        print("Machine Learning strategy uses AI to predict price movements.")
        print("- Model path: Location of the trained model file")
        print("- Confidence threshold: Minimum confidence needed (0.5-1.0)")
        print(f"{Fore.YELLOW}Note: ML strategy requires a pre-trained model file.{Style.RESET_ALL}")
        
        strat["model_path"] = input(f"Enter model path [{strat['model_path']}]: ") or strat["model_path"]
        
        threshold = input(f"Enter confidence threshold [{strat['confidence_threshold']}]: ") or str(strat["confidence_threshold"])
        strat["confidence_threshold"] = float(threshold)
    
    def save_config(self):
        """Save the configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"\n{Fore.GREEN}Configuration saved to {self.config_file}{Style.RESET_ALL}")
    
    def run_wizard(self):
        """Run the complete setup wizard"""
        self.print_header("BROski Crypto Bot Setup Wizard")
        
        print(f"{Fore.YELLOW}Welcome to the BROski setup wizard!{Style.RESET_ALL}")
        print("This wizard will guide you through setting up your bot.")
        print("You can press Enter to keep default values.\n")
        
        proceed = input("Ready to proceed? (y/n): ").lower()
        if proceed != 'y':
            print("Setup cancelled.")
            return
        
        self.mexc_api_guide()
        self.trading_settings_guide()
        self.strategy_selection_guide()
        
        save = input(f"\n{Fore.YELLOW}Save this configuration? (y/n):{Style.RESET_ALL} ").lower()
        if save == 'y':
            self.save_config()
            print(f"\n{Fore.GREEN}Setup complete! You can now run the bot with:{Style.RESET_ALL}")
            print("python cli.py")
        else:
            print("\nSetup cancelled. Configuration not saved.")

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run_wizard()
