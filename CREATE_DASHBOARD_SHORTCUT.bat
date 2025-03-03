@echo off
title Creating BROski Dashboard Shortcut
color 0A

echo Creating desktop shortcut for BROski Dashboard...

REM Get the current directory and desktop path
set CURRENT_DIR=%~dp0
set SHORTCUT_NAME=BROski Dashboard.lnk
set DASHBOARD_BAT=%CURRENT_DIR%BROSKI_DASHBOARD.bat
set DESKTOP=%USERPROFILE%\Desktop

REM Create VBScript to make the shortcut (more reliable than PowerShell)
echo Creating temporary VBScript file...
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%DESKTOP%\%SHORTCUT_NAME%"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%DASHBOARD_BAT%"
echo oLink.WorkingDirectory = "%CURRENT_DIR%"
echo If WScript.Arguments.Count ^> 0 Then oLink.IconLocation = WScript.Arguments^(0^)
echo oLink.Save
) > "%TEMP%\CreateShortcut.vbs"

REM Run the VBScript to create the shortcut
echo Running shortcut creation script...
if exist "%CURRENT_DIR%favicon.ico" (
    cscript //nologo "%TEMP%\CreateShortcut.vbs" "%CURRENT_DIR%favicon.ico"
) else (
    cscript //nologo "%TEMP%\CreateShortcut.vbs"
)

REM Clean up the temporary VBScript
del "%TEMP%\CreateShortcut.vbs"

REM Verify the shortcut was created
if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo.
    echo ✅ Desktop shortcut created successfully!
    echo   You can now launch BROski Dashboard by double-clicking
    echo   the shortcut on your desktop.
) else (
    echo.
    echo ❌ Failed to create shortcut.
    echo   You can still launch the dashboard by running BROSKI_DASHBOARD.bat
    
    echo.
    echo Attempting alternative method...
    
    REM Alternative method using direct copy
    copy "%DASHBOARD_BAT%" "%DESKTOP%\BROski Dashboard.bat" > nul
    if exist "%DESKTOP%\BROski Dashboard.bat" (
        echo ✅ Created alternative shortcut (batch file) on desktop.
    ) else (
        echo ❌ All shortcut creation methods failed.
    )
)

echo.
echo Press any key to exit...
pause > nul
