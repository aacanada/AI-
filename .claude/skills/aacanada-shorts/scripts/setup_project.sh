#!/usr/bin/env bash
# Usage: setup_project.sh <project-dir>
# Creates a HyperFrames project and copies in fonts, GSAP, the premium template and helper scripts.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJ="$1"
if [ ! -f "$PROJ/hyperframes.json" ]; then
  npx --yes hyperframes init "$PROJ" --non-interactive --example=blank --skill=faceless-explainer >/dev/null
fi
PROJ="$(cd "$PROJ" && pwd)"
mkdir -p "$PROJ"/{public/fonts,assets/voice,assets/music,src,renders}

TMP="$(mktemp -d)"
pushd "$TMP" >/dev/null
# CDNs are often blocked in render browsers / proxies → pull from the npm registry instead.
npm pack pretendard@1.3.9 gsap@3.14.2 @fontsource/playfair-display@5 >/dev/null 2>&1
for t in *.tgz; do mkdir -p "${t%.tgz}"; tar xzf "$t" -C "${t%.tgz}"; done
for w in Medium Bold ExtraBold Black; do
  cp pretendard-*/package/dist/web/static/woff2/Pretendard-$w.woff2 "$PROJ/public/fonts/"
done
for w in 600 700 800; do
  cp fontsource-playfair-display-*/package/files/playfair-display-latin-$w-normal.woff2 "$PROJ/public/fonts/PlayfairDisplay-$w.woff2"
done
cp fontsource-playfair-display-*/package/files/playfair-display-latin-600-italic.woff2 "$PROJ/public/fonts/PlayfairDisplay-600i.woff2"
cp gsap-*/package/dist/gsap.min.js "$PROJ/public/gsap.min.js"
popd >/dev/null
rm -rf "$TMP"

cp "$SKILL_DIR/scripts/gen_tts.py" "$SKILL_DIR/scripts/gen_bgm.py" "$SKILL_DIR/scripts/build.py" "$SKILL_DIR/scripts/prep_images.py" "$PROJ/"
[ -f "$PROJ/src/index.template.txt" ] || cp "$SKILL_DIR/templates/index.template.txt" "$PROJ/src/index.template.txt"
[ -f "$PROJ/scenes.json" ] || cp "$SKILL_DIR/templates/scenes.example.json" "$PROJ/scenes.json"
echo "ready: $PROJ"
