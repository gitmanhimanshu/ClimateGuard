"""
FastAPI application for ClimateGuard AI with Web UI
"""

import os
import sys
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server import create_fastapi_app
from models import ClimateAction, ClimateObservation

try:
    from .environment import ClimateGuardEnvironment
except ImportError:
    from server.environment import ClimateGuardEnvironment

# Enable web interface
os.environ.setdefault("ENABLE_WEB_INTERFACE", "true")

# Create FastAPI app
app = create_fastapi_app(
    ClimateGuardEnvironment,
    ClimateAction,
    ClimateObservation
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve dashboard at root
@app.get("/")
async def read_root():
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": "ClimateGuard AI API", "docs": "/docs"}


def main():
    """Run the server"""
    import uvicorn
    print("\n" + "="*60)
    print("🌍 ClimateGuard AI Server Starting...")
    print("="*60)
    print("\n📍 Server will be available at:")
    print("   http://localhost:7860")
    print("\n🎨 Dashboard:")
    print("   http://localhost:7860")
    print("\n📚 API Documentation:")
    print("   http://localhost:7860/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
