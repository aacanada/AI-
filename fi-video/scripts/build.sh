#!/usr/bin/env bash
# Rebuild index.html + captions from timing.json, then carve the music bed under the narration.
# Needs @hyperframes/core for the carve: set HF_CORE to a dir containing node_modules/@hyperframes/core.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_index.py
CARVE="${HF_SKILLS:-$HOME/.claude/skills}/hyperframes-audio/scripts/carve.mjs"
node "$CARVE" --comp index.html --bed bgm --voice narration ${HF_CORE:+--core "$HF_CORE"}
