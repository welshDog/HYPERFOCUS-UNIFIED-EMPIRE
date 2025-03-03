@echo off
color 0B
title BROski Bot Health Check

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo             BROski Bot Health Check
echo ====================================================
echo.
echo Running comprehensive system check...
echo.

python check_system.py
set ERRORLEVEL=%ERRORLEVEL%

echo.
echo Press any key to exit...
pause > nul
exit /b %ERRORLEVEL%
