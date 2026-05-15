from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from solver.run_paris import run_paris

app = FastAPI()

# 1. Cấu hình CORS
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

# 2. Các API Endpoint (Phải để TRƯỚC phần phục vụ Frontend)
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    return run_paris(req.nodes, req.edges, req.start, req.goal)

@app.get("/health")
def health():
    return {"status": "ok"}

# 3. Cấu hình phục vụ Frontend (Sửa lại đoạn này của bạn)
# Trong Docker, cấu trúc thư mục thường là: /app/backend/main.py và /app/frontend/dist/
# base_dir của bạn đang lấy ra /app là đúng
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dist_path = os.path.join(base_dir, "frontend", "dist")

# Kiểm tra xem folder assets có tồn tại không để tránh lỗi khi khởi động
assets_path = os.path.join(frontend_dist_path, "assets")

if os.path.exists(assets_path):
    # Mount thư mục assets. Lưu ý: Khi trình duyệt gọi /assets/..., nó sẽ tìm trong folder này.
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Route phục vụ trang chủ index.html
@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend build not found. Check /app/frontend/dist/index.html"}

# Route bổ trợ cho các link khác (nếu dùng React Router)
@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    # Nếu đường dẫn không phải là API (không bắt đầu bằng /solve hoặc /health)
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "File not found"}