import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 1. Cấu hình CORS mở rộng cho phép Frontend local (cổng 5173) gọi vào Backend WSL (cổng 8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khai báo cấu trúc dữ liệu nhận từ Frontend
class SolveRequest(BaseModel):
    nodes: List[int]
    edges: List[List[int]]
    start: List[int]
    goal: List[int]

# Tự động tính toán đường dẫn tuyệt đối dựa trên cấu trúc thư mục thực tế
current_file_path = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(backend_dir)

# 2. API Endpoint giải thuật toán - Kết nối trực tiếp với solve.sh mới
@app.post("/solve")
def solve(req: SolveRequest):
    if len(req.nodes) > 50:
        return {"reachable": False, "sequence": [], "result": "Too large. Max 50 nodes."}
    
    # Định nghĩa đường dẫn các file làm việc trong thư mục solver
    solver_dir = os.path.join(root_dir, "solver")
    script_path = os.path.join(solver_dir, "solve.sh")
    
    graph_file = os.path.join(solver_dir, "input.col")
    col_file = os.path.join(solver_dir, "input.dat")
    plan_file_path = os.path.join(solver_dir, "output.plan")
    
    # Dọn dẹp file kết quả cũ trước khi chạy để tránh nhận nhầm dữ liệu cũ khi sập bộ giải
    if os.path.exists(plan_file_path):
        os.remove(plan_file_path)
        
    try:
        # Ghi file đồ thị input.col (Định dạng DIMACS chuẩn - Đỉnh bắt đầu từ 1)
        with open(graph_file, "w") as f:
            f.write(f"p edge {len(req.nodes)} {len(req.edges)}\n")
            for u, v in req.edges:
                f.write(f"e {u + 1} {v + 1}\n")

        # Ghi file quân cờ input.dat (Dòng 1: Start, Dòng 2: Goal - Đỉnh bắt đầu từ 1)
        with open(col_file, "w") as f:
            start_str = " ".join(str(n + 1) for n in req.start)
            goal_str = " ".join(str(n + 1) for n in req.goal)
            f.write(f"{start_str}\n")
            f.write(f"{goal_str}\n")

        # Kích hoạt script solve.sh bằng bash qua Subprocess
        result = subprocess.run(
            ["bash", script_path, graph_file, col_file, plan_file_path], 
            capture_output=True, text=True, check=True
        )
        
        # In log thực thi của Fast Downward ra Terminal Uvicorn để tiện theo dõi
        print("\n=== PARIS SOLVER LOG ===")
        print(result.stdout)
        print("========================\n")
        
        # Kiểm tra và đọc file kết quả output.plan (sau khi đã được decode)
        if os.path.exists(plan_file_path) and os.path.getsize(plan_file_path) > 0:
            with open(plan_file_path, "r") as f:
                plan_content = f.read()
            
            # Xử lý chuỗi kết quả văn bản thành mảng Sequence để Frontend chạy hiệu ứng (Animation)
            lines = [line.strip() for line in plan_content.split("\n") if line.strip()]
            sequence = []
            
            for line in lines:
                # Bỏ qua dòng thông báo trạng thái hoặc dòng chữ lỗi
                if "unreachable" in line.lower() or "failed" in line.lower():
                    continue
                try:
                    # Chuyển chuỗi "1 3 5" thành mảng số nguyên [0, 2, 4] (Trừ 1 để khớp index 0 của Frontend)
                    state = [int(x) - 1 for x in line.split()]
                    sequence.append(state)
                except ValueError:
                    pass

            # Nếu trích xuất được chuỗi các bước đi hợp lệ
            if sequence:
                return {"reachable": True, "sequence": sequence, "result": plan_content}
                
        # Trường hợp bộ giải không tìm ra kết quả (File trống hoặc không sinh ra file)
        return {"reachable": False, "sequence": [], "result": "UNREACHABLE — No reconfiguration sequence exists."}
            
    except subprocess.CalledProcessError as e:
        # Bắt lỗi cú pháp hoặc lỗi crash hệ thống của parser/Fast Downward và in ra Terminal
        print("\n====== CRITICAL SOLVER ERROR ======")
        print("Exit Code:", e.returncode)
        print("Stderr:", e.stderr)
        print("Stdout:", e.stdout)
        print("===================================\n")
        return {"reachable": False, "sequence": [], "result": f"Backend script error: {e.stderr}"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 3. Cấu hình phục vụ giao diện Frontend tĩnh (Khi chạy Monolithic hoặc đẩy lên Railway)
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

# 4. Khối khởi chạy Uvicorn tự động đồng bộ cổng PORT theo Railway và Local
if __name__ == "__main__":
    import uvicorn
    # Tự động lấy cổng do Railway cấp phát, nếu chạy local mặc định sẽ dùng cổng 8080
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)