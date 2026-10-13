#!/usr/bin/env python3
"""녹음 원본(assets/voice/narration.mp3)에서 말 더듬은 구간을 잘라 narration_edit.mp3를 만들고,
STT 단어 타이밍도 같은 만큼 당겨 narration_edit.words.json으로 저장한다."""
import json, subprocess, pathlib
proj = pathlib.Path(__file__).resolve().parent.parent
V = proj / "assets" / "voice"
CUTS = [  # (start, end) 초 — 원본 기준
    (44.40, 45.02),    # "RN,"
    (163.50, 164.40),  # "건물들의,"
    (356.04, 357.10),  # "참여인,"
    (596.05, 597.45),  # "휴양 도시와"
    (607.49, 608.41),  # "졸업생,"
    (623.10, 623.87),  # "어..."
    (737.51, 738.15),  # "졸업,"
    (748.05, 749.40),  # "중단 없는-"
    (791.50, 791.86),  # "정구-"
]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(V / "narration.mp3")]))
keep, cur = [], 0.0
for a, b in CUTS:
    keep.append((cur, a)); cur = b
keep.append((cur, dur))
F = 0.012
parts, labels = [], []
for i, (a, b) in enumerate(keep):
    parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d={F},afade=t=out:st={b-a-F}:d={F}[k{i}]")
    labels.append(f"[k{i}]")
fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(keep)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "narration.mp3"), "-filter_complex", fc, "-map", "[out]",
                "-ar", "44100", "-b:a", "160k", str(V / "narration_edit.mp3")], check=True)

def shift(t):
    s = 0.0
    for a, b in CUTS:
        if t >= b: s += b - a
        elif t > a: return a - s
    return t - s

stt = json.load(open(V / "narration.stt.json"))
words = []
for w in stt["words"]:
    if w.get("type") != "word": continue
    if any(a <= (w["start"] + w["end"]) / 2 <= b for a, b in CUTS): continue
    words.append({"text": w["text"], "start": round(shift(w["start"]), 3), "end": round(shift(w["end"]), 3)})
json.dump({"words": words}, open(V / "narration_edit.words.json", "w"), ensure_ascii=False)
print("removed", round(sum(b - a for a, b in CUTS), 2), "s; words", len(words))
