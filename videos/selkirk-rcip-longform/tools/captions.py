#!/usr/bin/env python3
"""SCRIPT.md의 Line 텍스트로 자막 sub-composition을 만든다.
실제 녹음이 들어오기 전에는 글자 수 비례로 시간을 추정하고, 녹음 후에는 전사 타이밍으로 교체한다.
사용: captions.py <total_dur> <line:start:dur> ..."""
import re, sys, json, pathlib
proj = pathlib.Path(__file__).resolve().parent.parent
t = (proj / "SCRIPT.md").read_text(encoding="utf-8")
parts = re.split(r"^## Line (\d+).*$", t, flags=re.M)
lines = {}
for i in range(1, len(parts), 2):
    lines[int(parts[i])] = [l.strip() for l in parts[i + 1].splitlines() if l.startswith("    ") and l.strip()]

def chunks(s, maxlen=34):
    if len(s) <= maxlen: return [s]
    words = s.split(" "); out = []; cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxlen:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    # 마지막 조각이 너무 짧으면 앞에 붙인다
    if len(out) > 1 and len(out[-1]) < 8:
        last = out.pop(); out[-1] = out[-1] + " " + last
    return out

total = float(sys.argv[1]); cues = []
for spec in sys.argv[2:]:
    ln, st, du = spec.split(":"); ln = int(ln); st = float(st); du = float(du)
    segs = [c for s in lines[ln] for c in chunks(s)]
    w = [len(re.sub(r"\s", "", s)) + 3 for s in segs]
    a, b = st + 0.4, st + du - 0.5; span = b - a; tot = sum(w); cur = a
    for s, wi in zip(segs, w):
        d = span * wi / tot; cues.append((round(cur, 2), round(d - 0.08, 2), s)); cur += d

items = "\n".join(
    f'  <div class="cue clip" id="cap-{i}" data-start="{s}" data-duration="{d}"><span>{txt}</span></div>'
    for i, (s, d, txt) in enumerate(cues))
html = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
@font-face{{font-family:Pretendard;font-weight:700;src:url(assets/fonts/Pretendard-Bold.woff2) format("woff2")}}
#captions{{position:absolute;inset:0;pointer-events:none}}
#captions .cue{{position:absolute;left:0;right:0;top:auto;bottom:56px;height:auto;display:flex;justify-content:center}}
#captions .cue span{{background:#16324F;color:#FAF6EF;font-family:Pretendard,sans-serif;font-weight:700;font-size:40px;line-height:1.3;padding:12px 30px;border-radius:14px;word-break:keep-all;max-width:1500px;text-align:center}}
      </style>
      <div id="captions" data-composition-id="captions" data-width="1920" data-height="1080" data-duration="{total}">
{items}
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
(proj / "compositions" / "captions.html").write_text(html, encoding="utf-8")
print(len(cues), "cues")
