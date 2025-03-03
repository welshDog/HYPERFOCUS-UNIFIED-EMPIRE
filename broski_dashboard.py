import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

class BROskiDashboard:
    """
    Unified dashboard for BROski trading bot system.
    Provides access to all tools and functionality from a single interface.
    """
    
    def __init__(self, root=None):
        """Initialize the dashboard"""
        self.bot_process = None
        self.monitor_process = None
        
        # Create window
        self.root = tk.Tk() if root is None else root
        self.root.title("BROski Trading System")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Set icon
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass  # Icon not found, use default
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("Green.TButton", background="#4CAF50")
        self.style.configure("Red.TButton", background="#f44336")
        
        # Load configuration
        self.config = self.load_config()
        
        # Create UI
        self.create_widgets()
        
        # Status variables
        self.bot_status = "STOPPED"
        self.update_status()
        
        # Start status update loop
        self.update_bot_status()

    def load_config(self):
        """Load configuration from file"""
        config_path = Path("config.json")
        
        if not config_path.exists():
            example_config = Path("config.example.json")
            if example_config.exists():
                # Copy example config
                with open(example_config, 'r') as f:
                    config = json.load(f)
                    
                # Save as new config
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                messagebox.showinfo(
                    "Configuration Created", 
                    "A new configuration file has been created from the template.\n\n"
                    "Please configure your API keys and settings before trading."
                )
                return config
            else:
                messagebox.showerror(
                    "Configuration Error", 
                    "No configuration file found and example template is missing."
                )
                return {}
        
        # Load existing config
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error loading config: {str(e)}")
            return {}

    def create_widgets(self):
        """Create all dashboard widgets"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Create header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Logo/Header
        logo_label = ttk.Label(
            header_frame, 
            text="BROski Trading System", 
            font=("Arial", 18, "bold")
        )
        logo_label.pack(side="left")
        
        # Status indicators - right side of header
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side="right")
        
        self.status_label = ttk.Label(
            status_frame, 
            text="BOT: STOPPED", 
            font=("Arial", 10, "bold"),
            foreground="red"
        )
        self.status_label.pack(side="top")
        
        # Create tab control
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.pack(fill="both", expand=True)
        
        # Dashboard tab
        dashboard_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(dashboard_tab, text="Dashboard")
        self.create_dashboard_tab(dashboard_tab)
        
        # Configuration tab
        config_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(config_tab, text="Configuration")
        self.create_config_tab(config_tab)
        
        # Performance tab
        performance_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(performance_tab, text="Performance")
        self.create_performance_tab(performance_tab)
        
        # Help tab
        help_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(help_tab, text="Help")
        self.create_help_tab(help_tab)
        
        # Footer with version info
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=(10, 0))
        
        version_label = ttk.Label(
            footer_frame, 
            text="BROski v1.0", 
            font=("Arial", 8)
        )
        version_label.pack(side="left")
        
        # Close button
        close_button = ttk.Button(
            footer_frame, 
            text="Exit", 
            command=self.close_application
        )
        close_button.pack(side="right")
        
    def create_dashboard_tab(self, parent):
        """Create the main dashboard tab"""
        # Create two-column layout
        left_frame = ttk.Frame(parent, padding=10)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = ttk.Frame(parent, padding=10)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Left side - Bot controls
        control_frame = ttk.LabelFrame(left_frame, text="Bot Controls", padding=10)
        control_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Control buttons - using grid for better layout
        ttk.Button(
            control_frame,
            text="▶️ Start Bot",
            style="Green.TButton",
            command=self.start_bot,
            width=20
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            control_frame,
            text="⏹️ Stop Bot",
            style="Red.TButton",
            command=self.stop_bot,
            width=20
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            control_frame,
            text="🔍 Open Monitor",
            command=self.open_monitor,
            width=20
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            control_frame,
            text="📊 Trade Results",
            command=self.open_trade_results,
            width=20
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Quick strategy switcher
        strategy_frame = ttk.LabelFrame(left_frame, text="Strategy Selection", padding=10)
        strategy_frame.pack(fill="both", expand=True)
        
        ttk.Button(
            strategy_frame,
            text="Switch to HyperFocus Mode",
            command=lambda: self.switch_strategy("hyperfocus_strategy"),
            width=20
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            strategy_frame,
            text="Switch to RSI Strategy",
            command=lambda: self.switch_strategy("rsi_strategy"),
            width=20
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            strategy_frame,
            text="Switch to MACD Strategy",
            command=lambda: self.switch_strategy("macd_strategy"),
            width=20
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Right side - Status information
        status_frame = ttk.LabelFrame(right_frame, text="System Status", padding=10)
        status_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Status info
        self.active_strategy_var = tk.StringVar(value="Loading...")
        self.auto_trade_var = tk.StringVar(value="Disabled")
        self.trading_pair_var = tk.StringVar(value="Loading...")
        self.trade_amount_var = tk.StringVar(value="Loading...")
        
        ttk.Label(status_frame, text="Active Strategy:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.active_strategy_var, font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(status_frame, text="Auto-Trading:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.auto_trade_label = ttk.Label(status_frame, textvariable=self.auto_trade_var, font=("Arial", 10, "bold"))
        self.auto_trade_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(status_frame, text="Trading Pair:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.trading_pair_var).grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(status_frame, text="Trade Amount:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.trade_amount_var).grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        # Auto-trade toggle
        ttk.Button(
            status_frame,
            text="Toggle Auto-Trading",
            command=self.toggle_auto_trade,
            width=20
        ).grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Recent logs
        log_frame = ttk.LabelFrame(right_frame, text="Recent Activity", padding=10)
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, width=40, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
        # Refresh button
        ttk.Button(
            log_frame,
            text="🔄 Refresh",
            command=self.refresh_dashboard,
            width=10
        ).pack(side="right", pady=(5, 0))
        
        # Initialize status display
        self.update_dashboard_info()
        
    def create_config_tab(self, parent):
        """Create the configuration tab"""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # API Settings
        api_frame = ttk.LabelFrame(scrollable_frame, text="Exchange API Settings", padding=10)
        api_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(api_frame, text="Exchange:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(api_frame, text=self.config.get("exchange", {}).get("name", "Not set")).grid(row=0, column=1, sticky="w")
        
        ttk.Label(api_frame, text="API Key Status:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        api_key = self.config.get("exchange", {}).get("api_key", "")
        api_status = "Configured" if api_key and api_key != "YOUR_MEXC_API_KEY_HERE" else "Not Configured"
        ttk.Label(api_frame, text=api_status).grid(row=1, column=1, sticky="w")
        
        ttk.Button(
            api_frame,
            text="MEXC API Guide",
            command=self.open_api_guide
        ).grid(row=2, column=0, pady=10)
        
        ttk.Button(
            api_frame,
            text="Update API Settings",
            command=self.run_setup
        ).grid(row=2, column=1, pady=10)
        
        # Trading Settings
        trading_frame = ttk.LabelFrame(scrollable_frame, text="Trading Settings", padding=10)
        trading_frame.pack(fill="x", padx=10, pady=10)
        
        # Create trading settings form
        trading_settings = self.config.get("trading", {})
        
        ttk.Label(trading_frame, text="Base Symbol:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.base_symbol_var = tk.StringVar(value=trading_settings.get("base_symbol", "PI"))
        ttk.Entry(trading_frame, textvariable=self.base_symbol_var).grid(row=0, column=1, sticky="w")
        
        ttk.Label(trading_frame, text="Quote Symbol:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.quote_symbol_var = tk.StringVar(value=trading_settings.get("quote_symbol", "USDT"))
        ttk.Entry(trading_frame, textvariable=self.quote_symbol_var).grid(row=1, column=1, sticky="w")
        
        ttk.Label(trading_frame, text="Trade Amount:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.trade_amount_var = tk.StringVar(value=str(trading_settings.get("trade_amount", 10)))
        ttk.Entry(trading_frame, textvariable=self.trade_amount_var).grid(row=2, column=1, sticky="w")
        
        ttk.Label(trading_frame, text="Max Position Size:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.max_position_var = tk.StringVar(value=str(trading_settings.get("max_position_size", 100)))
        ttk.Entry(trading_frame, textvariable=self.max_position_var).grid(row=3, column=1, sticky="w")
        
        ttk.Label(trading_frame, text="Auto-Trade:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.auto_trade_config_var = tk.BooleanVar(value=trading_settings.get("auto_trade", False))
        ttk.Checkbutton(trading_frame, variable=self.auto_trade_config_var).grid(row=4, column=1, sticky="w")
        
        # Strategy Settings
        strategy_frame = ttk.LabelFrame(scrollable_frame, text="Strategy Settings", padding=10)
        strategy_frame.pack(fill="x", padx=10, pady=10)
        
        strategies = self.config.get("strategies", {})
        active_strategy = strategies.get("active_strategy", "rsi_strategy")
        
        ttk.Label(strategy_frame, text="Active Strategy:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.active_strategy_config_var = tk.StringVar(value=active_strategy)
        strategy_combo = ttk.Combobox(strategy_frame, textvariable=self.active_strategy_config_var, state="readonly")
        strategy_combo['values'] = ["rsi_strategy", "macd_strategy", "hyperfocus_strategy"]
        strategy_combo.grid(row=0, column=1, sticky="w")
        
        # Save button
        ttk.Button(
            scrollable_frame,
            text="Save Configuration",
            command=self.save_config,
            style="Green.TButton"
        ).pack(pady=20)
        
    def create_performance_tab(self, parent):
        """Create the performance tab"""
        # Top buttons
        buttons_frame = ttk.Frame(parent, padding=10)
        buttons_frame.pack(fill="x")
        
        ttk.Button(
            buttons_frame,
            text="Open Performance Dashboard",
            command=self.open_trade_results,
            width=25
        ).pack(side="left", padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Refresh Data",
            command=self.refresh_performance_data,
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Export Trading Data",
            command=self.export_trade_data,
            width=20
        ).pack(side="left", padx=5)
        
        # Performance summary
        summary_frame = ttk.LabelFrame(parent, text="Performance Summary", padding=10)
        summary_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.performance_text = tk.Text(summary_frame, wrap="word", height=10)
        self.performance_text.pack(fill="both", expand=True)
        
        self.load_performance_data()
        
    def create_help_tab(self, parent):
        """Create the help tab"""
        # Create scrollable frame for help
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Help sections
        sections = [
            ("Quick Start Guide", self.open_quick_start),
            ("Setup Guide", self.open_setup_guide),
            ("Trading Strategies", self.open_strategies_guide),
            ("Configuration Help", self.open_config_help),
            ("Troubleshooting", self.open_troubleshooting),
            ("FAQ", self.open_faq)
        ]
        
        for i, (title, command) in enumerate(sections):
            section_frame = ttk.LabelFrame(scrollable_frame, text=title, padding=10)
            section_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Button(
                section_frame,
                text=f"Open {title}",
                command=command,
                width=20
            ).pack(pady=5)
        
    def update_bot_status(self):
        """Periodically update the bot status"""
        self.check_bot_running()
        self.root.after(5000, self.update_bot_status)  # Check every 5 seconds
    
    def check_bot_running(self):
        """Check if the bot is currently running"""
        # Check if process is running
        if self.bot_process and self.bot_process.poll() is None:
            self.bot_status = "RUNNING"
        else:
            self.bot_status = "STOPPED"
            self.bot_process = None
            
        self.update_status()
        
    def update_status(self):
        """Update the status display"""
        if self.bot_status == "RUNNING":
            self.status_label.config(text="BOT: RUNNING", foreground="green")
        else:
            self.status_label.config(text="BOT: STOPPED", foreground="red")
    
    def update_dashboard_info(self):
        """Update the dashboard information"""
        # Load current config
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                
            # Update display variables
            active_strategy = config["strategies"]["active_strategy"]
            nice_names = {
                "rsi_strategy": "RSI Strategy",
                "macd_strategy": "MACD Strategy",
                "hyperfocus_strategy": "HyperFocus Mode",
                "ml_strategy": "Machine Learning"
            }
            self.active_strategy_var.set(nice_names.get(active_strategy, active_strategy))
            
            auto_trade = config["trading"]["auto_trade"]
            self.auto_trade_var.set("Enabled" if auto_trade else "Disabled")
            self.auto_trade_label.config(foreground="green" if auto_trade else "red")
            
            base = config["trading"]["base_symbol"]
            quote = config["trading"]["quote_symbol"]
            self.trading_pair_var.set(f"{base}/{quote}")
            
            self.trade_amount_var.set(f"{config['trading']['trade_amount']} {quote}")
        except Exception as e:
            print(f"Error updating dashboard: {str(e)}")
            
        # Update recent logs
        self.update_recent_logs()
            
    def update_recent_logs(self):
        """Update the recent logs display"""
        try:
            log_path = Path("logs/broski_bot.log")
            if log_path.exists():
                with open(log_path, 'r') as f:
                    # Get last 10 lines
                    lines = f.readlines()[-10:]
                    
                    self.log_text.config(state="normal")
                    self.log_text.delete("1.0", tk.END)
                    
                    for line in lines:
                        self.log_text.insert(tk.END, line)
                        
                    self.log_text.config(state="disabled")
        except Exception as e:
            print(f"Error updating logs: {str(e)}")
    
    def load_performance_data(self):
        """Load and display performance data"""
        trade_file = Path("logs/trade_history.json")
        
        if not trade_file.exists():
            self.performance_text.insert(tk.END, "No trading data found yet.\n\n")
            self.performance_text.insert(tk.END, "Run the bot to start collecting trading data.")
            return
            
        try:
            with open(trade_file, 'r') as f:
                trades = json.load(f)
                
            # Calculate basic metrics
            closed_trades = [t for t in trades if t.get('status') == 'closed']
            
            if not closed_trades:
                self.performance_text.insert(tk.END, "No closed trades found yet.\n\n")
                self.performance_text.insert(tk.END, "Trading data is being collected, but no trades have been completed.")
                return
                
            total_trades = len(closed_trades)
            winning_trades = len([t for t in closed_trades if t.get('pnl', 0) > 0])
            losing_trades = len([t for t in closed_trades if t.get('pnl', 0) < 0])
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            total_pnl = sum(t.get('pnl', 0) for t in closed_trades)
            
            # Display metrics
            self.performance_text.insert(tk.END, f"Total Trades: {total_trades}\n")
            self.performance_text.insert(tk.END, f"Win Rate: {win_rate:.1f}%\n")
            self.performance_text.insert(tk.END, f"Total Profit/Loss: {total_pnl:.2f} USDT\n\n")
            
            # Get strategy performance
            strategy_trades = {}
            for trade in closed_trades:
                strategy = trade.get('strategy', 'unknown')
                if strategy not in strategy_trades:
                    strategy_trades[strategy] = []
                strategy_trades[strategy].append(trade)
                
            self.performance_text.insert(tk.END, "Strategy Performance:\n")
            for strategy, trades in strategy_trades.items():
                wins = len([t for t in trades if t.get('pnl', 0) > 0])
                strat_win_rate = (wins / len(trades) * 100) if trades else 0
                strat_pnl = sum(t.get('pnl', 0) for t in trades)
                
                self.performance_text.insert(tk.END, f"- {strategy}: {strat_win_rate:.1f}% win rate, {strat_pnl:.2f} USDT\n")
            
        except Exception as e:
            self.performance_text.insert(tk.END, f"Error loading performance data: {str(e)}")
    
    def refresh_dashboard(self):
        """Refresh all dashboard information"""
        self.update_dashboard_info()
        
    def refresh_performance_data(self):
        """Refresh performance data"""
        self.performance_text.delete("1.0", tk.END)
        self.load_performance_data()
        
    def start_bot(self):
        """Start the trading bot"""
        if self.bot_process and self.bot_process.poll() is None:
            messagebox.showinfo("Already Running", "The bot is already running.")
            return
            
        try:
            # Ensure the logs directory exists
            os.makedirs("logs", exist_ok=True)
            
            # Clear previous log content
            with open(os.path.join("logs", "broski_bot.log"), 'w') as f:
                f.write(f"Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Start the bot process using direct_bot.py instead of broski_launcher.py
            self.bot_process = subprocess.Popen(
                ["python", "direct_bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.bot_status = "RUNNING"
            self.update_status()
            self.update_dashboard_info()
            
            messagebox.showinfo("Bot Started", "The trading bot has been started successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start the bot: {str(e)}")

    def stop_bot(self):
        """Stop the trading bot"""
        if not self.bot_process or self.bot_process.poll() is not None:
            messagebox.showinfo("Not Running", "The bot is not currently running.")
            return
            
        try:
            # Try to terminate gracefully
            self.bot_process.terminate()
            
            # Wait a bit for graceful shutdown
            self.bot_process.wait(timeout=5)
            
            # Force kill if needed
            if self.bot_process.poll() is None:
                self.bot_process.kill()
                
            self.bot_status = "STOPPED"
            self.update_status()
            messagebox.showinfo("Bot Stopped", "The trading bot has been stopped.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop the bot: {str(e)}")
    
    def open_monitor(self):
        """Open the bot monitor window"""
        if self.monitor_process and self.monitor_process.poll() is None:
            messagebox.showinfo("Already Running", "The monitor is already open.")
            return
            
        try:
            # Launch the monitor using the dedicated batch file
            if os.path.exists("MONITOR.bat"):
                # Use start command to ensure it opens in a new window
                self.monitor_process = subprocess.Popen(
                    ["cmd", "/c", "start", "MONITOR.bat"],
                    shell=True
                )
            else:
                # Fallback to direct Python execution with a visible console window
                self.monitor_process = subprocess.Popen(
                    ["python", "bot_monitor.py"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open monitor: {str(e)}")
    
    def open_trade_results(self):
        """Open the trade results dashboard"""
        try:
            # Check if we should use batch file or direct Python
            if os.path.exists("SHOW_RESULTS.bat"):
                subprocess.Popen(
                    ["cmd", "/c", "SHOW_RESULTS.bat"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                subprocess.Popen(
                    ["python", "show_trade_results.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open trade results: {str(e)}")
    
    def switch_strategy(self, strategy):
        """Switch to a different strategy"""
        try:
            # Load config
            with open("config.json", 'r') as f:
                config = json.load(f)
                
            # Update active strategy
            config["strategies"]["active_strategy"] = strategy
            
            # Set this strategy as enabled, disable others
            for strat in ["rsi_strategy", "macd_strategy", "hyperfocus_strategy"]:
                if strat in config["strategies"]:
                    config["strategies"][strat]["enabled"] = (strat == strategy)
                    
            # Save config
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update dashboard
            nice_names = {
                "rsi_strategy": "RSI Strategy",
                "macd_strategy": "MACD Strategy", 
                "hyperfocus_strategy": "HyperFocus Mode"
            }
            self.active_strategy_var.set(nice_names.get(strategy, strategy))
            
            messagebox.showinfo("Strategy Changed", f"Trading strategy switched to {nice_names.get(strategy, strategy)}")
            
            # Restart bot if running
            restart = False
            if self.bot_process and self.bot_process.poll() is None:
                restart = messagebox.askyesno("Restart Bot", 
                    "The bot is currently running. Do you want to restart it with the new strategy?")
                
            if restart:
                self.stop_bot()
                self.root.after(1000, self.start_bot)  # Start after 1 second delay
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch strategy: {str(e)}")
    
    def toggle_auto_trade(self):
        """Toggle auto-trading on/off"""
        try:
            # Load config
            with open("config.json", 'r') as f:
                config = json.load(f)
            
            # Toggle setting
            current = config["trading"]["auto_trade"]
            config["trading"]["auto_trade"] = not current
            
            # Save config
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update display
            auto_trade = config["trading"]["auto_trade"]
            self.auto_trade_var.set("Enabled" if auto_trade else "Disabled")
            self.auto_trade_label.config(foreground="green" if auto_trade else "red")
            
            status = "enabled" if auto_trade else "disabled"
            messagebox.showinfo("Auto-Trade", f"Auto-trading has been {status}.")
            
            # Ask about restarting the bot
            restart = False
            if self.bot_process and self.bot_process.poll() is None:
                restart = messagebox.askyesno("Restart Bot", 
                    "The bot is currently running. Do you want to restart it with the new settings?")
                
            if restart:
                self.stop_bot()
                self.root.after(1000, self.start_bot)  # Start after 1 second delay
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle auto-trade: {str(e)}")
    
    def save_config(self):
        """Save the configuration from the form to the config file"""
        try:
            # Load current config
            with open("config.json", 'r') as f:
                config = json.load(f)
            
            # Update with form values
            config["trading"]["base_symbol"] = self.base_symbol_var.get()
            config["trading"]["quote_symbol"] = self.quote_symbol_var.get()
            config["trading"]["trade_amount"] = float(self.trade_amount_var.get())
            config["trading"]["max_position_size"] = float(self.max_position_var.get())
            config["trading"]["auto_trade"] = self.auto_trade_config_var.get()
            
            # Update active strategy
            config["strategies"]["active_strategy"] = self.active_strategy_config_var.get()
            
            # Save config
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update dashboard
            self.update_dashboard_info()
            
            messagebox.showinfo("Saved", "Configuration saved successfully!")
            
            # Ask about restarting the bot
            restart = False
            if self.bot_process and self.bot_process.poll() is None:
                restart = messagebox.askyesno("Restart Bot", 
                    "The bot is currently running. Do you want to restart it with the new settings?")
                
            if restart:
                self.stop_bot()
                self.root.after(1000, self.start_bot)  # Start after 1 second delay
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def run_setup(self):
        """Run the setup wizard"""
        try:
            if os.path.exists("setup.py"):
                subprocess.Popen(
                    ["python", "setup.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif os.path.exists("wizard.py"):
                subprocess.Popen(
                    ["python", "wizard.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                messagebox.showerror("Error", "Setup script not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run setup: {str(e)}")
    
    def open_api_guide(self):
        """Open the API guide"""
        try:
            if os.path.exists("api_security_guide.md"):
                webbrowser.open(os.path.abspath("api_security_guide.md"))
            elif os.path.exists("mexc_api_guide.py"):
                subprocess.Popen(
                    ["python", "mexc_api_guide.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                messagebox.showerror("Error", "API Guide not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open API guide: {str(e)}")
    
    def open_quick_start(self):
        """Open the quick start guide"""
        self._open_help_document("GETTING_STARTED.md")
    
    def open_setup_guide(self):
        """Open the setup guide"""
        self._open_help_document("setup_guide.md")
    
    def open_strategies_guide(self):
        """Open the strategies guide"""
        self._open_help_document("STRATEGIES.md")
    
    def open_config_help(self):
        """Open the configuration help"""
        self._open_help_document("CONFIGURATION.md")
    
    def open_troubleshooting(self):
        """Open the troubleshooting guide"""
        self._open_help_document("TROUBLESHOOTING.md")
    
    def open_faq(self):
        """Open the FAQ"""
        self._open_help_document("FAQ.md")
    
    def _open_help_document(self, filename):
        """Helper to open a documentation file"""
        try:
            if os.path.exists(filename):
                webbrowser.open(os.path.abspath(filename))
            else:
                messagebox.showinfo("Documentation", f"The {filename} file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open document: {str(e)}")
    
    def export_trade_data(self):
        """Export trading data to CSV"""
        try:
            # Check if trade history exists
            trade_file = Path("logs/trade_history.json")
            if not trade_file.exists():
                messagebox.showinfo("Export", "No trading data available to export.")
                return
            
            # Ask for save location
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Trading Data"
            )
            
            if not file_path:
                return
            
            # Run the export script or do it directly
            try:
                import pandas as pd
                
                # Load trade data
                with open(trade_file, 'r') as f:
                    trades = json.load(f)
                
                # Convert to DataFrame
                df = pd.DataFrame(trades)
                
                # Add date column if timestamp exists
                if 'timestamp' in df.columns:
                    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                
                # Save to CSV
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Export", f"Trading data exported to {file_path}")
                
            except ImportError:
                # If pandas not available, use the export script if it exists
                if os.path.exists("export_data.py"):
                    subprocess.run(
                        ["python", "export_data.py", "--format", "csv", "--output", file_path],
                        check=True
                    )
                    messagebox.showinfo("Export", f"Trading data exported to {file_path}")
                else:
                    messagebox.showerror("Export Error", "Required libraries not found and export_data.py not available.")
                
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def close_application(self):
        """Close the dashboard and stop any running processes"""
        # Stop the bot if running
        if self.bot_process and self.bot_process.poll() is None:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=2)
            except:
                # Force kill if needed
                try:
                    self.bot_process.kill()
                except:
                    pass
        
        # Stop the monitor if running
        if self.monitor_process and self.monitor_process.poll() is None:
            try:
                self.monitor_process.terminate()
                self.monitor_process.wait(timeout=2)
            except:
                # Force kill if needed
                try:
                    self.monitor_process.kill()
                except:
                    pass
        
        # Destroy the window
        self.root.destroy()

# Allow running the dashboard directly
if __name__ == "__main__":
    dashboard = BROskiDashboard()
    dashboard.root.mainloop()
