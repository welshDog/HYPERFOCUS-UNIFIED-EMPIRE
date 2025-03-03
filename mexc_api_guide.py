from datetime import datetime
import os
import sys

class MEXCGuide:
    """Helper class to provide guidance on MEXC API setup"""
    
    @staticmethod
    def display_api_instructions():
        """Display instructions for getting MEXC API keys"""
        print("\n===== MEXC API Key Setup Guide =====\n")
        print("Step 1: Create a MEXC Account")
        print("  - Go to https://www.mexc.com/")
        print("  - Sign up for an account if you don't have one")
        print("  - Complete any required verification\n")
        
        print("Step 2: Enable 2-Factor Authentication (2FA)")
        print("  - This is required for API access")
        print("  - Go to Account -> Security Settings")
        print("  - Set up Google Authenticator or SMS verification\n")
        
        print("Step 3: Create API Keys")
        print("  - Go to Account -> API Management")
        print("  - Click 'Create API'")
        print("  - Enter a label like 'BROski Bot'")
        print("  - Set permissions (Read is required, Trade is needed for automated trading)")
        print("  - Consider setting IP restrictions for better security")
        print("  - Complete 2FA verification\n")
        
        print("Step 4: Save Your API Keys")
        print("  - Copy both the API Key and Secret Key")
        print("  - Store them in BROski Bot's configuration")
        print("  - IMPORTANT: Never share your Secret Key with anyone!")
        print("  - If you lose the Secret Key, you'll need to create new API keys\n")
        
        print("Step 5: Test Your API Keys")
        print("  - Use BROski Bot's 'Check API Connection' feature")
        print("  - This will verify your keys are working correctly\n")
        
        input("Press Enter to continue...")

    @staticmethod
    def display_trading_instructions():
        """Display instructions for configuring trading settings"""
        print("\n===== Trading Configuration Guide =====\n")
        print("Step 1: Select Trading Pair")
        print("  - Base Symbol: The cryptocurrency you want to trade (e.g., PI)")
        print("  - Quote Symbol: The currency used for pricing (e.g., USDT)\n")
        
        print("Step 2: Configure Trade Amount")
        print("  - Set the amount of quote currency (e.g., USDT) to use per trade")
        print("  - Start with a small amount for testing (e.g., 5-10 USDT)")
        print("  - The bot will calculate how much of the base currency to buy/sell\n")
        
        print("Step 3: Risk Management Settings")
        print("  - Stop Loss: Set percentage drop to trigger selling (e.g., 5%)")
        print("  - Take Profit: Set percentage gain to trigger selling (e.g., 10%)")
        print("  - Adjust these based on your risk tolerance\n")
        
        print("Step 4: Auto-Trading Mode")
        print("  - Disabled: Bot will only monitor and suggest trades")
        print("  - Enabled: Bot will execute trades automatically")
        print("  - RECOMMENDATION: Start with auto-trading disabled until you're comfortable\n")
        
        print("Step 5: Test Settings")
        print("  - Start the bot in monitor mode")
        print("  - Review suggested trades before enabling auto-trading\n")
        
        input("Press Enter to continue...")

    @staticmethod
    def display_strategy_instructions():
        """Display instructions for selecting and configuring strategies"""
        print("\n===== Trading Strategy Guide =====\n")
        print("BROski Bot offers multiple trading strategies:")
        
        print("\n1. RSI Strategy")
        print("  - Best for: Range-bound markets with clear oversold/overbought conditions")
        print("  - Key Parameters:")
        print("    • RSI Period: Period for calculation (default: 14)")
        print("    • Oversold Threshold: Buy signal (default: 30)")
        print("    • Overbought Threshold: Sell signal (default: 70)")
        print("    • Timeframe: Data interval (1m, 5m, 15m, 1h, etc.)\n")
        
        print("2. MACD Strategy")
        print("  - Best for: Trending markets")
        print("  - Key Parameters:")
        print("    • Fast Period: Short-term EMA (default: 12)")
        print("    • Slow Period: Long-term EMA (default: 26)")
        print("    • Signal Period: Signal line smoothing (default: 9)")
        print("    • Timeframe: Data interval\n")
        
        print("3. HyperFocus Strategy")
        print("  - Best for: All market conditions, adapts automatically")
        print("  - Advanced multi-indicator strategy with volume analysis")
        print("  - Key Parameters:")
        print("    • Sensitivity: Controls how aggressive trades are")
        print("    • Volume Confirmation: Uses volume to confirm signals")
        print("    • Multi-timeframe Analysis: Confirms across multiple timeframes\n")
        
        print("Strategy Selection Tips:")
        print("  - For beginners: Start with RSI strategy")
        print("  - For volatile markets: Use HyperFocus with lower sensitivity")
        print("  - For stable trends: MACD works well")
        print("  - Consider backtesting strategies before live trading\n")
        
        input("Press Enter to continue...")

    @staticmethod
    def save_guide():
        """Save the complete guide to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MEXC_Setup_Guide_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("===============================================\n")
            f.write("           MEXC SETUP GUIDE FOR BROSKI BOT     \n")
            f.write("===============================================\n\n")
            
            # Save API instructions
            f.write("===== MEXC API Key Setup Guide =====\n\n")
            f.write("Step 1: Create a MEXC Account\n")
            f.write("  - Go to https://www.mexc.com/\n")
            f.write("  - Sign up for an account if you don't have one\n")
            f.write("  - Complete any required verification\n\n")
            
            f.write("Step 2: Enable 2-Factor Authentication (2FA)\n")
            f.write("  - This is required for API access\n")
            f.write("  - Go to Account -> Security Settings\n")
            f.write("  - Set up Google Authenticator or SMS verification\n\n")
            
            f.write("Step 3: Create API Keys\n")
            f.write("  - Go to Account -> API Management\n")
            f.write("  - Click 'Create API'\n")
            f.write("  - Enter a label like 'BROski Bot'\n")
            f.write("  - Set permissions (Read is required, Trade is needed for automated trading)\n")
            f.write("  - Consider setting IP restrictions for better security\n")
            f.write("  - Complete 2FA verification\n\n")
            
            f.write("Step 4: Save Your API Keys\n")
            f.write("  - Copy both the API Key and Secret Key\n")
            f.write("  - Store them in BROski Bot's configuration\n")
            f.write("  - IMPORTANT: Never share your Secret Key with anyone!\n")
            f.write("  - If you lose the Secret Key, you'll need to create new API keys\n\n")
            
            # Save Trading instructions
            f.write("===== Trading Configuration Guide =====\n\n")
            f.write("Step 1: Select Trading Pair\n")
            f.write("  - Base Symbol: The cryptocurrency you want to trade (e.g., PI)\n")
            f.write("  - Quote Symbol: The currency used for pricing (e.g., USDT)\n\n")
            
            f.write("Step 2: Configure Trade Amount\n")
            f.write("  - Set the amount of quote currency (e.g., USDT) to use per trade\n")
            f.write("  - Start with a small amount for testing (e.g., 5-10 USDT)\n")
            f.write("  - The bot will calculate how much of the base currency to buy/sell\n\n")
            
            # Save Strategy instructions
            f.write("===== Trading Strategy Guide =====\n\n")
            f.write("BROski Bot offers multiple trading strategies:\n\n")
            
            f.write("1. RSI Strategy\n")
            f.write("  - Best for: Range-bound markets with clear oversold/overbought conditions\n")
            f.write("  - Key Parameters:\n")
            f.write("    • RSI Period: Period for calculation (default: 14)\n")
            f.write("    • Oversold Threshold: Buy signal (default: 30)\n")
            f.write("    • Overbought Threshold: Sell signal (default: 70)\n\n")
            
            f.write("2. MACD Strategy\n")
            f.write("  - Best for: Trending markets\n")
            f.write("  - Key Parameters:\n")
            f.write("    • Fast Period: Short-term EMA (default: 12)\n")
            f.write("    • Slow Period: Long-term EMA (default: 26)\n")
            f.write("    • Signal Period: Signal line smoothing (default: 9)\n\n")
            
            f.write("3. HyperFocus Strategy\n")
            f.write("  - Best for: All market conditions, adapts automatically\n")
            f.write("  - Advanced multi-indicator strategy with volume analysis\n\n")
            
            f.write("Generated by BROski Bot on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
        print(f"\nGuide saved to {filename}")
        return filename

if __name__ == "__main__":
    guide = MEXCGuide()
    
    print("📚 BROski MEXC Setup Guide 📚")
    print("==============================\n")
    print("This guide will help you set up your MEXC API keys and configure the bot.")
    print("Choose a topic below:\n")
    
    while True:
        print("1. How to get MEXC API Keys")
        print("2. How to configure Trading Settings")
        print("3. How to select Trading Strategies")
        print("4. Save guide to file")
        print("5. Exit guide")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            guide.display_api_instructions()
        elif choice == "2":
            guide.display_trading_instructions()
        elif choice == "3":
            guide.display_strategy_instructions()
        elif choice == "4":
            saved_file = guide.save_guide()
            print(f"Guide saved to {saved_file}")
            input("Press Enter to continue...")
        elif choice == "5":
            print("\nExiting guide. Happy trading with BROski Bot!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.\n")
