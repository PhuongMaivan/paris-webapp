import subprocess
import os

def run_paris(nodes, edges, start, goal):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_total_path = os.path.join(current_dir, "solve.sh") 
    
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # Xóa file cũ nếu có để tránh đọc nhầm kết quả cũ
    if os.path.exists(output_file):
        os.remove(output_file)

    # ---- Ghi file graph.col ----
    with open(col_file, "w", newline='\n') as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            f.write(f"e {int(edge[0])} {int(edge[1])}\n")

    # ---- Ghi file config.dat ----
    with open(dat_file, "w", newline='\n') as f:
        start_vals = [int(n.get('id')) if isinstance(n, dict) else int(n) for n in start]
        goal_vals = [int(n.get('id')) if isinstance(n, dict) else int(n) for n in goal]
        f.write(" ".join(map(str, start_vals)) + "\n")
        f.write(" ".join(map(str, goal_vals)) + "\n")

    # ---- Chạy script và hứng TOÀN BỘ lỗi ----
    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )

    # Đọc nội dung file output
    output_content = ""
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            output_content = f.read().strip()

    # === BẪY NỘI GIÁN: Nếu kết quả vẫn báo vô nghiệm hoặc lỗi, xuất thẳng log Terminal lên Web ===
    if "UNREACHABLE" in output_content or not output_content:
        # Tạo sớ nhật ký chẩn đoán bệnh
        error_report = (
            f"=== PHÂN TÍCH LỖI HỆ THỐNG RENDER ===\n\n"
            f"1. KẾT QUẢ FILE OUTPUT:\n{output_content if output_content else '[File trống rỗng - Không sinh được kết quả]'}\n\n"
            f"2. NHẬT KÝ LỆNH CHẠY (STDOUT):\n{result.stdout if result.stdout else '[Trống]'}\n\n"
            f"3. NHẬT KÝ LỖI HỆ THỐNG (STDERR):\n{result.stderr if result.stderr else '[Trống]'}\n"
        )
        return {"result": error_report}
                
    # Nếu thành công thực sự (Có chuỗi hành động)
    return {"result": output_content}