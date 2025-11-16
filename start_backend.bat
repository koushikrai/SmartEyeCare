@echo off
REM Start the backend using Python 3.11 virtual environment
echo Starting SmartEyeCare Backend...
echo.

REM Check if venv exists
if not exist "backend\venv311\Scripts\python.exe" (
    echo ERROR: Python 3.11 virtual environment not found!
    echo Please create it first:
    echo   py -3.11 -m venv backend\venv311
    echo   backend\venv311\Scripts\pip.exe install -r backend/requirements.txt
    echo   backend\venv311\Scripts\pip.exe install mediapipe
    pause
    exit /b 1
)

REM Start backend with venv Python
echo Using Python from: backend\venv311\Scripts\python.exe
echo.
backend\venv311\Scripts\python.exe backend/app.py

