
import sys, os

USAGE = "\n\tpython3 decode.py [pddl-single|pddl-split|sas-single|sas-split] <plan file> <instance file>\n"


def answer_line(tokenization):
    return 'a ' + ' '.join(sorted(tokenization))

def go(mode, pfile, ifile):

    SOL = ''

    # Check if the plan exists
    assert os.path.isfile(pfile), "Should only decode if a plan exists"

    with open(ifile, 'r') as f:
        instance = f.read().splitlines()
    assert "s " == instance[0][0:2]
    assert "t " == instance[1][0:2]

    init = instance[0]
    goal = instance[1]

    with open(pfile, 'r') as f:
        plines = f.readlines()

    plines = [x.strip() for x in plines if x[0] != ';']

    SOL += init + '\n'
    SOL += goal + '\n'
    SOL += 'a YES' + '\n'

    state = set(init[2:].split())
    SOL += answer_line(state) + '\n'

    # Check the mode we've solved -- example plans are listed below
    if mode == 'pddl-split':
        ind = 0
        while ind < len(plines):
            src = plines[ind].split('-')[-1].split(')')[0][1:].strip()
            dst = plines[ind+1].split('-')[-1].split(')')[0][1:].strip()
            state.remove(src)
            state.add(dst)
            ind += 2
            SOL += answer_line(state) + '\n'
    elif mode == 'pddl-single':
        for act in plines:
            src = act.split('-')[-2][1:].strip()
            dst = act.split('-')[-1].split(')')[0][1:].strip()
            state.remove(src)
            state.add(dst)
            SOL += answer_line(state) + '\n'
    elif mode == 'sas-single':
        for act in plines:
            act = act[1:-1]
            src = str(int(act.split()[1]) + 1)
            dst = str(int(act.split()[2]) + 1)
            state.remove(src)
            state.add(dst)
            SOL += answer_line(state) + '\n'
    elif mode == 'sas-split':
        ind = 0
        while ind < len(plines):
            src = str(int(plines[ind][1:-1].split()[1]) + 1)
            dst = str(int(plines[ind+1][1:-1].split()[1]) + 1)
            state.remove(src)
            state.add(dst)
            ind += 2
            SOL += answer_line(state) + '\n'
    elif mode == 'pddl-lifted':
        for act in plines:
            act = act[1:-1]
            # (move l3 l1)
            src = act.split()[1][1:]
            dst = act.split()[2][1:]
            state.remove(src)
            state.add(dst)
            SOL += answer_line(state) + '\n'
    else:
        print("\n\tError: Unrecognized mode:", mode)
        exit(1)

    assert(state == set(goal[2:].split()))

    return SOL



if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit(USAGE)

    mode = sys.argv[1]
    plan_file = sys.argv[2]
    instance_file = sys.argv[3]
    solution = go(mode, plan_file, instance_file)
    with open("solution.txt", "w") as f:
        f.write(solution)

