:'
#!/usr/bin/bash

# Cách dùng: ./run_paris.sh input.sas output.plan
SAS_FILE=$1
PLAN_FILE=$2

python3 /mnt/c/paris-webapp/solver/fd/fast-downward.py \
  --plan-file $PLAN_FILE $SAS_FILE \
  --landmarks lmg="lm_hm(use_orders=False, m=1)" \
  --evaluator "hlm=lmcount(lmg, admissible=True, pref=false)" \
  --search "eager(single(hlm),reopen_closed=False)"   '

#!/usr/bin/bash
SAS_FILE=$1
PLAN_FILE=$2

cd "$(dirname "$0")"

# Ép chạy trực tiếp file script bằng python3 của hệ thống Render
python3 ./fd/fast-downward.py \
  --plan-file "$PLAN_FILE" "$SAS_FILE" \
  --landmarks lmg="lm_hm(use_orders=False, m=1)" \
  --evaluator "hlm=lmcount(lmg, admissible=True, pref=false)" \
  --search "eager(single(hlm),reopen_closed=False)"
