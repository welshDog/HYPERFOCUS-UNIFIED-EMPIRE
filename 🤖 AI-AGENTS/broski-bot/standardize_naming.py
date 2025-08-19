"""
Script to standardize naming conventions across BROski files.
This will rename files to follow a consistent naming pattern.
"""

import os
import re
import shutil

def get_standardized_filename(filename):
    """Convert a filename to the standardized format."""
    # Extract base name and extension
    base, ext = os.path.splitext(filename)
    
    # Standardize batch files
    if ext.lower() == '.bat':
        # Convert to uppercase with underscores
        standardized = re.sub(r'[^a-zA-Z0-9]', '_', base).upper()
        return f"{standardized}{ext}"
    
    # Standardize Python files
    elif ext.lower() == '.py':
        # Convert to snake_case
        # First replace any camelCase pattern with snake_case
        snake_case = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', base)
        # Replace non-alphanumeric characters with underscores
        snake_case = re.sub(r'[^a-zA-Z0-9]', '_', snake_case)
        # Convert to lowercase
        snake_case = snake_case.lower()
        # Replace multiple underscores with a single one
        snake_case = re.sub(r'_+', '_', snake_case)
        # Remove leading/trailing underscores
        snake_case = snake_case.strip('_')
        
        # Special case handling for BROski prefix
        if snake_case.startswith(('broski_', 'brosky_')):
            snake_case = 'broski_' + snake_case[snake_case.find('_')+1:]
        
        return f"{snake_case}{ext}"
    
    # For other files, return as is
    return filename

def analyze_naming_conventions():
    """Analyze the current naming conventions used in the project."""
    print("Analyzing naming conventions...")
    
    patterns = {
        "broski_": 0,
        "BROSKI_": 0,
        "BROski_": 0,
        "Broski_": 0,
        "camelCase": 0,
        "snake_case": 0,
        "other": 0
    }
    
    all_files = []
    
    # Get all Python and batch files
    for file in os.listdir("."):
        if (file.endswith(".py") or file.endswith(".bat")) and os.path.isfile(file):
            all_files.append(file)
    
    for file in all_files:
        base, ext = os.path.splitext(file)
        
        # Check naming patterns
        if base.startswith("broski_"):
            patterns["broski_"] += 1
        elif base.startswith("BROSKI_"):
            patterns["BROSKI_"] += 1
        elif base.startswith("BROski_"):
            patterns["BROski_"] += 1
        elif base.startswith("Broski_"):
            patterns["Broski_"] += 1
        elif "_" in base and base.lower() == base:
            patterns["snake_case"] += 1
        elif re.search(r'([a-z][A-Z])', base):
            patterns["camelCase"] += 1
        else:
            patterns["other"] += 1
    
    print("\nNaming Convention Analysis:")
    print("--------------------------")
    total = sum(patterns.values())
    
    if total == 0:
        print("No Python or batch files found.")
        return
    
    for pattern, count in patterns.items():
        percentage = (count / total) * 100
        print(f"{pattern}: {count} files ({percentage:.1f}%)")
    
    print(f"\nTotal files analyzed: {total}")
    
    # Determine the most common pattern
    most_common = max(patterns.items(), key=lambda x: x[1])
    if most_common[1] > 0:
        print(f"\nMost common pattern: {most_common[0]} ({most_common[1]} files)")
        
        # Recommend standardization
        if most_common[0] == "broski_":
            print("Recommended standardization: snake_case with 'broski_' prefix")
        elif most_common[0] in ["BROSKI_", "BROski_", "Broski_"]:
            print("Recommended standardization: Convert all prefixes to 'broski_'")
        elif most_common[0] == "snake_case":
            print("Recommended standardization: Continue using snake_case")
        elif most_common[0] == "camelCase":
            print("Recommended standardization: Convert camelCase to snake_case")
        else:
            print("Recommended standardization: Use snake_case for Python files")

def standardize_filenames():
    """Rename files to follow a standardized naming convention."""
    # Get all Python and batch files
    py_files = [f for f in os.listdir(".") if f.endswith(".py") and os.path.isfile(f)]
    bat_files = [f for f in os.listdir(".") if f.endswith(".bat") and os.path.isfile(f)]
    
    all_files = py_files + bat_files
    
    # Filter out this script
    all_files = [f for f in all_files if f != os.path.basename(__file__)]
    
    changes = []
    for old_name in all_files:
        new_name = get_standardized_filename(old_name)
        if old_name != new_name:
            changes.append((old_name, new_name))
    
    if not changes:
        print("All filenames already follow the standardized convention.")
        return
    
    print("\nProposed changes:")
    print("----------------")
    for old, new in changes:
        print(f"{old} -> {new}")
    
    confirm = input("\nApply these changes? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Create backup directory
    backup_dir = "backup_names"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"\nCreated backup directory: {backup_dir}")
    
    # Apply changes
    for old, new in changes:
        try:
            # Backup original file
            backup_path = os.path.join(backup_dir, old)
            shutil.copy2(old, backup_path)
            
            # Rename file
            os.rename(old, new)
            print(f"Renamed: {old} -> {new}")
        except Exception as e:
            print(f"Error renaming {old}: {e}")
    
    print("\n✅ Naming standardization complete!")
    print(f"Original files backed up to: {backup_dir}/")

def main():
    print("🔄 BROski Filename Standardization Tool")
    analyze_naming_conventions()
    standardize_filenames()

if __name__ == "__main__":
    main()
