#!/usr/bin/env bash
# Publish to both registries. Stops on first failure.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

info "publishing to VS Code Marketplace + Open VSX"
bash "$ROOT_DIR/scripts/publish-vscode.sh"
bash "$ROOT_DIR/scripts/publish-openvsx.sh"
ok "done — live on both marketplaces"
