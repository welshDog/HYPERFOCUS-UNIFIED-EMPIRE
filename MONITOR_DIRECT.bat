@echo off
title BROski Bot Monitor
color 0B

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo             BROski Bot Monitor (Basic)
echo ====================================================
echo.
echo This simplified monitor displays real-time bot activity.
echo If nothing appears, the bot might not be running.
echo.
echo Commands:
echo   CTRL+C to exit
echo.
echo Press any key to start monitoring...
pause > nul
cls

:monitor
echo Monitoring broski_bot.log (press CTRL+C to exit)...
echo.

REM Create log directory if it doesn't exist
if not exist logs mkdir logs

REM Create log file if it doesn't exist
if not exist logs\broski_bot.log (
  echo Monitor started > logs\broski_bot.log
)

type logs\broski_bot.log

echo.
echo [Refreshing in 3 seconds...]
timeout /t 3 > nul
cls
goto monitor
