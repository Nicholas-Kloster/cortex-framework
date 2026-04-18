# Cortex Analysis Report
**Subject:** Phishing / 419 Advance-Fee Scam (as a class) — Authorization Context Analysis  
**Analyzed:** 2026-04-18T17:14:59.259953Z  
**Source:** `examples/phishing_419_scam.md`

---
## Summary

| Section    | Items |
|------------|-------|
| SKELETON   | 4 |
| VIOLATIONS | 11 |
| CONTEXT    | 11 |

**Authorization Violation Severity:** 🔴 Critical  
**Skeleton → Violation gap:** +7 (positive = more assumed rights than observed operations)

---
## Skeleton vs. Violations

> The gap between what code *does* and what it *assumes the right to do* is the attack surface.

| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |
|---|-------------------------------|---------------------------------------------|
| 1 | Attacker composes and sends a single unsolicited email (or SMS, or DM) to a recipient whose address was obtained from a breach dump, scraping, or purchased list | Assumes right to contact the recipient at all, despite having no prior relationship, consent, or legitimate business |
| 2 | The message presents a scripted narrative (Nigerian prince in political exile, inheritance recovery, lottery winnings, fictitious invoice, package-delivery failure, tax refund, compromised account alert, CEO urgent wire request, fake job offer, romance contact) | Assumes right to impersonate a person, a business, a government agency, a bank, a courier, a romantic partner, or a family member without their consent or knowledge |
| 3 | The message requests one of: (a) a reply, (b) a click on an attacker-controlled link, (c) opening an attachment, (d) transfer of funds, (e) purchase of gift cards, (f) sharing of an MFA code or credential | Assumes right to manufacture an urgency or fear or hope state in the recipient for purposes of bypassing the recipient's normal judgment |
| 4 | No exploitation of a software vulnerability; no malware required for the primary attack path; the execution context is the recipient's reading, cognition, and decision-making | Assumes right to solicit funds, credentials, MFA codes, personal identifying information, or account access on false pretenses |
| 5 | — | Assumes right to induce the recipient to take action against their own interests, their employer's interests, or their family's interests, including actions with permanent financial consequence |
| 6 | — | Assumes right to conduct the operation at global scale against millions of recipients simultaneously, selecting those whose life circumstances (bereavement, loneliness, financial pressure, new employment, recent loss) make them disproportionately likely to respond |
| 7 | — | Assumes right to re-engage successful victims repeatedly, a pattern known as "re-victimization" in which a responsive victim is re-scripted into further payments indefinitely |
| 8 | — | Assumes right to operate from jurisdictions whose law-enforcement cooperation with the victim's jurisdiction is weak or nonexistent, effectively immunizing the attacker from consequence |
| 9 | — | Assumes right to treat the recipient's personal data (email address, name, sometimes phone number or more) as an input commodity, trading breach dumps and target lists among operator networks as ordinary commerce |
| 10 | — | Assumes right to cause collateral harm to third parties named in impersonation scripts (the real bank whose name is used, the real courier whose brand is copied, the real executive whose voice is cloned, the deceased relative whose name is invoked) |
| 11 | — | Assumes right to exploit the structural feature that the global email system has no enforceable sender-identity requirement, and the structural feature that attention and credulity are not defended resources at any layer of the stack |

---
## [SKELETON] — What It Actually Does

> Functional operations, divorced from intent, vocabulary, or context.

- Attacker composes and sends a single unsolicited email (or SMS, or DM) to a recipient whose address was obtained from a breach dump, scraping, or purchased list
- The message presents a scripted narrative (Nigerian prince in political exile, inheritance recovery, lottery winnings, fictitious invoice, package-delivery failure, tax refund, compromised account alert, CEO urgent wire request, fake job offer, romance contact)
- The message requests one of: (a) a reply, (b) a click on an attacker-controlled link, (c) opening an attachment, (d) transfer of funds, (e) purchase of gift cards, (f) sharing of an MFA code or credential
- No exploitation of a software vulnerability; no malware required for the primary attack path; the execution context is the recipient's reading, cognition, and decision-making

---
## [VIOLATIONS] — Authorization Gaps

> What does this assume the right to do without explicit consent or validation?

- Assumes right to contact the recipient at all, despite having no prior relationship, consent, or legitimate business
- Assumes right to impersonate a person, a business, a government agency, a bank, a courier, a romantic partner, or a family member without their consent or knowledge
- Assumes right to manufacture an urgency or fear or hope state in the recipient for purposes of bypassing the recipient's normal judgment
- Assumes right to solicit funds, credentials, MFA codes, personal identifying information, or account access on false pretenses
- Assumes right to induce the recipient to take action against their own interests, their employer's interests, or their family's interests, including actions with permanent financial consequence
- Assumes right to conduct the operation at global scale against millions of recipients simultaneously, selecting those whose life circumstances (bereavement, loneliness, financial pressure, new employment, recent loss) make them disproportionately likely to respond
- Assumes right to re-engage successful victims repeatedly, a pattern known as "re-victimization" in which a responsive victim is re-scripted into further payments indefinitely
- Assumes right to operate from jurisdictions whose law-enforcement cooperation with the victim's jurisdiction is weak or nonexistent, effectively immunizing the attacker from consequence
- Assumes right to treat the recipient's personal data (email address, name, sometimes phone number or more) as an input commodity, trading breach dumps and target lists among operator networks as ordinary commerce
- Assumes right to cause collateral harm to third parties named in impersonation scripts (the real bank whose name is used, the real courier whose brand is copied, the real executive whose voice is cloned, the deceased relative whose name is invoked)
- Assumes right to exploit the structural feature that the global email system has no enforceable sender-identity requirement, and the structural feature that attention and credulity are not defended resources at any layer of the stack

---
## [CONTEXT] — Why the Violations Matter

> Impact, deception, unauthorized access, intent.

- Introduces a violation class not yet in the corpus: *cognitive-surface targeting under pure social engineering*. Every prior sample used some technical primitive; this sample uses zero. The target is the recipient's attention and judgment, and the attack surface is defended only by the recipient's skepticism — a resource that erodes under stress, fatigue, loneliness, or urgency
- Positive skeleton-to-violation gap is the framework-level teaching move: a single operation (send message) claims a dozen distinct authorizations. The framework correctly surfaces that the attacker's claimed authority is radically disproportionate to the observable action
- Connects this sample to SUNBURST's *identity-layer forgery*: the phishing email manufactures an identity claim the recipient cannot cryptographically verify. The delta is that SUNBURST forges tokens inside a protocol designed to enforce identity, while phishing forges identity in a protocol (email) that never promised to
- Global scale: FBI IC3 reports tens of billions of dollars in annual losses from business email compromise and romance scams alone; total phishing / social-engineering fraud is estimated to exceed all ransomware losses combined
- Victim harm is not recoverable in the way technical compromise is: there is no "patch and restore" for elderly victims whose retirement savings have been extracted over months of romance fraud, or for employees fired after falling for a CEO-impersonation wire request
- The violation is concentrated on whoever is already most vulnerable: recent bereavement, cognitive decline, isolation, financial distress, immigration uncertainty, first-job inexperience — the attacker's targeting logic optimizes for response rate, which correlates with the recipient's reduced ability to scrutinize
- Re-victimization is the definitional pattern: responsive targets receive escalating scripts, additional operators, and cross-referred pitches. The violation compounds over the victim's lifetime in a way no single message foreshadows
- Law-enforcement response is structurally poor: the attacker operates from one jurisdiction, the platform from a second, the victim in a third, the funds laundered through a fourth. No institution has end-to-end responsibility, and the marginal cost of attempting another victim is near zero
- Connects to the *pretense violation* class (NotPetya, prompt injection): the phishing message lies about what it is. It claims to be from a bank, a prince, a courier, a colleague, a lover. The violation is the categorization fraud, executed in natural language, at scale
- Cortex-level implication: the framework was initially intuitive on malware (which performs many operations and claims many rights) and on tool repositories (which perform many operations and claim none). Phishing is the third shape: few operations, many claimed rights. This completes the dimensional picture — the framework holds across *operation-rich / right-rich* (worms), *operation-rich / right-empty* (tools), and *operation-poor / right-rich* (social engineering) cases
- Historical provenance: "advance-fee fraud" predates the internet by more than a century. The "Spanish prisoner" confidence trick (17th century onward) uses the identical authorization-claim structure as the Nigerian-prince email, which is itself predated by fax-based and letter-based variants. The technical medium changes; the violation class is invariant. This is further evidence that the framework's unit of analysis (authorization context) is correctly chosen — it generalizes across media because authorization is a property of the consent relationship, not of the delivery layer

---
## Impact Statement

This artifact exhibits **11** distinct authorization violations at **critical** severity. The gap between what the code technically does (the skeleton) and what the system owner actually consented to is the entire attack surface. Operations that look benign in isolation become hostile when executed without the owner's knowledge, intent, or ability to refuse.
