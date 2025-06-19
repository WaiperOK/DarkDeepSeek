@echo off
title DarkDeepSeek Terminal - Elite Cybersecurity Platform by WaiperOK
chcp 65001 >nul

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

REM Проверка Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python found
) else (
    echo ✗ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Установка зависимостей
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, skipping dependency check
)

REM Запуск приложения
echo.
echo Starting DarkDeepSeek Terminal...
echo.
python run.py

pause 