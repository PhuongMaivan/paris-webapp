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

    # ---- BƯỚC 1: Ghi file graph.col ----
    with open(col_file, "w", newline='\n') as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            f.write(f"e {int(edge[0])} {int(edge[1])}\n")

    # ---- BƯỚC 2: Ghi file config.dat chuẩn ----
    with open(dat_file, "w", newline='\n') as f:
        start_str = " ".join([str(n) for n in start])
        goal_str = " ".join([str(n) for n in goal])
        
        f.write(f"{start_str}\n")
        f.write(f"{goal_str}\n")

    # ---- BƯỚC 3: CẤP QUYỀN VÀ KÍCH HOẠT SCRIPT ĐIỀU PHỐI (ĐOẠN BỊ THIẾU) ----
    try:
        subprocess.run(["chmod", "+x", script_total_path], check=True)
    except Exception:
        pass

    # Gọi file shell để chạy Fast Downward
    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True, cwd=current_dir
    )

    # ---- BƯỚC 4: Đọc nội dung file output sinh ra ----
    output_content = ""
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            output_content = f.read().strip()

    # === BẪY NỘI GIÁN: Nếu kết quả vẫn báo vô nghiệm hoặc lỗi, xuất thẳng log Terminal lên Web ===
    if "UNREACHABLE" in output_content or not output_content:
        stdout_log = result.stdout if result.stdout else "[Trống]"
        stderr_log = result.stderr if result.stderr else "[Trống]"
        
        error_report = (
            f"=== PHÂN TÍCH LỖI HỆ THỐNG RENDER ===\n\n"
            f"1. KẾT QUẢ FILE OUTPUT:\n{output_content if output_content else '[File trống rỗng - Không sinh được kết quả]'}\n\n"
            f"2. NHẬT KÝ LỆNH CHẠY (STDOUT):\n{stdout_log}\n\n"
            f"3. NHẬT KÝ LỖI HỆ THỐNG (STDERR):\n{stderr_log}\n"
        )
        return {"result": error_report}
                
    # Nếu thành công thực sự (Có chuỗi hành động)
    return {"result": output_content}