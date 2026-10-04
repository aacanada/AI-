"""Shared scene kit: wraps per-scene fragments into HyperFrames sub-composition files.

Placeholder `§` in css/html/js is replaced by the scene id prefix (e.g. `s01-`) so every
id stays unique in the assembled page.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DURS = json.loads((Path(__file__).parent / "durations.json").read_text())  # voice length + 0.6s per scene
CHAPTERS = ["INTRO", "WORK PERMIT · LMIA", "LMIA의 벽", "LMIA 면제 루트", "왜 몬트리올", "불어 레벨 로드맵", "정리"]

COMMON_CSS = """
@font-face { font-family: "Black Han Sans"; src: url("assets/fonts/BlackHanSans.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "IBM Plex Sans KR"; src: url("assets/fonts/PlexKR-400.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "IBM Plex Sans KR"; src: url("assets/fonts/PlexKR-700.woff2") format("woff2"); font-weight: 700; }
#root { position: absolute; inset: 0; overflow: hidden; background: #F4EFE6; color: #1E1C24;
  font-family: "IBM Plex Sans KR", sans-serif; word-break: keep-all; }
#root * { box-sizing: border-box; }
#§bg { position: absolute; inset: -60px; background-image:
  linear-gradient(rgba(30,28,36,0.07) 2px, transparent 2px),
  linear-gradient(90deg, rgba(30,28,36,0.07) 2px, transparent 2px);
  background-size: 120px 120px; }
#§glow { position: absolute; width: 1100px; height: 1100px; border-radius: 50%;
  background: radial-gradient(circle, rgba(200,16,46,0.16) 0%, rgba(200,16,46,0) 65%); }
#§ghost { position: absolute; left: 0; bottom: 40px; white-space: nowrap; font-family: "Black Han Sans";
  font-size: 380px; line-height: 1; color: rgba(30,28,36,0.06); letter-spacing: -0.02em; }
#§ghost::before { content: attr(data-t); }
#§top { position: absolute; left: 120px; right: 120px; top: 56px; height: 44px; display: flex;
  align-items: center; justify-content: space-between; }
#§chap { display: flex; align-items: center; gap: 18px; font-family: "Space Mono", monospace; font-size: 22px;
  font-weight: 700; letter-spacing: 0.08em; color: #1E1C24; }
#§chap .num { background: #1E1C24; color: #F4EFE6; padding: 4px 12px; }
#§chap .name { font-family: "IBM Plex Sans KR"; letter-spacing: 0; font-size: 24px; }
#§brand { font-family: "Space Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.18em; }
#§brand b { color: #C8102E; }
#§rail { position: absolute; left: 120px; right: 120px; bottom: 52px; height: 8px; display: flex; gap: 10px; }
#§rail i { display: block; flex: 1; height: 8px; background: rgba(30,28,36,0.14); }
#§rail i.done { background: rgba(30,28,36,0.45); }
#§rail i.on { background: #C8102E; }
.hl { font-family: "Black Han Sans", sans-serif; font-weight: 400; letter-spacing: -0.02em; line-height: 1.12; margin: 0; }
.mono { font-family: "Space Mono", monospace; font-weight: 700; letter-spacing: 0.06em; }
.red { color: #C8102E; }
.blue { color: #1F4FA0; }
.muted { color: #6A645C; }
.card { position: absolute; background: #FBF8F2; border: 4px solid #1E1C24; box-shadow: 12px 12px 0 #1E1C24; }
.chip { display: inline-block; padding: 10px 26px; border: 3px solid #1E1C24; border-radius: 999px; font-weight: 700; font-size: 34px; background: #FBF8F2; }
.stamp { position: absolute; border: 8px solid #C8102E; color: #C8102E; font-family: "Black Han Sans"; padding: 8px 34px;
  font-size: 64px; letter-spacing: 0.02em; background: rgba(244,239,230,0.92); white-space: nowrap; }
.rule { display: block; height: 4px; background: #1E1C24; transform-origin: left center; }
"""

PRELUDE_JS = """
const D = __DUR__;
const tl = gsap.timeline({ paused: true });
const E = { o: "power3.out", b: "back.out(1.7)", e: "expo.out", s: "sine.inOut" };
function up(sel, t, d = 0.6, y = 46) { tl.fromTo(sel, { opacity: 0, y: y }, { opacity: 1, y: 0, duration: d, ease: E.o }, t); }
function left(sel, t, d = 0.6, x = -70) { tl.fromTo(sel, { opacity: 0, x: x }, { opacity: 1, x: 0, duration: d, ease: E.e }, t); }
function right(sel, t, d = 0.6) { left(sel, t, d, 70); }
function pop(sel, t, d = 0.55) { tl.fromTo(sel, { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: d, ease: E.b }, t); }
function fade(sel, t, d = 0.5) { tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d, ease: "power1.out" }, t); }
function draw(sel, t, d = 0.7) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power2.inOut" }, t); }
function slam(sel, t, rot = -6) { tl.fromTo(sel, { opacity: 0, scale: 2.1, rotation: rot - 8 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.32, ease: "power4.in" }, t); }
function dim(sel, t, to = 0.28) { tl.to(sel, { opacity: to, duration: 0.5, ease: "power1.inOut" }, t); }
function stag(sel, t, each = 0.12, y = 40) { tl.fromTo(sel, { opacity: 0, y: y }, { opacity: 1, y: 0, duration: 0.55, ease: E.o, stagger: each }, t); }
function count(sel, t, from, to, d, fmt) {
  const el = document.querySelector(sel); const o = { v: from };
  tl.to(o, { v: to, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = fmt(Math.round(o.v)); } }, t);
  tl.set(o, { v: from }, 0);
}
// chrome + ambient
fade("#§bg", 0, 0.4);
tl.fromTo("#§bg", { x: 0, y: 0 }, { x: -60, y: -30, duration: D, ease: "none" }, 0);
tl.fromTo("#§glow", { scale: 0.9, opacity: 0.7 }, { scale: 1.15, opacity: 1, duration: D / 2, ease: E.s, yoyo: true, repeat: 1 }, 0);
tl.fromTo("#§ghost", { x: 40 }, { x: -260, duration: D, ease: "none" }, 0);
tl.fromTo("#§top", { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.5, ease: E.o }, 0.1);
tl.fromTo("#§rail", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.1);
"""


def chrome(sid, chapter, ghost, glow_pos):
    segs = []
    for i in range(1, 6):
        cls = "on" if i == chapter else ("done" if i < chapter else "")
        segs.append(f'<i class="{cls}"></i>')
    label = CHAPTERS[chapter]
    num = "AA" if chapter == 0 else f"CH {chapter:02d}"
    if chapter == 6:
        num = "END"
    gx, gy = glow_pos
    return f"""
  <div id="§bg" data-layout-allow-overflow></div>
  <div id="§glow" data-layout-allow-overflow style="left:{gx}px; top:{gy}px;"></div>
  <div id="§ghost" data-layout-allow-overflow data-t="{ghost}"></div>
  <div id="§top"><div id="§chap"><span class="num">{num}</span><span class="name">{label}</span></div>
    <div id="§brand">AA <b>CANADA</b></div></div>
  <div id="§rail">{''.join(segs)}</div>
"""


def build(n, chapter, ghost, css, html, js, glow=(900, -300)):
    sid = f"s{n:02d}"
    dur = DURS[str(n)]
    pre = sid + "-"
    body = chrome(sid, chapter, ghost, glow) + html
    doc = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{COMMON_CSS}
{css}
      </style>
      <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
{body}
      </div>
      <script>
(function () {{
{PRELUDE_JS.replace('__DUR__', str(dur))}
{js}
window.__timelines["{sid}"] = tl;
}})();
      </script>
    </template>
  </body>
</html>
"""
    doc = doc.replace("§", pre)
    out = ROOT / "compositions" / f"{sid}.html"
    out.write_text(doc, encoding="utf-8")
    return out
