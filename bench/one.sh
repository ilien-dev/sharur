#!/bin/bash
# usage: one.sh style promptIdx rep
# Prompts 1-13 run in fixture/, 14 and up in fixture2/. Files in tasks/p<N>/ are added for prompt N.
S="$(cd "$(dirname "$0")" && pwd)"
st=$1; p=$2; r=$3; id="${PFX}${st}_p${p}_r${r}"
[ -s "$S/out/$id.jsonl" ] && exit 0
mkdir -p "$S/out" "$S/runs"; rm -rf "$S/runs/$id"
if [ "$p" -ge 14 ]; then cp -r "$S/fixture2" "$S/runs/$id"; cp -r "$S/fixture/.claude" "$S/runs/$id/.claude"
else cp -r "$S/fixture" "$S/runs/$id"; fi
[ -d "$S/tasks/p$p" ] && cp -r "$S/tasks/p$p/." "$S/runs/$id/"
cd "$S/runs/$id"
prompt=$(sed -n "${p}p" "$S/prompts.txt")
claude -p "$prompt" --output-format stream-json --verbose ${SRC---setting-sources project} \
  --model "${MODEL:-claude-fable-5-2}" --settings "{\"outputStyle\":\"$st\"}" --no-session-persistence \
  --permission-mode acceptEdits --allowedTools "Bash(python:*)" "PowerShell(python:*)" Read Edit Write Grep Glob \
  < /dev/null > "$S/out/$id.jsonl" 2> "$S/out/$id.err"
# Drop runs that hit a usage limit or ended in error, so they are neither cached nor graded.
if ! node "$S/runok.cjs" "$S/out/$id.jsonl"; then
  mv "$S/out/$id.jsonl" "$S/out/$id.failed"; fi
