# Trust Ledger

Per-agent accuracy scorecard. Updated by `evidence-validator` verdicts and
`challenger` outcomes. CPO uses weights to break ties during synthesis.

## CLI

```
python3 ledger.py verdict   --agent <name> --finding-id <id> --verdict CONFIRMED|PARTIALLY_CONFIRMED|REFUTED|UNVERIFIABLE
python3 ledger.py challenge --agent <name> --rec-id <id> --outcome ACCEPT|REVISE|REJECT
python3 ledger.py show      --agent <name>
python3 ledger.py weight    --agent <name>
python3 ledger.py standings
```

## Schema

`ledger.json`:
```
{
  "<agent>": {
    "verdicts": {"CONFIRMED": N, "PARTIALLY_CONFIRMED": N, "REFUTED": N, "UNVERIFIABLE": N},
    "challenges": {"ACCEPT": N, "REVISE": N, "REJECT": N},
    "weight": 0.0–1.0
  }
}
```
