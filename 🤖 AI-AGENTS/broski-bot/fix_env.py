"""
Quick fix for corrupted virtual environment
"""
import os
import subprocess
import sys

def main():
    print("Fixing virtual environment...")
    
    # Get project directory
    project_dir = os.getcwd()
    print(f"Working in: {project_dir}")
    
    # Delete the old venv
    if os.path.exists("venv"):
        print("Removing old virtual environment...")
        os.system("rmdir /s /q venv")
    
    # Create new venv
    print("Creating new virtual environment...")
    os.system("python -m venv venv")
    
    # Install dependencies
    print("Installing dependencies...")
    pip_path = os.path.join("venv", "Scripts", "pip.exe")
    os.system(f"{pip_path} install ccxt pandas numpy matplotlib colorama requests")
    
    print("\nVirtual environment fixed! To use it, run:")
    print("venv\\Scripts\\activate")
    
if __name__ == "__main__":
    main()
