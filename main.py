from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import networkx as nx
import random
from datetime import datetime, timedelta
import os

app = FastAPI(title="Supply Chain Digital Twin API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve React app at root
@app.get("/")
async def serve_frontend():
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return {"error": f"Frontend not found: {str(e)}"}

# API endpoints
@app.get("/api/")
def read_root():
    return {"message": "Supply Chain Digital Twin API", "version": "1.0.0"}

# Your existing API endpoints with /api prefix...
@app.get("/api/nodes")
def get_nodes(type: Optional[str] = None):
    # Your existing nodes code here
    pass

@app.get("/api/edges")
def get_edges(type: Optional[str] = None):
    # Your existing edges code here
    pass

@app.get("/api/stats")
def get_stats():
    # Your existing stats code here
    pass

# Add the debug endpoint here
@app.get("/debug/static")
async def debug_static():
    try:
        if os.path.exists("static"):
            files = os.listdir("static")
            return {"static_files": files, "static_exists": True}
        else:
            return {"static_exists": False, "error": "static folder not found"}
    except Exception as e:
        return {"error": str(e)}

# Catch-all route (keep this last)
@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    # your code
