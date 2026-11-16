#!/bin/bash
# usage: mkstyle.sh name "body" [keep=true]
S="$(cd "$(dirname "$0")" && pwd)"
printf -- '---\nname: %s\ndescription: %s\nkeep-coding-instructions: %s\n---\n\n%s\n' "$1" "$1" "${3:-true}" "$2" > "$S/fixture/.claude/output-styles/$1.md"
