@echo off
echo ============================================================
echo    Cursor Automation Agent - Windows Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Install dependencies
echo Installing dependencies...
echo.
pip install --upgrade pip
pip install pyautogui opencv-python numpy Pillow keyboard mouse anthropic

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages failed to install
    echo Try running this script as Administrator
    echo.
) else (
    echo.
    echo [OK] All dependencies installed successfully
    echo.
)

REM Run diagnostics
echo Running diagnostics...
echo.
python diagnostics.py

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To start using the agent:
echo   1. Basic version:    python cursor_automation_agent.py
echo   2. Advanced version: python advanced_cursor_agent.py
echo   3. Read QUICKSTART.md for examples
echo.
echo Remember to run as Administrator for full permissions!
echo.
pause
