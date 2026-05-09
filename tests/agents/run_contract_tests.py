#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = sorted((ROOT / 'agents').glob('*.md'))

assertion_count = 0


def check(condition: bool, message: str) -> None:
    global assertion_count
    assertion_count += 1
    if not condition:
        raise AssertionError(message)


if len(AGENTS) != 31:
    raise AssertionError(f'expected 31 agents, found {len(AGENTS)}')
for agent_path in AGENTS:
    name = agent_path.stem
    title = name.replace('-', ' ').title()
    text = agent_path.read_text(encoding='utf-8')
    memory_path = ROOT / 'agent-memory' / name / 'MEMORY.md'

    check(text.startswith('---\n'), f'{name}: missing opening frontmatter fence')
    check('\n---\n\n# ' in text, f'{name}: missing closing frontmatter fence')
    check(f'name: {name}\n' in text, f'{name}: name mismatch')
    check('role: scaffold-placeholder\n' in text, f'{name}: missing scaffold role')
    check(f'memory_path: ../agent-memory/{name}/MEMORY.md\n' in text, f'{name}: memory path mismatch')
    check('version: 0.1.0\n' in text, f'{name}: missing version field')
    check(f'# {title}\n' in text, f'{name}: missing title heading')
    check('## Mission\n' in text, f'{name}: missing mission section')
    check('## Operating Protocol\n' in text, f'{name}: missing operating protocol section')
    check('## Outputs\n' in text, f'{name}: missing outputs section')
    check(memory_path.is_file(), f'{name}: missing memory scaffold')

expected_assertions = 31 * 11
print(f'contract tests passed: {assertion_count}/{expected_assertions} assertions')
