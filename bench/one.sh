#!/bin/bash
# usage: one.sh style promptIdx rep
S="$(cd "$(dirname "$0")" && pwd)"
st=$1; p=$2; r=$3; id="${PFX}${st}_p${p}_r${r}"
[ -s "$S/out/$id.jsonl" ] && exit 0
rm -rf "$S/runs/$id"; cp -r "$S/fixture" "$S/runs/$id"; cd "$S/runs/$id"
prompt=$(sed -n "${p}p" "$S/prompts.txt")
claude -p "$prompt" --output-format stream-json --verbose ${SRC---setting-sources project} \
  --model claude-fable-5-2 --settings "{\"outputStyle\":\"$st\"}" --no-session-persistence \
  --permission-mode acceptEdits --allowedTools "Bash(python:*)" "PowerShell(python:*)" Read Edit Write Grep Glob \
  < /dev/null > "$S/out/$id.jsonl" 2> "$S/out/$id.err"
