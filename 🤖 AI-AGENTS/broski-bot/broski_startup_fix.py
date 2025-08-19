import os
import sys
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import time
import traceback
import shutil

class BROskiControlCenter:
    def __init__(self, root):
        self.root = root
        self.fix_initialization()
        sys.excepthook = lambda *args: self.exception_handler(*args)

    def fix_initialization(self):
        """
        Add this method to the __init__ method of BROskiControlCenter
        to ensure all required attributes are initialized properly.
        """
        # Initialize basic attributes
        self.config = {}
        self.logs_directory = "logs"
        self.logs_queue = []
        self.strategy = None
        self.running = False
        self.activity_log = []
        self.status_var = tk.StringVar(value="Ready")
        self.last_update_time = None
        
        # Create required directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        
        # Make sure the UI elements are initialized
        # This avoids "attribute does not exist" errors
        if not hasattr(self, "info_label"):
            self.info_label = ttk.Label(self.root, text="Ready")
        
        if not hasattr(self, "diagnostic_text"):
            self.diagnostic_text = tk.Text(self.root, height=10, width=50)
        
        # Load config safely
        try:
            self.load_config()
        except Exception as e:
            print(f"Error loading configuration: {e}")
            # Create minimal default config
            self.config = {
                "exchange": {"name": "mexc"},
                "trading": {"base_symbol": "BTC", "quote_symbol": "USDT"},
                "strategies": {"active_strategy": "rsi"}
            }

    def load_config(self):
        """Load configuration from config.json"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r') as f:
                    self.config = json.load(f)
                self.info_label.config(text="Configuration loaded")
            else:
                self.info_label.config(text="No configuration file found")
                
                # Create default config
                self.config = {
                    "exchange": {
                        "name": "mexc",
                        "api_key": "",
                        "api_secret": ""
                    },
                    "trading": {
                        "base_symbol": "BTC", 
                        "quote_symbol": "USDT",
                        "auto_trade": False
                    },
                    "strategies": {
                        "active_strategy": "rsi",
                        "rsi": {
                            "enabled": True,
                            "period": 14,
                            "overbought": 70,
                            "oversold": 30
                        }
                    }
                }
        except Exception as e:
            self.info_label.config(text=f"Error loading configuration: {str(e)}")
            messagebox.showerror("Configuration Error", f"Failed to load configuration: {str(e)}")

    def save_config(self):
        """Save configuration to config.json"""
        try:
            # First create a backup of the existing config
            if os.path.exists("config.json"):
                backup_name = f"config.backup.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                try:
                    with open("config.json", 'r') as src, open(backup_name, 'w') as dst:
                        dst.write(src.read())
                    self.add_activity(f"Configuration backed up to {backup_name}")
                except:
                    pass  # Silently continue if backup fails
                    
            # Now save the current configuration
            with open("config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
                
            self.info_label.config(text="Configuration saved successfully")
        except Exception as e:
            self.info_label.config(text=f"Error saving configuration: {str(e)}")
            messagebox.showerror("Save Error", f"Failed to save configuration: {str(e)}")

    def add_activity(self, message):
        """Add a message to the activity log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.activity_log.append(f"[{timestamp}] {message}")
        
        # Keep only the last 100 messages
        if len(self.activity_log) > 100:
            self.activity_log = self.activity_log[-100:]
        
        # Update activity log display if it exists
        try:
            if hasattr(self, "activity_text") and isinstance(self.activity_text, tk.Text):
                self.activity_text.config(state=tk.NORMAL)
                self.activity_text.delete(1.0, tk.END)
                for activity in self.activity_log:
                    self.activity_text.insert(tk.END, activity + "\n")
                self.activity_text.see(tk.END)
                self.activity_text.config(state=tk.DISABLED)
        except:
            pass  # Silently ignore if we can't update the activity display

    def refresh_backup_list(self):
        """Refresh the list of backups"""
        # This is an empty implementation to prevent errors
        # if this method is called but not fully implemented
        pass

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

    def exception_handler(self, exc_type, exc_value, exc_traceback):
        """
        Global exception handler for unhandled exceptions.
        Add this to your __init__ method as follows:
        
        sys.excepthook = lambda *args: self.exception_handler(*args)
        """
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # Log to file
        try:
            os.makedirs("logs", exist_ok=True)
            log_file = os.path.join("logs", "error.log")
            with open(log_file, "a") as f:
                f.write(f"\n[{datetime.datetime.now()}] Unhandled Exception:\n")
                f.write(error_msg)
                f.write("\n" + "-"*50 + "\n")
        except:
            pass  # If we can't log to file, continue to show dialog
        
        # Display error message
        try:
            messagebox.showerror("BROski Error", 
                               f"An unexpected error occurred:\n\n{str(exc_value)}\n\n"
                               f"Please check error.log for details.")
        except:
            # If we can't show a dialog (maybe Tk is not initialized),
            # print to console
            print("=" * 60)
            print("CRITICAL ERROR:")
            print(error_msg)
            print("=" * 60)
