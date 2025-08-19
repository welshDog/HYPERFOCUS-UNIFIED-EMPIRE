import sys
import subprocess
import os

# Print debug info
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("\nChecking required modules:")

# Check tkinter
try:
    import tkinter as tk
    print("✓ Tkinter is available (version: {})".format(tk.TkVersion))
    
    # Test if it works
    root = tk.Tk()
    root.title("BROski Test Window")
    root.geometry("300x100")
    tk.Label(root, text="If you can see this window,\ntkinter is working correctly!").pack(pady=20)
    
    # Add auto-close button
    tk.Button(root, text="Close", command=root.destroy).pack(pady=10)
    
    # Auto-close after 5 seconds
    root.after(5000, root.destroy)
    root.mainloop()
except Exception as e:
    print("✗ Tkinter error:", str(e))

# Check if broski_dashboard.py exists
if os.path.exists("broski_dashboard.py"):
    print("✓ broski_dashboard.py exists")
    
    # Check for common errors in the file - using UTF-8 with error handling
    try:
        with open("broski_dashboard.py", "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "import tk" in content and "import tkinter as tk" not in content:
                print("✗ Possible error: 'import tk' found but should be 'import tkinter as tk'")
            if "root.mainloop()" not in content:
                print("✗ Warning: Could not find 'root.mainloop()' - dashboard may not run properly")
    except Exception as e:
        print(f"✗ Error reading dashboard file: {str(e)}")
else:
    print("✗ broski_dashboard.py not found")

# Try to fix the dashboard file directly
try:
    if os.path.exists("broski_dashboard.py"):
        print("\nAttempting to fix potential issues in broski_dashboard.py...")
        
        # Create a fixed version by addressing common issues
        with open("broski_dashboard.py", "rb") as f:
            content_bytes = f.read()
            
        # Try to decode with utf-8 first
        try:
            content = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to Windows encoding with replacement for invalid chars
            content = content_bytes.decode('cp1252', errors='replace')
        
        # Check for missing import
        if "import tk" in content and "import tkinter as tk" not in content:
            content = content.replace("import tk", "import tkinter as tk")
            print("  Fixed: Replaced 'import tk' with 'import tkinter as tk'")
        
        # Check for missing mainloop
        if "def __init__" in content and "root.mainloop()" not in content:
            if "if __name__ == \"__main__\":" not in content:
                content += "\n\nif __name__ == \"__main__\":\n    dashboard = BROskiDashboard()\n    dashboard.root.mainloop()\n"
                print("  Fixed: Added missing __main__ section with mainloop()")
        
        # Backup original file
        import shutil
        backup_path = "broski_dashboard.py.bak"
        shutil.copy2("broski_dashboard.py", backup_path)
        print(f"  Created backup of original file: {backup_path}")
        
        # Write the fixed content
        with open("broski_dashboard.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("  Updated broski_dashboard.py with fixes")
except Exception as e:
    print(f"✗ Error attempting to fix dashboard: {str(e)}")

# Provide alternative solution
print("\nFor a quick solution, try using the Simple Dashboard:")
print("  > SIMPLE_DASHBOARD.bat")

print("\nRun instructions:")
print("1. Try updating Tkinter: pip install tk")
print("2. Run the maintenance dashboard: BROSKI_MAINTENANCE.bat")
print("3. Run the simple dashboard: SIMPLE_DASHBOARD.bat")

input("\nPress Enter to exit...")
