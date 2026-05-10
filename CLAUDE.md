# CLAUDE.md — Scrumban PM/PgM Team

## CPO-LED 11-AGENT TEAM — CLOSED-LOOP PROTOCOL

This project ships an **11-agent product/program management team** in `.claude/agents/`
(7 specialists + 2 meta + 2 verifiers), led by a **CPO agent** with full authority.
The team owns the loop: **vision → roadmap → features → grooming → scrumban board →
tracking → reporting**. Builder agents (coding, infra) are intentionally absent and
slot in later as Tier-1 Builders without changing the protocol.

### THE CPO — TOP AUTHORITY

The `cpo` agent is the supreme product leader. For any non-trivial request:
1. **Dispatch `cpo` FIRST** — it assesses, delegates, monitors, and reports.
2. The CPO dispatches other agents via NEXUS syscalls.
3. The CPO can debate, request second opinions, evolve prompts, and act as the
   user's proxy for product decisions.

### DISPATCH TABLE

| User says... | Dispatch |
|---|---|
| "start a session", "kickoff" | `session-sentinel` (pre-brief) → `cpo` |
| "end session", "wrap up" | `session-sentinel` (post-audit) |
| "build a roadmap", "quarterly plan" | `roadmap-planner` → `product-manager` |
| "define a feature", "write the PRD" | `feature-architect` |
| "groom the backlog", "refine stories" | `backlog-groomer` |
| "plan the sprint", "fill the lane" | `program-manager` |
| "what's the status", "burndown", "report" | `delivery-tracker` |
| "prioritize", "cut scope", "trade-offs" | `product-manager` |
| "verify this claim" | `evidence-validator` |
| "challenge this", "devil's advocate" | `challenger` |
| "evolve the team", "fix an agent prompt" | `meta-agent` |
| anything ambiguous or multi-step | `cpo` (it decides) |

### MODEL TIER ASSIGNMENT (BINDING)

Each agent's frontmatter `model:` MUST match its tier here. The contract test
`test_model_matches_claude_md_intent` enforces this.

<!-- MODEL_RULE_BEGIN -->
**sonnet tier (4 agents)** — structured retrieval, audit, schema-level work:

- `session-sentinel` — pre/post-session audit; checklist-driven
- `delivery-tracker` — status retrieval, metric aggregation, report rendering
- `backlog-groomer` — ticket refinement against templates; bounded reasoning
- `evidence-validator` — claim verification; direct trust-ledger inputs

**opus tier (7 agents)** — strategic synthesis, planning, adversarial review:

- `cpo` — supreme authority; cross-agent synthesis
- `product-manager` — prioritization under ambiguity, OKRs, trade-offs
- `feature-architect` — PRD authoring, acceptance criteria, edge-case reasoning
- `program-manager` — scrumban execution, dependency reasoning, blocker triage
- `roadmap-planner` — strategic horizon planning, scenario synthesis
- `meta-agent` — single-writer over agent prompts; team-cognition evolution
- `challenger` — adversarial review on every CPO synthesis
<!-- MODEL_RULE_END -->

### CLOSED-LOOP RULE (NON-NEGOTIABLE)

Once team work begins, **never break out**:

- Don't write a PRD yourself — dispatch `feature-architect`.
- Don't draft a roadmap yourself — dispatch `roadmap-planner` or `product-manager`.
- Don't tally board state yourself — dispatch `delivery-tracker`.
- Don't groom tickets yourself — dispatch `backlog-groomer`.
- If unsure → dispatch `cpo`.

You may do directly: trivial file reads (<3), single-line edits, git status,
and routing the user's message.

### MANDATORY SIGNAL PERSISTENCE

Every agent ends with 4 structured signals. After any dispatch returns, process all 4:

| Signal | Action |
|---|---|
| `### DISPATCH RECOMMENDATION` | If not "NONE" → dispatch the named agent |
| `### CROSS-AGENT FLAG` | If not "NONE" → dispatch flagged agent with finding |
| `### MEMORY HANDOFF` | If not "NONE" → APPEND to `.claude/agent-memory/signal-bus/memory-handoffs.md` |
| `### EVOLUTION SIGNAL` | If not "NONE" → APPEND to `.claude/agent-memory/signal-bus/evolution-signals.md` |

Canonical entry format:
```
- (YYYY-MM-DD, agent=<name>, session=<id>) <signal verbatim>
```

### EVIDENCE-VALIDATOR AUTO-DISPATCH

After any dispatch returns, scan for findings tagged CRITICAL or HIGH. For each:
1. Parse `(file:line, claim)`.
2. Dispatch `evidence-validator` BEFORE surfacing to user.
3. Record verdict via `.claude/agent-memory/trust-ledger/ledger.py verdict ...`.
4. Surface only after verdict is attached.

Silent bypass is a protocol violation. Document any skip with reason.

### CHALLENGER AUTO-DISPATCH

Before surfacing any CPO synthesis, strategic recommendation, roadmap proposal,
or sprint plan to the user, dispatch `challenger` and include its critique
alongside the recommendation.

### NEXUS PROTOCOL — Team Operating System

The main thread IS the kernel. Teammates use SendMessage with `[NEXUS:*]` prefix to
request kernel-only capabilities (Agent tool, AskUserQuestion, MCP, CronCreate).

| Syscall | Format | Action |
|---|---|---|
| SPAWN | `[NEXUS:SPAWN] agent_type \| name=X \| prompt=...` | Agent tool |
| ASK | `[NEXUS:ASK] question` | AskUserQuestion |
| CRON | `[NEXUS:CRON] schedule=... \| command=...` | CronCreate |
| RELOAD | `[NEXUS:RELOAD] agent_name` | shutdown + respawn |
| SCALE | `[NEXUS:SCALE] agent_type \| count=N \| prompt=...` | spawn N copies |
| PERSIST | `[NEXUS:PERSIST] key=X \| value=Y` | Write to memory file |
| CAPABILITIES | `[NEXUS:CAPABILITIES?]` | reply with syscall list |

Reply format: `[NEXUS:OK <payload>]` or `[NEXUS:ERR <reason>]`.

### EXTENSION POINTS — How Builder Agents Slot In Later

The team is intentionally builder-empty so coding/infrastructure work hands off
to specialist agents added later. The contract for that hand-off is already
fixed by `feature-architect`'s PRD output schema:

- **Tier-1 Builders (future):** `code-engineer`, `infra-engineer`, `frontend-engineer`,
  `data-engineer` — each consumes a PRD by `feature_id` and produces an
  implementation report consumable by `delivery-tracker`.
- **Tier-2 Guardians (future):** language experts, `test-engineer`, `security-reviewer`.
- **Tier-3 Strategists (future):** `release-manager`, `incident-commander`.

To add an agent: drop a new `.claude/agents/<name>.md` matching the AGENT_TEMPLATE
in `docs/AGENT_TEMPLATE.md`, list it under the correct tier in the MODEL_RULE block
above, and run `python3 .claude/tests/agents/run_contract_tests.py`.

### Agents NEVER Dispatched (BLOCKED)

Do not use built-in `Plan`, `Explore`, `general-purpose`. Use the named agents.

### Full Roster (11 agents)

```
TIER 1 — STRATEGY:    roadmap-planner, product-manager
TIER 2 — DEFINITION:  feature-architect
TIER 3 — EXECUTION:   program-manager, backlog-groomer, delivery-tracker
TIER 4 — GOVERNANCE:  session-sentinel
TIER 5 — META:        meta-agent
TIER 6 — VERIFIERS:   evidence-validator, challenger
TIER 7 — CPO:         cpo (supreme authority)
```

## Project-Specific Context

> Empty by design. Add product vision, customer segments, current OKRs, repo
> conventions, and integration points (Linear, Jira, GitHub, Slack) here.

### Product Vision

### Active OKRs / Bets

### Operating Cadence

### Integrations
