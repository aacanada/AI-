"""Facecam shorts A–C (1080x1920) cut from the facecam longform (videos/alexander-free-edu-longform).
Inputs (made there): timing-facecam.json, assets/audio/narration-facecam.wav, assets/facecam/face_l.mp4 (the same
edit, 1920x1080), renders/graphics.mp4 (the motion-graphics scenes alone, on the same timeline).
Layout (revised after the owner's review): graphics are the main picture, caption under them; the face shows only in a small
16:9 window (no extra zoom) for the opening window and the key line,
last 2 s "전체 영상은 관련 동영상에서 ▶" card. Only the owner's own spoken lines, ≤ 59 s.
Usage: python3 tools/build.py → short-a.html, short-b.html, short-c.html (+ assets/media/*) → render -c short-a.html …"""
import json, pathlib, subprocess, sys, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
LF = ROOT.parent / "alexander-free-edu-longform"
sys.path.insert(0, str(ROOT.parent / "_kit"))
from pyk import r, hl_html

T = json.loads((LF / "timing-facecam.json").read_text())
SC = T["scenes"]
FPS = 30
CARD = 2.2  # closing "full video" card
GFX_Y, GFX_H, SEAM = 226, 608, 864

SHORTS = {
    "a": dict(title=("사립 컬리지도 ", "자녀무상교육", " 된다?"), sub="밴쿠버 기준은 '학위 과정'",
              ranges=[(0, 0, 3), (1, 4, 5), (1, 9, 11), (1, 12, 13), (1, 15, 16), (2, 0, 0), (2, 4, 5), (2, 8, 10)],
              emph=[(1, 15)], cards=[(0, 7.4, "사립은 <b>안 된다?</b>", "공립만 가야 된다는 말, 들어 보셨죠")], thumb=("사립인데", "무상?", "기준은 '학위 과정'")),
    "b": dict(title=("엄마는 한 학기 ", "3과목", ""), sub="수업은 집에서 라이브로",
              ranges=[(3, 1, 4), (3, 6, 9), (3, 16, 18), (4, 1, 2), (4, 6, 7), (4, 10, 14)],
              emph=[(3, 16)], cards=[(0, None, "부모님 걱정 1순위 <b>공부량</b>", "아이 케어하면서 공부할 수 있을까?"), (3, None, "<b>라이브</b> 온라인 수업", "녹화 강의가 아닌 실시간 수업")], thumb=("엄마는", "3과목", "수업은 집에서 라이브로")),
    "c": dict(title=("듀오링고 90점 · ", "아이 학비 0원", ""), sub="학비 한 학기 $5,940",
              ranges=[(5, 0, 3), (5, 4, 4), (5, 6, 9), (6, 0, 2), (6, 5, 10)],
              emph=[(6, 9)], thumb=("아이 학비", "0원?", "영어 90점 · 한 학기 $5,940")),
}
HL = ["자녀무상교육", "무상교육", "사립", "공립", "1년 이상", "학위", "어떤 과정", "BC 주정부", "승인한", "몇 안 되는", "9학점", "9시간", "3과목씩만", "풀타임",
      "라이브", "실시간", "집에서", "픽업", "110점", "90점", "조건부 입학", "English 099", "첫 학기부터", "660달러", "5,940달러", "18,000달러", "20,000달러", "2명, 3명", "메리트"]


def fr(t):
    return round(t * FPS) / FPS


def window(i, j0, j1):
    caps = SC[i]["captions"]
    prev_end = caps[j0 - 1]["speech_end"] if j0 else SC[i]["start"]
    nxt = caps[j1 + 1]["start"] if j1 + 1 < len(caps) else SC[i]["start"] + SC[i]["duration"]
    return fr(max(caps[j0]["start"] - 0.1, prev_end + 0.02)), fr(min(caps[j1]["speech_end"] + 0.28, nxt - 0.02))


def run(cmd):
    subprocess.run(cmd, check=True)


def media(key, wins):
    m = ROOT / "assets" / "media"
    m.mkdir(parents=True, exist_ok=True)
    # voice: each window with 30 ms fades, butt-joined
    fl = [f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{k}]" for k, (a, b) in enumerate(wins)]
    fl.append("".join(f"[a{k}]" for k in range(len(wins))) + f"concat=n={len(wins)}:v=0:a=1[out]")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(LF / "assets/audio/narration-facecam.wav"), "-filter_complex", ";".join(fl), "-map", "[out]",
         "-ar", "48000", "-ac", "1", str(m / f"short-{key}-voice.wav")])
    for name, src, vf in [("face", LF / "assets/facecam/face_l.mp4", "scale=640:360:flags=lanczos"), ("gfx", LF / "renders/graphics.mp4", f"scale=1080:{GFX_H}:flags=lanczos")]:
        fl = [f"[0:v]trim=start_frame={round(a * FPS)}:end_frame={round(b * FPS)},setpts=PTS-STARTPTS[v{k}]" for k, (a, b) in enumerate(wins)]
        fl.append("".join(f"[v{k}]" for k in range(len(wins))) + f"concat=n={len(wins)}:v=1:a=0,{vf},fps={FPS},format=yuv420p[out]")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", ";".join(fl), "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "16",
             "-preset", "medium", "-g", "30", str(m / f"short-{key}-{name}.mp4")])
    total = sum(b - a for a, b in wins) + CARD
    run(["ffmpeg", "-y", "-v", "error", "-ss", "8", "-i", str(ROOT / "assets/bgm/bgm.mp3"), "-af",
         f"afade=t=in:d=0.5,afade=t=out:st={total - 2.0:.2f}:d=2.0", "-t", f"{total:.2f}", "-ar", "48000", "-ac", "2", str(m / f"short-{key}-bed.wav")])
    return round(total, 3)


def build(key, cfg):
    wins = [window(i, j0, j1) for i, j0, j1 in cfg["ranges"]]
    total = media(key, wins) if "--no-media" not in sys.argv else round(sum(b - a for a, b in wins) + CARD, 3)
    speech = round(total - CARD, 3)
    caps, joins, emph, at = [], [], [], 0.0
    starts = []
    for (i, j0, j1), (a, b) in zip(cfg["ranges"], wins):
        for j in range(j0, j1 + 1):
            c = SC[i]["captions"][j]
            s0 = at + max(0.0, c["start"] - a)
            s1 = at + min(b - a, (SC[i]["captions"][j + 1]["start"] if j < j1 else b) - a)
            caps.append((c["text"], round(s0, 3), round(s1, 3)))
            if (i, j) in cfg["emph"]:
                emph.append((round(max(0.0, s0 - 0.2), 3), round(s1 + 0.2, 3)))
        starts.append((round(at, 3), round(b - a, 3)))
        at += b - a
        joins.append(round(at, 3))
    joins = joins[:-1]
    emph.insert(0, (0.0, joins[0]))  # face window: the opening line(s) + the key line only
    t0, t1, t2 = cfg["title"]
    cap_divs = "\n      ".join(
        f'<div id="cap-{k}" class="clip cap" data-start="{r(s)}" data-duration="{r(e - s)}" data-track-index="3"><div class="cap-box" id="cap-{k}-box">'
        f'<span class="cap-text">{hl_html(t, HL)}</span></div></div>' for k, (t, s, e) in enumerate(caps))
    card_divs = "\n      ".join(
        f'<div id="card-{n}" class="clip card-o" data-start="{r(starts[w][0])}" data-duration="{r(d or starts[w][1])}" data-track-index="7">'
        f'<div class="co-in" id="card-{n}-in"><div class="co-t">{t}</div><div class="co-s">{html.escape(sub)}</div></div></div>'
        for n, (w, d, t, sub) in enumerate(cfg.get("cards", [])))
    cap_divs = card_divs + "\n      " + cap_divs
    page = (ROOT / "tools" / "template.html").read_text()
    rep = dict(KEY=key, TOTAL_MINUS=r(total - speech), SPEECH_M=r(max(0, speech - 0.2)), TOTAL=r(total), SPEECH=r(speech), TITLE=f'{html.escape(t0)}<b>{html.escape(t1)}</b>{html.escape(t2)}', SUB=html.escape(cfg["sub"]),
               CAPTIONS=cap_divs, JOINS=json.dumps(joins), EMPH=json.dumps(emph), CAPS=json.dumps([[s, e] for _, s, e in caps]))
    for k, v in rep.items():
        page = page.replace(f"__{k}__", v)
    (ROOT / f"short-{key}.html").write_text(page)
    print(f"short-{key}: {total:.2f}s (speech {speech:.2f}s), {len(wins)} windows, joins {joins}, emph {emph}")
    return total


if __name__ == "__main__":
    import shutil
    for f in ("kit.js", "base.css"):
        shutil.copy(ROOT.parent / "_kit" / f, ROOT / "assets" / "kit" / f)
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for k, cfg in SHORTS.items():
        if not only or k in only:
            build(k, cfg)
