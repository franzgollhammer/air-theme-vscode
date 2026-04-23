#!/usr/bin/env bash
# Publish to the VS Code Marketplace.
# Auth: set VSCE_PAT, or run `npx @vscode/vsce login <publisher>` beforehand.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

require_cmd node
require_cmd npx

cd "$ROOT_DIR"

VERSION="$(pkg_version)"
VSIX="$(vsix_path)"

if [[ ! -f "$VSIX" ]]; then
  info "no vsix at $VSIX — packaging first"
  bash "$ROOT_DIR/scripts/package.sh"
fi

if [[ -z "${VSCE_PAT:-}" ]]; then
  warn "VSCE_PAT not set — vsce will prompt or use stored credentials"
fi

info "publishing v$VERSION to VS Code Marketplace"
npx --yes @vscode/vsce publish --packagePath "$VSIX"

ok "published to VS Code Marketplace"
ok "https://marketplace.visualstudio.com/items?itemName=$(node -p "require('$ROOT_DIR/package.json').publisher").$(pkg_name)"
