#!/usr/bin/env bash
# List, view, diff, or check status of pull requests via gh.
# Usage:
#   ./gh-prs.sh list [--state open|closed|merged|all] [--jq <expr>]
#   ./gh-prs.sh view <number>
#   ./gh-prs.sh diff <number>
#   ./gh-prs.sh checks <number>
#   ./gh-prs.sh comments <number>

set -euo pipefail

REPO="beckn/protocol-specifications-v2"

cmd="${1:-list}"
shift || true

case "$cmd" in
  list)
    gh pr list --repo "$REPO" "$@"
    ;;
  view)
    gh pr view "$1" --repo "$REPO"
    ;;
  diff)
    gh pr diff "$1" --repo "$REPO"
    ;;
  checks)
    gh pr checks "$1" --repo "$REPO"
    ;;
  comments)
    gh api "repos/$REPO/pulls/$1/comments" --jq '.[] | {user: .user.login, body: .body, path: .path, line: .line}'
    ;;
  *)
    echo "Unknown command: $cmd. Use list | view | diff | checks | comments" >&2
    exit 1
    ;;
esac
