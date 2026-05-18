import sys

def parse_col(col_file):
    nodes_set = set()
    edges = []
    num_nodes_expected = 0
    
    with open(col_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            if line.startswith("p edge"):
                num_nodes_expected = int(line.split()[2])
                for i in range(num_nodes_expected):
                    nodes_set.add(i)
                    
            elif line.startswith("e "):
                parts = line.split()
                u, v = int(parts[1]), int(parts[2])
                edges.append((u, v))
                nodes_set.add(u)
                nodes_set.add(v)
                
    return sorted(list(nodes_set)), edges

def parse_dat(dat_file):
    with open(dat_file) as f:
        lines = [l.strip() for l in f if l.strip()]
    start = list(map(int, lines[0].split()))
    goal  = list(map(int, lines[1].split()))
    return start, goal

def gen_pddl(nodes, edges, start, goal):
    node_objs = " ".join([f"l{v}" for v in nodes])
    init_adj = []
    for a, b in edges:
        init_adj.append(f"(adj l{a} l{b})")
        init_adj.append(f"(adj l{b} l{a})")

    domain = """(define (domain isr)
  (:requirements :typing :negative-preconditions :equality)
  (:types loc)
  (:predicates 
    (free ?l - loc) 
    (tokened ?l - loc) 
    (adj ?l1 ?l2 - loc)
  )
  (:action jump
    :parameters (?from - loc ?to - loc)
    :precondition (and 
        (tokened ?from) 
        (free ?to)
        (not (adj ?from ?to))
        (not (exists (?n - loc) 
            (and (adj ?to ?n) (tokened ?n) (not (= ?n ?from)))
        ))
    )
    :effect (and 
        (not (tokened ?from)) (free ?from) 
        (tokened ?to) (not (free ?to))
    )
  )
)"""

    init_states = []
    for v in nodes:
        if v in start:
            init_states.append(f"(tokened l{v})")
        else:
            init_states.append(f"(free l{v})")
    
    goal_str = " ".join(f"(tokened l{v})" for v in goal)

    problem = f"""(define (problem isr-instance)
  (:domain isr)
  (:objects {node_objs} - loc)
  (:init {" ".join(init_states)} {" ".join(init_adj)})
  (:goal (and {goal_str}))
)"""
    return domain, problem

def main():
    col_file = sys.argv[1]
    dat_file = sys.argv[2]
    out_dir  = sys.argv[3] if len(sys.argv) > 3 else "/tmp"
    nodes, edges = parse_col(col_file)
    start, goal  = parse_dat(dat_file)

    domain, problem = gen_pddl(nodes, edges, start, goal)
    with open(f"{out_dir}/problem.pddl", "w", newline='\n') as f:
        f.write(problem)

if __name__ == "__main__":
    main()