#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SHARE_DIR="${HOME}/.local/share/sq-dev-aigent"
APP_DIR="$SHARE_DIR/app"
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$APP_DIR" "$BIN_DIR" "$SHARE_DIR"
# Copy to a stable per-user location so the global command survives moving the checkout.
rm -rf "$APP_DIR/sq_dev_aigent"
cp -R "$ROOT/sq_dev_aigent" "$APP_DIR/sq_dev_aigent"
mkdir -p "$APP_DIR/skills"
cp "$ROOT/skills/catalog.json" "$APP_DIR/skills/catalog.json"
LAUNCHER="$BIN_DIR/ai"
cat > "$LAUNCHER" <<EOF
#!/bin/sh
APP_DIR="$APP_DIR"
export PYTHONPATH="$APP_DIR\${PYTHONPATH:+:\$PYTHONPATH}"
exec python -m sq_dev_aigent.cli "\$@"
EOF
chmod 755 "$LAUNCHER"
echo "Installed shared application: $APP_DIR"
echo "Installed global launcher: $LAUNCHER"
case ":$PATH:" in
  *":$BIN_DIR:"*) echo "$BIN_DIR is already on PATH." ;;
  *) echo "Add this to your shell profile: export PATH=\"$BIN_DIR:\$PATH\"" ;;
esac
echo "No models or dependencies were downloaded."
echo "Next: ai doctor && ai systems && ai skills"
