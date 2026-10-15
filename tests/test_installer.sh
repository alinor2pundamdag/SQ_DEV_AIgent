#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_HOME=$(mktemp -d)
trap 'rm -rf "$TMP_HOME"' EXIT HUP INT TERM
cp -R "$ROOT" "$TMP_HOME/source"
HOME="$TMP_HOME/home" mkdir -p "$TMP_HOME/home"
HOME="$TMP_HOME/home" sh "$TMP_HOME/source/install.sh" >/dev/null
LAUNCHER="$TMP_HOME/home/.local/bin/ai"
test -x "$LAUNCHER"
rm -rf "$TMP_HOME/source"
OUTPUT=$(HOME="$TMP_HOME/home" PATH="$TMP_HOME/home/.local/bin:$PATH" "$LAUNCHER" systems)
printf '%s\n' "$OUTPUT" | grep -q "AgentCore"
SKILLS=$(HOME="$TMP_HOME/home" PATH="$TMP_HOME/home/.local/bin:$PATH" "$LAUNCHER" skills)
printf '%s\n' "$SKILLS" | grep -q "100 entries"
printf '%s\n' "$SKILLS" | grep -q "validation: PASS"
echo "Installer smoke test passed."
