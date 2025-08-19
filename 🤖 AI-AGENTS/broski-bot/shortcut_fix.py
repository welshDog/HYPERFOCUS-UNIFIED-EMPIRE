"""
This contains a modified version of the create_shortcut function that handles
the case where win32com is not available.
"""

import os
import sys

def print_header(title, width=50, char='='):
    """
    Print a formatted header with the given title
    
    Args:
        title (str): The header text to display
        width (int): Total width of the header
        char (str): Character to use for the border
    """
    padding = width - len(title) - 2  # -2 for spaces on both sides
    left_padding = padding // 2
    right_padding = padding - left_padding
    
    print("\n" + char * width)
    print(char * left_padding + " " + title + " " + char * right_padding)
    print(char * width + "\n")

def print_warning(message, use_colors=True):
    """
    Print a formatted warning message to the console
    
    Args:
        message (str): The warning message to display
        use_colors (bool): Whether to use colored output (default: True)
    """
    try:
        if use_colors:
            # Yellow text for warnings
            print(f"\033[93m⚠️ WARNING: {message}\033[0m")
        else:
            print(f"WARNING: {message}")
    except UnicodeEncodeError:
        # Fallback if terminal doesn't support emojis
        print(f"WARNING: {message}")

def print_success(message, use_colors=True):
    """
    Print a formatted success message to the console
    
    Args:
        message (str): The success message to display
        use_colors (bool): Whether to use colored output (default: True)
    """
    try:
        if use_colors:
            # Green text for success
            print(f"\033[92m✅ SUCCESS: {message}\033[0m")
        else:
            print(f"SUCCESS: {message}")
    except UnicodeEncodeError:
        # Fallback if terminal doesn't support emojis
        print(f"SUCCESS: {message}")

def print_error(message, use_colors=True):
    """
    Print a formatted error message to the console
    
    Args:
        message (str): The error message to display
        use_colors (bool): Whether to use colored output (default: True)
    """
    try:
        if use_colors:
            # Red text for errors
            print(f"\033[91m❌ ERROR: {message}\033[0m")
        else:
            print(f"ERROR: {message}")
    except UnicodeEncodeError:
        # Fallback if terminal doesn't support emojis
        print(f"ERROR: {message}")

def create_shortcut_modified():
    """Create a desktop shortcut for BROski."""
    print_header("Creating BROski desktop shortcut...")
    
    try:
        # Try importing win32com
        try:
            import winshell
            from win32com.client import Dispatch
            win32_available = True
        except ImportError:
            print_warning("Required modules not installed for Windows shortcuts.")
            print("To create shortcuts, run: pip install pywin32 winshell")
            win32_available = False
            
        if not win32_available:
            # Create a batch file alternative if win32com is not available
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            batch_path = os.path.join(desktop_path, "BROski Bot.bat")
            
            with open(batch_path, "w") as f:
                f.write("@echo off\n")
                f.write(f"cd /d \"{os.getcwd()}\"\n")
                f.write(f"\"{sys.executable}\" unified_launcher.py\n")
                
            print_success("Created batch file shortcut instead")
            return
        
        # Standard shortcut creation with win32com
        desktop = winshell.desktop()
        path = os.path.join(desktop, "BROski Bot.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = os.path.abspath(__file__)
        shortcut.WorkingDirectory = os.getcwd()
        if os.path.exists("favicon.ico"):
            shortcut.IconLocation = os.path.abspath("favicon.ico")
        shortcut.save()
        
        print_success("Shortcut created successfully on desktop!")
        
    except Exception as e:
        print_error(f"Error creating shortcut: {e}")
        
    input("Press Enter to continue...")
