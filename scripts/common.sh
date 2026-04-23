#!/usr/bin/env bash
# Shared helpers for release scripts.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

color() { printf "\033[%sm%s\033[0m\n" "$1" "$2"; }
info()  { color "36" "▶ $*"; }
ok()    { color "32" "✓ $*"; }
warn()  { color "33" "! $*"; }
fail()  { color "31" "✗ $*"; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

pkg_version() {
  node -p "require('$ROOT_DIR/package.json').version"
}

pkg_name() {
  node -p "require('$ROOT_DIR/package.json').name"
}

vsix_path() {
  echo "$ROOT_DIR/$(pkg_name)-$(pkg_version).vsix"
}

ensure_clean_git() {
  if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
    fail "Working tree not clean. Commit or stash changes first."
  fi
}
