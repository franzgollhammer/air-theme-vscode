#!/usr/bin/env bash
# Build .vsix from current working tree.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

require_cmd node
require_cmd npx
require_cmd python3

cd "$ROOT_DIR"

info "regenerating theme variants"
python3 scripts/make-light.py
python3 scripts/make-italic.py

VERSION="$(pkg_version)"
OUT="$(vsix_path)"

info "packaging $(pkg_name) v$VERSION"
rm -f "$OUT"
npx --yes @vscode/vsce package --out "$OUT"

ok "built $OUT ($(du -h "$OUT" | cut -f1))"
