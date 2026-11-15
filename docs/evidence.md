# Verification and evidence ledger

Only observed results are recorded here. The authoritative main evidence is [Security gates run 8](https://github.com/roger737/devsecops/actions/runs/43693181233), commit `872cd653cddd2b7d4626182111848f7284606fe2`. It completed with the intentionally vulnerable target blocked by real findings.

| Requirement | Evidence | Status |
| --- | --- | --- |
| Juice Shop pinned without source changes | Submodule commit `266448aba68cd8ba5915f526a128da4fa7bc3f9f` | Confirmed |
| Local configuration and helper scripts | `actionlint` 1.7.12 passed both workflows; five unit tests passed; repository validator passed | Local validation passed |
| Pipeline runs end-to-end | [Run 8](https://github.com/roger737/devsecops/actions/runs/43693181233) ran every job and the aggregate gate | Completed; expected red gates |
| Custom rules have safe/unsafe tests | `security/semgrep/tests/`; [Static analysis job](https://github.com/roger737/devsecops/actions/runs/43693181233/job/132747915803) test step succeeded | Passed |
| Real SQL injection detected | `juice-shop/routes/login.ts:34`, raw interpolated Sequelize query; summary assertion succeeded | Confirmed |
| Real unrestricted cross-origin middleware detected | `juice-shop/server.ts`; custom-rule summary assertion succeeded | Confirmed |
| High/Critical static-analysis gate blocks | 14 High findings; final SAST enforcement and aggregate `verify` failed; [screenshot](evidence/sast.png) | Blocking confirmed |
| Fake secret blocks test branch | [Run 9](https://github.com/roger737/devsecops/actions/runs/43693225449), commit `da3b6677cf3115ddd7b40984f515d0d25fb2d7a2`; one redacted finding at `security/demo/fake-credentials.txt:3`; [job](https://github.com/roger737/devsecops/actions/runs/43693225449/job/132748053702) and [screenshot](evidence/secrets-blocked.png) | Blocking confirmed; PR link pending authentication |
| Removing fake secret passes current-tree gate | Final removal run on the same test branch | Pending final PR cleanup run |
| Dependency High/Critical gate | [Dependencies and SBOM job](https://github.com/roger737/devsecops/actions/runs/43693181233/job/132747915556): 30 High/Critical findings, including `ws`, `crypto-js`, `jsonwebtoken`, and `basic-ftp` | Blocking confirmed |
| CycloneDX software bill of materials | Run 8 `dependency-reports-and-sbom` artifact exists (205,997-byte ZIP), with JSON/table/SARIF and CycloneDX reports | Generated and uploaded |
| Hardened image builds and runs | [Container job](https://github.com/roger737/devsecops/actions/runs/43693181233/job/132747915741): build, `65532:0` assertion, and HTTP smoke test succeeded; [runtime screenshot](evidence/container-runtime.png) | Runtime checks passed |
| Image operating-system and application scan | Same container job: 29 High/Critical findings across OS/library scope; JSON/table/SARIF and smoke log in `container-reports`; [screenshot](evidence/container.png) | Blocking confirmed |
| Main branch requires review and security check | `docs/evidence/branch-protection-verified.json` | Pending administrator authentication |
| Presentation opens and renders | 21-slide PowerPoint package/notes validated; all 21 original PDF pages visually inspected; regenerated evidence slides 10–12 re-inspected; no shapes outside slide boundaries | Passed |

## Evidence-handling rules

- Link the immutable run or pull-request URL and record the commit SHA. Keep large JSON, SARIF, table, and software-bill-of-materials output as Actions artifacts with a 14-day retention.
- Screenshots must show the repository, run/job name, commit, and conclusion where practical. Redact credentials and personal access tokens. Synthetic credentials are still shown redacted to model safe handling.
- Do not describe a scan that found no High/Critical dependency issues as a failed vulnerability gate. A real static-analysis finding is sufficient for the challenge's “real vulnerability” criterion; dependency outcomes are reported as observed.
- Do not treat removal of a synthetic file as credential rotation or history cleanup. The separate history audit remains the correct control for old commits.
