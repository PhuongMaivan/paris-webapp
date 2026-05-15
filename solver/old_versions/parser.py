#! /usr/bin/env python

import subprocess
import sys

from lab.parser import Parser


VALIDATOR = "../../validator.py"


def print_error(msg):
    print(msg, file=sys.stderr)


def parse_solution(content, props):
    # For unsolvable tasks, froleyks-longest writes the solution to a file instead of to stdout.
    try:
        with open("problem._long.out", "rt") as f:
            content = f.read()
    except FileNotFoundError:
        pass

    ### Not really. We ignore unsolvability as it does not matter for the final score anyway.
    # For unsolvable tasks, paris-longest writes "c UNKNOWN" to stdout.
    #if ("Command being timed: \"python3 /2022solver/run.py submission sas split" in content
    #    and "c UNKNOWN\n" in content and "Exit status: 0" in content):
    #    content = "a NO"

    try:
        with open("problem._long.out", "rt") as f:
            content = f.read()
    except FileNotFoundError:
        pass

    solution_lines = []
    props["unknown"] = 0
    for line in content.splitlines(keepends=True):
        if line.startswith(("a ", "s ", "t ")):
            solution_lines.append(line)
        elif "c UNKNOWN" in line:
            props["unknown"] = 1

    normalized_solution_lines = set(line.strip().lower() for line in solution_lines)
    solved = int("a yes" in normalized_solution_lines)
    unsolvable = int("a no" in normalized_solution_lines)
    answer_lines = int("a " in normalized_solution_lines)

    if solution_lines and answer_lines > 0:
        with open("solution.txt", "w") as f:
            f.writelines(solution_lines)

        # Validate solution.
        p = subprocess.run(
            [sys.executable, VALIDATOR, "graph.col", "problem.dat", "solution.txt"],
            check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if p.returncode == 0:
            print(f"Validation succeeded:\n{p.stdout}")
            if ("[Code01] (Answer: YES) Validation success without any warning" in p.stdout or
                "[Code02] (Answer: YES) Validation success, but there is some warning" in p.stdout) and not solved:
                print_error("solver says it found no solution, but validator claims success")
                solved = 1
            elif "[Code00] (Answer: NO) Validation success" in p.stdout and solved:
                print_error("solver says it found a solution, but passes NO to validator")
                solved = 0
        else:
            print_error(f"Validation failed: {p.stdout}")
            solved = 0
            unsolvable = 0

    props["solved"] = solved
    props["unsolvable"] = unsolvable
    props["coverage"] = solved or unsolvable
    if solved:
        props["steps"] = len([line for line in solution_lines if line.startswith("a ")]) - 1


def set_outcome(content, props):
    lines = content.splitlines()
    solved = props["solved"]
    unsolvable = props["unsolvable"]
    unknown = props["unknown"]
    out_of_time = int("TIMEOUT=true" in lines)
    out_of_memory = int("MEMOUT=true" in lines)

    # the planner an out of memory itself, without being killed by
    # runsolver, and thus runsolver doesn't record an out of memory.
    #if out_of_memory == 0 and props.get("planner_exit_code") == 22:
    #    out_of_memory = 1

    # Check that runsolver doesn't miss a timeout.
    if (
        not solved
        and not unsolvable
        and not out_of_time
        and not out_of_memory
        and props["runtime"] > props["time_limit"]
    ):
        out_of_time = 1
    # In cases where CPU time is very slightly above the threshold so that
    # runsolver didn't kill the planner yet and the planner solved a task
    # just within the limit, runsolver will still record an "out of time".
    # We remove this record. This case also applies to iterative planners.
    # If such planners solve the task, we don't treat them as running out
    # of time.
    if (solved or unsolvable) and (out_of_time or out_of_memory):
        #print_error("task solved however runsolver recorded an out_of_*")
        #print_error(props)
        out_of_time = 0
        out_of_memory = 0

    if not solved and not unsolvable and not unknown:
        props["runtime"] = None

    props["out_of_time"] = out_of_time
    props["out_of_memory"] = out_of_memory

    if solved ^ unsolvable ^ out_of_time ^ out_of_memory ^ unknown:
        if solved:
            props["error"] = "solved"
        elif unsolvable:
            props["error"] = "unsolvable"
        elif out_of_time:
            props["error"] = "out-of-time"
        elif out_of_memory:
            props["error"] = "out-of-memory"
        elif unknown:
            props["error"] = "unknown"
    else:
        print(f"unexpected error: {props}", file=sys.stderr)
        props["error"] = "unexpected-error"


def main():
    print("Running custom parser")
    parser = Parser()
    parser.add_pattern(
        "node", r"node: (.+)\n", type=str, file="driver.log", required=True
    )
    parser.add_pattern(
        "time_limit",
        r"Enforcing CPUTime limit \(soft limit, will send "
        r"SIGTERM then SIGKILL\): (\d+) seconds",
        type=int,
        file="run.log",
        required=True,
    )
    parser.add_pattern(
        "exit_code", r"EXITSTATUS=(.+)\n", type=int, file="values.txt", required=True)
    parser.add_pattern(
        "wall_clock_time", r"WCTIME=(.+)\n", type=float, file="values.txt", required=True)
    # Cumulative runtime and virtual memory of the solver and all child processes.
    parser.add_pattern(
        "runtime", r"WCTIME=(.+)\n", type=float, file="values.txt", required=True)
    parser.add_pattern(
        "virtual_memory", r"MAXVM=(\d+)\n", type=int, file="values.txt", required=True)
    parser.add_pattern("raw_memory", r"Peak memory: (\d+) KB", type=int)
    parser.add_pattern("total_time", r"Total time: (.+)s", type=float)
    parser.add_pattern("expansions", r"Expanded: (\d+) state\(s\).", type=int)
    parser.add_pattern("expansions_until_last_jump", r"Expanded until last jump: (\d+) state\(s\).", type=int)
    parser.add_function(parse_solution, file="solver.log")
    parser.add_function(set_outcome, file="values.txt")
    parser.parse()


if __name__ == "__main__":
    main()
