#!/usr/bin/env bash
# Pre-release checks: print vsix file listing, confirm core assets, no junk.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

require_cmd node
require_cmd npx
require_cmd unzip

cd "$ROOT_DIR"

info "listing files that would be packaged"
npx --yes @vscode/vsce ls

VSIX="$(vsix_path)"
if [[ ! -f "$VSIX" ]]; then
  warn "no vsix found at $VSIX — run scripts/package.sh first"
  exit 0
fi

info "inspecting $VSIX"
CONTENTS="$(unzip -Z1 "$VSIX")"

EXPECTED=(
  "extension/package.json"
  "extension/themes/air-dark-color-theme.json"
  "extension/themes/air-light-color-theme.json"
  "extension/air-theme.png"
  "extension/README.md"
  "extension/LICENSE.md"
  "extension/CHANGELOG.md"
)

# vsce lowercases README/CHANGELOG/LICENSE; accept either form.
normalize() { echo "$1" | tr '[:upper:]' '[:lower:]'; }
NORMALIZED="$(echo "$CONTENTS" | tr '[:upper:]' '[:lower:]')"

for f in "${EXPECTED[@]}"; do
  if echo "$NORMALIZED" | grep -q "$(normalize "$f")"; then
    ok "contains $f"
  else
    warn "missing $f"
  fi
done

BLOCKED=(
  "extension/air-theme.svg"
  "extension/air-theme-512.png"
  "extension/.claude"
  "extension/.worktrees"
  "extension/scripts"
  "extension/node_modules"
  "extension/.vsix"
)

for f in "${BLOCKED[@]}"; do
  if echo "$NORMALIZED" | grep -q "$(normalize "$f")"; then
    fail "vsix contains forbidden path: $f"
  fi
done

THEME_COUNT=$(echo "$CONTENTS" | grep -c '^extension/themes/.*\.json$' || true)
ok "theme files: $THEME_COUNT"
ok "total files: $(echo "$CONTENTS" | wc -l | tr -d ' ')"
