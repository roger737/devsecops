# Live demo runbook and Q&A

## Before the interview

- Use a laptop charger, disable notifications, and sign in to GitHub. Test repository access and the projected font size.
- Open the repository, the latest **Security gates** run, the demonstration pull request, and `docs/evidence.md`. Keep the PowerPoint/PDF and downloaded artifacts offline.
- Confirm the fake secret is synthetic, the current-tree removal run exists, and no real token appears in any screenshot or report.
- Keep the intentionally vulnerable application private to the CI runner. Do not expose port 3000 publicly.
- If the network or a registry fails, say so, show the recorded run and artifacts, and continue. Do not improvise by disabling gates.

## 45-minute flow

Follow `presentation/speaker-notes.md`. The three live blocks total 12 minutes; the remaining slides explain business risk, architecture, adoption, and decisions. Keep Q&A after the 45-minute presentation unless the panel asks to interact earlier.

## Demo 1 — Real source findings and severity gate (4 minutes)

1. Open the Semgrep custom rules. Explain that High is represented by Semgrep `ERROR`, with explicit metadata and safe/unsafe test fixtures.
2. Show the rule-test step first: annotations prove the rules distinguish unsafe raw interpolation/unrestricted cross-origin middleware from safe replacements/allowlists.
3. Open the actual `juice-shop/routes/login.ts` finding. Show request input inside the raw Sequelize query and explain SQL injection without attempting an exploit.
4. Open `juice-shop/server.ts` and show unrestricted `cors()` middleware. Note that cross-origin resource sharing is not itself an authorization mechanism; exploitability depends on credentials, endpoints, and browser policy.
5. Show the red High-severity gate and aggregate check. Open JSON/SARIF artifacts and the false-positive fixture; explain narrow suppression with ticket, owner, and expiry.

**Message:** a working gate detects a real vulnerability and prevents an unreviewed risk decision; it does not prove the rest of the application is safe.

## Demo 2 — Synthetic secret blocked, then removed (4 minutes)

Perform this before the interview and retain both run URLs. The live interview should replay the evidence rather than wait for runners.

1. Create `demo/secret-leak` from the latest main branch and restore the reviewed synthetic fixture with `git checkout 795b829 -- security/demo/fake-credentials.txt`. It contains deliberately fake AWS-shaped values, not credentials generated for an account. Do not substitute real values; common AWS documentation examples ending in `EXAMPLE` are filtered by Gitleaks and do not prove the gate works.
2. Push the branch and open a pull request. Show the red **Secret detection** job, the redacted finding location, and the blocked aggregate check. The 72 upstream training findings are exact `file:rule:line` entries in `.gitleaksignore`, not a broad path exclusion; the synthetic addition must still fail.
3. Remove the file and push the branch again. Show that the current-tree secret gate returns to zero additional findings while other intentional Juice Shop gates remain red.
4. Explain that for a real credential the next action is immediate revoke/rotate and incident response. The weekly **Secret history audit** checks old commits; deleting the latest file is insufficient.

**Message:** preventive detection is immediate, but remediation is rotation and containment, not cosmetic deletion.

## Demo 3 — Inventory, hardened runtime, and image gate (4 minutes)

1. Show the ephemeral lockfile step. Juice Shop has no committed lockfile; CI resolves exact versions without executing package scripts for the filesystem scan and software bill of materials.
2. Open the CycloneDX JSON artifact and identify its component inventory purpose. Show the Trivy dependency conclusion exactly as observed; do not claim vulnerabilities if none are present.
3. Show the Dockerfile comparison: pinned slim builder and distroless runtime, exact build-tool versions, non-root numeric identity, and root-owned application files with limited writable paths.
4. Open the container job. Prove the image built, `65532:0` was asserted, the exact container returned HTTP success, and Linux capabilities were dropped with no-new-privileges.
5. Show the Trivy image report covering both operating-system and application packages. Distinguish “runs successfully” from “is vulnerability-free.”

**Message:** inventory, build provenance, runtime behavior, and known-vulnerability scanning are complementary controls.

## Likely Q&A

**Why is the main security workflow red?**
The target is intentionally vulnerable, and High/Critical gates are supposed to block. A red check with verified findings is the requested demonstration. The rollout plan starts real services in warning mode and baselines legacy findings rather than permanently stopping all delivery.

**Why not make all checks green?**
Suppressing genuine Juice Shop findings would hide the behavior being evaluated. Safe fixtures and a separate false-positive suppression demonstrate correct handling without pretending the target is fixed.

**Does a scanner catch everything?**
No. Pattern rules can miss obfuscated data flow, dependency databases have coverage gaps, and neither understands all business logic. Review, runtime controls, dynamic testing, cloud least privilege, and incident response remain necessary.

**Why use a submodule?**
It pins an exact upstream commit, keeps intentional source unchanged, makes updates auditable, and separates the consulting deliverables from the target. The trade-off is that contributors must clone recursively.

**Why current-tree and history secret scans?**
The current-tree gate gives an actionable add/remove merge demonstration. History scanning preserves visibility into old commits. For real leaks, rotation is mandatory regardless of either result.

**Why include unfixed vulnerabilities?**
Ignoring them can hide real exposure merely because no patch exists. They block by policy, but a documented exception with compensating controls, owner, and expiry provides an explicit business decision.

**What if a developer disputes a finding?**
Reproduce it within two business days. False positives receive narrow suppression and regression tests; genuine issues are fixed or escalated for a time-bounded exception. Nobody self-approves, and release pressure does not change technical truth.

**How does this protect the pipeline itself?**
Actions are pinned to commits, tools/images to versions or digests, tokens have least privilege, workflows do not use cloud credentials, reports are redacted, concurrency limits stale runs, and branch protection requires review. Production hardening would add ephemeral runners, dependency review, signed artifacts, and verified deployment identity.

**Why pin base-image digests?**
It makes builds repeatable and prevents an unexpected tag change. The cost is deliberate updates; scheduled vulnerability scans identify when that maintenance becomes urgent.

**Is unrestricted cross-origin sharing always exploitable?**
No. It is a dangerous policy, not proof of account compromise. Impact depends on browser credentials and endpoint authorization, which is why the brief and demo avoid claiming a universal exploit.

**Can a non-root container still be vulnerable?**
Yes. It limits post-compromise privilege but does not remove application flaws. The HTTP smoke test proves operability; application and image scans address different risks.

**What is not implemented?**
No real Acme cloud, firewall, distributed-denial-of-service, or secrets-manager environment was supplied. Those changes are prioritized in the risk and rollout documents, not falsely represented as deployed.

**What would you do with more time?**
Baseline-aware pull-request comparisons, committed lockfiles, signed images and provenance, dynamic testing in ephemeral environments, policy as code, and portfolio-level outcome metrics.
