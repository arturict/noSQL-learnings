@echo off
REM MongoDB M165 Project Setup for Windows
REM =======================================

set MONGODB_URI=mongodb://localhost:27017/

echo MongoDB M165 Project Setup
echo ==========================
echo Environment variable MONGODB_URI has been set for this session
echo Available applications:
echo.
echo 1. python environment_demo.py     - Environment variables demo
echo 2. python database_explorer.py    - Database browser
echo 3. python restaurant_crud.py      - Restaurant operations
echo 4. python power_monitor.py        - System monitoring
echo 5. python power_grapher.py        - Monitoring graphs
echo.
echo To make environment variable persistent, run this command as Administrator:
echo setx MONGODB_URI "mongodb://localhost:27017/" /M
echo.

set /p choice="Start an application? (1-5 or n): "

if "%choice%"=="1" (
    python environment_demo.py
) else if "%choice%"=="2" (
    python database_explorer.py
) else if "%choice%"=="3" (
    python restaurant_crud.py
) else if "%choice%"=="4" (
    python power_monitor.py
) else if "%choice%"=="5" (
    python power_grapher.py
) else (
    echo Setup complete!
)

pause
