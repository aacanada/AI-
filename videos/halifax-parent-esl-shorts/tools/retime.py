"""Lay out the voice-QC'd caption chunks (assets/audio/chunks, from voice_qc.py) with breathing pauses
so the motion graphics can land, and hold each scene before the next. Writes assets/audio/narration.wav + timing.json."""
import json, subprocess, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "script.json").read_text())
AUD = ROOT / "assets" / "audio"
SR = 44100
LEAD = 0.3
PAUSE = 0.45                       # default pause between chunks
PAUSES = {                         # (scene, after-chunk) -> pause seconds
    ("s1-hook", 0): 0.55,
    ("s2-rule", 0): 0.7,  ("s2-rule", 1): 0.75,
    ("s3-school", 1): 0.55, ("s3-school", 2): 0.75,
    ("s4-weeks", 0): 0.7, ("s4-weeks", 1): 0.95, ("s4-weeks", 2): 0.6,
    ("s5-price", 0): 0.35, ("s5-price", 1): 0.85,
    ("s6-parents", 0): 0.7, ("s6-parents", 1): 0.75, ("s6-parents", 2): 0.75,
    ("s7-cta", 0): 0.7,
}
HOLD = {"s1-hook": 0.55, "s2-rule": 1.5, "s3-school": 1.5, "s4-weeks": 3.4,
        "s5-price": 2.0, "s6-parents": 2.8, "s7-cta": 3.8}

def decode(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)

def fade(x, ms=12):
    n = min(len(x) // 2, int(SR * ms / 1000))
    if n:
        x = x.copy(); r = np.linspace(0, 1, n, dtype=np.float32); x[:n] *= r; x[-n:] *= r[::-1]
    return x

pieces, timing, t = [], {"scenes": []}, LEAD
CH = AUD / "chunks"  # QC'd chunks from .claude/skills/shorts-video/scripts/voice_qc.py
for sc in spec["scenes"]:
    sid = sc["id"]
    scene_start = 0.0 if not timing["scenes"] else t
    if timing["scenes"]:
        t += 0.25  # short breath after the scene cut
    caps = []
    for i, (disp, _) in enumerate(sc["chunks"]):
        meta = json.loads((CH / f"{sid}-{i}.json").read_text())
        seg = fade(decode(CH / f"{sid}-{i}.wav"))
        pieces.append((t, seg))
        caps.append({"text": disp, "start": round(t + meta["speech_start"], 3), "speech_end": round(t + meta["speech_end"], 3),
                     "place": round(t, 4), "take": meta["take"], "src_start": meta["src_start"], "removed": meta["removed"]})
        t += len(seg) / SR
        if i < len(sc["chunks"]) - 1:
            t += PAUSES.get((sid, i), PAUSE)
    audio_end = t
    t += HOLD[sid]
    for i in range(len(caps) - 1):
        caps[i]["end"] = caps[i + 1]["start"]
    caps[-1]["end"] = round(t, 3)
    for c in caps:
        c["end"] = round(c["end"], 3)
    timing["scenes"].append({"id": sid, "start": round(scene_start, 3), "duration": round(t - scene_start, 3),
                             "audio_end": round(audio_end, 3), "captions": caps})
total = round(t, 3)
timing["total"] = total
out = np.zeros(int(total * SR) + SR, dtype=np.float32)
for off, seg in pieces:
    a = int(off * SR); out[a:a + len(seg)] += seg
out = out[: int(total * SR)]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                str(AUD / "narration.wav")], input=out.tobytes(), check=True)
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print("total", total)
for s in timing["scenes"]:
    print(s["id"], s["start"], s["duration"], [c["start"] for c in s["captions"]])
