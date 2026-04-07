#!/bin/bash

echo "🐳 ClimateGuard AI - Docker Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker found"
echo ""

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker-compose not found!"
    exit 1
fi

echo "✅ Docker Compose found"
echo ""

# Build and start
echo "🔨 Building Docker image..."
$COMPOSE_CMD build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🚀 Starting ClimateGuard AI..."
    $COMPOSE_CMD up -d
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ClimateGuard AI is running!"
        echo ""
        echo "📍 Access the dashboard at:"
        echo "   http://localhost:7860"
        echo ""
        echo "📚 API Documentation:"
        echo "   http://localhost:7860/docs"
        echo ""
        echo "📊 View logs:"
        echo "   $COMPOSE_CMD logs -f"
        echo ""
        echo "🛑 Stop server:"
        echo "   $COMPOSE_CMD down"
        echo ""
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Build failed"
    exit 1
fi
