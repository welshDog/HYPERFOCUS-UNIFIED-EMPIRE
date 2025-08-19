@echo off
echo ===================================
echo BROski Bot - Virtual Environment Fix
echo ===================================
echo.
echo This script will:
echo 1. Delete the existing virtual environment
echo 2. Create a new one
echo 3. Install all required dependencies
echo.
echo Press any key to continue or CTRL+C to cancel...
pause > nul

echo.
echo Removing old virtual environment...
if exist venv (
    rmdir /s /q venv
    echo Old environment removed.
) else (
    echo No existing virtual environment found.
)

echo.
echo Creating new virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Make sure you have Python 3.8+ installed and venv module available
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing required packages...
pip install ccxt pandas numpy matplotlib colorama requests

echo.
echo Installing optional packages...
echo Would you like to install optional packages (scikit-learn, ta)?
set /p choice="Enter y/n: "
if /i "%choice%"=="y" (
    pip install scikit-learn ta
    echo Optional packages installed.
) else (
    echo Optional packages skipped.
)

echo.
echo ===================================
echo Virtual environment setup complete!
echo ===================================
echo.
echo To start BROski Bot, run:
echo venv\Scripts\activate.bat
echo python BROski_Control_Center.py
echo.
pause
