#!/bin/bash
# run_checks.sh <set> <toolset dir> <OMI_ROOT>: dofcheck_tee, allcfg (tee + straight), vbacheck on the NEW outputs of regen/<set>, regress old -> new
set -u; A=$(cd "$(dirname "$0")/.." && pwd); S=$1; T=$2; R=$3; N=$A/regen/$S/new; OL=$A/regen/$S/old; C=$A/checks/$S; mkdir -p $C
TEE=$(grep gen_tee] $A/regen/$S/cmp.txt | grep -v 'rc 1/1' | awk '{print $1}')   # rc 1/1: no SPEC for the root (old and new alike)
STR=$(grep gen_straight2] $A/regen/$S/cmp.txt | awk '{print $1}')
python3 -I -B $T/checks/dofcheck_tee.py $(for r in $TEE; do ls $N/$r/Build_*_MASTER.bas 2>/dev/null; done) > $C/dofcheck_tee.txt 2>&1
OMI_ROOT=$R GT_OUT=$C/scratch GS_OUT=$C/scratch python3 -I -B $T/checks/allcfg_check.py t $TEE > $C/allcfg_tee.txt 2>&1
OMI_ROOT=$R GT_OUT=$C/scratch GS_OUT=$C/scratch python3 -I -B $T/checks/allcfg_check.py s $STR > $C/allcfg_straight.txt 2>&1
python3 -I -B $T/checks/vbacheck.py $N/*/Build_*_MASTER.bas > $C/vbacheck.txt 2>&1
: > $C/regress.txt; for r in $TEE $STR; do python3 -I -B $T/checks/regress.py $OL/$r $N/$r $r >> $C/regress.txt 2>&1; done
