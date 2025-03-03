@echo off
title BROski Bot Monitor
echo Starting BROski Bot Monitor...
echo.
echo Features:
echo  - Live updates of your bot's activity
echo  - Color-coded signals (green for buy, red for sell)
echo  - Type "f RSI" to filter for RSI-related entries
echo  - Type "t" to toggle timestamps
echo.
echo Press any key to start monitoring...
pause > nul
cls
python bot_monitor.py
pause
