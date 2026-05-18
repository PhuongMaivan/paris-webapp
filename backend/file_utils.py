def write_col(filepath, nodes, edges):
    with open(filepath, "w") as f:
        f.write(f"p edge {len(nodes)} {len(edges)}\n")
        for a, b in edges:
            f.write(f"e {a+1} {b+1}\n")

def write_dat(filepath, start, goal):
    with open(filepath, "w") as f:
        f.write(" ".join(str(n+1) for n in start) + "\n")
        f.write(" ".join(str(n+1) for n in goal) + "\n")

def read_out(filepath):
    import os
    if not os.path.exists(filepath):
        return {"reachable": False, "sequence": []}
    with open(filepath, "r") as f:
        lines = f.readlines()
    if not lines:
        return {"reachable": False, "sequence": []}
    reachable = lines[0].strip() == "YES"
    sequence = []
    if reachable:
        for line in lines[1:]:
            state = [int(x)-1 for x in line.strip().split() if x]
            if state:
                sequence.append(state)
    return {"reachable": reachable, "sequence": sequence}