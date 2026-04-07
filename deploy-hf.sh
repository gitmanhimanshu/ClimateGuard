#!/bin/bash

echo "🤗 Hugging Face Deployment - ClimateGuard AI"
echo "============================================"
echo ""

# Check if huggingface_hub is installed
if ! python -c "import huggingface_hub" 2>/dev/null; then
    echo "📦 Installing Hugging Face Hub..."
    pip install huggingface_hub
    echo ""
fi

# Check if logged in
echo "🔐 Checking Hugging Face login..."
if ! huggingface-cli whoami &>/dev/null; then
    echo ""
    echo "❌ Not logged in to Hugging Face"
    echo ""
    echo "Please login first:"
    echo "  huggingface-cli login"
    echo ""
    echo "Get your token from: https://huggingface.co/settings/tokens"
    echo ""
    exit 1
fi

echo "✅ Logged in to Hugging Face"
echo ""

# Get username
read -p "Enter your Hugging Face username: " USERNAME
read -p "Enter space name (default: climateguard-ai): " SPACE_NAME

if [ -z "$SPACE_NAME" ]; then
    SPACE_NAME="climateguard-ai"
fi

echo ""
echo "📦 Deploying to: $USERNAME/$SPACE_NAME"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo "🚀 Starting deployment..."
python deploy.py "$USERNAME/$SPACE_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🔗 Your Space: https://huggingface.co/spaces/$USERNAME/$SPACE_NAME"
    echo ""
    echo "Note: It may take 5-10 minutes to build"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check the error messages above"
    echo ""
fi
