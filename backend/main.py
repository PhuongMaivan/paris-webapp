from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
#from solver import run_paris
from solver.run_paris import run_paris
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    nodes: List[int]
    edges: List[List[int]]
    start: List[int]
    goal:  List[int]

@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    return run_paris(req.nodes, req.edges, req.start, req.goal)

@app.get("/health")
def health():
    return {"status": "ok"}


#----
# Lấy thư mục gốc (thư mục /app trong Docker)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Trỏ thẳng vào thư mục dist vừa build
frontend_dist_path = os.path.join(base_dir, "frontend", "dist")

# Phục vụ các file tĩnh trong assets (quan trọng để load CSS/JS)
assets_path = os.path.join(frontend_dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Route trả về file index.html cho mọi đường dẫn khác
@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    return FileResponse(os.path.join(frontend_dist_path, "index.html"))