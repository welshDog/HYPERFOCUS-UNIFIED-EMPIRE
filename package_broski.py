import os
import sys
import shutil
import zipfile
import json
import datetime
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_step(text):
    print(f"{Fore.CYAN}[PACKAGE] {text}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}[SUCCESS] {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}[ERROR] {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}[WARNING] {text}{Style.RESET_ALL}")

def create_broski_package():
    """Create a distributable package for BROski Bot"""
    print_step("Starting BROski Bot packaging process...")
    
    # Get current directory
    source_dir = Path.cwd()
    
    # Create timestamp for version
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define output directory and filename
    output_dir = source_dir / "dist"
    zip_filename = f"BROski_Bot_{timestamp}.zip"
    zip_filepath = output_dir / zip_filename
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print_step(f"Created output directory: {output_dir}")
    
    # Files and directories to include
    include_files = [
        # Core files
        "start_bot.py", "direct_bot.py", "cli.py", "check_system.py",
        "config.example.json", "README.md", "QUICK_START.md", "TROUBLESHOOTING.md",
        "STRATEGIES.md", "requirements.txt",
        
        # Batch files
        "START_BOT.bat", "MONITOR_DIRECT.bat", "BROSKI_DASHBOARD.bat", 
        "CHECK_BROSKI.bat", "BACKUP_BOT.bat"
    ]
    
    include_dirs = [
        "strategies", "logs"
    ]
    
    # Files and directories to exclude
    exclude_files = [
        "config.json",  # Exclude personal config
        "__pycache__", 
        "*.pyc",
        "venv",
        ".git",
        ".gitignore",
        "dist"
    ]
    
    # Create a temporary directory for staging files
    temp_dir = output_dir / f"broski_temp_{timestamp}"
    os.makedirs(temp_dir, exist_ok=True)
    print_step(f"Created temporary staging directory: {temp_dir}")
    
    # Copy files and directories
    print_step("Copying files and directories...")
    
    # First, copy specified files
    for file in include_files:
        src_path = source_dir / file
        if src_path.exists():
            dst_path = temp_dir / file
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                print_success(f"Copied file: {file}")
            else:
                print_warning(f"Skipped, not a file: {file}")
        else:
            print_warning(f"File not found: {file}")
    
    # Copy directories
    for directory in include_dirs:
        src_dir = source_dir / directory
        dst_dir = temp_dir / directory
        
        if src_dir.exists():
            if not dst_dir.exists():
                os.makedirs(dst_dir, exist_ok=True)
            
            # If it's the logs directory, create it but don't copy content
            if (directory == "logs"):
                print_success(f"Created empty logs directory")
            else:
                # Copy all files in the directory
                for item in src_dir.glob('**/*'):
                    # Skip __pycache__ directories and .pyc files
                    if "__pycache__" in str(item) or item.name.endswith('.pyc'):
                        continue
                    
                    # Get the relative path from source_dir
                    rel_path = item.relative_to(source_dir)
                    dst_path = temp_dir / rel_path
                    
                    if item.is_file():
                        os.makedirs(dst_path.parent, exist_ok=True)
                        shutil.copy2(item, dst_path)
                    elif item.is_dir():
                        os.makedirs(dst_path, exist_ok=True)
                
                print_success(f"Copied directory: {directory}")
        else:
            os.makedirs(dst_dir, exist_ok=True)
            print_warning(f"Directory not found, created empty: {directory}")
    
    # Create a blank config.json from example
    try:
        with open(temp_dir / "config.example.json", 'r') as f:
            config = json.load(f)
        
        # Clear API keys
        config["exchange"]["api_key"] = ""
        config["exchange"]["api_secret"] = ""
        
        with open(temp_dir / "config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        print_success(f"Created blank config.json")
    except Exception as e:
        print_error(f"Failed to create config.json: {str(e)}")
    
    # Create installation readme
    install_readme = """# BROski Bot Installation

## Quick Installation Guide

1. Extract all files to a folder of your choice
2. Open a command prompt in this folder
3. Run: `pip install -r requirements.txt`
4. Run: `python setup.py` to configure your API keys
5. Run: `CHECK_BROSKI.bat` to verify installation
6. Start the bot with `START_BOT.bat`

For more detailed instructions, please read QUICK_START.md

Enjoy your trading with BROski Bot!
"""
    
    with open(temp_dir / "INSTALL.md", 'w') as f:
        f.write(install_readme)
    
    print_success(f"Created installation guide: INSTALL.md")
    
    # Create ZIP file
    print_step(f"Creating ZIP package: {zip_filepath}")
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from temp directory
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip with relative path
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))
    
    print_success(f"ZIP package created successfully!")
    
    # Clean up temporary directory
    print_step("Cleaning up temporary directory...")
    shutil.rmtree(temp_dir)
    print_success(f"Temporary directory removed")
    
    print_success(f"BROski Bot package created at: {zip_filepath}")
    print(f"\nYou can distribute this file to install BROski Bot on other computers.")
    print(f"The package contains all necessary files except personal API keys.")

if __name__ == "__main__":
    try:
        create_broski_package()
    except Exception as e:
        print_error(f"Packaging failed: {str(e)}")
        import traceback
        print_error(traceback.format_exc())
        sys.exit(1)
