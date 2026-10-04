#!/usr/bin/env python3
"""Assemble index.html from src/index.template.txt + scenes.json + voice_alignment.json.

Scene windows follow the real narration length. Captions and reveals are anchored to
substrings of each scene's `tts` text via ElevenLabs character timings, so they stay in
sync after any re-voice.

Template placeholders:
  %%S_<scene-id>%%  → data-start/data-duration for that scene's <section>
  %%TOTAL%% %%CAPTIONS%% %%AUDIO%% %%COUNTERS%% %%CUES%% %%STARTS%% %%DURS%%
  %%BRAND%% %%TOPIC%% %%BGM_VOLUME%%
"""
import json, os, re, subprocess, sys

cfg = json.load(open("scenes.json"))
st = cfg.get("settings", {})
scenes = cfg["scenes"]
GAP = float(st.get("gap", 0.2))     # silence between scenes
TAIL = float(st.get("tail", 1.2))   # hold on the last scene after the last word

al = {a["id"]: a for a in json.load(open("voice_alignment.json"))}
order = [s["id"] for s in scenes]
tts = {s["id"]: s["tts"] for s in scenes}
missing = [i for i in order if i not in al]
if missing:
    sys.exit(f"no narration for {missing} — run gen_tts.py first")

start, t = {}, 0.0
for sid in order:
    start[sid] = round(t, 3)
    t += al[sid]["duration"] + GAP
dur = {sid: round(al[sid]["duration"] + GAP, 3) for sid in order}
dur[order[-1]] = round(al[order[-1]]["duration"] + TAIL, 3)
TOTAL = round(start[order[-1]] + dur[order[-1]], 3)


def cue(sid, sub):
    text = tts[sid]
    if "".join(al[sid]["chars"]) != text:
        sys.exit(f"{sid}: tts text changed since voicing — rerun gen_tts.py")
    idx = text.find(sub)
    if idx < 0:
        sys.exit(f"{sid}: anchor '{sub}' not found in tts text")
    return round(start[sid] + al[sid]["starts"][idx], 3)


# captions ─ each [display, anchor]; shown from its anchor until the next anchor
cap_html, CUE = [], {}
for s in scenes:
    sid, items = s["id"], s.get("captions", [])
    scene_end = start[sid] + al[sid]["ends"][-1] + 0.12
    for i, (txt, anchor) in enumerate(items):
        a = cue(sid, anchor)
        e = cue(sid, items[i + 1][1]) if i + 1 < len(items) else scene_end
        if sid == order[-1] and i + 1 == len(items):
            e = TOTAL
        cap_html.append(
            f'<div id="cap-{sid}-{i}" class="clip cap" data-start="{a:.3f}" data-duration="{e - a:.3f}" '
            f'data-track-index="20"><span class="cap-pill">{txt}</span></div>')
        CUE[f"{sid}|{anchor}"] = a
    for sub in s.get("cues", []):
        CUE[f"{sid}|{sub}"] = cue(sid, sub)

audio_html = [
    f'<audio id="vo-{sid}" src="assets/voice/{sid}.mp3" data-start="{start[sid]:.3f}" '
    f'data-duration="{al[sid]["duration"]:.3f}" data-track-index="30" data-volume="1"></audio>'
    for sid in order]
n = len(order)
counter_html = [
    f'<div id="cnt-{sid}" class="clip counter" data-start="{start[sid]:.3f}" data-duration="{dur[sid]:.3f}" '
    f'data-track-index="11"><span class="counter-txt">{i + 1:02d} <i>/</i> {n:02d}</span></div>'
    for i, sid in enumerate(order)]

html = open("src/index.template.txt", encoding="utf-8").read()
for sid in order:
    html = html.replace(f"%%S_{sid}%%", f'data-start="{start[sid]:.3f}" data-duration="{dur[sid]:.3f}"')
html = (html.replace("%%TOTAL%%", f"{TOTAL:.3f}")
            .replace("%%CAPTIONS%%", "\n      ".join(cap_html))
            .replace("%%AUDIO%%", "\n      ".join(audio_html))
            .replace("%%COUNTERS%%", "\n      ".join(counter_html))
            .replace("%%CUES%%", json.dumps(CUE, ensure_ascii=False))
            .replace("%%STARTS%%", json.dumps(start))
            .replace("%%DURS%%", json.dumps(dur))
            .replace("%%BRAND%%", st.get("brand", "AA CANADA"))
            .replace("%%TOPIC%%", st.get("topic", ""))
            .replace("%%BGM_VOLUME%%", str(st.get("bgm_volume", 0.12))))
left = sorted(set(re.findall(r"%%[A-Z_0-9a-z\-]+%%", html)))
if left:
    sys.exit(f"unfilled placeholders: {left} (scene ids in template must match scenes.json)")
open("index.html", "w", encoding="utf-8").write(html)

if os.path.exists("assets/music/bgm.mp3"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "assets/music/bgm.mp3", "-af",
                    f"atrim=0:{TOTAL},afade=t=in:d=0.6,afade=t=out:st={max(TOTAL - 2.5, 0)}:d=2.5",
                    "-b:a", "160k", "assets/music/bgm-fit.mp3"], check=True)
else:
    print("! no assets/music/bgm.mp3 — remove the #bgm <audio> or run gen_bgm.py", file=sys.stderr)

print(f"TOTAL {TOTAL}s")
for sid in order:
    print(f"  {sid:<16} start {start[sid]:>7.2f}  dur {dur[sid]:>6.2f}")
