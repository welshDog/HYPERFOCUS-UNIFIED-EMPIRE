"""
Quick fix for scikit-learn import error in strategy_optimizer.py
"""
import subprocess
import importlib.util
import sys
import os

def is_installed(package):
    """Check if package is installed"""
    return importlib.util.find_spec(package) is not None

def main():
    print("Fixing scikit-learn import error...")
    
    # Check if scikit-learn is installed
    if is_installed("sklearn"):
        print("✅ scikit-learn is already installed!")
        print("The error might be related to VS Code's Pylance not finding the package.")
        print("Try restarting VS Code or refreshing the Python environment.")
        return
    
    # Install scikit-learn
    print("Installing scikit-learn...")
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    
    # Get the right pip command
    if in_venv:
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(sys.prefix, "Scripts", "pip.exe")
        else:
            pip_path = os.path.join(sys.prefix, "bin", "pip")
            
        if not os.path.exists(pip_path):
            pip_path = "pip"
    else:
        pip_path = "pip"
    
    # Run the install command
    try:
        subprocess.run([pip_path, "install", "scikit-learn"], check=True)
        print("✅ scikit-learn installed successfully!")
        
        # Check if we can import it now
        if is_installed("sklearn"):
            print("✅ Import verified!")
        else:
            print("❌ Installation seemed to work but module still not found.")
            print("You may need to restart your Python environment or IDE.")
    except Exception as e:
        print(f"❌ Error installing scikit-learn: {e}")
        print("\nManual installation instructions:")
        print("1. Open a command prompt or terminal")
        print("2. Run: pip install scikit-learn")
    
    print("\nAfter installation:")
    print("1. Close and reopen VS Code")
    print("2. Or reload the Python Interpreter (Ctrl+Shift+P → Python: Select Interpreter)")

if __name__ == "__main__":
    main()
