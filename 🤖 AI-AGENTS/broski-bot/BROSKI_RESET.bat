@echo off
title BROski Bot Cleanup and Reset
color 0E

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo              BROski Cleanup Utility
echo ====================================================
echo.
echo This script will clean up processes and restore your bot.
echo.
echo Steps that will be performed:
echo  1. Kill any running BROski processes
echo  2. Clean log files
echo  3. Verify configuration
echo  4. Restore proper file associations
echo  5. Reset Python environment
echo.
echo Press any key to begin cleanup...
pause > nul

echo.
echo Step 1: Killing any running BROski processes...
taskkill /F /FI "WINDOWTITLE eq BROski*" /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
echo Process cleanup complete.

echo.
echo Step 2: Cleaning up log files...
if not exist logs mkdir logs
echo. > logs\broski_bot.log
echo. > logs\broski_dashboard.log
echo. > logs\monitor_logger.log
echo Log files reset.

echo.
echo Step 3: Verifying configuration...
if not exist config.json (
    echo Creating new configuration from example...
    if exist config.example.json (
        copy config.example.json config.json >nul
        echo Configuration file created! Please update with your API keys.
    ) else (
        echo Configuration example not found! Please run setup.py manually.
    )
) else (
    echo Configuration file exists.
)

echo.
echo Step 4: Restoring file associations...
python.exe -m pip install --upgrade pip >nul 2>&1

echo.
echo Step 5: Verifying required packages...
python -m pip install ccxt pandas numpy matplotlib colorama requests >nul 2>&1

echo.
echo ====================================================
echo                 Cleanup Complete!
echo ====================================================
echo.
echo Your BROski Bot has been reset and cleaned.
echo.
echo Next steps:
echo  1. Make sure your config.json has valid API keys
echo  2. Run BROSKI_DASHBOARD.bat to start the bot
echo.
echo Press any key to continue...
pause > nul
