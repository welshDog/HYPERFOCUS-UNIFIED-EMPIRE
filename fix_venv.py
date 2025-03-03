"""
Script to fix a corrupted virtual environment by creating a new one
and installing all required dependencies.
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and print its output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Command completed successfully")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return True
    else:
        print(f"Command failed with exit code {result.returncode}")
        print(f"Error: {result.stderr.strip()}")
        return False

def main():
    print("=" * 60)
    print("BROski Bot Virtual Environment Repair Tool")
    print("=" * 60)
    
    # Get project folder
    project_dir = os.getcwd()
    print(f"Project directory: {project_dir}")
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"Python version: {python_version}")
    
    # Remove old virtual environment
    old_venv = os.path.join(project_dir, "venv")
    if os.path.exists(old_venv):
        print("\nRemoving old virtual environment...")
        try:
            # First try to use the proper method to clear it
            run_command(f"{sys.executable} -m venv --clear {old_venv}")
            print("Done clearing virtual environment")
        except:
            # If that fails, just delete the directory
            try:
                shutil.rmtree(old_venv)
                print("Removed old virtual environment directory")
            except Exception as e:
                print(f"Warning: Could not remove old venv: {e}")
                print("You may need to manually delete the 'venv' folder")
                
    # Create new virtual environment
    print("\nCreating new virtual environment...")
    if not run_command(f"{sys.executable} -m venv venv"):
        print("Failed to create virtual environment.")
        print("Try running as administrator or using a different Python version.")
        return False
    
    # Get the path to the virtual environment's Python and pip
    if os.name == 'nt':  # Windows
        venv_python = os.path.join(project_dir, "venv", "Scripts", "python.exe")
        venv_pip = os.path.join(project_dir, "venv", "Scripts", "pip.exe")
    else:  # Unix/Linux/Mac
        venv_python = os.path.join(project_dir, "venv", "bin", "python")
        venv_pip = os.path.join(project_dir, "venv", "bin", "pip")
    
    # Upgrade pip in the virtual environment
    print("\nUpgrading pip in virtual environment...")
    if not run_command(f'"{venv_python}" -m pip install --upgrade pip'):
        print("Failed to upgrade pip. Continuing anyway...")
    
    # Install dependencies
    print("\nInstalling required dependencies...")
    deps = ["ccxt", "pandas", "numpy", "matplotlib", "colorama", "requests"]
    if not run_command(f'"{venv_pip}" install {" ".join(deps)}'):
        print("Failed to install all dependencies.")
        return False
    
    # Optional dependencies
    print("\nWould you like to install optional dependencies?")
    print("These include: scikit-learn, ta (technical analysis)")
    choice = input("Install optional dependencies? (y/n): ").strip().lower()
    
    if choice == 'y':
        if not run_command(f'"{venv_pip}" install scikit-learn ta'):
            print("Failed to install optional dependencies.")
    
    print("\n" + "=" * 60)
    print("Virtual environment setup complete!")
    print("=" * 60)
    print("\nTo activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("Run: venv\\Scripts\\activate.bat")
    else:  # Unix/Linux/Mac
        print("Run: source venv/bin/activate")
    
    print("\nThen start BROski Bot:")
    print("python BROski_Control_Center.py")
    
    return True

if __name__ == "__main__":
    main()
