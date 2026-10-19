"""Generate timing.json, compositions/*.html and index.html. Run from project root:
    python3 -I tools/build.py
Re-run after audio/clips arrive (tools/audio_prep.py, tools/clip_prep.py) - everything re-times itself.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing  # noqa: E402
from common import FONTS, T_RE, scene_html  # noqa: E402
from scenes_a import S as SA  # noqa: E402
from scenes_b import S as SB  # noqa: E402
from scenes_c import S as SC  # noqa: E402
from script import CHAPTERS, CLIPS, SCENES  # noqa: E402
from templates import card, clip  # noqa: E402

SPECS = {**SA, **SB, **SC}
SC_BY = {s["id"]: s for s in SCENES}
CH = {c[0]: c for c in CHAPTERS}
os.makedirs("compositions", exist_ok=True)

slots, total = timing.build()
json.dump(dict(total=total, slots=slots), open("timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

SFX = {"whoosh": (0.574, 0.25, 30), "pop": (0.5, 0.30, 31), "impact": (1.2, 0.24, 32), "stamp": (1.2, 0.30, 33)}
MAXC = 22


def resolve_T(src, slot):
    def rep(m):
        ph = m.group(1)
        k = slot["text"].find(ph)
        if k < 0:
            raise SystemExit(f"{slot['id']}: cue phrase not in narration: {ph!r}")
        return f"{slot['chars'][k]:.3f}"
    return T_RE.sub(rep, src)


def paths(s):
    return s.replace("@P/", "assets/photos/").replace("@B/", "assets/brochure/")


def chunk(text):
    """Split into caption lines of <= MAXC chars at spaces, balanced (no orphan last word); prefer comma breaks."""
    if len(text) <= MAXC:
        return [text]
    n = -(-len(text) // MAXC)
    words = text.split()
    best = None

    def rec(ws, k):
        if k == 1:
            yield [" ".join(ws)]
            return
        for c in range(1, len(ws) - k + 2):
            head = " ".join(ws[:c])
            for rest in rec(ws[c:], k - 1):
                yield [head] + rest

    for k in (n, n + 1):
        for lines in rec(words, k):
            worst = max(len(x) for x in lines)
            score = (worst > MAXC, worst - 2 * sum(x.endswith(",") for x in lines[:-1]))
            if best is None or score < best[0]:
                best = (score, lines)
        if best and not best[0][0]:
            break
    return best[1]


# ------------------------------------------------------------------ compositions
files = {}
for s in slots:
    sid = s["id"]
    if s["kind"] == "card":
        c = CH[s["ch"]]
        html = card(sid, s["ch"], c[2], c[3], c[5], s["duration"], 40 + slots.index(s))
        fn = f"{sid}-chapter{s['ch']}.html"
    elif s["kind"] == "clip":
        html = clip(sid, s, CLIPS[s["clip"]], s["duration"], 40 + slots.index(s))
        fn = f"{SC_BY[sid]['name']}.html"
    else:
        sp = SPECS[sid]
        js = resolve_T(sp["js"], s)
        aud, fx = [], []
        for name, expr in sp.get("sfx", []):
            fx.append((round(eval(resolve_T(expr, s), {"__builtins__": {}}), 3), name))
        fx.sort()
        for n, (at, name) in enumerate(fx):
            ln, vol, _ = SFX[name]
            trk = 40 + slots.index(s)  # one sfx lane per scene (lint compares local times across files)
            nxt = [a for a, nm in fx[n + 1:]]
            d = round(min(ln, s["duration"] - at, (nxt[0] - at - 0.02) if nxt else 99), 3)
            if d > 0.05:
                aud.append(f'        <audio id="{sid}-fx{n}" src="assets/sfx/{name}.mp3" data-start="{at}" data-duration="{d}" data-track-index="{trk}" data-volume="{vol}" data-hf-media-start-basis="local"></audio>')
        html = scene_html(sid, s["duration"], sp["css"], sp["body"], js, sp.get("bg", ""), "\n".join(aud))
        fn = f"{SC_BY[sid]['name']}.html"
    html = paths(html)
    if "T('" in html:
        raise SystemExit(f"{sid}: unresolved cue")
    open(os.path.join("compositions", fn), "w", encoding="utf-8").write(html)
    files[sid] = fn
for f in os.listdir("compositions"):
    if f.endswith(".html") and f not in files.values():
        os.remove(os.path.join("compositions", f))

# ------------------------------------------------------------------ captions
caps = []  # (start, end, html)
for s in slots:
    if s["kind"] == "vo":
        keys = sorted(SC_BY[s["id"]].get("keys", []), key=len, reverse=True)
        pos = 0
        for r in s["rows"]:
            k0 = s["text"].find(r["text"], pos)
            pos = k0 + len(r["text"])
            lines = chunk(r["text"])
            off = k0
            for j, ln in enumerate(lines):
                k = s["text"].find(ln.split()[0], off)
                a = s["chars"][k]
                off = k + len(ln)
                caps.append([s["start"] + a, None, ln, keys, s["start"] + r["end"] + 0.25])
    elif s["kind"] == "clip":
        for sub in s["subs"]:
            lines = chunk(sub["text"])
            tot = sum(len(x) for x in lines)
            acc = 0
            for ln in lines:
                a = sub["t"] + (sub["end"] - sub["t"]) * acc / tot
                acc += len(ln)
                caps.append([s["start"] + a, None, ln, [], s["start"] + sub["end"] + 0.2])
caps.sort(key=lambda c: c[0])
for i, c in enumerate(caps):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else c[4]
    c[1] = min(c[4], nxt - 0.02) if nxt > c[0] else c[4]


def hl_all(text, keys):
    out = text
    for k in keys:
        if k in out and "<b>" not in out.split(k)[0][-3:]:
            out = re.sub(re.escape(k), f"<b>{k}</b>", out, count=1)
    return out


cap_html = "\n".join(
    f'      <div id="cap-{i:03d}" class="clip cap" data-start="{a:.3f}" data-duration="{max(0.2, b - a):.3f}" data-track-index="20"><span>{hl_all(t, keys)}</span></div>'
    for i, (a, b, t, keys, _) in enumerate(caps))

# ------------------------------------------------------------------ slots + transitions
slot_html, trans_js, whoosh = [], [], []
for k, s in enumerate(slots):
    slot_html.append(
        f'      <div id="el-{s["id"]}" style="z-index:{k + 1}" data-composition-id="{s["id"]}" data-composition-src="compositions/{files[s["id"]]}" '
        f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="{1 + k % 2}" data-width="1920" data-height="1080"></div>')
    if k == 0:
        continue
    old, new, t0, d = f'"#el-{slots[k - 1]["id"]}"', f'"#el-{s["id"]}"', s["start"], s["ov"]
    tr = s["trans_in"]
    if tr == "zoom":
        trans_js += [f'tl.to({old},{{scale:1.22,filter:"blur(14px)",opacity:0,duration:{d},ease:"power2.in"}},{t0});',
                     f'tl.fromTo({new},{{scale:0.86,filter:"blur(14px)",opacity:0}},{{scale:1,filter:"blur(0px)",opacity:1,duration:{d},ease:"power2.out"}},{t0});']
    elif tr == "leak":
        trans_js += [f'tl.fromTo("#fx-leak",{{opacity:0,x:-500}},{{opacity:0.95,x:0,duration:{d * 0.55},ease:"power1.in"}},{t0});',
                     f'tl.to("#fx-leak",{{opacity:0,x:500,duration:{d * 0.6},ease:"power2.out"}},{t0 + d * 0.55});',
                     f'tl.fromTo({new},{{opacity:0}},{{opacity:1,duration:0.05}},{t0 + d * 0.5});']
    elif tr == "flash":
        trans_js += [f'tl.fromTo("#fx-flash",{{opacity:0}},{{opacity:1,duration:{d * 0.45},ease:"power2.in"}},{t0});',
                     f'tl.to("#fx-flash",{{opacity:0,duration:{d * 0.55},ease:"power2.out"}},{t0 + d * 0.45});',
                     f'tl.fromTo({new},{{opacity:0}},{{opacity:1,duration:0.03}},{t0 + d * 0.43});']
    elif tr == "fade":
        trans_js += [f'tl.fromTo({new},{{opacity:0,scale:1.06}},{{opacity:1,scale:1,duration:{d},ease:"power2.out"}},{t0});']
    elif tr == "wipe":
        trans_js += [f'tl.fromTo({new},{{clipPath:"inset(0% 0% 0% 100%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:{d},ease:"power3.inOut"}},{t0});',
                     f'tl.to({old},{{x:-140,duration:{d},ease:"power3.inOut"}},{t0});']
    elif tr == "slide":
        trans_js += [f'tl.fromTo({new},{{x:1920}},{{x:0,duration:{d},ease:"power3.inOut"}},{t0});',
                     f'tl.to({old},{{x:-480,opacity:0.4,duration:{d},ease:"power3.inOut"}},{t0});']
    whoosh.append(f'      <audio id="wh-{s["id"]}" src="assets/sfx/whoosh.mp3" data-start="{t0}" data-duration="0.574" data-track-index="13" data-volume="0.22"></audio>')

# ------------------------------------------------------------------ narration audio
voice = []
for s in slots:
    if s["kind"] == "vo" and s["real"]:
        voice.append(f'      <audio id="vo-{s["id"]}" src="assets/voice/{s["id"]}.wav" data-start="{round(s["start"] + s["voiceAt"], 3)}" '
                     f'data-duration="{s["voiceDur"]}" data-track-index="10" data-volume="1"></audio>')

# ------------------------------------------------------------------ BGM (chain + ducking lane)
import subprocess  # noqa: E402

LV_BASE, LV_VO, LV_CLIP = 0.18, 0.09, 0.063  # clip duck = -24 dB
win = []
for s in slots:
    if s["kind"] == "vo":
        win.append((s["start"] + s["voiceAt"], s["start"] + s["voiceAt"] + s["voiceDur"], LV_VO))
    elif s["kind"] == "clip":
        win.append((s["start"] + s["clipAt"], s["start"] + s["content"], LV_CLIP))


def level_points(g0, g1):
    pts = [(g0, LV_BASE)]
    for a, b, lv in win:
        if b < g0 or a > g1:
            continue
        pts += [(max(g0, a - 0.3), LV_BASE), (max(g0, a), lv), (min(g1, b), lv), (min(g1, b + 0.4), LV_BASE)]
    pts.append((g1, LV_BASE))
    pts.sort()
    # merge: drop BASE bumps shorter than 1 s between two ducks
    out = []
    for p in pts:
        if out and abs(p[0] - out[-1][0]) < 1e-3:
            out[-1] = p
        else:
            out.append(p)
    return out


bgm, t, n, beds = "", 0.0, 0, ["bgm-a", "bgm-b"]
while t < total - 1:
    bed = beds[n % 2]
    ln = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/music/{bed}.mp3"]))
    d = round(min(ln, total - t), 3)
    pts = level_points(t, t + d)
    lane = [{"t": round(p[0] - t, 3), "v": p[1]} for p in pts]
    lane[0]["v"] = 0 if n else 0.0
    lane.insert(1, {"t": 2.5, "v": pts[0][1]}) if lane[1]["t"] > 2.5 else None
    lane[-1]["v"] = 0
    if d - 3 > lane[-2]["t"]:
        lane.insert(-1, {"t": round(d - 3, 3), "v": LV_BASE})
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": lane}]})
    bgm += f"      <audio id=\"bgm-{n}\" src=\"assets/music/{bed}.mp3\" data-start=\"{round(t, 3)}\" data-duration=\"{d}\" data-track-index=\"{11 + n % 2}\" data-volume=\"1\" data-automation='{auto}'></audio>\n"
    t += ln - 4
    n += 1

# ------------------------------------------------------------------ chrome: brand line, chapter pill, footnotes
chrome = [f'      <div id="brand" class="clip brand" data-start="0" data-duration="{total}" data-track-index="5"><i></i>AA CANADA · 토론토 조기유학</div>']
ch_start = {}
for s in slots:
    ch_start.setdefault(s["ch"], s["start"])
chs = sorted(ch_start)
for i, c in enumerate(chs):
    a = ch_start[c]
    b = ch_start[chs[i + 1]] if i + 1 < len(chs) else total
    chrome.append(f'      <div id="pill-{c}" class="clip chpill" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="6">CH {c} · {CH[c][1]}</div>')
for s in slots:
    f = SC_BY.get(s["id"], {}).get("foot")
    if f and s["kind"] == "vo":
        a = round(s["start"] + s["voiceAt"], 3)
        chrome.append(f'      <div id="foot-{s["id"]}" class="clip foot" data-start="{a}" data-duration="{round(s["voiceDur"], 3)}" data-track-index="7">{f}</div>')

index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #14254a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #14254a; font-family: Pretendard, sans-serif; }}
      [data-composition-id="root"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      .brand {{ position: absolute; left: 56px; top: 40px; z-index: 300; display: flex; align-items: center; gap: 12px; color: rgba(255,255,255,.88); font-weight: 800; font-size: 24px; letter-spacing: .06em; text-shadow: 0 2px 8px rgba(0,0,0,.45); }}
      .brand i {{ display: block; width: 12px; height: 12px; border-radius: 50%; background: #c8102e; box-shadow: 18px 0 0 #e8b931; margin-right: 18px; }}
      .chpill {{ position: absolute; right: 56px; top: 32px; z-index: 300; padding: 8px 22px; border-radius: 99px; background: rgba(11,22,48,.78); border: 2px solid #e8b931; color: #fff; font-weight: 800; font-size: 24px; }}
      .foot {{ position: absolute; left: 0; right: 0; top: 826px; z-index: 300; text-align: center; color: rgba(255,255,255,.6); font-weight: 500; font-size: 22px; text-shadow: 0 1px 6px rgba(0,0,0,.6); }}
      .cap {{ position: absolute; left: 0; right: 0; top: 880px; height: 100px; z-index: 310; display: flex; justify-content: center; align-items: center; }}
      .cap span {{ display: inline-block; background: rgba(8,16,36,.78); color: #fff; font-weight: 700; font-size: 52px; line-height: 1.3; padding: 12px 36px; border-radius: 16px; white-space: nowrap; }}
      .cap b {{ color: #e8b931; font-weight: 700; }}
      #fx-flash {{ position: absolute; inset: 0; z-index: 200; background: #fff; opacity: 0; pointer-events: none; }}
      #fx-leak {{ position: absolute; left: -400px; top: -300px; width: 2720px; height: 1680px; z-index: 200; opacity: 0; pointer-events: none;
        background: radial-gradient(ellipse at 35% 45%, rgba(255,214,140,.95) 0%, rgba(255,160,80,.55) 30%, rgba(200,16,46,.25) 55%, rgba(200,16,46,0) 75%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="{total}">
{chr(10).join(slot_html)}
      <div id="fx-flash"></div>
      <div id="fx-leak"></div>
{chr(10).join(chrome)}
{chr(10).join(voice)}
{chr(10).join(whoosh)}
{bgm}{cap_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#fx-flash", {{ opacity: 0 }}, 0);
      tl.set("#fx-leak", {{ opacity: 0, x: 0 }}, 0);
{chr(10).join('      ' + x for x in trans_js)}
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(index)
real = sum(1 for s in slots if s["kind"] == "vo" and s["real"])
print(f"slots {len(slots)} captions {len(caps)} total {total:.1f}s ({int(total // 60)}:{total % 60:04.1f}) real-voice {real}/29 clips-with-video {sum(1 for s in slots if s['kind'] == 'clip' and s['has_video'])}/4")
