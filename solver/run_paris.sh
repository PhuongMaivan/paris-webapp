#!/usr/bin/bash

# Cách dùng: ./run_paris.sh input.sas output.plan
SAS_FILE=$1
PLAN_FILE=$2

# Sửa lại đường dẫn gọi sang thư mục fd nằm cùng cấp với file .sh này
python3 ./fd/fast-downward.py \
  --plan-file "$PLAN_FILE" "$SAS_FILE" \
  --landmarks lmg="lm_hm(use_orders=False, m=1)" \
  --evaluator "hlm=lmcount(lmg, admissible=True, pref=false)" \
  --search "eager(single(hlm),reopen_closed=False)"