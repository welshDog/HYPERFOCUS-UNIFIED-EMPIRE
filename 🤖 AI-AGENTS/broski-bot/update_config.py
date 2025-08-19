import json
import os
from pathlib import Path
import shutil

def update_config_with_hyperfocus():
    """Add the hyperfocus strategy to an existing config file if it doesn't exist"""
    config_path = Path("config.json")
    example_config_path = Path("config.example.json")
    
    if not config_path.exists():
        print("Error: config.json not found.")
        return False
        
    if not example_config_path.exists():
        print("Error: config.example.json not found.")
        return False
    
    # Create a backup of the current config
    backup_path = Path("config.backup.json")
    shutil.copy(config_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Load the current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Load the example config to get hyperfocus strategy defaults
    with open(example_config_path, 'r') as f:
        example_config = json.load(f)
    
    # Add hyperfocus strategy if it doesn't exist
    if 'hyperfocus_strategy' not in config['strategies']:
        print("Adding hyperfocus_strategy to config.json...")
        config['strategies']['hyperfocus_strategy'] = example_config['strategies']['hyperfocus_strategy']
        print("Successfully added hyperfocus_strategy to config.json")
    
    # Save the updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        
    print("Config file updated successfully.")
    return True

if __name__ == "__main__":
    print("Updating your configuration with HyperFocus strategy...")
    update_config_with_hyperfocus()
    print("Done!")
