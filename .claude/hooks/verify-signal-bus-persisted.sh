#!/usr/bin/env bash
# SubagentStop hook — warns when non-NONE signals appear in the agent's tail
# but no edits to memory-handoffs.md / evolution-signals.md were observed.
set -u
TAIL="${CLAUDE_AGENT_OUTPUT_TAIL:-}"
[[ -z "$TAIL" ]] && exit 0
if grep -qE "^### MEMORY HANDOFF" <<<"$TAIL" && ! grep -qE "^NONE\$" <<<"$TAIL"; then
  echo "warn: MEMORY HANDOFF emitted — confirm signal-bus/memory-handoffs.md was updated." >&2
fi
if grep -qE "^### EVOLUTION SIGNAL" <<<"$TAIL" && ! grep -qE "^NONE\$" <<<"$TAIL"; then
  echo "warn: EVOLUTION SIGNAL emitted — confirm signal-bus/evolution-signals.md was updated." >&2
fi
exit 0
