"""
This utility helps fix import paths in Python files after the project reorganization.
It scans Python files and updates import statements to work with the new directory structure.
"""

import os
import re
import sys
from pathlib import Path

# Map of old import paths to new import paths
IMPORT_MAP = {
    "from core.BROski_Control_Center import": "from core.BROski_Control_Center import",
    "import core.BROski_Control_Center": "import core.BROski_Control_Center",
    "from core.start_bot import": "from core.start_bot import",
    "import core.start_bot": "import core.start_bot",
    "from core.direct_bot import": "from core.direct_bot import",
    "import core.direct_bot": "import core.direct_bot",
    "from monitor.bot_monitor import": "from monitor.bot_monitor import",
    "import monitor.bot_monitor": "import monitor.bot_monitor",
    "from monitor.cli import": "from monitor.cli import",
    "import monitor.cli": "import monitor.cli",
    "from ui.broski_dashboard import": "from ui.broski_dashboard import",
    "import ui.broski_dashboard": "import ui.broski_dashboard",
    # Add more mappings as needed
}

# Template for the import fixer code to add
FIX_IMPORTS_TEMPLATE = """
# Add path fixing for imports
import sys
import os
from pathlib import Path

# Ensure we can import from any directory
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

"""

def should_add_fix_imports(content):
    """Check if we should add the fix imports code to this file."""
    # If file already has path fixing code, don't add it again
    if "sys.path.insert" in content:
        return False
        
    # If file imports from other directories, add the fix
    for old_import in IMPORT_MAP.keys():
        if old_import in content:
            return True
            
    # Check for common patterns that indicate importing from other directories
    patterns = [
        r"from \w+\.\w+ import",  # from module.submodule import 
        r"import \w+\.\w+",       # import module.submodule
    ]
    
    for pattern in patterns:
        if re.search(pattern, content):
            return True
            
    return False

def fix_file_imports(file_path):
    """Update import statements in a file to use the new structure."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        original_content = content
        
        # Check if we should add fix imports code
        add_fix = should_add_fix_imports(content)
        
        # Replace imports according to the map
        for old_import, new_import in IMPORT_MAP.items():
            content = content.replace(old_import, new_import)
            
        # Add path fixing code if needed
        if add_fix:
            # Find a good spot to add the code (after imports but before code)
            import_section_end = 0
            lines = content.split('\n')
            
            # Find where imports end and code begins
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_section_end = i + 1
                    
            # Insert our fix imports code
            if import_section_end > 0:
                lines.insert(import_section_end, FIX_IMPORTS_TEMPLATE)
                content = '\n'.join(lines)
            else:
                # If no imports found, add at the top after docstring if any
                docstring_end = content.find('"""', content.find('"""') + 3)
                if docstring_end > 0:
                    content = content[:docstring_end+4] + FIX_IMPORTS_TEMPLATE + content[docstring_end+4:]
                else:
                    content = FIX_IMPORTS_TEMPLATE + content
        
        # Check if content was changed
        if content != original_content:
            # Create backup of original file
            backup_dir = Path(file_path).parent / "backups"
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = backup_dir / (Path(file_path).name + ".bak")
            with open(backup_path, 'w') as f:
                f.write(original_content)
                
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
                
            return True
            
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def scan_directory(directory="."):
    """Scan directory for Python files and fix imports."""
    fixed_count = 0
    scanned_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                scanned_count += 1
                
                if fix_file_imports(file_path):
                    fixed_count += 1
                    print(f"✓ Fixed imports in {file_path}")
    
    return scanned_count, fixed_count

def main():
    """Run the import fixer on the project."""
    print("🔧 BROski Import Path Fixer 🔧")
    print("=============================")
    print("This utility updates import statements to work with the new directory structure.")
    
    # Ask for the directory to scan
    directory = input("Enter the directory to scan (press Enter for current directory): ").strip()
    if not directory:
        directory = "."
        
    # Confirm before proceeding
    confirm = input(f"\nThis will scan and modify Python files in {directory}. Proceed? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
        
    print("\nScanning files and fixing imports...")
    scanned_count, fixed_count = scan_directory(directory)
    
    print("\n✅ Import path fixing complete!")
    print(f"Scanned {scanned_count} Python files")
    print(f"Fixed imports in {fixed_count} files")
    
    if fixed_count > 0:
        print("\nNOTE: Backups of modified files were created in their respective 'backups' directories.")

if __name__ == "__main__":
    main()
