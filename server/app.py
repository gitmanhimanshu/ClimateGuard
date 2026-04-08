"""
FastAPI application for ClimateGuard AI
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server import create_fastapi_app
from models import ClimateAction, ClimateObservation

try:
    from .environment import ClimateGuardEnvironment
except ImportError:
    from server.environment import ClimateGuardEnvironment

# Create FastAPI app
app = create_fastapi_app(
    ClimateGuardEnvironment,
    ClimateAction,
    ClimateObservation
)


def main():
    """Run the server"""
    import uvicorn
    print("\n" + "="*60)
    print("🌍 ClimateGuard AI Server Starting...")
    print("="*60)
    print("\n📍 Server will be available at:")
    print("   http://localhost:7860")
    print("\n📚 API Documentation:")
    print("   http://localhost:7860/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
