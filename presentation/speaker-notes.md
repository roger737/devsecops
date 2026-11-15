# Speaker notes — 45 minutes

Use `docs/demo-runbook.md` for detailed screen steps and backup handling. Run and pull-request links are maintained in `docs/evidence.md`.

## 1. Security that ships with the code — 1 min (00:00–01:00)

Introduce the objective: reduce delivery risk for a fintech team without creating an unworkable delivery tax. State that the demonstration uses an intentionally vulnerable, unmodified Juice Shop commit and that real scan outcomes are reported honestly.

## 2. The pipeline becomes a control point — 2 min (01:00–03:00)

Frame the result in business terms. The solution is not four scanners; it is a repeatable decision about what may merge. Independent jobs preserve evidence when one gate fails. The aggregate check simplifies enforcement, and the rollout acknowledges that legacy findings need managed remediation rather than an immediate portfolio-wide shutdown.

## 3. Five risks, ordered by business consequence — 3 min (03:00–06:00)

Use one realistic attack sentence per item. Credentials are searched in current files and history and then reused. Administrator access turns a single compromise into account-wide confidentiality, integrity, and availability loss. Direct merges let one identity alter production. Missing scanning and inventory leave known flaws and slow response. Missing edge protection and unrestricted browser-origin policy expose public services to abuse. Refer the panel to the one-page brief for full scenarios.

## 4. Small control gaps combine into major incidents — 2 min (06:00–08:00)

Emphasize chained risk. A scanner alone does not remove stolen credentials or excessive cloud privilege. Review, least privilege, inventory, and edge controls interrupt different parts of these paths. This is why the first-fix order is based on blast radius and immediacy rather than scanner convenience.

## 5. Contain immediate exposure first — 2 min (08:00–10:00)

Explain why credentials and cloud privilege precede scanner rollout: they may already enable compromise. Branch protection then prevents unreviewed delivery. Scanning begins this week but transitions from warning to enforcement after teams validate it. Edge and browser-origin changes follow because they require deployment-specific knowledge.

## 6. A pinned target; no modified Juice Shop source — 1 min (10:00–11:00)

Set boundaries early. A submodule gives reproducibility and clear ownership. This submission demonstrates delivery controls around the target. It does not claim to have changed Acme infrastructure or fixed the intentionally vulnerable application.

## 7. Parallel evidence; one merge decision — 2 min (11:00–13:00)

Walk left to right. Static analysis, secret detection, dependency analysis, and the container job run independently. Each produces concise and machine-readable output. The verify job fails if any required job fails or is cancelled. Branch protection requires that check and a reviewer. Scheduled runs address new vulnerability disclosures and old Git history.

## 8. Controls beyond scanning — 2 min (13:00–15:00)

This is a preventive control, not just detection. A required reviewer and required aggregate check stop direct unreviewed merges. CODEOWNERS assigns accountability. Pinning and token permissions address the CI attack surface. Note that branch protection must be demonstrated through the actual repository API response, not just a script.

## 9. Three proofs, twelve minutes — 1 min (15:00–16:00)

Orient the audience before changing screens. The live blocks use pre-recorded run evidence where necessary to avoid waiting on runners. The backup is the evidence ledger, downloaded artifacts, and screenshots. If infrastructure fails, disclose it and continue with evidence rather than disabling a gate.

## 10. A real login SQL injection blocks the change — 4 min (16:00–20:00)

Follow demo-runbook Demo 1. Show the custom rule tests, then the actual login finding and CORS finding. Explain that interpolated request data can alter the query; replacements or bind parameters preserve the statement structure. Show the High-severity failure and aggregate result. CORS is a dangerous policy, not proof of universal account compromise. Use the evidence image if embedded; otherwise open the linked run.

## 11. Block the leak; do not confuse deletion with rotation — 4 min (20:00–24:00)

Follow Demo 2 and use the recorded failed and later runs. Open the redacted report and pull-request result. Explain why the current-tree gate can pass after removal while the scheduled history audit remains necessary. For a real credential, removal is cosmetic: revoke it first, investigate use, replace it through managed secrets, and assess history.

## 12. Inventory and runtime proof answer different questions — 4 min (24:00–28:00)

Follow Demo 3. Call out the missing upstream lockfile and the ephemeral lockfile solution. Open the CycloneDX artifact. Then show the exact image build, runtime-user assertion, HTTP smoke log, and Trivy result. Do not invent dependency or image vulnerabilities if current upstream versions have none; the real static-analysis findings already satisfy the real-vulnerability criterion.

## 13. A red gate is a controlled business decision — 2 min (28:00–30:00)

Address the apparent paradox of a red main workflow. The demonstration intentionally retains real findings. Success is accurate detection and enforcement, not green cosmetics. In production, new findings block while legacy issues receive risk-based deadlines. An unavailable scanner is distinct from a vulnerability result and follows an explicit outage policy.

## 14. Build on upstream strengths; add repeatability and proof — 2 min (30:00–32:00)

Be honest: upstream already uses distroless and non-root. The added value is pinning, a smaller builder, exact tool versions, reduced application-file ownership, runtime restrictions, and verified execution. Digest pinning adds maintenance. Distroless complicates debugging, so use CI logs and separate debug images.

## 15. Narrow decisions with ownership and expiry — 2 min (32:00–34:00)

Differentiate false positives from accepted genuine risk. A false positive has technical evidence and a narrow suppression. A genuine issue needs remediation or an approved exception. Release pressure alone is not a technical justification. Expiry automatically restores the blocking decision. Escalation is visible, not an administrator quietly disabling a check.

## 16. “Critical” is an evidence-based classification — 2 min (34:00–36:00)

This definition avoids a vague critical label. Use the service catalog and deployment evidence, not team preference. Any of the listed criteria qualifies a service. Record the business owner, data, exposure, privileges, dependencies, and recovery objective. Reassess after architecture changes.

## 17. Warn, prove, enforce, then scale — 2 min (36:00–38:00)

The counts sum to 40. Start with payment, authentication, customer data, public interfaces, and privileged deployment services. Warning mode has a deadline and owner. Enforce new findings while existing ones follow Critical seven-day and High 30-day targets, faster if exploited. Rollout pauses are narrow exceptions, not global scanner shutdowns.

## 18. Measure risk reduction and delivery friction — 2 min (38:00–40:00)

Raw finding counts are not a success metric. Track protected coverage, live-secret elimination, remediation age, escaped findings, precision, reliability, delivery delay, and exception health. Developer pushback receives a two-day evidence review. Disagreement goes to the security lead and Engineering Manager; nobody self-approves. Repeated friction drives rule tuning or training.

## 19. Deliberate choices and their costs — 2 min (40:00–42:00)

Show that the design reasons about limitations. No tool is sufficient by itself. Narrow rules are easier to trust but can miss obfuscation. Pinning improves repeatability but needs updates. Strict enforcement in the demo is paired with a realistic adoption plan. A running container is not a vulnerability-free application.

## 20. From delivery controls to verified production assurance — 2 min (42:00–44:00)

Prioritize improvements that close current assurance gaps. Baseline-aware comparisons reduce legacy noise without hiding scheduled full-scan findings. Signing and deployment verification extend trust beyond the runner. Dynamic tests add runtime evidence. Real client work includes cloud privilege, managed secrets, and edge controls that could not be configured without the environment.

## 21. Reduce risk without losing delivery — 1 min (44:00–45:00)

Close on the three outcomes: immediate exposure containment, preventive delivery controls, and a measured adoption path. Point to the repository for the one-page brief, working pipeline, evidence, rollout, and reflection. Transition to Q&A after the 45-minute presentation.
