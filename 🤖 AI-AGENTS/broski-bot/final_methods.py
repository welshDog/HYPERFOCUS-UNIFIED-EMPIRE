"""
Final methods needed to complete the BROski Control Center.
Add these to your BROskiControlCenter class to finish implementation.
"""

import os
import sys
import json
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess

def show_system_info(self):
    """Show system information in diagnostic output"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "🖥️ System Information\n\n")
    self.info_label.config(text="Retrieving system information...")
    
    try:
        import platform
        import psutil
        
        # System info
        self.diagnostic_text.insert(tk.END, "Operating System:\n")
        self.diagnostic_text.insert(tk.END, f"- Platform: {platform.platform()}\n")
        self.diagnostic_text.insert(tk.END, f"- System: {platform.system()} {platform.version()}\n")
        self.diagnostic_text.insert(tk.END, f"- Machine: {platform.machine()}\n\n")
        
        # Python info
        self.diagnostic_text.insert(tk.END, "Python Environment:\n")
        self.diagnostic_text.insert(tk.END, f"- Python Version: {platform.python_version()}\n")
        self.diagnostic_text.insert(tk.END, f"- Python Path: {sys.executable}\n\n")
        
        # Hardware info
        self.diagnostic_text.insert(tk.END, "Hardware Information:\n")
        self.diagnostic_text.insert(tk.END, f"- CPU: {platform.processor()}\n")
        self.diagnostic_text.insert(tk.END, f"- Logical CPUs: {psutil.cpu_count()}\n")
        self.diagnostic_text.insert(tk.END, f"- Physical CPUs: {psutil.cpu_count(logical=False)}\n")
        self.diagnostic_text.insert(tk.END, f"- Memory: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n\n")
        
        # Network info
        self.diagnostic_text.insert(tk.END, "Network Information:\n")
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            self.diagnostic_text.insert(tk.END, f"- Hostname: {hostname}\n")
            self.diagnostic_text.insert(tk.END, f"- Local IP: {local_ip}\n\n")
        except:
            self.diagnostic_text.insert(tk.END, "- Could not retrieve network information\n\n")
        
        self.info_label.config(text="System information retrieved")
    except ImportError as e:
        self.diagnostic_text.insert(tk.END, f"Could not retrieve full system information: {str(e)}\n")
        self.diagnostic_text.insert(tk.END, "Consider installing psutil for more detailed information.\n")
        self.diagnostic_text.insert(tk.END, "Run: pip install psutil\n\n")
        
        # Try to get basic system info without psutil
        try:
            import platform
            self.diagnostic_text.insert(tk.END, "Basic System Information:\n")
            self.diagnostic_text.insert(tk.END, f"- System: {platform.system()}\n")
            self.diagnostic_text.insert(tk.END, f"- Version: {platform.version()}\n")
            self.diagnostic_text.insert(tk.END, f"- Python Version: {platform.python_version()}\n")
        except:
            self.diagnostic_text.insert(tk.END, "Could not retrieve system information.")
        
        self.info_label.config(text="Basic system information retrieved")
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"Error retrieving system information: {str(e)}")
        self.info_label.config(text="Error retrieving system information")

def check_internet(self):
    """Check internet connectivity"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "🌐 Checking Internet Connection...\n\n")
    self.info_label.config(text="Testing internet connection...")
    
    # List of services to check
    services = [
        {"name": "Google DNS", "host": "8.8.8.8", "port": 53},
        {"name": "MEXC Exchange", "host": "api.mexc.com", "port": 443},
        {"name": "CloudFlare DNS", "host": "1.1.1.1", "port": 53}
    ]
    
    import socket
    socket.setdefaulttimeout(3)  # Set timeout to 3 seconds
    
    results = []
    for service in services:
        try:
            # Try to connect to the service
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((service["host"], service["port"]))
            sock.close()
            
            if result == 0:
                status = "✅ CONNECTED"
                results.append(True)
            else:
                status = "❌ FAILED"
                results.append(False)
        except:
            status = "❌ ERROR"
            results.append(False)
            
        self.diagnostic_text.insert(tk.END, f"{service['name']}: {status}\n")
    
    self.diagnostic_text.insert(tk.END, "\n")
    
    # Overall Internet Status
    if any(results):
        self.diagnostic_text.insert(tk.END, "✅ Internet connection is available.\n")
        
        # Try to get public IP
        try:
            import requests
            ip = requests.get('https://api.ipify.org').text
            self.diagnostic_text.insert(tk.END, f"\nYour public IP address: {ip}\n")
        except:
            self.diagnostic_text.insert(tk.END, "\nCould not determine public IP address.\n")
        
        self.info_label.config(text="Internet connection test complete")
    else:
        self.diagnostic_text.insert(tk.END, "❌ No internet connection available.\n")
        self.diagnostic_text.insert(tk.END, "\nPlease check your network connection and try again.\n")
        self.info_label.config(text="Internet connection test failed")

def check_disk_space(self):
    """Check available disk space"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "💾 Checking Disk Space...\n\n")
    self.info_label.config(text="Checking disk space...")
    
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
            
            self.diagnostic_text.insert(tk.END, "Drive containing BROski Bot:\n\n")
            self.diagnostic_text.insert(tk.END, f"Total Space: {total_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Used Space: {used_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Free Space: {free_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Percent Used: {percent_used:.1f}%\n\n")
            
            # Add visual bar
            bar_length = 40
            used_bar = int(bar_length * percent_used / 100)
            bar = '[' + '█' * used_bar + ' ' * (bar_length - used_bar) + ']'
            self.diagnostic_text.insert(tk.END, f"Usage: {bar} {percent_used:.1f}%\n\n")
            
            # BROski folder size
            total_size = 0
            for dirpath, dirnames, filenames in os.walk('.'):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            
            folder_mb = total_size / (1024**2)
            self.diagnostic_text.insert(tk.END, f"BROski Bot folder size: {folder_mb:.2f} MB\n")
            
            # Show status message based on available space
            if free_gb < 1:
                self.diagnostic_text.insert(tk.END, "\n⚠️ WARNING: Very low disk space!\n")
            elif free_gb < 5:
                self.diagnostic_text.insert(tk.END, "\n⚠️ Notice: Disk space is getting low.\n")
            else:
                self.diagnostic_text.insert(tk.END, "\n✅ Disk space is adequate.\n")
            
            self.info_label.config(text="Disk space check complete")
        else:
            # For non-Windows systems
            try:
                import shutil
                total, used, free = shutil.disk_usage('/')
                
                total_gb = total / (1024**3)
                used_gb = used / (1024**3)
                free_gb = free / (1024**3)
                percent_used = (used_gb / total_gb) * 100
                
                self.diagnostic_text.insert(tk.END, "Drive containing BROski Bot:\n\n")
                self.diagnostic_text.insert(tk.END, f"Total Space: {total_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Used Space: {used_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Free Space: {free_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Percent Used: {percent_used:.1f}%\n")
                
                # Add visual bar
                bar_length = 40
                used_bar = int(bar_length * percent_used / 100)
                bar = '[' + '█' * used_bar + ' ' * (bar_length - used_bar) + ']'
                self.diagnostic_text.insert(tk.END, f"Usage: {bar} {percent_used:.1f}%\n")
                
                self.info_label.config(text="Disk space check complete")
            except:
                self.diagnostic_text.insert(tk.END, "Could not retrieve disk space on this platform.\n")
                self.info_label.config(text="Disk space check unsupported")
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"Error checking disk space: {str(e)}")
        self.info_label.config(text="Error checking disk space")

# The following methods complete the implementation of BROski Control Center

def show_system_info(self):
    """Show system information"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "System Information:\n\n")
    
    try:
        import platform
        self.diagnostic_text.insert(tk.END, f"System: {platform.system()}\n")
        self.diagnostic_text.insert(tk.END, f"Node Name: {platform.node()}\n")
        self.diagnostic_text.insert(tk.END, f"Release: {platform.release()}\n")
        self.diagnostic_text.insert(tk.END, f"Version: {platform.version()}\n")
        self.diagnostic_text.insert(tk.END, f"Machine: {platform.machine()}\n")
        self.diagnostic_text.insert(tk.END, f"Processor: {platform.processor()}\n")
        self.diagnostic_text.insert(tk.END, f"Python Version: {platform.python_version()}\n")
        
        self.status_var.set("System information displayed")
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"Error retrieving system information: {str(e)}")
        self.status_var.set("Error retrieving system information")

def check_internet(self):
    """Check internet connection"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "Checking internet connection...\n\n")
    self.info_label.config(text="Checking internet connection...")
    
    try:
        import socket
        
        # Try connecting to Google DNS
        host = "8.8.8.8"
        port = 53
        timeout = 3
        
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        
        self.diagnostic_text.insert(tk.END, "✅ Internet connection is working!\n")
        self.info_label.config(text="Internet connection active")
        
        # Try checking external IP
        try:
            import requests
            ip = requests.get('https://api.ipify.org').text
            self.diagnostic_text.insert(tk.END, f"\nYour public IP address is: {ip}\n")
        except:
            self.diagnostic_text.insert(tk.END, "\nNote: Could not determine your public IP address.\n")
        
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"❌ No internet connection detected!\n\n")
        self.diagnostic_text.insert(tk.END, f"Error details: {str(e)}\n\n")
        self.diagnostic_text.insert(tk.END, "Check your network connection and try again.\n")
        self.info_label.config(text="No internet connection detected")

def check_disk_space(self):
    """Check available disk space"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "Checking disk space...\n\n")
    self.info_label.config(text="Checking disk space...")
    
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
            
            self.diagnostic_text.insert(tk.END, f"Total Space: {total_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Used Space: {used_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Free Space: {free_gb:.2f} GB\n")
            self.diagnostic_text.insert(tk.END, f"Percent Used: {percent_used:.1f}%\n\n")
            
            # BROski folder size
            total_size = 0
            for dirpath, dirnames, filenames in os.walk('.'):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            
            folder_mb = total_size / (1024**2)
            self.diagnostic_text.insert(tk.END, f"\nBROski Bot folder size: {folder_mb:.2f} MB\n")
            
            self.info_label.config(text="Disk space check complete")
        else:
            # Unix-like systems
            try:
                import shutil
                total, used, free = shutil.disk_usage('/')
                
                total_gb = total / (1024**3)
                used_gb = used / (1024**3)
                free_gb = free / (1024**3)
                percent_used = (used_gb / total_gb) * 100
                
                self.diagnostic_text.insert(tk.END, f"Total Space: {total_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Used Space: {used_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Free Space: {free_gb:.2f} GB\n")
                self.diagnostic_text.insert(tk.END, f"Percent Used: {percent_used:.1f}%\n")
                
                self.info_label.config(text="Disk space check complete")
            except:
                self.diagnostic_text.insert(tk.END, "Could not retrieve disk information on this platform.")
                self.info_label.config(text="Disk space check not supported")
    except Exception as e:
        self.diagnostic_text.insert(tk.END, f"Error checking disk space: {str(e)}")
        self.info_label.config(text="Error checking disk space")

def generate_system_report(self):
    """Generate a comprehensive system report"""
    self.diagnostic_text.delete(1.0, tk.END)
    self.diagnostic_text.insert(tk.END, "Generating BROski Bot System Report...\n\n")
    self.info_label.config(text="Generating system report...")
    
    report = {}
    
    # System Information
    try:
        import platform
        report["system"] = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "machine": platform.machine()
        }
    except:
        report["system"] = {"error": "Could not retrieve system information"}
    
    # BROski Configuration
    try:
        if os.path.exists("config.json"):
            with open("config.json", 'r') as f:
                config = json.load(f)
            
            # Sanitize API keys for security
            if "exchange" in config and "api_key" in config["exchange"]:
                key = config["exchange"]["api_key"]
                if len(key) > 8:
                    config["exchange"]["api_key"] = key[:4] + "..." + key[-4:]
            
            if "exchange" in config and "api_secret" in config["exchange"]:
                config["exchange"]["api_secret"] = "********"
            
            report["config"] = config
        else:
            report["config"] = {"error": "config.json not found"}
    except:
        report["config"] = {"error": "Could not read configuration"}
    
    # Files and Directories
    try:
        report["files"] = {
            "python_scripts": [f for f in os.listdir() if f.endswith('.py')],
            "batch_files": [f for f in os.listdir() if f.endswith('.bat')],
            "directories": [d for d in os.listdir() if os.path.isdir(d)]
        }
        
        # Log files
        if os.path.exists("logs"):
            report["logs"] = {
                "count": len([f for f in os.listdir("logs") if f.endswith('.log')]),
                "recent_logs": []
            }
            
            # Get the 5 most recent logs
            log_files = [(f, os.path.getmtime(os.path.join("logs", f))) 
                        for f in os.listdir("logs") if f.endswith('.log')]
            log_files.sort(key=lambda x: x[1], reverse=True)
            
            for file, mtime in log_files[:5]:
                size_kb = os.path.getsize(os.path.join("logs", file)) / 1024
                mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                report["logs"]["recent_logs"].append({
                    "name": file,
                    "size": f"{size_kb:.2f} KB",
                    "modified": mtime_str
                })
    except:
        report["files"] = {"error": "Could not enumerate files"}
    
    # Available disk space
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
            
            report["disk"] = {
                "free_space_gb": f"{free_gb:.2f}",
                "total_space_gb": f"{total_gb:.2f}",
                "percent_free": f"{(free_gb/total_gb)*100:.1f}%"
            }
    except:
        report["disk"] = {"error": "Could not retrieve disk information"}
    
    # Display the report
    self.diagnostic_text.insert(tk.END, "BROski Bot System Report\n")
    self.diagnostic_text.insert(tk.END, "======================\n\n")
    
    # System section
    self.diagnostic_text.insert(tk.END, "System Information:\n")
    self.diagnostic_text.insert(tk.END, "------------------\n")
    if "error" not in report["system"]:
        self.diagnostic_text.insert(tk.END, f"Platform: {report['system']['platform']}\n")
        self.diagnostic_text.insert(tk.END, f"Python Version: {report['system']['python_version']}\n")
        self.diagnostic_text.insert(tk.END, f"Processor: {report['system']['processor']}\n")
        self.diagnostic_text.insert(tk.END, f"Machine: {report['system']['machine']}\n")
    else:
        self.diagnostic_text.insert(tk.END, f"Error: {report['system']['error']}\n")
    
    # Configuration section
    self.diagnostic_text.insert(tk.END, "\nConfiguration:\n")
    self.diagnostic_text.insert(tk.END, "--------------\n")
    if "error" not in report["config"]:
        if "trading" in report["config"]:
            trading = report["config"]["trading"]
            self.diagnostic_text.insert(tk.END, f"Trading Pair: {trading.get('base_symbol', '?')}/{trading.get('quote_symbol', '?')}\n")
            self.diagnostic_text.insert(tk.END, f"Auto-Trade: {'Enabled' if trading.get('auto_trade') else 'Disabled'}\n")
        
        if "exchange" in report["config"]:
            exchange = report["config"]["exchange"]
            self.diagnostic_text.insert(tk.END, f"Exchange: {exchange.get('name', '?')}\n")
            self.diagnostic_text.insert(tk.END, f"API Key: {exchange.get('api_key', 'Not configured')}\n")
        
        if "strategies" in report["config"]:
            strategies = report["config"]["strategies"]
            self.diagnostic_text.insert(tk.END, f"Active Strategy: {strategies.get('active_strategy', '?')}\n")
    else:
        self.diagnostic_text.insert(tk.END, f"Error: {report['config']['error']}\n")
    
    # Files section
    self.diagnostic_text.insert(tk.END, "\nFiles and Directories:\n")
    self.diagnostic_text.insert(tk.END, "--------------------\n")
    if "error" not in report["files"]:
        self.diagnostic_text.insert(tk.END, f"Python Scripts: {len(report['files']['python_scripts'])}\n")
        self.diagnostic_text.insert(tk.END, f"Batch Files: {len(report['files']['batch_files'])}\n")
        self.diagnostic_text.insert(tk.END, f"Directories: {len(report['files']['directories'])}\n")
        
        if "logs" in report:
            self.diagnostic_text.insert(tk.END, f"Log Files: {report['logs']['count']}\n")
            
            if report['logs']['recent_logs']:
                self.diagnostic_text.insert(tk.END, "\nRecent Logs:\n")
                for log in report['logs']['recent_logs']:
                    self.diagnostic_text.insert(tk.END, f"- {log['name']} ({log['size']}, {log['modified']})\n")
    else:
        self.diagnostic_text.insert(tk.END, f"Error: {report['files']['error']}\n")
    
    # Disk section
    self.diagnostic_text.insert(tk.END, "\nDisk Space:\n")
    self.diagnostic_text.insert(tk.END, "----------\n")
    if "error" not in report["disk"]:
        self.diagnostic_text.insert(tk.END, f"Total Space: {report['disk']['total_space_gb']} GB\n")
        self.diagnostic_text.insert(tk.END, f"Free Space: {report['disk']['free_space_gb']} GB\n")
        self.diagnostic_text.insert(tk.END, f"Percent Free: {report['disk']['percent_free']}\n")
    else:
        self.diagnostic_text.insert(tk.END, f"Error: {report['disk']['error']}\n")
    
    # Timestamp at the end
    self.diagnostic_text.insert(tk.END, f"\nReport generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    self.info_label.config(text="System report generated successfully")

    # Option to save report
    save = messagebox.askyesno("Save Report", "Do you want to save this report to a file?")
    if save:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"BROski_System_Report_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write(self.diagnostic_text.get(1.0, tk.END))
                
            self.info_label.config(text=f"Report saved to {filename}")
            messagebox.showinfo("Report Saved", f"Report saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save report: {str(e)}")
