import os
import time
import sys
import re
import json
from datetime import datetime
from colorama import init, Fore, Style, Back
from pathlib import Path

# Initialize colorama for colored text
init()

# Configuration
LOG_FILE = "logs/broski_bot.log"
LOG_FILE_TRADING = "logs/trading_bot.log"
REFRESH_RATE = 2  # seconds

class BotMonitor:
    """Simple real-time monitor for BROski Bot activity"""
    
    def __init__(self):
        self.last_position = 0
        self.last_trading_position = 0
        self.show_timestamp = True
        self.filter_keyword = None
        self.auto_scroll = True
        self.strategy_view = False  # New flag to show strategy info panel
        self.performance_view = False  # New flag for performance metrics panel
        self.current_strategy = "Loading..."  # Will be updated from logs
        self.strategy_metrics = {}  # Store HyperFocus metrics
        self.hyperfocus_enabled = False  # Track if HyperFocus is active
        
        # Trade performance tracking
        self.trades = []
        self.trade_stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'total_profit_loss': 0.0,
            'total_profit_loss_percent': 0.0,
            'average_win': 0.0,
            'average_loss': 0.0,
            'largest_win': 0.0,
            'largest_loss': 0.0,
            'strategy_performance': {}
        }
        self.open_positions = []
        
        self.show_help()
    
    def show_help(self):
        """Show help text"""
        print(f"{Fore.CYAN}BROski Bot Monitor{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}=" * 60)
        print(f"Interactive commands (type while monitoring):")
        print(f"  {Fore.GREEN}t{Style.RESET_ALL} - Toggle timestamps")
        print(f"  {Fore.GREEN}f <keyword>{Style.RESET_ALL} - Filter logs (e.g., 'f RSI' or 'f price')")
        print(f"  {Fore.GREEN}c{Style.RESET_ALL} - Clear filter")
        print(f"  {Fore.GREEN}s{Style.RESET_ALL} - Toggle auto-scroll")
        print(f"  {Fore.GREEN}v{Style.RESET_ALL} - Toggle strategy view")
        print(f"  {Fore.GREEN}p{Style.RESET_ALL} - {Fore.GREEN}Show performance metrics{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}h{Style.RESET_ALL} - {Fore.CYAN}Enable HyperFocus mode{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}r{Style.RESET_ALL} - {Fore.CYAN}Enable RSI strategy{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}m{Style.RESET_ALL} - {Fore.CYAN}Enable MACD strategy{Style.RESET_ALL}")
        print(f"  {Fore.RED}k{Style.RESET_ALL} - {Fore.RED}EMERGENCY KILL BUTTON{Style.RESET_ALL} - Cancel all orders & stop bot")
        print(f"  {Fore.GREEN}?{Style.RESET_ALL} - Show this help")
        print(f"  {Fore.GREEN}q{Style.RESET_ALL} - Quit monitor")
        print(f"{Fore.YELLOW}=" * 60 + Style.RESET_ALL)
        print(f"Starting monitor... Press {Fore.GREEN}?{Style.RESET_ALL} anytime for help.\n")
    
    def get_new_log_content(self):
        """Get new content from the log file since last check"""
        if not os.path.exists(LOG_FILE):
            return []
            
        with open(LOG_FILE, 'r') as f:
            f.seek(self.last_position)
            new_content = f.readlines()
            self.last_position = f.tell()
            
        return new_content
    
    def get_new_trading_content(self):
        """Get new content from the trading log file since last check"""
        if not os.path.exists(LOG_FILE_TRADING):
            return []
            
        with open(LOG_FILE_TRADING, 'r') as f:
            f.seek(self.last_trading_position)
            new_content = f.readlines()
            self.last_trading_position = f.tell()
            
        return new_content
    
    def format_log_line(self, line):
        """Format a log line with colors based on content"""
        # Extract timestamp and message if present
        timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([A-Z]+) - (.+)$', line)
        
        if timestamp_match:
            timestamp, level, message = timestamp_match.groups()
            
            # Format based on log level
            if level == "INFO":
                level_colored = f"{Fore.GREEN}{level}{Style.RESET_ALL}"
            elif level == "WARNING":
                level_colored = f"{Fore.YELLOW}{level}{Style.RESET_ALL}"
            elif level == "ERROR":
                level_colored = f"{Fore.RED}{level}{Style.RESET_ALL}"
            elif level == "CRITICAL":
                level_colored = f"{Back.RED}{Fore.WHITE}{level}{Style.RESET_ALL}"
            else:
                level_colored = level
                
            # Highlight key phrases in the message
            if "BUY signal" in message:
                message = message.replace("BUY signal", f"{Fore.GREEN}BUY signal{Style.RESET_ALL}")
            elif "SELL signal" in message:
                message = message.replace("SELL signal", f"{Fore.RED}SELL signal{Style.RESET_ALL}")
            elif "price:" in message:
                price_match = re.search(r'price: (\d+\.\d+)', message)
                if price_match:
                    price = price_match.group(1)
                    message = message.replace(f"price: {price}", f"price: {Fore.CYAN}{price}{Style.RESET_ALL}")
            elif "Current RSI:" in message:
                rsi_match = re.search(r'Current RSI: (\d+\.\d+)', message)
                if rsi_match:
                    rsi = rsi_match.group(1)
                    message = message.replace(f"Current RSI: {rsi}", f"Current RSI: {Fore.MAGENTA}{rsi}{Style.RESET_ALL}")
            
            # Track executed trades for performance metrics
            if "Executed trade:" in message:
                self._parse_trade_info(message, timestamp)
            elif "Trade closed:" in message:
                self._parse_trade_close_info(message, timestamp)
            
            # Capture active strategy info
            if "Active strategy:" in message:
                strategy_match = re.search(r'Active strategy: (\w+)', message)
                if strategy_match:
                    self.current_strategy = strategy_match.group(1)
                    if "hyperfocus" in self.current_strategy.lower():
                        self.hyperfocus_enabled = True
                    else:
                        self.hyperfocus_enabled = False
            
            # Capture HyperFocus confirmations
            if "Confirmations:" in message and self.hyperfocus_enabled:
                conf_match = re.search(r'Confirmations: (\d+)/(\d+)', message)
                if conf_match:
                    confirmed, total = conf_match.groups()
                    self.strategy_metrics['confirmations'] = f"{confirmed}/{total}"
            
            # Format with or without timestamp
            if self.show_timestamp:
                return f"{Fore.BLUE}{timestamp}{Style.RESET_ALL} - {level_colored} - {message}"
            else:
                return f"{level_colored} - {message}"
        else:
            return line.rstrip()
    
    def _parse_trade_info(self, message, timestamp):
        """Parse trade information from log message"""
        try:
            # Example expected format: "Executed trade: BUY 10.5 PI at 1.9532 USDT (Total: 20.5086 USDT)"
            trade_match = re.search(r'Executed trade: (BUY|SELL) (\d+\.\d+) (\w+) at (\d+\.\d+) (\w+)', message)
            if trade_match:
                action, amount, base_currency, price, quote_currency = trade_match.groups()
                
                trade = {
                    'id': len(self.trades) + 1,
                    'action': action,
                    'amount': float(amount),
                    'base_currency': base_currency,
                    'price': float(price),
                    'quote_currency': quote_currency,
                    'timestamp': timestamp,
                    'total_value': float(amount) * float(price),
                    'strategy': self.current_strategy,
                    'status': 'open',
                    'close_price': None,
                    'profit_loss': None,
                    'profit_loss_percent': None
                }
                
                self.trades.append(trade)
                if action == 'BUY':
                    self.open_positions.append(trade)
                
                # Update total trades count
                self.trade_stats['total_trades'] = len(self.trades)
                
                # Update strategy-specific stats
                if trade['strategy'] not in self.trade_stats['strategy_performance']:
                    self.trade_stats['strategy_performance'][trade['strategy']] = {
                        'trades': 0, 'winning': 0, 'profit': 0.0
                    }
                self.trade_stats['strategy_performance'][trade['strategy']]['trades'] += 1
                
        except Exception as e:
            print(f"{Fore.YELLOW}Error parsing trade info: {str(e)}{Style.RESET_ALL}")
    
    def _parse_trade_close_info(self, message, timestamp):
        """Parse trade closing information"""
        try:
            # Example expected format: "Trade closed: SELL 10.5 PI at 2.0532 USDT (Profit: +0.1 USDT, +5.12%)"
            close_match = re.search(r'Trade closed: (BUY|SELL) (\d+\.\d+) (\w+) at (\d+\.\d+) (\w+) \(Profit: ([+-]\d+\.\d+) \w+, ([+-]\d+\.\d+)%\)', message)
            if close_match:
                action, amount, base_currency, price, quote_currency, profit, percent = close_match.groups()
                
                # Find the corresponding open position to close
                for pos in self.open_positions[:]:
                    if pos['base_currency'] == base_currency and pos['amount'] == float(amount) and pos['action'] != action:
                        # Mark this position as closed
                        pos['status'] = 'closed'
                        pos['close_price'] = float(price)
                        pos['profit_loss'] = float(profit)
                        pos['profit_loss_percent'] = float(percent)
                        
                        # Remove from open positions
                        self.open_positions.remove(pos)
                        
                        # Update overall stats
                        is_win = float(profit) > 0
                        if is_win:
                            self.trade_stats['winning_trades'] += 1
                            self.trade_stats['total_profit_loss'] += float(profit)
                            
                            # Update largest win if applicable
                            if float(profit) > self.trade_stats['largest_win']:
                                self.trade_stats['largest_win'] = float(profit)
                                
                            # Update strategy stats
                            if pos['strategy'] in self.trade_stats['strategy_performance']:
                                self.trade_stats['strategy_performance'][pos['strategy']]['winning'] += 1
                                self.trade_stats['strategy_performance'][pos['strategy']]['profit'] += float(profit)
                        else:
                            self.trade_stats['losing_trades'] += 1
                            self.trade_stats['total_profit_loss'] += float(profit)
                            
                            # Update largest loss if applicable
                            if float(profit) < self.trade_stats['largest_loss']:
                                self.trade_stats['largest_loss'] = float(profit)
                        
                        # Update win rate
                        total = self.trade_stats['winning_trades'] + self.trade_stats['losing_trades']
                        if total > 0:
                            self.trade_stats['win_rate'] = (self.trade_stats['winning_trades'] / total) * 100
                        
                        # Calculate average win/loss
                        if self.trade_stats['winning_trades'] > 0:
                            winning_trades = [t for t in self.trades if t['status'] == 'closed' and t['profit_loss'] > 0]
                            self.trade_stats['average_win'] = sum(t['profit_loss'] for t in winning_trades) / len(winning_trades)
                            
                        if self.trade_stats['losing_trades'] > 0:
                            losing_trades = [t for t in self.trades if t['status'] == 'closed' and t['profit_loss'] < 0]
                            self.trade_stats['average_loss'] = sum(t['profit_loss'] for t in losing_trades) / len(losing_trades)
                            
                        break
                
        except Exception as e:
            print(f"{Fore.YELLOW}Error parsing trade close info: {str(e)}{Style.RESET_ALL}")
    
    def process_user_input(self):
        """Check for user input commands"""
        try:
            # Windows-compatible input handling
            import os
            if os.name == 'nt':  # Windows
                import msvcrt
                if msvcrt.kbhit():  # Check if a key has been pressed
                    # Read and process the key
                    char = msvcrt.getch().decode('utf-8')
                    # Handle single character commands
                    if char == 't':
                        self.show_timestamp = not self.show_timestamp
                        print(f"Timestamps {'enabled' if self.show_timestamp else 'disabled'}")
                    elif char == 's':
                        self.auto_scroll = not self.auto_scroll
                        print(f"Auto-scroll {'enabled' if self.auto_scroll else 'disabled'}")
                    elif char == '?' or char == 'h' and not self.hyperfocus_enabled:
                        self.show_help()
                    elif char == 'c':
                        self.filter_keyword = None
                        print("Filter cleared")
                    elif char == 'v':
                        self.strategy_view = not self.strategy_view
                        self.performance_view = False  # Close other panel if open
                        if self.strategy_view:
                            self._display_strategy_panel()
                        else:
                            print("Strategy view disabled")
                    elif char == 'p':  # New command for performance view
                        self.performance_view = not self.performance_view
                        self.strategy_view = False  # Close other panel if open
                        if self.performance_view:
                            self._display_performance_panel()
                        else:
                            print("Performance view disabled")
                    elif char == 'h' and not self.hyperfocus_enabled:  # HyperFocus mode
                        self._switch_strategy("hyperfocus_strategy")
                    elif char == 'r':  # RSI strategy
                        self._switch_strategy("rsi_strategy")
                    elif char == 'm':  # MACD strategy
                        self._switch_strategy("macd_strategy")
                    elif char == 'k':
                        print(f"{Fore.RED}⚠️ EMERGENCY KILL BUTTON PRESSED! ⚠️{Style.RESET_ALL}")
                        confirm = input(f"{Fore.RED}Are you sure you want to cancel all orders and stop the bot? (y/n):{Style.RESET_ALL} ")
                        if confirm.lower() == 'y':
                            try:
                                # Import and run the emergency kill function
                                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                                from emergency_kill import emergency_kill
                                emergency_kill()
                            except Exception as e:
                                print(f"{Fore.RED}Error executing emergency kill: {str(e)}{Style.RESET_ALL}")
                        else:
                            print("Emergency kill aborted.")
                    elif char == 'q':
                        print("Quitting monitor...")
                        sys.exit(0)
                    elif char == 'f':  # For filter, we need to get the full input
                        print("Enter filter keyword: ", end='')
                        keyword = input().strip()
                        self.filter_keyword = keyword.lower()
                        print(f"Filtering for keyword: '{self.filter_keyword}'")
            else:  # Unix/Linux/macOS
                # Original select-based input handling
                import select
                if select.select([sys.stdin], [], [], 0.0)[0]:
                    command = sys.stdin.readline().strip()
                    
                    if command.lower() == 'q':
                        print("Quitting monitor...")
                        sys.exit(0)
                    elif command.lower() == 't':
                        self.show_timestamp = not self.show_timestamp
                        print(f"Timestamps {'enabled' if self.show_timestamp else 'disabled'}")
                    elif command.lower() == 's':
                        self.auto_scroll = not self.auto_scroll
                        print(f"Auto-scroll {'enabled' if self.auto_scroll else 'disabled'}")
                    elif command.lower() == '?' or command.lower() == 'help':
                        self.show_help()
                    elif command.lower() == 'c':
                        self.filter_keyword = None
                        print("Filter cleared")
                    elif command.lower() == 'v':
                        self.strategy_view = not self.strategy_view
                        self.performance_view = False  # Close other panel if open
                        if self.strategy_view:
                            self._display_strategy_panel()
                        else:
                            print("Strategy view disabled")
                    elif command.lower() == 'p':  # New command for performance view
                        self.performance_view = not self.performance_view
                        self.strategy_view = False  # Close other panel if open
                        if self.performance_view:
                            self._display_performance_panel()
                        else:
                            print("Performance view disabled")
                    elif command.lower() == 'h':  # HyperFocus mode
                        self._switch_strategy("hyperfocus_strategy")
                    elif command.lower() == 'r':  # RSI strategy
                        self._switch_strategy("rsi_strategy")
                    elif command.lower() == 'm':  # MACD strategy
                        self._switch_strategy("macd_strategy")
                    elif command.lower() == 'k':
                        print(f"{Fore.RED}⚠️ EMERGENCY KILL BUTTON PRESSED! ⚠️{Style.RESET_ALL}")
                        confirm = input(f"{Fore.RED}Are you sure you want to cancel all orders and stop the bot? (y/n):{Style.RESET_ALL} ")
                        if confirm.lower() == 'y':
                            try:
                                # Import and run the emergency kill function
                                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                                from emergency_kill import emergency_kill
                                emergency_kill()
                            except Exception as e:
                                print(f"{Fore.RED}Error executing emergency kill: {str(e)}{Style.RESET_ALL}")
                        else:
                            print("Emergency kill aborted.")
                    elif command.lower().startswith('f '):
                        self.filter_keyword = command[2:].lower()
                        print(f"Filtering for keyword: '{self.filter_keyword}'")
        except Exception as e:
            # Fallback if input handling fails
            print(f"{Fore.YELLOW}Input handling error: {str(e)}{Style.RESET_ALL}")
            
    def _switch_strategy(self, strategy_name):
        """Switch to a different strategy"""
        strategy_display_names = {
            "rsi_strategy": "RSI Strategy",
            "macd_strategy": "MACD Strategy", 
            "ml_strategy": "Machine Learning Strategy",
            "hyperfocus_strategy": "HyperFocus Mode"
        }
        
        display_name = strategy_display_names.get(strategy_name, strategy_name)
        
        try:
            # Change the strategy in config.json
            config_path = Path("config.json")
            if config_path.exists():
                print(f"{Fore.YELLOW}Switching strategy to {display_name}...{Style.RESET_ALL}")
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Update the active strategy
                old_strategy = config["strategies"]["active_strategy"]
                config["strategies"]["active_strategy"] = strategy_name
                
                # Enable the new strategy and disable others
                strategy_names = ["rsi_strategy", "macd_strategy", "ml_strategy", "hyperfocus_strategy"]
                for strat in strategy_names:
                    if strat in config["strategies"]:
                        config["strategies"][strat]["enabled"] = (strat == strategy_name)
                
                # Save the updated configuration
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"{Fore.GREEN}Strategy changed from {old_strategy} to {strategy_name}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please restart the bot for changes to take effect{Style.RESET_ALL}")
                
                # Update the current strategy (for display purposes)
                if strategy_name == "hyperfocus_strategy":
                    self.hyperfocus_enabled = True
                else:
                    self.hyperfocus_enabled = False
                self.current_strategy = display_name
                
                # Show the strategy panel
                self.strategy_view = True
                self._display_strategy_panel()
            else:
                print(f"{Fore.RED}Error: config.json not found!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error changing strategy: {str(e)}{Style.RESET_ALL}")
    
    def _display_strategy_panel(self):
        """Display the strategy information panel"""
        print("\n" + "=" * 60)
        print(f"{Fore.CYAN}STRATEGY INFORMATION PANEL{Style.RESET_ALL}")
        print("=" * 60)
        
        print(f"Active Strategy: {Fore.GREEN}{self.current_strategy}{Style.RESET_ALL}")
        
        if self.hyperfocus_enabled:
            print("\n🔍 HYPERFOCUS MODE ACTIVE")
            print(f"Signal strength: {self.strategy_metrics.get('confirmations', 'N/A')}")
            print(f"Signal indicators: {', '.join(self.strategy_metrics.get('indicators', ['RSI', 'MACD', 'MA', 'Volume']))}")
            print("\nHyperFocus combines multiple indicators for high-precision trading signals")
            print("- Primary indicator: RSI")
            print("- Confirmation indicators: MACD, Moving Averages, Volume")
        elif "rsi" in self.current_strategy.lower():
            print("\n📊 RSI STRATEGY ACTIVE")
            print("RSI (Relative Strength Index) measures momentum by comparing recent gains to losses")
            print("- Buy signal: RSI crosses above oversold threshold (30)")
            print("- Sell signal: RSI crosses below overbought threshold (70)")
        elif "macd" in self.current_strategy.lower():
            print("\n📈 MACD STRATEGY ACTIVE")
            print("MACD (Moving Average Convergence Divergence) identifies trend changes")
            print("- Buy signal: MACD line crosses above signal line")
            print("- Sell signal: MACD line crosses below signal line")
        
        print("\nCommands:")
        print(f"  {Fore.CYAN}h{Style.RESET_ALL} - Switch to HyperFocus Mode")
        print(f"  {Fore.CYAN}r{Style.RESET_ALL} - Switch to RSI Strategy")
        print(f"  {Fore.CYAN}m{Style.RESET_ALL} - Switch to MACD Strategy")
        print("=" * 60 + "\n")
    
    def _display_performance_panel(self):
        """Display trading performance metrics"""
        print("\n" + "=" * 60)
        print(f"{Fore.CYAN}TRADING PERFORMANCE METRICS{Style.RESET_ALL}")
        print("=" * 60)
        
        if self.trade_stats['total_trades'] == 0:
            print(f"\n{Fore.YELLOW}No trades recorded yet.{Style.RESET_ALL}")
        else:
            # Overall statistics
            print(f"\n📊 {Fore.GREEN}OVERALL PERFORMANCE{Style.RESET_ALL}")
            print(f"Total Trades: {self.trade_stats['total_trades']}")
            print(f"Win/Loss: {self.trade_stats['winning_trades']}/{self.trade_stats['losing_trades']}")
            
            win_rate = self.trade_stats['win_rate']
            win_rate_color = Fore.RED if win_rate < 40 else (Fore.YELLOW if win_rate < 60 else Fore.GREEN)
            print(f"Win Rate: {win_rate_color}{win_rate:.1f}%{Style.RESET_ALL}")
            
            pnl = self.trade_stats['total_profit_loss']
            pnl_color = Fore.RED if pnl < 0 else Fore.GREEN
            print(f"Total P&L: {pnl_color}{pnl:.4f} USDT{Style.RESET_ALL}")
            
            # Average metrics
            if self.trade_stats['winning_trades'] > 0 or self.trade_stats['losing_trades'] > 0:
                print(f"\n📈 {Fore.CYAN}TRADE METRICS{Style.RESET_ALL}")
                if self.trade_stats['winning_trades'] > 0:
                    print(f"Average Win: {Fore.GREEN}{self.trade_stats['average_win']:.4f}{Style.RESET_ALL}")
                if self.trade_stats['losing_trades'] > 0:
                    print(f"Average Loss: {Fore.RED}{self.trade_stats['average_loss']:.4f}{Style.RESET_ALL}")
                print(f"Largest Win: {Fore.GREEN}{self.trade_stats['largest_win']:.4f}{Style.RESET_ALL}")
                print(f"Largest Loss: {Fore.RED}{self.trade_stats['largest_loss']:.4f}{Style.RESET_ALL}")
            
            # Performance by strategy
            if self.trade_stats['strategy_performance']:
                print(f"\n🧠 {Fore.MAGENTA}STRATEGY PERFORMANCE{Style.RESET_ALL}")
                for strategy, stats in self.trade_stats['strategy_performance'].items():
                    strat_win_rate = (stats['winning'] / stats['trades']) * 100 if stats['trades'] > 0 else 0
                    strat_color = Fore.RED if strat_win_rate < 40 else (Fore.YELLOW if strat_win_rate < 60 else Fore.GREEN)
                    print(f"{strategy}: {strat_color}{strat_win_rate:.1f}% win rate{Style.RESET_ALL} ({stats['winning']}/{stats['trades']} trades)")
            
            # Recent trades
            print(f"\n🔄 {Fore.BLUE}RECENT TRADES{Style.RESET_ALL}")
            recent_trades = sorted([t for t in self.trades if t['status'] == 'closed'], key=lambda x: x['timestamp'], reverse=True)[:5]
            if recent_trades:
                for t in recent_trades:
                    trade_color = Fore.GREEN if t['profit_loss'] and t['profit_loss'] > 0 else Fore.RED
                    profit_text = f"{t['profit_loss']:.4f} ({t['profit_loss_percent']}%)" if t['profit_loss'] is not None else "Open"
                    print(f"• {t['action']} {t['amount']} {t['base_currency']} @ {t['price']} - {trade_color}{profit_text}{Style.RESET_ALL}")
            else:
                print("No closed trades yet")
            
            # Open positions
            print(f"\n📌 {Fore.YELLOW}OPEN POSITIONS{Style.RESET_ALL}")
            if self.open_positions:
                for pos in self.open_positions:
                    print(f"• {pos['action']} {pos['amount']} {pos['base_currency']} @ {pos['price']} {pos['quote_currency']}")
            else:
                print("No open positions")
        
        print("\nCommands:")
        print(f"  {Fore.GREEN}p{Style.RESET_ALL} - Hide performance panel")
        print(f"  {Fore.GREEN}v{Style.RESET_ALL} - Switch to strategy panel")
        print("=" * 60 + "\n")
        
    def monitor(self):
        """Main monitoring loop"""
        print(f"{Fore.GREEN}Starting monitoring of bot activities...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press '?' for help and available commands{Style.RESET_ALL}")
        
        # Check if log files exist
        if not os.path.exists("logs"):
            os.makedirs("logs")
            print(f"{Fore.YELLOW}Created logs directory{Style.RESET_ALL}")
            
        if not os.path.exists(LOG_FILE):
            print(f"{Fore.YELLOW}Log file not found. Waiting for bot to start...{Style.RESET_ALL}")
        
        try:
            display_counter = 0  # Counter for periodic updates
            while True:
                # Process any user commands
                self.process_user_input()
                
                # Get new log content
                new_content = self.get_new_log_content()
                new_trading_content = self.get_new_trading_content()
                
                # Process and display new content
                for line in new_content + new_trading_content:
                    # Apply keyword filter if set
                    if self.filter_keyword and self.filter_keyword.lower() not in line.lower():
                        continue
                        
                    formatted_line = self.format_log_line(line)
                    print(formatted_line)
                
                # Auto-scroll command
                if self.auto_scroll and (new_content or new_trading_content):
                    print(f"{Fore.BLUE}--- {datetime.now().strftime('%H:%M:%S')} ---{Style.RESET_ALL}")
                
                # Periodically show active panel if enabled
                display_counter += 1
                if display_counter >= 180:  # Show every ~5-6 minutes
                    if self.strategy_view:
                        self._display_strategy_panel()
                    elif self.performance_view:
                        self._display_performance_panel()
                    display_counter = 0
                
                time.sleep(REFRESH_RATE)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Monitor stopped. Goodbye!{Style.RESET_ALL}")

if __name__ == "__main__":
    monitor = BotMonitor()
    monitor.monitor()
