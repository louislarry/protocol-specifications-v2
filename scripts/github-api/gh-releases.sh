#!/usr/bin/env bash
# List or view releases via gh.
# Usage:
#   ./gh-releases.sh list
#   ./gh-releases.sh view <tag>
#   ./gh-releases.sh latest

set -euo pipefail

REPO="beckn/protocol-specifications-v2"

cmd="${1:-list}"
shift || true

case "$cmd" in
  list)
    gh release list --repo "$REPO" "$@"
    ;;
  view)
    gh release view "$1" --repo "$REPO"
    ;;
  latest)
    gh release view --repo "$REPO" --jq '{tag: .tagName, name: .name, published: .publishedAt, url: .url}' --json tagName,name,publishedAt,url
    ;;
  *)
    echo "Unknown command: $cmd. Use list | view | latest" >&2
    exit 1
    ;;
esac
