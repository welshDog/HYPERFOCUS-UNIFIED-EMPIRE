@echo off
title BROski Bot Monitor - Now with HyperFocus Mode!
color 0B
echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo         BROski Bot Monitor with HyperFocus
echo ====================================================
echo.
echo Features:
echo  - Live updates of your bot's activity
echo  - Color-coded signals (green for buy, red for sell)
echo  - Special Windows-compatible input handling
echo  - NEW! HyperFocus Mode available directly from monitor
echo.
echo Interactive commands:
echo  - Press "t" to toggle timestamps
echo  - Press "f" to set filter (you'll be prompted for keyword)
echo  - Press "v" to view strategy information panel
echo  - Press "h" to enable HyperFocus Mode
echo  - Press "r" to enable RSI Strategy
echo  - Press "m" to enable MACD Strategy
echo  - Press "?" for full help
echo.
echo Press any key to start monitoring...
pause > nul
cls
python bot_monitor.py
pause
