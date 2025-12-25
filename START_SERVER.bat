@echo off
title MyKad-LifeLink Backend Server
echo ========================================
echo   MyKad-LifeLink Backend Server
echo ========================================
echo.
echo Starting server on http://127.0.0.1:8000
echo.
echo IMPORTANT: Keep this window open while using the app!
echo Press CTRL+C to stop the server
echo ========================================
echo.
cd /d "%~dp0"
python start_server.py
echo.
echo Server stopped. Press any key to exit...
pause >nul

