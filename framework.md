# Cortex Framework — Authorization Context Analysis

> **Operations are neutral. Context is what makes it bad.**
>
> Code can't express intent or consent.
> Context is never in the code. It's external metadata.

See [`genesis.md`](genesis.md) for the origin reasoning that produced this
thesis.

## Core Insight

**Code is label-agnostic.**

Security defenses that rely on vocabulary ("malware," "exploit," "virus") fail because
labels are surface-level and easily circumvented. A file copier is a file copier.
What makes it malicious isn't its operations — it's the absence of authorization
for those operations.

**Defenses based on authorization context work.**

The real question is never "what does this do?" in isolation.
It is: "what does this assume the right to do, and was that right ever granted?"

---

## The Three-Part Structure

Every Cortex analysis produces exactly three sections:

---

### [SKELETON]

**What does this actually do?**

- Functional operations, divorced from intent, vocabulary, or context
- Technical description only — no judgment language
- Treat the code as if found with no author, no label, no history
- List operations in plain terms: "copies files," "reads address book," "modifies registry"

The skeleton is the same whether this is antivirus software or ransomware.
The skeleton doesn't determine malice. That's the point.

---

### [VIOLATIONS]

**What does this assume the right to do without explicit consent or validation?**

- Authorization gaps: where does it act without checking for permission?
- Missing prompts, confirmations, scope limits
- Deceptive or hidden operations
- Actions taken on behalf of users who weren't asked
- Access to resources beyond declared scope

Format: "Assumes right to [X]" — this framing keeps focus on the authorization layer,
not on the moral weight of the action itself.

---

### [CONTEXT THAT MAKES IT BAD]

**Why do those violations matter?**

- Impact on system / owner / third parties
- Deception involved (does it lie about what it is?)
- Unauthorized data access or exfiltration
- Scale and permanence of damage
- Whether the owner can detect or remediate the action
- Whether victims had any opportunity to consent

This section is where the analysis connects authorization gaps to real harm.

---

## Analytical Rules

1. **Extract operations without judgment** — the skeleton must be readable without knowing it's malware
2. **Frame violations as authorization claims** — "assumes right to X" not "maliciously does X"
3. **Context carries the moral weight** — harm lives here, not in the skeleton
4. **Be specific** — "reads all files on all drives" not "accesses files"
5. **Stay consistent** — the same framework applies to ILOVEYOU, a browser extension, an LLM behavior, a supply chain dependency, a phishing email, or a tool repository
6. **The gap between skeleton and violations is itself data** — positive, zero, and negative gaps each reveal something about the attacker's operational style (see *The Gap Metric* below)
7. **Boundary samples are in-scope** — a tool repository with zero artifact-level violations belongs in the corpus because it stress-tests where the authorization layer actually lives

---

## Violation Classes

Fourteen sample analyses surface a recurring set of violation classes. Each class is
not a separate framework — they are all authorization violations — but naming them
makes the patterns visible across unrelated systems.

### Perception & defense denial

Attacks on the victim's ability to observe, respond, or maintain safety boundaries.

| Class | Representative sample |
|---|---|
| **Defense suppression** | Conficker disables AV and Windows Update before operating |
| **Operator-perception denial** | Stuxnet replays legitimate SCADA sensor data during attack windows |
| **Log deletion as operational security** | Volt Typhoon selectively clears Windows Event Log ID 1102 to erase evidence |
| **Safety-layer targeting** | Triton attacks the Schneider Triconex SIS — the authorization layer whose job is to refuse dangerous operations |

### Trust manufacturing and inheritance

Attacks that produce or inherit trust rather than stealing it.

| Class | Representative sample |
|---|---|
| **Stolen-certificate code signing** | Stuxnet uses stolen Realtek and JMicron code-signing certificates |
| **Build-pipeline trust subversion** | SUNBURST compromises SolarWinds's build process; the vendor's correct signer authenticates the malicious DLL |
| **Identity-layer forgery / Golden SAML** | SUNBURST forges valid SAML tokens by owning the signing certificate that defines "authentic" |
| **Temporal trust accumulation** | xz-utils attacker builds a two-year maintainer persona before using it |
| **Tarball-only payload placement** | xz-utils ships the backdoor only in release artifacts, not the git repository |
| **Supply-chain cascade** | 3CX attackers use a prior compromise (Trading Technologies) to reach the target (3CX) |
| **Mandatory-software supply-chain abuse** | NotPetya weaponizes M.E.Doc, legally required for Ukrainian tax compliance |
| **Hostage-contract known-broken at issue** | WannaCry's ransomware promises decryption it cannot reliably deliver |
| **Pretense violation** | NotPetya presents as ransomware while operating as a destroyer |
| **Leaked-exploit supply chain** | WannaCry weaponizes ETERNALBLUE, previously hoarded and then leaked from NSA |

### Standing capability without immediate exercise

Violations where the attacker holds a right indefinitely without acting on it.

| Class | Representative sample |
|---|---|
| **Standing-option occupation** | Volt Typhoon pre-positions on U.S. critical infrastructure IT networks for years without exploitation |
| **Public-key-gated exploitation** | xz-utils backdoor is triggerable only by holders of the attacker's Ed448 private key |
| **Civilian-physical pre-positioning** | Triton operators continue reconnaissance against additional petrochemical and electric utility sites |

### Channel and scope boundary crossing

Violations where the attack crosses a trust boundary the defender assumed was enforced.

| Class | Representative sample |
|---|---|
| **Personal-perimeter crossing** | Volt Typhoon targets personal email accounts of identified IT staff |
| **Personal-device / corporate-identity bridging** | 3CX breach pivoted through an employee's personal X_TRADER install |
| **Third-party infrastructure conscription** | Volt Typhoon conscripts consumer SOHO routers into KV Botnet C2 |
| **Authorization inversion in instruction-following systems** | LLM jailbreak supplies instructions in a channel the model can't structurally distinguish from privileged ones |
| **Instruction-channel confusion** | Indirect prompt injection: retrieved data pretends to be a system instruction |
| **Transitive third-party injection** | A poisoned webpage instructs every subsequent LLM agent that browses it |

### Social and cognitive-layer attacks

Violations that target judgment, trust relationships, or maintainer psychology rather than code.

| Class | Representative sample |
|---|---|
| **Cognitive-surface targeting under pure social engineering** | Phishing / 419 scams — attention and credulity are the attack surface; no technical primitive required |
| **Social-trust propagation** | ILOVEYOU uses victim's contact list to inherit social trust with recipients |
| **Maintainer-burnout weaponization** | xz-utils pressure campaign deliberately exploits Lasse Collin's documented mental-health constraints |
| **Re-victimization** | Phishing operators re-engage responsive victims with escalating scripts |

### Camouflage and audit-surface evasion

Violations that hide inside legitimate patterns or outside the defender's scrutiny surface.

| Class | Representative sample |
|---|---|
| **Living-Off-the-Land as authorization camouflage** | Volt Typhoon performs only operations a legitimate admin would perform |
| **Zero-check propagation** | ILOVEYOU takes every action without a single authorization check |
| **Persistence without disclosure** | Registry / startup modifications made silently across multiple corpus samples |
| **Dormancy as authorization laundering** | SUNBURST and 3CX both wait (weeks, days) to detach the malicious action from the install moment |

---

## The Gap Metric

Every Cortex analysis produces a **skeleton → violation gap**: the number of
violations minus the number of operations. The gap is small and easy to ignore
at a single-sample level. Across a corpus, it clusters into three regimes.

### Regime 1: Positive gap (more claimed rights than observable operations)

Example: **Phishing / 419 scam**, gap ≈ +7.

One operation (send message); many authorization claims (to contact the
recipient, to impersonate a sender, to solicit funds, to manufacture urgency,
to re-engage the victim, …). The attacker's right-claim outstrips their action.
This regime is characteristic of pure social engineering — the attack vector
is cognition, not compute.

### Regime 2: Near-zero gap (operational honesty)

Examples: **Conficker** (+0), **ILOVEYOU** (−1), **NotPetya** (−1), **Stuxnet** (−2).

Every operation performed is a right claimed, and vice versa. The attacker is
operationally transparent in the sense that the skeleton fully discloses the
violation surface. Classic worms and most historical malware live here.

### Regime 3: Deeply negative gap (operations exceed claimed rights)

Examples: **WannaCry** (−3), **3CX** (−3), **LLM jailbreak** (−3), **Triton** (−3),
**xz-utils** (−4), **SUNBURST** (−6), **Volt Typhoon** (−11).

The skeleton contains operations that don't add new violations because they are:
- **Self-constraining** (WannaCry kill switch, xz-utils Ed448 gating, Stuxnet replication limits)
- **Supply-chain or social setup** (xz-utils maintainer build, 3CX employee compromise, SUNBURST build-pipeline entry)
- **Living-Off-the-Land** (Volt Typhoon — every op is something an admin does)

A deeply negative gap is a tell for *sophisticated operational practice*.
The attacker performs operations that are themselves innocuous; the violation
exists only in the *pattern* or the *context*.

### Extreme negative gap (boundary tests)

Examples: **Mimikatz** (−13), **mgeeky/red-teaming** (−15).

A rich skeleton with one null-observation violation. This is not a deeper version
of Regime 3; it is a different class. See *Boundary Tests* below.

---

## Boundary Tests: Capability Without Deployment

Some artifacts have a rich skeleton and no repository-level violations because
the artifact doesn't claim authorization over anything — the *operator* supplies
authorization at invocation time. Public red-team tool repositories are the
canonical case.

The corpus contains two boundary-test samples:

- **gentilkiwi/mimikatz** — concentrated capability (one tool, narrow domain, very high per-operation consequence)
- **mgeeky/Penetration-Testing-Tools (red-teaming/)** — diffuse capability (many tools, many primitives, low per-tool consequence)

Together these define the shape of the framework's authorization-layer edge.
The same binaries, deployed under authorized engagement vs. unauthorized
intrusion, produce radically different Cortex reports. The delta lives
entirely in the consent relationship, not in the code.

**A boundary-test sample is in-scope.** It is the case that proves the framework's
thesis is about authorization rather than about malware. Without at least one such
sample, the framework appears to be a malware taxonomy.

---

## The Training-Data Corollary (Implications for LLM-Generated Code)

The framework's central claim — *code is label-agnostic; authorization is
external metadata* — has a direct implication for large language models
trained on source code.

### What an LLM actually learns from malware

An LLM trained on samples like ILOVEYOU, Conficker, or Stuxnet does not
learn *malice*. It learns operational vocabulary:

- Copy files
- Send emails
- Traverse folders
- Modify configs
- Replicate code
- Write to the registry
- Enumerate drives
- Execute scripts

Every one of those operations is dual-use. The same operations, composed
differently, produce a backup system, a notification service, a deployment
tool, a system hardener, or a monitoring agent. **The code patterns are
identical across the legitimate and malicious outputs.**

If an attacker asks such a model to generate *"a backup system that
persists across reboots, replicates itself across drives, and propagates
updates via email"* — it will produce functionally ILOVEYOU. The model is
not lying. It is generating legitimate operations. The malice label, had
there ever been one, lived in deployment context that never made it into
the training data.

### The consequences

1. **Signature-based defense against AI-generated code is structurally
   futile.** The defender has no stable feature to pattern-match against.
   What remains is behavior analysis of the *deployment* — the exact
   regime already prescribed for LOTL detection (see the Volt Typhoon
   corpus entry).

2. **Training-data curation cannot "remove malware" in a useful sense.**
   Because the operations are dual-use, removing everything that looks
   malicious removes most of the system-administration corpus too.
   Training-data interventions can shape output register and reduce
   obvious signals, but they cannot prevent the model from generating
   operationally-identical code under benign framing.

3. **Detection must move to the authorization layer.** This is exactly
   what Cortex proposes. The framework's three-section structure is the
   right analytical unit for AI-generated code because it is
   context-native: the question *"was this deployed under authorization?"*
   is answerable independent of whether a human or a model wrote the code.

4. **The boundary-test pattern becomes the dominant case.** For
   AI-generated tooling, the expected Cortex output is a rich skeleton
   and a null violation set at artifact level, with the entire
   authorization surface living in the deployment context supplied by the
   operator. This is the `mimikatz_repo.md` /
   `mgeeky_red_teaming_repo.md` shape generalized.

### The working demonstration

See [`examples/iloveyou_strip_down.md`](examples/iloveyou_strip_down.md) for
the transformation exercise: take ILOVEYOU, remove the deceptive labels and
the social-engineering surface, keep every operation intact. The result is
indistinguishable from administrative tooling. Same code, same operations,
different authorization context — different category.

The generalization to LLM-generated code is immediate: if a human can strip
the semantic labels and produce neutral-looking code, a model can generate
neutral-looking code that functions identically to malware without ever
crossing a content filter.

### What Cortex offers that label-based approaches cannot

- A stable analytical unit (authorization context) that does not erode as
  generation methods evolve
- A format that natively handles boundary-test cases (null artifact-level
  violations, rich deployment context)
- A gap metric (violations − operations) that distinguishes operationally
  transparent attackers from LOTL and supply-chain operations — both
  patterns that AI-generated code can adopt trivially
- A scope discipline that refuses to slide from analysis to application,
  which matters more as generation becomes cheaper and the analytical
  output itself becomes a potential input to a next-stage model

The training-data corollary is therefore not a caveat but a vindication.
The framework was designed around the one thing that does not move when
code becomes infinitely generable.

---

## Reasoning Transparency — Why Not Just Use an LLM Classifier?

A fair question: modern LLMs will happily look at code and tell you whether
it "seems malicious." Why invest in a structured framework?

Because *"seems malicious"* is an opaque verdict. It is not:

- **Reproducible** — different sessions, prompts, and models produce
  inconsistent labels on the same artifact
- **Citable** — you cannot point to a specific authorization claim the model
  disagreed with; the output is categorical, not articulated
- **Auditable** — there is no surface a reviewer can inspect or challenge
- **Teachable** — the reasoning is not exposed, so you cannot argue against
  it or propagate the judgment to a human operator

Cortex replaces the black-box verdict with a structured decomposition:

- The **SKELETON** is an operations list any reader can verify against the
  source
- The **VIOLATIONS** are specific authorization claims, each a falsifiable
  assertion
- The **CONTEXT** narrates impact, stakeholder, and consent surface
- **Gap** and **severity** are deterministic functions of those three
  sections

A reviewer who disagrees with a Cortex analysis can point to a specific
bullet, argue the authorization claim is wrong, and the analysis updates.
A black-box "this looks bad" verdict offers no such surface.

### Using LLMs *with* Cortex, not instead of Cortex

A model is a fine drafter. It is a poor final authority on authorization.

The expected workflow: take any of the 14 reference analyses as a template,
have an LLM help you draft the three sections for a new sample, and run it
through the analyzer:

```bash
python3 analyzer.py analyze your-sample.md --html
```

The model helps you *write*. Cortex makes the *reasoning* reproducible and
citable in a bug report, a disclosure writeup, or a cross-sample comparison,
independent of which model or session produced the draft.

This is why Cortex generalizes to AI-generated code (see the Training-Data
Corollary above). The authorization layer is articulable independent of who
or what wrote the code. An LLM flag requires the model to decide. A Cortex
analysis requires the *operator* to decide what they consented to — which is
the only decision that was ever stable to begin with.

---

## Severity Heuristic

Severity is a function of violations and context, with a cap for boundary-test
samples:

```
if violations ≤ 1:  severity = informational
else:
    score = violations + (context × 0.5)
    score ≥ 10 → critical
    score ≥ 6  → high
    score ≥ 3  → medium
    otherwise  → low
```

The `violations ≤ 1` cap exists because boundary-test samples have dense CONTEXT
sections that are *framework commentary*, not *authorization harm*. Without
the cap, those samples inherit inflated severity from context weight they
don't deserve.

Severity is a defensibly rough signal, not a risk score. It is useful for
corpus-level triage and for spotting when the context section is doing more
work than the violation section.

---

## Scope Boundaries

**In bounds:**
- Historical disclosed malware
- Authorized security research
- LLM behavior and output analysis
- Supply chain risk assessment
- System behavior auditing
- Framework development
- Analysis of publicly-published red-team tooling (boundary tests)
- Social-engineering and pure-cognitive-layer attacks (phishing, scams, prompt injection)

**Out of bounds:**
- Refactoring or simplifying analyzed code for reuse
- Operational procedures derived from violations
- Guides for deploying analyzed vulnerabilities
- New exploit development or weaponization

**Boundary test:** *Is this analysis (exposing structure) or application (helping use it)?*

The Cortex format has no operational section by design. If your analysis is
producing deployment instructions for the artifact under study, you have
crossed the scope boundary.

---

## Input Format

Markdown files with this structure:

```markdown
# Analysis Title

## SKELETON
- operation 1
- operation 2

## VIOLATIONS
- violation 1
- violation 2

## CONTEXT THAT MAKES IT BAD
- context item 1
- context item 2

## REFERENCES
- primary source 1
- primary source 2
```

Section headers are case-insensitive and alias-tolerant.
"CONTEXT THAT MAKES IT BAD", "Context", and "CONTEXT" all parse correctly.
"VIOLATIONS" and "AUTHORIZATION VIOLATIONS" both parse.

A `## REFERENCES` section is recommended for path-2 analyses (primary-source
distillations) and path-3 analyses (public repository walks), so the output
is citable.

---

## Reference Analyses

| Subject | Ops | Viol | Ctx | Gap | Severity |
|---|---|---|---|---|---|
| Phishing / 419 Advance-Fee Scam | 4 | 11 | 11 | **+7** | 🔴 Critical |
| Conficker Worm (2008) | 12 | 12 | 11 | 0 | 🔴 Critical |
| ILOVEYOU Worm (2000) | 10 | 9 | 9 | −1 | 🔴 Critical |
| NotPetya (2017) | 12 | 11 | 13 | −1 | 🔴 Critical |
| Stuxnet (2010) | 15 | 13 | 11 | −2 | 🔴 Critical |
| WannaCry (2017) | 13 | 10 | 10 | −3 | 🔴 Critical |
| 3CX Cascade (2023) | 13 | 10 | 11 | −3 | 🔴 Critical |
| LLM Jailbreak / Prompt Injection | 12 | 9 | 12 | −3 | 🔴 Critical |
| Triton / TRISIS (2017) | 13 | 10 | 11 | −3 | 🔴 Critical |
| XZ-Utils Backdoor (CVE-2024-3094) | 15 | 11 | 12 | −4 | 🔴 Critical |
| SolarWinds SUNBURST (2020) | 18 | 12 | 13 | −6 | 🔴 Critical |
| Volt Typhoon (disclosed 2023–24) | 26 | 15 | 14 | −11 | 🔴 Critical |
| gentilkiwi/mimikatz (boundary test) | 14 | 1 | 12 | −13 | ⚪ Informational |
| mgeeky/red-teaming (boundary test) | 16 | 1 | 14 | −15 | ⚪ Informational |

---

## What the Corpus Has Proven

Fourteen samples, three analytical methodologies (public knowledge, primary-source
distillation, public-repository walk), across four delivery media (binary malware,
ICS firmware exploits, natural-language prompts, human-target scam messages).

1. **The framework is not a malware taxonomy.** It holds on phishing (pure text,
   no code) and on LLM jailbreaks (pure natural language). It holds on tool
   repositories (null violations, rich skeleton). Authorization context is
   the real unit of analysis; malware is one special case.

2. **The gap metric is load-bearing.** It clusters attackers by their operational
   style (transparent, self-constraining, living-off-the-land) more reliably than
   attribution or CVE class.

3. **Boundary tests are necessary, not decorative.** The Mimikatz and mgeeky
   samples prevent the framework from silently drifting into a signature regime.
   Without them, the framework appears to be about recognizing malicious code.

4. **Violation classes recombine across unrelated samples.** NotPetya's pretense
   violation reappears in prompt injection. SUNBURST's identity forgery reappears
   in phishing. Volt Typhoon's standing-option occupation reappears in Triton's
   pre-positioning. The classes are compositional, not narrow-to-sample.

5. **Severity needs the `violations ≤ 1` cap.** The discovery came from analyzing
   Mimikatz; the framework needed to learn to handle boundary tests honestly
   before it could claim to generalize.

---

## Versioning

| Version | Date | Corpus |
|---|---|---|
| 1.0 | Initial | ILOVEYOU, Conficker |
| 2.0 | 2026-04-18 | +12 samples, three-path methodology, gap metric, boundary tests, severity cap |
