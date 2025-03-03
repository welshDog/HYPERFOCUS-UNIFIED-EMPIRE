import requests
import webbrowser
import json
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def get_current_ip():
    """Get the current public IP address"""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        ip_data = response.json()
        return ip_data["ip"]
    except Exception as e:
        print(f"{Fore.RED}Error getting IP address: {e}{Style.RESET_ALL}")
        return None

def open_mexc_api_page():
    """Open the MEXC API management page in a browser"""
    url = "https://www.mexc.com/user/openapi"
    print(f"{Fore.YELLOW}Opening MEXC API management page...{Style.RESET_ALL}")
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error opening browser: {e}{Style.RESET_ALL}")
        print(f"Please manually visit: {url}")
        return False

def update_config_ip(ip_address):
    """Add current IP to config file for reference"""
    config_path = Path("config.json")
    if not config_path.exists():
        print(f"{Fore.RED}Config file not found.{Style.RESET_ALL}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "exchange" not in config:
            config["exchange"] = {}
        
        if "ip_whitelist" not in config["exchange"]:
            config["exchange"]["ip_whitelist"] = []
        
        if ip_address not in config["exchange"]["ip_whitelist"]:
            config["exchange"]["ip_whitelist"].append(ip_address)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"{Fore.GREEN}Added IP address to config file for reference.{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error updating config file: {e}{Style.RESET_ALL}")
        return False

def show_instructions(ip_address):
    """Display instructions for updating IP whitelist"""
    print(f"\n{Fore.CYAN}═══ IP WHITELIST INSTRUCTIONS ═══{Style.RESET_ALL}")
    print(f"\nYour current IP address is: {Fore.GREEN}{ip_address}{Style.RESET_ALL}")
    print("\nTo add this IP to your MEXC whitelist:")
    
    print(f"\n{Fore.YELLOW}Step 1:{Style.RESET_ALL} Log into your MEXC account")
    print(f"{Fore.YELLOW}Step 2:{Style.RESET_ALL} Go to Account → API Management")
    print(f"{Fore.YELLOW}Step 3:{Style.RESET_ALL} Find your API key and click 'Edit'")
    print(f"{Fore.YELLOW}Step 4:{Style.RESET_ALL} In the 'IP restriction' section, add your current IP:")
    print(f"         {Fore.GREEN}{ip_address}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Step 5:{Style.RESET_ALL} Save changes")
    
    print(f"\n{Fore.CYAN}Note:{Style.RESET_ALL} If you have multiple IPs in the whitelist, separate them with commas.")
    print(f"{Fore.CYAN}Example:{Style.RESET_ALL} 151.224.117.246,192.168.1.1,10.0.0.1")

def main():
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║      MEXC IP WHITELIST HELPER            ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Get current IP
    print("\nDetecting your current IP address...")
    ip_address = get_current_ip()
    
    if ip_address:
        print(f"\n{Fore.GREEN}Your current public IP address is: {ip_address}{Style.RESET_ALL}")
        
        # Save IP to config for reference
        update_config_ip(ip_address)
        
        # Display instructions
        show_instructions(ip_address)
        
        # Ask if user wants to open MEXC API page
        open_page = input(f"\nWould you like to open the MEXC API management page? (y/n): ").lower() == 'y'
        if open_page:
            open_mexc_api_page()
    else:
        print(f"\n{Fore.RED}Failed to detect your IP address.{Style.RESET_ALL}")
        print("Please visit https://whatismyip.com to find your IP address manually.")
    
    print(f"\n{Fore.CYAN}After updating your IP whitelist, restart the bot.{Style.RESET_ALL}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
