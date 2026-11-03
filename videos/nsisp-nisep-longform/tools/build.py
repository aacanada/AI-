"""Generate compositions/*.html, index.html, timing.json and mix_cues.json. Run from the project root:
    python3 -I tools/build.py
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FONTS, PLAN, XF, Align, scene_html, timeline  # noqa: E402
from scenes import SCENES, endcard  # noqa: E402
from script import CHAPTER  # noqa: E402

os.makedirs("compositions", exist_ok=True)
os.makedirs(os.path.join("assets", "voice"), exist_ok=True)
D, V, E, CLIP, TOTAL = timeline()

# voice files for preview playback (the final audio is mixed by tools/mix.py)
for k in range(1, 10):
    dst = os.path.join("assets", "voice", f"S{k}.wav")
    if k in (1, 9):
        src = os.path.join(PLAN, "heygen", f"S{k}_face.mp4")
    else:
        src = os.path.join(PLAN, "audio", f"S{k}.mp3")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ar", "48000", "-ac", "2", dst], check=True)

AL = {k: Align(k) for k in range(1, 10)}
OFF = {k: (V[k] - CLIP[k][0]) for k in range(1, 10)}  # local time of voice start inside each scene clip
cue_log, sfx = {}, []

for k in range(1, 10):
    log = cue_log.setdefault(f"S{k}", {})

    def T(p, k=k, log=log):
        t = round(OFF[k] + AL[k].at(p), 3)
        log[p] = t
        return t

    css, body, js = SCENES[k](T, CLIP[k][1])
    cid = f"s{k:02d}"
    open(f"compositions/{cid}.html", "w", encoding="utf-8").write(
        scene_html(cid, CLIP[k][1], css, body, "\n".join(js), bg=k not in (1, 9)))
    # scene SFX: stamps in S5, check clicks in S6
    for line in js:
        m = re.match(r'(\w+)\("([^"]+)",([\d.]+)', line)
        if not m:
            continue
        fn, sel, at = m.group(1), m.group(2), float(m.group(3))
        g = round(CLIP[k][0] + at, 3)
        if fn == "stamp":
            sfx.append({"kind": "stamp", "t": g})
        elif k == 6 and fn == "draw" and sel.endswith(" .cm"):
            sfx.append({"kind": "click", "t": g})
        elif fn == "count" and k in (2, 4, 5) and sel in ("#s02-n1", "#s04-n7", "#s05-tv"):
            sfx.append({"kind": "click", "t": g})

css, body, js = endcard(None, CLIP["end"][1])
open("compositions/end.html", "w", encoding="utf-8").write(scene_html("end", CLIP["end"][1], css, body, "\n".join(js)))

# ------------------------------------------------------------------ captions
caps = []
for k in range(1, 10):
    for st, en, txt in AL[k].captions():
        caps.append((round(V[k] + st, 3), round(V[k] + en, 3), txt))
for i in range(len(caps) - 1):  # never overlap
    if caps[i][1] > caps[i + 1][0] - 0.02:
        caps[i] = (caps[i][0], round(caps[i + 1][0] - 0.02, 3), caps[i][2])


def cap_html(t):
    t = html.escape(t)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


# ------------------------------------------------------------------ index.html
els, tl = [], []
f1 = CLIP[1]
els.append(f'<video id="face1" class="clip face" src="assets/face/S1_face.mp4" muted playsinline data-start="0" data-duration="{D[1]}" data-track-index="0"></video>')
els.append(f'<video id="face9" class="clip face" src="assets/face/S9_face.mp4" muted playsinline data-start="{V[9]}" data-duration="{D[9]}" data-track-index="0"></video>')
for k in range(1, 10):
    s, d = CLIP[k]
    els.append(f'<div id="el-s{k:02d}" style="z-index:{10 + k}" data-composition-id="s{k:02d}" data-composition-src="compositions/s{k:02d}.html" '
               f'data-start="{s}" data-duration="{d}" data-track-index="{1 + (k % 2)}" data-width="1920" data-height="1080"></div>')
    if 2 <= k <= 8:
        tl.append(f'tl.fromTo("#el-s{k:02d}",{{opacity:0,scale:1.04}},{{opacity:1,scale:1,duration:{XF},ease:"power2.out"}},{s});')
        sfx.append({"kind": "whoosh", "t": s})
s, d = CLIP["end"]
els.append(f'<div id="el-end" style="z-index:30" data-composition-id="end" data-composition-src="compositions/end.html" '
           f'data-start="{s}" data-duration="{d}" data-track-index="1" data-width="1920" data-height="1080"></div>')
tl.append(f'tl.fromTo("#el-end",{{opacity:0}},{{opacity:1,duration:{XF},ease:"power2.out"}},{s});')
tl.append(f'tl.fromTo("#face9",{{opacity:0}},{{opacity:1,duration:{XF},ease:"power2.out"}},{V[9]});')
sfx.append({"kind": "whoosh", "t": round(V[9] - 0.05, 3)})
sfx.append({"kind": "whoosh", "t": s})

els.append(f'<div id="brand" class="clip brand" data-start="0" data-duration="{CLIP["end"][0]}" data-track-index="5">'
           f'AA CANADA</div>')
for k in range(2, 9):
    st = round(CLIP[k][0] + XF, 3)
    en = E[k] if k < 8 else V[9]
    els.append(f'<div id="pill-{k}" class="clip chpill" data-start="{st}" data-duration="{round(en - st, 3)}" data-track-index="6">'
               f'<i></i><span>{k - 1}</span>{CHAPTER[k]}</div>')
for k in range(1, 10):
    src = f"assets/voice/S{k}.wav"
    els.append(f'<audio id="vo-s{k}" src="{src}" data-start="{V[k]}" data-duration="{D[k]}" data-track-index="10" data-volume="1"></audio>')
for i, (st, en, txt) in enumerate(caps):
    els.append(f'<div id="cap-{i:03d}" class="clip cap" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="20"><span>{cap_html(txt)}</span></div>')

index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0a1c30; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0a1c30; font-family: Pretendard, sans-serif; }}
      [data-composition-id="root"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      .face {{ position: absolute; inset: 0; width: 1920px; height: 1080px; object-fit: cover; z-index: 1; }}
      #face9 {{ z-index: 19; }}
      #el-s09 {{ z-index: 20 !important; }}
      .brand {{ position: absolute; left: 44px; top: 32px; z-index: 300; display: flex; align-items: center; gap: 14px; padding: 6px 24px 6px 6px; border-radius: 99px; background: rgba(7,19,31,.80); color: #f5f0e6; font-weight: 900; font-size: 26px; letter-spacing: .08em; }}
      .brand:before {{ content: ''; display: block; width: 52px; height: 50px; border-radius: 50%; background: #fff url(assets/img/aa-canada-logo-transparent.png) center/52px 50px no-repeat; }}
      .chpill {{ position: absolute; right: 48px; top: 36px; z-index: 300; display: flex; align-items: center; gap: 12px; padding: 8px 24px 8px 10px; border-radius: 99px; background: rgba(7,19,31,.80); border: 2px solid rgba(245,240,230,.28); color: #f5f0e6; font-weight: 800; font-size: 26px; }}
      .chpill i {{ display: none; }}
      .chpill span {{ display: flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; background: #2fb5a5; color: #07131f; font-weight: 900; font-size: 22px; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 884px; height: 100px; z-index: 310; display: flex; justify-content: center; align-items: center; }}
      .cap span {{ display: inline-block; background: rgba(5,14,24,.82); color: #fff; font-weight: 700; font-size: 50px; line-height: 1.3; padding: 12px 36px; border-radius: 16px; white-space: nowrap; }}
      .cap b {{ color: #f2c14e; font-weight: 800; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="{TOTAL}">
      {chr(10).join("      " + e for e in els).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in tl).strip()}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(index)

json.dump(dict(total=TOTAL, durations=D, voice_start=V, voice_end=E, clips={str(k): v for k, v in CLIP.items()}, cues=cue_log,
               captions=caps), open("timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
voice = [{"id": f"S{k}", "src": f"assets/voice/S{k}.wav", "t": V[k], "d": D[k]} for k in range(1, 10)]
json.dump(dict(total=TOTAL, voice=voice, sfx=sorted(sfx, key=lambda e: e["t"])), open("mix_cues.json", "w"), indent=1)
print(f"total {TOTAL:.3f}s  captions {len(caps)}  sfx {len(sfx)}")
for k in range(1, 10):
    print(f"S{k} voice {V[k]:.2f}-{E[k]:.2f}  clip {CLIP[k]}")
