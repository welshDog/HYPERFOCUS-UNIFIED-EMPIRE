"""
Installs the pywin32 package required for desktop shortcut creation.
This will fix the 'Import "win32com.client" could not be resolved from source' error
in the unified_launcher.py file.
"""

import os
import sys
import subprocess
import importlib.util

def is_installed(package_name):
    """Check if a package is installed"""
    return importlib.util.find_spec(package_name) is not None

def install_package():
    print("Installing pywin32 package...")
    
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
        subprocess.check_call([pip_path, "install", "pywin32"])
        print("✅ pywin32 installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing pywin32: {e}")
        return False

def alternative_solution():
    """Provide alternative solution if installation fails"""
    print("\nAlternative Solution:")
    print("1. Open a command prompt with admin privileges")
    print("2. Run: pip install pywin32")
    print("3. If still facing issues, try: pip install pywin32==303")  # Specific version that's known to be stable

if __name__ == "__main__":
    if is_installed("win32com"):
        print("✅ pywin32 is already installed!")
    else:
        success = install_package()
        if not success:
            alternative_solution()
    
    print("\nAfter installation, restart your IDE/editor for changes to take effect.")
    input("Press Enter to exit...")
