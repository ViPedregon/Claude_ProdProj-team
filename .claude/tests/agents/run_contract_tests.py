#!/usr/bin/env python3
"""Contract tests for the scrumban PM/PgM team.

Validates every .claude/agents/*.md file against a fixed set of contracts.
Run on every commit and at session start.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = ROOT / ".claude" / "agents"
CLAUDE_MD = ROOT / "CLAUDE.md"

REQUIRED_SECTIONS = [
    "## Mission",
    "## Authority Boundary",
    "## Inputs",
    "## Outputs",
    "## Workflow",
    "## Closing Protocol",
    "### DISPATCH RECOMMENDATION",
    "### CROSS-AGENT FLAG",
    "### MEMORY HANDOFF",
    "### EVOLUTION SIGNAL",
]
ALLOWED_MODELS = {"sonnet", "opus"}  # haiku reserved (see CLAUDE.md)

def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm

def parse_model_rule(claude_md_text):
    m = re.search(r"<!-- MODEL_RULE_BEGIN -->(.*?)<!-- MODEL_RULE_END -->", claude_md_text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    tier_for = {}
    current_tier = None
    for line in block.splitlines():
        tm = re.match(r"\*\*(sonnet|opus|haiku) tier", line)
        if tm:
            current_tier = tm.group(1); continue
        am = re.match(r"-\s+`([a-z0-9-]+)`", line)
        if am and current_tier:
            tier_for[am.group(1)] = current_tier
    return tier_for

def main():
    failures = []
    if not AGENTS_DIR.is_dir():
        print(f"FAIL: missing {AGENTS_DIR}"); return 1
    tier_for = parse_model_rule(CLAUDE_MD.read_text() if CLAUDE_MD.exists() else "")
    agents = sorted(p for p in AGENTS_DIR.glob("*.md"))
    if not agents:
        print("FAIL: no agents found"); return 1
    for path in agents:
        name = path.stem
        text = path.read_text()
        fm = parse_frontmatter(text)
        if fm is None:
            failures.append((name, "missing frontmatter")); continue
        # frontmatter contracts
        for key in ("name", "description", "model"):
            if key not in fm:
                failures.append((name, f"frontmatter missing {key}"))
        if fm.get("name") != name:
            failures.append((name, f"frontmatter name {fm.get('name')!r} != filename"))
        if fm.get("model") not in ALLOWED_MODELS:
            failures.append((name, f"model {fm.get('model')!r} not in {ALLOWED_MODELS}"))
        if fm.get("model") == "haiku":
            failures.append((name, "haiku reserved"))
        # tier alignment
        expected_tier = tier_for.get(name)
        if expected_tier and fm.get("model") != expected_tier:
            failures.append((name, f"model {fm.get('model')!r} != CLAUDE.md tier {expected_tier!r}"))
        # required sections
        for sec in REQUIRED_SECTIONS:
            if sec not in text:
                failures.append((name, f"missing section {sec!r}"))
        # closing protocol comes last
        if "## Closing Protocol" in text:
            tail = text.split("## Closing Protocol", 1)[1]
            for s in ["### DISPATCH RECOMMENDATION","### CROSS-AGENT FLAG","### MEMORY HANDOFF","### EVOLUTION SIGNAL"]:
                if s not in tail:
                    failures.append((name, f"closing-protocol missing {s!r}"))

    contracts_per_agent = 12
    total = len(agents) * contracts_per_agent
    if failures:
        print(f"FAIL: {len(failures)} contract failures across {len(agents)} agents")
        for name, msg in failures:
            print(f"  - {name}: {msg}")
        return 1
    print(f"PASS: {len(agents)} agents × {contracts_per_agent} contracts = {total} assertions")
    return 0

if __name__ == "__main__":
    sys.exit(main())
