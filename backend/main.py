from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import subprocess # 👈 Thêm thư viện này để gọi trực tiếp file .sh từ đây luôn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# Định vị đường dẫn tuyệt đối đến file run_paris.sh nằm trong folder solver
current_file_path = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(backend_dir)
solver_dir = os.path.join(root_dir, "solver")
sh_script_path = os.path.join(solver_dir, "run_paris.sh")

# 2. Các API Endpoint
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    
    # Kiểm tra xem file .sh có tồn tại thật trong container Docker không
    if not os.path.exists(sh_script_path):
        return {"error": f"Không tìm thấy file run_paris.sh tại: {sh_script_path}"}

    try:
        # Thay vì gọi qua cái module import bị lỗi, ta đấm trực tiếp bằng subprocess chuẩn Docker luôn
        # Bác có thể truyền các biến req.nodes, req.edges... vào làm đối số của file .sh nếu cần nhé
        result = subprocess.run(
            ["bash", "run_paris.sh"], 
            cwd=solver_dir,           # Ép Linux nhảy vào đúng thư mục solver để chạy
            capture_output=True,
            text=True,
            check=True
        )
        # Bác dựa vào logic parse kết quả từ chuỗi trả về (stdout) của bác ở local để return ra nhé
        # Ví dụ tạm thời trả về output dạng text:
        return {"status": "success", "result": result.stdout}
        
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

@app.get("/health")
def health():
    return {"status": "ok"}

# 3. Cấu hình phục vụ Frontend
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