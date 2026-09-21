#!/bin/bash
#
# Run all three variants of Example 5, one after another.
#
#   ./run_all.sh
#
# One at a time on purpose. Two of the three figures are cost comparisons
# between solvers, and jobs sharing cores would show up in them as solver cost.
# Eight ranks per run, so a machine with eight free cores can do this unattended
# -- budget a few hours, most of it the plain FFT run.
#
# On a cluster with a batch system use submit.sh instead.

set -e
cd "$(dirname "$0")"

for VARIANT in FFT_TP UGLMAT FFT; do
  echo "=== $VARIANT"
  ./run.sh "$VARIANT"
done

echo
echo "all three done; plot them with: python eval.py all"
