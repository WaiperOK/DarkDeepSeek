@echo off
title DarkDeepSeek Terminal - Elite Cybersecurity Platform by WaiperOK
chcp 65001 >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║██████╗  █████╗ ██████╗ ██╗  ██╗██████╗ ███████╗███████╗██████╗ ███████╗██╗  ██╗║
echo ║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██║ ██╔╝║
echo ║██║  ██║███████║██████╔╝█████╔╝ ██║  ██║█████╗  █████╗  ██████╔╝███████╗█████╔╝ ║
echo ║██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ╚════██║██╔═██╗ ║
echo ║██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝███████╗███████╗██║     ███████║██║  ██╗║
echo ║╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo DarkDeepSeek Terminal - Elite Cybersecurity Platform by WaiperOK
echo Copyright (C) 2025 WaiperOK - https://github.com/WaiperOK/DarkDeepS
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found
) else (
    echo Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

if exist requirements.txt (
    echo Installing requirements...
    python -m pip install -r requirements.txt >nul 2>&1
) else (
    echo requirements.txt not found, skipping dependency check
)

echo.
echo Starting DarkDeepSeek Terminal...
echo.

set PYTHONWARNINGS=ignore
set PYTHONDONTWRITEBYTECODE=1
python -W ignore run.py

pause 