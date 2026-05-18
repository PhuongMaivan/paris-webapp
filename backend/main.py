import sys
import os

# 1. Ép Python phải tìm kiếm module từ thư mục gốc của dự án (/app)
# Điều này giúp Docker và Railway nhận diện được thư mục 'solver' ngay lập tức
current_file_path = os.path.abspath(__file__) # Đường dẫn file main.py
backend_dir = os.path.dirname(current_file_path) # Thư mục backend
root_dir = os.path.dirname(backend_dir) # Thư mục gốc chứa cả backend và solver
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from solver import run_paris  # Đã an toàn, không còn sợ lỗi ImportError!

app = FastAPI()

# 2. Cấu hình CORS
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

# 3. Các API Endpoint
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    return run_paris(req.nodes, req.edges, req.start, req.goal)

@app.get("/health")
def health():
    return {"status": "ok"}

# 4. Cấu hình phục vụ Frontend (Đoạn này đã được tối ưu để không lỗi MIME)
frontend_dist_path = os.path.join(root_dir, "frontend", "dist")

# Mount thư mục assets trước để xử lý file tĩnh (.js, .css)
assets_path = os.path.join(frontend_dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Route phục vụ trang chủ index.html
@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    # Debug nếu không thấy file (Sẽ hiện lên web để bạn chụp mình xem)
    files_in_dist = os.listdir(frontend_dist_path) if os.path.exists(frontend_dist_path) else "Folder dist khong ton tai"
    return {
        "error": "Khong thay index.html", 
        "debug_path": index_file,
        "files_in_dist": files_in_dist
    }

# Route catch-all cho React Router
@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "File not found"}