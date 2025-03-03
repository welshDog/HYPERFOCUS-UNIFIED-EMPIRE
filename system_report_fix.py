# This fixes the generate_system_report method by completing the strategies section
# Replace the incomplete strategies section in generate_system_report with this:
import tkinter as tk
import psutil

class SystemReport:
    def __init__(self):
        self.diagnostic_text = None
        
    def setup_ui(self):
        """Initialize the UI elements"""
        root = tk.Tk()
        self.diagnostic_text = tk.Text(root)
        self.diagnostic_text.pack()
        return root
        
    def generate_system_report(self, report):
        """Generate a report with strategy information"""
        # (Inside the Configuration section, after displaying API Key)
        if "strategies" in report["config"]:
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
        import platform
        import sys
        
        system_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "os": platform.system(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",
            "memory_available": f"{round(psutil.virtual_memory().available / (1024.0 ** 3), 2)} GB",
        }
        
        return system_info

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
    info = report.generate_report()
    print(info)
