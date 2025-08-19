@echo off
title BROski Bot Launcher
color 0A

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo          BROski Bot - Direct Launcher
echo ====================================================
echo.
echo This launcher will start the trading bot directly,
echo bypassing the dashboard interface.
echo.
echo Performing pre-launch checks...

REM Check for Python
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or newer
    goto :error
)

REM Check for config file
if not exist config.json (
    echo.
    echo ERROR: config.json not found
    echo Please run setup.py or create config.json first
    goto :error
)

REM Check API keys
python -c "import json; c=open('config.json').read(); print('API_CONFIGURED' if json.loads(c)['exchange']['api_key'] != 'YOUR_MEXC_API_KEY_HERE' else 'API_NOT_CONFIGURED')" > temp.txt
set /p API_STATUS=<temp.txt
del temp.txt

if "%API_STATUS%"=="API_NOT_CONFIGURED" (
    echo.
    echo ERROR: API keys not configured
    echo Please update your config.json with valid API keys
    goto :error
)

echo All checks passed! Starting bot...
echo.
echo The bot will run in this window. Do not close it.
echo.
echo Press Ctrl+C to stop the bot.
echo.

REM Start the bot with proper error handling
python start_bot.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Bot stopped with an error
    echo Check the logs folder for details
    goto :error
)

goto :end

:error
echo.
echo ====================================================
echo                     ERROR
echo ====================================================
echo.
echo The bot could not be started due to errors.
echo.
echo Try running BROSKI_RESET.bat to fix common issues.
echo.

:end
echo.
echo Press any key to exit...
pause > nul
