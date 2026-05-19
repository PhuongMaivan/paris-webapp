export const EXAMPLES = [
  {
    id: "ex1",
    label: "Path P3 — Easy Test (YES)",
    nodes: [0, 1, 2],
    edges: [[0, 1], [1, 2]],
    start: [0],      
    goal:  [2],      
    // Giải thích: Token nhảy từ 0 sang 2 (vì 0 và 2 không kề nhau). 
    // Kết quả: YES.
  },
  {
    id: "ex2",
    label: "Triangle K3 — Unreachable (NO)",
    nodes: [0, 1, 2],
    edges: [[0, 1], [1, 2], [0, 2]],
    start: [0],
    goal:  [1],
    // Giải thích: Trong tam giác, mọi đỉnh đều kề nhau. 
    // Token ở 0 không thể nhảy đi đâu cả (vì nhảy đến đâu cũng bị kề với chính nó).
    // Kết quả: NO.
  },
  {
    id: "ex3",
    label: "Path P5 — Complex Reachable (YES)",
    nodes: [0, 1, 2, 3, 4],
    edges: [[0, 1], [1, 2], [2, 3], [3, 4]],
    start: [0, 4],
    goal:  [2, 4],
    // Giải thích: Di chuyển token từ 0 sang 2. Đỉnh 2 không kề 0 và không kề 4.
    // Kết quả: YES.
  },
  {
    id: "ex4",
    label: "Star Graph — Reachable (YES)",
    nodes: [0, 1, 2, 3],
    edges: [[0, 1], [0, 2], [0, 3]],
    start: [1],
    goal:  [3],
    // Giải thích: Đỉnh trung tâm là 0. Nhảy từ cánh 1 sang cánh 3 (1 và 3 không kề nhau, không kề token nào).
    // Kết quả: YES.
  },
  {
    id: "ex5",
    label: "Cycle C4 — Opposite Switch (YES)",
    nodes: [0, 1, 2, 3],
    edges: [[0, 1], [1, 2], [2, 3], [3, 0]],
    start: [0],
    goal:  [2],
    // Giải thích: Đồ thị vòng gồm 4 đỉnh. Token ở 0 nhảy sang đỉnh đối diện là 2 thành công.
    // Kết quả: YES.
  },
  {
    id: "ex6",
    label: "Cycle C4 — Two Tokens Blocked (NO)",
    nodes: [0, 1, 2, 3],
    edges: [[0, 1], [1, 2], [2, 3], [3, 0]],
    start: [0, 2],
    goal:  [1, 3],
    // Giải thích: Có 2 token nằm đối diện nhau (0 và 2). Bất kỳ nước đi nào của một trong hai token 
    // sang 1 hoặc 3 đều sẽ vi phạm luật vì đỉnh đích kề với token còn lại. Hệ thống bị kẹt cứng (Deadlock).
    // Kết quả: NO.
  },
  {
    id: "ex7",
    label: "Bipartite K2,2 — Strict Deadlock (NO)",
    nodes: [0, 1, 2, 3],
    edges: [[0, 2], [0, 3], [1, 2], [1, 3]],
    start: [0, 1],
    goal:  [2, 3],
    // Giải thích: Hai tập độc lập {0,1} và {2,3} kề nhau hoàn toàn. 
    // Do tất cả các đỉnh trống đều kề với vị trí hiện tại của token, không có token nào có thể di chuyển.
    // Kết quả: NO.
  },
  {
    id: "ex8",
    label: "Long Path P6 — Step by Step (YES)",
    nodes: [0, 1, 2, 3, 4, 5],
    edges: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]],
    start: [0, 5],
    goal:  [3, 5],
    // Giải thích: Bài toán chuỗi dài 6 đỉnh với 2 token ở hai đầu (0 và 5). 
    // Token ở 0 dịch dần qua các vị trí trung gian không kề (0 -> 2 -> 4 rồi lùi về 3).
    // Kết quả: YES.
  }
];