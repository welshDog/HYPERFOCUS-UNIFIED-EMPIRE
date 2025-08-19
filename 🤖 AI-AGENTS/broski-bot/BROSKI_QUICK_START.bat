@echo off
title BROski Quick Start Menu
color 0A

:menu
cls
echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ===============================================================
echo                  BROski Bot Quick Start Menu
echo ===============================================================
echo.
echo  [1] START BOT WITH HYPERFOCUS MODE
echo  [2] Start Bot with RSI Strategy
echo  [3] Start Bot with MACD Strategy
echo.
echo  [4] Open Bot Monitor
echo  [5] Show Current Settings
echo  [6] EMERGENCY KILL
echo.
echo  [0] Exit
echo.
echo ===============================================================
echo.

set /p choice=Enter your choice (0-6): 

if "%choice%"=="0" exit
if "%choice%"=="1" goto hyperfocus
if "%choice%"=="2" goto rsi
if "%choice%"=="3" goto macd
if "%choice%"=="4" goto monitor
if "%choice%"=="5" goto settings
if "%choice%"=="6" goto kill

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:hyperfocus
cls
echo.
echo =====================================
echo   Starting Bot with HYPERFOCUS MODE
echo =====================================
echo.
echo Setting strategy to HyperFocus...
python -c "import json; config = json.load(open('config.json', 'r')); config['strategies']['active_strategy'] = 'hyperfocus_strategy'; config['strategies'].setdefault('hyperfocus_strategy', {'enabled': True, 'timeframe': '15m', 'rsi_period': 14, 'rsi_overbought': 70, 'rsi_oversold': 30, 'fast_period': 12, 'slow_period': 26, 'signal_period': 9, 'ma_fast': 20, 'ma_slow': 50, 'volume_factor': 1.5, 'volume_lookback': 20, 'require_confirmation': True, 'smart_exit': True}); config['strategies']['hyperfocus_strategy']['enabled'] = True; json.dump(config, open('config.json', 'w'), indent=2); print('Successfully switched to HyperFocus Mode!')"
echo.
echo Starting the bot...
echo.
start cmd /k python broski_launcher.py
echo.
echo The bot is now starting in a new window.
echo.
pause
goto menu

:rsi
cls
echo.
echo =====================================
echo    Starting Bot with RSI Strategy
echo =====================================
echo.
echo Setting strategy to RSI...
python -c "import json; config = json.load(open('config.json', 'r')); config['strategies']['active_strategy'] = 'rsi_strategy'; config['strategies']['rsi_strategy']['enabled'] = True; json.dump(config, open('config.json', 'w'), indent=2); print('Successfully switched to RSI Strategy!')"
echo.
echo Starting the bot...
echo.
start cmd /k python broski_launcher.py
echo.
echo The bot is now starting in a new window.
echo.
pause
goto menu

:macd
cls
echo.
echo =====================================
echo   Starting Bot with MACD Strategy
echo =====================================
echo.
echo Setting strategy to MACD...
python -c "import json; config = json.load(open('config.json', 'r')); config['strategies']['active_strategy'] = 'macd_strategy'; config['strategies']['macd_strategy']['enabled'] = True; json.dump(config, open('config.json', 'w'), indent=2); print('Successfully switched to MACD Strategy!')"
echo.
echo Starting the bot...
echo.
start cmd /k python broski_launcher.py
echo.
echo The bot is now starting in a new window.
echo.
pause
goto menu

:monitor
cls
echo.
echo =====================================
echo      Starting BROski Monitor
echo =====================================
echo.
start cmd /k monitor_win.bat
echo Monitor started in a new window.
echo.
pause
goto menu

:settings
cls
echo.
echo =====================================
echo     Checking Current Settings
echo =====================================
echo.
python -c "import json; config = json.load(open('config.json', 'r')); print(f'Active strategy: {config[\"strategies\"][\"active_strategy\"]}'); print(f'Auto-trading: {\"Enabled\" if config[\"trading\"][\"auto_trade\"] else \"Disabled\"}'); print(f'Trading pair: {config[\"trading\"][\"base_symbol\"]}/{config[\"trading\"][\"quote_symbol\"]}'); print(f'Trade amount: {config[\"trading\"][\"trade_amount\"]} {config[\"trading\"][\"quote_symbol\"]}')"
echo.
echo Want to change settings?
echo.
set /p settings_choice=Open settings wizard? (y/n): 

if /i "%settings_choice%"=="y" (
    start cmd /k python wizard.py
)
echo.
pause
goto menu

:kill
cls
echo.
echo =====================================
echo     EMERGENCY KILL ACTIVATED
echo =====================================
echo.
echo WARNING: This will cancel all orders and stop the bot!
echo.
set /p kill_confirm=Are you sure? (y/n): 

if /i "%kill_confirm%"=="y" (
    echo.
    echo Executing emergency kill...
    python emergency_kill.py
    echo.
    echo Emergency kill completed.
) else (
    echo.
    echo Emergency kill aborted.
)
echo.
pause
goto menu
