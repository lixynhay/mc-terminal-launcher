@echo off
chcp 65001 >nul
title Terminal Launcher
cd /d "%~dp0"

:menu
cls
echo ====================================================
echo         TERMINAL LAUNCHER
echo ====================================================
echo.
echo [1] Start Terminal Launcher
echo [2] Exit
echo.

set /p choice="Select [1-2]: "

if "%choice%"=="1" goto :launch
if "%choice%"=="2" exit /b
goto :menu

:launch
cls
echo ====================================================
echo         START LAUNCHER
echo ====================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [❌] Python not found!
    echo.
    echo Download Python: https://www.python.org/downloads/
    echo.
    pause
    goto :menu
)

python -c "import minecraft_launcher_lib" >nul 2>&1
if errorlevel 1 (
    echo [📦] Installing minecraft-launcher-lib...
    pip install minecraft-launcher-lib -q
    echo.
)

echo [🚀] Start...
echo.
python launcher.py

echo.
pause
goto :menu