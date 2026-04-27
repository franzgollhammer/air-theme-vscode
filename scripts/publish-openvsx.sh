#!/usr/bin/env bash
# Publish to Open VSX (used by Cursor, VSCodium, Gitpod, etc).
# Auth: export OVSX_PAT=<token from https://open-vsx.org/user-settings/tokens>
# Namespace must exist: `npx ovsx create-namespace <publisher> -p $OVSX_PAT`

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

if [[ -z "${OVSX_PAT:-}" ]]; then
  fail "OVSX_PAT not set — get a token from https://open-vsx.org/user-settings/tokens"
fi

info "publishing v$VERSION to Open VSX"
npx --yes ovsx publish "$VSIX" -p "$OVSX_PAT"

ok "published to Open VSX"
ok "https://open-vsx.org/extension/$(node -p "require('$ROOT_DIR/package.json').publisher")/$(pkg_name)"
