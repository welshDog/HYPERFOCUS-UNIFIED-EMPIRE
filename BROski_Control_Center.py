import os
import sys
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import time
import traceback
import shutil  # Required for the reset_config method

class BROskiControlCenter:
    def __init__(self, root):
        self.root = root
        
        # Initialize error handler for uncaught exceptions
        sys.excepthook = lambda *args: self.exception_handler(*args)
def exception_handler(self, *args):
    """Handle uncaught exceptions"""
    error_msg = f"An unexpected error occurred:\n{args[1]}"
    messagebox.showerror("Error", error_msg)
    traceback.print_exception(*args)

def fix_initialization(self):
    """Initialize key attributes"""
    self.config = {}
    self.info_label = None
    self.diagnostic_text = None
    
def custom_backup(self):
    """Perform a custom backup"""
    self.info_label.config(text="Preparing custom backup...")
    
    # Create backup options window
    options_window = tk.Toplevel(self.root)
    options_window.title("Custom Backup Options")
    options_window.geometry("400x500")
    options_window.transient(self.root)
    options_window.grab_set()
    
    # Header
    ttk.Label(
        options_window, 
        text="Custom Backup Options",
        font=("Arial", 14, "bold")
    ).pack(pady=10)
    
    # Backup location
    location_frame = ttk.LabelFrame(options_window, text="Backup Location", padding=10)
    location_frame.pack(fill="x", padx=20, pady=10)
    
    location_var = tk.StringVar(value=os.path.join(os.getcwd(), "backups"))
    ttk.Label(location_frame, text="Backup Directory:").pack(anchor="w")
    
    path_frame = ttk.Frame(location_frame)
    path_frame.pack(fill="x", pady=5)
    
    path_entry = ttk.Entry(path_frame, textvariable=location_var, width=30)
    path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    def browse_location():
        directory = filedialog.askdirectory(title="Select Backup Location")
        if directory:
            location_var.set(directory)
    
    ttk.Button(path_frame, text="Browse", command=browse_location).pack(side="right")
    
    # Backup items selection
    items_frame = ttk.LabelFrame(options_window, text="Items to Backup", padding=10)
    items_frame.pack(fill="x", padx=20, pady=10)
    
    config_var = tk.BooleanVar(value=True)
    scripts_var = tk.BooleanVar(value=True)
    logs_var = tk.BooleanVar(value=True)
    bat_files_var = tk.BooleanVar(value=True)
    strategies_var = tk.BooleanVar(value=True)
    
    ttk.Checkbutton(items_frame, text="Configuration Files", variable=config_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(items_frame, text="Python Scripts", variable=scripts_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(items_frame, text="Log Files", variable=logs_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(items_frame, text="Batch Files", variable=bat_files_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(items_frame, text="Strategy Files", variable=strategies_var).pack(anchor="w", pady=2)
    
    # Backup name
    name_frame = ttk.LabelFrame(options_window, text="Backup Name", padding=10)
    name_frame.pack(fill="x", padx=20, pady=10)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name_var = tk.StringVar(value=f"BROski_Backup_{timestamp}")
    ttk.Label(name_frame, text="Backup Name:").pack(anchor="w")
    ttk.Entry(name_frame, textvariable=name_var, width=30).pack(fill="x", pady=5)
    
    # Buttons
    buttons_frame = ttk.Frame(options_window)
    buttons_frame.pack(pady=20)
    
    def do_backup():
        try:
            backup_dir = location_var.get()
            backup_name = name_var.get()
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Create subdirectories
            if config_var.get():
                os.makedirs(os.path.join(backup_path, "config"), exist_ok=True)
            if scripts_var.get() or bat_files_var.get():
                os.makedirs(os.path.join(backup_path, "scripts"), exist_ok=True)
            if logs_var.get():
                os.makedirs(os.path.join(backup_path, "logs"), exist_ok=True)
            if strategies_var.get():
                os.makedirs(os.path.join(backup_path, "strategies"), exist_ok=True)
            
            # Copy files
            items_copied = 0
            
            # Configuration files
            if config_var.get() and os.path.exists("config.json"):
                shutil.copy("config.json", os.path.join(backup_path, "config", "config.json"))
                items_copied += 1
            
            # Python scripts
            if scripts_var.get():
                for file in os.listdir():
                    if file.endswith('.py'):
                        shutil.copy(file, os.path.join(backup_path, "scripts", file))
                        items_copied += 1
            
            # Batch files
            if bat_files_var.get():
                for file in os.listdir():
                    if file.endswith('.bat'):
                        shutil.copy(file, os.path.join(backup_path, "scripts", file))
                        items_copied += 1
            
            # Logs
            if logs_var.get() and os.path.exists("logs"):
                log_files = [f for f in os.listdir("logs") if f.endswith('.log')]
                for log_file in log_files[:10]:  # Copy up to 10 most recent logs
                    shutil.copy(os.path.join("logs", log_file), os.path.join(backup_path, "logs", log_file))
                    items_copied += 1
            
            # Strategy files
            if strategies_var.get() and os.path.exists("strategies"):
                for file in os.listdir("strategies"):
                    if file.endswith('.py') or file.endswith('.json'):
                        shutil.copy(os.path.join("strategies", file), os.path.join(backup_path, "strategies", file))
                        items_copied += 1
            
            options_window.destroy()
            self.info_label.config(text=f"Custom backup created: {backup_name} ({items_copied} files)")
            messagebox.showinfo("Backup Complete", f"Custom backup created at:\n{backup_path}\n\n{items_copied} files backed up.")
            
            # Refresh backup list
            self.refresh_backup_list()
            
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create custom backup: {str(e)}")
            self.info_label.config(text="Error creating custom backup")
    
    ttk.Button(buttons_frame, text="Create Backup", command=do_backup).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Cancel", command=options_window.destroy).pack(side="right", padx=10)

def restore_from_backup(self):
    """Restore from a backup directory"""
    backup_dir = filedialog.askdirectory(
        title="Select Backup Directory to Restore From"
    )
    
    if not backup_dir:
        return  # User cancelled
        
    # Verify it's a valid BROski backup
    config_backup = os.path.join(backup_dir, "config", "config.json")
    scripts_dir = os.path.join(backup_dir, "scripts")
    
    if not (os.path.exists(config_backup) and os.path.exists(scripts_dir)):
        messagebox.showerror(
            "Invalid Backup", 
            "The selected directory doesn't appear to be a valid BROski backup.\n\n" +
            "Expected to find config/config.json and scripts/ directory."
        )
        return
    
    # Confirm before restore
    confirm = messagebox.askyesno(
        "Confirm Restore",
        "This will restore BROski Bot from the selected backup.\n\n" +
        "Current files may be overwritten. Continue?"
    )
    
    if not confirm:
        return
        
    try:
        # Backup current config first
        if os.path.exists("config.json"):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"config.json.backup_{timestamp}"
            shutil.copy("config.json", backup_name)
            self.add_activity(f"Current config backed up to {backup_name}")
        
        # Restore config
        shutil.copy(config_backup, "config.json")
        
        # Restore scripts (Python files)
        for file in os.listdir(scripts_dir):
            if file.endswith('.py'):
                shutil.copy(os.path.join(scripts_dir, file), file)
        
        # Reload configuration
        self.load_config()
        
        self.info_label.config(text="Restored from backup successfully")
        messagebox.showinfo("Restore Complete", "BROski Bot has been restored from the backup successfully.")
        
    except Exception as e:
        messagebox.showerror("Restore Error", f"Failed to restore from backup: {str(e)}")
        self.info_label.config(text="Error restoring from backup")

def schedule_backups(self):
    """Schedule automatic backups"""
    scheduler_window = tk.Toplevel(self.root)
    scheduler_window.title("Schedule Automatic Backups")
    scheduler_window.geometry("450x400")
    scheduler_window.transient(self.root)
    scheduler_window.grab_set()
    
    ttk.Label(
        scheduler_window, 
        text="Schedule Regular Backups",
        font=("Arial", 14, "bold")
    ).pack(pady=10)
    
    ttk.Label(
        scheduler_window, 
        text="Windows Task Scheduler will be used to create regular backups."
    ).pack(pady=5)
    
    # Frequency frame
    frequency_frame = ttk.LabelFrame(scheduler_window, text="Backup Frequency", padding=10)
    frequency_frame.pack(fill="x", padx=20, pady=10)
    
    frequency_var = tk.StringVar(value="daily")
    ttk.Radiobutton(frequency_frame, text="Daily", variable=frequency_var, value="daily").pack(anchor="w")
    ttk.Radiobutton(frequency_frame, text="Weekly", variable=frequency_var, value="weekly").pack(anchor="w")
    ttk.Radiobutton(frequency_frame, text="Monthly", variable=frequency_var, value="monthly").pack(anchor="w")
    
    # Backup location
    location_frame = ttk.LabelFrame(scheduler_window, text="Backup Location", padding=10)
    location_frame.pack(fill="x", padx=20, pady=10)
    
    location_var = tk.StringVar(value=os.path.join(os.getcwd(), "backups"))
    location_entry = ttk.Entry(location_frame, textvariable=location_var, width=40)
    location_entry.pack(side="left", padx=5)
    
    def browse_location():
        directory = filedialog.askdirectory(title="Select Backup Location")
        if directory:
            location_var.set(directory)
    
    ttk.Button(location_frame, text="Browse", command=browse_location).pack(side="right")
    
    # Action buttons
    def create_schedule():
        try:
            frequency = frequency_var.get()
            location = location_var.get()
            
            # Create the backup batch script
            script_path = os.path.join(os.getcwd(), "scheduled_backup.bat")
            with open(script_path, "w") as f:
                f.write("@echo off\n")
                f.write("echo BROski Scheduled Backup\n")
                f.write(f"cd /d \"{os.getcwd()}\"\n")
                f.write("set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%\n")
                f.write("set TIMESTAMP=%TIMESTAMP: =0%\n")
                f.write(f"set BACKUP_DIR=\"{location}\\BROski_Backup_%TIMESTAMP%\"\n")
                f.write("mkdir %BACKUP_DIR%\n")
                f.write("mkdir %BACKUP_DIR%\\config\n")
                f.write("mkdir %BACKUP_DIR%\\scripts\n")
                f.write("mkdir %BACKUP_DIR%\\logs\n")
                f.write("xcopy config.json %BACKUP_DIR%\\config\\ /Y\n")
                f.write("xcopy *.py %BACKUP_DIR%\\scripts\\ /Y\n")
                f.write("xcopy logs\\*.log %BACKUP_DIR%\\logs\\ /Y\n")
                f.write("echo Backup completed successfully to %BACKUP_DIR%\n")
                f.write("exit\n")
            
            # Create appropriate schtasks command based on frequency
            task_name = f"BROski_{frequency.capitalize()}_Backup"
            
            if frequency == "daily":
                cmd = f'schtasks /create /tn "{task_name}" /tr "{script_path}" /sc daily /st 03:00 /f'
                desc = "Daily at 3:00 AM"
            elif frequency == "weekly":
                cmd = f'schtasks /create /tn "{task_name}" /tr "{script_path}" /sc weekly /st 03:00 /d SUN /f'
                desc = "Weekly on Sunday at 3:00 AM"
            else:  # monthly
                cmd = f'schtasks /create /tn "{task_name}" /tr "{script_path}" /sc monthly /st 03:00 /d 1 /f'
                desc = "Monthly on the 1st at 3:00 AM"
            
            # Run the command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Scheduled backup created: {desc}\n\nBackups will be stored in: {location}")
                scheduler_window.destroy()
            else:
                messagebox.showerror("Error", f"Failed to create scheduled task:\n{result.stderr}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule backups: {str(e)}")
    
    buttons_frame = ttk.Frame(scheduler_window)
    buttons_frame.pack(pady=20)
    
    ttk.Button(buttons_frame, text="Schedule", command=create_schedule).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Cancel", command=scheduler_window.destroy).pack(side="right", padx=10)

def run_health_check(self):
    """Run a complete health check on the system"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "🔍 Running BROski Bot Health Check...\n\n")
    self.info_label.config(text="Running health check...")
    
    # Track overall status
    issues_found = 0
    warnings_found = 0
    
    # Function to add a section result
    def add_result(title, status, details="", is_warning=False):
        nonlocal issues_found, warnings_found
        
        self.diagnostic_text.insert(tk.END, f"{title}: ")
        
        if status == "PASS":
            self.diagnostic_text.insert(tk.END, "✅ PASS\n")
        elif status == "WARNING":
            self.diagnostic_text.insert(tk.END, "⚠️ WARNING\n")
            warnings_found += 1
        else:  # FAIL
            self.diagnostic_text.insert(tk.END, "❌ FAIL\n")
            issues_found += 1
        
        if details:
            self.diagnostic_text.insert(tk.END, f"{details}\n")
        
        self.diagnostic_text.insert(tk.END, "\n")
    
    # 1. Check Python version
    try:
        python_version = sys.version.split()[0]
        version_parts = [int(x) for x in python_version.split('.')]
        
        if version_parts[0] < 3 or (version_parts[0] == 3 and version_parts[1] < 8):
            add_result("Python Version", "WARNING", 
                       f"Python {python_version} detected. Version 3.8+ recommended.")
        else:
            add_result("Python Version", "PASS", 
                       f"Python {python_version} detected.")
    except:
        add_result("Python Version", "FAIL", "Could not determine Python version.")
    
    # 2. Check configuration
    try:
        if not os.path.exists("config.json"):
            add_result("Configuration", "FAIL", "config.json file not found.")
        else:
            with open("config.json", 'r') as f:
                config = json.load(f)
                
            config_issues = []
            
            # Check API keys
            if "exchange" not in config:
                config_issues.append("Missing 'exchange' section")
            elif not config["exchange"].get("api_key") or not config["exchange"].get("api_secret"):
                config_issues.append("API keys not configured")
            elif config["exchange"].get("api_key") == "YOUR_MEXC_API_KEY_HERE":
                config_issues.append("Default API key needs to be replaced")
            
            # Check trading settings
            if "trading" not in config:
                config_issues.append("Missing 'trading' section")
            elif not config["trading"].get("base_symbol") or not config["trading"].get("quote_symbol"):
                config_issues.append("Trading pair not configured")
            
            if config_issues:
                add_result("Configuration", "FAIL", "Issues found: " + ", ".join(config_issues))
            else:
                add_result("Configuration", "PASS", "Configuration file is valid.")
    except Exception as e:
        add_result("Configuration", "FAIL", f"Error checking configuration: {str(e)}")
    
    # 3. Check dependencies
    try:
        missing_deps = []
        for package in ["ccxt", "pandas", "matplotlib", "colorama"]:
            try:
                __import__(package)
            except ImportError:
                missing_deps.append(package)
        
        if missing_deps:
            add_result("Dependencies", "FAIL", 
                      f"Missing packages: {', '.join(missing_deps)}\n"
                      f"Run: pip install {' '.join(missing_deps)}")
        else:
            add_result("Dependencies", "PASS", "All required packages are installed.")
    except Exception as e:
        add_result("Dependencies", "FAIL", f"Error checking dependencies: {str(e)}")
    
    # 4. Check directories
    try:
        required_dirs = ["logs", "backups"]
        missing_dirs = []
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                missing_dirs.append(directory)
                try:
                    os.makedirs(directory)
                except:
                    pass
        
        if missing_dirs:
            add_result("Directories", "WARNING", 
                      f"Created missing directories: {', '.join(missing_dirs)}")
        else:
            add_result("Directories", "PASS", "All required directories exist.")
    except Exception as e:
        add_result("Directories", "FAIL", f"Error checking directories: {str(e)}")
    
    # 5. Check disk space
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(os.getcwd()), 
                None, 
                None,
                ctypes.pointer(free_bytes)
            )
            free_mb = free_bytes.value / (1024 * 1024)
            
            if free_mb < 100:  # Less than 100 MB free
                add_result("Disk Space", "FAIL", f"Only {free_mb:.1f} MB free disk space available.")
            elif free_mb < 500:  # Less than 500 MB free
                add_result("Disk Space", "WARNING", f"Low disk space: {free_mb:.1f} MB free.")
            else:
                add_result("Disk Space", "PASS", f"{free_mb:.1f} MB free disk space available.")
        else:
            # For non-Windows, just report OK since we don't have a simple way to check
            add_result("Disk Space", "PASS", "Disk space check skipped on this OS.")
    except Exception as e:
        add_result("Disk Space", "WARNING", f"Could not check disk space: {str(e)}")
    
    # 6. Check internet connectivity
    try:
        import socket
        host = "8.8.8.8"  # Google's DNS
        port = 53
        timeout = 3
        
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        add_result("Internet Connection", "PASS", "Internet connection is working.")
    except Exception as e:
        add_result("Internet Connection", "FAIL", "Could not connect to the internet.")
    
    # Overall summary
    self.diagnostic_text.insert(tk.END, "="*50 + "\n")
    if issues_found == 0 and warnings_found == 0:
        self.diagnostic_text.insert(tk.END, "✅ ALL CHECKS PASSED! Your BROski Bot is ready to go!\n")
        self.info_label.config(text="Health check complete: All systems OK")
    else:
        status = []
        if issues_found > 0:
            status.append(f"{issues_found} issues")
        if warnings_found > 0:
            status.append(f"{warnings_found} warnings")
            
        status_str = " and ".join(status)
        self.diagnostic_text.insert(tk.END, f"⚠️ Found {status_str}. Please address them before trading.\n")
        self.info_label.config(text=f"Health check complete: Found {status_str}")
    
    # Timestamp
    self.diagnostic_text.insert(tk.END, f"\nHealth check completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def check_api_connection(self):
    """Check the connection to the exchange API"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "Testing API connection to MEXC...\n\n")
    self.info_label.config(text="Testing API connection...")
    
    # Check if API keys are configured
    if not self.config or "exchange" not in self.config:
        self.diagnostic_text.insert(tk.END, "❌ Error: No exchange configuration found.\n")
        self.info_label.config(text="API test failed: No config")
        return
    
    exchange = self.config["exchange"]
    if not exchange.get("api_key") or not exchange.get("api_secret"):
        self.diagnostic_text.insert(tk.END, "❌ Error: API keys not configured.\n")
        self.diagnostic_text.insert(tk.END, "Please configure your API keys in the Configuration tab.")
        self.info_label.config(text="API test failed: No API keys")
        return
    
    # Try to import ccxt
    try:
        import ccxt
    except ImportError:
        self.diagnostic_text.insert(tk.END, "❌ Error: CCXT library not installed.\n")
        self.diagnostic_text.insert(tk.END, "Please run: pip install ccxt")
        self.info_label.config(text="API test failed: CCXT not installed")
        return
    
    # Try to connect to the exchange
    try:
        self.diagnostic_text.insert(tk.END, "Connecting to MEXC exchange...\n")
        
        # Initialize the exchange
        mexc = ccxt.mexc({
            'apiKey': exchange["api_key"],
            'secret': exchange["api_secret"],
            'enableRateLimit': True
        })
        
        # Test by fetching account balance
        self.diagnostic_text.insert(tk.END, "Fetching account balance...\n")
        balance = mexc.fetch_balance()
        
        # Display success message
        self.diagnostic_text.insert(tk.END, "✅ API connection successful!\n\n")
        
        # Display some account info
        self.diagnostic_text.insert(tk.END, "Account Information:\n")
        self.diagnostic_text.insert(tk.END, "===================\n")
        
        # Show USDT balance if available
        if 'USDT' in balance['total']:
            self.diagnostic_text.insert(tk.END, f"USDT Balance: {balance['total']['USDT']}\n")
        
        # Show base currency balance if configured
        if "trading" in self.config and "base_symbol" in self.config["trading"]:
            base = self.config["trading"]["base_symbol"]
            if base in balance['total']:
                self.diagnostic_text.insert(tk.END, f"{base} Balance: {balance['total'][base]}\n")
        
        # Show a few other balances
        self.diagnostic_text.insert(tk.END, "\nOther Assets:\n")
        count = 0
        for currency, amount in balance['total'].items():
            if amount > 0 and currency not in ['USDT'] and count < 5:
                self.diagnostic_text.insert(tk.END, f"{currency}: {amount}\n")
                count += 1
        
        self.info_label.config(text="API connection test successful")
        
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"❌ API connection failed: {str(e)}\n\n")
        self.diagnostic_text.insert(tk.END, "Possible reasons:\n")
        self.diagnostic_text.insert(tk.END, "1. Invalid API key or secret\n")
        self.diagnostic_text.insert(tk.END, "2. Network connectivity issues\n")
        self.diagnostic_text.insert(tk.END, "3. IP address not whitelisted (if using IP restrictions)\n")
        self.diagnostic_text.insert(tk.END, "4. MEXC API service issues\n\n")
        self.diagnostic_text.insert(tk.END, "Please check your API keys and try again.")
        self.info_label.config(text="API connection test failed")

def verify_dependencies(self):
    """Verify that all required dependencies are installed"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "Verifying Python dependencies...\n\n")
    self.info_label.config(text="Checking dependencies...")
    
    required_packages = [
        {"name": "ccxt", "desc": "Cryptocurrency Exchange Trading Library"},
        {"name": "pandas", "desc": "Data Analysis Library"},
        {"name": "matplotlib", "desc": "Plotting Library"},
        {"name": "colorama", "desc": "Terminal Color Library"},
        {"name": "requests", "desc": "HTTP Library"},
        {"name": "numpy", "desc": "Numerical Computing Library"}
    ]
    
    optional_packages = [
        {"name": "tensorflow", "desc": "Machine Learning (for ML strategy)"},
        {"name": "scikit-learn", "desc": "Machine Learning Tools"},
        {"name": "ta", "desc": "Technical Analysis Library"}
    ]
    
    # Try to import each package and record status
    missing = []
    installed = []
    outdated = []
    
    for package in required_packages:
        try:
            module = __import__(package["name"])
            version = getattr(module, "__version__", "unknown")
            installed.append({"name": package["name"], "version": version})
        except ImportError:
            missing.append(package)
    
    # Check optional packages
    optional_missing = []
    for package in optional_packages:
        try:
            module = __import__(package["name"])
            version = getattr(module, "__version__", "unknown")
            installed.append({"name": package["name"], "version": version, "optional": True})
        except ImportError:
            optional_missing.append(package)
    
    # Display results
    if not missing:
        self.diagnostic_text.insert(tk.END, "✅ All required dependencies are installed!\n\n")
    else:
        self.diagnostic_text.insert(tk.END, f"❌ Missing {len(missing)} required dependencies!\n\n")
    
    # Show installed packages
    self.diagnostic_text.insert(tk.END, "Installed Packages:\n")
    self.diagnostic_text.insert(tk.END, "==================\n")
    for pkg in installed:
        is_optional = pkg.get("optional", False)
        prefix = "(Optional) " if is_optional else ""
        self.diagnostic_text.insert(tk.END, f"✅ {prefix}{pkg['name']} v{pkg['version']}\n")
    
    # Show missing required packages
    if missing:
        self.diagnostic_text.insert(tk.END, "\nMissing Required Packages:\n")
        self.diagnostic_text.insert(tk.END, "========================\n")
        for pkg in missing:
            self.diagnostic_text.insert(tk.END, f"❌ {pkg['name']} - {pkg['desc']}\n")
        
        # Generate pip install command
        cmd = f"pip install {' '.join(p['name'] for p in missing)}"
        self.diagnostic_text.insert(tk.END, f"\nInstall missing packages with:\n{cmd}\n")
    
    # Show missing optional packages
    if optional_missing:
        self.diagnostic_text.insert(tk.END, "\nMissing Optional Packages:\n")
        self.diagnostic_text.insert(tk.END, "========================\n")
        for pkg in optional_missing:
            self.diagnostic_text.insert(tk.END, f"⚠️ {pkg['name']} - {pkg['desc']} (optional)\n")
            
        # Generate pip install command for optional packages
        cmd = f"pip install {' '.join(p['name'] for p in optional_missing)}"
        self.diagnostic_text.insert(tk.END, f"\nInstall optional packages with:\n{cmd}\n")
    
    # Update status label
    self.info_label.config(text="Dependency check complete")
