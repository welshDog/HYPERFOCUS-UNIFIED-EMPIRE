#!/usr/bin/env python3
"""
Launch script for BROski Trade Results Window
"""
import os
import sys
import tkinter as tk
from trade_results_window import TradeResultsWindow

def main():
    """Run the trade results window"""
    # Check if trade history file exists
    trade_history_file = os.path.join("logs", "trade_history.json")
    if not os.path.exists(trade_history_file):
        print(f"Trade history file not found: {trade_history_file}")
        print("Please run the bot first to generate trading data.")
        input("Press Enter to continue...")
        return
    
    # Create tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Set application title and icon
    root.title("BROski Trade Results")
    try:
        root.iconbitmap("favicon.ico")
    except:
        pass  # Icon not found, use default
    
    # Launch the trade results window
    try:
        app = TradeResultsWindow(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Error launching trade results window: {e}")
        traceback.print_exc()
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
