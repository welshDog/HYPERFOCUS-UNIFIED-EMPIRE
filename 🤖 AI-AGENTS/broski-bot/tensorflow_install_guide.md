# TensorFlow Installation Guide for BROski Bot

## Understanding the Error

You're seeing this error:
```
ERROR: Could not find a version that satisfies the requirement tensorflow (from versions: none)
ERROR: No matching distribution found for tensorflow
```

This typically happens when:
1. Your Python version isn't compatible with TensorFlow
2. Your system architecture doesn't have pre-built TensorFlow packages
3. There's a connectivity issue with PyPI repositories

## Quick Solutions

### Option 1: Use BROski Without ML Features

The bot works perfectly fine without TensorFlow by using the RSI or MACD strategies:

```bash
# Run this script to switch to non-ML strategies
python ml_alternatives.py
```

### Option 2: Try TensorFlow CPU-Only Version

```bash
pip install tensorflow-cpu
```

### Option 3: Check Python Compatibility

TensorFlow supports Python versions 3.7-3.11. Check your version:

```bash
python --version
```

If your Python version is outside this range, consider installing a compatible version.

## Installation Methods by System Type

### Windows

1. **Make sure you have Visual C++ Redistributable**
   - Download from: https://aka.ms/vs/16/release/vc_redist.x64.exe

2. **Try installing via pip directly**
   ```bash
   pip install tensorflow==2.10.0
   ```

3. **Or try Anaconda/Conda (Recommended)**
   ```bash
   conda create -n brotf python=3.9
   conda activate brotf
   conda install tensorflow
   ```

### macOS

1. **For Intel Macs**
   ```bash
   pip install tensorflow-macos
   ```

2. **For M1/M2/M3 Apple Silicon Macs**
   ```bash
   pip install tensorflow-macos
   pip install tensorflow-metal  # For GPU acceleration
   ```

### Linux

1. **Ubuntu/Debian**
   ```bash
   sudo apt update
   sudo apt install python3-dev python3-pip
   pip3 install tensorflow
   ```

2. **Using Conda (Recommended)**
   ```bash
   conda install tensorflow
   ```

## Using Alternative ML Libraries

If you can't install TensorFlow but still want ML features:

1. Install lighter ML libraries:
   ```bash
   pip install scikit-learn joblib
   ```

2. Run the ML alternatives setup:
   ```bash
   python ml_alternatives.py
   ```

## Getting Help

If you continue to have issues:

1. Join our support channel on Telegram (link in README)
2. Open an issue on our GitHub repository
3. Try the non-ML strategies which require no special ML libraries
