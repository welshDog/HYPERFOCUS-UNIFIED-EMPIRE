"""
Master script to fix all known issues in BROski code
"""

import os
import sys
import shutil
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def backup_file(file_path):
    """Create a backup of a file"""
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found, skipping backup")
        return False
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"Error backing up {file_path}: {e}")
        return False

def fix_unified_launcher():
    """Remove duplicate call to handle_main_menu() in unified_launcher.py"""
    file_path = "unified_launcher.py"
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found, skipping fix")
        return False
    
    # Create backup
    if not backup_file(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove the duplicate call at the end
        if content.endswith("handle_main_menu()"):
            content = content[:-len("handle_main_menu()")]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed {file_path} by removing duplicate handle_main_menu() call")
            return True
        else:
            print(f"No duplicate handle_main_menu() call found in {file_path}")
            return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
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
                    # Add a function to check and install dependencies
                    dependencies_check = """
def install_missing_packages():
    '''Install missing required packages'''
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
"""
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
                    # Add try/except block to install psutil
                    psutil_check = """
# Ensure psutil is installed
try:
    import psutil
except ImportError:
    print("Installing psutil...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil
"""
                    # Insert after the imports
                    import_section_end = content.find("class SystemReport")
                    if import_section_end > 0:
                        content = content[:import_section_end] + psutil_check + content[import_section_end:]
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"Added psutil check to {file_path}")
                
        except Exception as e:
            print(f"Error adding imports to {file_path}: {e}")

def create_install_dependencies_script():
    """Create a script to install all required dependencies"""
    file_path = "install_dependencies.py"
    
    dependencies_script = """
# filepath: /c:/Users/Lyndz/OneDrive/Documents/BROski the Crypto Bot/install_dependencies.py
\"\"\"
Script to install all dependencies required by BROski Bot
\"\"\"

import subprocess
import sys
import os
from pathlib import Path
import platform

def print_header(text):
    \"\"\"Print a formatted header\"\"\"
    print("=" * 60)
    print(text)
    print("=" * 60)

def install_packages(packages, message):
    \"\"\"Install a list of packages\"\"\"
    print_header(message)
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except Exception as e:
            print(f"✗ Error installing {package}: {e}")
    
    print()

def main():
    print_header("BROski Bot Dependency Installer")
    
    # Core dependencies
    core_packages = [
        "ccxt",        # Crypto exchange library
        "pandas",      # Data analysis
        "numpy",       # Numerical computation
        "matplotlib",  # Plotting
        "colorama",    # Terminal colors
        "requests",    # HTTP requests
        "psutil",      # System monitoring
    ]
    
    # Optional dependencies
    optional_packages = [
        "scikit-learn",  # Machine learning
        "ta",            # Technical analysis
    ]
    
    # Platform specific
    windows_packages = [
        "pywin32",     # Windows API (for shortcuts)
        "winshell",    # Windows shell integration
    ]
    
    # Install core packages
    install_packages(core_packages, "Installing Core Dependencies")
    
    # Ask about optional packages
    print("Optional dependencies provide additional functionality:")
    print("- scikit-learn: Machine learning capabilities")
    print("- ta: Technical analysis indicators")
    install_optional = input("Install optional dependencies? (y/n): ").lower() == 'y'
    
    if install_optional:
        install_packages(optional_packages, "Installing Optional Dependencies")
    
    # Install platform-specific packages
    if platform.system() == "Windows":
        print("Windows detected, installing Windows-specific dependencies...")
        install_packages(windows_packages, "Installing Windows Dependencies")
    
    print_header("Installation Complete!")
    print("All required dependencies for BROski Bot have been installed.")
    print("You can now run BROski Bot's components.")
    
    # Create directories if they don't exist
    directories = ["logs", "data", "backups", "strategies"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("Created required directories: logs, data, backups, strategies")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
"""
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(dependencies_script)
        
        print(f"Created {file_path}")
        return True
    except Exception as e:
        print(f"Error creating {file_path}: {e}")
        return False

def run_gui():
    """Run a GUI to apply fixes"""
    root = tk.Tk()
    root.title("BROski Bot Fix Tool")
    root.geometry("500x400")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill="both", expand=True)
    
    # Title
    tk.Label(frame, text="BROski Bot Fix Tool", font=("Arial", 16, "bold")).pack(pady=(0, 20))
    
    # Fix options
    tk.Label(frame, text="Select fixes to apply:", font=("Arial", 12)).pack(anchor="w")
    
    # Checkboxes for fixes
    unified_launcher_var = tk.BooleanVar(value=True)
    tk.Checkbutton(frame, text="Fix unified_launcher.py (Remove duplicate call)", variable=unified_launcher_var).pack(anchor="w", pady=2)
    
    emergency_kill_var = tk.BooleanVar(value=True)
    tk.Checkbutton(frame, text="Fix emergency_kill.py (Add missing imports)", variable=emergency_kill_var).pack(anchor="w", pady=2)
    
    system_report_var = tk.BooleanVar(value=True)
    tk.Checkbutton(frame, text="Fix system_report_fix.py (Add psutil dependency)", variable=system_report_var).pack(anchor="w", pady=2)
    
    install_script_var = tk.BooleanVar(value=True)
    tk.Checkbutton(frame, text="Create dependency installer script", variable=install_script_var).pack(anchor="w", pady=2)
    
    # Status text area
    status_frame = tk.Frame(frame)
    status_frame.pack(fill="both", expand=True, pady=10)
    
    status_text = tk.Text(status_frame, height=10, width=50)
    status_text.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(status_frame, command=status_text.yview)
    scrollbar.pack(side="right", fill="y")
    status_text.config(yscrollcommand=scrollbar.set)
    
    def log_status(message):
        """Add a message to the status text"""
        status_text.insert(tk.END, f"{message}\n")
        status_text.see(tk.END)
        root.update_idletasks()
    
    def apply_fixes():
        """Apply selected fixes"""
        status_text.delete(1.0, tk.END)
        log_status("Starting to apply fixes...")
        
        if unified_launcher_var.get():
            log_status("Fixing unified_launcher.py...")
            if fix_unified_launcher():
                log_status("✓ unified_launcher.py fixed successfully")
            else:
                log_status("✗ Failed to fix unified_launcher.py")
        
        if emergency_kill_var.get() or system_report_var.get():
            log_status("Adding missing imports to files...")
            add_missing_imports()
            log_status("✓ Added missing imports to files")
        
        if install_script_var.get():
            log_status("Creating dependency installer script...")
            if create_install_dependencies_script():
                log_status("✓ Created install_dependencies.py")
            else:
                log_status("✗ Failed to create install_dependencies.py")
        
        log_status("\nAll selected fixes have been applied!")
        messagebox.showinfo("Fixes Applied", "All selected fixes have been applied!")
    
    # Buttons
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)
    
    apply_button = tk.Button(button_frame, text="Apply Fixes", command=apply_fixes, width=15)
    apply_button.pack(side="left", padx=5)
    
    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy, width=15)
    exit_button.pack(side="left", padx=5)
    
    # Initial message
    log_status("Ready to apply fixes. Select options and click 'Apply Fixes'.")
    
    root.mainloop()

def main():
    """Main function to run the fix tool"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BROski Bot Fix Tool")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode (no GUI)")
    parser.add_argument("--all", action="store_true", help="Apply all fixes")
    args = parser.parse_args()
    
    if args.cli:
        print("Running in CLI mode...")
        
        if args.all:
            print("Applying all fixes...")
            fix_unified_launcher()
            add_missing_imports()
            create_install_dependencies_script()
            print("All fixes applied!")
        else:
            print("No specific fixes selected. Use --all to apply all fixes.")
    else:
        run_gui()

if __name__ == "__main__":
    main()
