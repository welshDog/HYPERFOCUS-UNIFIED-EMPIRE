@echo off
title BROski Strategy Optimizer
color 0A

echo.
echo  ____  ____   __   ____  _  _  __  
echo ^| __ )/ ___^| / /  / ___^|^| ^|/ / ^|_ ^| 
echo ^|  _ \___ \ / /   \___ \^| ' /   ^| ^| 
echo ^| ^|_) ^|__) / /___ ___) ^| . \   ^| ^| 
echo ^|____/____/\____/^|____/^|_^|\_\  ^|_^|  Trading Bot
echo.
echo ====================================================
echo            BROski Strategy Optimizer
echo ====================================================
echo.
echo This tool will analyze your trading data and optimize 
echo the HyperFocus strategy for better performance.
echo.
echo Requirements:
echo  - At least 5 days of trading or monitoring data
echo  - HyperFocus strategy must be enabled in config
echo.
echo Press any key to start optimization...
pause > nul

echo.
echo Analyzing trading data and optimizing parameters...
python strategy_optimizer.py --optimize

echo.
echo Would you like to apply the optimized parameters to your config?
choice /C YN /M "Apply optimized parameters"

if %ERRORLEVEL% EQU 1 (
  echo.
  echo Applying optimized parameters...
  python strategy_optimizer.py --optimize --apply-optimal
)

echo.
echo Would you like to generate a performance report?
choice /C YN /M "Generate performance report"

if %ERRORLEVEL% EQU 1 (
  echo.
  echo Generating performance report...
  python strategy_optimizer.py --report --days 30
)

echo.
echo Optimization complete!
echo.
echo Press any key to exit...
pause > nul
