@echo off
echo 🐳 ClimateGuard AI - Docker Setup
echo ==================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker found
echo.

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    set COMPOSE_CMD=docker-compose
) else (
    docker compose version >nul 2>&1
    if %errorlevel% equ 0 (
        set COMPOSE_CMD=docker compose
    ) else (
        echo ❌ docker-compose not found!
        pause
        exit /b 1
    )
)

echo ✅ Docker Compose found
echo.

REM Build and start
echo 🔨 Building Docker image...
%COMPOSE_CMD% build

if %errorlevel% equ 0 (
    echo ✅ Build successful!
    echo.
    echo 🚀 Starting ClimateGuard AI...
    %COMPOSE_CMD% up -d
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ ClimateGuard AI is running!
        echo.
        echo 📍 Access the dashboard at:
        echo    http://localhost:7860
        echo.
        echo 📚 API Documentation:
        echo    http://localhost:7860/docs
        echo.
        echo 📊 View logs:
        echo    %COMPOSE_CMD% logs -f
        echo.
        echo 🛑 Stop server:
        echo    %COMPOSE_CMD% down
        echo.
        pause
    ) else (
        echo ❌ Failed to start container
        pause
        exit /b 1
    )
) else (
    echo ❌ Build failed
    pause
    exit /b 1
)
