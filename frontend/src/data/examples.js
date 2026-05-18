export const EXAMPLES = [
  {
    id: "ex1",
    label: "Path P3 — Easy Test",
    nodes: [0, 1, 2],
    edges: [[0, 1], [1, 2]],
    start: [0],      
    goal:  [2],      
    // Giải thích: Token nhảy từ 0 sang 2 (vì 0 và 2 không kề nhau). 
    // Kết quả: YES.
  },
  {
    id: "ex2",
    label: "Triangle K3 — Unreachable",
    nodes: [0, 1, 2],
    edges: [[0, 1], [1, 2], [0, 2]],
    start: [0],
    goal:  [1],
    // Giải thích: Trong tam giác, mọi đỉnh đều kề nhau. 
    // Token ở 0 không thể nhảy đi đâu cả (vì nhảy đến đâu cũng bị kề).
    // Kết quả: NO.
  },
  {
    id: "ex3",
    label: "Path P5 — Complex Reachable",
    nodes: [0, 1, 2, 3, 4],
    edges: [[0, 1], [1, 2], [2, 3], [3, 4]],
    start: [0, 4],
    goal:  [2, 4],
    // Giải thích: Di chuyển token từ 0 sang 2. 2 không kề 0 và không kề 4.
    // Kết quả: YES.
  },
  {
    id: "ex4",
    label: "Star Graph — Reachable",
    nodes: [0, 1, 2, 3],
    edges: [[0, 1], [0, 2], [0, 3]],
    start: [1],
    goal:  [3],
    // Giải thích: Nhảy từ cánh này sang cánh kia của ngôi sao.
    // Kết quả: YES.
  }
];