#!/usr/bin/env bash
# Usage: thumbnail.sh <project-dir>   (renders <project>/thumbnail/thumbnail.html → thumbnail.png + .jpg, 1080x1920)
set -euo pipefail
P="$(cd "$1" && pwd)"
CHROME="$(ls /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
CHROME="${CHROME:-$(command -v chromium || command -v google-chrome)}"
# render taller than 1920 then crop: headless reserves a strip at the bottom of the viewport
"$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1080,2100 --virtual-time-budget=3000 --screenshot="$P/thumbnail/full.png" "file://$P/thumbnail/thumbnail.html" >/dev/null 2>&1
ffmpeg -y -v error -i "$P/thumbnail/full.png" -vf crop=1080:1920:0:0 "$P/thumbnail/thumbnail.png"
ffmpeg -y -v error -i "$P/thumbnail/thumbnail.png" -q:v 2 "$P/thumbnail/thumbnail.jpg"
rm -f "$P/thumbnail/full.png"
echo "$P/thumbnail/thumbnail.png"
