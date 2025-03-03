@echo off
color 0E
title BROski Bot Packager

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo             BROski Bot Packaging Tool
echo ====================================================
echo.
echo This tool creates a distributable ZIP package of BROski Bot.
echo The package can be installed on other computers.
echo.
echo Press any key to start packaging...
pause > nul

echo.
echo Creating BROski Bot package...
python package_broski.py
set ERRORLEVEL=%ERRORLEVEL%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Packaging failed! Please check the error message above.
    echo.
) else (
    echo.
    echo Packaging completed! 
    echo The BROski Bot package has been created in the "dist" folder.
)

echo.
echo Press any key to exit...
pause > nul
exit /b %ERRORLEVEL%
