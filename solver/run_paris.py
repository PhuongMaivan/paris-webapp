import subprocess
import os

def run_paris(nodes, edges, start, goal):
    # 1. Lấy đường dẫn thư mục solver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tên file script tổng điều phối của bạn (Hãy đổi đúng tên file .sh tổng đó)
    script_total_path = os.path.join(current_dir, "solve.sh") 
    
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
    
    # ---- BƯỚC 4: Chẩn đoán lỗi tối cao ----
    # Gom tất cả nhật ký hệ thống lại để xem dòng nào trong solve.sh bị sập
    debug_log = (
        f"--- CONSOLE LOG (STDOUT) ---\n{result.stdout}\n\n"
        f"--- ERROR LOG (STDERR) ---\n{result.stderr}\n\n"
    )

    # Nếu tìm thấy file kết quả decode thành công và có dữ liệu
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            content = f.read().strip()
            # Nếu nội dung file output chứa báo lỗi kết quả rỗng của bộ giải
            if "UNREACHABLE" in content or not content:
                return {"result": debug_log + f"--- DECODE OUTPUT ---\n{content}"}
            return {"result": content}
                
    # Nếu không tìm thấy file output, chứng tỏ luồng dịch dịch/giải đã bị gãy ở giữa
    return {"result": debug_log + "TRẠNG THÁI: Thất bại - Không sinh được file final_output.txt"}