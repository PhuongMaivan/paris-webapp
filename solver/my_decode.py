import sys, re, os

def parse_col(col_file):
    nodes, edges = [], []
    with open(col_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("p edge"):
                n = int(line.split()[2])
                nodes = list(range(1, n+1))
            elif line.startswith("e "):
                parts = line.split()
                edges.append((int(parts[1]), int(parts[2])))
    return nodes, edges

def parse_dat(dat_file):
    with open(dat_file) as f:
        lines = [l.strip() for l in f if l.strip()]
    start = list(map(int, lines[0].split()))
    goal  = list(map(int, lines[1].split()))
    return start, goal

def decode_plan(plan_file, start):
    if not os.path.exists(plan_file):
        return None
    
    sequence = [list(start)]
    current = set(start)
    
    with open(plan_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            # Fast Downward ghi plan dạng: (jump l1 l2)
            # Chúng ta dùng regex để lấy số sau chữ 'l'
            m = re.search(r'jump l(\d+) l(\d+)', line)
            if m:
                u, v = int(m.group(1)), int(m.group(2))
                if u in current:
                    current.remove(u)
                    current.add(v)
                    sequence.append(list(current))
    return sequence

def main():
    col_file  = sys.argv[1]
    dat_file  = sys.argv[2]
    plan_file = sys.argv[3]
    out_file  = sys.argv[4]
    nodes, edges = parse_col(col_file)
    start, goal  = parse_dat(dat_file)
    sequence = decode_plan(plan_file, start)
    with open(out_file, "w") as f:
        if sequence is None:
            f.write("NO\n")
        else:
            f.write("YES\n")
            for state in sequence:
                f.write(" ".join(map(str, state)) + "\n")

if __name__ == "__main__":
    main()