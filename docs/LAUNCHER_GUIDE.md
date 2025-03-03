# BROski Unified Launcher Guide

## Introduction

The BROski Unified Launcher provides a central interface to access all components of the BROski Crypto Bot from one convenient location. This eliminates the need for multiple batch files and simplifies the user experience.

## Getting Started

### Launch the Unified Launcher

- **Windows**: Double-click `unified_launcher.py` or run:
  ```
  python unified_launcher.py
  ```

- **Create Desktop Shortcut**: Select option 4 in the Utilities menu, then select "Create Desktop Shortcut"

## Main Menu Options

The launcher presents the following main options:

1. **Start BROski Control Center** - Launch the main GUI control panel
2. **Launch Dashboard** - Open the trading dashboard with charts and metrics
3. **Start Trading Bot** - Start the bot directly in a new window
4. **Monitoring Tools** - Access logs and monitoring utilities
5. **Utilities** - Access system utilities and maintenance tools
6. **Documentation** - Browse and open documentation files
0. **Exit** - Close the launcher

## Monitoring Tools Menu

Access monitoring capabilities:

1. **Launch Command-Line Monitor** - Text-based monitoring interface
2. **Start Enhanced Bot Monitor** - Graphical monitoring dashboard
3. **View Latest Logs** - Display most recent log entries
4. **Check Trading Status** - Show current trading status

## Utilities Menu

Access system utilities:

1. **System Health Check** - Run diagnostics on the bot system
2. **Kill All Bot Processes** - Emergency stop for all bot components
3. **Backup Configuration** - Create backup of current configuration
4. **Create Desktop Shortcut** - Add launcher shortcut to desktop 
5. **Run Maintenance Tasks** - Perform system maintenance

## Documentation Menu

The launcher automatically scans and lists all documentation files (.md) found in your project. Simply select the number of the document you want to read.

## Tips

- You can have multiple components running simultaneously (Control Center + Monitor)
- The launcher uses color coding to make navigation easier
- When a process is launched "in background," it opens in a new window
- Press Enter to return to the previous menu after viewing information

## Troubleshooting

If the launcher doesn't start:

1. Ensure Python 3.8+ is installed and in your PATH
2. Check that all files are in the correct locations after reorganization
3. If colors don't display correctly, try running in a different terminal

For Windows users experiencing issues with color display, you may need to enable ANSI color support in your terminal.
