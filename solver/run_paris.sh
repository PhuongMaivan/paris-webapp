#!/usr/bin/bash

# Nhận 3 tham số truyền từ solver.py sang
COL_FILE=$1
DAT_FILE=$2
OUT_FILE=$3

# Lấy thư mục chứa chính file solve.sh này (/app/solver trên Railway)
SOLVER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 1. Chạy parser của bác để chuyển đổi file .col và .dat thành file PDDL hoặc SAS bài toán
# (Đoạn này bác kiểm tra lại xem ở local file my_parser.py nhận tham số thế nào nhé)
python3 "$SOLVER_DIR/my_parser.py" "$COL_FILE" "$DAT_FILE"

# 2. Gọi bộ giải Fast Downward bằng đường dẫn tương đối chuẩn Docker
# Thêm toán tử > /dev/null hoặc xử lý lỗi nếu cần để tránh làm treo luồng
python3 "$SOLVER_DIR/fd/fast-downward.py" \
  --plan-file "$SOLVER_DIR/output.plan" "$SOLVER_DIR/output.sas" \
  --landmarks lmg="lm_hm(use_orders=False, m=1)" \
  --evaluator "hlm=lmcount(lmg, admissible=True, pref=false)" \
  --search "eager(single(hlm),reopen_closed=False)"

# 3. Chạy bộ decode của bác để chuyển đổi file kết quả output.plan thành file kết quả .out cuối cùng
python3 "$SOLVER_DIR/my_decode.py" "$SOLVER_DIR/output.plan" "$OUT_FILE"