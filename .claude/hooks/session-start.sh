#!/bin/bash
# Cloud (Claude Code on the web) setup: node deps, ffmpeg, map/texture data.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR"
npm install --no-audit --no-fund >/dev/null 2>&1 || npm install
if ! command -v ffmpeg >/dev/null 2>&1; then
  pip install -q imageio-ffmpeg >/dev/null 2>&1 || true
  FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || true)
  if [ -n "$FF" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then echo "export FFMPEG_PATH=$FF" >> "$CLAUDE_ENV_FILE"; fi
  export FFMPEG_PATH="$FF"
fi
node tools/fetch-data.mjs || echo "fetch-data failed (network?) - run: npm run setup"
