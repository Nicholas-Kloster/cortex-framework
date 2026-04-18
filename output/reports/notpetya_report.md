# Cortex Analysis Report
**Subject:** NotPetya (June 2017) — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.219985Z  
**Source:** `examples/notpetya.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 12 |
| VIOLATIONS | 11 |
| CONTEXT    | 13 |

**Authorization Violation Severity:** 🔴 Critical  
**Skeleton → Violation gap:** -1 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Initial delivery via compromised update server for M.E.Doc, a Ukrainian tax and accounting software package with mandatory use by Ukrainian businesses | Assumes right to inherit a trusted software vendor's update channel as a delivery mechanism |
| 2 | Signs the trojanized M.E.Doc update with the vendor's legitimate update infrastructure, inheriting the vendor's trust relationship | Assumes right to weaponize a mandatory-use national software package against the population legally required to run it |
| 3 | Propagates laterally using ETERNALBLUE (CVE-2017-0144) and ETERNALROMANCE (CVE-2017-0145) SMB vulnerabilities | Assumes right to execute code via trusted update signatures on systems that have no opt-out |
| 4 | Propagates laterally using credential harvesting derived from Mimikatz-style LSASS memory extraction | Assumes right to laterally traverse networks using multiple unpatched SMB vulnerabilities in parallel |
| 5 | Propagates laterally via Windows Management Instrumentation (WMIC) and PsExec using harvested credentials | Assumes right to harvest credentials from system memory to impersonate any user the host can authenticate as |
| 6 | Modifies the Master Boot Record (MBR) on infected hosts to replace normal boot with a fake CHKDSK screen | Assumes right to destroy the boot sector and file system metadata of any reachable host |
| 7 | Encrypts the Master File Table (MFT) of the NTFS volume, rendering the filesystem unmountable | Assumes right to masquerade as ransomware while operating as a destroyer — claiming a recovery contract that cannot exist |
| 8 | Displays a ransom note demanding $300 in Bitcoin and instructing victims to email a single hardcoded address | Assumes right to publish a payment contact known to be fragile, ensuring even willing victims cannot attempt recovery |
| 9 | Generates per-victim "installation keys" that are cryptographic noise, not actual key material — no recovery path exists even with the operator's cooperation | Assumes right to inflict global collateral damage in pursuit of a targeted geopolitical objective against Ukraine |
| 10 | The email contact address used for payment coordination was disabled by the hosting provider within hours of the outbreak | Assumes right to operate under a false criminal frame to obscure state attribution |
| 11 | Does not exfiltrate or catalog victims; does not maintain a decryption key database | Zero authorization checks at any layer; zero scope discipline; zero recovery path |
| 12 | Wipes its own artifacts from the infected host after execution | — |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Initial delivery via compromised update server for M.E.Doc, a Ukrainian tax and accounting software package with mandatory use by Ukrainian businesses
- Signs the trojanized M.E.Doc update with the vendor's legitimate update infrastructure, inheriting the vendor's trust relationship
- Propagates laterally using ETERNALBLUE (CVE-2017-0144) and ETERNALROMANCE (CVE-2017-0145) SMB vulnerabilities
- Propagates laterally using credential harvesting derived from Mimikatz-style LSASS memory extraction
- Propagates laterally via Windows Management Instrumentation (WMIC) and PsExec using harvested credentials
- Modifies the Master Boot Record (MBR) on infected hosts to replace normal boot with a fake CHKDSK screen
- Encrypts the Master File Table (MFT) of the NTFS volume, rendering the filesystem unmountable
- Displays a ransom note demanding $300 in Bitcoin and instructing victims to email a single hardcoded address
- Generates per-victim "installation keys" that are cryptographic noise, not actual key material — no recovery path exists even with the operator's cooperation
- The email contact address used for payment coordination was disabled by the hosting provider within hours of the outbreak
- Does not exfiltrate or catalog victims; does not maintain a decryption key database
- Wipes its own artifacts from the infected host after execution

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- Assumes right to inherit a trusted software vendor's update channel as a delivery mechanism
- Assumes right to weaponize a mandatory-use national software package against the population legally required to run it
- Assumes right to execute code via trusted update signatures on systems that have no opt-out
- Assumes right to laterally traverse networks using multiple unpatched SMB vulnerabilities in parallel
- Assumes right to harvest credentials from system memory to impersonate any user the host can authenticate as
- Assumes right to destroy the boot sector and file system metadata of any reachable host
- Assumes right to masquerade as ransomware while operating as a destroyer — claiming a recovery contract that cannot exist
- Assumes right to publish a payment contact known to be fragile, ensuring even willing victims cannot attempt recovery
- Assumes right to inflict global collateral damage in pursuit of a targeted geopolitical objective against Ukraine
- Assumes right to operate under a false criminal frame to obscure state attribution
- Zero authorization checks at any layer; zero scope discipline; zero recovery path

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- Most expensive cyberattack in history at the time — estimated $10B+ in damages globally
- Maersk lost ~$300M and had to rebuild 45,000 PCs, 4,000 servers, and 2,500 applications from a single surviving Active Directory replica recovered from Ghana
- Merck lost ~$870M including production disruption and lost sales; Reckitt Benckiser lost ~$130M; FedEx/TNT lost ~$400M; Mondelez lost ~$100M
- Insurance carriers invoked war-exclusion clauses to deny coverage, triggering multi-year litigation (Mondelez v. Zurich, Merck v. ACE) that reshaped cyber insurance doctrine
- Masqueraded as ransomware but was a destroyer — the ransom UI was a disguise, not a contract; no amount of payment could recover affected systems
- Surfaces a violation class not yet in the corpus: *pretense violation* — the attacker lies about what the artifact is, operating under a false frame to confuse attribution and delay response
- Supply-chain trust inheritance via M.E.Doc — victims had no option to refuse the compromised update because M.E.Doc was legally mandated; the trust relationship was not voluntary
- Targeted Ukraine during an active geopolitical conflict (Russia-Ukraine), with global spread as either collateral damage or plausible-deniability camouflage
- Attribution by US, UK, Australia, Canada, New Zealand, and Denmark to GRU Unit 74455 (Sandworm); Russia denied involvement and no consequences were imposed for years
- Establishes that state-sponsored operations can achieve massive global economic damage while hiding behind a criminal costume
- Reveals a second new violation class: *mandatory-software supply chain abuse* — when a jurisdiction requires use of a specific package, the trust relationship ceases to be consensual, and compromising that package becomes population-scale targeting
- Previews the xz-utils pattern: the most dangerous supply-chain attacks are not technical zero-days but trust-relationship inheritance at update boundaries
- Full recovery for many victims required rebuilding from bare metal; some data was unrecoverable and represented permanent loss of historical business records

---
## Impact Statement

This artifact exhibits **11** distinct authorization violations at **critical** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
