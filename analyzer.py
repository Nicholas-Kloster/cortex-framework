#!/usr/bin/env python3
"""
Cortex — Authorization Context Analyzer
========================================
Parses structured markdown analyses into SKELETON / VIOLATIONS / CONTEXT
and emits JSON + human-readable reports (markdown, optional HTML).

Core insight: Code is label-agnostic. The gap between what code *does*
and what it *assumes the right to do* is the real defense surface.
"""

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from html import escape as html_escape
from pathlib import Path


# ---------------------------------------------------------------------------
# BANNER
# ---------------------------------------------------------------------------

VERSION = "2.0"

_BANNER_ART = r"""
   ____ ___  ____ _____ _______  __
  / ___/ _ \|  _ \_   _| ____\ \/ /
 | |  | | | | |_) || | |  _|  \  /
 | |__| |_| |  _ < | | | |___ /  \
  \____\___/|_| \_\|_| |_____/_/\_\
"""

_BANNER_TAGLINE = "  authorization context analyzer"
_BANNER_THESIS = "  code is label-agnostic · authorization is the defense surface"


def print_banner(stream=sys.stderr, force: bool = False) -> None:
    """Print the banner to `stream` if it's a TTY and colors aren't disabled.

    Honors the NO_COLOR convention (https://no-color.org).
    Prints to stderr by default so stdout piping remains clean.
    Pass force=True to print even when the stream is not a TTY.
    """
    if not force and not stream.isatty():
        return

    use_color = stream.isatty() and "NO_COLOR" not in os.environ \
        and os.environ.get("TERM") != "dumb"
    if use_color:
        BOLD = "\033[1m"
        WHITE = "\033[97m"
        DIM = "\033[90m"
        RED = "\033[91m"
        RESET = "\033[0m"
    else:
        BOLD = WHITE = DIM = RED = RESET = ""

    for line in _BANNER_ART.strip("\n").splitlines():
        stream.write(f"{BOLD}{WHITE}{line}{RESET}\n")
    stream.write(f"{DIM}{_BANNER_TAGLINE}{RESET}"
                 f"{RED}{'':>18}v{VERSION}{RESET}\n")
    stream.write(f"{DIM}{_BANNER_THESIS}{RESET}\n\n")


# ---------------------------------------------------------------------------
# PARSING
# ---------------------------------------------------------------------------

SECTION_ALIASES = {
    "skeleton": {"skeleton"},
    "violations": {"violations", "authorization violations"},
    "context": {"context", "context that makes it bad", "bad context"},
}

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.+?)\s*$")


def _normalize_header(text: str) -> str:
    return re.sub(r"[^a-z ]", "", text.strip().lower()).strip()


def _classify_section(header: str) -> str | None:
    norm = _normalize_header(header)
    for key, aliases in SECTION_ALIASES.items():
        if norm in aliases:
            return key
    return None


@dataclass
class Analysis:
    analysis_name: str
    source_file: str
    analyzed_at: str
    skeleton: list = field(default_factory=list)
    violations: list = field(default_factory=list)
    context: list = field(default_factory=list)
    analysis_summary: dict = field(default_factory=dict)
    parse_warnings: list = field(default_factory=list)


def parse_markdown(filepath: Path) -> Analysis:
    raw = filepath.read_text(encoding="utf-8")

    title_match = TITLE_RE.search(raw)
    title = title_match.group(1).strip() if title_match else filepath.stem

    buckets: dict[str, list[str]] = {"skeleton": [], "violations": [], "context": []}
    found_sections: set[str] = set()
    current: str | None = None

    for raw_line in raw.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        h2 = H2_RE.match(line)
        if h2:
            current = _classify_section(h2.group(1))
            if current:
                found_sections.add(current)
            continue

        bullet = BULLET_RE.match(line)
        if bullet and current:
            buckets[current].append(bullet.group(1).strip())

    warnings: list[str] = []
    for section in ("skeleton", "violations", "context"):
        if section not in found_sections:
            warnings.append(f"Section '{section}' not found in document.")
        elif not buckets[section]:
            warnings.append(f"Section '{section}' found but contains no bullet items.")

    summary = _build_summary(buckets)

    return Analysis(
        analysis_name=title,
        source_file=str(filepath),
        analyzed_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        skeleton=buckets["skeleton"],
        violations=buckets["violations"],
        context=buckets["context"],
        analysis_summary=summary,
        parse_warnings=warnings,
    )


# ---------------------------------------------------------------------------
# SUMMARY / SEVERITY
# ---------------------------------------------------------------------------

def _build_summary(buckets: dict[str, list[str]]) -> dict:
    ops = len(buckets["skeleton"])
    viol = len(buckets["violations"])
    ctx = len(buckets["context"])
    gap = viol - ops

    if viol <= 1:
        severity = "informational"
    else:
        score = viol + (ctx * 0.5)
        if score >= 10:
            severity = "critical"
        elif score >= 6:
            severity = "high"
        elif score >= 3:
            severity = "medium"
        else:
            severity = "low"

    return {
        "total_operations": ops,
        "total_violations": viol,
        "total_context_notes": ctx,
        "skeleton_violation_gap": gap,
        "severity": severity,
    }


SEVERITY_BADGES = {
    "critical": "🔴 Critical",
    "high": "🔴 High",
    "medium": "🟠 Medium",
    "low": "🟡 Low",
    "informational": "⚪ Informational",
}


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

def validate(a: Analysis) -> tuple[bool, list[str]]:
    errors = []
    for section in ("skeleton", "violations", "context"):
        if not getattr(a, section):
            errors.append(f"Missing or empty section: {section.upper()}")
    return (not errors), errors


# ---------------------------------------------------------------------------
# OUTPUT: JSON
# ---------------------------------------------------------------------------

def write_json(a: Analysis, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(a)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"[JSON]   → {output_path}")


# ---------------------------------------------------------------------------
# OUTPUT: MARKDOWN REPORT
# ---------------------------------------------------------------------------

def render_markdown_report(a: Analysis) -> str:
    s = a.analysis_summary
    sev = s["severity"]
    sev_badge = SEVERITY_BADGES.get(sev, sev)

    pair_count = max(len(a.skeleton), len(a.violations))
    sk = a.skeleton + [""] * (pair_count - len(a.skeleton))
    vi = a.violations + [""] * (pair_count - len(a.violations))

    lines: list[str] = []
    lines.append("# Cortex Analysis Report")
    lines.append(f"**Subject:** {a.analysis_name}  ")
    lines.append(f"**Analyzed:** {a.analyzed_at}  ")
    lines.append(f"**Source:** `{a.source_file}`")
    lines.append("")
    lines.append("---")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Section    | Items |")
    lines.append("|------------|-------|")
    lines.append(f"| SKELETON   | {s['total_operations']} |")
    lines.append(f"| VIOLATIONS | {s['total_violations']} |")
    lines.append(f"| CONTEXT    | {s['total_context_notes']} |")
    lines.append("")
    lines.append(f"**Authorization Violation Severity:** {sev_badge}  ")
    lines.append(f"**Skeleton → Violation gap:** {s['skeleton_violation_gap']:+d} "
                 "(positive = more assumed rights than observed operations)")
    lines.append("")
    lines.append("---")
    lines.append("## Skeleton vs. Violations")
    lines.append("")
    lines.append("> The gap between what code *does* and what it *assumes the right to do* "
                 "is the attack surface.")
    lines.append("")
    lines.append("| # | What the code does (Skeleton) | What it assumes the right to do (Violation) |")
    lines.append("|---|-------------------------------|---------------------------------------------|")
    for i, (a_sk, a_vi) in enumerate(zip(sk, vi), 1):
        sk_c = a_sk.replace("|", "\\|") if a_sk else "—"
        vi_c = a_vi.replace("|", "\\|") if a_vi else "—"
        lines.append(f"| {i} | {sk_c} | {vi_c} |")
    lines.append("")
    lines.append("---")
    lines.append("## [SKELETON] — What It Actually Does")
    lines.append("")
    lines.append("> Functional operations, divorced from intent, vocabulary, or context.")
    lines.append("")
    for item in a.skeleton:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("## [VIOLATIONS] — Authorization Gaps")
    lines.append("")
    lines.append("> What does this assume the right to do without explicit consent or validation?")
    lines.append("")
    for item in a.violations:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("## [CONTEXT] — Why the Violations Matter")
    lines.append("")
    lines.append("> Impact, deception, unauthorized access, intent.")
    lines.append("")
    for item in a.context:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("## Impact Statement")
    lines.append("")
    lines.append(_impact_statement(a))
    lines.append("")

    if a.parse_warnings:
        lines.append("---")
        lines.append("## ⚠ Parse Warnings")
        for w in a.parse_warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def _impact_statement(a: Analysis) -> str:
    s = a.analysis_summary
    v = s["total_violations"]
    if v == 0:
        return ("No authorization violations cataloged. The skeleton and the owner's "
                "consent boundary appear to coincide.")
    return (
        f"This artifact exhibits **{v}** distinct authorization violations at "
        f"**{s['severity']}** severity. The gap between what the code technically does "
        f"(the skeleton) and what the system owner actually consented to is the entire "
        f"attack surface. Operations that look benign in isolation become hostile when "
        f"executed without the owner's knowledge, intent, or ability to refuse."
    )


def write_report(a: Analysis, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(a), encoding="utf-8")
    print(f"[REPORT] → {output_path}")


# ---------------------------------------------------------------------------
# OUTPUT: HTML REPORT
# ---------------------------------------------------------------------------

HTML_CSS = """
:root { color-scheme: dark; }
body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; max-width: 960px;
       margin: 2rem auto; padding: 0 1rem; background:#0d1117; color:#e6edf3; }
h1, h2 { border-bottom:1px solid #30363d; padding-bottom:.3rem; }
code, pre { background:#161b22; padding:.1rem .3rem; border-radius:4px; }
table { border-collapse: collapse; width:100%; margin: 1rem 0; }
th, td { border:1px solid #30363d; padding:.5rem .6rem; vertical-align: top; text-align:left; }
th { background:#161b22; }
blockquote { color:#8b949e; border-left:3px solid #30363d; margin:.5rem 0; padding:.2rem .8rem; }
.sev-critical { color:#ff6b6b; font-weight:700; }
.sev-high     { color:#ff6b6b; font-weight:700; }
.sev-medium   { color:#ffb86c; font-weight:600; }
.sev-low      { color:#f1fa8c; }
.sev-informational { color:#6272a4; }
.meta { color:#8b949e; font-size:.9rem; }
ul li { margin:.2rem 0; }
"""


def render_html_report(a: Analysis) -> str:
    s = a.analysis_summary
    sev = s["severity"]

    def li(items):
        return "\n".join(f"    <li>{html_escape(i)}</li>" for i in items) or "    <li><em>(none)</em></li>"

    pair_count = max(len(a.skeleton), len(a.violations))
    sk = a.skeleton + [""] * (pair_count - len(a.skeleton))
    vi = a.violations + [""] * (pair_count - len(a.violations))
    rows = "\n".join(
        f"      <tr><td>{i}</td><td>{html_escape(x) or '—'}</td><td>{html_escape(y) or '—'}</td></tr>"
        for i, (x, y) in enumerate(zip(sk, vi), 1)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html_escape(a.analysis_name)} — Cortex Report</title>
<style>{HTML_CSS}</style>
</head>
<body>
  <h1>Cortex Analysis Report</h1>
  <p class="meta"><strong>Subject:</strong> {html_escape(a.analysis_name)}<br>
  <strong>Analyzed:</strong> {html_escape(a.analyzed_at)}<br>
  <strong>Source:</strong> <code>{html_escape(a.source_file)}</code></p>

  <h2>Summary</h2>
  <ul>
    <li>Severity: <span class="sev-{sev}">{html_escape(SEVERITY_BADGES.get(sev, sev))}</span></li>
    <li>Operations (skeleton): {s['total_operations']}</li>
    <li>Authorization violations: {s['total_violations']}</li>
    <li>Context notes: {s['total_context_notes']}</li>
    <li>Skeleton → Violation gap: {s['skeleton_violation_gap']:+d}</li>
  </ul>

  <h2>Skeleton vs. Violations</h2>
  <blockquote>The gap between what code <em>does</em> and what it <em>assumes the right to do</em> is the attack surface.</blockquote>
  <table>
    <thead><tr><th>#</th><th>Skeleton</th><th>Violation</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>

  <h2>[SKELETON] — What It Actually Does</h2>
  <ul>
{li(a.skeleton)}
  </ul>

  <h2>[VIOLATIONS] — Authorization Gaps</h2>
  <ul>
{li(a.violations)}
  </ul>

  <h2>[CONTEXT] — Why the Violations Matter</h2>
  <ul>
{li(a.context)}
  </ul>

  <h2>Impact Statement</h2>
  <p>{html_escape(_impact_statement(a))}</p>
</body>
</html>
"""


def write_html(a: Analysis, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html_report(a), encoding="utf-8")
    print(f"[HTML]   → {output_path}")


# ---------------------------------------------------------------------------
# COMPARE
# ---------------------------------------------------------------------------

def _term_width() -> int:
    try:
        return max(shutil.get_terminal_size((100, 24)).columns, 60)
    except Exception:
        return 100


def compare_analyses(a: Analysis, b: Analysis) -> None:
    width = _term_width()
    col = max((width - 8) // 2, 30)
    divider = "=" * width

    print()
    print(divider)
    print("COMPARISON")
    print(f"  A: {a.analysis_name}")
    print(f"  B: {b.analysis_name}")
    print(divider)

    sections = [
        ("skeleton", "SKELETON"),
        ("violations", "VIOLATIONS"),
        ("context", "CONTEXT"),
    ]

    for key, label in sections:
        a_items = getattr(a, key)
        b_items = getattr(b, key)
        print(f"\n--- {label} ---")
        print(f"  A ({len(a_items)} items)".ljust(col + 4) + f"| B ({len(b_items)} items)")
        max_len = max(len(a_items), len(b_items), 1)
        for i in range(max_len):
            lhs = a_items[i] if i < len(a_items) else "—"
            rhs = b_items[i] if i < len(b_items) else "—"
            for j, (l, r) in enumerate(zip(_wrap(lhs, col), _wrap(rhs, col))):
                prefix = f"  [{i+1}] " if j == 0 else "      "
                print(f"{prefix}{l.ljust(col)} | {r}")

    print(f"\n--- SUMMARY ---")
    sa, sb = a.analysis_summary, b.analysis_summary
    print(f"  severity:     {sa['severity']:<20} | {sb['severity']}")
    print(f"  ops:          {sa['total_operations']:<20} | {sb['total_operations']}")
    print(f"  violations:   {sa['total_violations']:<20} | {sb['total_violations']}")
    print(f"  context:      {sa['total_context_notes']:<20} | {sb['total_context_notes']}")
    print(f"  sk→vi gap:    {sa['skeleton_violation_gap']:<+20} | {sb['skeleton_violation_gap']:+d}")
    print()


def _wrap(text: str, width: int) -> list[str]:
    if not text:
        return [""]
    out, cur = [], ""
    for word in text.split():
        if len(cur) + 1 + len(word) <= width:
            cur = (cur + " " + word).strip()
        else:
            if cur:
                out.append(cur)
            cur = word if len(word) <= width else word[:width]
    if cur:
        out.append(cur)
    return out or [""]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_analyze(args: argparse.Namespace) -> int:
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return 1

    print(f"\nAnalyzing: {filepath.name}")
    a = parse_markdown(filepath)

    ok, errors = validate(a)
    if not ok:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  - {e}")
        if not args.force:
            print("Use --force to output anyway.")
            return 1

    stem = filepath.stem
    out_dir = Path(args.output_dir) if args.output_dir else Path("output/reports")
    json_path = Path(args.json) if args.json else out_dir / f"{stem}.json"
    report_path = Path(args.report) if args.report else out_dir / f"{stem}_report.md"

    write_json(a, json_path)
    write_report(a, report_path)

    if args.html:
        html_path = Path(args.html) if isinstance(args.html, str) else out_dir / f"{stem}_report.html"
        write_html(a, html_path)

    if a.parse_warnings:
        print(f"\n⚠  {len(a.parse_warnings)} parse warning(s):")
        for w in a.parse_warnings:
            print(f"   - {w}")

    s = a.analysis_summary
    print(f"\nDone. {s['total_operations']} ops / {s['total_violations']} violations / "
          f"severity={s['severity']}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return 1

    a = parse_markdown(filepath)
    ok, errors = validate(a)

    if ok:
        print(f"✓ {filepath.name} — valid Cortex analysis format")
        if a.parse_warnings:
            for w in a.parse_warnings:
                print(f"  ⚠ {w}")
        return 0
    print(f"✗ {filepath.name} — validation failed:")
    for e in errors:
        print(f"  - {e}")
    return 1


def cmd_compare(args: argparse.Namespace) -> int:
    f1, f2 = Path(args.file1), Path(args.file2)
    for f in (f1, f2):
        if not f.exists():
            print(f"ERROR: File not found: {f}", file=sys.stderr)
            return 1
    compare_analyses(parse_markdown(f1), parse_markdown(f2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cortex",
                                description="Cortex — Authorization Context Analyzer")
    p.add_argument("--version", action="version", version=f"cortex {VERSION}")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress the startup banner")
    p.add_argument("--banner", action="store_true",
                   help="Force the banner to print even when stderr is not a TTY")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("analyze", help="Parse and report on a markdown analysis")
    a.add_argument("file", help="Input markdown file")
    a.add_argument("--json", help="JSON output path")
    a.add_argument("--report", help="Markdown report output path")
    a.add_argument("--html", nargs="?", const=True, default=False,
                   help="Also emit HTML report (optionally specify path)")
    a.add_argument("--output-dir", help="Output directory (default: output/reports)")
    a.add_argument("--force", action="store_true", help="Output even if validation fails")

    v = sub.add_parser("validate", help="Validate markdown file structure")
    v.add_argument("file", help="Input markdown file")

    c = sub.add_parser("compare", help="Compare two analyses side-by-side")
    c.add_argument("file1", help="First markdown file")
    c.add_argument("file2", help="Second markdown file")

    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.banner:
        print_banner(stream=sys.stderr, force=True)
    elif not args.quiet:
        print_banner(stream=sys.stderr)
    return {
        "analyze": cmd_analyze,
        "validate": cmd_validate,
        "compare": cmd_compare,
    }[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
