@echo off
echo Setting up Voice Journal Environment...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the Python setup script
python setup.py

echo.
echo Setup complete! Press any key to exit...
pause >nul
