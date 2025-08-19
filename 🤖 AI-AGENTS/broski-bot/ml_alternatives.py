import os
import json
import sys
from pathlib import Path
import platform

def display_header(message):
    """Display a formatted header message"""
    print("\n" + "=" * 60)
    print(message.center(60))
    print("=" * 60 + "\n")

def check_system_compatibility():
    """Check if system is compatible with TensorFlow"""
    system_info = {}
    
    # Check Python version
    python_version = platform.python_version()
    system_info['python_version'] = python_version
    
    # Check OS and architecture
    system = platform.system()
    architecture = platform.architecture()[0]
    machine = platform.machine()
    system_info['os'] = system
    system_info['architecture'] = architecture
    system_info['machine'] = machine
    
    # Check if pip is available
    try:
        import pip
        system_info['pip_version'] = pip.__version__
    except ImportError:
        system_info['pip_version'] = "Not found"
    
    return system_info

def check_ml_dependencies():
    """Check which ML libraries are installed"""
    ml_libraries = {}
    
    try:
        import tensorflow # type: ignore
        ml_libraries['tensorflow'] = tensorflow.__version__
    except ImportError:
        ml_libraries['tensorflow'] = "Not installed"
        
    try:
        import sklearn
        ml_libraries['scikit-learn'] = sklearn.__version__
    except ImportError:
        ml_libraries['scikit-learn'] = "Not installed"
        
    try:
        import numpy
        ml_libraries['numpy'] = numpy.__version__
    except ImportError:
        ml_libraries['numpy'] = "Not installed"
        
    try:
        import pandas
        ml_libraries['pandas'] = pandas.__version__
    except ImportError:
        ml_libraries['pandas'] = "Not installed"
        
    return ml_libraries

def enable_fallback_strategy():
    """Enable a fallback strategy in the config"""
    config_path = Path("config.json")
    
    if not config_path.exists():
        print("❌ Cannot find config.json. Please run setup.py first.")
        return False
        
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Check if ML strategy is active
    if config["strategies"]["active_strategy"] == "ml_strategy":
        print("📊 ML strategy is currently active. Switching to RSI strategy...")
        config["strategies"]["active_strategy"] = "rsi_strategy"
        config["strategies"]["rsi_strategy"]["enabled"] = True
        config["strategies"]["ml_strategy"]["enabled"] = False
        
        # Save changes
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✅ Successfully switched to RSI strategy as fallback")
        return True
    else:
        print("ℹ️ ML strategy is not active. No changes needed.")
        return True

def provide_tensorflow_alternatives():
    """Provide alternative installation methods for TensorFlow"""
    system_info = check_system_compatibility()
    
    display_header("TensorFlow Installation Solutions")
    
    print("Your system information:")
    print(f"• Python version: {system_info['python_version']}")
    print(f"• Operating system: {system_info['os']}")
    print(f"• Architecture: {system_info['architecture']} ({system_info['machine']})")
    print(f"• pip version: {system_info['pip_version']}")
    
    print("\n1️⃣ Try TensorFlow CPU-only version:")
    print("   pip install tensorflow-cpu")
    
    if system_info['os'] == 'Windows':
        print("\n2️⃣ For Windows, you might need Visual C++ redistributable:")
        print("   Download from: https://aka.ms/vs/16/release/vc_redist.x64.exe")
    
    if system_info['os'] == 'Linux':
        print("\n2️⃣ For Linux, try using conda instead of pip:")
        print("   conda install tensorflow")
        
    print("\n3️⃣ Check Python compatibility (TensorFlow supports Python 3.7-3.11):")
    python_major = int(system_info['python_version'].split('.')[0])
    python_minor = int(system_info['python_version'].split('.')[1])
    
    if python_major < 3 or (python_major == 3 and python_minor < 7):
        print("   ❌ Your Python version is too old for TensorFlow")
        print("   ℹ️ Consider upgrading to Python 3.7-3.11")
    elif python_major == 3 and python_minor > 11:
        print("   ❌ Your Python version is too new for TensorFlow")
        print("   ℹ️ Consider installing Python 3.11 instead")
    else:
        print("   ✅ Your Python version is compatible with TensorFlow")
    
    display_header("Using BROski Without ML")
    
    print("You can still use BROski without TensorFlow by using alternative strategies:")
    print("• RSI Strategy - Based on Relative Strength Index")
    print("• MACD Strategy - Moving Average Convergence/Divergence")
    print("\nTo switch to non-ML strategies:")
    print("1. Run setup.py and select RSI or MACD when prompted")
    print("2. Or manually edit config.json to set active_strategy")
    print("\nWould you like to automatically switch to the RSI strategy now?")
    
    choice = input("Switch to RSI strategy? (y/n): ").lower()
    if choice == 'y':
        enable_fallback_strategy()

if __name__ == "__main__":
    display_header("BROski ML Alternatives")
    
    print("This script helps you use BROski without TensorFlow/ML capabilities")
    print("Checking your system and installed ML libraries...")
    
    ml_libs = check_ml_dependencies()
    
    print("\nML Library Status:")
    for lib, version in ml_libs.items():
        status = "✅ Installed" if "Not" not in version else "❌ Not installed"
        print(f"• {lib}: {status} ({version})")
    
    if ml_libs['tensorflow'] == "Not installed":
        provide_tensorflow_alternatives()
    else:
        print("\n✅ TensorFlow is already installed!")
        print("You can use the ML strategy without issues.")
