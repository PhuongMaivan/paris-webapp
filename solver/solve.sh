:'
#!/bin/bash
COL=$1
DAT=$2
OUT=$3

SOLVER_DIR="/mnt/c/paris-webapp/solver"
FD="$SOLVER_DIR/fd/fast-downward.py"
# Dùng đường dẫn cố định cho domain nếu parser không tự sinh ra nó vào TMPDIR
DOMAIN_FIXED="/mnt/c/paris-webapp/solver/domain.pddl"

TMPDIR="/tmp/paris_$$"
mkdir -p "$TMPDIR"

# 1. Chạy parser để tạo problem.pddl (và domain.pddl nếu bạn dùng parser sinh cả hai)
python3 "$SOLVER_DIR/my_parser.py" "$COL" "$DAT" "$TMPDIR"

# 2. Chạy Fast Downward (Dùng đường dẫn tuyệt đối cho chắc chắn)
python3 "$FD" \
  --plan-file "$TMPDIR/output.plan" \
  "/mnt/c/paris-webapp/solver/domain.pddl" \
  "$TMPDIR/problem.pddl" \
  --search "astar(blind())"

# 3. Decode kết quả
python3 "$SOLVER_DIR/my_decode.py" "$COL" "$DAT" "$TMPDIR/output.plan" "$OUT"

rm -rf "$TMPDIR"  '


#!/usr/bin/bash
COL=$1
DAT=$2
OUT=$3

FD="./fd/fast-downward.py"
DOMAIN="./domain.pddl"
TMPDIR="/tmp/paris_$$"
mkdir -p "$TMPDIR"

# ==== DÒNG QUAN TRỌNG NHẤT: Ép hệ thống nhảy vào đúng thư mục solver ====
cd "$(dirname "$0")"
# =======================================================================

# 1. Chạy parser tạo problem.pddl vào TMPDIR
python3 my_parser.py "$COL" "$DAT" "$TMPDIR"

# 2. Dịch PDDL sang SAS (Gọi trực tiếp file fast-downward.py bằng python3)
python3 ./fd/fast-downward.py --translate --plan-file "$TMPDIR/output.plan" "$DOMAIN" "$TMPDIR/problem.pddl"

# 3. Giải file SAS
bash ./run_paris.sh output.sas "$TMPDIR/output.plan"

# 4. Decode kết quả
python3 my_decode.py "$COL" "$DAT" "$TMPDIR/output.plan" "$OUT"

# Dọn dẹp
rm -rf "$TMPDIR" output.sas