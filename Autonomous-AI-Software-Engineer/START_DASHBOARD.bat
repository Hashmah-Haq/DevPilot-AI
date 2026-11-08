@echo off
setlocal
cd /d "%~dp0"
title DevPilot AI - Local Dashboard
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 launcher.py
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    python launcher.py
  ) else (
    echo.
    echo Python 3 is required. Install it from https://www.python.org/downloads/
    echo During installation, select "Add python.exe to PATH".
    echo Then double-click START_DASHBOARD.bat again.
    pause
    exit /b 1
  )
)
if errorlevel 1 (
  echo.
  echo Startup failed. See launcher_error.log for details.
  pause
)
