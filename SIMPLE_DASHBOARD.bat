@echo off
color 0A
title BROski Simple Dashboard

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  
echo.
echo ====================================================
echo             SIMPLE DASHBOARD
echo ====================================================
echo.
echo This is a simplified dashboard to control BROski Bot.
echo.
echo [1] Start Trading Bot
echo [2] Open Monitor
echo [3] Check Bot Health
echo [4] View Bot Logs
echo [5] Maintenance Dashboard
echo [0] Exit
echo.

:menu
set /p choice="Enter your choice (0-5): "

if "%choice%"=="1" (
    echo Starting trading bot...
    start START_BOT.bat
    goto menu
)
if "%choice%"=="2" (
    echo Opening monitor...
    start MONITOR_DIRECT.bat
    goto menu
)
if "%choice%"=="3" (
    echo Running health check...
    start CHECK_BROSKI.bat
    goto menu
)
if "%choice%"=="4" (
    echo Opening logs directory...
    explorer logs
    goto menu
)
if "%choice%"=="5" (
    echo Opening maintenance dashboard...
    start BROSKI_MAINTENANCE.bat
    goto menu
)
if "%choice%"=="0" (
    echo Exiting...
    exit /b 0
)

echo Invalid choice. Try again.
goto menu
