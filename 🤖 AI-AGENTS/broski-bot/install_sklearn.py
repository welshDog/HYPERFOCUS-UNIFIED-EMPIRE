"""
Helper script to install scikit-learn package for strategy optimization
"""

import os
import sys
import subprocess

def install_sklearn():
    """Install scikit-learn package"""
    print("Installing scikit-learn package...")
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    
    if in_venv:
        # In virtual environment, use the venv's pip
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(sys.prefix, "Scripts", "pip.exe")
        else:
            pip_path = os.path.join(sys.prefix, "bin", "pip")
        
        if not os.path.exists(pip_path):
            pip_path = "pip"  # Fallback to system pip
    else:
        pip_path = "pip"  # Use system pip
    
    # Install the package
    try:
        subprocess.check_call([pip_path, "install", "scikit-learn"])
        print("✅ scikit-learn installed successfully!")
        return True, pip_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing scikit-learn: {e}")
        return False, pip_path

if __name__ == "__main__":
    success, pip_path = install_sklearn()
    
    print("\nAdditional packages for machine learning and data analysis:")
    install_more = input("Would you like to install additional ML packages? (y/n): ").lower()
    
    if install_more == 'y':
        try:
            subprocess.check_call([pip_path, "install", "numpy", "pandas", "matplotlib"])
            print("✅ Additional packages installed successfully!")
        except Exception as e:
            print(f"❌ Error installing additional packages: {e}")
    
    print("\nRestart your IDE/editor for changes to take effect.")
