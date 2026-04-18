# Cortex Analysis Report
**Subject:** SolarWinds SUNBURST (March–December 2020) — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.347773Z  
**Source:** `examples/sunburst.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 18 |
| VIOLATIONS | 12 |
| CONTEXT    | 13 |

**Authorization Violation Severity:** 🔴 Critical  
**Skeleton → Violation gap:** -6 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Compromises the SolarWinds build pipeline and inserts a trojanized DLL (`solarwinds.orion.core.businesslayer.dll`) into affected Orion Platform releases (2019.4 HF5 through 2020.2 HF1) | Assumes right to insert attacker-controlled code into a software vendor's build pipeline without the vendor's awareness |
| 2 | Allows the trojanized DLL to be signed by SolarWinds' own legitimate code-signing certificate as part of the vendor's standard build process | Assumes right to have malicious code signed by the victim vendor's own legitimate certificate, laundering the malicious artifact through the vendor's intact trust chain |
| 3 | Distributes the signed, backdoored update to ~18,000 Orion customers through the vendor's normal update channel | Assumes right to distribute malicious software through a trusted update channel to every customer, then later select which of those customers actually gets exploited |
| 4 | Implements a dormancy period after installation before initiating any network activity | Assumes right to exploit the pervasive privilege SolarWinds Orion holds in customer networks by virtue of its monitoring function |
| 5 | Beacons to a per-victim subdomain of `avsvmcloud[.]com` using a protocol crafted to imitate legitimate SolarWinds telemetry | Assumes right to forge SAML tokens that any federated service must accept as genuine, because the signing certificate itself is now attacker-controlled |
| 6 | Selectively delivers second-stage infrastructure (TEARDROP, RAINDROP, Cobalt Strike BEACON) only to a narrow subset of infected organizations of interest to the operator | Assumes right to manufacture trust inside the victim's identity layer rather than merely stealing an existing credential — the forged tokens are cryptographically valid |
| 7 | Uses DGA-style subdomains and DNS CNAME responses to direct follow-on command and control to rotating IP addresses | Assumes right to add new federation trusts to on-premises identity infrastructure, creating attacker-controlled identity providers the victim does not see |
| 8 | Applies sandbox-detection checks against hardcoded IPv4/IPv6 ranges (including RFC-reserved addresses) and halts on hits | Assumes right to impersonate any user the compromised identity provider can authenticate, across all SaaS and cloud services the organization has federated |
| 9 | Applies time-threshold checks to produce unpredictable delays between C2 attempts, defeating network-based timing analysis | Assumes right to access email belonging to the very personnel responsible for detecting and responding to the intrusion |
| 10 | Uses steganography to obscure C2 communications (per FireEye) | Assumes right to operate for many months inside compromised environments without triggering detection, by deliberately mimicking legitimate SolarWinds protocol behavior and legitimate administrator activity |
| 11 | Routes C2 traffic through VPS infrastructure geolocated in the victim's own country and rotates last-mile IPs frequently | Assumes right to fragment its own signature across many hosts, relying on the dormancy and selectivity to prevent cross-victim correlation |
| 12 | Escalates privileges within Active Directory to compromise the SAML token-signing certificate ("Golden SAML") | Zero authorization checks at any layer; no consent from vendor, from any intermediate customer, or from users whose tokens were forged |
| 13 | Forges valid, unauthorized SAML tokens and presents them to cloud and SaaS services that federate trust to the compromised identity provider | — |
| 14 | Adds attacker-controlled authentication credentials (tokens, certificates) to existing Azure / Microsoft 365 application service principals | — |
| 15 | Adds new federation trusts to on-premises AD FS infrastructure to enable authentication from outside the victim's known identity perimeter | — |
| 16 | Accesses hosted email, SharePoint, OneDrive, and other SAML-trusting services via Microsoft Graph API and similar programmatic interfaces | — |
| 17 | Targets email accounts of IT staff and incident responders specifically | — |
| 18 | Uses password guessing, password spraying, and previously-stolen secret keys to bypass MFA (e.g., Duo cookie-forgery at Volexity) | — |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Compromises the SolarWinds build pipeline and inserts a trojanized DLL (`solarwinds.orion.core.businesslayer.dll`) into affected Orion Platform releases (2019.4 HF5 through 2020.2 HF1)
- Allows the trojanized DLL to be signed by SolarWinds' own legitimate code-signing certificate as part of the vendor's standard build process
- Distributes the signed, backdoored update to ~18,000 Orion customers through the vendor's normal update channel
- Implements a dormancy period after installation before initiating any network activity
- Beacons to a per-victim subdomain of `avsvmcloud[.]com` using a protocol crafted to imitate legitimate SolarWinds telemetry
- Selectively delivers second-stage infrastructure (TEARDROP, RAINDROP, Cobalt Strike BEACON) only to a narrow subset of infected organizations of interest to the operator
- Uses DGA-style subdomains and DNS CNAME responses to direct follow-on command and control to rotating IP addresses
- Applies sandbox-detection checks against hardcoded IPv4/IPv6 ranges (including RFC-reserved addresses) and halts on hits
- Applies time-threshold checks to produce unpredictable delays between C2 attempts, defeating network-based timing analysis
- Uses steganography to obscure C2 communications (per FireEye)
- Routes C2 traffic through VPS infrastructure geolocated in the victim's own country and rotates last-mile IPs frequently
- Escalates privileges within Active Directory to compromise the SAML token-signing certificate ("Golden SAML")
- Forges valid, unauthorized SAML tokens and presents them to cloud and SaaS services that federate trust to the compromised identity provider
- Adds attacker-controlled authentication credentials (tokens, certificates) to existing Azure / Microsoft 365 application service principals
- Adds new federation trusts to on-premises AD FS infrastructure to enable authentication from outside the victim's known identity perimeter
- Accesses hosted email, SharePoint, OneDrive, and other SAML-trusting services via Microsoft Graph API and similar programmatic interfaces
- Targets email accounts of IT staff and incident responders specifically
- Uses password guessing, password spraying, and previously-stolen secret keys to bypass MFA (e.g., Duo cookie-forgery at Volexity)

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- Assumes right to insert attacker-controlled code into a software vendor's build pipeline without the vendor's awareness
- Assumes right to have malicious code signed by the victim vendor's own legitimate certificate, laundering the malicious artifact through the vendor's intact trust chain
- Assumes right to distribute malicious software through a trusted update channel to every customer, then later select which of those customers actually gets exploited
- Assumes right to exploit the pervasive privilege SolarWinds Orion holds in customer networks by virtue of its monitoring function
- Assumes right to forge SAML tokens that any federated service must accept as genuine, because the signing certificate itself is now attacker-controlled
- Assumes right to manufacture trust inside the victim's identity layer rather than merely stealing an existing credential — the forged tokens are cryptographically valid
- Assumes right to add new federation trusts to on-premises identity infrastructure, creating attacker-controlled identity providers the victim does not see
- Assumes right to impersonate any user the compromised identity provider can authenticate, across all SaaS and cloud services the organization has federated
- Assumes right to access email belonging to the very personnel responsible for detecting and responding to the intrusion
- Assumes right to operate for many months inside compromised environments without triggering detection, by deliberately mimicking legitimate SolarWinds protocol behavior and legitimate administrator activity
- Assumes right to fragment its own signature across many hosts, relying on the dormancy and selectivity to prevent cross-victim correlation
- Zero authorization checks at any layer; no consent from vendor, from any intermediate customer, or from users whose tokens were forged

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- Compromised the SolarWinds build pipeline — the damaged trust relationship was not between victim and attacker, but between victim and their own trusted vendor, which propagated automatically through normal software update behavior
- CISA published this as "a grave risk to the Federal Government and state, local, tribal, and territorial governments as well as critical infrastructure entities and other private sector organizations"
- U.S. Government formally attributed the activity to the Russian Foreign Intelligence Service (SVR), making this a nation-state intrusion disguised as ordinary vendor update traffic
- Dwell time exceeded nine months — attackers were inside federal networks from at least March 2020 and were not discovered until December 2020 via FireEye's self-disclosure of its own breach
- Known victims include CISA itself, the Treasury, Commerce, State, DHS, DOE (including NNSA), and Justice departments; estimated ~100 high-value organizations received second-stage follow-on targeting out of ~18,000 that received the backdoor
- Introduces a violation class not yet in the corpus: *build-pipeline trust subversion* — the attacker did not steal a code-signing certificate (as in Stuxnet), they compromised the signing process itself so the vendor's correct signer authenticated malicious code
- Introduces a second new violation class: *identity-layer forgery* via Golden SAML — the attacker owns the certificate that defines what "authentic" means for the victim organization, making every trust decision downstream structurally unreliable
- Federated identity abuse means the victim's cloud services cannot distinguish attacker from user from inside the protocol itself; detection must come from anomaly patterns, not from authentication layer checks
- CISA guidance explicitly states that when this level of compromise has occurred, "the entire identity trust store" must be considered compromised and a "full reconstitution of identity and trust services" is required — there is no selective remediation available
- Operational security targeting of IR personnel's own mailboxes means the standard response playbook (coordinate remediation over email) is itself within the attacker's observation window
- Establishes a template for follow-on supply-chain operations: the same TTPs were later reused in Kaseya, 3CX, and other vendor compromises, and previewed the trust-inheritance logic that xz-utils would formalize at the open-source tier
- Dormancy + selectivity inverts the usual detection calculus: ~18,000 organizations had the artifact but most were never exploited, so artifact presence alone is not compromise evidence and artifact absence is not safety evidence
- No nation has faced meaningful consequences for the operation; no international framework addresses build-pipeline trust subversion as a distinct category of hostile state action

---
## Impact Statement

This artifact exhibits **12** distinct authorization violations at **critical** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
