#!/bin/sh
# 장면·자막·오디오 생성 후 BGM 덕킹(carve)까지 한 번에
set -e
cd "$(dirname "$0")/.."
node scripts/gen.mjs
node ../../.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html
