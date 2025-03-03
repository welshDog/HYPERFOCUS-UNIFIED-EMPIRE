"""
Fixed implementation of SystemReport class.
This version adds proper initialization and imports.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import time

# Ensure psutil is installed
try:
    import psutil
except ImportError:
    print("Installing psutil...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

class SystemReport:
    def __init__(self, root=None):
        """Initialize the SystemReport class"""
        self.diagnostic_text = None
        
        if root is None:
            self.root = tk.Tk()
            self.root.title("BROski System Report")
            self.root.geometry("800x600")
            self.setup_ui()
        else:
            self.root = root
            # Create diagnostic_text if it doesn't exist
            if not hasattr(self, "diagnostic_text") or self.diagnostic_text is None:
                self.diagnostic_text = tk.Text(self.root)
                self.diagnostic_text.pack(fill="both", expand=True)
    
    def setup_ui(self):
        """Initialize the UI elements"""
        if self.diagnostic_text is None:
            self.diagnostic_text = tk.Text(self.root, wrap=tk.WORD, padx=10, pady=10)
            self.diagnostic_text.pack(fill="both", expand=True)
        
        # Add a button to generate report
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        generate_btn = tk.Button(button_frame, text="Generate Report", command=self.generate_report)
        generate_btn.pack(side="left", padx=5)
        
        quit_btn = tk.Button(button_frame, text="Quit", command=self.root.destroy)
        quit_btn.pack(side="left", padx=5)
        
        return self.root
        
    def generate_system_report(self, report):
        """Generate a report with strategy information"""
        if self.diagnostic_text is None:
            print("Error: diagnostic_text not initialized")
            return
            
        # (Inside the Configuration section, after displaying API Key)
        if "strategies" in report.get("config", {}):
            strategies = report["config"]["strategies"]
            active_strategy = strategies.get('active_strategy', '?')
            self.diagnostic_text.insert(tk.END, f"Active Strategy: {active_strategy}\n\n")
            
            # Show all available strategies
            self.diagnostic_text.insert(tk.END, "Available Strategies:\n")
            for strategy_name, strategy_config in strategies.items():
                if strategy_name != "active_strategy":
                    # If this is the active strategy, mark it
                    if strategy_name == active_strategy:
                        status = "✓ ACTIVE"
                    elif strategy_config.get("enabled", False):
                        status = "ENABLED"
                    else:
                        status = "DISABLED"
                    
                    self.diagnostic_text.insert(tk.END, f"- {strategy_name} [{status}]\n")
            
            # Show detailed parameters for active strategy
            if active_strategy in strategies and active_strategy != "active_strategy":
                active_config = strategies[active_strategy]
                self.diagnostic_text.insert(tk.END, f"\nActive Strategy Parameters ({active_strategy}):\n")
                
                # Display all parameters for active strategy
                for param, value in active_config.items():
                    if param != "enabled":  # Skip the enabled flag, already shown above
                        self.diagnostic_text.insert(tk.END, f"  • {param}: {value}\n")
        else:
            self.diagnostic_text.insert(tk.END, "No strategy configuration found.\n")
    
    def generate_report(self):
        """Generate system information report"""
        try:
            import platform
            
            # Clear the text area
            if self.diagnostic_text:
                self.diagnostic_text.delete(1.0, tk.END)
                self.diagnostic_text.insert(tk.END, "Generating System Report...\n\n")
                self.diagnostic_text.update()
            
            # Get system information
            system_info = {
                "python_version": sys.version,
                "platform": platform.platform(),
                "os": platform.system(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",
                "memory_available": f"{round(psutil.virtual_memory().available / (1024.0 ** 3), 2)} GB",
            }
            
            # Display in text area
            if self.diagnostic_text:
                self.diagnostic_text.delete(1.0, tk.END)
                self.diagnostic_text.insert(tk.END, "System Report\n")
                self.diagnostic_text.insert(tk.END, "=============\n\n")
                
                for key, value in system_info.items():
                    self.diagnostic_text.insert(tk.END, f"{key}: {value}\n")
                
                # Add disk information
                disk_info = get_system_info()
                self.diagnostic_text.insert(tk.END, "\nDisk Information\n")
                self.diagnostic_text.insert(tk.END, "===============\n")
                for key, value in disk_info.items():
                    self.diagnostic_text.insert(tk.END, f"{key}: {value}\n")
                
                # Try to add config and strategy information
                try:
                    self.diagnostic_text.insert(tk.END, "\nChecking for configuration file...\n")
                    
                    if os.path.exists("config.json"):
                        import json
                        with open("config.json", "r") as f:
                            config = json.load(f)
                        
                        report = {"config": config}
                        self.diagnostic_text.insert(tk.END, "Configuration found. Generating strategy report...\n\n")
                        self.generate_system_report(report)
                    else:
                        self.diagnostic_text.insert(tk.END, "No configuration file found.\n")
                except Exception as e:
                    self.diagnostic_text.insert(tk.END, f"Error loading configuration: {str(e)}\n")
            
            return system_info
            
        except Exception as e:
            if self.diagnostic_text:
                self.diagnostic_text.insert(tk.END, f"Error generating report: {str(e)}\n")
            print(f"Error: {e}")
            return None

def get_system_info():
    # CPU information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    
    # Memory information
    memory = psutil.virtual_memory()
    memory_total = round(memory.total / (1024.0 ** 3), 2)  # GB
    memory_available = round(memory.available / (1024.0 ** 3), 2)  # GB
    
    # Disk information
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024.0 ** 3), 2)  # GB
    disk_free = round(disk.free / (1024.0 ** 3), 2)  # GB
    
    return {
        "cpu_percent": f"{cpu_percent}%",
        "cpu_count": cpu_count,
        "memory_total": f"{memory_total} GB",
        "memory_available": f"{memory_available} GB",
        "disk_total": f"{disk_total} GB",
        "disk_free": f"{disk_free} GB"
    }

# Example usage
if __name__ == "__main__":
    report = SystemReport()
    report.root.mainloop()
