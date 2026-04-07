# 🐳 Docker Setup Guide - ClimateGuard AI

## Quick Start (3 Commands)

```bash
# 1. Build image
docker-compose build

# 2. Run container
docker-compose up

# 3. Open browser
# http://localhost:7860
```

---

## Method 1: Docker Compose (Recommended) ⭐

### Build and Run
```bash
# Build and start in one command
docker-compose up --build

# Or run in background (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Check Status
```bash
# Check if running
docker-compose ps

# View logs
docker-compose logs climateguard

# Restart
docker-compose restart
```

---

## Method 2: Docker CLI

### Build Image
```bash
docker build -t climateguard-ai .
```

### Run Container
```bash
# Run in foreground
docker run -p 7860:7860 climateguard-ai

# Run in background
docker run -d -p 7860:7860 --name climateguard climateguard-ai

# Run with auto-restart
docker run -d -p 7860:7860 --restart unless-stopped --name climateguard climateguard-ai
```

### Manage Container
```bash
# Check status
docker ps

# View logs
docker logs climateguard
docker logs -f climateguard  # Follow logs

# Stop
docker stop climateguard

# Start
docker start climateguard

# Restart
docker restart climateguard

# Remove
docker rm climateguard
```

---

## Access the Application

Once running, access at:
- **Dashboard**: http://localhost:7860
- **API Docs**: http://localhost:7860/docs
- **Health Check**: http://localhost:7860/health

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:7860 | xargs kill -9

# Or use different port
docker run -p 8000:7860 climateguard-ai
```

### Container Won't Start
```bash
# Check logs
docker logs climateguard

# Check if image built correctly
docker images | grep climateguard

# Rebuild without cache
docker build --no-cache -t climateguard-ai .
```

### Permission Denied (Linux)
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

### Out of Disk Space
```bash
# Clean up unused images
docker system prune -a

# Remove specific image
docker rmi climateguard-ai
```

---

## Advanced Usage

### Custom Port
```bash
# Run on port 8000
docker run -p 8000:7860 climateguard-ai

# Access at http://localhost:8000
```

### Environment Variables
```bash
docker run -p 7860:7860 \
  -e PYTHONUNBUFFERED=1 \
  -e ENABLE_WEB_INTERFACE=true \
  climateguard-ai
```

### Volume Mounting (Development)
```bash
# Mount current directory
docker run -p 7860:7860 -v $(pwd):/app climateguard-ai

# Windows PowerShell
docker run -p 7860:7860 -v ${PWD}:/app climateguard-ai
```

### Interactive Shell
```bash
# Enter container
docker exec -it climateguard bash

# Or start with shell
docker run -it climateguard-ai bash
```

---

## Docker Compose Advanced

### Scale Services
```bash
# Run multiple instances
docker-compose up --scale climateguard=3
```

### View Resource Usage
```bash
docker stats climateguard
```

### Update and Restart
```bash
# Pull latest code, rebuild, restart
git pull
docker-compose up --build -d
```

---

## Production Deployment

### Build for Production
```bash
# Build optimized image
docker build -t climateguard-ai:latest .

# Tag for registry
docker tag climateguard-ai:latest myregistry/climateguard-ai:latest

# Push to registry
docker push myregistry/climateguard-ai:latest
```

### Run in Production
```bash
docker run -d \
  -p 7860:7860 \
  --restart always \
  --name climateguard-prod \
  --memory="2g" \
  --cpus="2" \
  climateguard-ai:latest
```

---

## Health Checks

### Manual Health Check
```bash
# Check if healthy
docker inspect --format='{{.State.Health.Status}}' climateguard

# View health check logs
docker inspect --format='{{json .State.Health}}' climateguard | python -m json.tool
```

### Test Endpoints
```bash
# Health endpoint
curl http://localhost:7860/health

# API docs
curl http://localhost:7860/docs
```

---

## Cleanup

### Remove Everything
```bash
# Stop and remove container
docker-compose down

# Remove image
docker rmi climateguard-ai

# Clean all unused resources
docker system prune -a --volumes
```

### Remove Only Container
```bash
docker stop climateguard
docker rm climateguard
```

---

## Multi-Stage Build (Optional)

For smaller image size, use multi-stage build:

```dockerfile
# Build stage
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "-m", "server.app"]
```

---

## Docker Hub Deployment

### Push to Docker Hub
```bash
# Login
docker login

# Tag
docker tag climateguard-ai YOUR_USERNAME/climateguard-ai:latest

# Push
docker push YOUR_USERNAME/climateguard-ai:latest
```

### Pull and Run
```bash
docker pull YOUR_USERNAME/climateguard-ai:latest
docker run -p 7860:7860 YOUR_USERNAME/climateguard-ai:latest
```

---

## Quick Commands Cheat Sheet

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Status
docker-compose ps

# Clean
docker system prune -a
```

---

## Verification

After starting, verify:

1. ✅ Container running: `docker ps`
2. ✅ Health check passing: `docker inspect climateguard`
3. ✅ Dashboard accessible: http://localhost:7860
4. ✅ API working: http://localhost:7860/docs

---

## Performance Tips

1. **Use .dockerignore** - Exclude unnecessary files
2. **Multi-stage builds** - Smaller images
3. **Layer caching** - Faster builds
4. **Resource limits** - Prevent memory issues

---

**Ready to deploy!** 🚀

Run: `docker-compose up`
