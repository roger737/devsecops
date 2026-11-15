# Acme Financial Services: Day 1 risk brief

**To:** Engineering Manager
**Purpose:** Reduce the most credible paths to financial loss, customer-data exposure, and service outage. This is a current-state assessment; the pipeline demonstrates controls, not proof that the whole environment is secure.

## 1. Credentials committed to source control — **Critical**

**Why:** Anyone with repository access, including a compromised developer account or dependency, may obtain reusable cloud or service credentials.

**Attack scenario:** An attacker searches current files and Git history for keys, then uses them against the associated service. Depending on the credential, they could read customer records, move money, impersonate internal systems, or incur cloud charges; cleanup would require incident response, customer notification, and regulatory assessment.

## 2. Administrator access on every cloud role — **Critical**

**Why:** One stolen role can become complete control of the cloud account rather than access to one workload.

**Attack scenario:** A malicious dependency or phished developer session assumes an administrator role, creates persistent access, disables audit logs, and exports or deletes data. Acme could lose confidentiality, integrity, and availability across all services simultaneously, with prolonged recovery and severe trust and regulatory consequences.

## 3. Direct, unreviewed changes to the production branch — **High**

**Why:** No independent review or required check stands between a compromised account and production code.

**Attack scenario:** An attacker with one developer account merges a backdoor or altered payment routine directly to the main branch, and the existing automation deploys it. Customers and the business could suffer fraudulent transactions or data loss, while a lack of independent review delays detection and undermines accountability.

## 4. No code, dependency, or image vulnerability management — **High**

**Why:** Acme cannot reliably prevent or quickly respond to known weaknesses, and without a software bill of materials it lacks a dependable component inventory.

**Attack scenario:** An attacker scans an internet-facing service for a publicly disclosed package or application flaw and exploits it before Acme knows the component is present. The result could be customer-data theft or service takeover; during the next urgent disclosure, engineers would also lose days manually determining which of 40 services are affected.

## 5. Internet services lack edge and browser-request protections — **High**

**Why:** There is no managed web firewall or distributed-denial-of-service protection, and every website is currently trusted to make cross-origin requests.

**Attack scenario:** Attackers automate abusive requests and flood public endpoints until legitimate customers cannot transact, while a malicious website can attempt cross-origin actions through a visitor's browser. Acme could lose revenue and availability, expose customer information where authentication and browser policy permit it, and face prolonged operational disruption.

## What to fix first

**Today:** revoke exposed credentials, move replacements into a managed secrets store, and remove administrator policies from roles. These are immediate compromise paths; scanning can wait a few hours, active credentials cannot. Preserve evidence before history cleanup, and rotate rather than merely delete secrets.

**This week:** protect the main branch with review and required checks, then introduce secret scanning, dependency inventory, and High/Critical code, dependency, and image gates in warning mode. Assign owners to existing findings and enforce new findings after teams validate the rules.

**Next:** restrict cross-origin access to known sites, add managed edge filtering, rate limits, and denial-of-service protection, and finish container hardening. Track exposure removal, privileged-role reduction, remediation time, and service coverage so leadership sees risk reduction rather than scanner counts.
