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
#!/bin/bash
# Tự động nhảy vào thư mục chứa script này
cd "$(dirname "$0")"

COL=$1
DAT=$2
OUT=$3

# Đường dẫn tương đối (Làm việc được cả Windows và Linux)
FD="./fd/fast-downward.py"
DOMAIN="./domain.pddl"
TMPDIR="/tmp/paris_$$"
mkdir -p "$TMPDIR"

# 1. Chạy parser tạo problem.pddl vào TMPDIR
python3 my_parser.py "$COL" "$DAT" "$TMPDIR"

# 2. Dịch PDDL sang SAS (Đây là bước tạo file SAS đề tài yêu cầu)
python3 "$FD" --translate --plan-file "$TMPDIR/output.plan" "$DOMAIN" "$TMPDIR/problem.pddl"
# Sau bước này sẽ sinh ra file 'output.sas' ở thư mục hiện tại

# 3. Gọi run_paris.sh để giải file SAS bằng Landmarks
bash ./run_paris.sh output.sas "$TMPDIR/output.plan"

# 4. Decode kết quả
python3 my_decode.py "$COL" "$DAT" "$TMPDIR/output.plan" "$OUT"

# Dọn dẹp
rm -rf "$TMPDIR" output.sas