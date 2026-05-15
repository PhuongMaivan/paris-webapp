import subprocess
import os

def run_paris(input_file, output_file):
    # Lấy đường dẫn tuyệt đối của thư mục chứa file này (thư mục solver)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "run_paris.sh")
    
    # Chạy file .sh bằng lệnh bash
    result = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running solver: {result.stderr}")
    return result.stdout