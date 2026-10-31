#!/bin/bash
# Regenerate one scene (same script text) and keep every take: audio/takes/<id>_tN.mp3 + video/asr/takes/<id>_tN.json
# Usage: retake.sh s04 [count]
set -e
P=/home/user/AI-/plans/montreal-multilang-longform
k=$1; n=${2:-1}
mkdir -p $P/audio/takes $P/video/asr/takes
for i in $(seq 1 $n); do
  t=$(ls $P/audio/takes/${k}_t*.mp3 2>/dev/null | wc -l); t=$((t + 1))
  python3 $P/video/tools/tts.py $k >/dev/null
  python3 $P/video/tools/asr.py $k
  cp $P/audio/mlang_$k.mp3 $P/audio/takes/${k}_t$t.mp3
  cp $P/video/asr/$k.json $P/video/asr/takes/${k}_t$t.json
  echo "  -> saved take $t"
done
