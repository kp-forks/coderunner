# Incident Response Plan (IRP)

This document outlines how we handle security vulnerabilities. It is a living document. Reporters and stakeholders can use the phases below to understand where we are during an active incident.

We support two disclosure strategies:

- **Advisory With Patch** _(default)_: A fix is prepared privately and released alongside a public advisory.
- **Advisory Early** _(rare)_: An advisory is published before a fix is available — used when the vulnerability is already public or actively exploited.

---

## Phase 1 — Triage
_"We're investigating."_
**Target: within 36 hours of report**

- Acknowledge receipt to the reporter.
- Reproduce and validate the vulnerability.
- Assess severity:
  - **Critical** — Active exploitation or data exposure. Drop everything.
  - **High** — Exploitable, no known active exploitation.
  - **Medium/Low** — Limited impact or requires unlikely conditions.
- Create a draft [GitHub Security Advisory (GHSA)](https://docs.github.com/en/code-security/security-advisories).
- Decide disclosure strategy (Advisory With Patch or Advisory Early).

## Phase 2 — Containment
_"We've identified the issue and are limiting its impact."_
**Target: 1–7 days after triage**

- Isolate affected systems or services (revoke keys, disable endpoints, pull images).
- Preserve evidence (logs, snapshots) before making changes.
- Scope impact: identify affected components, versions, and platforms.
- Request a CVE via the GitHub advisory interface.
- Communicate status to the reporter.

## Phase 3 — Fix & Release
_"We're working on a fix."_
**Target: within 90 days of initial report**

- Develop and test a patch.
- At least 2 team members review and sign off.
- Publish the GHSA and deploy the fix simultaneously.
- _Advisory Early: update the existing public advisory with fix details._

## Phase 4 — Disclosure
_"The fix is live. Here's what happened."_
**Target: same day as fix release**

- Notify the reporter that the issue is resolved.
- Credit the reporter (unless they prefer anonymity).
- Verify the published advisory is accurate and complete.
- We follow the industry-standard **90-day coordinated disclosure window**. If a fix cannot ship in 90 days, we coordinate with the reporter on a revised timeline.

## Phase 5 — Post-Incident Review
_"We're making sure this doesn't happen again."_
**Target: within 2 weeks of resolution**

- Document root cause, timeline, and actions taken.
- Identify process or code improvements to prevent recurrence.
- Update this plan if gaps were found.

---

## Contact

Email: [hello@instavm.io](mailto:hello@instavm.io)

## Reporting a Vulnerability

See [SECURITY.md](SECURITY.md). **Do not open public issues.**
