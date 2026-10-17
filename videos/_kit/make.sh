#!/usr/bin/env bash
# Shared: bash ../_kit/make.sh  (run from a project dir) → music bed fitted to the film, index.html, voiceover carve.
set -euo pipefail
TOTAL=$(python3 -c "import json;print(json.load(open('timing.json'))['total'])")
# loop the track if it is shorter than the film, fade out the last 2.5 s, trim to length
ffmpeg -y -v error -stream_loop 2 -i assets/bgm/bgm.mp3 -af "afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print(max(0,$TOTAL-2.5))"):d=2.5" \
  -t "$TOTAL" -ar 48000 -ac 2 assets/bgm/bed.wav
python3 tools/build.py
[ -d node_modules/@hyperframes/core ] || npm i -D --no-audit --no-fund @hyperframes/core >/dev/null 2>&1
node ../../.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music-bed --voice narration ${CARVE_ARGS:-}
