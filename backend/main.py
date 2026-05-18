from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import subprocess
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 1. Cấu hình CORS chuẩn chỉnh cho Railway
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

# Tự động tính toán đường dẫn tuyệt đối dựa trên cấu trúc thư mục của Railway (/app)
current_file_path = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(backend_dir)

# 2. API Endpoint giải thuật toán bằng cách gọi trực tiếp file .sh
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    
    # Định nghĩa đường dẫn tuyệt đối thẳng từ gốc /app của Container Linux trên Railway
    script_path = "/app/solver/run_paris.sh"
    sas_file_path = "/app/solver/input.sas"
    plan_file_path = "/app/solver/output.plan"
    
    try:
        # Thực thi lệnh với shell=True để Linux nhận diện biến môi trường và quyền thực thi tốt hơn
        subprocess.run(
            f"bash {script_path} {sas_file_path} {plan_file_path}", 
            shell=True, capture_output=True, text=True, check=True
        )
        
        if os.path.exists(plan_file_path):
            with open(plan_file_path, "r") as f:
                plan_content = f.read()
            # Nếu file plan trống (Fast Downward chạy lỗi ngầm) thì trả về unreachable
            if not plan_content.strip():
                return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            return {"status": "success", "result": plan_content}
        else:
            return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            
    except subprocess.CalledProcessError as e:
        # Log lỗi ra bảng điều khiển Railway để nếu có lỗi gì mình nhìn thấy ngay
        print("BỘ GIẢI BÁO LỖI HỆ THỐNG:", e.stderr)
        return {"status": "unreachable", "result": f"UNREACHABLE — no reconfiguration sequence exists."}

@app.get("/health")
def health():
    return {"status": "ok"}

# 3. Cấu hình phục vụ Frontend tĩnh
frontend_dist_path = os.path.join(root_dir, "frontend", "dist")

assets_path = os.path.join(frontend_dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    files_in_dist = os.listdir(frontend_dist_path) if os.path.exists(frontend_dist_path) else "Folder dist khong ton tai"
    return {"error": "Khong thay index.html", "debug_path": index_file, "files_in_dist": files_in_dist}

@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "File not found"}