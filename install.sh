#!/usr/bin/env bash
# dot-init-agents installer: links CLI tools into ~/.local/bin
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${BIN_DIR}"
chmod +x "${SCRIPT_DIR}"/bin/*
chmod +x "${SCRIPT_DIR}"/dotagents/*.py

ln -sf "${SCRIPT_DIR}/bin/dotagents-init" "${BIN_DIR}/dotagents-init"
ln -sf "${SCRIPT_DIR}/bin/dotagents-adr" "${BIN_DIR}/dotagents-adr"
ln -sf "${SCRIPT_DIR}/bin/dotagents-lint" "${BIN_DIR}/dotagents-lint"

echo "[✓] dot-init-agents installed successfully into ${BIN_DIR}:"
echo "    - dotagents-init"
echo "    - dotagents-adr"
echo "    - dotagents-lint"
echo ""
echo "Ensure ${BIN_DIR} is in your PATH. Run 'dotagents-init --help' to get started."
