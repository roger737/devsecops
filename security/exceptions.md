# Security finding decisions

A finding is either remediated, shown to be a false positive with evidence, or accepted temporarily through an exception. A failing check alone is not a reason to suppress a rule.

## False positives

1. Reproduce the finding and explain why the matched code is not exploitable in its actual data flow and deployment context.
2. Add a safe test fixture. Use the narrowest possible inline suppression, including rule ID, tracking ticket, owner, and expiry; do not exclude an entire directory for one false positive.
3. Obtain the code owner's review. Re-test the rule so genuine instances remain detectable.

Example: `security/semgrep/examples/false-positive.ts` uses a fixed deployment constant, not request input. The suppression references a sample ticket and must be replaced with a real owner/ticket in an organizational rollout.

For secrets, `.gitleaks.toml` extends the complete default ruleset. It suppresses only the `private-key` rule for three exact Juice Shop paths where upstream intentionally embeds the same public training key; other rules and all other paths remain active. This is a known-fixture allowlist, not approval to commit operational credentials.

`.gitleaksignore` additionally records 72 findings deliberately distributed in the unchanged Juice Shop training target. It contains only exact `file:rule:line` fingerprints, not values or directory exclusions. The current-tree scan ignores only these reviewed entries, so new, moved, or differently classified findings remain visible. Gitleaks' JSON baseline comparison also includes platform-sensitive columns and entropy; exact fingerprints avoid that portability problem. Refreshing the inventory requires independent review and a report diff; this fixture inventory is not a production risk exception.

## Risk exceptions

Record the vulnerable component or rule, affected service and environment, business justification, compensating controls, accountable owner, approver, and expiry. High/Critical exceptions require Engineering Manager and security approval; expiry is at most 30 days for Critical and 90 days for High. The service owner escalates to the Engineering Manager before expiry if remediation will miss the date.

| ID | Service | Finding | Owner | Approver | Compensating control | Created | Expires | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| None | — | No exceptions are approved in this demonstration | — | — | — | — | — | — |

Expired exceptions automatically return the gate to blocking. Security tool outages fail closed for critical services; the Engineering Manager may authorize a time-bounded bypass for lower-risk services, recorded as an incident and reviewed the next business day.
