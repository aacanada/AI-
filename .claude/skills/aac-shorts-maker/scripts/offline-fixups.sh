#!/usr/bin/env bash
# Point every GSAP CDN reference at the local copy (cdn.jsdelivr.net is blocked in the cloud
# container; local also makes renders reproducible). Run after captions build AND after
# assemble-index / transitions inject, before lint/check/render.
# usage: offline-fixups.sh <PROJECT_DIR>
set -euo pipefail
P="$1"; SK="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$P/assets/vendor"; [ -f "$P/assets/vendor/gsap.min.js" ] || cp "$SK/assets/gsap.min.js" "$P/assets/vendor/"
for f in "$P/index.html" "$P"/compositions/*.html "$P"/compositions/frames/*.html; do
  [ -f "$f" ] || continue
  sed -i -E 's#<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*/dist/gsap\.min\.js"[^>]*></script>#<script src="assets/vendor/gsap.min.js"></script>#g' "$f"
done
grep -l 'cdn.jsdelivr' "$P/index.html" "$P"/compositions/*.html "$P"/compositions/frames/*.html 2>/dev/null && echo "⚠ CDN refs remain" || echo "✓ GSAP local everywhere"
