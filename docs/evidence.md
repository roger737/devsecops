# Verification and evidence ledger

Only observed results are recorded here. “Pending” is not evidence of success; it identifies work that requires the target GitHub repository and its Actions runners.

| Requirement | Evidence | Status |
| --- | --- | --- |
| Juice Shop pinned without source changes | Submodule commit `266448aba68cd8ba5915f526a128da4fa7bc3f9f` | Local configuration confirmed |
| Local configuration and helper scripts | `actionlint` 1.7.12 passed both workflows; four unit tests passed; repository validator passed | Local validation passed |
| Pipeline runs end-to-end | Main workflow run: pending repository URL | Pending |
| Custom rules have safe/unsafe tests | `security/semgrep/tests/`; Actions test step | Pending runner result |
| Real SQL injection detected | Expected location `juice-shop/routes/login.ts`, raw interpolated Sequelize query | Pending runner result |
| Real unrestricted cross-origin middleware detected | Expected location `juice-shop/server.ts` | Pending runner result |
| High/Critical static-analysis gate blocks | Expected `Static analysis` failure and aggregate `verify` failure | Pending runner result |
| Fake secret blocks test branch | Failed run/PR and redacted Gitleaks report: pending | Pending |
| Removing fake secret passes current-tree gate | Later run on same test branch: pending | Pending |
| Dependency High/Critical gate | Trivy filesystem report and job outcome: pending | Pending |
| CycloneDX software bill of materials | `dependency-reports-and-sbom` Actions artifact | Pending |
| Hardened image builds and runs | `container-reports/container-smoke.txt`, HTTP result, non-root assertion | Pending |
| Image operating-system and application scan | Trivy image JSON/table/SARIF and job outcome | Pending |
| Main branch requires review and security check | `docs/evidence/branch-protection-verified.json` | Pending administrator configuration |
| Presentation opens and renders | 21-slide PowerPoint package/notes validated; all 21 PDF pages visually inspected; shapes within boundaries | Local validation passed |

## Evidence-handling rules

- Link the immutable run or pull-request URL and record the commit SHA. Keep large JSON, SARIF, table, and software-bill-of-materials output as Actions artifacts with a 14-day retention.
- Screenshots must show the repository, run/job name, commit, and conclusion where practical. Redact credentials and personal access tokens. Synthetic credentials are still shown redacted to model safe handling.
- Do not describe a scan that found no High/Critical dependency issues as a failed vulnerability gate. A real static-analysis finding is sufficient for the challenge's “real vulnerability” criterion; dependency outcomes are reported as observed.
- Do not treat removal of a synthetic file as credential rotation or history cleanup. The separate history audit remains the correct control for old commits.
