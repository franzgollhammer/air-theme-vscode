#!/usr/bin/env bash
# Package and install into VS Code (or Cursor via --cursor).

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

TARGET="${1:-code}"
case "$TARGET" in
  code|code-insiders|cursor) ;;
  *) fail "Unknown target: $TARGET (expected code|code-insiders|cursor)" ;;
esac

require_cmd "$TARGET"

bash "$ROOT_DIR/scripts/package.sh"

VSIX="$(vsix_path)"
info "installing $VSIX into $TARGET"
"$TARGET" --install-extension "$VSIX" --force
ok "installed into $TARGET"
