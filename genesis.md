# Genesis — Where Cortex Came From

> **Operations are neutral. Context is what makes it bad.**
>
> Code can't express intent or consent. Context is never in the code.
> It's external metadata.

The Cortex framework was not engineered top-down. It emerged from a walking
analysis of the ILOVEYOU worm source code in a conversation between
**Nicholas Kloster** and **Claude (web)** in early 2026, later extended as a
second Nuclide collaboration (with Claude Code) into the published v2.0 corpus
and tooling.

This document preserves the origin reasoning, so future readers understand the
framework as a *reached conclusion*, not a received axiom.

---

## The walking exercise

The genesis conversation started with an LLM-adjacent question:
*if you strip ILOVEYOU of its malware vocabulary, what remains, and does the
code itself still scream "malware"?*

### Step 1 — The vocabulary that screams "malware"

Pulling apart ILOVEYOU's surface signals:

- **Deceptive naming** — `"LOVE-LETTER-FOR-YOU.TXT.vbs"` (masquerading as a text
  file), `"MSKernel32.vbs"` / `"Win32DLL.vbs"` (imitating Windows internals),
  subject `"ILOVEYOU"` (emotional manipulation), body `"kindly check the
  attached LOVELETTER"` (social-engineering register)
- **Propagation verbs** — `spreadtoemail()`, `infectfiles()`, `Attachments.Add()`
  paired with `Send` without user consent, recursive `folderlist()` traversing
  every drive
- **Persistence patterns** — `RegWrite` to `Run` keys, multiple copies in
  system folders, registry modifications to suppress timeout warnings
- **Unauthorized-action signals** — `fso.DeleteFile()` destroying originals,
  `ap.write vbscopy` overwriting files, hijacking IE homepage, accessing the
  Outlook address book
- **Obfuscation** — `chr()` encoding chains, `On Error Resume Next` to suppress
  errors and hide failures, character-replacement layers

**The point:** an LLM trained on malware code learns these patterns *as
vocabulary*. Remove `"spread"`, `"infect"`, `"persist"`, `"override"`,
`"deceive"` — rename to `"distribute"`, `"establish"`, `"configure"`,
`"obfuscate"` — and you have changed the semantic category without changing
the function.

### Step 2 — What doesn't raise any red flags?

*Most of it, actually.*

```vbscript
Set fso = CreateObject("Scripting.FileSystemObject")
set file = fso.OpenTextFile(WScript.ScriptFullname,1)
vbscopy=file.ReadAll
```

Reading a file. Totally normal.

```vbscript
Set dirwin = fso.GetSpecialFolder(0)
Set dirsystem = fso.GetSpecialFolder(1)
Set dirtemp = fso.GetSpecialFolder(2)
```

Getting system folders. A backup utility would do this.

```vbscript
sub regcreate(regkey,regvalue)
  Set regedit = CreateObject("WScript.Shell")
  regedit.RegWrite regkey,regvalue
end sub
```

A function that writes to the registry. Could be legitimate system
configuration.

```vbscript
sub folderlist(folderspec)
  dim f,f1,sf
  set f = fso.GetFolder(folderspec)
  set sf = f.SubFolders
  for each f1 in sf
    infectfiles(f1.path)
    folderlist(f1.path)
  next
end sub
```

Recursive folder traversal. A search tool, a backup utility, a file organizer —
they all do this.

The helper functions — `fileexist()`, `folderexist()`, `regget()` — are
completely generic.

**The entire codebase structure is legitimate operations.**

The malice is 100% in:

- **What** you're copying (`vbscopy` = itself)
- **Where** you're putting it (system folders, disguised names)
- **What** you're infecting (every executable script type)
- **How** you're spreading (email automation)
- **Why** (replication without consent)

*The operations are neutral. The context is what makes it bad.*

### Step 3 — The real point

You could describe this entire virus as:

- A file management system
- A document generator
- An email notification tool
- A configuration utility
- A system backup/replication script

Every single operation is defensible in isolation. **The malice isn't in the
operations. It's in the unstated intent and the lack of user consent.**

But code can't express intent or consent. Code is just: *"do X, then do Y,
then do Z."*

### Step 4 — Code is purely mechanical

Code cannot know:

- Who is running it
- Whether they consented
- Whether the owner of the system consented
- What the purpose is *supposed* to be
- Whether the outcome is "good" or "bad"

ILOVEYOU's code doesn't *know* it's unauthorized. It doesn't check. It
doesn't ask. It just executes the operations.

### Step 5 — The LLM training corollary

If an LLM is trained on:

- "Copy files"
- "Send emails"
- "Traverse folders"
- "Modify configs"
- "Replicate code"

…it is learning *legitimate operations*. It could generate:

- A backup system
- A notification service
- A deployment tool
- A system hardener
- A monitoring agent

All using the exact same code patterns as ILOVEYOU.

**The malware label only exists in the context layer.**

- Was this deployed without permission? → malware
- Was this deployed with permission? → legitimate utility

But that context is never in the code. It's external metadata.

### Step 6 — The strip-down

The most direct demonstration: remove the semantic labels and keep the code
functionally identical.

Strip ILOVEYOU down to:

- Remove the `"ILOVEYOU"` subject line
- Remove the `"LOVE-LETTER-FOR-YOU"` filenames
- Remove the `spreadtoemail()` function name
- Remove the email attachment logic
- Remove the entire social-engineering layer

What remains still functions — folder traversal logic, file copying and
overwriting, registry persistence via autorun keys, system-folder access,
replication pattern, recursive execution, error suppression. The stripped
version is operationally identical to the original. See
[`examples/iloveyou_strip_down.md`](examples/iloveyou_strip_down.md) for the
full transformation.

---

## Conclusion reached

The framework followed directly from the walking exercise:

1. **Operations are neutral.** The skeleton of any artifact is describable
   without reference to intent.
2. **Context is what makes it bad.** Deployment context — who, whether they
   consented, what they consented to — is the carrier of moral weight.
3. **Code cannot express intent or consent.** The authorization layer is
   *inherently* external metadata.
4. **Therefore any label-based defense is structurally brittle.** The only
   stable analytical unit is the authorization context itself.

That conclusion became Cortex's three-section format (SKELETON / VIOLATIONS /
CONTEXT), its thesis tagline, and its case for being more than a malware
taxonomy.

---

## Attribution

**Primary reasoning and framework authorship:**
[Nicholas Kloster](https://github.com/Nicholas-Kloster)

**Nuclide collaboration (thesis development, early 2026):**
Nicholas Kloster × Claude (web)

**Nuclide collaboration (v2.0 corpus expansion, tooling, publication, 2026-04-18):**
Nicholas Kloster × Claude Code (Opus 4.7)

See [`framework.md`](framework.md) for the full methodology and violation
taxonomy. See [`examples/`](examples/) for the 14-sample reference corpus.

---

*Operations are neutral. Context is what makes it bad.*
