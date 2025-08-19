import os
import sys
import time
import subprocess
from colorama import init, Fore, Style
from pathlib import Path
import signal

# Initialize colorama
init()

class BroskiLauncher:
    """Launcher to start both the BROski bot and monitor together"""
    
    def __init__(self):
        self.bot_process = None
        self.monitor_process = None
        self.running = False
    
    def show_banner(self):
        """Display the BROski banner"""
        banner = """
 ____  ____   __   ____  _  _  __
| __ )/ ___| / /  / ___|| |/ / |_ |
|  _ \\___ \\ / /   \\___ \\| ' /   | |
| |_) |__) / /___ ___) | . \\   | |
|____/____/\\____/|____/|_|\\_\\  |_|  Trading Bot
        """
        
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Automated Trading Bot & Monitor{Style.RESET_ALL}".center(60))
        print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}\n")
    
    def check_files(self):
        """Check if required files exist"""
        required_files = [
            Path("start_bot.py"),
            Path("bot_monitor.py"),
            Path("config.json")
        ]
        
        missing = [f for f in required_files if not f.exists()]
        if missing:
            print(f"{Fore.RED}Error: Required files not found:{Style.RESET_ALL}")
            for file in missing:
                print(f"  - {file}")
            return False
        
        return True
    
    def start_bot(self):
        """Start the trading bot in a separate process"""
        try:
            print(f"{Fore.GREEN}Starting BROski trading bot...{Style.RESET_ALL}")
            # Use subprocess.Popen to start the bot as a separate process
            self.bot_process = subprocess.Popen([sys.executable, "start_bot.py"])
            print(f"{Fore.GREEN}✓ Bot started (PID: {self.bot_process.pid}){Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Failed to start bot: {str(e)}{Style.RESET_ALL}")
            return False
    
    def start_monitor(self):
        """Start the monitor in a separate process"""
        try:
            # Wait a moment for the bot to initialize and create log files
            time.sleep(2)
            
            print(f"{Fore.GREEN}Starting BROski monitor...{Style.RESET_ALL}")
            # Use subprocess.Popen to start the monitor as a separate process
            self.monitor_process = subprocess.Popen([sys.executable, "bot_monitor.py"])
            print(f"{Fore.GREEN}✓ Monitor started (PID: {self.monitor_process.pid}){Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Failed to start monitor: {str(e)}{Style.RESET_ALL}")
            return False
    
    def start_all(self):
        """Start both bot and monitor"""
        if not self.check_files():
            return False
            
        self.running = self.start_bot()
        
        if self.running:
            self.running = self.start_monitor()
            
        return self.running
    
    def monitor_processes(self):
        """Monitor the running processes and handle shutdown"""
        try:
            print("\nBROski is now running! Press Ctrl+C to stop all components.\n")
            
            # Keep running until interrupted
            while self.running:
                # Check if processes are still running
                if self.bot_process and self.bot_process.poll() is not None:
                    print(f"{Fore.YELLOW}Warning: Bot process has terminated.{Style.RESET_ALL}")
                    self.running = False
                    break
                
                if self.monitor_process and self.monitor_process.poll() is not None:
                    print(f"{Fore.YELLOW}Warning: Monitor process has terminated.{Style.RESET_ALL}")
                    self.running = False
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Shutdown requested. Stopping all components...{Style.RESET_ALL}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of all processes"""
        if self.bot_process:
            print(f"{Fore.YELLOW}Stopping bot (PID: {self.bot_process.pid})...{Style.RESET_ALL}")
            try:
                # Send interrupt signal to the process
                if os.name == 'nt':  # Windows
                    self.bot_process.terminate()
                else:  # Unix/Linux
                    os.kill(self.bot_process.pid, signal.SIGINT)
                self.bot_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}Bot didn't terminate gracefully, forcing...{Style.RESET_ALL}")
                self.bot_process.terminate()
            except Exception as e:
                print(f"{Fore.RED}Error stopping bot: {str(e)}{Style.RESET_ALL}")
                
        if self.monitor_process:
            print(f"{Fore.YELLOW}Stopping monitor (PID: {self.monitor_process.pid})...{Style.RESET_ALL}")
            try:
                self.monitor_process.terminate()
                self.monitor_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}Monitor didn't terminate gracefully, forcing...{Style.RESET_ALL}")
                self.monitor_process.terminate()
            except Exception as e:
                print(f"{Fore.RED}Error stopping monitor: {str(e)}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}All components stopped. BROski is shut down.{Style.RESET_ALL}")
    
    def run(self):
        """Run the launcher"""
        self.show_banner()
        
        # Show current config
        try:
            import json
            with open("config.json", 'r') as f:
                config = json.load(f)
                
            pair = f"{config['trading']['base_symbol']}/{config['trading']['quote_symbol']}"
            strategy = config['strategies']['active_strategy']
            auto_trade = "ENABLED" if config['trading']['auto_trade'] else "DISABLED"
            
            print(f"{Fore.YELLOW}Current settings:{Style.RESET_ALL}")
            print(f"• Trading pair: {Fore.CYAN}{pair}{Style.RESET_ALL}")
            print(f"• Active strategy: {Fore.CYAN}{strategy}{Style.RESET_ALL}")
            print(f"• Auto-trading: {Fore.GREEN if auto_trade == 'ENABLED' else Fore.RED}{auto_trade}{Style.RESET_ALL}")
            print(f"• Trade amount: {Fore.CYAN}{config['trading']['trade_amount']} {config['trading']['quote_symbol']}{Style.RESET_ALL}")
            print("")
            
            # Confirm start
            confirm = input(f"{Fore.YELLOW}Start BROski with these settings? (y/n):{Style.RESET_ALL} ").lower()
            if confirm != 'y':
                print("Launch cancelled.")
                return
        except:
            # If we can't read config, just continue
            pass
            
        if self.start_all():
            self.monitor_processes()
        else:
            print(f"{Fore.RED}Failed to start BROski. Please check the errors above.{Style.RESET_ALL}")

if __name__ == "__main__":
    launcher = BroskiLauncher()
    launcher.run()
