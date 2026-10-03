#!/usr/bin/env bash
# Scaffold a new AA Canada Shorts project.
#   setup_project.sh <slug> <palette-id> [image ...]
# Creates videos/<slug> with hyperframes init (faceless-explainer), Pretendard woff2 + GSAP vendored
# from npm (CDNs are blocked in this sandbox), frame.md from the blue-professional preset remixed to
# Pretendard and recoloured with the chosen palette, user images under assets/images/, and the frame
# generator template under scripts/.
set -euo pipefail
SLUG="$1"; PAL="$2"; shift 2
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$SKILL/../../.." && pwd)"
HFS="$REPO/.claude/skills"
P="$REPO/videos/$SLUG"
TMP="$(mktemp -d)"
[ -e "$P" ] && { echo "✗ $P already exists" >&2; exit 1; }
cd "$REPO"
npx hyperframes init "videos/$SLUG" --non-interactive --example=blank --skill=faceless-explainer >/dev/null
mkdir -p "$P"/{assets/fonts,assets/vendor,assets/images,assets/voice,capture/extracted,compositions/frames,scripts}
( cd "$TMP" && npm pack pretendard@1.3.9 -q >/dev/null 2>&1 && tar xzf pretendard-1.3.9.tgz && \
  for w in Regular SemiBold Bold ExtraBold Black; do cp package/dist/web/static/woff2/Pretendard-$w.woff2 "$P/assets/fonts/"; done && \
  rm -rf package && npm pack gsap@3.14.2 -q >/dev/null 2>&1 && tar xzf gsap-3.14.2.tgz && cp package/dist/gsap.min.js "$P/assets/vendor/" )
cat > "$P/capture/extracted/tokens.json" <<JSON
{ "title": "$SLUG", "description": "", "colors": [], "fonts": [{ "family": "Pretendard", "weights": [400, 600, 700, 800, 900] }] }
JSON
( cd "$P" && node "$HFS/faceless-explainer/scripts/build-frame.mjs" --preset blue-professional --hyperframes . >/dev/null )
python3 "$SKILL/scripts/pick_palette.py" apply "$PAL" "$P"
cp "$SKILL/assets/build_frames_template.py" "$P/scripts/build_frames.py"
cp "$SKILL/scripts/post_assemble.sh" "$P/scripts/post_assemble.sh"
for img in "$@"; do cp "$img" "$P/assets/images/"; done
printf 'renders/work-*/\nrenders/.*hf-transaction*/\nsnapshots/\n' > "$P/.gitignore"
rm -rf "$TMP"
echo "✓ $P ready (palette $PAL, $(ls "$P/assets/images" | wc -l) image(s))"
