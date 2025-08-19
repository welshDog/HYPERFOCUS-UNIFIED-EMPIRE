import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import shutil
import datetime
import json
from pathlib import Path

class BROskiMaintenanceDashboard:
    def __init__(self, root=None):
        """Initialize the maintenance dashboard"""
        # Create window
        self.root = tk.Tk() if root is None else root
        self.root.title("BROski Bot - Maintenance Dashboard")
        self.root.geometry("900x680")
        self.root.minsize(800, 600)
        
        # Set icon
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass  # Icon not found, use default
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a modern theme
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("Green.TButton", background="#4CAF50")
        self.style.configure("Red.TButton", background="#f44336")
        self.style.configure("Orange.TButton", background="#FF9800")
        self.style.configure("Blue.TButton", background="#2196F3")
        
        # Find all .bat files
        self.bat_files = self.find_bat_files()
        
        # Create main layout
        self.create_widgets()

    def find_bat_files(self):
        """Find all .bat files in the current directory"""
        bat_files = {}
        for file in os.listdir('.'):
            if file.endswith('.bat') and file != 'BROSKI_MAINTENANCE.bat':
                name = file.replace('.bat', '').replace('_', ' ')
                bat_files[name] = file
        return bat_files

    def create_widgets(self):
        """Create all dashboard widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        header_label = ttk.Label(
            header_frame,
            text="BROski Bot Maintenance Dashboard",
            font=("Arial", 18, "bold"),
            foreground="#336699"
        )
        header_label.pack(side="left")
        
        # Create the notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Tab 1: Quick Access
        quick_tab = ttk.Frame(notebook)
        notebook.add(quick_tab, text="Quick Access")
        self.create_quick_access_tab(quick_tab)
        
        # Tab 2: Maintenance Tools
        maint_tab = ttk.Frame(notebook)
        notebook.add(maint_tab, text="Maintenance")
        self.create_maintenance_tab(maint_tab)
        
        # Tab 3: Diagnostics
        diag_tab = ttk.Frame(notebook)
        notebook.add(diag_tab, text="Diagnostics")
        self.create_diagnostics_tab(diag_tab)
        
        # Tab 4: Backup & Restore
        backup_tab = ttk.Frame(notebook)
        notebook.add(backup_tab, text="Backup & Restore")
        self.create_backup_tab(backup_tab)
        
        # Status bar at bottom
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side="left")
        
        version_label = ttk.Label(status_frame, text="BROski v1.0")
        version_label.pack(side="right")
    
    def create_quick_access_tab(self, parent):
        """Create the Quick Access tab content"""
        # Main launchers section
        main_frame = ttk.LabelFrame(parent, text="Main BROski Tools", padding=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create button grid - 3 columns
        col, row = 0, 0
        max_cols = 3
        
        # Priority batch files - these are shown at the top
        priority_files = [
            "BROSKI_DASHBOARD", 
            "START_BOT", 
            "MONITOR_DIRECT", 
            "CHECK_BROSKI",
            "OPTIMIZE", 
            "BACKUP_BOT"
        ]
        
        # First add the priority files
        for name in priority_files:
            if name in self.bat_files.keys() or name + " BAT" in self.bat_files.keys():
                key = name if name in self.bat_files.keys() else name + " BAT"
                file = self.bat_files.get(key)
                if file:
                    button_style = "Green.TButton" if "DASHBOARD" in file or "START" in file else "TButton"
                    btn = ttk.Button(
                        main_frame,
                        text=key,
                        style=button_style,
                        command=lambda f=file: self.run_batch_file(f),
                        width=25
                    )
                    btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
        
        # Then add all other batch files
        for name, file in self.bat_files.items():
            # Skip if already added as a priority file
            if name in priority_files or any(pf in name for pf in priority_files):
                continue
                
            button_style = "TButton"  # Default style
            
            btn = ttk.Button(
                main_frame,
                text=name,
                style=button_style,
                command=lambda f=file: self.run_batch_file(f),
                width=25
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Adjust grid layout to be more responsive
        for i in range(max_cols):
            main_frame.columnconfigure(i, weight=1)
    
    def create_maintenance_tab(self, parent):
        """Create the Maintenance Tools tab content"""
        # Create a frame for the tools
        tools_frame = ttk.Frame(parent, padding=10)
        tools_frame.pack(fill="both", expand=True)
        
        # Create two columns layout
        left_frame = ttk.Frame(tools_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(tools_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Left column - Log Management
        log_frame = ttk.LabelFrame(left_frame, text="Log Management", padding=10)
        log_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Button(
            log_frame,
            text="View Bot Logs",
            command=self.view_bot_logs,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            log_frame,
            text="Clear Bot Logs",
            command=self.clear_bot_logs,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            log_frame,
            text="Export Logs",
            command=self.export_logs,
            width=25
        ).pack(fill="x", pady=5)
        
        # Left column - Process Management
        process_frame = ttk.LabelFrame(left_frame, text="Process Management", padding=10)
        process_frame.pack(fill="both", expand=True)
        
        ttk.Button(
            process_frame,
            text="View Running Processes",
            command=self.view_processes,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            process_frame,
            text="Kill All BROski Processes",
            style="Red.TButton",
            command=self.kill_all_processes,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            process_frame,
            text="Restart BROski Dashboard",
            command=self.restart_dashboard,
            width=25
        ).pack(fill="x", pady=5)
        
        # Right column - Configuration Management
        config_frame = ttk.LabelFrame(right_frame, text="Configuration", padding=10)
        config_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Button(
            config_frame,
            text="Edit Config File",
            command=self.edit_config,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            config_frame,
            text="Reset to Default Config",
            command=self.reset_config,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            config_frame,
            text="Validate Configuration",
            command=self.validate_config,
            width=25
        ).pack(fill="x", pady=5)
        
        # Right column - System Tools
        system_frame = ttk.LabelFrame(right_frame, text="System Tools", padding=10)
        system_frame.pack(fill="both", expand=True)
        
        ttk.Button(
            system_frame,
            text="Create Desktop Shortcut",
            command=self.create_shortcut,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            system_frame,
            text="System Information",
            command=self.show_system_info,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            system_frame,
            text="Check Internet Connection",
            command=self.check_internet,
            width=25
        ).pack(fill="x", pady=5)
    
    def create_diagnostics_tab(self, parent):
        """Create the Diagnostics tab content"""
        diag_frame = ttk.Frame(parent, padding=10)
        diag_frame.pack(fill="both", expand=True)
        
        # Create two columns layout
        left_frame = ttk.Frame(diag_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(diag_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Left column - System Checks
        check_frame = ttk.LabelFrame(left_frame, text="System Checks", padding=10)
        check_frame.pack(fill="both", expand=True)
        
        ttk.Button(
            check_frame,
            text="Run Health Check",
            style="Green.TButton",
            command=lambda: self.run_batch_file("CHECK_BROSKI.bat"),
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            check_frame,
            text="Check API Connection",
            command=self.check_api_connection,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            check_frame,
            text="Verify Dependencies",
            command=self.verify_dependencies,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            check_frame,
            text="Generate System Report",
            command=self.generate_system_report,
            width=25
        ).pack(fill="x", pady=5)
        
        # Right column - File Management
        file_frame = ttk.LabelFrame(right_frame, text="File Management", padding=10)
        file_frame.pack(fill="both", expand=True)
        
        ttk.Button(
            file_frame,
            text="Directory Tree",
            command=self.view_directory_tree,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            file_frame,
            text="Check Disk Space",
            command=self.check_disk_space,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            file_frame,
            text="Clean Temporary Files",
            command=self.clean_temp_files,
            width=25
        ).pack(fill="x", pady=5)
        
        # Output display for diagnostics
        output_frame = ttk.LabelFrame(diag_frame, text="Diagnostic Output", padding=10)
        output_frame.pack(fill="both", expand=True, pady=10)
        
        self.output_text = tk.Text(output_frame, height=10, wrap="word")
        self.output_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.output_text, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)
        
    def create_backup_tab(self, parent):
        """Create the Backup & Restore tab content"""
        backup_frame = ttk.Frame(parent, padding=10)
        backup_frame.pack(fill="both", expand=True)
        
        # Main backup section
        backup_section = ttk.LabelFrame(backup_frame, text="Backup", padding=10)
        backup_section.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Button(
            backup_section,
            text="Quick Backup",
            style="Blue.TButton",
            command=self.quick_backup,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            backup_section,
            text="Custom Backup...",
            command=self.custom_backup,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            backup_section,
            text="Schedule Regular Backups",
            command=self.schedule_backups,
            width=25
        ).pack(fill="x", pady=5)
        
        # Restore section
        restore_section = ttk.LabelFrame(backup_frame, text="Restore", padding=10)
        restore_section.pack(fill="both", expand=True, pady=(0, 10))
        
        ttk.Button(
            restore_section,
            text="Restore from Backup...",
            command=self.restore_backup,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            restore_section,
            text="View Backup History",
            command=self.view_backup_history,
            width=25
        ).pack(fill="x", pady=5)
        
        # Distribution section
        dist_section = ttk.LabelFrame(backup_frame, text="Distribution", padding=10)
        dist_section.pack(fill="both", expand=True)
        
        ttk.Button(
            dist_section,
            text="Create Distribution Package",
            command=lambda: self.run_batch_file("PACKAGE_BROSKI.bat") if os.path.exists("PACKAGE_BROSKI.bat") else self.create_dist_package(),
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            dist_section,
            text="Export Configuration",
            command=self.export_config,
            width=25
        ).pack(fill="x", pady=5)
        
        ttk.Button(
            dist_section,
            text="Import Configuration",
            command=self.import_config,
            width=25
        ).pack(fill="x", pady=5)
    
    # Event handlers and functions
    def run_batch_file(self, filename):
        """Run a batch file"""
        self.status_var.set(f"Running {filename}...")
        try:
            subprocess.Popen(["cmd", "/c", "start", filename], shell=True)
            self.status_var.set(f"Started {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run {filename}: {str(e)}")
            self.status_var.set("Error running batch file")
    
    def view_bot_logs(self):
        """View bot logs"""
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            messagebox.showerror("Error", "Logs directory not found")
            return
            
        # Try to open the logs directory
        try:
            os.startfile(log_dir)
            self.status_var.set("Opened logs directory")
        except Exception as e:
            try:
                # Alternative method
                subprocess.run(["explorer", log_dir], check=True)
                self.status_var.set("Opened logs directory")
            except Exception as e2:
                messagebox.showerror("Error", f"Failed to open logs: {str(e2)}")
                self.status_var.set("Error opening logs")
    
    def clear_bot_logs(self):
        """Clear bot log files"""
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            self.status_var.set("Created logs directory")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Clear Logs", 
            "This will clear all log files. Are you sure you want to continue?"
        )
        if not confirm:
            return
            
        try:
            count = 0
            for filename in os.listdir(log_dir):
                if filename.endswith('.log'):
                    log_path = os.path.join(log_dir, filename)
                    # Keep the file but clear its contents
                    with open(log_path, 'w') as f:
                        f.write(f"Log cleared on {datetime.datetime.now()}\n")
                    count += 1
                    
            self.status_var.set(f"Cleared {count} log files")
            messagebox.showinfo("Logs Cleared", f"Successfully cleared {count} log files")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear logs: {str(e)}")
            self.status_var.set("Error clearing logs")
    
    def export_logs(self):
        """Export logs to a zip file"""
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir) or not os.listdir(log_dir):
            messagebox.showerror("Error", "No logs found to export")
            return
            
        # Ask for export location
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"BROski_logs_{timestamp}.zip"
        export_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
            initialfile=default_filename,
            title="Export Logs"
        )
        
        if not export_path:
            return
            
        try:
            import zipfile
            
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(log_dir):
                    for file in files:
                        if file.endswith('.log'):
                            zipf.write(
                                os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file), os.getcwd())
                            )
                            
            self.status_var.set(f"Logs exported to {export_path}")
            messagebox.showinfo("Export Successful", f"Logs exported to:\n{export_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting logs: {str(e)}")
            self.status_var.set("Error exporting logs")
    
    def view_processes(self):
        """View running BROski processes"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Checking for BROski processes...\n\n")
        
        try:
            # Get all running Python processes
            output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq python.exe"], text=True)
            self.output_text.insert(tk.END, output)
            
            # Additional info for BROski-related windows
            self.output_text.insert(tk.END, "\nBROski Windows:\n")
            window_output = subprocess.check_output(["tasklist", "/FI", "WINDOWTITLE eq BROski*"], text=True)
            self.output_text.insert(tk.END, window_output)
            
            self.status_var.set("Viewed running processes")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error getting process list: {str(e)}")
            self.status_var.set("Error getting processes")
    
    def kill_all_processes(self):
        """Kill all BROski-related processes"""
        confirm = messagebox.askyesno(
            "Confirm Kill Processes", 
            "This will terminate all BROski processes. Are you sure?"
        )
        if not confirm:
            return
            
        try:
            # Kill by window title
            subprocess.run(["taskkill", "/F", "/FI", "WINDOWTITLE eq BROski*"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # For thoroughness, also try to kill python processes with BROski in their command line
            # This is more aggressive and might kill this dashboard too
            try:
                subprocess.run(["wmic", "process", "where", "name='python.exe'", "delete"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
                
            self.status_var.set("All BROski processes terminated")
            messagebox.showinfo("Processes Terminated", "All BROski processes have been terminated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to kill processes: {str(e)}")
            self.status_var.set("Error killing processes")
    
    def restart_dashboard(self):
        """Restart the BROski dashboard"""
        confirm = messagebox.askyesno(
            "Confirm Restart", 
            "This will close the current dashboard and start a new one. Continue?"
        )
        if not confirm:
            return
            
        try:
            # Start the dashboard in a new process
            subprocess.Popen(["cmd", "/c", "start", "BROSKI_DASHBOARD.bat"], shell=True)
            
            # Exit this script (which will close the maintenance dashboard)
            self.status_var.set("Restarting dashboard...")
            self.root.after(1000, self.root.destroy)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart dashboard: {str(e)}")
            self.status_var.set("Error restarting dashboard")
    
    def edit_config(self):
        """Open config.json in the default text editor"""
        config_path = os.path.join(os.getcwd(), "config.json")
        if not os.path.exists(config_path):
            messagebox.showerror("Error", "config.json not found")
            return
            
        try:
            os.startfile(config_path)
            self.status_var.set("Opened config.json")
        except Exception as e:
            try:
                subprocess.run(["notepad", config_path], check=True)
                self.status_var.set("Opened config.json")
            except Exception as e2:
                messagebox.showerror("Error", f"Failed to open config.json: {str(e2)}")
                self.status_var.set("Error opening config")
    
    def reset_config(self):
        """Reset config to default"""
        confirm = messagebox.askyesno(
            "Confirm Reset", 
            "This will reset your configuration to default values.\n\n" +
            "Your API keys will be preserved. Continue?"
        )
        if not confirm:
            return
            
        config_path = os.path.join(os.getcwd(), "config.json")
        example_path = os.path.join(os.getcwd(), "config.example.json")
        
        if not os.path.exists(config_path):
            if not os.path.exists(example_path):
                messagebox.showerror("Error", "No configuration or example found")
                return
                
            # Just copy example if no config exists
            shutil.copy(example_path, config_path)
            self.status_var.set("Created new config.json")
            messagebox.showinfo("Config Created", "Created new configuration from example")
            return
            
        try:
            # Read current config to preserve API keys
            with open(config_path, 'r') as f:
                current_config = json.load(f)
                
            api_key = current_config.get("exchange", {}).get("api_key", "")
            api_secret = current_config.get("exchange", {}).get("api_secret", "")
            
            # Read example config
            with open(example_path, 'r') as f:
                example_config = json.load(f)
                
            # Preserve API keys
            example_config["exchange"]["api_key"] = api_key
            example_config["exchange"]["api_secret"] = api_secret
            
            # Backup current config
            backup_path = f"{config_path}.bak"
            shutil.copy(config_path, backup_path)
            
            # Write new config
            with open(config_path, 'w') as f:
                json.dump(example_config, f, indent=2)
                
            self.status_var.set("Configuration reset")
            messagebox.showinfo(
                "Config Reset", 
                f"Configuration reset to default values.\nAPI keys preserved.\nBackup saved to {backup_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset config: {str(e)}")
            self.status_var.set("Error resetting config")
    
    def validate_config(self):
        """Validate the configuration file"""
        config_path = os.path.join(os.getcwd(), "config.json")
        if not os.path.exists(config_path):
            messagebox.showerror("Error", "config.json not found")
            return
            
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Basic validation
            issues = []
            
            # Check for required sections
            required_sections = ["exchange", "trading", "strategies"]
            for section in required_sections:
                if section not in config:
                    issues.append(f"Missing required section: {section}")
            
            # Check API keys
            if "exchange" in config:
                api_key = config["exchange"].get("api_key", "")
                api_secret = config["exchange"].get("api_secret", "")
                
                if not api_key or api_key == "YOUR_MEXC_API_KEY_HERE":
                    issues.append("API key is missing or using default value")
                    
                if not api_secret or api_secret == "YOUR_MEXC_API_SECRET_HERE":
                    issues.append("API secret is missing or using default value")
            
            # Check trading settings
            if "trading" in config:
                trading = config["trading"]
                if "base_symbol" not in trading or not trading["base_symbol"]:
                    issues.append("Missing base_symbol in trading settings")
                
                if "quote_symbol" not in trading or not trading["quote_symbol"]:
                    issues.append("Missing quote_symbol in trading settings")
            
            # Check strategies settings
            if "strategies" in config:
                strategies = config["strategies"]
                if "active_strategy" not in strategies:
                    issues.append("Missing active_strategy in strategies settings")
                else:
                    active = strategies["active_strategy"]
                    if active not in strategies:
                        issues.append(f"Active strategy '{active}' is not defined")
            
            # Display results
            self.output_text.delete(1.0, tk.END)
            
            if not issues:
                self.output_text.insert(tk.END, "✅ Configuration validated successfully!\n\n")
                self.output_text.insert(tk.END, f"Trading Pair: {config['trading']['base_symbol']}/{config['trading']['quote_symbol']}\n")
                self.output_text.insert(tk.END, f"Active Strategy: {config['strategies']['active_strategy']}\n")
                self.output_text.insert(tk.END, f"Auto-Trade: {'Enabled' if config['trading'].get('auto_trade', False) else 'Disabled'}\n")
                self.status_var.set("Configuration validated successfully")
            else:
                self.output_text.insert(tk.END, "❌ Configuration has issues:\n\n")
                for i, issue in enumerate(issues, 1):
                    self.output_text.insert(tk.END, f"{i}. {issue}\n")
                self.status_var.set("Configuration has issues")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate config: {str(e)}")
            self.status_var.set("Error validating config")
    
    def check_api_connection(self):
        """Test API connection to exchange"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Testing API connection to MEXC...\n\n")
        self.status_var.set("Testing API connection...")
        
        try:
            result = subprocess.run(["python", "check_system.py", "--api-only"], 
                                   capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                self.output_text.insert(tk.END, "✅ API connection successful!\n\n")
                self.output_text.insert(tk.END, result.stdout)
                self.status_var.set("API connection successful")
            else:
                self.output_text.insert(tk.END, "❌ API connection failed!\n\n")
                self.output_text.insert(tk.END, result.stderr)
                self.status_var.set("API connection failed")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error testing API connection: {str(e)}")
            self.status_var.set("Error testing API connection")
    
    def verify_dependencies(self):
        """Verify Python dependencies"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Checking Python dependencies...\n\n")
        self.status_var.set("Verifying dependencies...")
        
        try:
            # Try to run a simple command to check dependencies
            result = subprocess.run(["pip", "list"], capture_output=True, text=True)
            
            # Look for required packages
            required_packages = ['ccxt', 'pandas', 'colorama', 'matplotlib', 'tk']
            installed = result.stdout.lower()
            
            missing = []
            for package in required_packages:
                if package.lower() not in installed:
                    missing.append(package)
            
            if not missing:
                self.output_text.insert(tk.END, "✅ All required dependencies are installed!\n\n")
                self.output_text.insert(tk.END, "Required packages found:\n")
                for package in required_packages:
                    self.output_text.insert(tk.END, f"- {package}\n")
                self.status_var.set("All dependencies installed")
            else:
                self.output_text.insert(tk.END, "❌ Missing dependencies:\n\n")
                for package in missing:
                    self.output_text.insert(tk.END, f"- {package}\n")
                    
                install_cmd = f"pip install {' '.join(missing)}"
                self.output_text.insert(tk.END, f"\nYou can install missing packages with:\n{install_cmd}\n")
                self.status_var.set("Missing dependencies found")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error checking dependencies: {str(e)}")
            self.status_var.set("Error checking dependencies")
    
    def generate_system_report(self):
        """Generate a comprehensive system report"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Generating BROski Bot system report...\n\n")
        self.status_var.set("Generating system report...")
        
        report_data = {}
        
        # System info
        try:
            import platform
            report_data["OS"] = platform.platform()
            report_data["Python"] = platform.python_version()
            report_data["Processor"] = platform.processor()
        except:
            report_data["System"] = "Could not retrieve system information"
        
        # Bot info
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            
            report_data["Trading Pair"] = f"{config['trading']['base_symbol']}/{config['trading']['quote_symbol']}"
            report_data["Active Strategy"] = config['strategies']['active_strategy']
            report_data["Auto-Trade"] = "Enabled" if config['trading'].get('auto_trade', False) else "Disabled"
        except:
            report_data["Bot Config"] = "Could not retrieve configuration"
        
        # Directory info
        report_data["Log Files"] = []
        try:
            log_dir = os.path.join(os.getcwd(), "logs")
            if os.path.exists(log_dir):
                log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
                for log_file in log_files:
                    path = os.path.join(log_dir, log_file)
                    size = os.path.getsize(path) / 1024  # KB
                    modified = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                    report_data["Log Files"].append({
                        "name": log_file,
                        "size_kb": f"{size:.2f} KB",
                        "modified": modified
                    })
        except:
            report_data["Log Files"].append("Could not retrieve log files")
        
        # Display report
        self.output_text.insert(tk.END, "BROski Bot System Report\n")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.output_text.insert(tk.END, "System Information:\n")
        for key, value in {k:v for k,v in report_data.items() if k in ["OS", "Python", "Processor", "System"]}.items():
            self.output_text.insert(tk.END, f"- {key}: {value}\n")
        
        self.output_text.insert(tk.END, "\nBot Configuration:\n")
        for key, value in {k:v for k,v in report_data.items() if k in ["Trading Pair", "Active Strategy", "Auto-Trade", "Bot Config"]}.items():
            self.output_text.insert(tk.END, f"- {key}: {value}\n")
        
        self.output_text.insert(tk.END, "\nLog Files:\n")
        if isinstance(report_data["Log Files"], list) and report_data["Log Files"]:
            for log in report_data["Log Files"]:
                if isinstance(log, dict):
                    self.output_text.insert(tk.END, f"- {log['name']} ({log['size_kb']}, modified: {log['modified']})\n")
                else:
                    self.output_text.insert(tk.END, f"- {log}\n")
        else:
            self.output_text.insert(tk.END, "- No log files found\n")
        
        # Add report generated timestamp
        self.output_text.insert(tk.END, f"\nReport generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.status_var.set("System report generated")
    
    def view_directory_tree(self):
        """Display directory tree"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Generating directory tree...\n\n")
        self.status_var.set("Generating directory tree...")
        
        try:
            result = subprocess.run(["tree", "/F", "/A", "."], capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                tree_output = result.stdout
                self.output_text.insert(tk.END, tree_output)
                self.status_var.set("Directory tree generated")
            else:
                self.output_text.insert(tk.END, "Could not generate directory tree.\n")
                self.output_text.insert(tk.END, result.stderr)
                self.status_var.set("Failed to generate directory tree")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error generating directory tree: {str(e)}\n")
            
            # Fallback to manual directory listing
            self.output_text.insert(tk.END, "Falling back to basic directory listing:\n\n")
            try:
                for root, dirs, files in os.walk("."):
                    level = root.replace(".", "").count(os.sep)
                    indent = " " * 4 * level
                    self.output_text.insert(tk.END, f"{indent}{os.path.basename(root)}/\n")
                    sub_indent = " " * 4 * (level + 1)
                    for file in files:
                        self.output_text.insert(tk.END, f"{sub_indent}{file}\n")
                self.status_var.set("Basic directory listing completed")
            except Exception as e2:
                self.output_text.insert(tk.END, f"Error listing directory: {str(e2)}")
                self.status_var.set("Error listing directory")
    
    def check_disk_space(self):
        """Check available disk space"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Checking disk space...\n\n")
        self.status_var.set("Checking disk space...")
        
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(os.getcwd()), 
                    None, 
                    ctypes.pointer(total_bytes),
                    ctypes.pointer(free_bytes)
                )
                
                free_gb = free_bytes.value / (1024**3)
                total_gb = total_bytes.value / (1024**3)
                used_gb = total_gb - free_gb
                percent_used = (used_gb / total_gb) * 100
                
                self.output_text.insert(tk.END, f"Drive containing BROski Bot:\n\n")
                self.output_text.insert(tk.END, f"Total Space: {total_gb:.2f} GB\n")
                self.output_text.insert(tk.END, f"Used Space: {used_gb:.2f} GB\n")
                self.output_text.insert(tk.END, f"Free Space: {free_gb:.2f} GB\n")
                self.output_text.insert(tk.END, f"Percent Used: {percent_used:.1f}%\n")
                
                # BROski folder size
                total_size = 0
                for dirpath, dirnames, filenames in os.walk('.'):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            total_size += os.path.getsize(fp)
                
                folder_mb = total_size / (1024**2)
                self.output_text.insert(tk.END, f"\nBROski Bot folder size: {folder_mb:.2f} MB\n")
                
                self.status_var.set("Disk space check complete")
            else:  # Unix-like
                self.output_text.insert(tk.END, "Disk space check not implemented for this OS.")
                self.status_var.set("Disk space check not implemented")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error checking disk space: {str(e)}")
            self.status_var.set("Error checking disk space")
    
    def clean_temp_files(self):
        """Clean temporary files"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Cleaning temporary files...\n\n")
        self.status_var.set("Cleaning temporary files...")
        
        cleaned_count = 0
        
        try:
            # Clean up log files over 7 days old
            log_dir = os.path.join(os.getcwd(), "logs")
            if os.path.exists(log_dir):
                self.output_text.insert(tk.END, "Cleaning old log files...\n")
                now = datetime.datetime.now()
                for file in os.listdir(log_dir):
                    if file.endswith('.log'):
                        file_path = os.path.join(log_dir, file)
                        file_age = now - datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        if file_age.days > 7:
                            try:
                                os.remove(file_path)
                                self.output_text.insert(tk.END, f"- Deleted old log: {file}\n")
                                cleaned_count += 1
                            except Exception as e:
                                self.output_text.insert(tk.END, f"- Could not delete {file}: {str(e)}\n")
            
            # Clean up __pycache__ directories
            self.output_text.insert(tk.END, "\nCleaning Python cache files...\n")
            for root, dirs, files in os.walk('.'):
                if '__pycache__' in dirs:
                    try:
                        pycache_dir = os.path.join(root, '__pycache__')
                        shutil.rmtree(pycache_dir)
                        self.output_text.insert(tk.END, f"- Deleted: {pycache_dir}\n")
                        cleaned_count += 1
                    except Exception as e:
                        self.output_text.insert(tk.END, f"- Could not delete {pycache_dir}: {str(e)}\n")
                
                for file in files:
                    if file.endswith('.pyc'):
                        try:
                            pyc_file = os.path.join(root, file)
                            os.remove(pyc_file)
                            self.output_text.insert(tk.END, f"- Deleted: {pyc_file}\n")
                            cleaned_count += 1
                        except Exception as e:
                            self.output_text.insert(tk.END, f"- Could not delete {pyc_file}: {str(e)}\n")
            
            self.output_text.insert(tk.END, f"\nCleaning complete! Removed {cleaned_count} files/directories.\n")
            self.status_var.set(f"Cleaned {cleaned_count} temporary files")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error during cleanup: {str(e)}")
            self.status_var.set("Error cleaning temporary files")
    
    def quick_backup(self):
        """Perform quick backup of BROski Bot"""
        # Create backup directory if it doesn't exist
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create timestamp for backup name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"BROski_Backup_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            # Run the backup script or use direct method
            if os.path.exists("BACKUP_BOT.bat"):
                self.run_batch_file("BACKUP_BOT.bat")
                self.status_var.set("Quick backup started")
            else:
                os.makedirs(backup_path, exist_ok=True)
                
                # Copy important files
                files_to_backup = [
                    "config.json",
                    "logs",
                    "strategies",
                    "*.py",
                    "*.bat",
                    "*.md"
                ]
                
                for pattern in files_to_backup:
                    if "*" in pattern:
                        # Use glob for wildcard patterns
                        import glob
                        for file in glob.glob(pattern):
                            if os.path.isfile(file):
                                shutil.copy2(file, backup_path)
                    elif os.path.isdir(pattern):
                        # Copy directories recursively
                        dest_dir = os.path.join(backup_path, os.path.basename(pattern))
                        shutil.copytree(pattern, dest_dir, dirs_exist_ok=True)
                    elif os.path.isfile(pattern):
                        # Copy single file
                        shutil.copy2(pattern, backup_path)
                        
                messagebox.showinfo("Backup Complete", f"Backup created at: {backup_path}")
                self.status_var.set(f"Quick backup completed: {backup_name}")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
            self.status_var.set("Error creating backup")
    
    def custom_backup(self):
        """Create a custom backup with selected files"""
        # Ask for backup location
        backup_dir = filedialog.askdirectory(title="Select Backup Location")
        if not backup_dir:
            return
            
        # Create timestamp for backup name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"BROski_Custom_Backup_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Create backup options dialog
            backup_options = tk.Toplevel(self.root)
            backup_options.title("Backup Options")
            backup_options.geometry("400x500")
            backup_options.transient(self.root)
            backup_options.grab_set()
            
            ttk.Label(backup_options, text="Select items to backup:", font=("Arial", 12)).pack(pady=10)
            
            # Checkboxes for backup options
            config_var = tk.BooleanVar(value=True)
            logs_var = tk.BooleanVar(value=True)
            strategies_var = tk.BooleanVar(value=True)
            scripts_var = tk.BooleanVar(value=True)
            bat_files_var = tk.BooleanVar(value=True)
            docs_var = tk.BooleanVar(value=True)
            
            ttk.Checkbutton(backup_options, text="Configuration (config.json)", variable=config_var).pack(anchor="w", padx=20, pady=5)
            ttk.Checkbutton(backup_options, text="Log Files (logs/)", variable=logs_var).pack(anchor="w", padx=20, pady=5)
            ttk.Checkbutton(backup_options, text="Strategy Files (strategies/)", variable=strategies_var).pack(anchor="w", padx=20, pady=5)
            ttk.Checkbutton(backup_options, text="Python Scripts (*.py)", variable=scripts_var).pack(anchor="w", padx=20, pady=5)
            ttk.Checkbutton(backup_options, text="Batch Files (*.bat)", variable=bat_files_var).pack(anchor="w", padx=20, pady=5)
            ttk.Checkbutton(backup_options, text="Documentation (*.md)", variable=docs_var).pack(anchor="w", padx=20, pady=5)
            
            def perform_backup():
                try:
                    # Copy selected items
                    if config_var.get() and os.path.exists("config.json"):
                        shutil.copy2("config.json", backup_path)
                    
                    if logs_var.get() and os.path.exists("logs"):
                        shutil.copytree("logs", os.path.join(backup_path, "logs"), dirs_exist_ok=True)
                        
                    if strategies_var.get() and os.path.exists("strategies"):
                        shutil.copytree("strategies", os.path.join(backup_path, "strategies"), dirs_exist_ok=True)
                    
                    if scripts_var.get():
                        for file in os.listdir('.'):
                            if file.endswith('.py') and os.path.isfile(file):
                                shutil.copy2(file, backup_path)
                    
                    if bat_files_var.get():
                        for file in os.listdir('.'):
                            if file.endswith('.bat') and os.path.isfile(file):
                                shutil.copy2(file, backup_path)
                    
                    if docs_var.get():
                        for file in os.listdir('.'):
                            if file.endswith('.md') and os.path.isfile(file):
                                shutil.copy2(file, backup_path)
                    
                    messagebox.showinfo("Backup Complete", f"Backup created successfully at:\n{backup_path}")
                    self.status_var.set(f"Custom backup completed: {backup_name}")
                    backup_options.destroy()
                except Exception as e:
                    messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
                    self.status_var.set("Error creating custom backup")
            
            # Buttons
            buttons_frame = ttk.Frame(backup_options)
            buttons_frame.pack(pady=20)
            
            ttk.Button(buttons_frame, text="Backup", command=perform_backup).pack(side="left", padx=10)
            ttk.Button(buttons_frame, text="Cancel", command=backup_options.destroy).pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare backup: {str(e)}")
            self.status_var.set("Error preparing backup")
    
    def schedule_backups(self):
        """Configure scheduled backups"""
        # Create scheduler dialog
        scheduler = tk.Toplevel(self.root)
        scheduler.title("Schedule Regular Backups")
        scheduler.geometry("450x350")
        scheduler.transient(self.root)
        scheduler.grab_set()
        
        ttk.Label(scheduler, text="Schedule Automatic Backups", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(scheduler, text="Windows Task Scheduler will be used to create regular backups.").pack(pady=5)
        
        # Frequency options
        frequency_frame = ttk.LabelFrame(scheduler, text="Backup Frequency", padding=10)
        frequency_frame.pack(fill="x", padx=20, pady=10)
        
        frequency_var = tk.StringVar(value="daily")
        ttk.Radiobutton(frequency_frame, text="Daily", variable=frequency_var, value="daily").pack(anchor="w")
        ttk.Radiobutton(frequency_frame, text="Weekly", variable=frequency_var, value="weekly").pack(anchor="w")
        ttk.Radiobutton(frequency_frame, text="Monthly", variable=frequency_var, value="monthly").pack(anchor="w")
        
        # Backup location
        location_frame = ttk.LabelFrame(scheduler, text="Backup Location", padding=10)
        location_frame.pack(fill="x", padx=20, pady=10)
        
        path_var = tk.StringVar(value=os.path.join(os.getcwd(), "backups"))
        path_entry = ttk.Entry(location_frame, textvariable=path_var, width=40)
        path_entry.pack(side="left", padx=5)
        
        def browse_path():
            path = filedialog.askdirectory(title="Select Backup Directory")
            if path:
                path_var.set(path)
        
        ttk.Button(location_frame, text="Browse", command=browse_path).pack(side="left")
        
        def create_schedule():
            try:
                frequency = frequency_var.get()
                location = path_var.get()
                
                # Ensure backup directory exists
                os.makedirs(location, exist_ok=True)
                
                # Create the batch file that will perform the backup
                backup_script = os.path.join(os.getcwd(), "scheduled_backup.bat")
                with open(backup_script, 'w') as f:
                    f.write("@echo off\n")
                    f.write("echo BROski Scheduled Backup - %date% %time%\n")
                    f.write(f"cd /d {os.getcwd()}\n")
                    f.write("set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%\n")
                    f.write("set TIMESTAMP=%TIMESTAMP: =0%\n")
                    f.write(f"set BACKUP_DIR={location}\\BROski_Backup_%TIMESTAMP%\n")
                    f.write("mkdir %BACKUP_DIR%\n")
                    f.write("xcopy config.json %BACKUP_DIR%\\ /Y\n")
                    f.write("xcopy strategies %BACKUP_DIR%\\strategies /E /I /H /Y\n")
                    f.write("xcopy logs %BACKUP_DIR%\\logs /E /I /H /Y\n")
                    f.write("xcopy *.py %BACKUP_DIR%\\ /Y\n")
                    f.write("xcopy *.md %BACKUP_DIR%\\ /Y\n")
                    f.write("echo Backup completed to %BACKUP_DIR%\n")
                
                # Create the task based on frequency
                if frequency == "daily":
                    cmd = f'schtasks /create /tn "BROski_Daily_Backup" /tr "{backup_script}" /sc daily /st 03:00'
                    task_name = "Daily"
                elif frequency == "weekly":
                    cmd = f'schtasks /create /tn "BROski_Weekly_Backup" /tr "{backup_script}" /sc weekly /st 03:00 /d SUN'
                    task_name = "Weekly (Sunday)"
                else:  # monthly
                    cmd = f'schtasks /create /tn "BROski_Monthly_Backup" /tr "{backup_script}" /sc monthly /st 03:00 /d 1'
                    task_name = "Monthly (1st)"
                
                # Execute the command
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"{task_name} backups have been scheduled.\n\nBackups will be stored in:\n{location}")
                    scheduler.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to create scheduled task:\n{result.stderr}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set up scheduled backups: {str(e)}")
        
        # Buttons
        buttons_frame = ttk.Frame(scheduler)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="Create Schedule", command=create_schedule).pack(side="left", padx=10)
        ttk.Button(buttons_frame, text="Cancel", command=scheduler.destroy).pack(side="left", padx=10)
    
    def restore_backup(self):
        """Restore from a backup"""
        # Ask for backup directory
        backup_path = filedialog.askdirectory(title="Select Backup Directory to Restore")
        if not backup_path:
            return
            
        # Check if it's a valid backup directory
        required_files = ["config.json", "strategies", "*.py"]
        missing_items = []
        
        for item in required_files:
            if "*" in item:
                # Check if any matching files exist
                import glob
                matches = glob.glob(os.path.join(backup_path, item))
                if not matches:
                    missing_items.append(item)
            elif not os.path.exists(os.path.join(backup_path, item)):
                missing_items.append(item)
        
        if missing_items:
            messagebox.showerror("Invalid Backup", 
                f"The selected directory does not appear to be a valid BROski backup.\n\n"
                f"Missing items: {', '.join(missing_items)}")
            return
        
        # Confirm restore
        confirm = messagebox.askyesno("Confirm Restore", 
            "This will restore BROski Bot from the selected backup.\n\n"
            "Current files may be overwritten. Continue?")
        
        if not confirm:
            return
        
        try:
            # Create a backup of current config before restoring
            if os.path.exists("config.json"):
                shutil.copy2("config.json", "config.json.before_restore")
            
            # Copy files from backup to current directory
            for item in os.listdir(backup_path):
                item_path = os.path.join(backup_path, item)
                if os.path.isdir(item_path):
                    shutil.copytree(item_path, item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item_path, ".")
            
            messagebox.showinfo("Restore Complete", "BROski Bot has been restored from the backup.")
            self.status_var.set("Restore completed")
        except Exception as e:
            messagebox.showerror("Restore Error", f"Failed to restore backup: {str(e)}")
            self.status_var.set("Error restoring backup")
    
    def view_backup_history(self):
        """View backup history"""
        backup_dir = os.path.join(os.getcwd(), "backups")
        if not os.path.exists(backup_dir):
            messagebox.showerror("Error", "No backup history found")
            return
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Backup History:\n\n")
        
        try:
            for backup in os.listdir(backup_dir):
                backup_path = os.path.join(backup_dir, backup)
                if os.path.isdir(backup_path):
                    self.output_text.insert(tk.END, f"- {backup}\n")
            
            self.status_var.set("Viewed backup history")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error viewing backup history: {str(e)}")
            self.status_var.set("Error viewing backup history")
    
    def create_shortcut(self):
        """Create a desktop shortcut for the dashboard"""
        try:
            # Try to import required modules
            winshell = None  # Initialize as None to check later
            try:
                # Dynamic import to avoid IDE errors
                winshell = __import__('winshell')
                win32com_client = __import__('win32com.client', fromlist=['Dispatch'])
                Dispatch = win32com_client.Dispatch
            except ImportError:
                # Try to install the missing packages automatically
                self.status_var.set("Installing required packages...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "winshell"])
                    # Try importing again after installation
                    winshell = __import__('winshell')
                    win32com_client = __import__('win32com.client', fromlist=['Dispatch'])
                    Dispatch = win32com_client.Dispatch
                    self.status_var.set("Required packages installed successfully")
                except Exception as install_error:
                    # Offer manual installation instructions
                    response = messagebox.askyesno("Missing Package", 
                        "The required packages for creating shortcuts are not installed.\n\n"
                        "Do you want to install them now?\n"
                        "(This will run: pip install pywin32 winshell)")
                    
                    if response:
                        # Open terminal with installation command
                        os.system(f'start cmd /k {sys.executable} -m pip install pywin32 winshell')
                    
                    self.status_var.set("Error: Missing shortcut libraries")
                    return
                
            if winshell is None:
                # If we got here and winshell is still None, something went wrong
                raise ImportError("Failed to import winshell after installation attempt")
                
            desktop = winshell.desktop()
            path = os.path.join(desktop, "BROski Dashboard.lnk")
            target = os.path.join(os.getcwd(), "BROSKI_DASHBOARD.bat")
            wDir = os.getcwd()
            icon = os.path.join(os.getcwd(), "favicon.ico")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            
            messagebox.showinfo("Shortcut Created", "A shortcut has been created on your desktop.")
            self.status_var.set("Shortcut created")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create shortcut: {str(e)}")
            self.status_var.set("Error creating shortcut")
    
    def show_system_info(self):
        """Show system information"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "System Information:\n\n")
        
        try:
            import platform
            self.output_text.insert(tk.END, f"System: {platform.system()}\n")
            self.output_text.insert(tk.END, f"Node Name: {platform.node()}\n")
            self.output_text.insert(tk.END, f"Release: {platform.release()}\n")
            self.output_text.insert(tk.END, f"Version: {platform.version()}\n")
            self.output_text.insert(tk.END, f"Machine: {platform.machine()}\n")
            self.output_text.insert(tk.END, f"Processor: {platform.processor()}\n")
            self.output_text.insert(tk.END, f"Python Version: {platform.python_version()}\n")
            
            self.status_var.set("System information displayed")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error retrieving system information: {str(e)}")
            self.status_var.set("Error retrieving system information")
    
    def check_internet(self):
        """Check internet connection"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Checking internet connection...\n\n")
        self.status_var.set("Checking internet connection...")
        
        try:
            import requests
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                self.output_text.insert(tk.END, "✅ Internet connection is active.\n")
                self.status_var.set("Internet connection active")
            else:
                self.output_text.insert(tk.END, "❌ Internet connection is not active.\n")
                self.status_var.set("Internet connection not active")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error checking internet connection: {str(e)}")
            self.status_var.set("Error checking internet connection")
    
    def create_dist_package(self):
        """Create a distribution package"""
        dist_dir = os.path.join(os.getcwd(), "dist")
        os.makedirs(dist_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"BROski_Distribution_{timestamp}.zip"
        package_path = os.path.join(dist_dir, package_name)
        
        try:
            import zipfile
            
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(os.getcwd()):
                    for file in files:
                        if file.endswith(('.py', '.bat', '.md', 'config.json', 'favicon.ico')):
                            zipf.write(
                                os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file), os.getcwd())
                            )
            
            messagebox.showinfo("Package Created", f"Distribution package created at:\n{package_path}")
            self.status_var.set(f"Distribution package created: {package_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create distribution package: {str(e)}")
            self.status_var.set("Error creating distribution package")
    
    def export_config(self):
        """Export configuration to a file"""
        config_path = os.path.join(os.getcwd(), "config.json")
        if not os.path.exists(config_path):
            messagebox.showerror("Error", "config.json not found")
            return
        
        export_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="BROski_config.json",
            title="Export Configuration"
        )
        
        if not export_path:
            return
        
        try:
            shutil.copy2(config_path, export_path)
            messagebox.showinfo("Export Successful", f"Configuration exported to:\n{export_path}")
            self.status_var.set("Configuration exported")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export configuration: {str(e)}")
            self.status_var.set("Error exporting configuration")
    
    def import_config(self):
        """Import configuration from a file"""
        import_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Configuration"
        )
        
        if not import_path:
            return
        
        try:
            config_path = os.path.join(os.getcwd(), "config.json")
            shutil.copy2(import_path, config_path)
            messagebox.showinfo("Import Successful", f"Configuration imported from:\n{import_path}")
            self.status_var.set("Configuration imported")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import configuration: {str(e)}")
            self.status_var.set("Error importing configuration")

if __name__ == "__main__":
    app = BROskiMaintenanceDashboard()
    app.root.mainloop()
