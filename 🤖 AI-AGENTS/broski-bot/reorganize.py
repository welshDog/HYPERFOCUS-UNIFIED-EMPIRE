"""
Script to reorganize the BROski project structure by moving files into appropriate subdirectories.
This reduces root directory clutter while maintaining project functionality.
"""

import os
import shutil
import sys
from pathlib import Path

# Define the directory structure
DIRECTORIES = {
    "core": [
        "BROski_Control_Center.py", 
        "start_bot.py",
        "direct_bot.py",
        "launch_broski.py",
        "master_install.py",
        "config.py",
        "exchange_connector.py"
    ],
    "utils": [
        "check_system.py",
        "create_config.py",
        "emergency_kill.py",
        "copy_config.py",
        "fix_imports.py",
        "kill_processes.py",
        "time_import_fix.py",
        "update_config.py",
        "fix_reset_config.py",
        "package_broski.py"
    ],
    "ui": [
        "broski_dashboard.py",
        "maintenance_dashboard.py",
        "trade_results_window.py",
        "broski_launcher.py"
    ],
    "monitor": [
        "bot_monitor.py",
        "bot_monitor_enhanced.py",
        "monitor_logger.py",
        "cli.py"
    ],
    "docs": [
        "*.md",  # All markdown files
        "TESTING_GUIDE.md",
        "PERFORMANCE_GUIDE.md",
        "QUICK_START.md",
        "README.md",
        "*.txt"   # All text files
    ],
    "setup": [
        "setup.py",
        "install_dependencies.py",
        "wizard.py"
    ],
    "launcher": [
        "*.bat"  # All batch files
    ]
}

def create_directory_structure():
    """Create the new directory structure."""
    print("Creating directory structure...")
    
    # Create each directory if it doesn't exist
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def move_files():
    """Move files to their appropriate directories."""
    print("\nMoving files to appropriate directories...")
    
    # Process each directory and file list
    for directory, file_patterns in DIRECTORIES.items():
        for pattern in file_patterns:
            # Handle wildcards
            if "*" in pattern:
                extension = pattern.replace("*", "")
                for file in os.listdir("."):
                    if file.endswith(extension) and os.path.isfile(file):
                        # Don't move this script itself
                        if file == os.path.basename(__file__):
                            continue
                        try:
                            dest_path = os.path.join(directory, file)
                            # Don't overwrite existing files
                            if not os.path.exists(dest_path):
                                shutil.move(file, dest_path)
                                print(f"  Moved {file} to {directory}/")
                        except Exception as e:
                            print(f"  Error moving {file}: {e}")
            else:
                # Direct file match
                if os.path.exists(pattern) and os.path.isfile(pattern):
                    try:
                        dest_path = os.path.join(directory, pattern)
                        # Don't overwrite existing files
                        if not os.path.exists(dest_path):
                            shutil.move(pattern, dest_path)
                            print(f"  Moved {pattern} to {directory}/")
                    except Exception as e:
                        print(f"  Error moving {pattern}: {e}")

def create_gitignore():
    """Create a .gitignore file with common Python patterns."""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/

# Logs and databases
*.log
*.sqlite
logs/

# User-specific files
config.json
*.backup.json
backups/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("\n✓ Created .gitignore file")

def create_imports_fix():
    """Create a fix_imports.py script that helps modules find each other after reorganization."""
    fix_imports_content = '''"""
Import fixer for BROski modules after reorganization.
Add this import at the top of scripts that need to import from other directories:

from fix_imports import fix_paths
fix_paths()
"""

import os
import sys
from pathlib import Path

def fix_paths():
    """Add all project subdirectories to the Python path."""
    # Get the project root directory (parent of this file's directory)
    project_root = Path(__file__).resolve().parent.parent
    
    # Add root and all direct subdirectories to path
    dirs_to_add = [project_root] + [
        project_root / d for d in os.listdir(project_root) 
        if os.path.isdir(project_root / d)
    ]
    
    for directory in dirs_to_add:
        dir_str = str(directory)
        if dir_str not in sys.path:
            sys.path.insert(0, dir_str)
            
    return True

if __name__ == "__main__":
    # When run directly, print current path information
    fix_paths()
    print("Python path updated to include BROski directories:")
    for path in sys.path[:10]:  # Show first 10 paths
        print(f"  - {path}")
'''
    
    # Create utils directory if it doesn't exist
    os.makedirs("utils", exist_ok=True)
    
    # Write the fix_imports.py script
    with open(os.path.join("utils", "fix_imports.py"), "w") as f:
        f.write(fix_imports_content)
    
    print("\n✓ Created utils/fix_imports.py helper module")

def main():
    print("🚀 BROski Project Reorganization 🚀")
    print("===================================")
    
    # Ask for confirmation
    confirm = input("This will reorganize your BROski project files into subdirectories.\n"
                   "Are you sure you want to proceed? (y/n): ").lower()
    
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Create backup
    print("\nCreating backup directory...")
    backup_dir = "backup_before_reorg"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy all Python and batch files to backup
    for file in os.listdir("."):
        if (file.endswith(".py") or file.endswith(".bat")) and os.path.isfile(file):
            try:
                shutil.copy2(file, os.path.join(backup_dir, file))
            except Exception as e:
                print(f"Error backing up {file}: {e}")
    
    print(f"✓ Backed up Python and batch files to {backup_dir}/")
    
    # Create directories and move files
    create_directory_structure()
    move_files()
    create_gitignore()
    create_imports_fix()
    
    print("\n✅ Project reorganization complete!")
    print("\nNote: You may need to update imports in some files.")
    print("Use the utils/fix_imports.py module in files that need to import from other directories.")
    print("\nExample usage:")
    print("```python")
    print("from utils.fix_imports import fix_paths")
    print("fix_paths()")
    print("```")

if __name__ == "__main__":
    main()
