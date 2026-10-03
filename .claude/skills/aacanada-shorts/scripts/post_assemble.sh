#!/usr/bin/env bash
# Run after captions.mjs + assemble-index.mjs + transitions.mjs inject (they rewrite these files).
#  1. CDNs are blocked: index loads the vendored GSAP; captions drop their own GSAP load (index has it).
#  2. captions.html ships its own Pretendard @font-face map (800 -> Black) which conflicts with the
#     frames' map (800 -> ExtraBold, 900 -> Black); conflicting faces crash the compiler with
#     "Maximum call stack size exceeded" in `hyperframes check`. Reuse the frames' map.
#  3. Captions move to the TOP band (y 180–330) with larger type — the user's standing preference.
#  4. Mark the captions host for Studio's caption track.
set -euo pipefail
cd "${1:-$(dirname "$0")/..}"
sed -i -E 's#<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*/dist/gsap\.min\.js"[^>]*></script>#<script src="assets/vendor/gsap.min.js"></script>#' index.html
sed -i -E '\#<script src="(https://cdn\.jsdelivr\.net/npm/gsap@[^"]*|assets/vendor)/(dist/)?gsap\.min\.js"[^>]*></script>#d' compositions/captions.html
python3 - <<'PY'
import re, glob
p = "compositions/captions.html"; s = open(p, encoding="utf-8").read()
frame = sorted(glob.glob("compositions/frames/*.html"))[0]
ff = re.search(r"@font-face\{.*?\}(?:@font-face\{.*?\})*", open(frame, encoding="utf-8").read()).group(0)
s = "\n".join(l for l in s.split("\n") if "@font-face { font-family" not in l)
if ff not in s:
    s = s.replace("<style data-brand-tokens>", "<style data-brand-tokens>\n" + ff, 1)
s = re.sub(r"--cap-band-top: \d+px;", "--cap-band-top: 180px;", s)
s = re.sub(r"--cap-band-height: \d+px;", "--cap-band-height: 150px;", s)
s = re.sub(r"(\n\s*top: )\d+px;(\n\s*height: )\d+px;", r"\g<1>180px;\g<2>150px;", s)
if "/* aac-top-captions */" not in s:
    s = s.replace("</template>", "<style>/* aac-top-captions */ .caption-line{font-size:58px !important;} .caption-pill{max-width:92% !important;}</style>\n</template>", 1)
open(p, "w", encoding="utf-8").write(s)
PY
grep -q 'data-track-kind="captions"' index.html || sed -i 's#id="el-captions"#id="el-captions" data-track-kind="captions"#' index.html
echo "✓ post-assemble fixups applied"
