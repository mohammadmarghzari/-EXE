@echo off
chcp 65001 >nul
title Building Portfolio360 Ultimate Pro

echo ==========================================
echo  Portfolio360 Ultimate Pro - Build Tool
echo ==========================================
echo.

:: چک کردن Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo [3/5] Running build script...
python build.py

echo [4/5] Cleaning up...
call venv\Scripts\deactivate.bat
rmdir /s /q venv

echo [5/5] Done!
echo.
echo ==========================================
echo  Build completed successfully!
echo  Location: dist\Portfolio360-Ultimate-Pro.exe
echo ==========================================
echo.
pause
