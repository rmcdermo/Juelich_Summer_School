#!/bin/bash
#
# Cut one time step out of each _pressit.csv in results/.
#
#   ./slice_pressit.sh [STEP]
#
# STEP defaults to 2500, the step the slide's figure is drawn from.
#
# The error figure needs one time step. The file it comes from holds every
# pressure iteration of the whole run, which for the plain FFT variant is 2000
# a half step for the length of the run -- on the order of a gigabyte. This
# writes Example_5_<VARIANT>_pressit_step<STEP>.csv beside each one, a few
# hundred kilobytes at most, and that is what to copy back.
#
# `python eval.py slice --step <STEP>` does the same thing and is the version to
# use on a laptop. This one is here for the cluster, where pandas may not be:
# it needs nothing but awk.

set -e
cd "$(dirname "$0")"

STEP="${1:-2500}"

shopt -s nullglob
FILES=(results/*_pressit.csv)
if [ ${#FILES[@]} -eq 0 ]; then
  echo "no results/*_pressit.csv to slice" >&2
  exit 1
fi

for FULL in "${FILES[@]}"; do
  OUT="${FULL%_pressit.csv}_pressit_step${STEP}.csv"
  # Column 2 is "Time Step". NR==1 keeps the header; $2+0 drops the leading
  # blanks FDS pads the field with.
  awk -F, -v s="$STEP" 'NR==1 || $2+0==s' "$FULL" > "$OUT"
  N=$(( $(grep -c "" "$OUT") - 1 ))
  if [ "$N" -le 0 ]; then
    echo "$(basename "$FULL"): no time step $STEP -- run had fewer" >&2
    rm -f "$OUT"
    continue
  fi
  echo "$(basename "$OUT")  ($N rows)"
done
