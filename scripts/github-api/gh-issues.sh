#!/usr/bin/env bash
# List, view, or search issues via gh.
# Usage:
#   ./gh-issues.sh list [--state open|closed|all] [--label <label>] [--jq <expr>]
#   ./gh-issues.sh view <number>
#   ./gh-issues.sh search "<query>"

set -euo pipefail

REPO="beckn/protocol-specifications-v2"

cmd="${1:-list}"
shift || true

case "$cmd" in
  list)
    gh issue list --repo "$REPO" "$@"
    ;;
  view)
    gh issue view "$1" --repo "$REPO"
    ;;
  search)
    gh search issues "$@" --repo "$REPO"
    ;;
  *)
    echo "Unknown command: $cmd. Use list | view | search" >&2
    exit 1
    ;;
esac
