#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/ai"
cat > "$LAUNCHER" <<EOF
#!/bin/sh
PYTHONPATH="$ROOT${PYTHONPATH:+:\$PYTHONPATH}" exec python -m sq_dev_aigent.cli "\$@"
EOF
chmod 755 "$LAUNCHER"
echo "Installed launcher: $LAUNCHER"
case ":$PATH:" in
  *":$BIN_DIR:"*) echo "$BIN_DIR is already on PATH." ;;
  *) echo "Add this to your shell profile: export PATH=\"$BIN_DIR:\$PATH\"" ;;
esac
echo "No models or dependencies were downloaded."
echo "Next: ai doctor"
