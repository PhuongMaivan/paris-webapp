#!/bin/bash
COL=$1
DAT=$2
OUT=$3

# Lấy đường dẫn của chính thư mục chứa file solve.sh này (tự động đúng ở cả local và Railway)
SOLVER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FD="$SOLVER_DIR/fd/fast-downward.py"
DOMAIN_FIXED="$SOLVER_DIR/domain.pddl"

TMPDIR="/tmp/paris_$$"
mkdir -p "$TMPDIR"

# 1. Chạy parser để tạo problem.pddl
python3 "$SOLVER_DIR/my_parser.py" "$COL" "$DAT" "$TMPDIR"

# 2. Chạy Fast Downward 
python3 "$FD" \
  --plan-file "$TMPDIR/output.plan" \
  "$DOMAIN_FIXED" \
  "$TMPDIR/problem.pddl" \
  --search "astar(blind())"

# 3. Decode kết quả
python3 "$SOLVER_DIR/my_decode.py" "$COL" "$DAT" "$TMPDIR/output.plan" "$OUT"

rm -rf "$TMPDIR"

: '#!/bin/bash
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

