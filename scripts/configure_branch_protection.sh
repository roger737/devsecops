#!/usr/bin/env bash
set -euo pipefail

repository="${1:-${GITHUB_REPOSITORY:-}}"
if [[ -z "$repository" || "$repository" != */* ]]; then
  echo "Usage: $0 OWNER/REPOSITORY" >&2
  exit 2
fi
if grep -q '@REPOSITORY_OWNER' .github/CODEOWNERS; then
  echo "Replace @REPOSITORY_OWNER in .github/CODEOWNERS first." >&2
  exit 2
fi
command -v gh >/dev/null
gh auth status

mkdir -p docs/evidence
gh api --method PUT "/repos/$repository/branches/main/protection" --input - <<'JSON' | tee docs/evidence/branch-protection.json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Security gates / verify"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1,
    "require_last_push_approval": true
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": false
}
JSON

gh api "/repos/$repository/branches/main/protection" | tee docs/evidence/branch-protection-verified.json
