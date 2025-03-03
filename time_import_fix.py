# Add this to the top of the file that's having issues with time import

import sys
import os

# Fix Python path issues if any
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Make sure time is properly imported
try:
    import time
    print("Time module imported successfully")
except ImportError as e:
    print(f"Error importing time module: {e}")
    # Try alternative approach
    try:
        from time import sleep, time as time_func
        print("Imported specific time functions")
        
        # Create replacement for any missing functions
        if not hasattr(sys.modules[__name__], 'time'):
            time = time_func
    except Exception as e2:
        print(f"Critical error importing time: {e2}")
