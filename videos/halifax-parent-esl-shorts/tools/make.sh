#!/usr/bin/env bash
# Rebuild index.html from timing.json and re-apply the BGM voiceover carve (build.py overwrites it).
# Full pipeline: python3 tools/tts.py [--force] → python3 tools/retime.py → bash tools/make.sh → render
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build.py
node ../../.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music-bed --voice narration
