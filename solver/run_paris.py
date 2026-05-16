import subprocess
import os

def run_paris(nodes, edges, start, goal):
    # 1. Lấy đường dẫn thư mục solver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tên file script tổng điều phối của bạn (Hãy đổi đúng tên file .sh tổng đó)
    script_total_path = os.path.join(current_dir, "solver.sh") 
    
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # ---- BƯỚC 1: Ghi file graph.col chuẩn DIMACS ----
    with open(col_file, "w") as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            # Ép kiểu int để đảm bảo không bị lỗi dữ liệu dạng chuỗi
            f.write(f"e {int(edge[0])} {int(edge[1])}\n")

    # ---- BƯỚC 2: Ghi file config.dat chuẩn theo yêu cầu của parse_dat ----
    # KHÔNG ghi chữ 'Init:' hay 'Goal:', chỉ ghi danh sách các số cách nhau bởi dấu cách
    with open(dat_file, "w") as f:
        # Dòng 1: Danh sách các đỉnh Start
        start_str = " ".join(map(str, [int(n) for n in start]))
        f.write(f"{start_str}\n")
        
        # Dòng 2: Danh sách các đỉnh Goal
        goal_str = " ".join(map(str, [int(n) for n in goal]))
        f.write(f"{goal_str}\n")

    # ---- BƯỚC 3: Chạy script điều phối ----
    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return {"error": f"Script Error: {result.stderr}"}

    # ---- BƯỚC 4: Đọc kết quả giải từ file final_output.txt ----
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            content = f.read().strip()
            return {"result": content}
                
    # Nếu không có file output, trả về kết quả thô từ terminal (chữ WELCOME hoặc log hành trình)
    return {"result": result.stdout.strip() if result.stdout else "No plan found."}