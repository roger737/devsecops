# Written reflection

## Methodology

I treated this as a risk-reduction engagement rather than a scanner installation. The Day 1 brief prioritizes credentials and administrator cloud roles because they create immediate compromise paths. The implementation then protects the delivery path with four independent gates, a single required aggregate check, review rules, artifacts, and a repeatable exception process. Juice Shop remains an unmodified, pinned submodule so the evidence is reproducible and the intentionally vulnerable training source is not confused with my delivery configuration.

I chose controls that produce different kinds of evidence. Custom static-analysis rules demonstrate whether a dangerous source pattern exists; dependency and image scans identify known vulnerabilities with resolved package versions; the software bill of materials answers “what is inside”; and the container smoke test answers “does the exact image run.” A successful scan is not a claim that Juice Shop is secure. Indeed, a High-severity finding and blocked merge are expected evidence for this target.

## Trade-offs and decisions

GitHub Actions fits the company's existing automation and avoids new infrastructure. Third-party actions and tools are version- or commit-pinned, and workflow tokens receive only the permissions needed. The trade-off is maintenance: pinned actions, base-image digests, scanners, and vulnerability databases need deliberate updates. Scheduled scans cover newly disclosed issues in unchanged code, but only if somebody owns the alerts.

Semgrep rules are deliberately narrow. The raw-query rule catches template interpolation and recommends bind parameters or replacements; it is not full data-flow analysis. This improves explainability and testability but can miss obfuscated flows and can match harmless constants. The included false-positive example shows narrow suppression, while safe test cases protect against overmatching. A broader commercial or CodeQL setup could provide deeper analysis later.

Strict High/Critical gating demonstrates prevention, but enforcing every historical finding on day one would stop delivery across a real 40-service portfolio. The rollout therefore warns first, baselines existing issues, and blocks new findings after a short validation period. Genuine findings in this demonstration are not suppressed merely to obtain a green build. Critical internet-facing or actively exploited issues still require immediate action regardless of rollout phase.

The current-tree secret gate supports the required add-and-remove demonstration. A separate history audit makes an important limitation explicit: deleting a leaked value from the latest commit neither removes history nor revokes access. Real credentials must be rotated immediately. Reports are redacted, and only synthetic credentials are used for the demonstration.

For containers, I retained upstream's useful distroless and non-root design rather than inventing a false “before.” The changes pin images and build tools, reduce builder size, keep application code root-owned, limit writes to required paths, and exercise runtime privilege restrictions. Distroless improves the attack surface but makes interactive debugging harder; a separate debug image is preferable to production shells.

## Challenges and limitations

The pinned Juice Shop version has no committed dependency lockfile, so a deterministic `npm ci` build and exact-version filesystem scan cannot be assumed. The pipeline creates ephemeral lockfiles without executing package scripts for dependency scanning and the software bill of materials. The image build retains upstream installation behavior; committing reviewed lockfiles would be a meaningful follow-up, but modifying upstream source was outside this challenge's scope.

The Windows development environment did not provide Node.js or Docker. Authoritative scanner, image-build, and HTTP-runtime verification therefore belongs to GitHub-hosted Ubuntu runners. Local syntax checks cannot substitute for those results; final evidence must link to actual runs. The initial configuration also relies on pattern-rule tests passing on the pinned Semgrep version, so any rule adjustment must be validated rather than inferred from YAML validity.

This submission does not configure Acme's real cloud administrator policies, web firewall, denial-of-service protection, secrets manager, or production browser-origin policy because no real environment or credentials were supplied. It provides prioritized decisions and rollout controls instead. A scanner cannot prove exploitability, business impact, runtime identity, or network exposure; those require deployment context and, where appropriate, dynamic testing.

## What I would improve with more time

I would add baseline-aware pull-request comparisons while retaining full scheduled scans; signed images and attestations verified at deployment; ephemeral dynamic-application tests; and policy as code for branch and environment rules. I would also commit upstream lockfiles, test container read-only filesystems with explicit writable mounts, and measure scan duration and false-positive rates across several teams.

For a production client, I would connect findings to a tracked inventory and incident process, test restoration after a cloud-role compromise, run load and edge-protection exercises, and review runtime detections. Most importantly, I would compare escaped vulnerabilities, remediation age, delivery delay, and exception trends before and after rollout. Those outcomes show whether the controls reduce risk without becoming an unmanaged delivery tax.
