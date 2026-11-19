#!/usr/bin/env bash
# Mux the HyperFrames render with the mastered mix, verify loudness, split for git if > 90MB.
set -euo pipefail
cd "$(dirname "$0")/.."
TOTAL=$(python3 -c "import json;print(json.load(open('build/timeline.json'))['total'])")
ffmpeg -y -hide_banner -loglevel error -i renders/render_raw.mp4 -i audio/mix_master.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -t "$TOTAL" -movflags +faststart renders/video.mp4
echo "== loudness (decoded from final mp4) =="
ffmpeg -hide_banner -nostats -i renders/video.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p'
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of compact renders/video.mp4
SIZE=$(stat -c %s renders/video.mp4)
if [ "$SIZE" -gt 94371840 ]; then
  rm -f renders/video.mp4.part-*
  split -b 85m -d renders/video.mp4 renders/video.mp4.part-
  (cd renders && sha256sum video.mp4 > video.mp4.sha256)
  ls -la renders/video.mp4.part-* renders/video.mp4.sha256
fi
