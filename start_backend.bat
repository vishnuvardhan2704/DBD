@echo off
echo 🌱 Starting ESG Recommender Backend...
echo.
cd /d "%~dp0backend"
echo 📂 Current directory: %CD%
echo 🐍 Python version:
python --version
echo.
echo 🚀 Starting Flask server...
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Backend failed to start!
    echo 💡 Common solutions:
    echo    - Install dependencies: pip install -r requirements.txt
    echo    - Check if port 5000 is available
    echo    - Run setup.py for automatic configuration
    echo.
)
pause 