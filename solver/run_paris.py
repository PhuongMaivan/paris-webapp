import subprocess
import os

def run_paris(nodes, edges, start, goal):
    # 1. Lấy đường dẫn thư mục solver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "run_paris.sh")
    
    # 2. Tạo đường dẫn cho file input và output dạng .txt thuần túy
    input_file = os.path.join(current_dir, "input.txt")
    output_file = os.path.join(current_dir, "output.txt")

    # 3. SỬA TẠI ĐÂY: Ghi dữ liệu đồ thị theo dạng TEXT thuần túy cho bộ giải đọc hiểu
    with open(input_file, "w") as f:
        # Dòng 1: Số lượng đỉnh và Số lượng cạnh
        f.write(f"{len(nodes)} {len(edges)}\n")
        
        # Các dòng tiếp theo: Liệt kê các cạnh (u v)
        for edge in edges:
            f.write(f"{edge[0]} {edge[1]}\n")
            
        # Dòng tiếp theo: Số lượng token ở Start, rồi liệt kê các đỉnh Start
        f.write(f"{len(start)} " + " ".join(map(str, start)) + "\n")
        
        # Dòng cuối cùng: Số lượng token ở Goal, rồi liệt kê các đỉnh Goal
        f.write(f"{len(goal)} " + " ".join(map(str, goal)) + "\n")

    # 4. Chạy file .sh
    result = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True, text=True)
    
    if result.returncode != 0:
        return {"error": f"Error running solver: {result.stderr}"}

    # 5. Đọc kết quả thô trả về từ bộ giải
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as f:
            return {"result": f.read().strip()}
                
    # Nếu bộ giải in trực tiếp ra màn hình thay vì ghi file
    return {"result": result.stdout.strip()}