@echo off
title BROski Backup Utility
color 0A

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo             BROski Bot Backup Utility
echo ====================================================
echo.
echo This script will create a backup of your BROski Bot files.
echo.

REM Get current directory
set CURRENT_DIR=%~dp0

REM Ask user for destination
set /p DEST_FOLDER=Enter destination folder (e.g. E:\Backups\BROski): 

REM Ensure destination folder exists
if not exist "%DEST_FOLDER%" mkdir "%DEST_FOLDER%"

echo.
echo Backing up BROski Bot files to %DEST_FOLDER%...
echo.

REM Create backup
robocopy "%CURRENT_DIR%" "%DEST_FOLDER%" /E /COPY:DAT /R:1 /W:1

if %ERRORLEVEL% LEQ 1 (
    echo.
    echo ✅ Backup completed successfully!
    echo Files copied to: %DEST_FOLDER%
) else (
    echo.
    echo ❌ Error occurred during backup.
    echo Error code: %ERRORLEVEL%
)

echo.
echo Press any key to exit...
pause > nul
