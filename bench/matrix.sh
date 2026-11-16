#!/bin/bash
# usage: PROMPTS="1 2" matrix.sh reps style...
S="$(cd "$(dirname "$0")" && pwd)"; reps=$1; shift
for st in "$@"; do for p in ${PROMPTS:-1 2 3 4 5 6 9 10 11}; do for r in $(seq 1 $reps); do echo "$st $p $r"; done; done; done | xargs -P 10 -L 1 bash "$S/one.sh"
