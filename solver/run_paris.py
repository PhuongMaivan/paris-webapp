import subprocess
import os

def run_paris(nodes, edges, start, goal):
    # 1. Định nghĩa các đường dẫn file (Nằm gọn trong thư mục solver)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_total_path = os.path.join(current_dir, "solve.sh") 
    
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # ---- BƯỚC 1: Ghi file graph.col chuẩn định dạng DIMACS ----
    with open(col_file, "w") as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            # Vì edges là List[List[int]], ta lấy trực tiếp edge[0] và edge[1]
            f.write(f"e {edge[0]} {edge[1]}\n")

    # ---- BƯỚC 2: Ghi file config.dat (Chỉ có 2 dòng số, cách nhau bởi dấu cách) ----
    with open(dat_file, "w") as f:
        f.write(" ".join(map(str, start)) + "\n")
        f.write(" ".join(map(str, goal)) + "\n")

    # ---- BƯỚC 3: Cấp quyền và Chạy script điều phối solve.sh ----
    try:
        subprocess.run(["chmod", "+x", script_total_path], check=True)
    except Exception:
        pass # Bỏ qua nếu môi trường không hỗ trợ chmod trực tiếp

    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )

    # ---- BƯỚC 4: Trả kết quả về cho backend/main.py ----
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            return {"result": f.read().strip()}
                
    # Nếu có lỗi xảy ra khiến không sinh được file, in log hệ thống để kiểm tra
    return {"result": f"ERROR LOG:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"}