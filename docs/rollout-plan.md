# DevSecOps rollout plan for 40 microservices

## Outcome and ownership

Within 90 days, every service will have an owned component inventory and security scan results; every production branch will require review; and new High/Critical findings will block unless covered by an approved, unexpired exception. The Engineering Manager owns adoption and delivery trade-offs, service owners own remediation, the three DevOps engineers own the shared pipeline, and an appointed security lead owns rule quality and exception review.

## What “critical service” means

Classify services using deployment and business evidence, not team preference. A service is **critical** if any of these applies:

1. It initiates, approves, settles, or reconciles financial transactions.
2. It stores or exposes customer identity, payment, authentication, or regulated financial data.
3. It is internet-facing and can directly reach one of the above, or it provides identity/authentication to other services.
4. Its cloud role can modify production infrastructure, networking, secrets, or audit controls.
5. Its unavailability stops customer transactions or regulatory reporting, with no tested manual workaround for more than one hour.

Record data type, exposure, privileges, transaction dependency, recovery objective, owner, and repository in a service catalog. Resolve uncertain classifications with the Engineering Manager; until resolved, treat the service as critical. Reassess quarterly and after material architecture changes.

## Phased approach

### Phase 1 — Establish control and prove value (days 1–15; five critical services)

Choose a representative pilot: payment initiation, authentication, customer profile, public web application programming interface, and one privileged deployment service. Freeze new administrator-role grants and committed credentials immediately.

- Inventory credentials and revoke exposed values; add current-tree secret gates and a weekly history audit.
- Require one reviewer and the aggregate security check on production branches; disallow force pushes and deletion.
- Generate a software bill of materials and run dependency, static-code, and image scans in **warning-only** mode.
- Build a baseline of existing findings with owner, severity, exploitability, and due date. Fix actively exploited or internet-exposed Critical findings immediately rather than waiting for phase gates.
- Hold a 60-minute workshop and office hours; measure scan duration and false positives on real pull requests.

**Exit:** all five services have owners, baselines, branch protection, and reliable scan results; no unresolved leaked live credentials; the shared workflow runs within the agreed time budget.

### Phase 2 — Enforce new risk on critical services (days 16–45; remaining critical and internet-facing services, approximately 15)

- Roll the same reusable workflow to the next services, starting with transaction and privileged paths.
- Turn secret and new High/Critical static-code, dependency, and image findings into required blocking checks. Keep the existing baseline visible with remediation dates; do not relabel it as fixed.
- Require immutable/non-root images for new deployments. Add runtime capability dropping and no-privilege-escalation settings.
- Reduce cloud roles to specific actions/resources, beginning with continuous-integration and deployment roles.
- Publish a weekly service scorecard and review exceptions in a 30-minute risk forum.

**Exit:** 20 services are covered; critical services block new High/Critical findings; at least 90% of routine scans complete without infrastructure error; no exception lacks an owner or expiry.

### Phase 3 — Scale to the remaining portfolio (days 46–90; final 20 services)

- Onboard lower-risk internal and batch services through the same template, with two teams onboarded per DevOps engineer per week.
- Enable blocking after a five-business-day warning period per service and completion of owner training.
- Add managed web firewall, rate limiting, distributed-denial-of-service protection, and explicit browser-origin allowlists to exposed routes.
- Add scheduled scans so new disclosures affect already-merged code. Connect alerts to service owners and the incident process.
- Audit bypasses and administrator access monthly; sample software bills of materials against deployed images.

**Exit:** all 40 services have required review, current-tree secret gates, dependency inventory, and severity gates; all exposed services have an owner-approved edge-protection design; overdue exceptions are visible to the Engineering Manager.

### Ongoing — Improve assurance (after day 90)

Add dynamic testing of ephemeral deployments, signed images and verified provenance, policy as code, and runtime detection. Review rules quarterly against escaped defects and developer feedback. Do not use the interview's intentionally vulnerable target as a production deployment.

## Adoption without unnecessary blockage

Start with warnings, but give warning mode a deadline and an owner. During the first five business days, DevOps pairs with each team to reproduce findings, correct scanner configuration, and establish the baseline. Enforce **new** findings first while existing issues follow risk-based remediation service-level targets: Critical within seven days and High within 30 days, faster when actively exploited.

Keep scans in parallel, cache vulnerability databases where safe, and set a 15-minute operational budget. A scanner outage is not a vulnerability finding: retry transient failures, show an explicit “scan unavailable” status, and follow the outage exception policy. Never silently convert a failed scanner into success.

Provide one reusable workflow, clear pull-request summaries, safe autofix guidance, example remediations, and weekly office hours. Teams should spend most time on their own findings, not learning scanner installation.

## When a developer pushes back

1. The developer supplies the finding, affected data flow, deployment context, and proposed correction within two business days.
2. DevOps and the service owner reproduce it. A false positive receives the narrowest suppression, a safe regression test, and code-owner review; the global rule is changed only after testing genuine matches.
3. A genuine issue is fixed, or the owner requests a time-bounded exception. Urgent release pressure does not make a finding a false positive.
4. Disagreement escalates to the security lead and Engineering Manager, who balance explicit business risk and compensating controls. No developer self-approves an exception, and no administrator quietly disables the check.
5. The decision and customer/delivery impact are recorded. Repeated disputes trigger rule tuning or training; repeated bypasses trigger management review.

See `security/exceptions.md` for approval and expiry rules. Expired exceptions automatically become blocking again.

## Metrics and operating review

| Metric | Definition | Target / decision supported |
| --- | --- | --- |
| Protected-service coverage | Services with required review and all four gates ÷ 40 | 5 by day 15, 20 by day 45, 40 by day 90 |
| Live-secret exposure | Confirmed active credentials found in source/history | Zero; every finding triggers revocation, not just deletion |
| Remediation age | Median days from confirmed finding to deployed fix | Critical ≤ 7 days; High ≤ 30 days |
| New-finding escape rate | High/Critical issues found after deployment ÷ changes deployed | Downward trend; review missed rule/classes monthly |
| Rule precision | Confirmed true findings ÷ reviewed findings | ≥ 90% before global blocking; tune noisy rules |
| Scan reliability | Completed scans without tool/infrastructure error ÷ runs | ≥ 95%; fund platform work if below target |
| Pipeline impact | Median and 95th-percentile added pull-request time | No more than five minutes median added time without approval |
| Exception health | Active, expired, and overdue exceptions by owner | Zero expired; decreasing repeat exceptions |
| Adoption friction | Reverted gates, support tickets, and bypasses per team | Review weekly; distinguish training needs from unsafe pressure |

The Engineering Manager receives a one-page weekly trend: exposed secrets removed, administrator roles reduced, protected services, overdue Critical/High issues, and delivery impact. Raw finding counts alone are not success; reduced exposure and remediation age are.

## Rollback and incident handling

If a gate causes widespread disruption, pause enforcement only for the affected rule and service through an approved, expiring exception; keep scanning and reporting. Do not disable the entire pipeline. For an active leak or exploited vulnerability, incident response takes precedence: revoke, contain, patch, and preserve evidence, then update the control that should have prevented or detected it.
