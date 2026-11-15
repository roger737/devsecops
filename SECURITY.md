# Security policy

This repository intentionally references OWASP Juice Shop, which contains exploitable training vulnerabilities. Run it only on an isolated local or CI runner network. Do not deploy it to production, expose it to the internet, or attach production credentials/data.

Do not open a public issue for an unintended vulnerability in this repository's delivery configuration. Report it privately to the repository owner. Intentional Juice Shop vulnerabilities are the subject of the demonstration, not newly discovered upstream defects.

If a credential is exposed, revoke and rotate it immediately. Removing a file or rewriting Git history does not revoke a credential.
