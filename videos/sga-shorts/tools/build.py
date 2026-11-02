"""Build one short: python3 -I tools/build.py <N>   (run from videos/sga-shorts after tools/tts.py <N>)
Writes compositions/sN-scene.html, compositions/cta.html, index.html (the render entry) and sN/timing.json."""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FONTS, T_RE, scene_html  # noqa: E402
from shorts import SHORTS  # noqa: E402

N = int(sys.argv[1])
SP = SHORTS[N]
TM = json.load(open(f"assets/voice/s{N}.timing.json", encoding="utf-8"))
MAXC = 15
SFX = {"whoosh": (0.574, 0.25), "pop": (0.5, 0.30), "impact": (1.2, 0.24), "stamp": (1.2, 0.30)}
CTA_LEN, MIN_TOTAL = 3.3, 35.0

# display text + per-character times (display aligned to the TTS text of each row)
text, chars, rows = "", [], []
for r in TM["rows"]:
    disp, tts, ts = r["text"], r["tts"], r["tts_starts"]
    sm = difflib.SequenceMatcher(None, disp, tts, autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            m[a + k] = ts[b + k]
    known = sorted(m.items())
    times = []
    for k in range(len(disp)):
        if k in m:
            times.append(m[k])
            continue
        prev = [kv for kv in known if kv[0] < k]
        nxt = [kv for kv in known if kv[0] > k]
        if prev and nxt:
            (k0, t0), (k1, t1) = prev[-1], nxt[0]
            times.append(t0 + (t1 - t0) * (k - k0) / (k1 - k0))
        else:
            times.append(prev[-1][1] if prev else r["t"])
    if text:
        text += " "
        chars.append(times[0])
    rows.append(dict(t=r["t"], end=r["end"], text=disp, off=len(text)))
    text += disp
    chars += [round(x, 3) for x in times]

last = TM["rows"][-1]
cta_start = round(last["t"] - 0.2, 3) if "canlog" in last["text"] else round(TM["voice_end"] + 0.3, 3)
total = round(max(cta_start + CTA_LEN, TM["voice_end"] + 0.8, MIN_TOTAL), 3)
cta_dur = round(total - cta_start, 3) if total - cta_start <= 6 else CTA_LEN
if total - cta_start > 6:  # voice too short for 35 s: hold the scene, CTA keeps the last seconds
    cta_start = round(total - CTA_LEN - 1.2, 3)
    cta_dur = round(total - cta_start, 3)


def resolve(src):
    def rep(mt):
        k = text.find(mt.group(1))
        if k < 0:
            raise SystemExit(f"s{N}: cue phrase not in narration: {mt.group(1)!r}")
        return f"{chars[k]:.3f}"
    return T_RE.sub(rep, src)


def paths(s):
    return s.replace("@P/", "assets/photos/").replace("@B/", "assets/brand/")


# ---------------- scene
cid = f"k{N}"
fx, aud = sorted((round(eval(resolve(e), {"__builtins__": {}}), 3), n) for n, e in SP.get("sfx", [])), []
for i, (at, name) in enumerate(fx):
    ln, vol = SFX[name]
    nxt = [a for a, _ in fx[i + 1:]]
    d = round(min(ln, total - at, (nxt[0] - at - 0.02) if nxt else 99), 3)
    if d > 0.05:
        aud.append(f'        <audio id="{cid}-fx{i}" src="assets/sfx/{name}.mp3" data-start="{at}" data-duration="{d}" data-track-index="30" data-volume="{vol}" data-hf-media-start-basis="local"></audio>')
js = resolve(SP["js"]) + f"\ntl.to(q('.stage'),{{opacity:0,duration:0.35,ease:'power1.in'}},{cta_start});\n"  # scene clears under the CTA card
html = scene_html(cid, total, SP["css"], SP["body"], js, SP.get("bg", ""), "\n".join(aud))
os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    os.remove(os.path.join("compositions", f))
open(f"compositions/s{N}-scene.html", "w", encoding="utf-8").write(paths(html))

# ---------------- CTA (last seconds)
CTA_CSS = """
R .bg{background:#0f1d3d}
R #cta-logo{left:360px;top:330px;width:360px;height:348px}
R #cta-btn{left:110px;top:1060px;width:860px;height:130px;border-radius:70px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:54px;box-shadow:0 18px 44px rgba(200,16,46,.45)}
"""
cta_body = """
          <div class="abs" id="cta-logo"><img src="@B/aa-canada-logo.png" alt="" style="width:100%;height:100%;object-fit:contain" /></div>
          <div class="abs h" id="cta-aa" style="left:0;right:0;top:730px;text-align:center;font-size:120px;letter-spacing:.02em">AA CANADA</div>
          <div class="abs hd" id="cta-l1" style="left:0;right:0;top:880px;text-align:center;font-size:44px">캐나다 관리형 조기유학 · 토론토</div>
          <div class="abs" id="cta-btn">무료 학점 계산 · 카톡 canlog</div>
          <div class="abs b" id="cta-tel" style="left:0;right:0;top:1220px;text-align:center;font-size:36px;color:rgba(255,255,255,.85)">02-567-4345</div>"""
cta_js = """
tl.fromTo('.bg',{opacity:0},{opacity:1,duration:0.35},0);
tl.fromTo('#cta-logo',{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.5,ease:'back.out(1.8)'},0.1);
mask('#cta-aa',0.3,0.6,'l');inn('#cta-l1',0.55,{y:14});
slam('#cta-btn',0.7,{s:1.5});inn('#cta-tel',1.0,{y:10});
tl.fromTo('#cta-btn',{scale:1},{scale:1.06,duration:0.5,ease:'sine.inOut',yoyo:true,repeat:Math.max(1,Math.floor((D-1.2)/0.5)-1)},1.2);
"""
cta = scene_html("cta", cta_dur, CTA_CSS, cta_body, cta_js.replace("'.bg'", "root.querySelector('.bg')"), "", "")
open("compositions/cta.html", "w", encoding="utf-8").write(paths(cta))


# ---------------- captions (<= 15 chars a line, up to 2 lines)
def lines_of(t):
    if len(t) <= MAXC:
        return [t]
    words, best = t.split(), None

    def rec(ws, k):
        if k == 1:
            yield [" ".join(ws)]
            return
        for c in range(1, len(ws) - k + 2):
            for rest in rec(ws[c:], k - 1):
                yield [" ".join(ws[:c])] + rest
    n = -(-len(t) // MAXC)
    for k in (n, n + 1):
        for ls in rec(words, k):
            sc = (max(len(x) for x in ls) > MAXC, max(len(x) for x in ls) - 2 * sum(x.endswith(",") for x in ls[:-1]))
            if best is None or sc < best[0]:
                best = (sc, ls)
        if not best[0][0]:
            break
    return best[1]


caps = []
for r in rows:
    ls = lines_of(r["text"])
    pos = r["off"]
    for i in range(0, len(ls), 2):
        grp = ls[i:i + 2]
        k = text.find(grp[0], pos)
        caps.append([chars[k], None, grp, r["end"] + 0.3])
        pos = k + len(grp[0])
for i, c in enumerate(caps):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else c[3]
    c[1] = min(c[3], nxt - 0.02) if nxt > c[0] else c[3]
keys = sorted(SP.get("keys", []), key=len, reverse=True)


def hl(s):
    for k in keys:
        if k in s:
            s = s.replace(k, f"<b>{k}</b>", 1)
    return s


cap_html = "\n".join(
    f'      <div id="cap-{i:02d}" class="clip cap" data-start="{a:.3f}" data-duration="{max(0.2, b - a):.3f}" data-track-index="20">'
    + "".join(f"<span>{hl(x)}</span>" for x in ls) + "</div>"
    for i, (a, b, ls, _) in enumerate(caps))

bgm_auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0.0}, {"t": 1.0, "v": 0.10}, {"t": round(cta_start, 3), "v": 0.10}, {"t": round(cta_start + 0.6, 3), "v": 0.16},
    {"t": round(total - 1.2, 3), "v": 0.16}, {"t": total, "v": 0}]}]})
index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #14254a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #14254a; font-family: Pretendard, sans-serif; }}
      [data-composition-id="root"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      .brand {{ position: absolute; left: 0; right: 0; top: 200px; z-index: 300; display: flex; justify-content: center; align-items: center; gap: 12px; color: rgba(255,255,255,.9); font-weight: 800; font-size: 30px; letter-spacing: .06em; text-shadow: 0 2px 8px rgba(0,0,0,.5); }}
      .brand i {{ display: block; width: 14px; height: 14px; border-radius: 50%; background: #c8102e; box-shadow: 22px 0 0 #e8b931; margin-right: 22px; }}
      .cap {{ position: absolute; left: 40px; right: 40px; top: 1380px; height: 180px; z-index: 310; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 6px; }}
      .cap span {{ display: block; background: rgba(8,16,36,.8); color: #fff; font-weight: 700; font-size: 56px; line-height: 1.25; padding: 6px 26px; border-radius: 14px; white-space: nowrap; }}
      .cap b {{ color: #e8b931; font-weight: 700; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-duration="{total}">
      <div id="el-scene" style="z-index:1" data-composition-id="{cid}" data-composition-src="compositions/s{N}-scene.html" data-start="0" data-duration="{total}" data-track-index="1" data-width="1080" data-height="1920"></div>
      <div id="el-cta" style="z-index:2" data-composition-id="cta" data-composition-src="compositions/cta.html" data-start="{cta_start}" data-duration="{cta_dur}" data-track-index="2" data-width="1080" data-height="1920"></div>
      <div id="brand" class="clip brand" data-start="0" data-duration="{total}" data-track-index="5"><i></i>AA CANADA · 토론토 조기유학</div>
      <audio id="vo" src="assets/voice/s{N}.wav" data-start="0" data-duration="{round(TM['voice_end'] + 0.3, 3)}" data-track-index="10" data-volume="1"></audio>
      <audio id="bgm" src="assets/music/bgm-a.mp3" data-start="0" data-duration="{total}" data-track-index="11" data-volume="1" data-automation='{bgm_auto}'></audio>
{cap_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(paths(index))
os.makedirs(f"s{N}", exist_ok=True)
json.dump(dict(short=N, total=total, cta_start=cta_start, voice_end=TM["voice_end"], rows=rows, captions=[[round(a, 3), round(b, 3), ls] for a, b, ls, _ in caps]),
          open(f"s{N}/timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"s{N}: total {total}s, voice {TM['voice_end']}s, cta at {cta_start}, captions {len(caps)}")
