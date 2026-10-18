#!/usr/bin/env bash
# Facecam cut: bash tools/make_facecam.sh (run from the project dir, after python3 tools/facecam_edl.py)
# → music bed fitted to the film, facecam.html + graphics.html, voiceover carve on the bed.
set -euo pipefail
TOTAL=$(python3 -c "import json;print(json.load(open('timing-facecam.json'))['total'])")
ffmpeg -y -v error -stream_loop 2 -i assets/bgm/bgm.mp3 -af "afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print(max(0,$TOTAL-2.5))"):d=2.5" \
  -t "$TOTAL" -ar 48000 -ac 2 assets/bgm/bed-facecam.wav
python3 tools/build_facecam.py
[ -d node_modules/@hyperframes/core ] || npm i -D --no-audit --no-fund @hyperframes/core >/dev/null 2>&1
node ../../.claude/skills/hyperframes-audio/scripts/carve.mjs --comp facecam.html --bed music-bed --voice narration ${CARVE_ARGS:-}
