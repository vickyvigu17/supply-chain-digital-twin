from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (React build)
app.mount("/static", StaticFiles(directory="static/static", check_dir=False), name="static")

@app.get("/")
async def serve_frontend():
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found"}
    return FileResponse("static/index.html")

# Debug endpoint to check static folder
@app.get("/debug/static")
async def debug_static():
    try:
        return {"static_files": os.listdir("static")}
    except Exception as e:
        return {"error": str(e)}

# Catch-all for React Router
@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    if not os.path.exists("static/index.html"):
        return {"error": "static/index.html not found"}
    return FileResponse("static/index.html")
