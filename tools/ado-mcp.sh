#!/usr/bin/env bash
# Launches the Azure DevOps MCP server (ado) for Claude Code with a PAT credential.
#
# Why: GUI-launched apps (Claude desktop from the Dock) do not read ~/.zshenv, so the
# ${PERSONAL_ACCESS_TOKEN} reference in .mcp.json reached the server unexpanded (-> 401).
# This wrapper resolves the credential itself; no secret lives in the repo.
#
# Credential order:
#   1. PERSONAL_ACCESS_TOKEN already in env (base64(":<PAT>"), e.g. set by ~/.zshenv)
#   2. macOS Keychain generic password, raw PAT; service name from ADO_PAT_KEYCHAIN_SERVICE
#      (default: nutriscan-ado-pat). Encoded here, because @azure-devops/mcp in pat mode
#      sends the value as the Basic credential as-is.
# Server arguments (org, domains, auth mode) stay in .mcp.json and are passed through.
set -euo pipefail

if [ -z "${PERSONAL_ACCESS_TOKEN:-}" ]; then
  service="${ADO_PAT_KEYCHAIN_SERVICE:-nutriscan-ado-pat}"
  if ! pat="$(/usr/bin/security find-generic-password -s "$service" -w 2>/dev/null)" || [ -z "$pat" ]; then
    echo "ado-mcp: no PERSONAL_ACCESS_TOKEN in env and no Keychain item '$service'" >&2
    exit 1
  fi
  PERSONAL_ACCESS_TOKEN="$(printf ':%s' "$pat" | base64 | tr -d '\n')"
  unset pat
  export PERSONAL_ACCESS_TOKEN
fi

exec npx -y "$@"
