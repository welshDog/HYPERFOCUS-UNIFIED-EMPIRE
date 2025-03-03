@echo off
echo Installing BROski Bot dependencies...
echo.

rem Activate the virtual environment
call venv\Scripts\activate.bat

echo.
echo Installing required packages...
pip install ccxt pandas numpy matplotlib colorama requests

echo.
echo Done! Press any key to exit.
pause > nul
