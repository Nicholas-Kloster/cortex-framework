# Cortex Analysis Report
**Subject:** ILOVEYOU Worm (2000) — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.045563Z  
**Source:** `examples/iloveyou.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 10 |
| VIOLATIONS | 9 |
| CONTEXT    | 9 |

**Authorization Violation Severity:** 🔴 Critical  
**Skeleton → Violation gap:** -1 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Arrives as email attachment named `LOVE-LETTER-FOR-YOU.TXT.vbs` | Assumes right to read the user's entire contact list without asking |
| 2 | Executes as VBScript when opened by user | Assumes right to send email as the user to all contacts without notification or consent |
| 3 | Reads Windows Address Book to enumerate contacts | Assumes right to traverse and read any file on any mounted drive |
| 4 | Sends copy of itself to all discovered contacts via Outlook | Assumes right to permanently overwrite and destroy user files (photos, music, scripts) |
| 5 | Traverses local drives searching for files by extension | Assumes right to persist across reboots via registry modification without disclosure |
| 6 | Overwrites files matching target extensions (.jpg, .jpeg, .mp3, .mp2, .css, .js, .vbs, .vbe, .jse, .wsh, .sct, .hta, .bat, .com, .ht) with copy of itself | Assumes right to download and execute arbitrary remote code |
| 7 | Renames overwritten files with `.vbs` extension appended | Assumes right to modify browser configuration |
| 8 | Modifies registry to set itself as startup executable | Zero authorization checks at any step — no prompts, confirmations, or scope limits |
| 9 | Downloads additional payload from remote URL (via IRC channel) | Impersonates a legitimate personal message to obtain initial execution |
| 10 | Sets Internet Explorer start page to payload download URL | — |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Arrives as email attachment named `LOVE-LETTER-FOR-YOU.TXT.vbs`
- Executes as VBScript when opened by user
- Reads Windows Address Book to enumerate contacts
- Sends copy of itself to all discovered contacts via Outlook
- Traverses local drives searching for files by extension
- Overwrites files matching target extensions (.jpg, .jpeg, .mp3, .mp2, .css, .js, .vbs, .vbe, .jse, .wsh, .sct, .hta, .bat, .com, .ht) with copy of itself
- Renames overwritten files with `.vbs` extension appended
- Modifies registry to set itself as startup executable
- Downloads additional payload from remote URL (via IRC channel)
- Sets Internet Explorer start page to payload download URL

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- Assumes right to read the user's entire contact list without asking
- Assumes right to send email as the user to all contacts without notification or consent
- Assumes right to traverse and read any file on any mounted drive
- Assumes right to permanently overwrite and destroy user files (photos, music, scripts)
- Assumes right to persist across reboots via registry modification without disclosure
- Assumes right to download and execute arbitrary remote code
- Assumes right to modify browser configuration
- Zero authorization checks at any step — no prompts, confirmations, or scope limits
- Impersonates a legitimate personal message to obtain initial execution

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- Operates entirely against the owner's intent — no legitimate user wants files overwritten
- Destruction is permanent: overwritten files cannot be recovered without backup
- Propagation uses the victim's social trust to infect contacts — recipients believe it is from a known person
- Estimated 50 million infections in 10 days; estimated $10 billion in damages
- Contact list exfiltration exposes PII of third parties who never consented
- Remote code download creates an unbounded attack surface — any payload could be retrieved
- Registry persistence means damage continues across reboots without user awareness
- File overwriting disguised as extension rename — deceptive even in its destructive mechanism
- Executed in user context but operates with no user-defined authorization scope

---
## Impact Statement

This artifact exhibits **9** distinct authorization violations at **critical** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
