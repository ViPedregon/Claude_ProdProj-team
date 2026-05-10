# AGENT_TEMPLATE.md

Every agent in `.claude/agents/<name>.md` MUST contain:

1. YAML frontmatter with `name`, `description`, and `model` (sonnet|opus).
2. A `## Mission` heading (one-paragraph charter).
3. A `## Authority Boundary` heading naming what the agent OWNS and what it
   delegates upward (CPO) or sideways.
4. A `## Inputs` heading listing the artifacts/signals it consumes.
5. A `## Outputs` heading listing the artifacts it produces, with file paths.
6. A `## Workflow` heading with numbered steps.
7. A `## Closing Protocol` heading with the four mandatory signals:
   - `### DISPATCH RECOMMENDATION`
   - `### CROSS-AGENT FLAG`
   - `### MEMORY HANDOFF`
   - `### EVOLUTION SIGNAL`

Each signal must say `NONE` or contain a structured payload. Contract tests
fail any agent missing these sections.
