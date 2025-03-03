import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import json
import datetime
import time
import shutil
from pathlib import Path

class BROskiControlCenter:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("BROski Bot - Control Center")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 650)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("Green.TButton", background="#4CAF50")
        self.style.configure("Red.TButton", background="#f44336")
        self.style.configure("Orange.TButton", background="#FF9800")
        self.style.configure("Blue.TButton", background="#2196F3")
        
        # Set icon
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass  # Icon not found, use default
        
        # Status variables
        self.bot_running = False
        self.bot_process = None
        self.monitor_process = None
        
        # Load configuration
        self.load_config()
        
        # Create the UI
        self.create_widgets()
        
        # Start status updater
        self.update_status()
        
    # ... existing widget creation methods ...
    
    def create_control_tab(self, parent):
        """Create the main control tab"""
        # ... existing code ...
        pass

    def create_monitor_tab(self, parent):
        """Create the monitoring tab"""
        # ... existing code ...
        pass

    def create_config_tab(self, parent):
        """Create the configuration tab"""
        # ... existing code ...
        pass

    def create_tools_tab(self, parent):
        """Create the tools and utilities tab"""
        # ... existing code ...
        pass

    def create_log_management_tab(self, parent):
        """Create log management tools"""
        # ... existing code ...
        pass

    def create_process_management_tab(self, parent):
        """Create process management tools"""
        # ... existing code ...
        pass

    def create_backup_tab(self, parent):
        """Create backup & restore tools"""
        # ... existing code ...
        pass

    def create_health_tab(self, parent):
        """Create the health & diagnostics tab"""
        # ... existing code ...
        pass
    
    # ===== Bot Control Functions =====
    def start_bot(self):
        """Start the trading bot"""
        # ... existing code ...
        pass
    
    def stop_bot(self):
        """Stop the trading bot"""
        # ... existing code ...
        pass
    
    def monitor_bot_output(self):
        """Monitor the bot's output in a separate thread"""
        # ... existing code ...
        pass
    
    def handle_bot_terminated(self):
        """Handle bot process termination"""
        # ... existing code ...
        pass
    
    def toggle_auto_trade(self):
        """Toggle auto trading mode"""
        # ... existing code ...
        pass
    
    def toggle_show_keys(self):
        """Toggle showing/hiding API keys"""
        # ... existing code ...
        pass
    
    def load_config(self):
        """Load configuration from file"""
        # ... existing code ...
        pass
    
    def save_config(self):
        """Save current configuration to file"""
        # ... existing code ...
        pass
    
    def update_status(self):
        """Update status periodically"""
        # ... existing code ...
        pass
    
    def add_activity(self, message):
        """Add message to activity log"""
        # ... existing code ...
        pass
    
    def write_to_log(self, message):
        """Write message to the bot log file"""
        # ... existing code ...
        pass
    
    def refresh_log(self):
        """Refresh the log display"""
        # ... existing code ...
        pass
    
    def clear_log(self):
        """Clear the log display"""
        # ... existing code ...
        pass
    
    def export_log(self):
        """Export log to a file"""
        # ... existing code ...
        pass
    
    # Fix: These methods were previously defined outside the class
    def reset_config(self):
        """Reset configuration to default values"""
        confirm = messagebox.askyesno(
            "Reset Configuration",
            "Are you sure you want to reset the configuration to default values?\n\nThis will overwrite your current settings."
        )
        
        if not confirm:
            return
            
        try:
            # Check for example config
            example_path = "config.example.json"
            
            if not os.path.exists(example_path):
                messagebox.showerror("Error", "Example configuration file not found.")
                return
            
            # Load example config
            with open(example_path, 'r') as f:
                default_config = json.load(f)
                
            # Keep API keys from current config if they exist
            if self.config and "exchange" in self.config:
                api_key = self.config["exchange"].get("api_key", "")
                api_secret = self.config["exchange"].get("api_secret", "")
                
                if api_key and api_secret:
                    default_config["exchange"]["api_key"] = api_key
                    default_config["exchange"]["api_secret"] = api_secret
            
            # Backup current config
            if os.path.exists("config.json"):
                backup_name = f"config.backup.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                shutil.copy("config.json", backup_name)
                self.add_activity(f"Configuration backed up to {backup_name}")
            
            # Save default config
            with open("config.json", 'w') as f:
                json.dump(default_config, f, indent=2)
            
            # Update our config
            self.config = default_config
            
            # Update UI
            self.load_config()  # Reload config to UI
            
            self.info_label.config(text="Configuration reset to default values")
            messagebox.showinfo("Reset Complete", "Configuration has been reset to default values.\n\nAny existing API keys were preserved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset configuration: {str(e)}")
            self.info_label.config(text="Error resetting configuration")

    def validate_config(self):
        """Validate the current configuration"""
        self.diagnostic_text.delete(1.0, tk.END)
        self.diagnostic_text.insert(tk.END, "Validating configuration...\n\n")
        
        issues = []
        warnings = []
        
        try:
            # Check if config exists
            if not self.config:
                issues.append("Configuration is empty or not loaded")
                
            else:
                # Check exchange section
                if "exchange" not in self.config:
                    issues.append("Missing 'exchange' section")
                else:
                    exchange = self.config["exchange"]
                    
                    # Check exchange name
                    if "name" not in exchange:
                        issues.append("Missing exchange name")
                    elif exchange["name"] != "mexc":
                        warnings.append(f"Exchange is set to '{exchange['name']}', but only 'mexc' is fully supported")
                    
                    # Check API keys
                    if "api_key" not in exchange or not exchange["api_key"]:
                        issues.append("API key is missing")
                    elif exchange["api_key"] == "YOUR_MEXC_API_KEY_HERE":
                        issues.append("Default API key needs to be replaced with your actual API key")
                        
                    if "api_secret" not in exchange or not exchange["api_secret"]:
                        issues.append("API secret is missing")
                    elif exchange["api_secret"] == "YOUR_MEXC_API_SECRET_HERE":
                        issues.append("Default API secret needs to be replaced with your actual API secret")
                
                # Check trading section
                if "trading" not in self.config:
                    issues.append("Missing 'trading' section")
                else:
                    trading = self.config["trading"]
                    
                    # Check trading pair
                    if "base_symbol" not in trading or not trading["base_symbol"]:
                        issues.append("Missing base symbol (e.g., PI)")
                    if "quote_symbol" not in trading or not trading["quote_symbol"]:
                        issues.append("Missing quote symbol (e.g., USDT)")
                    
                    # Check trade amount
                    if "trade_amount" not in trading:
                        issues.append("Missing trade amount")
                    elif trading["trade_amount"] <= 0:
                        issues.append("Trade amount must be greater than zero")
                    elif trading["trade_amount"] > 100:
                        warnings.append(f"Trade amount is set to {trading['trade_amount']}, which is quite high. Consider reducing it.")
                
                # Check strategies section
                if "strategies" not in self.config:
                    issues.append("Missing 'strategies' section")
                elif "active_strategy" not in self.config["strategies"]:
                    issues.append("No active strategy defined")
                else:
                    active = self.config["strategies"]["active_strategy"]
                    if active not in self.config["strategies"]:
                        issues.append(f"Active strategy '{active}' is not defined in strategies")
                    elif not self.config["strategies"][active].get("enabled", False):
                        warnings.append(f"Active strategy '{active}' is not enabled")
            
            # Display validation results
            if not issues and not warnings:
                self.diagnostic_text.insert(tk.END, "✅ Configuration is valid!\n\n")
                self.diagnostic_text.insert(tk.END, "No issues found in your configuration.\n")
                
                # Show some config details
                if self.config:
                    self.diagnostic_text.insert(tk.END, "\nConfiguration Summary:\n")
                    self.diagnostic_text.insert(tk.END, "────────────────────\n")
                    
                    if "exchange" in self.config:
                        self.diagnostic_text.insert(tk.END, f"Exchange: {self.config['exchange'].get('name', 'unknown')}\n")
                        self.diagnostic_text.insert(tk.END, f"API Key: {'✓ Configured' if self.config['exchange'].get('api_key') else '❌ Missing'}\n")
                    
                    if "trading" in self.config:
                        trading = self.config["trading"]
                        self.diagnostic_text.insert(tk.END, f"Trading Pair: {trading.get('base_symbol', '?')}/{trading.get('quote_symbol', '?')}\n")
                        self.diagnostic_text.insert(tk.END, f"Trade Amount: {trading.get('trade_amount', '?')} {trading.get('quote_symbol', '')}\n")
                        self.diagnostic_text.insert(tk.END, f"Auto Trade: {'Enabled' if trading.get('auto_trade', False) else 'Disabled'}\n")
                    
                    if "strategies" in self.config:
                        strategies = self.config["strategies"]
                        self.diagnostic_text.insert(tk.END, f"Active Strategy: {strategies.get('active_strategy', '?')}\n")
                
                self.info_label.config(text="Configuration validated successfully")
                
            else:
                if issues:
                    self.diagnostic_text.insert(tk.END, "❌ Configuration has issues:\n\n")
                    for i, issue in enumerate(issues, 1):
                        self.diagnostic_text.insert(tk.END, f"{i}. {issue}\n")
                    self.diagnostic_text.insert(tk.END, "\n")
                
                if warnings:
                    self.diagnostic_text.insert(tk.END, "⚠️ Warnings:\n\n")
                    for i, warning in enumerate(warnings, 1):
                        self.diagnostic_text.insert(tk.END, f"{i}. {warning}\n")
                
                self.info_label.config(text=f"Configuration has {len(issues)} issues, {len(warnings)} warnings")
            
                # Switch to Health tab to show the results
                self.notebook.select(4)  # Index of Health tab
        
        except Exception as e:
            self.diagnostic_text.insert(tk.END, f"Error validating configuration: {str(e)}")
            self.info_label.config(text="Error validating configuration")

    # Include all other methods from remaining_methods.py, missing_methods.py, and final_methods.py
    def edit_config_file(self):
        """Open the config.json file in a text editor"""
        # ... existing code from missing_methods.py ...
        pass

    def import_config(self):
        """Import configuration from a file"""
        # ... existing code from missing_methods.py ...
        pass

    def export_config(self):
        """Export configuration to a file"""
        # ... existing code from missing_methods.py ...
        pass

    def create_package(self):
        """Create a distribution package"""
        # ... existing code from missing_methods.py ...
        pass

    def create_shortcut(self):
        """Create a desktop shortcut"""
        # ... existing code from missing_methods.py ...
        pass

    def export_all_logs(self):
        """Export all logs to a zip file"""
        # ... existing code from missing_methods.py ...
        pass

    def refresh_processes(self):
        """Refresh the list of running BROski processes"""
        # ... existing code from missing_methods.py ...
        pass

    def kill_selected_process(self):
        """Kill the selected process"""
        # ... existing code from missing_methods.py ...
        pass

    def kill_all_processes(self):
        """Kill all BROski processes"""
        # ... existing code from missing_methods.py ...
        pass

    def refresh_backup_list(self):
        """Refresh the list of backups"""
        # ... existing code from missing_methods.py ...
        pass

    def quick_backup(self):
        """Perform a quick backup"""
        # Already implemented in the existing code
        self.backup_bot()

    def custom_backup(self):
        """Perform a custom backup"""
        # ... existing code from BROski_Control_Center_completion.py ...
        pass

    def restore_from_backup(self):
        """Restore from a backup directory"""
        # ... existing code from remaining_methods.py ...
        pass

    def schedule_backups(self):
        """Schedule automatic backups"""
        # ... existing code from remaining_methods.py ...
        pass

    def run_health_check(self):
        """Run a complete health check on the system"""
        # ... existing code from remaining_methods.py ...
        pass

    def check_api_connection(self):
        """Check the connection to the exchange API"""
        # ... existing code from remaining_methods.py ...
        pass

    def verify_dependencies(self):
        """Verify that all required dependencies are installed"""
        # ... existing code from remaining_methods.py ...
        pass

    def show_system_info(self):
        """Show system information in diagnostic output"""
        # ... existing code from final_methods.py ...
        pass

    def check_internet(self):
        """Check internet connectivity"""
        # ... existing code from final_methods.py ...
        pass

    def check_disk_space(self):
        """Check available disk space"""
        # ... existing code from final_methods.py ...
        pass
        
    def generate_system_report(self):
        """Generate a comprehensive system report"""
        # ... existing code from final_methods.py ...
        pass

    # Main function to run the application
    def run(self):
        """Start the control center"""
        self.root.mainloop()

# Create and run the application if executed directly
if __name__ == "__main__":
    app = BROskiControlCenter()
    app.run()
