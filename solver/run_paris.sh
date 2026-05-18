#!/bin/bash

# 1. Chuyển hẳn vào thư mục solver trên Railway
cd /app/solver

# 2. Định nghĩa chính xác file thực thi Fast Downward và tham số truyền vào
FD_PATH="/app/solver/fd/fast-downward.py"
INPUT_SAS=$1
OUTPUT_PLAN=$2

# 3. Chạy bộ giải với cấu hình thuật toán chuẩn của bạn
# (Nếu lệnh gốc của bạn dùng thuật toán khác thuật toán dưới này, hãy đổi lại cho đúng nhé)
python3 $FD_PATH $INPUT_SAS --search "astar(lmcut())"

# 4. Gom file kết quả 'sas_plan' mặc định đổi tên thành file output.plan cho Backend đọc
if [ -f "sas_plan" ]; then
    mv sas_plan $OUTPUT_PLAN
fi