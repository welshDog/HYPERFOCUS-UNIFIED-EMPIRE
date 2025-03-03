import subprocess
import sys
import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import json
import shutil
from pathlib import Path
import threading

class BROskiSetupWizard:
    def __init__(self):
        # Create setup wizard window
        self.root = tk.Tk()
        self.root.title("BROski Bot - Setup Wizard")
        self.root.geometry("700x500")
        self.root.minsize(600, 450)
        
        # Set icon
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass  # Icon not found, use default
        
        # Configure style
        self.style = ttk.Style()
        if os.name == "nt":  # Windows
            self.style.theme_use("vista")
        else:
            self.style.theme_use("clam")
        
        self.style.configure("TCheckbutton", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("Green.TButton", background="#4CAF50")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_label = ttk.Label(
            main_frame,
            text="BROski Bot - Installation Wizard",
            font=("Arial", 16, "bold"),
            foreground="#336699"
        )
        header_label.pack(pady=(0, 15))
        
        # System info
        sys_frame = ttk.LabelFrame(main_frame, text="System Information", padding=10)
        sys_frame.pack(fill="x", pady=(0, 15))
        
        sys_info = f"Python: {sys.version.split()[0]}\n"
        sys_info += f"System: {platform.system()} {platform.release()}\n"
        sys_info += f"Path: {os.getcwd()}"
        
        sys_label = ttk.Label(sys_frame, text=sys_info, justify="left")
        sys_label.pack(anchor="w")
        
        # Required packages frame
        req_frame = ttk.LabelFrame(main_frame, text="Required Packages (Recommended)", padding=10)
        req_frame.pack(fill="x", pady=(0, 15))
        
        # Required packages checkboxes
        self.req_packages = {
            "ccxt": {"var": tk.BooleanVar(value=True), "desc": "Cryptocurrency Exchange Trading Library"},
            "pandas": {"var": tk.BooleanVar(value=True), "desc": "Data Analysis Library"},
            "matplotlib": {"var": tk.BooleanVar(value=True), "desc": "Plotting Library"},
            "colorama": {"var": tk.BooleanVar(value=True), "desc": "Terminal Color Library"},
            "requests": {"var": tk.BooleanVar(value=True), "desc": "HTTP Library"},
            "numpy": {"var": tk.BooleanVar(value=True), "desc": "Numerical Computing Library"},
            "psutil": {"var": tk.BooleanVar(value=True), "desc": "System Resource Monitoring"}
        }
        
        # Create checkbox for each required package
        for pkg, data in self.req_packages.items():
            cb = ttk.Checkbutton(
                req_frame,
                text=f"{pkg} - {data['desc']}",
                variable=data["var"]
            )
            cb.pack(anchor="w", pady=2)
        
        # Select/Deselect all button
        req_btn_frame = ttk.Frame(req_frame)
        req_btn_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(
            req_btn_frame,
            text="Select All",
            command=lambda: self.toggle_all(self.req_packages, True),
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            req_btn_frame,
            text="Deselect All",
            command=lambda: self.toggle_all(self.req_packages, False),
            width=15
        ).pack(side="left", padx=5)
        
        # Optional packages frame
        opt_frame = ttk.LabelFrame(main_frame, text="Optional Packages", padding=10)
        opt_frame.pack(fill="x", pady=(0, 15))
        
        # Optional packages checkboxes
        self.opt_packages = {
            "pywin32": {"var": tk.BooleanVar(value=True), "desc": "Windows API (for shortcuts)"},
            "winshell": {"var": tk.BooleanVar(value=True), "desc": "Windows Shell Interface"},
            "tensorflow": {"var": tk.BooleanVar(value=False), "desc": "Machine Learning Support (large)"},
            "scikit-learn": {"var": tk.BooleanVar(value=False), "desc": "Machine Learning Tools"},
            "ta": {"var": tk.BooleanVar(value=False), "desc": "Technical Analysis Library"}
        }
        
        # Create checkbox for each optional package
        for pkg, data in self.opt_packages.items():
            cb = ttk.Checkbutton(
                opt_frame,
                text=f"{pkg} - {data['desc']}",
                variable=data["var"]
            )
            cb.pack(anchor="w", pady=2)
        
        # Select/Deselect all button for optional packages
        opt_btn_frame = ttk.Frame(opt_frame)
        opt_btn_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(
            opt_btn_frame,
            text="Select All",
            command=lambda: self.toggle_all(self.opt_packages, True),
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            opt_btn_frame,
            text="Deselect All",
            command=lambda: self.toggle_all(self.opt_packages, False),
            width=15
        ).pack(side="left", padx=5)
        
        # Bottom buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(
            btn_frame,
            text="Quick Install (All Required)",
            style="Green.TButton",
            command=self.quick_install,
            width=25
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Install Selected Packages",
            command=self.install_selected,
            width=25
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Exit",
            command=self.root.destroy,
            width=15
        ).pack(side="right", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to install. Select packages and click Install.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", side="bottom", pady=(10, 0))
        
    def toggle_all(self, package_dict, state):
        """Select or deselect all checkboxes in the given dictionary"""
        for pkg_data in package_dict.values():
            pkg_data["var"].set(state)
    
    def quick_install(self):
        """Install all required packages"""
        for pkg, data in self.req_packages.items():
            data["var"].set(True)
            
        self.install_selected()
    
    def install_selected(self):
        """Install selected packages"""
        selected_packages = []
        
        # Collect selected required packages
        for pkg, data in self.req_packages.items():
            if data["var"].get():
                selected_packages.append(pkg)
                
        # Collect selected optional packages
        for pkg, data in self.opt_packages.items():
            if data["var"].get() and pkg != "pywin32":  # Handle pywin32 specially
                selected_packages.append(pkg)
        
        if not selected_packages:
            messagebox.showinfo("No Packages Selected", "Please select at least one package to install.")
            return
        
        # Special handling for pywin32 (needs to be installed as pywin32)
        if self.opt_packages["pywin32"]["var"].get():
            selected_packages.append("pywin32")
        
        # Install packages
        self.status_var.set(f"Installing {len(selected_packages)} packages. Please wait...")
        self.root.update_idletasks()
        
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + selected_packages
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Show installation progress window
            self.show_progress_window(process)
            
        except Exception as e:
            messagebox.showerror("Installation Error", f"Error installing packages: {str(e)}")
            self.status_var.set("Installation failed.")
    
    def show_progress_window(self, process):
        """Show installation progress in a new window"""
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Installing Packages")
        progress_window.geometry("700x400")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Output text area
        ttk.Label(progress_window, text="Installation Progress:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        text_frame = ttk.Frame(progress_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        output_text = tk.Text(text_frame, wrap="word", height=15)
        output_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=output_text.yview)
        scrollbar.pack(side="right", fill="y")
        output_text.config(yscrollcommand=scrollbar.set)
        
        # Progress bar
        progress = ttk.Progressbar(progress_window, mode="indeterminate")
        progress.pack(fill="x", padx=10, pady=10)
        progress.start()
        
        # Close button (initially disabled)
        close_btn = ttk.Button(
            progress_window, 
            text="Close", 
            command=progress_window.destroy,
            state="disabled"
        )
        close_btn.pack(pady=(0, 10))
        
        # Function to read output in the background
        def read_output():
            # Read output line by line
            for line in iter(process.stdout.readline, ''):
                if line:
                    output_text.insert(tk.END, line)
                    output_text.see(tk.END)
                    progress_window.update_idletasks()
            
            # Read any error output
            for line in iter(process.stderr.readline, ''):
                if line:
                    output_text.insert(tk.END, f"ERROR: {line}", "error")
                    output_text.see(tk.END)
                    progress_window.update_idletasks()
            
            # Wait for process to complete
            process.wait()
            
            # Update UI when done
            progress.stop()
            close_btn.config(state="normal")
            
            if process.returncode == 0:
                output_text.insert(tk.END, "\nInstallation completed successfully!\n")
                self.status_var.set("Installation completed successfully!")
            else:
                output_text.insert(tk.END, f"\nInstallation failed with return code {process.returncode}\n")
                self.status_var.set("Installation failed.")
        
        # Start reading output in a separate thread
        threading.Thread(target=read_output, daemon=True).start()
    
    def run(self):
        """Run the setup wizard"""
        self.root.mainloop()

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = [
        "# BROski Bot Requirements",
        "# Required packages",
        "ccxt>=1.92.0",
        "pandas>=1.3.5",
        "matplotlib>=3.5.0",
        "colorama>=0.4.4",
        "requests>=2.26.0",
        "numpy>=1.21.5",
        "psutil>=5.9.0",
        "",
        "# Optional packages",
        "# pywin32>=303 ; platform_system=='Windows'",
        "# winshell>=0.6 ; platform_system=='Windows'",
        "# tensorflow>=2.8.0",
        "# scikit-learn>=1.0.2",
        "# ta>=0.10.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("Created requirements.txt")

def create_install_script():
    """Create installation batch script"""
    if os.name == "nt":  # Windows
        script = [
            "@echo off",
            "echo BROski Bot - Installation Script",
            "echo ==============================",
            "echo.",
            "echo This script will install all required packages for BROski Bot.",
            "echo.",
            "set /p CHOICE=Do you want to proceed? (Y/N): ",
            "if /i \"%CHOICE%\"==\"Y\" goto install",
            "goto end",
            "",
            ":install",
            "echo.",
            "echo Installing required packages...",
            "python -m pip install --upgrade ccxt pandas matplotlib colorama requests numpy psutil",
            "echo.",
            "",
            "echo Do you want to install optional packages?",
            "set /p CHOICE=This includes ML libraries and may take longer (Y/N): ",
            "if /i \"%CHOICE%\"==\"Y\" (",
            "    echo.",
            "    echo Installing optional packages...",
            "    python -m pip install --upgrade pywin32 winshell tensorflow scikit-learn ta",
            ")",
            "",
            "echo.",
            "echo Installation complete!",
            "echo.",
            "echo You can now start BROski Bot by running:",
            "echo   python BROski_Control_Center.py",
            "echo.",
            "pause",
            "",
            ":end",
            "echo.",
            "echo Installation cancelled.",
            "pause"
        ]
        
        with open("INSTALL.bat", "w") as f:
            f.write("\n".join(script))
        
        print("Created INSTALL.bat script")
        
    else:  # Unix/Linux/Mac
        script = [
            "#!/bin/bash",
            "echo \"BROski Bot - Installation Script\"",
            "echo \"==============================\"",
            "echo",
            "echo \"This script will install all required packages for BROski Bot.\"",
            "echo",
            "read -p \"Do you want to proceed? (y/n): \" CHOICE",
            "if [[ $CHOICE =~ ^[Yy]$ ]]; then",
            "    echo",
            "    echo \"Installing required packages...\"",
            "    pip install --upgrade ccxt pandas matplotlib colorama requests numpy psutil",
            "    echo",
            "",
            "    echo \"Do you want to install optional packages?\"",
            "    read -p \"This includes ML libraries and may take longer (y/n): \" CHOICE",
            "    if [[ $CHOICE =~ ^[Yy]$ ]]; then",
            "        echo",
            "        echo \"Installing optional packages...\"",
            "        pip install --upgrade tensorflow scikit-learn ta",
            "    fi",
            "",
            "    echo",
            "    echo \"Installation complete!\"",
            "    echo",
            "    echo \"You can now start BROski Bot by running:\"",
            "    echo \"  python3 BROski_Control_Center.py\"",
            "    echo",
            "else",
            "    echo",
            "    echo \"Installation cancelled.\"",
            "fi"
        ]
        
        with open("install.sh", "w") as f:
            f.write("\n".join(script))
        
        # Make script executable
        try:
            os.chmod("install.sh", 0o755)
        except:
            pass
        
        print("Created install.sh script")

def main():
    """Main function"""
    print("BROski Bot - Setup Tools")
    print("=======================")
    
    # Create requirements.txt file
    create_requirements_file()
    
    # Create install script
    create_install_script()
    
    # Run the setup wizard if we're running the script directly
    if __name__ == "__main__":
        print("\nStarting setup wizard...")
        wizard = BROskiSetupWizard()
        wizard.run()

if __name__ == "__main__":
    main()
