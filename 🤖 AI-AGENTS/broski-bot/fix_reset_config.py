import os
import json
from tkinter import messagebox
from datetime import datetime
# or
import datetime
import shutil

# Add this method to your BROskiControlCenter class in BROski_Control_Center.py

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

# Show an information message
messagebox.showinfo("Title", "This is an info message")

# Ask user a yes/no question
result = messagebox.askyesno("Confirm", "Do you want to proceed?")
if result:
    print("User clicked Yes")
else:
    print("User clicked No")

# Check if file exists
if os.path.exists("config.json"):
    print("Config file found")

# Create directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Join paths (works on all operating systems)
config_path = os.path.join("settings", "config.json")
