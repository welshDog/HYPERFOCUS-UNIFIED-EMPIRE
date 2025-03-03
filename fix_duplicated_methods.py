"""
This script identifies and resolves duplicated methods across fix files
"""

import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def find_method_definitions(file_path):
    """Find all method definitions in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for "def method_name(self," pattern
        pattern = r'def\s+(\w+)\s*\(self'
        methods = re.findall(pattern, content)
        return methods
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def find_duplicated_methods():
    """Find duplicated method names across Python files"""
    method_map = {}  # method_name -> list of files
    
    # Search through Python files
    for path in Path('.').glob('*.py'):
        file_path = str(path)
        methods = find_method_definitions(file_path)
        
        for method in methods:
            if method not in method_map:
                method_map[method] = []
            method_map[method].append(file_path)
    
    # Find duplicates
    duplicates = {method: files for method, files in method_map.items() if len(files) > 1}
    return duplicates

def show_duplicates_gui(duplicates):
    """Show duplicated methods in a GUI"""
    if not duplicates:
        messagebox.showinfo("No Duplicates", "No duplicated methods found.")
        return
    
    root = tk.Tk()
    root.title("Duplicated Methods")
    root.geometry("600x400")
    
    # Create a frame
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill="both", expand=True)
    
    # Add a label
    tk.Label(frame, text="Duplicated Methods Found", font=("Arial", 14)).pack(pady=10)
    
    # Add a text area
    text = tk.Text(frame, wrap="word")
    text.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Add scrollbar
    scrollbar = tk.Scrollbar(text)
    scrollbar.pack(side="right", fill="y")
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)
    
    # Add duplicate information
    text.insert("1.0", "The following methods are defined in multiple files:\n\n")
    
    for method, files in duplicates.items():
        text.insert("end", f"Method: {method}\n")
        text.insert("end", f"Found in files:\n")
        for file in files:
            text.insert("end", f"  - {file}\n")
        text.insert("end", "\n")
    
    text.insert("end", "To fix duplications:\n")
    text.insert("end", "1. Decide which implementation of each method you want to keep\n")
    text.insert("end", "2. Remove duplicates from other files\n")
    text.insert("end", "3. Use the integrate_methods.py script to merge methods into your main file\n")
    
    # Disable editing
    text.config(state="disabled")
    
    # Add a button to close
    tk.Button(frame, text="Close", command=root.destroy).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    duplicates = find_duplicated_methods()
    
    if duplicates:
        print("Found duplicated methods:")
        for method, files in duplicates.items():
            print(f"Method '{method}' is defined in:")
            for file in files:
                print(f"  - {file}")
            print()
        
        # Show GUI with duplicates
        show_duplicates_gui(duplicates)
    else:
        print("No duplicated methods found.")
        messagebox.showinfo("No Duplicates", "No duplicated methods found.")
