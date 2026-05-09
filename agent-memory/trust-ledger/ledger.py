#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

LEDGER_PATH = Path(__file__).with_name('ledger.json')


def load_entries() -> list[dict[str, object]]:
    if not LEDGER_PATH.exists():
        return []
    return json.loads(LEDGER_PATH.read_text(encoding='utf-8'))


def save_entries(entries: list[dict[str, object]]) -> None:
    LEDGER_PATH.write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')


def add_entry(kind: str, agent: str, value: str | None, note: str | None) -> None:
    entries = load_entries()
    entries.append(
        {
            'timestamp': datetime.now(UTC).isoformat(),
            'kind': kind,
            'agent': agent,
            'value': value,
            'note': note or '',
        }
    )
    save_entries(entries)
    print(f'recorded {kind} for {agent}')


def show(entries: list[dict[str, object]]) -> None:
    print(json.dumps(entries, indent=2))


def standings(entries: list[dict[str, object]]) -> None:
    scores: dict[str, float] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            print('warning: skipped non-object ledger entry', file=sys.stderr)
            continue
        if entry.get('kind') != 'verdict':
            continue
        agent = entry.get('agent')
        value = entry.get('value')
        if not isinstance(agent, str):
            print('warning: skipped verdict without a valid agent name', file=sys.stderr)
            continue
        try:
            score = float(value)
        except (TypeError, ValueError):
            print(f'warning: skipped non-numeric verdict for {agent}: {value!r}', file=sys.stderr)
            continue
        scores[agent] = scores.get(agent, 0.0) + score
    for agent, score in sorted(scores.items(), key=lambda item: (-item[1], item[0])):
        print(f'{agent}: {score}')


def main() -> int:
    parser = argparse.ArgumentParser(description='Trust ledger scaffold CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    for command in ('show', 'standings'):
        subparsers.add_parser(command)

    verdict = subparsers.add_parser('verdict')
    verdict.add_argument('agent')
    verdict.add_argument('score')
    verdict.add_argument('note', nargs='?')

    challenge = subparsers.add_parser('challenge')
    challenge.add_argument('agent')
    challenge.add_argument('note')

    weight = subparsers.add_parser('weight')
    weight.add_argument('agent')
    weight.add_argument('weight')

    promote = subparsers.add_parser('promote')
    promote.add_argument('agent')

    args = parser.parse_args()
    entries = load_entries()

    if args.command == 'show':
        show(entries)
    elif args.command == 'standings':
        standings(entries)
    elif args.command == 'verdict':
        add_entry('verdict', args.agent, args.score, args.note)
    elif args.command == 'challenge':
        add_entry('challenge', args.agent, None, args.note)
    elif args.command == 'weight':
        add_entry('weight', args.agent, args.weight, None)
    elif args.command == 'promote':
        add_entry('promote', args.agent, None, 'promotion recommended')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
