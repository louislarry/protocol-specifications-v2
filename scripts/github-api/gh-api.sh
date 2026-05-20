#!/usr/bin/env bash
# Thin wrapper around `gh api` for this repo.
# Usage: ./gh-api.sh <endpoint> [gh api flags...]
# Example: ./gh-api.sh /repos/{owner}/{repo}/pulls --jq '.[].title'
#
# {owner} and {repo} are auto-substituted from GITHUB_REPO below.

set -euo pipefail

GITHUB_REPO="beckn/protocol-specifications-v2"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <endpoint> [gh api flags...]" >&2
  echo "  {owner} and {repo} in the endpoint are replaced automatically." >&2
  exit 1
fi

endpoint="${1/\{owner\}/$(cut -d/ -f1 <<<"$GITHUB_REPO")}"
endpoint="${endpoint/\{repo\}/$(cut -d/ -f2 <<<"$GITHUB_REPO")}"
shift

gh api "$endpoint" "$@"
