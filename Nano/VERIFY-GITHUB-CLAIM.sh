#!/usr/bin/env bash
# Read-only check. Requires GitHub CLI (gh) authenticated locally.
# Never prints tokens or comment body; never writes to GitHub.
set -u
OWNER="AtmaOVictu"
REPO="Atmavictu"
ISSUE="753"
COMMENT_ID="6397386784"
TARGET="${OWNER}/${REPO}"

if ! command -v gh >/dev/null 2>&1; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=GitHub CLI (gh) is not installed.'
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=No valid GitHub CLI login detected; authenticate locally without sharing credentials.'
  exit 2
fi

if ! repo_json="$(gh api "repos/${TARGET}" 2>/dev/null)"; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=Repository lookup failed or authenticated user lacks access.'
  exit 3
fi
repo_name="$(printf '%s' "$repo_json" | jq -r '.full_name // "unknown"')"
repo_url="$(printf '%s' "$repo_json" | jq -r '.html_url // "unknown"')"
echo "REPOSITORY=${repo_name}"
echo "REPOSITORY_URL=${repo_url}"

if ! issue_json="$(gh api "repos/${TARGET}/issues/${ISSUE}" 2>/dev/null)"; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=Issue lookup failed.'
  exit 4
fi
issue_url="$(printf '%s' "$issue_json" | jq -r '.html_url // "unknown"')"
echo "ISSUE_URL=${issue_url}"

# Search paginated issue comments for the exact numeric comment ID. Do not output body.
if ! match="$(gh api --paginate "repos/${TARGET}/issues/${ISSUE}/comments" --jq ".[] | select(.id == ${COMMENT_ID}) | {id: .id, html_url: .html_url, created_at: .created_at, updated_at: .updated_at, author: .user.login}" 2>/dev/null)"; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=Comment endpoint could not be queried.'
  exit 5
fi
if [ -z "${match//[[:space:]]/}" ]; then
  echo 'STATUS=UNCONFIRMED'
  echo 'REASON=The specified comment ID was not returned from the accessible issue comments.'
  exit 6
fi
echo 'COMMENT_METADATA_BEGIN'
printf '%s\n' "$match"
echo 'COMMENT_METADATA_END'
echo 'STATUS=COMMENT_METADATA_VERIFIED'
echo 'NOTE=This confirms metadata returned by the authenticated GitHub API; preserve this output with timestamp before making any broader claim.'
