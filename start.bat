@echo off
REM WebMents Python Backend Startup Script
REM Author: Anuj Singla (2210991317)

echo ============================================================
echo WebMents Python Backend - Quick Start
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install/Update dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if MongoDB is running
echo Checking MongoDB...
net start MongoDB 2>nul
if errorlevel 1 (
    echo MongoDB service not found or already running
)
echo.

REM Start the server
echo ============================================================
echo Starting WebMents Server...
echo ============================================================
echo.
python run.py

pause
