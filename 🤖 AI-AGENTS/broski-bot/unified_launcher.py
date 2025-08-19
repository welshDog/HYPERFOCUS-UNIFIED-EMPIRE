"""
Unified launcher menu system for BROski Bot
This script provides a central menu interface to launch all BROski components
"""

import os
import sys
import subprocess
import time

# Define color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the BROski launcher header."""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔══════════════════════════════════════════════╗")
    print("║             BROski Crypto Bot                ║")
    print("║               Unified Launcher               ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

def get_module_path(module_name):
    """Return the correct path to a module based on directory reorganization."""
    # Mapping of module names to their locations
    module_map = {
        # Core modules
        "BROski_Control_Center.py": os.path.join("core", "BROski_Control_Center.py"),
        "start_bot.py": os.path.join("core", "start_bot.py"),
        "direct_bot.py": os.path.join("core", "direct_bot.py"),
        
        # Monitor modules
        "bot_monitor.py": os.path.join("monitor", "bot_monitor.py"),
        "cli.py": os.path.join("monitor", "cli.py"),
        
        # UI modules
        "broski_dashboard.py": os.path.join("ui", "broski_dashboard.py"),
        
        # Utils
        "check_system.py": os.path.join("utils", "check_system.py"),
        "emergency_kill.py": os.path.join("utils", "emergency_kill.py"),
    }
    
    # Check if the module exists in the mapped location
    if module_name in module_map and os.path.exists(module_map[module_name]):
        return module_map[module_name]
    
    # Check if the module exists in the root directory
    if os.path.exists(module_name):
        return module_name
    
    # Default case: try both core directory and root
    potential_paths = [
        os.path.join("core", module_name),
        module_name
    ]
    
    for path in potential_paths:
        if os.path.exists(path):
            return path
    
    # If nothing found, return the original name and let Python handle the error
    return module_name

def run_module(module_name, wait=True):
    """Run a Python module and optionally wait for it to complete."""
    module_path = get_module_path(module_name)
    
    try:
        if wait:
            # Run and wait for completion
            print(f"{Colors.YELLOW}Running {module_name}...{Colors.ENDC}")
            subprocess.run([sys.executable, module_path], check=True)
            input(f"\n{Colors.GREEN}Process completed. Press Enter to continue...{Colors.ENDC}")
        else:
            # Run in background
            print(f"{Colors.YELLOW}Starting {module_name} in background...{Colors.ENDC}")
            if os.name == 'nt':  # Windows
                subprocess.Popen([sys.executable, module_path], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, module_path])
            print(f"{Colors.GREEN}Process started.{Colors.ENDC}")
            time.sleep(1)  # Brief pause
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error running {module_name}: {e}{Colors.ENDC}")
        input("Press Enter to continue...")

def display_main_menu():
    """Display the main menu options."""
    print_header()
    print(f"{Colors.BOLD}Select an option:{Colors.ENDC}")
    print(f"{Colors.BLUE}1. 🚀 Start BROski Control Center{Colors.ENDC}")
    print(f"{Colors.BLUE}2. 📊 Launch Dashboard{Colors.ENDC}")
    print(f"{Colors.BLUE}3. 🤖 Start Trading Bot{Colors.ENDC}")
    print(f"{Colors.BLUE}4. 👁️ Monitoring Tools{Colors.ENDC}")
    print(f"{Colors.BLUE}5. 🛠️ Utilities{Colors.ENDC}")
    print(f"{Colors.BLUE}6. 📋 Documentation{Colors.ENDC}")
    print(f"{Colors.RED}0. Exit{Colors.ENDC}")
    print()

def display_monitor_menu():
    """Display monitoring tools menu options."""
    print_header()
    print(f"{Colors.BOLD}Monitor & Logging Tools:{Colors.ENDC}")
    print(f"{Colors.BLUE}1. Launch Command-Line Monitor{Colors.ENDC}")
    print(f"{Colors.BLUE}2. Start Enhanced Bot Monitor{Colors.ENDC}")
    print(f"{Colors.BLUE}3. View Latest Logs{Colors.ENDC}")
    print(f"{Colors.BLUE}4. Check Trading Status{Colors.ENDC}")
    print(f"{Colors.RED}0. Back to Main Menu{Colors.ENDC}")
    print()

def display_utilities_menu():
    """Display utilities menu options."""
    print_header()
    print(f"{Colors.BOLD}Utilities:{Colors.ENDC}")
    print(f"{Colors.BLUE}1. System Health Check{Colors.ENDC}")
    print(f"{Colors.BLUE}2. Kill All Bot Processes{Colors.ENDC}")
    print(f"{Colors.BLUE}3. Backup Configuration{Colors.ENDC}")
    print(f"{Colors.BLUE}4. Create Desktop Shortcut{Colors.ENDC}")
    print(f"{Colors.BLUE}5. Run Maintenance Tasks{Colors.ENDC}")
    print(f"{Colors.RED}0. Back to Main Menu{Colors.ENDC}")
    print()

def display_documentation_menu():
    """Display documentation menu options."""
    print_header()
    print(f"{Colors.BOLD}Documentation:{Colors.ENDC}")
    
    # List markdown files
    docs_dir = "docs" if os.path.exists("docs") else "."
    md_files = []
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    
    # Sort alphabetically but put README.md first
    md_files.sort(key=lambda x: "" if os.path.basename(x) == "README.md" else os.path.basename(x))
    
    # Display menu options
    for i, file_path in enumerate(md_files, 1):
        filename = os.path.basename(file_path)
        print(f"{Colors.BLUE}{i}. {filename}{Colors.ENDC}")
    
    print(f"{Colors.RED}0. Back to Main Menu{Colors.ENDC}")
    print()
    
    return md_files

def open_markdown_file(file_path):
    """Open a markdown file using the appropriate method for the OS."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS, Linux
            if sys.platform == 'darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
    except Exception as e:
        print(f"{Colors.RED}Error opening file: {e}{Colors.ENDC}")
        
    input("Press Enter to continue...")

def view_logs():
    """Display the latest log file contents."""
    print_header()
    print(f"{Colors.BOLD}Latest Log Contents:{Colors.ENDC}\n")
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        print(f"{Colors.RED}No logs directory found.{Colors.ENDC}")
        input("Press Enter to continue...")
        return
    
    # Find the most recent log file
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith(".log")]
    if not log_files:
        print(f"{Colors.RED}No log files found.{Colors.ENDC}")
        input("Press Enter to continue...")
        return
    
    latest_log = max(log_files, key=os.path.getmtime)
    print(f"{Colors.YELLOW}Displaying: {os.path.basename(latest_log)}{Colors.ENDC}\n")
    
    # Display the last 20 lines of the log
    with open(latest_log, "r") as f:
        lines = f.readlines()
        for line in lines[-20:]:
            print(line.strip())
    
    print(f"\n{Colors.YELLOW}Showing last 20 lines of {os.path.basename(latest_log)}{Colors.ENDC}")
    input("\nPress Enter to continue...")

def handle_main_menu():
    """Handle user input for the main menu."""
    while True:
        display_main_menu()
        choice = input("Enter your choice [0-6]: ")
        
        if choice == '0':
            print(f"{Colors.YELLOW}Exiting BROski Launcher. Goodbye!{Colors.ENDC}")
            break
        elif choice == '1':
            run_module("BROski_Control_Center.py", wait=False)
        elif choice == '2':
            run_module("broski_dashboard.py", wait=False)
        elif choice == '3':
            run_module("direct_bot.py", wait=False)
        elif choice == '4':
            handle_monitor_menu()
        elif choice == '5':
            handle_utilities_menu()
        elif choice == '6':
            handle_documentation_menu()
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
            time.sleep(1)

def handle_monitor_menu():
    """Handle user input for the monitor menu."""
    while True:
        display_monitor_menu()
        choice = input("Enter your choice [0-4]: ")
        
        if choice == '0':
            break
        elif choice == '1':
            run_module("cli.py", wait=True)
        elif choice == '2':
            run_module("bot_monitor.py", wait=False)
        elif choice == '3':
            view_logs()
        elif choice == '4':
            run_module("check_trading_status.py", wait=True)
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
            time.sleep(1)

def handle_utilities_menu():
    """Handle user input for the utilities menu."""
    while True:
        display_utilities_menu()
        choice = input("Enter your choice [0-5]: ")
        
        if choice == '0':
            break
        elif choice == '1':
            run_module("check_system.py", wait=True)
        elif choice == '2':
            run_module("emergency_kill.py", wait=True)
        elif choice == '3':
            backup_config()
        elif choice == '4':
            create_shortcut()
        elif choice == '5':
            run_module("maintenance_dashboard.py", wait=False)
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
            time.sleep(1)

def handle_documentation_menu():
    """Handle user input for the documentation menu."""
    while True:
        md_files = display_documentation_menu()
        
        choice = input(f"Enter your choice [0-{len(md_files)}]: ")
        
        if choice == '0':
            break
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(md_files):
                open_markdown_file(md_files[choice_num - 1])
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
                time.sleep(1)
        except ValueError:
            print(f"{Colors.RED}Please enter a number.{Colors.ENDC}")
            time.sleep(1)

def backup_config():
    """Create a backup of the configuration file."""
    print_header()
    print(f"{Colors.YELLOW}Creating backup of configuration...{Colors.ENDC}")
    
    import datetime
    import shutil
    
    config_file = "config.json"
    if not os.path.exists(config_file):
        print(f"{Colors.RED}No config.json file found to backup.{Colors.ENDC}")
        input("Press Enter to continue...")
        return
    
    # Create backups directory if it doesn't exist
    backups_dir = "backups"
    os.makedirs(backups_dir, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backups_dir, f"config_{timestamp}.json")
    
    # Copy file
    try:
        shutil.copy2(config_file, backup_file)
        print(f"{Colors.GREEN}Config backed up successfully to: {backup_file}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Error backing up config: {e}{Colors.ENDC}")
    
    input("Press Enter to continue...")

def install_package(package):
    """Install a Python package if it's not already installed."""
    try:
        # Handle pywin32 differently as it's imported as win32com
        module_name = package.replace("pywin32", "win32com") if package == "pywin32" else package
        __import__(module_name)
        return True
    except ImportError:
        print(f"{Colors.YELLOW}Installing package: {package}...{Colors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return False
def create_shortcut():
    """Create a desktop shortcut for BROski."""
    print_header()
    print(f"{Colors.YELLOW}Creating BROski desktop shortcut...{Colors.ENDC}")
    
    try:
        if os.name == 'nt':  # Windows
            # Check if required packages are installed
            packages_installed = True
            for package in ["winshell", "pywin32"]:
                try:
                    __import__(package.replace("pywin32", "win32com"))
                except ImportError:
                    packages_installed = False
                    print(f"{Colors.YELLOW}Installing required package: {package}...{Colors.ENDC}")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            if not packages_installed:
                print(f"{Colors.YELLOW}Required packages have been installed. Please run 'Create Desktop Shortcut' again.{Colors.ENDC}")
            else:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                path = os.path.join(desktop, "BROski Bot.lnk")
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = os.path.abspath(__file__)
                shortcut.WorkingDirectory = os.getcwd()
                if os.path.exists("favicon.ico"):
                    shortcut.IconLocation = os.path.abspath("favicon.ico")
                shortcut.save()
                
                print(f"{Colors.GREEN}Shortcut created successfully on desktop!{Colors.ENDC}")
        else:
            print(f"{Colors.RED}Desktop shortcuts are only supported on Windows.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Error creating shortcut: {e}{Colors.ENDC}")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    # Check if we're running in a terminal that supports colors
    if os.name != 'nt':
        # Check if we're in a terminal that supports colors
        if not sys.stdout.isatty():
            # Disable colors
            for attr in dir(Colors):
                if not attr.startswith("__"):
                    setattr(Colors, attr, "")
    
    handle_main_menu()
handle_main_menu()
