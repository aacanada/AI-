#!/usr/bin/env bash
# Render colour-option sample sheets before the full render.
#   theme_samples.sh <project-dir> "<t1,t2,t3>" <palette-id> [<palette-id> ...]
# For each palette: copies the project to a temp dir, rebuilds frames with THEME=<palette>, snapshots
# the given times, and writes <project>/design-samples/option-<palette>.jpg (frames side by side).
set -euo pipefail
P="$(cd "$1" && pwd)"; AT="$2"; shift 2
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$P/design-samples"
for PAL in "$@"; do
  D="$(mktemp -d)"
  cp -r "$P"/{index.html,compositions,assets,hyperframes.json,meta.json,package.json,STORYBOARD.md,scripts} "$D/"
  ( cd "$D" && THEME="$(python3 "$SKILL/scripts/pick_palette.py" theme-json "$PAL")" python3 scripts/build_frames.py >/dev/null \
      && npx hyperframes snapshot --at "$AT" --no-end >/dev/null 2>&1 )
  mapfile -t SHOTS < <(ls "$D"/snapshots/frame-*.png | sort)
  ARGS=(); F=""; i=0
  for s in "${SHOTS[@]}"; do ARGS+=(-i "$s"); F+="[$i]scale=540:960[s$i];"; i=$((i+1)); done
  IN=""; for ((j=0;j<i;j++)); do IN+="[s$j]"; done
  ffmpeg -y -loglevel error "${ARGS[@]}" -filter_complex "${F}${IN}hstack=$i,pad=iw+40:ih+40:20:20:color=0x222222" -q:v 3 "$P/design-samples/option-$PAL.jpg"
  rm -rf "$D"; echo "✓ design-samples/option-$PAL.jpg"
done
