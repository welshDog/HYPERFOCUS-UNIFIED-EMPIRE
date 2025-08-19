"""
Fixed emergency kill script to handle missing dependencies and work in reorganized structure
"""

def install_missing_dependencies():
    """Install missing dependencies needed for emergency kill"""
    import subprocess
    import sys
    
    required_packages = ["psutil", "colorama", "ccxt"]
    missing_packages = []
    
    # Check for missing packages
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"Installing required packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("Installation complete!")
            # Re-import colorama and initialize
            import colorama
            colorama.init()
            return True
        except:
            print("Failed to install required packages.")
            print("Please run: pip install psutil colorama ccxt")
            return False
    
    return True

def fix_emergency_kill():
    """
    Fixes the emergency_kill.py module.
    Apply this at the top of the file.
    """
    # Add this at the top of emergency_kill.py right after imports
    
    # Ensure all required packages are installed
    if not install_missing_dependencies():
        print("Cannot continue - missing required packages.")
        sys.exit(1)
    
    # Add directory navigation for reorganized structure
    import sys
    from pathlib import Path

    # Get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # Add parent directory to path to handle reorganization
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
