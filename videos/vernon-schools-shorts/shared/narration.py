"""Owner-recorded narration -> assets/audio/narration.wav + timing.json.

Usage: python3 shared/narration.py <short-dir> <audio-dir>
  <audio-dir> holds short-N_s1.m4a ... (N = script.json "n"; one file per scene, in scene order).

Per file: ffmpeg trim leading/trailing silence (silenceremove), light denoise (afftdn), loudness normalise
(loudnorm I=-16) -> wav.  Scenes are joined with a 0.35 s gap.  Caption chunks inside a scene are split by
TTS-text character ratio (good enough for 2-4 short chunks; refine by hand if a chunk drifts).
Stops with an error if any scene file is missing.
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
SRC = pathlib.Path(sys.argv[2]).resolve()
spec = json.loads((ROOT / "script.json").read_text())
out = ROOT / "assets" / "audio"
out.mkdir(parents=True, exist_ok=True)
GAP, LEAD, TAIL = 0.35, 0.25, 1.6

files = [SRC / f"short-{spec['n']}_s{k + 1}.m4a" for k in range(len(spec["scenes"]))]
missing = [f.name for f in files if not f.exists()]
if missing:
    sys.exit("missing recordings: " + ", ".join(missing))

FILT = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
        "afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11")


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


timing, t, parts = {"scenes": []}, LEAD, []
for k, (sc, f) in enumerate(zip(spec["scenes"], files)):
    wav = out / f"{sc['id']}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-af", FILT, "-ar", "44100", "-ac", "1", str(wav)], check=True)
    d = dur(wav)
    weights = [max(1, len(tts.replace(" ", ""))) for _, tts in sc["chunks"]]
    tot, acc, caps = sum(weights), 0.0, []
    for (disp, _), w in zip(sc["chunks"], weights):
        caps.append({"text": disp, "start": round(t + d * acc / tot, 3), "end": round(t + d * (acc + w) / tot, 3)})
        acc += w
    timing["scenes"].append({"id": sc["id"], "start": round(t - (LEAD if k == 0 else GAP / 2), 3),
                             "audio_start": round(t, 3), "audio_dur": round(d, 3), "captions": caps, "file": f.name})
    parts.append((wav, t))
    t += d + GAP
total = round(t - GAP + TAIL, 2)
for i, s in enumerate(timing["scenes"]):
    nxt = timing["scenes"][i + 1]["start"] if i + 1 < len(timing["scenes"]) else total
    s["start"] = max(0.0, s["start"]); s["duration"] = round(nxt - s["start"], 3)
    for j in range(len(s["captions"]) - 1):
        s["captions"][j]["end"] = s["captions"][j + 1]["start"]
    s["captions"][-1]["end"] = round(min(nxt, s["captions"][-1]["end"] + 0.3), 3)
timing["total"] = total
inputs, filt = [], []
for i, (p, off) in enumerate(parts):
    inputs += ["-i", str(p)]
    filt.append(f"[{i}:a]adelay={int(off * 1000)}|{int(off * 1000)}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-ac", "1",
                str(out / "narration.wav")], check=True)
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print("total", total)
for s in timing["scenes"]:
    print(s["id"], s["file"], "start", s["start"], "audio", s["audio_dur"])
