import subprocess
import os
import json

def run_paris(nodes, edges, start, goal):
    # 1. Lấy đường dẫn thư mục solver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "run_paris.sh")
    
    # 2. Tạo đường dẫn cho file input và output tạm thời
    # Chúng ta ghi dữ liệu ra file để file .sh có cái mà đọc
    input_file = os.path.join(current_dir, "input.json")
    output_file = os.path.join(current_dir, "output.json")

    # 3. Ghi dữ liệu từ React (nodes, edges...) vào file input.json
    input_data = {
        "nodes": nodes,
        "edges": edges,
        "start": start,
        "goal": goal
    }
    with open(input_file, "w") as f:
        json.dump(input_data, f)

    # 4. Chạy file .sh (truyền đường dẫn file vào)
    # Đảm bảo file .sh của bạn nhận 2 tham số là đường dẫn file input và output
    result = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True, text=True)
    
    if result.returncode != 0:
        return {"error": f"Error running solver: {result.stderr}"}

    # 5. Đọc kết quả từ file output_file mà bộ giải C++ vừa tạo ra
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                plan = json.load(f)
                return plan
            except:
                return {"result": f"Raw output: {result.stdout}"}
                
    return {"result": result.stdout}