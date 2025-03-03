import os
import re
import shutil
from datetime import datetime

def analyze_naming_conventions():
    """
    Analyze naming conventions of files in the current directory.
    """
    print("\n📊 Analyzing naming conventions...")
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    
    if not files:
        print("No files found in the directory.")
        return
    
    # Count different naming patterns
    patterns = {'snake_case': 0, 'camelCase': 0, 'PascalCase': 0, 'kebab-case': 0, 'other': 0}
    
    print(f"\nFound {len(files)} files:")
    for file in files:
        name, ext = os.path.splitext(file)
        # Determine file naming style
        if re.match(r'^[a-z][a-z0-9_]*$', name):
            style = "snake_case"
            patterns[style] += 1
        elif re.match(r'^[a-z][a-zA-Z0-9]*$', name) and '_' not in name:
            style = "camelCase"
            patterns[style] += 1
        elif re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
            style = "PascalCase"
            patterns[style] += 1
        elif re.match(r'^[a-z][a-z0-9-]*$', name):
            style = "kebab-case"
            patterns[style] += 1
        else:
            style = "other"
            patterns[style] += 1
        print(f"  - {file} ({style})")
    
    print("\nNaming convention summary:")
    for style, count in patterns.items():
        print(f"  - {style}: {count} files")

def standardize_filenames():
    """
    Standardize filenames according to snake_case convention.
    Creates backups before renaming.
    """
    print("\n🔄 Standardizing filenames...")
    
    # Create backup directory
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"Created backup directory: {backup_dir}")
    
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    renamed_count = 0
    
    for file in files:
        name, ext = os.path.splitext(file)
        # Convert to snake_case
        new_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        new_name = re.sub(r'-', '_', new_name).lower()
        new_file = new_name + ext
        
        if new_file != file:
            # Create backup
            shutil.copy2(file, os.path.join(backup_dir, file))
            # Rename file
            os.rename(file, new_file)
            print(f"  Renamed: {file} → {new_file}")
            renamed_count += 1
    
    print(f"\n✅ Standardization complete! Renamed {renamed_count} files.")

def main():
    print("🔄 BROski Naming Standardization 🔄")
    print("===================================")
    print("\nThis tool will analyze and standardize filenames in your BROski project.")
    print("It will create backups of all files before renaming them.")
    
    # Show the analysis first
    analyze_naming_conventions()
    
    # Ask whether to proceed with standardization
    choice = input("\nDo you want to standardize filenames? (y/n): ").lower()
    if choice == 'y':
        standardize_filenames()
    else:
        print("\nStandardization cancelled. No changes were made.")

if __name__ == "__main__":
    main()
