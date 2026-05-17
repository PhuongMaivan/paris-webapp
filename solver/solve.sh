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

# Nhận 3 tham số truyền vào từ Python
COL_FILE=$1
DAT_FILE=$2
OUT_FILE=$3

# Tự động xác định thư mục chứa file solve.sh này (Thư mục solver gốc)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Định nghĩa đường dẫn tuyệt đối tới các file parser và bộ dịch
PARSER_PY="$SCRIPT_DIR/my_parser.py"
DECODER_PY="$SCRIPT_DIR/my_decode.py"
FD_PY="$SCRIPT_DIR/fd/fast-downward.py"

# Tạo một thư mục tạm biệt lập cho phiên chạy này bên trong /tmp
TMP_DIR=$(mktemp -d)

# 1. Chạy parser để dịch file .col và .dat thành problem.pddl
python3 "$PARSER_PY" "$COL_FILE" "$DAT_FILE" "$TMP_DIR"

# 2. Kiểm tra xem file problem.pddl có được sinh ra thành công không
if [ ! -f "$TMP_DIR/problem.pddl" ]; then
    echo "NO" > "$OUT_FILE"
    echo "ERROR: my_parser.py failed to generate problem.pddl" >> "$OUT_FILE"
    rm -rf "$TMP_DIR"
    exit 0
fi

# 3. Kích hoạt bộ giải Fast Downward bằng đường dẫn tuyệt đối ổn định
# Sử dụng cấu hình cấu trúc trạng thái cơ bản (Astar + Landmark Count) gọn nhẹ cho Render Free Tier
python3 "$FD_PY" --translate --plan-file "$TMP_DIR/output.plan" "$SCRIPT_DIR/domain.pddl" "$TMP_DIR/problem.pddl" > /dev/null 2>&1
python3 "$FD_PY" --search-memory-limit 250M --search "astar(lmcount(lm_merged([lm_rhw(),lm_hm()]),admissible=true),pref=[])" --plan-file "$TMP_DIR/output.plan" "$TMP_DIR/output.sas" > /dev/null 2>&1

# 4. Kiểm tra xem bộ giải tìm ra phương án (plan) hay không
if [ -f "$TMP_DIR/output.plan" ]; then
    # Nếu có plan, chạy bộ giải mã decode dịch sang chuỗi trạng thái số nguyên
    python3 "$DECODER_PY" "$COL_FILE" "$DAT_FILE" "$TMP_DIR/output.plan" "$OUT_FILE"
else
    # Nếu vô nghiệm hoặc bộ giải bị crash ngầm, ghi chữ NO để hệ thống nhận diện sạch
    echo "NO" > "$OUT_FILE"
fi

# 5. Dọn dẹp sạch sẽ tài nguyên rác trong bộ nhớ tạm /tmp
rm -rf "$TMP_DIR"