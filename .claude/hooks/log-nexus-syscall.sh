#!/usr/bin/env bash
# PostToolUse hook (matcher: SendMessage). Appends NEXUS syscalls to the log.
set -u
MSG="${CLAUDE_TOOL_ARGS_MESSAGE:-}"
TO="${CLAUDE_TOOL_ARGS_TO:-}"
FROM="${CLAUDE_AGENT_NAME:-unknown}"
[[ "$MSG" == \[NEXUS:* ]] || exit 0
SYSCALL=$(awk -F'[][:]' '{print $3}' <<<"$MSG")
TS=$(date -u +"%Y-%m-%d %H:%M")
echo "- ($TS, agent=$FROM, to=$TO, syscall=$SYSCALL) $MSG" >> .claude/agent-memory/signal-bus/nexus-log.md
exit 0
