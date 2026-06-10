#!/usr/bin/env bash
set -euo pipefail

plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_root="${STORYTELLING_MEDIA_MCP_ROOT:-}"

if [[ -n "$repo_root" && -f "$repo_root/pyproject.toml" ]]; then
  cd "$repo_root"
  if [[ -x "$repo_root/.venv/bin/python" ]]; then
    exec "$repo_root/.venv/bin/python" -m storytelling_mcp
  fi
  exec python -m storytelling_mcp
fi

data_dir="${STORYTELLING_MEDIA_MCP_DATA_DIR:-${CLAUDE_PLUGIN_DATA:-${CODEX_PLUGIN_DATA:-$plugin_root/.plugin-data}}}"
venv_dir="$data_dir/venv"

if [[ ! -x "$venv_dir/bin/python" ]]; then
  python3 -m venv "$venv_dir"
fi

if ! "$venv_dir/bin/python" -c "import storytelling_mcp" >/dev/null 2>&1; then
  "$venv_dir/bin/python" -m pip install --quiet \
    "git+https://github.com/imyousuf/storytelling-media-mcp.git"
fi

exec "$venv_dir/bin/python" -m storytelling_mcp
