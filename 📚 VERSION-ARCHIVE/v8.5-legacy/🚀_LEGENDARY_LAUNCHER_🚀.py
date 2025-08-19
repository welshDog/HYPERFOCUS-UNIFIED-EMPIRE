"""
🚀💎⚡ HYPERFOCUS ZONE V8.5 LAUNCHER ⚡💎🚀
The Ultimate ADHD-Optimized Productivity Empire

Quick start script for Chief LYNDZ's legendary workspace
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def legendary_banner():
    """Display the epic startup banner"""
    print("""
🚀💎⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡💎🚀
         🧠⚡ HYPERFOCUS ZONE V8.5 ULTRA LAUNCHER ⚡🧠
         
    Empire running at MAXIMUM LEGENDARY HYPERFOCUS.
    
    ✨ Built for Chief LYNDZ by BROski♾️ AI Empire ✨
    🎯 ADHD-Optimized • Neurodivergent Excellence • Focus Amplified
🚀💎⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡💎🚀
    """)

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking system requirements...")
    
    try:
        import flask
        print("✅ Flask - READY")
    except ImportError:
        print("❌ Flask not found - Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"])
    
    try:
        import psutil
        print("✅ psutil - READY")
    except ImportError:
        print("❌ psutil not found - Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil"])
    
    print("🎯 Dependencies check complete!")

def launch_hyperfocus_zone():
    """Launch the main HyperFocus Zone application"""
    print("\n🚀 Launching HYPERFOCUS ZONE Portal...")
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found in current directory")
        return False
    
    try:
        # Start the Flask application in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⚡ HyperFocus Zone Portal starting...")
        time.sleep(3)  # Give it time to start
        
        # Open the browser to the command center
        print("🌟 Opening Ultimate Command Center...")
        webbrowser.open("http://127.0.0.1:5005/ultimate-command-center")
        
        print("""
🎯 HYPERFOCUS ZONE IS LIVE!

📊 Main Dashboard: http://127.0.0.1:5005/ultimate-command-center
🔥 Boardroom Hub: Open 🔥🕋💪_HYPERBEAST_BOARDROOM_DASHBOARD_💪🕋🔥.html
📱 Live Monitor: Open live_dashboard.html
🗂️ File Manager: Open ultra_file_keeper_dashboard.html

🌟 Your LEGENDARY productivity empire is ready!
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to launch: {e}")
        return False

def main():
    """Main launcher function"""
    legendary_banner()
    
    print("🎯 Initializing LEGENDARY launch sequence...")
    check_dependencies()
    
    if launch_hyperfocus_zone():
        print("\n💎 Welcome to your HYPERFOCUS EMPIRE, Chief LYNDZ! 💎")
        print("🚀 Press Ctrl+C to shutdown when done")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🌟 HYPERFOCUS ZONE shutdown complete. See you soon! 🌟")
    else:
        print("\n❌ Launch failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
