export const EXAMPLES = [
  {
    id: "ex1", label: "Path P5 — reachable",
    nodes: [0,1,2,3,4],
    edges: [[0,1],[1,2],[2,3],[3,4]],
    start: [0,2,4], goal: [1,3],
    reachable: true,
    sequence: [
      [0,2,4],[0,2,3],[0,1,3],[0,1,4],[2,1,4],[2,3,4]
    ],
  },
  {
    id: "ex2", label: "Triangle K3 — unreachable",
    nodes: [0,1,2],
    edges: [[0,1],[1,2],[0,2]],
    start: [0], goal: [1],
    reachable: false,
    sequence: [],
  },
  {
    id: "ex3", label: "Cycle C6 — reachable",
    nodes: [0,1,2,3,4,5],
    edges: [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],
    start: [0,2,4], goal: [1,3,5],
    reachable: true,
    sequence: [
      [0,2,4],[0,2,5],[0,3,5],[1,3,5]
    ],
  },
];

const DEFAULT_POSITIONS = {
  0: {x:220, y:80},
  1: {x:360, y:80},
  2: {x:220, y:200},
  3: {x:360, y:200},
  4: {x:290, y:300},
  5: {x:150, y:200},
};
