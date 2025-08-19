# Add this at the top of your script to help diagnose and fix import issues

import sys
import os
import importlib.util

def fix_imports():
    """Fix common import issues and print diagnostic information"""
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    print("Current working directory:", os.getcwd())
    print("Python path:", sys.path)
    
    # Try to ensure necessary paths are in sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        print(f"Adding current directory to path: {current_dir}")
        sys.path.insert(0, current_dir)
        
    # Check for commonly used modules
    modules_to_check = ["time", "datetime", "json", "tkinter", "ccxt"]
    for module_name in modules_to_check:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ {module_name} found at: {module.__file__}")
        except ImportError:
            print(f"❌ {module_name} not found")
    
    return True

if __name__ == "__main__":
    fix_imports()
