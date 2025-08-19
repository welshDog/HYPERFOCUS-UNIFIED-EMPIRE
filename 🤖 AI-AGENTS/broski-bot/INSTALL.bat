@echo off
echo BROski Bot - Installation Script
echo ==============================
echo.
echo This script will install all required packages for BROski Bot.
echo.
set /p CHOICE=Do you want to proceed? (Y/N): 
if /i "%CHOICE%"=="Y" goto install
goto end

:install
echo.
echo Installing required packages...
python -m pip install --upgrade ccxt pandas matplotlib colorama requests numpy psutil
echo.

echo Do you want to install optional packages?
set /p CHOICE=This includes ML libraries and may take longer (Y/N): 
if /i "%CHOICE%"=="Y" (
    echo.
    echo Installing optional packages...
    python -m pip install --upgrade pywin32 winshell tensorflow scikit-learn ta
)

echo.
echo Installation complete!
echo.
echo You can now start BROski Bot by running:
echo   python BROski_Control_Center.py
echo.
pause

:end
echo.
echo Installation cancelled.
pause