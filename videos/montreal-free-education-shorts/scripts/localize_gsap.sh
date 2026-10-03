#!/usr/bin/env bash
# Post-assembly fixups for this sandbox:
#  - CDNs are blocked: point index at the vendored GSAP, and drop captions' own GSAP load (index already loads it).
#  - captions.html ships its own Pretendard @font-face map (800 -> Black) that conflicts with the frames'
#    (800 -> ExtraBold, 900 -> Black); conflicting faces overflow the compiler, so reuse the frames' map.
#  - mark the captions host for the timeline's caption track.
cd "$(dirname "$0")/.."
sed -i -E 's#<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*/dist/gsap\.min\.js"[^>]*></script>#<script src="assets/vendor/gsap.min.js"></script>#' index.html
sed -i -E '\#<script src="(https://cdn\.jsdelivr\.net/npm/gsap@[^"]*|assets/vendor)/(dist/)?gsap\.min\.js"[^>]*></script>#d' compositions/captions.html
python3 - <<'PY'
import re
p = "compositions/captions.html"; s = open(p).read()
ff = re.search(r"@font-face\{.*?\}(?:@font-face\{.*?\})*", open("compositions/frames/01-hook.html").read()).group(0)
s = "\n".join(l for l in s.split("\n") if "@font-face { font-family" not in l)
if ff not in s:
    s = s.replace("<style data-brand-tokens>", "<style data-brand-tokens>\n" + ff, 1)
open(p, "w").write(s)
PY
grep -q 'data-track-kind="captions"' index.html || sed -i 's#id="el-captions"#id="el-captions" data-track-kind="captions"#' index.html
