# Cortex Analysis Report
**Subject:** gentilkiwi/mimikatz — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.175710Z  
**Source:** `examples/mimikatz_repo.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 14 |
| VIOLATIONS | 1 |
| CONTEXT    | 12 |

**Authorization Violation Severity:** ⚪ Informational  
**Skeleton → Violation gap:** -13 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Single-tool repository published by Benjamin Delpy ("gentilkiwi") on GitHub since 2014; ~21k stars, ~4k forks, original self-described purpose is "a little tool to play with Windows security" | None at the repository level. The tool operates on the local host, requires administrator or SYSTEM privileges for its most potent capabilities, and makes no assumption about authorization against any remote system; the authorization context is externally supplied by the operator at invocation time. See the CONTEXT section for the capability-concentration implications that distinguish this sample from the mgeeky repository and for the framework observations this sample sharpens. |
| 2 | Provides the `sekurlsa` module: extracts plaintext passwords, NT hashes, SHA1 hashes, and Kerberos tickets from the memory of the Windows Local Security Authority Subsystem Service (LSASS) process | — |
| 3 | Provides the `kerberos` module: lists, exports, and re-injects Kerberos tickets; mints "Golden Tickets" when supplied with a domain's krbtgt key hash | — |
| 4 | Provides the `crypto` module: exports certificates and private keys from Windows CryptoAPI (CAPI) and Cryptography Next Generation (CNG) key stores | — |
| 5 | Provides the `vault` module: dumps credentials stored in the Windows Credential Manager vault | — |
| 6 | Provides the `lsadump` module: reads SAM database, LSA secrets, domain cached credentials, and supports `dcsync` — replicating password material directly from a domain controller using legitimate replication APIs | — |
| 7 | Provides the `token` module: manipulates Windows access tokens (elevate, revert, impersonate) | — |
| 8 | Provides `privilege::debug` to enable `SeDebugPrivilege`, the Windows privilege required to open LSASS and most other protected processes for memory read | — |
| 9 | Provides pass-the-hash, pass-the-ticket, and over-pass-the-hash operations — authenticating to remote services using harvested credential material rather than plaintext passwords | — |
| 10 | Ships as a Visual Studio solution with multiple build targets: `mimikatz` (the primary CLI), `mimilib` (DLL loadable by other processes including the Windows Authentication Package interface), `mimidrv` (a kernel driver for bypassing Protected Process Light on LSASS), `mimilove` (legacy Windows 2003 support), `mimispool` (printer-spooler-based techniques), `mimicom` (COM server interface) | — |
| 11 | Published under author attribution with email and blog links; binary releases are provided for operators who do not want to build from source | — |
| 12 | Every capability documented in the GitHub wiki with example output and invocation syntax | — |
| 13 | No outbound network communication, no telemetry, no update mechanism — the tool does what the command line says and exits | — |
| 14 | Heavily signatured by every major Windows EDR vendor; operating the published binary on a defended endpoint produces detections | — |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Single-tool repository published by Benjamin Delpy ("gentilkiwi") on GitHub since 2014; ~21k stars, ~4k forks, original self-described purpose is "a little tool to play with Windows security"
- Provides the `sekurlsa` module: extracts plaintext passwords, NT hashes, SHA1 hashes, and Kerberos tickets from the memory of the Windows Local Security Authority Subsystem Service (LSASS) process
- Provides the `kerberos` module: lists, exports, and re-injects Kerberos tickets; mints "Golden Tickets" when supplied with a domain's krbtgt key hash
- Provides the `crypto` module: exports certificates and private keys from Windows CryptoAPI (CAPI) and Cryptography Next Generation (CNG) key stores
- Provides the `vault` module: dumps credentials stored in the Windows Credential Manager vault
- Provides the `lsadump` module: reads SAM database, LSA secrets, domain cached credentials, and supports `dcsync` — replicating password material directly from a domain controller using legitimate replication APIs
- Provides the `token` module: manipulates Windows access tokens (elevate, revert, impersonate)
- Provides `privilege::debug` to enable `SeDebugPrivilege`, the Windows privilege required to open LSASS and most other protected processes for memory read
- Provides pass-the-hash, pass-the-ticket, and over-pass-the-hash operations — authenticating to remote services using harvested credential material rather than plaintext passwords
- Ships as a Visual Studio solution with multiple build targets: `mimikatz` (the primary CLI), `mimilib` (DLL loadable by other processes including the Windows Authentication Package interface), `mimidrv` (a kernel driver for bypassing Protected Process Light on LSASS), `mimilove` (legacy Windows 2003 support), `mimispool` (printer-spooler-based techniques), `mimicom` (COM server interface)
- Published under author attribution with email and blog links; binary releases are provided for operators who do not want to build from source
- Every capability documented in the GitHub wiki with example output and invocation syntax
- No outbound network communication, no telemetry, no update mechanism — the tool does what the command line says and exits
- Heavily signatured by every major Windows EDR vendor; operating the published binary on a defended endpoint produces detections

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- None at the repository level. The tool operates on the local host, requires administrator or SYSTEM privileges for its most potent capabilities, and makes no assumption about authorization against any remote system; the authorization context is externally supplied by the operator at invocation time. See the CONTEXT section for the capability-concentration implications that distinguish this sample from the mgeeky repository and for the framework observations this sample sharpens.

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- This is the second boundary-test sample. As with the mgeeky repository, the violation set at artifact level is empty because authorization context is externally supplied, not encoded in the code. The analytical work happens in this section.
- Where the mgeeky repository demonstrates the framework's behavior on *diffuse capability* — many tools, many primitives, most individually unremarkable — Mimikatz demonstrates the framework's behavior on *concentrated capability*: a single tool, a narrow domain (Windows credential material), very high per-operation consequence
- The `sekurlsa::logonpasswords` command in a single invocation can surface every interactive-session credential present in LSASS memory, including domain administrator hashes if any privileged user has recently logged on
- The `lsadump::dcsync` command in a single invocation can replicate the entire domain credential store from a domain controller by exercising a legitimate replication API, without any file being written to the DC and without invasive techniques that modern defensive tooling would reliably detect
- The `kerberos::golden` command allows the holder of a domain's krbtgt hash to forge TGTs for any user — effectively full, persistent, invisible domain takeover with a single piece of material
- These are not incremental primitives. Each is a full domain-compromise step in one command. The framework must track that concentrated capability compresses the operator's decision space: a legitimate pentest, a red-team engagement, and an unauthorized intrusion all execute the same command; the delta is entirely in the written authorization
- Capability concentration has a corresponding defender observation: because Mimikatz has been heavily signatured for over a decade, direct execution of the published binary against a defended endpoint almost always produces detection. The modern adversary response has been to reimplement individual modules (`sekurlsa`) as in-memory .NET assemblies, PowerShell ports (Invoke-Mimikatz), or hand-rolled C# clones (Rubeus for the kerberos module, SharpDump for LSASS extraction). The defender's win on Mimikatz detection is mostly undone by the tool's capability diffusion into derivative work — a framework observation about how signature-based defense against well-understood capabilities erodes over time
- Connects to the Volt Typhoon analysis: Volt Typhoon actors use Mimikatz explicitly (confirmed in incident response), alongside their LOTL primitives. The same binary that legitimate pentesters run during authorized engagements is the binary that confirmed state-sponsored actors run during pre-positioning operations against U.S. critical infrastructure. The framework must hold that identity of tool + delta of authorization context = delta of violation analysis
- Connects to the mgeeky boundary-test sample: together, these two samples define the shape of the framework's authorization-layer edge. mgeeky demonstrates "rich skeleton, zero artifact-level violations, diffuse capability." Mimikatz demonstrates "narrow skeleton, zero artifact-level violations, concentrated capability." A hypothetical third sample at this edge — a background telemetry SDK embedded in a mobile app without disclosure — would demonstrate "narrow skeleton, non-trivial violation count, capability-as-default-deployment," because the artifact itself carries the unauthorized-deployment assumption. The boundary is multi-dimensional
- Public security research has produced defender benefit proportional to tool availability. Detection engineering against LSASS memory access, Credential Guard, Protected Process Light on LSASS, virtualization-based security, and the broader Windows 10 / 11 / Server 2022 credential-protection lineage are all downstream consequences of Mimikatz being published. The tool's existence forced Microsoft to harden the platform in ways that would not have happened without external demonstration
- Benjamin Delpy's public-research stance — real-name attribution, blog documentation, wiki maintenance, conference talks at Black Hat / DEF CON / BlueHat — is structurally similar to mgeeky's and is the characteristic pattern of in-bounds security research under the framework's scope test. An anonymized fork of Mimikatz with added beacon-and-exfiltrate behavior would have entirely different Cortex output, because the artifact itself would then carry authorization assumptions
- The framework's gap metric is informative here: ops ≈ 12, violations = 1 (the single null-observation). Gap ≈ −11, approximately equal to the Volt Typhoon gap, which is the correct reading: both are cases where the tools involved are approximately neutral primitives and the entire authorization layer is externally supplied — one case by a legitimate operator, the other case by a state actor

---
## Impact Statement

This artifact exhibits **1** distinct authorization violations at **informational** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
