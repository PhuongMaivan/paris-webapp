#!/usr/bin/bash
DOMAIN=$1
PROBLEM=$2
PLAN=$3

python3 /mnt/c/paris-webapp/solver/fd/builds/release/bin/translate/translate.py $DOMAIN $PROBLEM --sas-file temp.sas
./run_paris.sh temp.sas $PLAN
