@echo off
color 0A
title BROski Trading Dashboard
cls

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  
echo.
echo ====================================================
echo             TRADING DASHBOARD
echo ====================================================

REM Enable debug output to see any errors
echo Initializing BROski Dashboard...
python broski_dashboard.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Dashboard failed to start. Error code: %ERRORLEVEL%
    echo.
    echo Checking for missing dependencies...
    python -c "import tkinter; print('Tkinter is available')"
    echo.
    echo Press any key to exit...
    pause > nul
)
