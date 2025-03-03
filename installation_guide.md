# BROski Crypto Bot - Installation Guide

## Dependency Error
You encountered the following error because the required dependencies are not installed:
```
ModuleNotFoundError: No module named 'ccxt'
```

The `ccxt` library is essential for connecting to cryptocurrency exchanges like MEXC.

## Quick Fix

Run this command to install all required dependencies:
```bash
pip install -r requirements.txt
```

Or use the installation helper script:
```bash
python install_dependencies.py
```

## Complete Installation Guide

### 1. Install Core Dependencies

These libraries are required for the basic functionality:
- `ccxt`: Cryptocurrency exchange API integration
- `colorama`: Terminal text coloring
- `requests`: API communication
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `matplotlib`: Charting and visualization
- `python-telegram-bot`: Telegram notifications

```bash
pip install ccxt colorama requests pandas numpy matplotlib python-telegram-bot
```

### 2. Optional: Install Machine Learning Dependencies

If you want to use the ML strategy, you'll need these additional libraries:
- `tensorflow`: Deep learning framework
- `scikit-learn`: Machine learning utilities

```bash
pip install tensorflow scikit-learn
```

### 3. Optional: Using a Virtual Environment (Recommended)

For a cleaner installation that won't interfere with other Python projects:

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After installation, you can run the bot with:
```bash
python cli.py
```

## Troubleshooting

### Installation Errors
If you encounter errors during installation, try:
1. Update pip: `pip install --upgrade pip`
2. Install packages individually to identify which one is causing issues

### TensorFlow Installation Issues
TensorFlow can sometimes be problematic to install. If you encounter errors:
1. Check [TensorFlow's official documentation](https://www.tensorflow.org/install)
2. Consider using a CPU-only version: `pip install tensorflow-cpu`

### Python Version Compatibility
BROski requires Python 3.7 or higher. Check your version with:
```bash
python --version
```

If you have an older version, please update your Python installation.
