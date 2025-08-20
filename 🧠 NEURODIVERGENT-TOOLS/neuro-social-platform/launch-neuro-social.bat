@echo off
echo 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
echo 🚀 LAUNCHING NEURODIVERGENT SOCIAL PLATFORM! 🚀
echo ❤️‍🔥 Built by neurodivergent developers for neurodivergent minds ❤️‍🔥
echo 🧠 Your ADHD superpowers are about to change the world! 🧠
echo 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
echo.

echo 📦 Setting up development environment...
echo.

REM Change to platform directory
cd /d "h:\HYPERFOCUS-UNIFIED-EMPIRE\🧠 NEURODIVERGENT-TOOLS\neuro-social-platform"

echo 🌐 Starting Next.js Web App...
start "Neuro Social Web" cmd /k "cd frontend\web && npm run dev"

timeout /t 3 /nobreak >nul

echo 📱 Starting React Native Mobile...
start "Neuro Social Mobile" cmd /k "cd frontend\mobile && npm start"

timeout /t 3 /nobreak >nul

echo 🔧 Starting Backend API...
start "Neuro Social Backend" cmd /k "cd backend && npm run dev"

timeout /t 3 /nobreak >nul

echo 💰 Starting BROski Economy Service...
start "BROski Economy" cmd /k "cd ai-agents && python broski-economy-service.py"

echo.
echo 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
echo 🎉 NEURO SOCIAL PLATFORM - DEVELOPMENT DASHBOARD 🎉
echo 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
echo.
echo 🌐 Web App: http://localhost:3000
echo 📱 Mobile Metro: http://localhost:8081
echo 🔧 Backend API: http://localhost:5000
echo 💰 BROski Economy: http://localhost:8888
echo.
echo 🧠 ADHD-Optimized Features:
echo    ✨ Haptic feedback buttons
echo    ⏰ 25-minute focus timers
echo    🎯 Progress celebrations
echo    💰 BROski$ social earning
echo    🤖 AI neurodivergent support agents
echo.
echo 🌟 Ready to build the most AMAZING neuro social platform! 🌟
echo ❤️‍🔥 Your ADHD superpowers are about to change the world! ❤️‍🔥
echo.
echo Press any key to close this dashboard...
pause >nul
