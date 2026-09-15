#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/vidclip"
VENV_DIR="$INSTALL_ROOT/venv"
BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python 3.10+ is required. Install Python and re-run ./install.sh"
  exit 1
fi

"$PYTHON" - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY

echo "Installing vidclip..."
mkdir -p "$INSTALL_ROOT" "$BIN_DIR"
"$PYTHON" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install -U pip
"$VENV_DIR/bin/python" -m pip install --upgrade "$REPO_ROOT"

cat > "$BIN_DIR/vidclip" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/vidclip" "\$@"
EOF
chmod +x "$BIN_DIR/vidclip"

echo
echo "Installed. If 'vidclip' is not found, add $BIN_DIR to PATH, then run:"
echo "  vidclip doctor"
echo "  vidclip"
echo "  vidclip \"https://www.youtube.com/watch?v=VIDEO_ID\""
