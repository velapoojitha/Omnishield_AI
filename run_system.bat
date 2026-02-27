@echo off
title OMNISHIELD AI SYSTEM CONTROL
cd /d C:\OmniShield_AI
echo Starting OmniShield AI Security Suite...  at C:\OmniShield_AI...
echo.

:: Start the Vision Engine in a new window
echo Launching Vision Engine...
start cmd /k "title VISION ENGINE && venv\Scripts\activate && python vision_engine.py"

:: Wait 3 seconds for the camera to initialize
timeout /t 3

:: Start the Web Dashboard in a new window
echo Launching Web Dashboard...
start cmd /k "title WEB DASHBOARD && venv\Scripts\activate && python dashboard.py"

echo.
echo ---------------------------------------------------
echo SYSTEM ONLINE
echo Camera: ACTIVE
echo Server: http://127.0.0.1:5000
echo ---------------------------------------------------
pause