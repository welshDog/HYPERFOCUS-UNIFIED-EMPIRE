@echo off
title BROski Bot Monitor for Windows
echo Starting BROski Bot Windows Monitor...
echo.
echo Features:
echo  - Live updates of your bot's activity
echo  - Color-coded signals (green for buy, red for sell)
echo  - Special Windows-compatible input handling
echo.
echo Interactive commands:
echo  - Press "t" to toggle timestamps
echo  - Press "f" to set filter (you will be prompted for keyword)
echo  - Press "c" to clear filter
echo  - Press "h" to show help
echo  - Press "q" to quit monitor
echo.
echo Press any key to start monitoring...
pause > nul
cls
python bot_monitor.py
pause
