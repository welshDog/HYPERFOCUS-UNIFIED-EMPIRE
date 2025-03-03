import os
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(text):
    """Print a formatted section header"""
    width = 60
    print("\n" + "=" * width)
    print(f"{Fore.CYAN}{text.center(width)}{Style.RESET_ALL}")
    print("=" * width + "\n")

def create_model_directories():
    """Create directories needed for ML models"""
    dirs = ["models", "data/training"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def display_ml_guide():
    """Display guide information about the ML strategy"""
    print_header("BROski ML Strategy Guide")
    
    print(f"{Fore.YELLOW}About the ML Strategy{Style.RESET_ALL}")
    print("The Machine Learning strategy uses a trained model to predict")
    print("price movements based on historical data patterns.")
    print("\nWhen configuring the ML strategy, you need to specify:")
    print("1. The path to a pre-trained model file")
    print("2. A confidence threshold for trade signals")
    
    print(f"\n{Fore.YELLOW}Model Path Options:{Style.RESET_ALL}")
    print("1. Use the default path (models/prediction_model.h5)")
    print("   - This will work with the starter model we provide")
    print("2. Specify a custom path if you've trained your own model")
    print("   - Example: models/my_custom_model.h5")
    
    print(f"\n{Fore.YELLOW}About Model Files:{Style.RESET_ALL}")
    print("- Models are typically saved as .h5 files (HDF5 format)")
    print("- The bot includes functionality to train basic models")
    print("- You can also import models trained with external tools")
    
    print(f"\n{Fore.YELLOW}Getting Started with ML:{Style.RESET_ALL}")
    print("1. For beginners: Use the sample model (will be created)")
    print("2. For advanced users: Train a custom model with:")
    print(f"   {Fore.CYAN}python train_model.py{Style.RESET_ALL}")
    
    # Create model directories
    create_model_directories()
    
    # Create a sample model placeholder
    if not os.path.exists("models/prediction_model.h5"):
        with open("models/prediction_model.h5", "wb") as f:
            f.write(b"PLACEHOLDER_MODEL")
        print(f"\n✅ Created placeholder model file at: models/prediction_model.h5")
        print("   (This is a placeholder - use train_model.py to create a real model)")
    
    print(f"\n{Fore.GREEN}Next Steps:{Style.RESET_ALL}")
    print("1. Accept the default model path in the setup wizard")
    print("2. Later, train a proper model using:")
    print(f"   {Fore.CYAN}python train_model.py{Style.RESET_ALL}")
    print("3. Start with a high confidence threshold (0.75-0.85)")
    print("   to reduce false signals")

if __name__ == "__main__":
    display_ml_guide()
