# Scrumban PM/PgM Team

A scaled-down, **product- and program-management-focused** sibling to the parent
31-agent system. Eleven agents own the loop from product vision through
sprint-level delivery; builder agents (coding, infra) slot in as a later layer.

## What it does

- **Vision → Roadmap.** `roadmap-planner` and `product-manager` produce a
  versioned `ROADMAP.md` with horizons, bets, and sequencing.
- **Feature definition.** `feature-architect` turns roadmap items into PRDs
  with acceptance criteria and a machine-readable `feature_id` schema.
- **Backlog grooming.** `backlog-groomer` refines stories to "Ready" against a
  Definition-of-Ready template; sizes them; flags dependencies.
- **Scrumban board.** `program-manager` runs the WIP-limited board, plans
  cadence cycles, triages blockers, and orchestrates dependency hand-offs.
- **Tracking & reporting.** `delivery-tracker` produces stand-up notes,
  burnup/cumulative-flow snapshots, and stakeholder-ready status reports.
- **Governance.** `session-sentinel` audits protocol; `evidence-validator`
  gates HIGH-severity claims; `challenger` adversarially reviews CPO synthesis.
- **Self-evolution.** `meta-agent` is the single writer of agent prompts and
  applies lessons from `signal-bus/evolution-signals.md`.

## Layout

```
scrumban-pm-team/
├── CLAUDE.md
├── README.md
├── settings.json
├── .claude/
│   ├── agents/                       # 11 agent prompts
│   ├── hooks/                        # protocol enforcement + NEXUS log
│   ├── tests/agents/                 # contract tests
│   └── agent-memory/
│       ├── signal-bus/               # cross-agent signal log
│       ├── trust-ledger/             # per-agent accuracy + ledger CLI
│       ├── roadmap/ROADMAP.md        # canonical roadmap
│       ├── backlog/BACKLOG.md        # canonical backlog
│       ├── board/BOARD.md            # canonical scrumban board
│       └── reports/                  # status snapshots
└── docs/AGENT_TEMPLATE.md            # required structure for any new agent
```

## Quickstart

1. Run from a Claude Code session whose working directory is this folder.
2. Say one of:
   - "start a session" → triggers `session-sentinel` then `cpo`
   - "build a Q3 roadmap targeting [outcome]" → routes through `roadmap-planner`
   - "define the feature for [problem]" → routes through `feature-architect`
   - "plan this sprint" → routes through `program-manager`
   - "what's our delivery status?" → routes through `delivery-tracker`

## Verifying

```bash
python3 .claude/tests/agents/run_contract_tests.py
```

All agents × contracts must pass. Pre-commit hook runs this on staged agent edits.

## Extending into builders

Drop new agents under `.claude/agents/`, list them under the correct tier in
`CLAUDE.md`'s `MODEL_RULE` block, and rerun the contract tests. The PRD output
contract from `feature-architect` is already shaped for builder consumption.
