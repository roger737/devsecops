# Hardened Dockerfile: before and after

The scenario describes generic, unhardened images. The pinned upstream Juice Shop Dockerfile is already better than that scenario: it uses multiple stages, distroless, and a non-root user. This comparison therefore separates the hypothetical current state, the actual upstream baseline, and this submission rather than claiming credit for upstream controls.

| Control | Scenario “before” | Upstream at pinned commit | This submission “after” |
| --- | --- | --- | --- |
| Build stage | General-purpose image | `node:24`, mutable tag | `node:24-bookworm-slim`, pinned by digest; smaller build attack surface |
| Runtime | General-purpose image, shell and package manager available | Distroless Node.js, mutable tag | Same distroless family, pinned by digest; no shell or package manager |
| Build tools | Unpinned | Version ranges | TypeScript and CycloneDX build tools pinned to exact versions |
| Runtime identity | Unspecified/root risk | Numeric user `65532` | Numeric user/group `65532:0`; no privilege escalation at runtime |
| Application file ownership | Unspecified | Entire copied application owned by runtime user | Application remains root-owned; only required data, log, upload, and localization paths receive group write access |
| Runtime capabilities | Defaults | Not specified by Dockerfile | CI smoke test drops all Linux capabilities and enables `no-new-privileges` |
| Dependency inventory | None | Application SBOM generated during build | Upstream SBOM retained and an independent CycloneDX SBOM produced in CI |
| Vulnerability gate | None | None in this delivery pipeline | High/Critical operating-system and application vulnerabilities fail the image job |
| Runtime proof | None | Not part of this submission | CI starts the exact image and requires a successful HTTP response on port 3000 |

## Build and run

From the repository root, with Docker installed:

```bash
docker build --file Dockerfile --tag juice-shop:hardened juice-shop
docker run --rm --name juice-shop \
  --cap-drop ALL --security-opt no-new-privileges \
  --publish 127.0.0.1:3000:3000 juice-shop:hardened
```

Open `http://127.0.0.1:3000` only on an isolated machine. Do not publicly expose this intentionally vulnerable application.

## Trade-offs and remaining work

- Digest pinning improves repeatability but creates an update obligation; scheduled scans and deliberate digest updates are required.
- The upstream project does not commit a lockfile, so `npm ci` is not available. CI creates ephemeral lockfiles for exact-version scanning, while the image build retains upstream's `npm install` behavior. Committing and enforcing reviewed lockfiles would be a follow-up improvement.
- Distroless reduces tooling available to an attacker and to troubleshooting. Debug through CI logs and a separate debug image rather than adding a shell to production.
- A non-root, minimal image does not remove Juice Shop's intentional application vulnerabilities. The vulnerability scan and HTTP smoke test answer different questions and both are required.
