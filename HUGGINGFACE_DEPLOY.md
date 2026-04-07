# 🤗 Hugging Face Deployment Guide

## Complete Step-by-Step Guide

---

## Method 1: Automated Script (Easiest) ⭐

### Step 1: Install Hugging Face CLI
```bash
pip install huggingface_hub
```

### Step 2: Login
```bash
huggingface-cli login
```
- Ye browser me open hoga
- Login karo
- Token copy karo
- Paste karo terminal me

### Step 3: Deploy
```bash
python deploy.py YOUR_USERNAME/climateguard-ai
```

Example:
```bash
python deploy.py john/climateguard-ai
```

**Done!** 🎉

---

## Method 2: Manual Upload (Web Interface)

### Step 1: Create Space

1. Go to: https://huggingface.co/new-space
2. Fill details:
   - **Space name**: `climateguard-ai`
   - **License**: `MIT`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic (free)`
3. Click **Create Space**

### Step 2: Upload Files

Upload these files to your Space:

**Required Files:**
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `models.py`
- ✅ `openenv.yaml`
- ✅ `server/__init__.py`
- ✅ `server/app.py`
- ✅ `server/environment.py`
- ✅ `static/index.html`
- ✅ `README.md`

**Optional:**
- `.gitignore`
- `demo.py`
- `test_environment.py`

### Step 3: Wait for Build

- Hugging Face will automatically build your Docker image
- Takes 5-10 minutes
- Check logs for any errors

### Step 4: Access

Your Space will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/climateguard-ai
```

---

## Method 3: Git Push

### Step 1: Clone Space Repository
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/climateguard-ai
cd climateguard-ai
```

### Step 2: Copy Files
```bash
# Copy all required files
cp /path/to/facebook/* .
```

### Step 3: Commit and Push
```bash
git add .
git commit -m "Initial commit: ClimateGuard AI"
git push
```

---

## Troubleshooting

### Build Fails

**Check Dockerfile:**
```dockerfile
# Make sure paths are correct
COPY models.py .
COPY openenv.yaml .
COPY server/ ./server/
COPY static/ ./static/
```

**Check requirements.txt:**
```txt
openenv-core>=0.2.2
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
numpy>=1.24.0
```

### Space Shows Error

1. Check build logs in HF Space
2. Look for missing files
3. Verify Dockerfile CMD is correct:
   ```dockerfile
   CMD ["python", "-m", "server.app"]
   ```

### Port Issues

Make sure Dockerfile exposes port 7860:
```dockerfile
EXPOSE 7860
```

And server runs on 0.0.0.0:
```python
uvicorn.run(app, host="0.0.0.0", port=7860)
```

---

## Pre-Deployment Checklist

Before deploying, verify locally:

```bash
# 1. Test with Docker
docker build -t climateguard-ai .
docker run -p 7860:7860 climateguard-ai

# 2. Access locally
# http://localhost:7860

# 3. Test API
curl http://localhost:7860/health

# 4. Test dashboard
# Open browser: http://localhost:7860
```

If all works locally, it will work on HF! ✅

---

## Files Structure for HF

```
your-space/
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── models.py              # Pydantic models
├── openenv.yaml           # OpenEnv config
├── server/
│   ├── __init__.py
│   ├── app.py            # FastAPI app
│   └── environment.py    # Environment logic
├── static/
│   └── index.html        # Dashboard UI
└── README.md             # Documentation
```

---

## Update Deployed Space

### Method 1: Using Script
```bash
python deploy.py YOUR_USERNAME/climateguard-ai
```

### Method 2: Git Push
```bash
git add .
git commit -m "Update: improvements"
git push
```

### Method 3: Web Interface
- Go to your Space
- Click "Files and versions"
- Upload updated files

---

## Custom Domain (Optional)

1. Go to Space settings
2. Click "Custom domain"
3. Add your domain
4. Update DNS records

---

## Space Settings

### Recommended Settings:

- **Visibility**: Public
- **Hardware**: CPU basic (free tier)
- **Sleep time**: Never (for demos)
- **Secrets**: Add if needed (API keys, etc.)

### Add Secrets (if needed):
1. Go to Space settings
2. Click "Repository secrets"
3. Add secrets (e.g., API keys)

---

## Monitoring

### View Logs
1. Go to your Space
2. Click "Logs" tab
3. Monitor real-time logs

### Check Status
- Green dot = Running
- Red dot = Error
- Yellow dot = Building

---

## Cost

- **CPU basic**: FREE ✅
- **CPU upgrade**: $0.03/hour
- **GPU T4**: $0.60/hour
- **GPU A10G**: $3.15/hour

For this project, **FREE tier is enough!**

---

## Example Spaces

Check these for reference:
- https://huggingface.co/spaces/openai/whisper
- https://huggingface.co/spaces/stabilityai/stable-diffusion

---

## Quick Deploy Script

Save as `quick-deploy.sh`:

```bash
#!/bin/bash

# Quick deploy to Hugging Face
USERNAME="YOUR_USERNAME"
SPACE_NAME="climateguard-ai"

echo "🚀 Deploying to Hugging Face..."

# Login (if not already)
huggingface-cli login

# Deploy
python deploy.py $USERNAME/$SPACE_NAME

echo "✅ Deployed!"
echo "🔗 https://huggingface.co/spaces/$USERNAME/$SPACE_NAME"
```

Run:
```bash
chmod +x quick-deploy.sh
./quick-deploy.sh
```

---

## Post-Deployment

### Share Your Space:
```
🌍 ClimateGuard AI - Live Demo
https://huggingface.co/spaces/YOUR_USERNAME/climateguard-ai

Multi-Crisis Climate Response System with:
- 5 crisis types (Wildfire, Flood, Drought, Hurricane, Heatwave)
- Real-time dashboard
- Interactive API
- Based on NOAA + IPCC data
```

### Add to README:
```markdown
## 🚀 Live Demo

Try it now: [ClimateGuard AI Dashboard](https://huggingface.co/spaces/YOUR_USERNAME/climateguard-ai)
```

---

## Support

If you face issues:
1. Check HF Space logs
2. Test locally with Docker first
3. Ask in HF forums: https://discuss.huggingface.co/

---

## Final Checklist

Before deploying:

- [ ] All files present
- [ ] Dockerfile correct
- [ ] requirements.txt complete
- [ ] Tested locally with Docker
- [ ] README.md updated
- [ ] Logged into HF CLI
- [ ] Space created on HF

After deploying:

- [ ] Build successful
- [ ] Space running (green dot)
- [ ] Dashboard accessible
- [ ] API working
- [ ] No errors in logs

---

**Ready to deploy!** 🚀

Run: `python deploy.py YOUR_USERNAME/climateguard-ai`
