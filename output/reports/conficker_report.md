# Cortex Analysis Report
**Subject:** Conficker Worm (2008) — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.004360Z  
**Source:** `examples/conficker.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 12 |
| VIOLATIONS | 12 |
| CONTEXT    | 11 |

**Authorization Violation Severity:** 🔴 Critical  
**Skeleton → Violation gap:** +0 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Exploits MS08-067 (Windows Server Service buffer overflow) for remote code execution | Assumes right to exploit OS vulnerability to gain execution without any user interaction |
| 2 | Disables Windows Automatic Update service | Assumes right to disable host security mechanisms (Defender, Security Center, Windows Update) |
| 3 | Disables Windows Security Center and Windows Defender | Assumes right to modify DNS resolution behavior system-wide |
| 4 | Blocks DNS resolution for security vendor domains | Assumes right to block owner's access to security resources and patches |
| 5 | Downloads and executes arbitrary code from generated domain names (DGA) | Assumes right to brute-force credentials on network shares belonging to other systems |
| 6 | Generates pseudo-random domain names daily using date as seed (Domain Generation Algorithm) | Assumes right to write to removable media and modify autorun behavior |
| 7 | Propagates via network shares using password brute-force | Assumes right to establish persistent outbound C2 communication |
| 8 | Propagates via removable media (autorun.inf injection) | Assumes right to map and traverse the local network |
| 9 | Patches MS08-067 on infected hosts to block competing malware | Assumes right to download and execute arbitrary remote code at attacker's direction |
| 10 | Establishes peer-to-peer C2 network across infected hosts | Assumes right to modify OS internals to maintain exclusive infection (patches vulnerability for self-protection) |
| 11 | Polls generated domains for updated payload instructions | Zero user interaction required for propagation after initial infection vector |
| 12 | Enumerates and maps local network topology | Actively works to prevent owner from regaining control (update/AV blocking) |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Exploits MS08-067 (Windows Server Service buffer overflow) for remote code execution
- Disables Windows Automatic Update service
- Disables Windows Security Center and Windows Defender
- Blocks DNS resolution for security vendor domains
- Downloads and executes arbitrary code from generated domain names (DGA)
- Generates pseudo-random domain names daily using date as seed (Domain Generation Algorithm)
- Propagates via network shares using password brute-force
- Propagates via removable media (autorun.inf injection)
- Patches MS08-067 on infected hosts to block competing malware
- Establishes peer-to-peer C2 network across infected hosts
- Polls generated domains for updated payload instructions
- Enumerates and maps local network topology

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- Assumes right to exploit OS vulnerability to gain execution without any user interaction
- Assumes right to disable host security mechanisms (Defender, Security Center, Windows Update)
- Assumes right to modify DNS resolution behavior system-wide
- Assumes right to block owner's access to security resources and patches
- Assumes right to brute-force credentials on network shares belonging to other systems
- Assumes right to write to removable media and modify autorun behavior
- Assumes right to establish persistent outbound C2 communication
- Assumes right to map and traverse the local network
- Assumes right to download and execute arbitrary remote code at attacker's direction
- Assumes right to modify OS internals to maintain exclusive infection (patches vulnerability for self-protection)
- Zero user interaction required for propagation after initial infection vector
- Actively works to prevent owner from regaining control (update/AV blocking)

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- Infection requires zero user consent — exploits unpatched systems without interaction
- Systematically removes the owner's ability to detect or remediate the infection
- Blocking security updates and AV domains leaves the host permanently degraded even post-removal
- DGA-based C2 makes takedown exceptionally difficult — attacker rotates domains faster than defenders can block
- Brute-forcing network shares extends unauthorized access to systems beyond the originally infected host
- Peer-to-peer C2 eliminates single point of failure — no central server to shut down
- Estimated 9–15 million machines infected across government, military, business, and consumer systems
- Patching MS08-067 on infected hosts demonstrates deliberate owner-exclusion: attacker maintains sole access
- Removable media propagation jumps air-gapped or network-isolated systems
- Full network topology mapping gives attacker persistent intelligence about victim infrastructure
- Represents a platform, not just a worm — designed to maintain a controllable botnet, not just spread

---
## Impact Statement

This artifact exhibits **12** distinct authorization violations at **critical** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
