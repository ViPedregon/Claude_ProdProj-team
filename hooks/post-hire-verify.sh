#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
agent_name="${1:-}"
if [[ -z "$agent_name" ]]; then
  printf "post-hire-verify: agent name required\n" >&2
  exit 1
fi
[[ -f "$SCRIPT_DIR/../agents/${agent_name}.md" ]]
[[ -f "$SCRIPT_DIR/../agent-memory/${agent_name}/MEMORY.md" ]]
printf "post-hire-verify: %s verified\n" "$agent_name"
