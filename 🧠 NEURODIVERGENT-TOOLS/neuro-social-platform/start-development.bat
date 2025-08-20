@echo off
REM HYPERFOCUS ZONE DEVELOPMENT LAUNCHER (WINDOWS)
REM Starts all development services for legendary platform building

echo Starting HYPERFOCUS ZONE Development Environment...
echo ================================================================

REM Start BROski Bot (if available)
if exist "..\\..\\🤖 AI-AGENTS\\broski-bot\\START_BROSKI.bat" (
    echo Starting BROski Bot economy service...
    start "BROski Bot" cmd /c "cd /d ..\\..\\🤖 AI-AGENTS\\broski-bot && START_BROSKI.bat"
)

REM Start backend services
echo Starting backend API...
if exist "backend\\package.json" (
    start "Backend API" cmd /c "cd backend && npm run dev"
)

REM Start web application
echo Starting Next.js web app...
if exist "frontend\\web\\package.json" (
    start "Web App" cmd /c "cd frontend\\web && npm run hyperfocus-dev"
)

REM Start mobile development
echo Starting React Native Metro bundler...
if exist "frontend\\mobile\\package.json" (
    start "Mobile Metro" cmd /c "cd frontend\\mobile && npm run start"
)

echo ================================================================
echo DEVELOPMENT ENVIRONMENT ACTIVE!
echo Web: http://localhost:3000
echo Mobile: Metro bundler running
echo API: http://localhost:3001
echo BROski: Economy service active
echo ================================================================
echo READY FOR LEGENDARY DEVELOPMENT!

pause
