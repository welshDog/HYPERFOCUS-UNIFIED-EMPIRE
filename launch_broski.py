import os
import sys
import platform
import subprocess
import time

def check_environment():
    """Check if the environment is ready to run BROski"""
    print("⚙️ Checking environment...")
    
    # Check Python version
    python_version = platform.python_version_tuple()
    major, minor = int(python_version[0]), int(python_version[1])
    if major < 3 or (major == 3 and minor < 8):
        print(f"❌ Python version {major}.{minor} is too old. BROski requires Python 3.8+")
        return False
    else:
        print(f"✓ Python version: {major}.{minor}")
    
    # Check for config file
    if not os.path.exists("config.json"):
        print("❌ config.json not found. Please run master_install.py first")
        return False
    else:
        print("✓ Config file found")
    
    # Check for required directories
    required_dirs = ["logs", "backups", "data"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created missing directory: {directory}")
        else:
            print(f"✓ Directory found: {directory}")
    
    # Check if main script exists
    if not os.path.exists("BROski_Control_Center.py"):
        print("❌ BROski_Control_Center.py not found. Please reinstall BROski")
        return False
    else:
        print("✓ Main application script found")
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n⚙️ Checking dependencies...")
    required_packages = ["ccxt", "pandas", "matplotlib", "colorama", "requests", "numpy"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing.append(package)
    
    if missing:
        try:
            print(f"\n📦 Installing missing packages: {', '.join(missing)}")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✓ All dependencies installed")
        except:
            print("❌ Failed to install dependencies. Please run master_install.py")
            return False
    
    return True

def start_broski():
    """Start the BROski Control Center"""
    if not check_environment():
        print("\n❌ Environment check failed. Please fix issues before starting BROski.")
        input("Press Enter to exit...")
        return
    
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please fix issues before starting BROski.")
        input("Press Enter to exit...")
        return
    
    print("\n🚀 Starting BROski Control Center...")
    try:
        # Use subprocess to start BROski in a separate process
        subprocess.Popen([sys.executable, "BROski_Control_Center.py"])
        print("✓ BROski Control Center launched successfully!")
    except Exception as e:
        print(f"❌ Failed to start BROski: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    print("🤖 BROski Crypto Bot - Quick Launch")
    print("=====================================")
    
    try:
        start_broski()
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        input("Press Enter to exit...")
