"""
Helper script to integrate missing methods into BROski_Control_Center.py
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path):
    """Create a backup of a file before modifying it"""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def integrate_methods(target_file, methods_files):
    """Integrate methods from multiple files into the target file"""
    if not backup_file(target_file):
        return
    
    # Read the target file
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {target_file}: {e}")
        return
    
    # Find the class definition
    class_match = re.search(r'class\s+BROskiControlCenter\s*:', content)
    if not class_match:
        print("Error: Could not find BROskiControlCenter class in the target file.")
        return
    
    # Find the end of the class
    # We'll look for the last method in the class
    method_pattern = r'^\s{4}def\s+\w+\s*\(self'  # 4 spaces, def, method name, (self
    last_method = None
    
    for match in re.finditer(method_pattern, content, re.MULTILINE):
        last_method = match
    
    if not last_method:
        print("Error: Could not find methods in the target class.")
        return
    
    # Find the end of the last method by scanning for the next line that's not indented
    lines = content.splitlines()
    method_start_line = content[:last_method.start()].count('\n')
    method_end_line = method_start_line
    
    for i in range(method_start_line + 1, len(lines)):
        # A line that's part of the method will start with at least 8 spaces
        # (4 for class indentation + 4 for method indentation)
        if lines[i].strip() and not lines[i].startswith("        ") and not lines[i].startswith("    def "):
            method_end_line = i - 1
            break
    
    # Extract missing methods from source files
    missing_methods = []
    for methods_file in methods_files:
        try:
            with open(methods_file, 'r', encoding='utf-8') as f:
                methods_content = f.read()
                
            # Extract all method definitions (add 4 spaces for proper indentation)
            for match in re.finditer(r'def\s+(\w+)\s*\(self.*?\):\s*(?:""".*?""")?\s*(.*?)(?=\n\w+|$)', 
                                     methods_content, re.DOTALL):
                method_name = match.group(1)
                
                # Skip if method already exists in target file
                if re.search(rf'def\s+{method_name}\s*\(self', content):
                    print(f"Method {method_name} already exists in target file. Skipping.")
                    continue
                
                # Extract the entire method
                method_text = match.group(0)
                # Add proper indentation (4 spaces)
                indented_method = "    " + method_text.replace("\n", "\n    ")
                missing_methods.append(indented_method)
                
                print(f"Extracted method: {method_name}")
                
        except Exception as e:
            print(f"Error processing {methods_file}: {e}")
    
    # Insert missing methods into target file
    if missing_methods:
        # Split content into before and after insertion point
        insertion_point = content.splitlines()[method_end_line]
        insertion_index = content.index(insertion_point) + len(insertion_point)
        
        before_content = content[:insertion_index]
        after_content = content[insertion_index:]
        
        # Create updated content
        updated_content = before_content + "\n\n" + "\n\n".join(missing_methods) + after_content
        
        # Write updated file
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Successfully integrated {len(missing_methods)} methods into {target_file}")
        except Exception as e:
            print(f"Error writing to {target_file}: {e}")
    else:
        print("No new methods to integrate.")

if __name__ == "__main__":
    target_file = "BROski_Control_Center.py"
    
    # Ensure files exist
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        exit(1)
    
    # Methods source files
    methods_files = [
        "missing_methods.py",
        "final_methods.py",
        "final_remaining_methods.py"
    ]
    
    # Filter for existing files
    existing_methods_files = [f for f in methods_files if os.path.exists(f)]
    
    if not existing_methods_files:
        print("Error: No methods files found.")
        exit(1)
    
    print(f"Integrating methods from {len(existing_methods_files)} files into {target_file}")
    integrate_methods(target_file, existing_methods_files)
