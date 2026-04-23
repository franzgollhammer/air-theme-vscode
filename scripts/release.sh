#!/usr/bin/env bash
# End-to-end release: bump version, tag, push, package, publish to both registries.
#
# Usage:
#   scripts/release.sh patch   # 1.0.0 -> 1.0.1
#   scripts/release.sh minor   # 1.0.0 -> 1.1.0
#   scripts/release.sh major   # 1.0.0 -> 2.0.0
#   scripts/release.sh 1.2.3   # explicit version
#
# Requires: clean git tree, VSCE_PAT (or prior vsce login), OVSX_PAT.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

require_cmd node
require_cmd npx
require_cmd git

BUMP="${1:-}"
[[ -z "$BUMP" ]] && fail "Usage: $0 <patch|minor|major|X.Y.Z>"

cd "$ROOT_DIR"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  fail "Refusing to release from $BRANCH — create a release branch first"
fi

ensure_clean_git

OLD="$(pkg_version)"
info "current version: $OLD"

# npm version updates package.json without creating a git tag.
NEW_TAG="$(npm version "$BUMP" --no-git-tag-version)"
NEW="${NEW_TAG#v}"
ok "bumped to $NEW"

info "packaging"
bash "$ROOT_DIR/scripts/package.sh"

info "verifying vsix"
bash "$ROOT_DIR/scripts/verify.sh"

info "publishing to both marketplaces"
bash "$ROOT_DIR/scripts/publish-all.sh"

info "committing + tagging"
git add package.json package-lock.json 2>/dev/null || git add package.json
git commit -m "chore(release): v$NEW"
git tag -a "v$NEW" -m "v$NEW"

ok "release v$NEW published"
warn "next: git push origin $BRANCH && git push origin v$NEW"
