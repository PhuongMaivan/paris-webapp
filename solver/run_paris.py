import subprocess
import os

def run_paris(nodes, edges, start, goal):
    # Lấy đường dẫn thư mục solver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Định nghĩa file script tổng (Đoạn code shell bạn vừa gửi)
    # Giả sử file shell đó của bạn tên là 'solve_total.sh' (hoặc bạn đổi tên biến bên dưới cho đúng tên file đó)
    script_total_path = os.path.join(current_dir, "solver.sh") 
    
    # Tạo đường dẫn cho 3 file: 2 file input và 1 file kết quả output
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # ---- BƯỚC 1: Ghi file graph.col (Chứa cấu trúc Đồ thị) ----
    with open(col_file, "w") as f:
        # Định nghĩa chuẩn cho file .col (Số lượng đỉnh, số lượng cạnh)
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            # Ghi danh sách cạnh (u v) tăng lên 1 nếu thuật toán gốc của bạn dùng 1-based index
            f.write(f"e {edge[0]} {edge[1]}\n")

    # ---- BƯỚC 2: Ghi file config.dat (Chứa cấu hình Start và Goal) ----
    with open(dat_file, "w") as f:
        # Ghi danh sách các đỉnh chứa token ở Start
        start_str = " ".join(map(str, start))
        f.write(f"Init: {start_str}\n")
        # Ghi danh sách các đỉnh chứa token ở Goal
        goal_str = " ".join(map(str, goal))
        f.write(f"Goal: {goal_str}\n")

    # ---- BƯỚC 3: Chạy file script tổng bằng Bash ----
    # Truyền đủ 3 tham số: col_file ($1), dat_file ($2), output_file ($3)
    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return {"error": f"Script Error: {result.stderr}"}

    # ---- BƯỚC 4: Đọc kết quả đã được decode từ final_output.txt ----
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            content = f.read().strip()
            return {"result": content}
                
    # Nếu không thấy file output thì trả về log lỗi từ console
    return {"result": result.stdout.strip() if result.stdout else "No output plan generated."}