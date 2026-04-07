# 🚀 Complete Setup Guide - ClimateGuard AI

## Prerequisites

- Python 3.10 or higher
- Git
- Hugging Face account (for deployment)
- Docker (optional, for containerized deployment)

---

## Step 1: Install Python 3.10+

### Windows
```bash
# Check version
python --version

# If not 3.10+, download from python.org
```

### Mac
```bash
brew install python@3.10
```

### Linux
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv
```

---

## Step 2: Clone/Setup Project

```bash
# If from Git
git clone <your-repo-url>
cd climateguard-ai

# Or if starting fresh
mkdir climateguard-ai
cd climateguard-ai
# Copy all project files here
```

---

## Step 3: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

---

## Step 4: Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Verify installation
python -c "import openenv; print('✅ OpenEnv installed')"
```

---

## Step 5: Test Environment

```bash
# Run comprehensive tests
python test_environment.py

# Expected output: All tests should pass
# ✅ ALL TESTS PASSED!
```

---

## Step 6: Run Grader

```bash
# Run automated grading
python grader.py

# Expected score: 550+/600 (90%+)
```

---

## Step 7: Start Server Locally

```bash
# Start FastAPI server
uvicorn server.app:app --host 0.0.0.0 --port 7860

# Or use Python
python -m server.app

# Server will be available at:
# http://localhost:7860
```

---

## Step 8: Test API

```bash
# In another terminal, test the API
curl http://localhost:7860/health

# Or open in browser:
# http://localhost:7860/docs
```

---

## Step 9: Setup Git Repository

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: ClimateGuard AI"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/climateguard-ai.git
git branch -M main
git push -u origin main
```

---

## Step 10: Deploy to Hugging Face

### Option A: Using CLI

```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login
# Enter your token from: https://huggingface.co/settings/tokens

# Deploy
python deploy.py YOUR_USERNAME/climateguard-ai
```

### Option B: Manual Upload

1. Go to https://huggingface.co/new-space
2. Create new Space:
   - Name: climateguard-ai
   - SDK: Docker
   - Hardware: CPU basic (free)
3. Upload all files via web interface
4. Wait for build to complete

---

## Step 11: Verify Deployment

```bash
# Check your Space URL
# https://huggingface.co/spaces/YOUR_USERNAME/climateguard-ai

# Test API endpoint
curl https://YOUR_USERNAME-climateguard-ai.hf.space/health
```

---

## 🐳 Docker Deployment (Optional)

### Build and Run

```bash
# Build image
docker build -t climateguard-ai .

# Run container
docker run -p 7860:7860 climateguard-ai

# Or use docker-compose
docker-compose up
```

### Test Docker Container

```bash
# Check if running
docker ps

# View logs
docker logs climateguard-ai

# Test API
curl http://localhost:7860/health
```

---

## 🧪 Testing Checklist

Before submission, verify:

- [ ] All tests pass (`python test_environment.py`)
- [ ] Grader score is 550+/600 (`python grader.py`)
- [ ] Server starts without errors
- [ ] All 5 tasks work (single_crisis, multi_crisis, etc.)
- [ ] API responds at `/health` endpoint
- [ ] Docker build succeeds (if using Docker)
- [ ] Deployed to Hugging Face successfully
- [ ] README.md is complete and clear

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install --upgrade -r requirements.txt
```

### "OpenEnv not found"
```bash
pip install openenv-core>=0.2.2
```

### Port already in use
```bash
# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:7860 | xargs kill -9
```

### Docker build fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t climateguard-ai .
```

### HF deployment fails
```bash
# Re-login
huggingface-cli logout
huggingface-cli login

# Try again
python deploy.py YOUR_USERNAME/climateguard-ai
```

---

## 📚 Additional Resources

- OpenEnv Docs: https://github.com/openenv/openenv
- FastAPI Docs: https://fastapi.tiangolo.com/
- Hugging Face Spaces: https://huggingface.co/docs/hub/spaces
- Docker Docs: https://docs.docker.com/

---

## 💡 Tips for High Score

1. ✅ Make sure all 5 tasks work perfectly
2. ✅ Test with different seeds for reproducibility
3. ✅ Ensure reward function is well-balanced
4. ✅ Add comprehensive documentation
5. ✅ Test cascading effects work correctly
6. ✅ Verify resource consumption logic
7. ✅ Check all crisis types are represented
8. ✅ Ensure code is clean and well-organized

---

## 🎯 Submission Checklist

- [ ] Code pushed to GitHub
- [ ] Deployed to Hugging Face Spaces
- [ ] README.md is complete
- [ ] All tests passing
- [ ] Grader score documented
- [ ] Demo video (optional but recommended)
- [ ] Submission form filled

---

**Good luck with your submission!** 🚀🌍
