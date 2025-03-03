@echo off
color 0A
title BROski Bot - Maintenance Dashboard
cls

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  
echo.
echo ====================================================
echo             MAINTENANCE DASHBOARD
echo ====================================================
echo.
echo Loading maintenance dashboard...

python maintenance_dashboard.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running maintenance dashboard.
    echo.
    echo Press any key to exit...
    pause > nul
)
