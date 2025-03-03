# Add this code to your generate_system_report method to fix the missing strategy section
import tkinter as tk

def add_strategy_report(self, report):
    """Add detailed strategy information to the system report"""
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
