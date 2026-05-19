import subprocess, os, hashlib, json
from tracemalloc import start

SOLVER_DIR = "/mnt/c/paris-webapp/solver"
SOLVE_SH   = f"{SOLVER_DIR}/solve.sh"

def get_cache_key(nodes, edges, start, goal):
    data = json.dumps({
        "nodes": sorted(nodes),
        "edges": sorted([sorted(e) for e in edges]),
        "start": sorted(start),
        "goal":  sorted(goal)
    }, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

def write_col(filepath, nodes, edges):
    with open(filepath, "w") as f:
        # Giữ nguyên len(nodes) và len(edges)
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for a, b in edges:
            # XÓA +1: Để nguyên a, b
            f.write(f"e {a} {b}\n")

def write_dat(filepath, start, goal):
    with open(filepath, "w") as f:
        # XÓA +1: Để nguyên n
        f.write(" ".join(str(n) for n in start) + "\n")
        f.write(" ".join(str(n) for n in goal) + "\n")

# Trong solver.py (Backend FastAPI)

def read_out(filepath):
    if not os.path.exists(filepath):
        return {"reachable": False, "sequence": []}
    with open(filepath) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    if not lines or lines[0].upper() == "NO":
        return {"reachable": False, "sequence": []}

    sequence = []
    for line in lines[1:]:
        # Lấy nguyên số từ file .out (0, 2, 1, 3...)
        state = [int(x) for x in line.split() if x.isdigit()]
        sequence.append(state)
    
    return {"reachable": True, "sequence": sequence}

def run_paris(nodes, edges, start, goal, timeout=30):
    # Tạo key để không bị trùng file khi nhiều người dùng cùng lúc
    key = get_cache_key(nodes, edges, start, goal)
    
    # Tạo đường dẫn file tạm
    col_path = f"/tmp/{key}.col"
    dat_path = f"/tmp/{key}.dat"
    out_path = f"/tmp/{key}.out"
    
    # Ghi dữ liệu ra file (Dùng các hàm đã sửa ở trên)
    write_col(col_path, nodes, edges)
    write_dat(dat_path, start, goal)

    try:
        # Log để kiểm tra trong Terminal
        print(f"DEBUG - Running Solver for {len(nodes)} nodes")
        
        # Gọi solve.sh với 3 tham số: .col .dat và file .out kết quả
        subprocess.run(
            ["bash", SOLVE_SH, col_path, dat_path, out_path], 
            timeout=timeout, 
            check=False # Để nó không văng lỗi khi vô nghiệm (Exit code 12)
        )
        
        # Đọc kết quả từ file .out
        return read_out(out_path)
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"reachable": False, "error": str(e)}