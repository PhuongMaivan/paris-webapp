#!/bin/bash

# 1. Đảm bảo script luôn đứng đúng thư mục solver để chạy
cd /app/solver

# 2. Khai báo đường dẫn tuyệt đối đến file thực thi của Fast Downward
FD_PATH="/app/solver/fd/fast-downward.py"

# 3. Lấy tham số đầu vào ($1 là file .sas) và đầu ra ($2 là file .plan) từ main.py truyền sang
INPUT_SAS=$1
OUTPUT_PLAN=$2

# 4. Chạy bộ giải Fast Downward với cấu hình thuật toán của bạn
# (Sửa lại --search ... đúng theo cấu hình giải thuật toán gốc của bạn)
python3 $FD_PATH $INPUT_SAS --search "astar(lmcut())"

# 5. Di chuyển file sas_plan sinh ra mặc định về đúng tên/đường dẫn mà Backend yêu cầu
if [ -f "sas_plan" ]; then
    mv sas_plan $OUTPUT_PLAN
fi