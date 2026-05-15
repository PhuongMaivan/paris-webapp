from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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

# --- Thêm đoạn này vào dưới cùng của file main.py ---

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Lấy đường dẫn thư mục frontend (nằm cùng cấp với thư mục backend)
# Trong Docker, cấu trúc là /app/backend và /app/frontend
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(current_dir, "frontend")

# 1. Phục vụ các file tĩnh (CSS, JS, v.v.)
# Nếu bạn có thư mục con bên trong frontend thì dùng dòng này
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# 2. Route trả về file index.html khi truy cập trang chủ
@app.get("/")
async def read_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Không tìm thấy file index.html trong thư mục frontend"}