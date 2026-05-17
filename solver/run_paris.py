import subprocess
import os

def run_paris(nodes, edges, start, goal):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_total_path = os.path.join(current_dir, "solve.sh") 
    
    col_file = os.path.join(current_dir, "graph.col")
    dat_file = os.path.join(current_dir, "config.dat")
    output_file = os.path.join(current_dir, "final_output.txt")

    # Trước khi chạy, xóa file output cũ nếu có để tránh nhận nhầm kết quả cũ
    if os.path.exists(output_file):
        os.remove(output_file)

    # ---- Ghi file graph.col ----
    with open(col_file, "w") as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for edge in edges:
            f.write(f"e {edge[0]} {edge[1]}\n")

    # ---- Ghi file config.dat ----
    with open(dat_file, "w") as f:
        f.write(" ".join(map(str, start)) + "\n")
        f.write(" ".join(map(str, goal)) + "\n")

    # ---- Chạy script điều phối ----
    result = subprocess.run(
        ["bash", script_total_path, col_file, dat_file, output_file], 
        capture_output=True, text=True
    )

    # ---- BẮT MA: Trả về Log chi tiết nếu không chạy ra kết quả đúng ----
    stdout_log = result.stdout if result.stdout else "Không có dữ liệu STDOUT"
    stderr_log = result.stderr if result.stderr else "Không có dữ liệu STDERR"
    
    # Đọc nội dung file output nếu nó được sinh ra
    output_content = "File final_output.txt không được sinh ra!"
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            output_content = f.read().strip()

    # Nếu kết quả ra UNREACHABLE hoặc không sinh được file, phun hết log Terminal lên Web luôn
    if "UNREACHABLE" in output_content or "không được sinh ra" in output_content:
        return {
            "result": (
                f"=== HỆ THỐNG TRẢ VỀ: UNREACHABLE ===\n\n"
                f"--- NỘI DUNG FILE OUTPUT ---\n{output_content}\n\n"
                f"--- TERMINAL OUTPUT (STDOUT) ---\n{stdout_log}\n\n"
                f"--- TERMINAL ERROR (STDERR) ---\n{stderr_log}\n"
            )
        }
                
    # Nếu thành công thực sự (Có chuỗi hành động)
    return {"result": output_content}