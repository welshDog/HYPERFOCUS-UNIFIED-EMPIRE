import os
import json
import shutil
from pathlib import Path

def create_config_from_example():
    """Create a config.json file from the example configuration"""
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    example_config_path = current_dir / 'config.example.json'
    config_path = current_dir / 'config.json'
    
    if not example_config_path.exists():
        print("❌ Error: config.example.json not found!")
        return False
    
    print(f"Creating config.json from example configuration...")
    
    # Read the example config
    with open(example_config_path, 'r') as f:
        config = json.load(f)
    
    # API keys are already set in your example config, so we'll just use those
    
    # Save the config file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration file created: {config_path}")
    print("You can now run the bot with: python start_bot.py")
    return True

if __name__ == "__main__":
    create_config_from_example()
