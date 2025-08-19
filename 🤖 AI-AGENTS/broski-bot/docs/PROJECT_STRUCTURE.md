# BROski Bot Project Structure Guide

## New Directory Organization

The BROski Bot project has been reorganized into a modular structure for better maintainability:

```
BROski/
├── core/             # Core bot functionality
│   ├── BROski_Control_Center.py
│   ├── start_bot.py
│   ├── direct_bot.py
│   └── ...
├── utils/            # Utility scripts and helpers
│   ├── fix_imports.py
│   ├── check_system.py
│   └── ...
├── ui/               # User interface components
│   ├── broski_dashboard.py
│   └── ...
├── monitor/          # Monitoring and logging tools
│   ├── bot_monitor.py
│   ├── cli.py
│   └── ...
├── docs/             # Documentation files
│   ├── PROJECT_STRUCTURE.md (this file)
│   └── ...
├── setup/            # Installation and setup scripts
│   └── ...
├── launcher/         # Batch files and shortcuts
│   └── ...
├── strategies/       # Trading strategy implementations
│   ├── rsi_strategy.py
│   ├── macd_strategy.py
│   └── ...
├── logs/             # Log files directory
├── data/             # Trading data and history
└── backups/          # Configuration backups
```

## Key Files

- `unified_launcher.py` - Central entry point for all BROski components
- `core/BROski_Control_Center.py` - Main control center GUI
- `utils/fix_imports.py` - Helper for managing imports between directories

## Naming Conventions

The project now follows consistent naming conventions:

- Python files use `snake_case` (e.g., `bot_monitor.py`)
- Batch files use `UPPERCASE_WITH_UNDERSCORES` (e.g., `START_BOT.BAT`)
- All bot-related files use the `broski_` prefix for easy identification

## Import Management

When importing modules across directories, use:

```python
# Add at the top of your file
from utils.fix_imports import fix_paths
fix_paths()

# Now you can import from any directory
from core.module import function
from strategies.rsi_strategy import RSIStrategy
```

## Documentation

- All documentation files are now centralized in the `docs/` directory
- The unified launcher provides access to all documentation through its menu

This new structure improves organization, maintainability, and makes the codebase more professional.
