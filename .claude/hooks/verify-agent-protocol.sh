#!/usr/bin/env bash
# SubagentStop hook — best-effort check that the subagent's transcript ended
# with the four required protocol sections. Non-fatal warning by design.
set -u
TRANSCRIPT_TAIL="${CLAUDE_AGENT_OUTPUT_TAIL:-}"
[[ -z "$TRANSCRIPT_TAIL" ]] && exit 0
required=("DISPATCH RECOMMENDATION" "CROSS-AGENT FLAG" "MEMORY HANDOFF" "EVOLUTION SIGNAL")
missing=0
for section in "${required[@]}"; do
  grep -qE "^### $section" <<<"$TRANSCRIPT_TAIL" || { echo "warn: missing closing-protocol section: $section" >&2; missing=1; }
done
exit 0
