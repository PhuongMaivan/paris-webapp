import json
import hashlib
from collections import deque

def get_cache_key(nodes, edges, start, goal):
    data = json.dumps({
        "nodes": sorted(nodes),
        "edges": sorted([sorted(e) for e in edges]),
        "start": sorted(start),
        "goal":  sorted(goal)
    }, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

def run_paris(nodes, edges, start, goal, timeout=30):
    """
    Thuật toán tìm kiếm không gian trạng thái (BFS) giải bài toán ISR thuần Python.
    Bypass hoàn toàn Fast Downward để deploy lên Railway Free mượt mà 100%.
    """
    # 1. Chuẩn hóa dữ liệu đầu vào thành tập hợp (set) cố định để tra cứu nhanh
    all_nodes = set(nodes)
    start_state = tuple(sorted(start))
    goal_state = set(goal)
    
    # Xây dựng danh sách kề để kiểm tra mối quan hệ (adj) giữa các đỉnh
    adj = {v: set() for v in all_nodes}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)

    # 2. Thuật toán BFS tìm chuỗi cấu hình ngắn nhất
    # Queue lưu: (trạng thái_hiện_tại, chuỗi_các_trạng_thái_đã_qua)
    queue = deque([(start_state, [list(start_state)])])
    
    # Set đánh dấu các trạng thái đã duyệt qua tránh lặp vô hạn
    visited = {start_state}
    
    import time
    start_time = time.time()

    while queue:
        # Kiểm tra quá thời gian timeout đề phòng đồ thị quá lớn
        if time.time() - start_time > timeout:
            print("DEBUG SOLVER - Timeout reached!")
            return {"reachable": False, "sequence": []}

        curr_state, path = queue.popleft()
        curr_set = set(curr_state)

        # Nếu toàn bộ token đã khớp với mục tiêu (goal) -> Thành công!
        if curr_set == goal_state:
            return {"reachable": True, "sequence": path}

        # Duyệt qua từng token hiện tại để tìm nước đi hợp lệ
        for token_from in curr_state:
            # Token này có thể nhảy đến bất kỳ vị trí trống nào không kề nó
            for token_to in all_nodes:
                # Điều kiện 1 & 2: Vị trí đích phải trống VÀ không được kề trực tiếp với vị trí xuất phát
                if token_to in curr_set or token_to in adj[token_from]:
                    continue
                
                # Điều kiện 3: Vị trí đích không được phép kề với bất kỳ vị trí có token nào khác (trừ chính nó)
                has_neighbor_token = False
                for neighbor in adj[token_to]:
                    if neighbor in curr_set and neighbor != token_from:
                        has_neighbor_token = True
                        break
                
                if has_neighbor_token:
                    continue

                # Tạo trạng thái mới sau khi di chuyển token thành công
                next_set = (curr_set - {token_from}) | {token_to}
                next_state = tuple(sorted(next_set))

                # Nếu trạng thái này chưa từng đi qua, lưu vào queue
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [list(next_state)]
                    queue.append((next_state, new_path))

    # Duyệt hết không gian trạng thái mà không tìm thấy đường đi
    return {"reachable": False, "sequence": []}