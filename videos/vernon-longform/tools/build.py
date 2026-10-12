"""Generate compositions/*.html and index.html from timing.json + scene specs.

Run from the project root:  python3 -I tools/build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FONTS, scene_html  # noqa: E402
from scenes_a import S as SA  # noqa: E402
from scenes_b import S as SB  # noqa: E402

SPECS = {**SA, **SB}
ROOT = os.path.dirname(HERE)
timing = json.load(open(os.path.join(ROOT, "timing.json"), encoding="utf-8"))
os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)

MAX = 26


def chunks(text):
    words = text.split()
    out, cur = [], ""
    for w in words:
        nxt = (cur + " " + w).strip()
        if len(nxt) > MAX and cur:
            out.append(cur)
            cur = w
        else:
            cur = nxt
    if cur:
        if out and len(cur) <= 6:
            out[-1] = out[-1] + " " + cur
        else:
            out.append(cur)
    return out


slots, audios, caps = [], [], []
for s in timing:
    sid = s["id"]
    cid = f"s{s['idx']:02d}"
    spec = dict(SPECS[sid])
    spec.pop("no_out", None)
    cues = json.dumps([r["t"] for r in s["rows"]])
    html = scene_html(cid, sid, s["duration"], cues, spec["css"], spec["body"], spec["js"], spec.get("bg", ""))
    open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w", encoding="utf-8").write(html)
    slots.append(
        f'      <div id="slot-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{sid}.html" '
        f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" data-width="1920" data-height="1080"></div>'
    )
    audios.append(
        f'      <audio id="vo-{cid}" src="assets/voice/line{s["idx"]:02d}.mp3" data-start="{round(s["start"] + s["voiceAt"], 3)}" '
        f'data-duration="{s["voiceDur"]}" data-track-index="10" data-volume="1"></audio>'
    )
    for r in s["rows"]:
        parts = chunks(r["text"])
        total = sum(len(p) for p in parts)
        t0, t1 = r["t"], r["end"]
        acc = 0
        for k, p in enumerate(parts):
            a = t0 + (t1 - t0) * acc / total
            acc += len(p)
            b = t0 + (t1 - t0) * acc / total if k < len(parts) - 1 else t1 + 0.25
            gs = round(s["start"] + a, 3)
            caps.append((gs, round(b - a, 3), p))

# avoid caption overlap
for i in range(len(caps) - 1):
    g, d, p = caps[i]
    nxt = caps[i + 1][0]
    if g + d > nxt:
        caps[i] = (g, round(nxt - g - 0.02, 3), p)

total = round(sum(s["duration"] for s in timing), 2)
cap_html = "\n".join(
    f'      <div id="cap-{i:03d}" class="clip cap" data-start="{g}" data-duration="{d}" data-track-index="20"><span>{p}</span></div>'
    for i, (g, d, p) in enumerate(caps)
)

bgm = ""
for name, start in (("bgm-a", 0), ("bgm-b", None)):
    path = os.path.join(ROOT, "assets", "music", f"{name}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        bgm += f'      <audio id="{name}" src="assets/music/{name}.mp3" data-start="__{name}__" data-track-index="{11 if name == "bgm-a" else 12}" data-volume="1" __AUTO_{name}__></audio>\n'

index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #16324F; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #16324F; font-family: Pretendard, sans-serif; }}
      [data-composition-id="root"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      .cap {{ position: absolute; left: 0; right: 0; bottom: 56px; display: flex; justify-content: center; z-index: 100; }}
      .cap span {{ display: inline-block; max-width: 1500px; background: rgba(22, 50, 79, 0.86); color: #FAF6EF; font-weight: 700; font-size: 42px; line-height: 1.35; padding: 10px 30px; border-radius: 14px; text-align: center; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="{total}">
{chr(10).join(slots)}
{chr(10).join(audios)}
{bgm}{cap_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
# BGM placement: a from 0, b starts where a ends minus 4s overlap (computed from file length when present)
import subprocess  # noqa: E402

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

if "__bgm-a__" in index:
    a_len = dur(os.path.join(ROOT, "assets/music/bgm-a.mp3"))
    LV = 0.14
    ad = round(min(a_len, total), 2)
    index = index.replace('data-start="__bgm-a__"', f'data-start="0" data-duration="{ad}"')
    auto_a = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 2, "v": LV}, {"t": round(ad - 4, 2), "v": LV}, {"t": ad, "v": 0}]}]}
    index = index.replace("__AUTO_bgm-a__", "data-automation='" + json.dumps(auto_a) + "'")
    if "__bgm-b__" in index:
        b_start = round(max(0, a_len - 4), 2)
        b_len = dur(os.path.join(ROOT, "assets/music/bgm-b.mp3"))
        bd = round(min(b_len, total - b_start), 2)
        index = index.replace('data-start="__bgm-b__"', f'data-start="{b_start}" data-duration="{bd}"')
        auto_b = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 4, "v": LV}, {"t": round(bd - 3, 2), "v": LV}, {"t": bd, "v": 0}]}]}
        index = index.replace("__AUTO_bgm-b__", "data-automation='" + json.dumps(auto_b) + "'")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index)
print("scenes", len(timing), "captions", len(caps), "total", total, "bgm", bool(bgm))

# Re-apply the voiceover carve to both music beds (build rewrites index.html).
CARVE = os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs")
if bgm and os.path.exists(CARVE) and os.path.isdir(os.path.join(ROOT, "node_modules", "@hyperframes", "core")):
    for bed in ("bgm-a", "bgm-b"):
        subprocess.run(["node", CARVE, "--comp", "index.html", "--bed", bed], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    print("carve applied")
