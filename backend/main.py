from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import subprocess
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    nodes: List[int]
    edges: List[List[int]]
    start: List[int]
    goal:  List[int]

def write_sas_file(req: SolveRequest, filepath: str):
    with open(filepath, "w") as f:
        f.write(f"{len(req.nodes)}\n")
        for i in range(len(req.nodes)):
            f.write(f"node_{i}\n2\n")
        for val in req.start:
            f.write(f"{val}\n")
        f.write(f"{len(req.goal)}\n")
        for i, val in enumerate(req.goal):
            f.write(f"{i} {val}\n")
        f.write(f"{len(req.edges)}\n")
        for edge in req.edges:
            f.write(f"{edge[0]} {edge[1]}\n")

@app.post("/solve")
def solve(req: SolveRequest):
    print("====== DA NHAN DUOC YEU CAU GIAI TOAN TU FRONTEND ======")
    if len(req.nodes) > 50:
        return {"error": "Too large. Max 50 nodes."}
    
    script_path = "/app/solver/run_paris.sh"
    sas_file_path = "/app/solver/input.sas"
    plan_file_path = "/app/solver/output.plan"
    
    try:
        write_sas_file(req, sas_file_path)
        
        if os.path.exists(plan_file_path):
            os.remove(plan_file_path)
            
        print("Dang kich hoat chay file run_paris.sh...")
        result = subprocess.run(
            f"bash {script_path} {sas_file_path} {plan_file_path}", 
            shell=True, capture_output=True, text=True, check=True
        )
        print("Bộ giải Fast Downward log:", result.stdout)
        
        if os.path.exists(plan_file_path):
            with open(plan_file_path, "r") as f:
                plan_content = f.read()
            if not plan_content.strip():
                return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            return {"status": "success", "result": plan_content}
        else:
            print("Loi: Khong tim thay file output.plan sau khi chay!")
            return {"status": "unreachable", "result": "UNREACHABLE — no reconfiguration sequence exists."}
            
    except subprocess.CalledProcessError as e:
        print("BO GIAI GAP LOI C++:", e.stderr)
        return {"status": "unreachable", "result": "UNREACHABLE — solver error."}

@app.get("/health")
def health():
    return {"status": "ok"}

frontend_dist_path = "/app/frontend/dist"
assets_path = os.path.join(frontend_dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Khong thay index.html"}

@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    index_file = os.path.join(frontend_dist_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "File not found"}