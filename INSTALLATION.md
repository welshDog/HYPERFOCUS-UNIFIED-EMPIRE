# BROski Bot Installation Guide

This guide provides complete instructions for installing BROski Bot and all its dependencies.

## Prerequisites

- **Python 3.8+** - BROski Bot requires Python 3.8 or newer
- **Internet Connection** - Required to download dependencies
- **MEXC Account** - You'll need an account to obtain API keys

## Installation Methods

### Method 1: Automated Installation (Recommended)

For a complete setup with all dependencies:

1. Open a command prompt or terminal
2. Navigate to your BROski Bot directory
3. Run the installation script:

```bash
python install_all.py
```

This will:
- Create all required directories
- Install all necessary dependencies
- Generate default configuration files
- Test the installation

### Method 2: Manual Installation

If you prefer to install manually:

#### Step 1: Create Required Directories

Create the following directories in your BROski Bot folder:
- `logs` - For storing bot activity logs
- `data` - For storing market data and analysis
- `backups` - For configuration backups
- `strategies` - For trading strategies

#### Step 2: Install Dependencies

Required packages:
```bash
pip install ccxt pandas numpy matplotlib colorama requests
```

Optional packages:
```bash
pip install scikit-learn ta
```

#### Step 3: Create Configuration

Copy `config.example.json` to `config.json` and update with your settings:
```bash
cp config.example.json config.json
```

## Package Information

- **ccxt**: Cryptocurrency Exchange Trading Library - Provides API access to exchanges
- **pandas**: Data manipulation and analysis library
- **matplotlib**: Plotting and visualization library
- **colorama**: Terminal text coloring for better readability
- **numpy**: Numerical computing library
- **requests**: HTTP library for API calls

Optional packages:
- **scikit-learn**: Machine learning library for advanced strategies
- **ta**: Technical analysis indicators library

## MEXC API Setup

1. Log in to your MEXC account
2. Navigate to "API Management"
3. Create a new API key (Enable trading permissions if you want auto-trading)
4. Copy the API key and secret to your `config.json` file
5. Consider restricting IP addresses for better security

## Starting BROski Bot

After installation is complete:

```bash
python BROski_Control_Center.py
```

## Troubleshooting

If you encounter any issues during installation:

1. **ImportError**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Module not found**: Check if Python path is correctly set
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. **Permission errors**: Try running with administrator/sudo privileges

4. **API Connection errors**: Verify your internet connection and API keys

## Next Steps

1. Configure your API keys in the Configuration tab
2. Start with monitoring mode to observe signals without trading
3. Begin with small trade amounts when enabling auto-trading
4. Regularly check logs for any issues

For more information, see the documentation in the `docs` directory.
