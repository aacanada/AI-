"""Generate timing.json, compositions/*.html and index.html for the 16:9 long-form. Run from project root:
    python3 -I tools/build.py
Re-run after tools/audio_prep.py - everything re-times itself from the recordings."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing  # noqa: E402
from common import T_RE, fonts_css, scene_html  # noqa: E402
import mapkit  # noqa: E402
from scenes_a import S as SA  # noqa: E402
from scenes_b import S as SB  # noqa: E402
from scenes_c import S as SC  # noqa: E402
from script import SCENES  # noqa: E402

SPECS = {**SA, **SB, **SC}
SC_BY = {s["id"]: s for s in SCENES}
SFX = {"whoosh": (0.574, 0.22), "pop": (0.5, 0.28), "impact": (1.2, 0.22), "stamp": (1.2, 0.26)}
MAXC = 24


def resolve_T(src, slot):
    def rep(m):
        ph = m.group(1)
        k = slot["text"].find(ph)
        if k < 0:
            raise SystemExit(f"{slot['id']}: cue phrase not in narration: {ph!r}")
        return f"{slot['chars'][k]:.3f}"
    return T_RE.sub(rep, src)


def paths(s):
    return s.replace("@I/", "assets/img/")


EXPR_RE = re.compile(r"⟦(.*?)⟧")


def resolve_body(src, slot):
    """⟦expr⟧ in scene bodies: T() cues resolved to seconds, then evaluated (video data-start/duration)."""
    return EXPR_RE.sub(lambda m: f"{eval(resolve_T(m.group(1), slot), {'__builtins__': {}, 'min': min, 'max': max}):.3f}", src)


def scene_file(slot, off=0.0, duration=None, cid=None):
    """Scene composition html. off/duration/cid let the shorts host a window of the same scene."""
    sid = slot["id"]
    sp = SPECS[sid]
    cid = cid or sid
    dur = duration if duration is not None else slot["duration"]
    js = resolve_T(sp["js"], slot)
    fx = sorted((round(eval(resolve_T(e, slot), {"__builtins__": {}}), 3), n) for n, e in sp.get("sfx", []))
    aud = []
    for n, (at, name) in enumerate(fx):
        ln, vol = SFX[name]
        at -= off
        nxt = [a - off for a, _ in fx[n + 1:]]
        d = round(min(ln, dur - at, (nxt[0] - at - 0.02) if nxt else 99), 3)
        if at >= 0 and d > 0.05:
            aud.append(f'        <audio id="{cid}-fx{n}" src="assets/sfx/{name}.mp3" data-start="{at:.3f}" data-duration="{d}" '
                       f'data-track-index="30" data-volume="{vol}" data-hf-media-start-basis="local"></audio>')
    body = resolve_body(sp["body"], slot)
    if off:  # shorts window: shift scene-local media starts
        body = re.sub(r'data-start="([0-9.]+)"', lambda m: f'data-start="{float(m.group(1)) - off:.3f}"', body)
    html = paths(scene_html(cid, dur, mapkit.CSS + sp["css"], body, js, "\n".join(aud), off))
    if "T('" in html:
        raise SystemExit(f"{sid}: unresolved cue")
    return html


def chunk(text, maxc=MAXC):
    """Caption lines of <= maxc chars, split at spaces, balanced; prefer comma breaks."""
    if len(text) <= maxc:
        return [text]
    n = -(-len(text) // maxc)
    words = text.split()
    best = None

    def rec(ws, k):
        if k == 1:
            yield [" ".join(ws)]
            return
        for c in range(1, len(ws) - k + 2):
            for rest in rec(ws[c:], k - 1):
                yield [" ".join(ws[:c])] + rest

    for k in (n, n + 1, n + 2):
        if k > len(words):
            break
        for lines in rec(words, k):
            worst = max(len(x) for x in lines)
            score = (worst > maxc, worst - 3 * sum(x.endswith(",") for x in lines[:-1]))
            if best is None or score < best[0]:
                best = (score, lines)
        if best and not best[0][0]:
            break
    return best[1]


def captions(slots, maxc=MAXC, base=0.0):
    """[(start, end, line, keys)] in root time. Two lines on screen at most (one caption = one line pair)."""
    caps = []
    for s in slots:
        keys = sorted(SC_BY[s["id"]]["keys"], key=len, reverse=True)
        pos = 0
        for r in s["rows"]:
            k0 = s["text"].find(r["text"], pos)
            pos = k0 + len(r["text"])
            lines = chunk(r["text"], maxc)
            off = k0
            for ln in lines:
                k = s["text"].find(ln.split()[0], off)
                off = k + len(ln)
                caps.append([s["start"] + s["chars"][k] - base, None, ln, keys, s["start"] + r["end"] + 0.3 - base])
    caps.sort(key=lambda c: c[0])
    for i, c in enumerate(caps):
        nxt = caps[i + 1][0] if i + 1 < len(caps) else c[4]
        c[1] = min(c[4], nxt - 0.02) if nxt > c[0] else c[4]
    return caps


def hl(text, keys):
    out = text
    for k in keys:
        if k in out and "<b>" not in out:
            out = out.replace(k, f"<b>{k}</b>", 1)
    # numbers red too (brief: 숫자 강조는 레드)
    parts = re.split(r"(<b>.*?</b>)", out)
    parts = [p if p.startswith("<b>") else re.sub(r"(\d[\d,.~]*\s?(?:만\s?원대|만\s?원|천\s?원|원|%|년|명|세|달러|학년)?)", r"<b>\1</b>", p) for p in parts]
    return "".join(parts)


def bgm_lane(total, win, base=0.16, duck=0.07):
    """BGM chained beds with a ducking automation lane under the narration."""
    out, t, n, beds = "", 0.0, 0, ["bgm-a", "bgm-b"]
    while t < total - 1:
        bed = beds[n % 2]
        ln = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/music/{bed}.mp3"]))
        d = round(min(ln, total - t), 3)
        pts = [(0.0, 0.0), (2.0, base)]
        for a, b in win:
            a, b = a - t, b - t
            if b < 0 or a > d:
                continue
            pts += [(max(2.0, a - 0.3), base), (max(2.1, a), duck), (min(d - 0.1, b), duck), (min(d - 0.05, b + 0.5), base)]
        pts += [(max(pts[-1][0] + 0.01, d - 3), pts[-1][1]), (d, 0.0)]
        pts.sort()
        lane, last = [], -1
        for p in pts:
            if p[0] > last + 1e-3:
                lane.append({"t": round(p[0], 3), "v": p[1]})
                last = p[0]
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": lane}]})
        out += (f"      <audio id=\"bgm-{n}\" src=\"assets/music/{bed}.mp3\" data-start=\"{round(t, 3)}\" data-duration=\"{d}\" "
                f"data-track-index=\"{11 + n % 2}\" data-volume=\"1\" data-automation='{auto}'></audio>\n")
        t += ln - 4
        n += 1
    return out


CHROME_CSS = """
      .logo { position: absolute; right: 40px; bottom: 34px; z-index: 300; display: flex; align-items: center; gap: 12px; color: #2B2B2B; font-weight: 900; font-size: 26px; }
      .logo img { width: 64px; height: 62px; }
      .foot { position: absolute; left: 0; right: 0; top: 846px; z-index: 300; text-align: center; color: #7A1B26; font-weight: 500; font-size: 22px; opacity: .85; }
      .cap { position: absolute; left: 0; right: 0; top: 896px; height: 110px; z-index: 310; display: flex; justify-content: center; align-items: center; }
      .cap span { display: inline-block; background: #fff; color: #2B2B2B; font-weight: 700; font-size: 50px; line-height: 1.3; padding: 12px 40px; border-radius: 18px; border-bottom: 6px solid #C8102E; white-space: nowrap; box-shadow: 0 10px 26px rgba(122,27,38,.18); }
      .cap b { color: #C8102E; font-weight: 900; }
"""

if __name__ == "__main__":
    os.makedirs("compositions", exist_ok=True)
    slots, total = timing.build()
    json.dump(dict(total=total, slots=slots), open("timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    files = {}
    for s in slots:
        fn = f"{s['id']}.html"
        open(os.path.join("compositions", fn), "w", encoding="utf-8").write(scene_file(s))
        files[s["id"]] = fn

    caps = captions(slots)
    cap_html = "\n".join(
        f'      <div id="cap-{i:03d}" class="clip cap" data-start="{a:.3f}" data-duration="{max(0.2, b - a):.3f}" data-track-index="20"><span>{hl(t, keys)}</span></div>'
        for i, (a, b, t, keys, _) in enumerate(caps))

    slot_html, trans_js, whoosh = [], [], []
    for k, s in enumerate(slots):
        slot_html.append(
            f'      <div id="el-{s["id"]}" style="z-index:{k + 1}" data-composition-id="{s["id"]}" data-composition-src="compositions/{files[s["id"]]}" '
            f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="{1 + k % 2}" data-width="1920" data-height="1080"></div>')
        if k == 0:
            continue
        new, t0, d = f'"#el-{s["id"]}"', s["start"], timing.TR
        old = f'"#el-{slots[k - 1]["id"]}"'
        if k % 2:
            trans_js += [f'tl.fromTo({new},{{clipPath:"inset(0% 0% 0% 100%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:{d},ease:"power3.inOut"}},{t0});',
                         f'tl.to({old},{{x:-160,duration:{d},ease:"power3.inOut"}},{t0});']
        else:
            trans_js += [f'tl.fromTo({new},{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:{d + 0.1},ease:"power2.inOut"}},{t0});']
        whoosh.append(f'      <audio id="wh-{s["id"]}" src="assets/sfx/whoosh.mp3" data-start="{t0}" data-duration="0.574" data-track-index="13" data-volume="0.2"></audio>')

    voice = [f'      <audio id="vo-{s["id"]}" src="assets/voice/{s["id"]}.wav" data-start="{round(s["start"] + s["voiceAt"], 3)}" '
             f'data-duration="{s["voiceDur"]}" data-track-index="10" data-volume="1"></audio>' for s in slots if s["real"]]
    win = [(s["start"] + s["voiceAt"], s["start"] + s["voiceAt"] + s["voiceDur"]) for s in slots]
    bgm = bgm_lane(total, win)

    chrome = [f'      <div id="logo" class="clip logo" data-start="0" data-duration="{total}" data-track-index="5"><img src="assets/img/aa-canada-logo-transparent.png" alt="" />AA Canada</div>']
    for s in slots:
        f = SC_BY[s["id"]]["foot"]
        if f:
            chrome.append(f'      <div id="foot-{s["id"]}" class="clip foot" data-start="{round(s["start"] + s["voiceAt"], 3)}" data-duration="{round(s["voiceDur"], 3)}" data-track-index="7">{f}</div>')

    index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{fonts_css()}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #FFF8F2; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #FFF8F2; font-family: 'Noto Sans KR', sans-serif; }}
      [data-composition-id="root"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
{CHROME_CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="{total}">
{chr(10).join(slot_html)}
{chr(10).join(chrome)}
{chr(10).join(voice)}
{chr(10).join(whoosh)}
{bgm}{cap_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + x for x in trans_js)}
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
"""
    open("index.html", "w", encoding="utf-8").write(index)
    print(f"slots {len(slots)} captions {len(caps)} total {total:.1f}s ({int(total // 60)}:{total % 60:04.1f}) real-voice {sum(s['real'] for s in slots)}/{len(slots)}")
