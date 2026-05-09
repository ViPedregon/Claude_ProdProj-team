#!/usr/bin/env bash
set -euo pipefail
log_path="${NEXUS_SYSCALL_LOG:-/tmp/claude-nexus-syscalls.log}"
printf "%s %s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$log_path"
