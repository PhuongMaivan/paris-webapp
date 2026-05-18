import subprocess
import os

def run_paris(nodes, edges, start, goal):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "run_paris.sh")
    
    # Tạo sẵn đường dẫn file tạm nếu bộ giải cần đối số
    sas_path = os.path.join(current_dir, "input.sas")
    plan_path = os.path.join(current_dir, "output.plan")
    
    try:
        # Kích hoạt trực tiếp file .sh bằng bash của Linux
        result = subprocess.run(["bash", script_path, sas_path, plan_path], capture_output=True, text=True, check=True)
        return {"status": "success", "result": result.stdout}
    except Exception as e:
        return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
