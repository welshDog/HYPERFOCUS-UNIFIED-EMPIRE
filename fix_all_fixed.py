"""
Master script to fix all known issues in BROski code - Corrected version
"""

import os
import sys
import shutil
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# ...existing code...

def backup_file(file_path):
    """Create a backup of the specified file
    
    Args:
        file_path: Path to the file to backup
        
    Returns:
        bool: True if backup was successful, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: Cannot backup {file_path}, file not found")
            return False
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.{timestamp}.bak"
        
        # Create backup
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup of {file_path}: {e}")
        return False

def add_missing_imports():
    """Add missing imports to files"""
    files_to_check = [
        "emergency_kill.py",
        "system_report_fix.py"
    ]
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found, skipping import check")
            continue
        
        # Create backup
        if not backup_file(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path == "emergency_kill.py":
                # Check if psutil is imported
                if "import psutil" not in content:
                    # Fix: Using raw string to avoid nested triple quote issues
                    dependencies_check = r'''
def install_missing_packages():
    """Install missing required packages"""
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
            return True
        except:
            print("Failed to install required packages.")
            print(f"Please run: pip install {' '.join(missing_packages)}")
            return False
    
    return True

# Check dependencies before starting
if not install_missing_packages():
    print("Cannot continue without required packages.")
    sys.exit(1)
'''
                    # Insert after the imports
                    import_section_end = content.find("def")
                    if import_section_end > 0:
                        content = content[:import_section_end] + dependencies_check + content[import_section_end:]
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"Added dependency check to {file_path}")
            
            elif file_path == "system_report_fix.py":
                # Check for psutil import
                if "import psutil" not in content:
                    # Fix: Using raw string to avoid nested triple quote issues
                    psutil_check = r'''
# Ensure psutil is installed
try:
    import psutil
except ImportError:
    print("Installing psutil...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil
'''
                    # Insert after the imports
                    import_section_end = content.find("class SystemReport")
                    if import_section_end > 0:
                        content = content[:import_section_end] + psutil_check + content[import_section_end:]
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"Added psutil check to {file_path}")
                
        except Exception as e:
            print(f"Error adding imports to {file_path}: {e}")

# ...existing code...

# The rest of the functions remain the same
