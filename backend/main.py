from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import subprocess
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# --- HÀM QUAN TRỌNG: Chuyển đổi dữ liệu đồ thị từ Web thành file input.sas ---
def write_sas_file(req: SolveRequest, filepath: str):
    with open(filepath, "w") as f:
        # Ghi số lượng đỉnh (variables)
        f.write(f"{len(req.nodes)}\n")
        # Khai báo trạng thái của từng đỉnh (0: trống, 1: có robot)
        for i in range(len(req.nodes)):
            f.write(f"node_{i}\n2\n")  # 2 trạng thái: 0 hoặc 1
        
        # Ghi trạng thái bắt đầu (Initial State)
        for val in req.start:
            f.write(f"{val}\n")
            
        # Ghi trạng thái mục tiêu (Goal State)
        f.write(f"{len(req.goal)}\n")
        for i, val in enumerate(req.goal):
            f.write(f"{i} {val}\n")
            
        # Ghi danh sách cạnh (Cấu trúc kết nối đồ thị)
        f.write(f"{len(req.edges)}\n")
        for edge in req.edges:
            f.write(f"{edge[0]} {edge[1]}\n")

# --- API ENDPOINT CHÍNH ---
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    
    # Định nghĩa chính xác đường dẫn tuyệt đối trong Docker của Railway
    script_path = "/app/solver/run_paris.sh"
    sas_file_path = "/app/solver/input.sas"
    plan_file_path = "/app/solver/output.plan"
    
    try:
        # 1. Ghi dữ liệu đồ thị người dùng vừa vẽ vào file input.sas
        write_sas_file(req, sas_file_path)
        
        # 2. Xóa file kết quả cũ đi nếu có để tránh đọc nhầm
        if os.path.exists(plan_file_path):
            os.remove(plan_file_path)
            
        # 3. Kích hoạt file shell chạy Fast Downward bằng lệnh bash kèm shell=True
        result = subprocess.run(
            f"bash {script_path} {sas_file_path} {plan_file_path}", 
            shell=True, capture_output=True, text=True, check=True
        )
        
        # 4. Đọc file kết quả output.plan trả về Frontend
        if os.path.exists(plan_file_path):
            with open(plan_file_path, "r") as f:
                plan_content = f.read()
            if not plan_content.strip():
                return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            return {"status": "success", "result": plan_content}
        else:
            return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            
    except subprocess.CalledProcessError as e:
        # Nếu bộ giải sập hoặc lỗi đường dẫn, in hẳn log lỗi ra Railway để xem
        print("LỖI CHẠY BỘ GIẢI:", e.stderr)
        return {"status": "unreachable", "result": "UNREACHABLE — solver error or no sequence exists."}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- PHỤC VỤ FILE TĨNH FRONTEND ---
frontend_dist_path = "/app/frontend/dist"

assets_path = os.path.join(frontend_dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Khong thay index.html trong dist"}

@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "File not found"}