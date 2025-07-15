@echo off
echo 🌱 Starting ESG Recommender Frontend...
echo.
cd /d "%~dp0frontend"
echo 📂 Current directory: %CD%
echo 📦 Node.js version:
node --version
echo 📦 npm version:
npm --version
echo.
echo 🚀 Starting React development server...
npm start
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Frontend failed to start!
    echo 💡 Common solutions:
    echo    - Install Node.js from nodejs.org
    echo    - Install dependencies: npm install
    echo    - Check if port 3000 is available
    echo.
)
pause 