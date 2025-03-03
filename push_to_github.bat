@echo off
echo =======================================
echo  BROski Bot - GitHub Upload Script
echo =======================================
echo.

echo This script will help you upload your BROski Bot to GitHub.
echo.

REM Check if Git is installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git first from https://git-scm.com/downloads
    pause
    exit /b
)

REM Ask for GitHub username
set /p GITHUB_USER=Enter your GitHub username: 

echo.
echo Creating .gitignore file to protect sensitive data...
echo.

REM Create .gitignore file
echo # BROski Bot .gitignore file > .gitignore
echo. >> .gitignore
echo # Config files with sensitive data >> .gitignore
echo config.json >> .gitignore
echo. >> .gitignore
echo # Logs >> .gitignore
echo logs/ >> .gitignore
echo *.log >> .gitignore
echo. >> .gitignore
echo # Cache files >> .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo. >> .gitignore
echo # Virtual environment >> .gitignore
echo venv/ >> .gitignore
echo env/ >> .gitignore
echo. >> .gitignore
echo # Data files >> .gitignore
echo *.csv >> .gitignore
echo *.pkl >> .gitignore
echo. >> .gitignore
echo # Other >> .gitignore
echo .DS_Store >> .gitignore
echo .env >> .gitignore

echo Creating config.example.json from your config.json...
REM Create example config file without sensitive data
if exist config.json (
    type config.json | findstr /v "api_key api_secret" > config.example.json
) else (
    echo ERROR: config.json not found! Skipping example creation.
)

echo.
echo Initializing Git repository...
git init

echo.
echo Adding files to repository...
git add .

echo.
echo Creating initial commit...
git commit -m "Initial commit of BROski Bot"

echo.
echo.
echo Please complete these steps manually:
echo 1. Go to https://github.com/new
echo 2. Create a new repository named "BROski-Bot"
echo 3. Do NOT initialize with README, .gitignore, or license
echo 4. After creating, run these commands:
echo.
echo    git remote add origin https://github.com/%GITHUB_USER%/BROski-Bot.git
echo    git push -u origin master
echo.

echo When ready, press any key to continue...
pause > nul

set /p CONTINUE=Have you created the GitHub repository? (Y/N): 
if /i "%CONTINUE%" neq "Y" (
    echo Please create the GitHub repository and then run this script again.
    pause
    exit /b
)

echo.
echo Connecting to GitHub...
git remote add origin https://github.com/%GITHUB_USER%/BROski-Bot.git

echo.
echo Pushing code to GitHub...
git push -u origin master

echo.
echo =======================================
echo  Upload Complete!
echo =======================================
echo.
echo Your BROski Bot code is now on GitHub at:
echo https://github.com/%GITHUB_USER%/BROski-Bot
echo.
pause
