import subprocess
import os

def run_paris(nodes, edges, start, goal):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_total_path = os.path.join(current_dir, "solve.sh") 
    
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # ---- BƯỚC 1: Ghi file graph.col chuẩn định dạng DIMACS ----
    # Sử dụng newline='\n' để ép ghi theo chuẩn Linux, không dính \r
    with open(col_file, "w", newline='\n') as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            f.write(f"e {int(edge[0])} {int(edge[1])}\n")

    # ---- BƯỚC 2: Ghi file config.dat chuẩn (Ép kiểu int và dùng LF) ----
    with open(dat_file, "w", newline='\n') as f:
        # Ép chặt dữ liệu thành số nguyên sạch, loại bỏ mọi tạp chất cấu trúc
        start_vals = [int(n.get('id')) if isinstance(n, dict) else int(n) for n in start]
        goal_vals = [int(n.get('id')) if isinstance(n, dict) else int(n) for n in goal]
        
        f.write(" ".join(map(str, start_vals)) + "\n")
        f.write(" ".join(map(str, goal_vals)) + "\n")

    # ---- BƯỚC 3: Cấp quyền và chạy solve.sh ----
    try:
        subprocess.run(["chmod", "+x", script_total_path], check=True)
    except Exception:
        pass

    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )

    # ---- BƯỚC 4: Đọc kết quả ----
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            # Dùng .strip() để làm sạch mọi ký tự xuống dòng dư thừa
            return {"result": f.read().strip()}
                
    return {"result": f"ERROR LOG:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"}