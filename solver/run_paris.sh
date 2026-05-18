#!/bin/bash
cd /app/solver
FD_PATH="/app/solver/fd/fast-downward.py"
INPUT_SAS=$1
OUTPUT_PLAN=$2

# Chạy Fast Downward
python3 $FD_PATH $INPUT_SAS --search "astar(lmcut())"

if [ -f "sas_plan" ]; then
    mv sas_plan $OUTPUT_PLAN
fi