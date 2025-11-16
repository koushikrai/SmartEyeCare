# Start the backend using Python 3.11 virtual environment
Write-Host "Starting SmartEyeCare Backend..." -ForegroundColor Green
Write-Host ""

# Check if venv exists
if (-not (Test-Path "backend\venv311\Scripts\python.exe")) {
    Write-Host "ERROR: Python 3.11 virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first:" -ForegroundColor Yellow
    Write-Host "  py -3.11 -m venv backend\venv311"
    Write-Host "  backend\venv311\Scripts\pip.exe install -r backend/requirements.txt"
    Write-Host "  backend\venv311\Scripts\pip.exe install mediapipe"
    Read-Host "Press Enter to exit"
    exit 1
}

# Start backend with venv Python
Write-Host "Using Python from: backend\venv311\Scripts\python.exe" -ForegroundColor Cyan
Write-Host ""
& "backend\venv311\Scripts\python.exe" backend/app.py

