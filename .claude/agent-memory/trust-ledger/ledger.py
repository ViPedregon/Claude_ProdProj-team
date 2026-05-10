#!/usr/bin/env python3
"""Minimal trust ledger CLI for the scrumban PM/PgM team."""
import argparse, json, os, sys
from pathlib import Path

LEDGER = Path(__file__).parent / "ledger.json"
VERDICTS = ["CONFIRMED", "PARTIALLY_CONFIRMED", "REFUTED", "UNVERIFIABLE"]
OUTCOMES = ["ACCEPT", "REVISE", "REJECT"]

def load():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text() or "{}")
    return {}

def save(d):
    LEDGER.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")

def ensure(d, agent):
    d.setdefault(agent, {
        "verdicts": {v: 0 for v in VERDICTS},
        "challenges": {o: 0 for o in OUTCOMES},
        "weight": 0.5,
    })
    return d[agent]

def recompute_weight(rec):
    v = rec["verdicts"]; c = rec["challenges"]
    v_total = sum(v.values()) or 1
    c_total = sum(c.values()) or 1
    # Bayesian-ish blend: confirmed + partial credit, minus refuted; accept minus reject.
    v_score = (v["CONFIRMED"] + 0.5 * v["PARTIALLY_CONFIRMED"] - v["REFUTED"]) / v_total
    c_score = (c["ACCEPT"] - c["REJECT"]) / c_total
    raw = 0.5 + 0.35 * v_score + 0.15 * c_score
    rec["weight"] = max(0.0, min(1.0, raw))

def cmd_verdict(args):
    d = load(); rec = ensure(d, args.agent)
    if args.verdict not in VERDICTS:
        sys.exit(f"unknown verdict: {args.verdict}")
    rec["verdicts"][args.verdict] += 1
    recompute_weight(rec); save(d)
    print(f"recorded: {args.agent} verdict={args.verdict} weight={rec['weight']:.3f}")

def cmd_challenge(args):
    d = load(); rec = ensure(d, args.agent)
    if args.outcome not in OUTCOMES:
        sys.exit(f"unknown outcome: {args.outcome}")
    rec["challenges"][args.outcome] += 1
    recompute_weight(rec); save(d)
    print(f"recorded: {args.agent} challenge={args.outcome} weight={rec['weight']:.3f}")

def cmd_show(args):
    d = load(); rec = d.get(args.agent)
    if not rec:
        sys.exit(f"no record for {args.agent}")
    print(json.dumps(rec, indent=2, sort_keys=True))

def cmd_weight(args):
    d = load(); rec = d.get(args.agent)
    print(f"{rec['weight']:.3f}" if rec else "0.500")

def cmd_standings(args):
    d = load()
    rows = sorted(d.items(), key=lambda kv: kv[1]["weight"], reverse=True)
    for name, rec in rows:
        print(f"{rec['weight']:.3f}  {name}")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("verdict"); s.add_argument("--agent", required=True); s.add_argument("--finding-id", required=False); s.add_argument("--verdict", required=True); s.set_defaults(fn=cmd_verdict)
    s = sub.add_parser("challenge"); s.add_argument("--agent", required=True); s.add_argument("--rec-id", required=False); s.add_argument("--outcome", required=True); s.set_defaults(fn=cmd_challenge)
    s = sub.add_parser("show"); s.add_argument("--agent", required=True); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("weight"); s.add_argument("--agent", required=True); s.set_defaults(fn=cmd_weight)
    s = sub.add_parser("standings"); s.set_defaults(fn=cmd_standings)
    args = p.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
