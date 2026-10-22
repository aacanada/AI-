"""9:16 shorts A-E cut from the South Shore long-form recordings. Run from the long-form project root after build.py:
    python3 -I tools/shorts.py
Writes ../southshore-shorts/short-<x>/ (index.html + compositions/, assets -> the long-form assets). Each short is a list of segments
(scene, first row, last row); a segment hosts a window of the same 1920x1080 scene composition (scrubbed from the
window start, so every cue keeps its real speech time) scaled into the middle of a 1080x1920 frame, with the
matching slice of that scene's narration wav. Render one with:
    cd ../southshore-shorts/short-a && npx hyperframes render -o ../renders/short-a.mp4
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timing  # noqa: E402
from build import bgm_lane, captions, chunk, hl, scene_file  # noqa: E402
from common import fonts_css  # noqa: E402
from script import SCENES  # noqa: E402

OUT = os.path.join("..", "southshore-shorts")
SC_BY = {s["id"]: s for s in SCENES}
CTA = ("s10", 4, 4)  # "아이 학년과 성향을 카카오톡으로 보내 주시면, ... 보내 드리겠습니다."

SHORTS = {  # brief: plans/southshore-longform/VIDEO_BRIEF.md 4장
    "a": dict(title=["다운타운 <em>18분</em>,", "REM 타고 학교 동네로"], segs=[("s03", 1, 5), ("s03", 7, 7)]),
    "b": dict(title=["코퀴틀람 <em>11,900명</em>", "vs 생랑베르 <em>50명</em>"], segs=[("s04", 1, 7), CTA]),
    "c": dict(title=["브로사드 vs 생랑베르,", "<em>솔직 비교</em>"], segs=[("s04", 8, 14)]),
    "d": dict(title=["몬트리올 영어 공립", "<em>고등학교 4곳</em>"], segs=[("s06", 2, 3), ("s06", 5, 5), ("s06", 7, 8), ("s06", 10, 10)]),
    "e": dict(title=["캐나다 공립 조기유학", "1년, <em>얼마일까?</em>"], segs=[("s08", 0, 4), CTA]),
}
PRE, POST, XF = 0.3, 0.35, 0.3
S = 1080 / 1920  # scene scale
TOP = 520        # scene frame top


def windows(slots):
    by = {s["id"]: s for s in slots}
    for key, sh in SHORTS.items():
        t, segs = 0.0, []
        for n, (sid, r0, r1) in enumerate(sh["segs"]):
            sl = by[sid]
            a = max(0.0, sl["rows"][r0]["t"] - PRE)
            b = min(sl["voiceAt"] + sl["voiceDur"], sl["rows"][r1]["end"] + POST)
            segs.append(dict(n=n, sid=sid, r0=r0, r1=r1, a=round(a, 3), b=round(b, 3), start=round(t, 3), dur=round(b - a, 3)))
            t += b - a
        yield key, sh, segs, round(t, 3)


def short_html(key, sh, segs, total, slots):
    by = {s["id"]: s for s in slots}
    d = os.path.join(OUT, f"short-{key}")
    os.makedirs(os.path.join(d, "compositions"), exist_ok=True)
    for f in os.listdir(os.path.join(d, "compositions")):
        os.remove(os.path.join(d, "compositions", f))
    if not os.path.lexists(os.path.join(d, "assets")):
        os.symlink(os.path.join("..", "..", "southshore-longform", "assets"), os.path.join(d, "assets"))
    open(os.path.join(d, "hyperframes.json"), "w").write(open(os.path.join(OUT, "hyperframes.json")).read())
    hosts, voice, cap_rows, trans, foots = [], [], [], [], []
    for g in segs:
        sl = by[g["sid"]]
        cid = f"{key}{g['n'] + 1}-{g['sid']}"
        dur = round(g["dur"] + (XF if g is not segs[-1] else 0), 3)
        fn = f"{cid}.html"
        open(os.path.join(d, "compositions", fn), "w", encoding="utf-8").write(scene_file(sl, off=g["a"], duration=dur, cid=cid))
        hosts.append(f'        <div id="h-{cid}" class="host" style="z-index:{g["n"] + 1}" data-composition-id="{cid}" data-composition-src="compositions/{fn}" '
                     f'data-start="{g["start"]}" data-duration="{dur}" data-track-index="{1 + g["n"] % 2}" data-width="1920" data-height="1080"></div>')
        ms = round(max(0.0, g["a"] - sl["voiceAt"]), 3)
        vstart = round(g["start"] + max(0.0, sl["voiceAt"] - g["a"]), 3)
        vdur = round(min(sl["voiceDur"] - ms, g["b"] - max(g["a"], sl["voiceAt"])), 3)
        if sl["real"]:
            voice.append(f'    <audio id="vo-{cid}" src="assets/voice/{g["sid"]}.wav" data-start="{vstart}" data-media-start="{ms}" '
                         f'data-duration="{vdur}" data-track-index="10" data-volume="1"></audio>')
        if g["n"]:
            trans.append(f'tl.fromTo("#h-{cid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"power1.inOut"}},{g["start"]});')
        # rows of this window, re-based to short time
        rows = [dict(r) for r in sl["rows"][g["r0"]:g["r1"] + 1]]
        sub = dict(sl, rows=rows, start=round(g["start"] - g["a"], 3))
        cap_rows.append(sub)
        f = SC_BY[g["sid"]]["foot"]
        if f:
            foots.append(f'    <div id="ft-{cid}" class="clip foot" data-start="{g["start"]}" data-duration="{g["dur"]}" data-track-index="7">{f}</div>')
    caps = captions(cap_rows, maxc=14)
    cap_html = "\n".join(
        f'    <div id="cap-{i:03d}" class="clip cap" data-start="{a:.3f}" data-duration="{max(0.2, b - a):.3f}" data-track-index="20"><span>{hl(t, keys)}</span></div>'
        for i, (a, b, t, keys, _) in enumerate((a, min(b, total), t, k, x) for a, b, t, k, x in caps))
    win = [(g["start"], g["start"] + g["dur"]) for g in segs]
    bgm = bgm_lane(total, win)
    title = "".join(f"<div>{x}</div>" for x in sh["title"])
    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{fonts_css()}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #FFF8F2; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #FFF8F2; font-family: 'Noto Sans KR', sans-serif; color: #2B2B2B; }}
      .bar {{ position: absolute; left: 0; right: 0; top: 0; height: 18px; background: #C8102E; }}
      .title {{ position: absolute; left: 0; right: 0; top: 190px; text-align: center; font-family: 'Black Han Sans', sans-serif; font-size: 96px; line-height: 1.12; }}
      .title em {{ font-style: normal; color: #C8102E; }}
      .frame {{ position: absolute; left: 0; top: {TOP}px; width: 1080px; height: {1080 * S:.0f}px; overflow: hidden; border-top: 6px solid #C8102E; border-bottom: 6px solid #C8102E; background: #FFF8F2; }}
      .scaler {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform: scale({S}); transform-origin: 0 0; }}
      .host {{ position: absolute; inset: 0; }}
      .foot {{ position: absolute; left: 40px; right: 40px; top: {TOP + 1080 * S + 18:.0f}px; text-align: center; color: #7A1B26; font-size: 24px; font-weight: 500; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1250px; height: 140px; display: flex; justify-content: center; align-items: center; }}
      .cap span {{ display: inline-block; background: #fff; color: #2B2B2B; font-weight: 900; font-size: 66px; line-height: 1.25; padding: 14px 40px; border-radius: 22px; border-bottom: 8px solid #C8102E; white-space: nowrap; box-shadow: 0 10px 26px rgba(122,27,38,.18); }}
      .cap b {{ color: #C8102E; font-weight: 900; }}
      .cta {{ position: absolute; left: 90px; right: 90px; top: 1470px; text-align: center; font-weight: 900; font-size: 36px; color: #7A1B26; }}
      .cta i {{ font-style: normal; color: #C8102E; }}
      .logo {{ position: absolute; left: 0; right: 0; top: 1545px; display: flex; justify-content: center; align-items: center; gap: 14px; font-weight: 900; font-size: 34px; }}
      .logo img {{ width: 72px; height: 70px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="short-{key}" data-width="1080" data-height="1920" data-duration="{total}">
    <div class="bar"></div>
    <div class="title">{title}</div>
    <div class="frame"><div class="scaler">
{chr(10).join(hosts)}
    </div></div>
    <div class="cta">전체 영상은 <i>관련 동영상</i>에서 · 카카오톡 <i>canlog</i></div>
    <div class="logo"><img src="assets/img/aa-canada-logo-transparent.png" alt="" />AA Canada</div>
{chr(10).join(foots)}
{chr(10).join(voice)}
{bgm}{cap_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo(".title div", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, stagger: 0.15, ease: "back.out(1.6)" }}, 0.1);
{chr(10).join('      ' + x for x in trans)}
      window.__timelines["short-{key}"] = tl;
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    slots, _ = timing.build()
    plan = {}
    for key, sh, segs, total in windows(slots):
        html = short_html(key, sh, segs, total, slots)
        open(os.path.join(OUT, f"short-{key}", "index.html"), "w", encoding="utf-8").write(html)
        plan[key] = dict(total=total, segs=segs)
        print(f"short-{key}: {total:.1f}s  " + " + ".join(f"{g['sid']}[{g['r0']}-{g['r1']}] {g['dur']:.1f}s" for g in segs))
    json.dump(plan, open(os.path.join(OUT, "shorts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
