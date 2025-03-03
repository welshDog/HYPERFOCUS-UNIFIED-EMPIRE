import shutil
import os
from pathlib import Path

# Simple script to copy config.example.json to config.json
example_path = Path('config.example.json')
config_path = Path('config.json')

if not example_path.exists():
    print("Error: config.example.json not found")
else:
    shutil.copy(example_path, config_path)
    print(f"✅ Created config.json using example configuration")
    
    # Check if the file was actually created
    if config_path.exists():
        print("✅ config.json created successfully")
        print("You can now run: python start_bot.py")
    else:
        print("❌ Failed to create config.json")
