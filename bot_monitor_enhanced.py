import os
import sys
import time
import json
import re
import threading
import signal
import curses
from datetime import datetime
from pathlib import Path

class BROskiMonitor:
    """Enhanced visual monitor for BROski trading bot"""
    
    def __init__(self):
        self.log_file = os.path.join("logs", "broski_bot.log")
        self.config_file = "config.json"
        self.trade_file = os.path.join("logs", "trade_history.json")
        self.show_timestamps = True
        self.filter_text = None
        self.auto_scroll = True
        self.last_position = 0
        self.log_buffer = []
        self.max_buffer_size = 1000
        self.current_price = 0.0
        self.open_positions = []
        self.last_signals = []
        self.config = self.load_config()
        self.base_symbol = self.config.get("trading", {}).get("base_symbol", "PI")
        self.quote_symbol = self.config.get("trading", {}).get("quote_symbol", "USDT")
        self.auto_trade = self.config.get("trading", {}).get("auto_trade", False)
        self.active_strategy = self.config.get("strategies", {}).get("active_strategy", "rsi_strategy")
        
    def load_config(self):
        """Load configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
            
    def load_trades(self):
        """Load trade history"""
        try:
            if os.path.exists(self.trade_file):
                with open(self.trade_file, 'r') as f:
                    trades = json.load(f)
                # Extract open positions
                self.open_positions = [t for t in trades if t.get('status') == 'open']
                return trades
            return []
        except Exception:
            return []
    
    def run_curses(self):
        """Run the monitor in curses mode for better formatting"""
        curses.wrapper(self.main_loop)
    
    def main_loop(self, stdscr):
        """Main program loop using curses"""
        # Setup colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Buy signals
        curses.init_pair(2, curses.COLOR_RED, -1)    # Sell signals
        curses.init_pair(3, curses.COLOR_YELLOW, -1) # Warnings/alerts
        curses.init_pair(4, curses.COLOR_CYAN, -1)   # Info
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE) # Header
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN) # Positive
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_RED)  # Negative
        
        # Hide cursor
        curses.curs_set(0)
        
        # Start log monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_logs)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Trade refresh thread
        trade_thread = threading.Thread(target=self.refresh_trades)
        trade_thread.daemon = True
        trade_thread.start()
        
        # Handle keypresses
        input_thread = threading.Thread(target=self.handle_input, args=(stdscr,))
        input_thread.daemon = True
        input_thread.start()
        
        # Refresh display periodically
        try:
            while True:
                self.draw_screen(stdscr)
                time.sleep(0.5)
        except KeyboardInterrupt:
            return
    
    def draw_screen(self, stdscr):
        """Draw the monitor screen with all sections"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw header
        self.draw_header(stdscr, width)
        
        # Draw status panel
        self.draw_status_panel(stdscr, 2, width)
        
        # Draw position summary if we have open positions
        if self.open_positions:
            self.draw_positions(stdscr, 5, width)
            log_start = 8
        else:
            log_start = 5
        
        # Draw logs (bottom section)
        self.draw_logs(stdscr, log_start, height, width)
        
        stdscr.refresh()
    
    def draw_header(self, stdscr, width):
        """Draw header with title and status"""
        header = f" BROski Monitor - {self.base_symbol}/{self.quote_symbol} "
        header = header.center(width, '=')
        stdscr.addstr(0, 0, header, curses.color_pair(5) | curses.A_BOLD)
    
    def draw_status_panel(self, stdscr, start_row, width):
        """Draw trading status information"""
        # Active strategy
        strategy_name = self.active_strategy.replace('_strategy', '').upper()
        stdscr.addstr(start_row, 0, f"Strategy: ", curses.A_BOLD)
        stdscr.addstr(strategy_name, curses.color_pair(4) | curses.A_BOLD)
        
        # Current price if available
        if self.current_price > 0:
            price_col = width - len(f"Price: {self.current_price:.4f}") - 2
            stdscr.addstr(start_row, price_col, f"Price: ", curses.A_BOLD)
            stdscr.addstr(f"{self.current_price:.4f}", curses.color_pair(4))
        
        # Auto-trade status
        auto_status = "ENABLED" if self.auto_trade else "DISABLED"
        auto_color = curses.color_pair(1) if self.auto_trade else curses.color_pair(2)
        status_text = f"Auto-Trading: {auto_status}"
        stdscr.addstr(start_row + 1, 0, "Auto-Trading: ", curses.A_BOLD)
        stdscr.addstr(auto_status, auto_color | curses.A_BOLD)
        
        # Filter status if active
        if self.filter_text:
            filter_col = width - len(f"Filter: {self.filter_text}") - 2
            stdscr.addstr(start_row + 1, filter_col, f"Filter: ", curses.A_BOLD)
            stdscr.addstr(self.filter_text, curses.color_pair(3))
    
    def draw_positions(self, stdscr, start_row, width):
        """Draw current open positions"""
        stdscr.addstr(start_row, 0, "Open Positions:", curses.A_BOLD)
        if not self.open_positions:
            return
            
        # Just show the first position if we have multiple
        pos = self.open_positions[0]
        pos_type = pos.get('type', 'unknown').upper()
        pos_amount = pos.get('amount', 0)
        pos_price = pos.get('price', 0)
        
        # Calculate current P&L if we have current price
        pnl = 0
        if self.current_price > 0 and pos_price > 0:
            if pos_type.lower() == 'buy':
                pnl = (self.current_price - pos_price) * pos_amount
            else:
                pnl = (pos_price - self.current_price) * pos_amount
        
        # Format position info
        position_text = f"{pos_type} {pos_amount} @ {pos_price:.4f}"
        stdscr.addstr(start_row + 1, 2, position_text)
        
        # Show P&L if calculated
        if pnl != 0:
            pnl_text = f"P&L: {pnl:.2f} ({(pnl/(pos_price*pos_amount))*100:.1f}%)"
            pnl_color = curses.color_pair(1) if pnl > 0 else curses.color_pair(2)
            stdscr.addstr(start_row + 1, len(position_text) + 4, pnl_text, pnl_color)
        
        # Show count if we have more positions
        if len(self.open_positions) > 1:
            more_text = f"(+{len(self.open_positions)-1} more)"
            stdscr.addstr(start_row + 1, width - len(more_text) - 2, more_text)
    
    def draw_logs(self, stdscr, start_row, height, width):
        """Draw log entries with formatting"""
        log_height = height - start_row - 1
        log_width = width - 2
        
        # Draw separator
        separator = "─" * width
        stdscr.addstr(start_row - 1, 0, separator, curses.color_pair(4))
        
        # Calculate which logs to display based on available space
        display_logs = self.get_filtered_logs()
        if self.auto_scroll and display_logs:
            display_logs = display_logs[-log_height:]
        else:
            # TODO: Implement scrolling
            display_logs = display_logs[-log_height:]
        
        # Draw logs
        for i, log in enumerate(display_logs):
            if start_row + i >= height:
                break
                
            # Default color
            color = curses.color_pair(0)
            
            # Apply specific colors based on log content
            if "BUY signal" in log or " buy " in log.lower():
                color = curses.color_pair(1)
            elif "SELL signal" in log or " sell " in log.lower():
                color = curses.color_pair(2)
            elif "error" in log.lower() or "failed" in log.lower():
                color = curses.color_pair(2)
            elif "warning" in log.lower():
                color = curses.color_pair(3)
            elif "price" in log.lower():
                color = curses.color_pair(4)
                
                # Try to extract price
                price_match = re.search(r'price[:\s]+([0-9.]+)', log.lower())
                if price_match:
                    try:
                        self.current_price = float(price_match.group(1))
                    except ValueError:
                        pass
            
            # Truncate log if needed
            if len(log) > log_width:
                log = log[:log_width-3] + "..."
            
            # Display the log
            stdscr.addstr(start_row + i, 0, log, color)
        
        # Status line
        status_line = f"Logs: {len(display_logs)}/{len(self.log_buffer)}"
        if self.filter_text:
            status_line += f" | Filter: {self.filter_text}"
        stdscr.addstr(height - 1, 0, status_line, curses.A_REVERSE)
    
    def get_filtered_logs(self):
        """Get logs that match the current filter"""
        if not self.filter_text:
            return self.log_buffer
        
        return [log for log in self.log_buffer if self.filter_text.lower() in log.lower()]
    
    def monitor_logs(self):
        """Background thread to monitor log file"""
        try:
            # Ensure log file exists
            if not os.path.exists(self.log_file):
                log_dir = os.path.dirname(self.log_file)
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                with open(self.log_file, 'w') as f:
                    f.write("Log file created for BROski Bot\n")
            
            # Initial file position
            with open(self.log_file, 'r') as f:
                # Start from the end of the file
                f.seek(0, 2)
                self.last_position = f.tell()
            
            # Continue reading as file grows
            while True:
                with open(self.log_file, 'r') as f:
                    f.seek(self.last_position)
                    new_logs = f.readlines()
                    if new_logs:
                        self.process_new_logs(new_logs)
                    self.last_position = f.tell()
                
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Error monitoring logs: {e}")
    
    def process_new_logs(self, logs):
        """Process new log entries, format them, and add to buffer"""
        # Import the monitor logger for metrics capture
        try:
            from monitor_logger import MonitorLogger
            logger = MonitorLogger()
        except ImportError:
            logger = None
        
        for log in logs:
            log = log.strip()
            if not log:
                continue
                
            # Extract timestamp and message if present
            timestamp_match = re.match(r'^\[([^\]]+)\]', log)
            if timestamp_match and self.show_timestamps:
                timestamp = timestamp_match.group(1)
                formatted_log = log
            elif timestamp_match and not self.show_timestamps:
                message = log[len(timestamp_match.group(0)):].strip()
                formatted_log = message
            else:
                formatted_log = log
            
            # Capture important metrics for strategy optimization
            if logger:
                # Try to extract indicator values from logs
                if "RSI:" in log:
                    try:
                        rsi_match = re.search(r'RSI:[\s]*([0-9.]+)', log)
                        if rsi_match:
                            rsi_value = float(rsi_match.group(1))
                            logger.capture_indicator_values(
                                self.active_strategy,
                                {'rsi_value': rsi_value},
                                "unknown",  # Timeframe often not in logs
                                self.current_price
                            )
                    except Exception:
                        pass
                
                # Capture trading signals
                if "signal" in log.lower():
                    signal_type = None
                    if "buy signal" in log.lower():
                        signal_type = "BUY"
                    elif "sell signal" in log.lower():
                        signal_type = "SELL"
                        
                    if signal_type:
                        logger.capture_signal(
                            self.active_strategy,
                            signal_type,
                            "unknown",  # Timeframe
                            self.current_price
                        )
                
                # Track price information
                price_match = re.search(r'price[:\s]+([0-9.]+)', log.lower())
                if price_match:
                    try:
                        price = float(price_match.group(1))
                        self.current_price = price
                    except ValueError:
                        pass
                
            # Track trade signals
            if "signal" in log.lower():
                self.last_signals.append((time.time(), formatted_log))
                # Keep only recent signals
                self.last_signals = [s for s in self.last_signals if time.time() - s[0] < 300]
            
            # Add to buffer
            self.log_buffer.append(formatted_log)
            
            # Trim buffer if too large
            if len(self.log_buffer) > self.max_buffer_size:
                self.log_buffer = self.log_buffer[-self.max_buffer_size:]
    
    def refresh_trades(self):
        """Background thread to periodically refresh trade data"""
        while True:
            self.load_trades()
            time.sleep(5)  # Refresh every 5 seconds
    
    def handle_input(self, stdscr):
        """Handle user keyboard input"""
        stdscr.nodelay(True)
        while True:
            try:
                key = stdscr.getch()
                if key != -1:
                    self.process_key(stdscr, key)
            except Exception:
                pass
            time.sleep(0.1)
    
    def process_key(self, stdscr, key):
        """Process a keypress"""
        # Convert key to character if possible
        try:
            char = chr(key).lower()
        except ValueError:
            char = None
        
        # Process known commands
        if char == 't':
            # Toggle timestamps
            self.show_timestamps = not self.show_timestamps
        elif char == 'c':
            # Clear screen/buffer
            self.log_buffer = []
        elif char == 's':
            # Toggle auto-scroll
            self.auto_scroll = not self.auto_scroll
        elif char == 'f':
            # Set filter
            curses.echo()
            stdscr.addstr(0, 0, "Enter filter text: ")
            stdscr.clrtoeol()
            stdscr.refresh()
            curses.curs_set(1)
            filter_text = stdscr.getstr(0, 17)
            curses.curs_set(0)
            curses.noecho()
            self.filter_text = filter_text.decode('utf-8') if filter_text else None
        elif char == 'h':
            # Switch to HyperFocus strategy
            self.update_strategy("hyperfocus_strategy")
        elif char == 'r':
            # Switch to RSI strategy
            self.update_strategy("rsi_strategy")
        elif char == 'm':
            # Switch to MACD strategy
            self.update_strategy("macd_strategy")
        elif char == '?':
            # Show help
            self.show_help(stdscr)
        elif char == 'q':
            # Quit
            sys.exit(0)
    
    def update_strategy(self, strategy):
        """Update trading strategy in config file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Set active strategy
            config["strategies"]["active_strategy"] = strategy
            
            # Enable the selected strategy, disable others
            for strat in ["rsi_strategy", "macd_strategy", "hyperfocus_strategy"]:
                if strat in config["strategies"]:
                    config["strategies"][strat]["enabled"] = (strat == strategy)
            
            # Save updated config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update local tracking
            self.active_strategy = strategy
            
            # Add to log buffer
            self.log_buffer.append(f"✓ Strategy changed to {strategy}")
            
        except Exception as e:
            self.log_buffer.append(f"❌ Error changing strategy: {e}")
    
    def show_help(self, stdscr):
        """Show help overlay"""
        height, width = stdscr.getmaxyx()
        help_win = curses.newwin(14, 50, (height // 2) - 7, (width // 2) - 25)
        help_win.box()
        help_win.addstr(0, 20, " HELP ", curses.A_BOLD)
        
        help_items = [
            (1, "t", "Toggle timestamps"),
            (2, "f", "Filter log entries"),
            (3, "c", "Clear log display"),
            (4, "s", "Toggle auto-scroll"),
            (5, "h", "Switch to HyperFocus strategy"),
            (6, "r", "Switch to RSI strategy"),
            (7, "m", "Switch to MACD strategy"),
            (8, "p", "Show open positions"),
            (9, "v", "View strategy settings"),
            (10, "q", "Quit monitor"),
            (12, " ", "Press any key to close help")
        ]
        
        for row, key, description in help_items:
            help_win.addstr(row, 2, f"{key}")
            help_win.addstr(row, 10, f"{description}")
        
        help_win.refresh()
        stdscr.getch()  # Wait for keypress

if __name__ == "__main__":
    # Initialize and run monitor
    monitor = BROskiMonitor()
    try:
        monitor.run_curses()
    except KeyboardInterrupt:
        sys.exit(0)
