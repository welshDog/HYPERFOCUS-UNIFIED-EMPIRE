@echo off
title BROski Trade Results
color 0B

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo          BROski Trade Results Dashboard
echo ====================================================
echo.
echo Loading your trading performance dashboard...
echo.
echo This window will show:
echo  - Overall profit/loss summary
echo  - Win rate and performance metrics
echo  - Strategy comparison charts
echo  - Complete trade history
echo.
echo Please wait while the dashboard loads...
echo.

python show_trade_results.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Failed to launch the trade results dashboard.
    echo Please make sure Python and required libraries are installed.
    echo.
    pause
)
