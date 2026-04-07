@echo off
echo 🤗 Hugging Face Deployment - ClimateGuard AI
echo ============================================
echo.

REM Check if huggingface_hub is installed
python -c "import huggingface_hub" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installing Hugging Face Hub...
    pip install huggingface_hub
    echo.
)

REM Check if logged in
echo 🔐 Checking Hugging Face login...
huggingface-cli whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Not logged in to Hugging Face
    echo.
    echo Please login first:
    echo   huggingface-cli login
    echo.
    echo Get your token from: https://huggingface.co/settings/tokens
    echo.
    pause
    exit /b 1
)

echo ✅ Logged in to Hugging Face
echo.

REM Get username
set /p USERNAME="Enter your Hugging Face username: "
set /p SPACE_NAME="Enter space name (default: climateguard-ai): "

if "%SPACE_NAME%"=="" set SPACE_NAME=climateguard-ai

echo.
echo 📦 Deploying to: %USERNAME%/%SPACE_NAME%
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo 🚀 Starting deployment...
python deploy.py %USERNAME%/%SPACE_NAME%

if %errorlevel% equ 0 (
    echo.
    echo ✅ Deployment successful!
    echo.
    echo 🔗 Your Space: https://huggingface.co/spaces/%USERNAME%/%SPACE_NAME%
    echo.
    echo Note: It may take 5-10 minutes to build
    echo.
) else (
    echo.
    echo ❌ Deployment failed
    echo Check the error messages above
    echo.
)

pause
