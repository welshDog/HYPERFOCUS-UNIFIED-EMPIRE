import sys
import subprocess
import os
from pathlib import Path
import platform

def check_python_version():
    """Check if Python version is compatible"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("⚠️ Warning: This bot requires Python 3.7 or higher")
        print(f"Your version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    return True

def install_requirements():
    """Install required packages from requirements.txt"""
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    if not requirements_path.exists():
        print("Creating requirements.txt file...")
        with open(requirements_path, "w") as f:
            f.write("ccxt>=3.0.0\n")
            f.write("colorama>=0.4.4\n")
            f.write("requests>=2.25.1\n")
            f.write("pandas>=1.3.0\n")
            f.write("numpy>=1.20.0\n")
            f.write("matplotlib>=3.4.0\n")
            f.write("python-telegram-bot>=13.7\n")
            f.write("# Optional ML dependencies\n")
            f.write("# tensorflow>=2.7.0\n")
            f.write("# scikit-learn>=1.0.0\n")
    
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def install_ml_dependencies():
    """Install machine learning dependencies"""
    user_input = input("\nDo you want to install ML dependencies (TensorFlow, scikit-learn)? (y/n): ").lower()
    
    if user_input == 'y':
        print("\n📦 Installing ML dependencies (this may take a while)...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tensorflow>=2.7.0", "scikit-learn>=1.0.0"])
            print("✅ ML dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing ML dependencies: {e}")
            return False
    else:
        print("\nℹ️ Skipping ML dependencies. You can install them later if needed.")
        return True

def create_venv():
    """Create a virtual environment (optional)"""
    user_input = input("\nDo you want to create a virtual environment for the bot? (y/n): ").lower()
    
    if user_input == 'y':
        venv_path = Path(__file__).parent / "venv"
        
        if venv_path.exists():
            print(f"Virtual environment already exists at: {venv_path}")
            return True
            
        print("\n🔧 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
            
            # Determine activation command based on platform
            if platform.system() == "Windows":
                activate_script = venv_path / "Scripts" / "activate.bat"
                activate_cmd = f"{activate_script}"
            else:
                activate_script = venv_path / "bin" / "activate"
                activate_cmd = f"source {activate_script}"
                
            print("✅ Virtual environment created successfully!")
            print("\n📝 To activate the virtual environment, run:")
            print(f"   {activate_cmd}")
            print("\nAfter activation, install dependencies with:")
            print("   python install_dependencies.py")
            
            # Ask if the user wants to activate it now
            auto_activate = input("\nActivate virtual environment now? (y/n): ").lower()
            if auto_activate == 'y':
                if platform.system() == "Windows":
                    activate_and_install_script = venv_path / "Scripts" / "install_after_activate.bat"
                    with open(activate_and_install_script, "w") as f:
                        f.write(f"@echo off\n")
                        f.write(f"call {activate_script}\n")
                        f.write(f"python {__file__}\n")
                        f.write(f"cmd /k")
                    
                    os.startfile(activate_and_install_script)
                    print("✅ New terminal window opened with activated environment")
                    print("   Please continue installation there")
                    return False  # Stop this instance since a new one will be started
                else:
                    print("⚠️ Automatic activation is only supported on Windows.")
                    print(f"   Please manually run: {activate_cmd}")
                    return True
            
            return False  # Skip further installation as we need to activate first
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
            print("Continuing with global installation...")
            return True
    else:
        print("\nℹ️ Skipping virtual environment creation, using global Python environment.")
        return True

def main():
    print("🤖 BROski Crypto Bot - Dependency Installer 🤖")
    print("=============================================")

    # Check Python version
    if not check_python_version():
        input("Press Enter to continue anyway or Ctrl+C to exit...")

    # Create virtual environment if requested
    continue_install = create_venv()
    
    if continue_install:
        # Install basic dependencies
        if install_requirements():
            # Install ML dependencies if requested
            install_ml_dependencies()
            
            print("\n🎉 Installation complete! You can now run:")
            print("   python cli.py")
        else:
            print("\n⚠️ Installation incomplete. Please fix the errors above and try again.")

if __name__ == "__main__":
    main()
