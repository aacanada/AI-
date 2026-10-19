"""TEMPORARY timing.json (no audio yet): each chunk lasts len(TTS text) x 0.13 s.
Usage: python3 shared/estimate_timing.py <short-dir>
Replaced by narration.py once the owner's recordings (short-N_sK.m4a) arrive."""
import json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
spec = json.loads((ROOT / "script.json").read_text())
CPS, PAUSE, GAP, LEAD, TAIL = 0.13, 0.18, 0.35, 0.25, 1.6

timing, t = {"scenes": [], "estimated": True}, LEAD
for k, sc in enumerate(spec["scenes"]):
    caps, a0 = [], t
    for disp, tts in sc["chunks"]:
        d = len(tts) * CPS
        caps.append({"text": disp, "start": round(t, 3), "end": round(t + d, 3)})
        t += d + PAUSE
    t -= PAUSE
    timing["scenes"].append({"id": sc["id"], "start": round(a0 - (LEAD if k == 0 else GAP / 2), 3),
                             "audio_start": round(a0, 3), "audio_dur": round(t - a0, 3), "captions": caps})
    t += GAP
total = round(t - GAP + TAIL, 2)
for i, s in enumerate(timing["scenes"]):
    nxt = timing["scenes"][i + 1]["start"] if i + 1 < len(timing["scenes"]) else total
    s["start"] = max(0.0, s["start"]); s["duration"] = round(nxt - s["start"], 3)
    for j in range(len(s["captions"]) - 1):
        s["captions"][j]["end"] = s["captions"][j + 1]["start"]
    s["captions"][-1]["end"] = round(min(nxt, s["captions"][-1]["end"] + 0.3), 3)
timing["total"] = total
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print("estimated total", total)
