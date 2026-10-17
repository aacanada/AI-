# Usage: python3 tts.py <project-dir> [--force]
"""Generate per-scene ElevenLabs narration with character timestamps, then build
narration.wav + timing.json (scene windows and caption chunk windows)."""
import json, os, subprocess, sys, base64, pathlib

ROOT = pathlib.Path(sys.argv[1]).resolve()  # project dir containing script.json
spec = json.loads((ROOT / "script.json").read_text())
out = ROOT / "assets" / "audio"
out.mkdir(parents=True, exist_ok=True)
key = os.environ["ELEVENLABS_API_KEY"]
GAP = 0.35  # silence between scenes (s)
LEAD = 0.25  # silence before first word

def tts(text, path):
    body = json.dumps({"text": text, "model_id": spec["model_id"],
                       "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}})
    r = subprocess.run(["curl", "-sS", "-f", "-X", "POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{spec['voice_id']}/with-timestamps?output_format=mp3_44100_128",
        "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    d = json.loads(r.stdout)
    path.write_bytes(base64.b64decode(d["audio_base64"]))
    return d["alignment"]

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())

timing, t, parts = {"scenes": []}, LEAD, []
force = "--force" in sys.argv
for sc in spec["scenes"]:
    text = " ".join(c[1] for c in sc["chunks"])
    mp3 = out / f"{sc['id']}.mp3"
    aj = out / f"{sc['id']}.align.json"
    if force or not mp3.exists():
        aj.write_text(json.dumps(tts(text, mp3), ensure_ascii=False))
    al = json.loads(aj.read_text())
    d = dur(mp3)
    chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    assert "".join(chars) == text, (sc["id"], "".join(chars), text)
    caps, pos = [], 0
    for disp, tt in sc["chunks"]:
        a, b = pos, pos + len(tt) - 1
        caps.append({"text": disp, "start": round(t + starts[a], 3), "end": round(t + ends[b], 3)})
        pos += len(tt) + 1
    # chunk shows until the next chunk begins
    for i in range(len(caps) - 1):
        caps[i]["end"] = caps[i + 1]["start"]
    timing["scenes"].append({"id": sc["id"], "start": round(t - (LEAD if not parts else GAP / 2), 3),
                             "audio_start": round(t, 3), "audio_dur": round(d, 3), "captions": caps})
    parts.append((mp3, t))
    t += d + GAP
total = round(t + 0.6, 2)
for i, s in enumerate(timing["scenes"]):
    nxt = timing["scenes"][i + 1]["start"] if i + 1 < len(timing["scenes"]) else total
    s["start"] = max(0.0, s["start"]); s["duration"] = round(nxt - s["start"], 3)
    s["captions"][-1]["end"] = round(min(nxt, s["captions"][-1]["end"] + 0.3), 3)
timing["total"] = total
# mix: place each scene at its offset
inputs, filt = [], []
for i, (p, off) in enumerate(parts):
    inputs += ["-i", str(p)]
    filt.append(f"[{i}:a]adelay={int(off*1000)}|{int(off*1000)}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-ac", "1", str(out / "narration.wav")], check=True)
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print("total", total)
for s in timing["scenes"]:
    print(s["id"], s["start"], s["duration"])
