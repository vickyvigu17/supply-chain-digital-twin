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
app.mount("/static", StaticFiles(directory="static/static", check_dir=False), name="static")

# Serve React app at root
@app.get("/")
async def serve_frontend():
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return {"error": f"Frontend not found: {str(e)}"}

# Debug endpoint
@app.get("/debug/static")
async def debug_static():
    try:
        result = {"static_exists": False}
        
        if os.path.exists("static"):
            result["static_exists"] = True
            result["static_files"] = os.listdir("static")
            
            if os.path.exists("static/static"):
                result["static_static_files"] = os.listdir("static/static")
                
                if os.path.exists("static/static/css"):
                    result["css_files"] = os.listdir("static/static/css")
                    
                if os.path.exists("static/static/js"):
                    result["js_files"] = os.listdir("static/static/js")
        
        return result
    except Exception as e:
        return {"error": str(e)}

# API endpoints
@app.get("/api/")
def read_root():
    return {"message": "Supply Chain Digital Twin API", "version": "1.0.0"}

@app.get("/api/nodes")
def get_nodes(type: Optional[str] = None):
    return {"message": "Nodes endpoint"}

@app.get("/api/edges")
def get_edges(type: Optional[str] = None):
    return {"message": "Edges endpoint"}

@app.get("/api/stats")
def get_stats():
    return {"message": "Stats endpoint"}

# Catch-all route
@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return {"error": f"Frontend not found: {str(e)}"}
