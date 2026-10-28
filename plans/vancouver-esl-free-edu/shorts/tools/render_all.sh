#!/bin/bash
# Render each short's composition (silent) sequentially.
cd /home/user/AI-/plans/vancouver-esl-free-edu/shorts/hf
for s in "$@"; do
  cp ../src/short_$s.html index.html
  npx hyperframes render -o ../$s/silent.mp4 --fps 30 --quality looks --skill general-video > ../$s/render.log 2>&1
  echo "$s exit $?"
done
