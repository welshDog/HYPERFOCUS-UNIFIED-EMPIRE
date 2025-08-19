@echo off
title BROski Bot - Direct Launch
color 0A

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo             BROski Bot - Direct Launch
echo ====================================================
echo.
echo Launching bot directly (bypassing dashboard)...

REM Ensure log directory exists
if not exist logs mkdir logs

REM Clear previous log
echo Bot started at %date% %time% > logs\broski_bot.log

REM Launch bot
echo Starting bot...
python direct_bot.py

echo.
echo Bot has stopped. Press any key to exit...
pause > nul
