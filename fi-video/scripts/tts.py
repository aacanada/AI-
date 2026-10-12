"""Generate per-line ElevenLabs narration, build one narration track, and write timing.

Usage: python3 scripts/tts.py [scene-id ...]   (default: all scenes in narration.json)
Writes assets/voice/<line-id>.mp3 (cached), assets/narration.wav, timing.json.
"""
import json, os, subprocess, sys, urllib.request, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, "narration.json"), encoding="utf-8"))
voice = os.environ[cfg["voice_id_env"]]
key = os.environ["ELEVENLABS_API_KEY"]
vdir = os.path.join(ROOT, "assets", "voice")
os.makedirs(vdir, exist_ok=True)
only = set(sys.argv[1:])
scenes = [s for s in cfg["scenes"] if not only or s["id"] in only]


def synth(line, prev_text, next_text):
    out = os.path.join(vdir, line["id"] + ".mp3")
    spoken = line.get("tts", line["text"])
    stamp = out + ".txt"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp, encoding="utf-8").read() == spoken:
        return out
    body = {
        "text": spoken,
        "model_id": cfg["model_id"],
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True},
    }
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r, open(out, "wb") as f:
        f.write(r.read())
    open(stamp, "w", encoding="utf-8").write(spoken)
    print("synth", line["id"])
    return out


RATE = 44100


def pcm(path):
    """Decode to 44.1k mono s16 so durations are exact sample counts."""
    return subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(RATE),
                                    "-f", "s16le", "-"])


def silence(sec):
    return b"\x00\x00" * int(round(sec * RATE))


timing = {"scenes": []}
chunks = []
t = 0.0
for s in scenes:
    lines = s["lines"]
    sc = {"id": s["id"], "start": round(t, 3), "lines": []}
    local = cfg["lead"]
    chunks.append(silence(cfg["lead"]))
    for i, ln in enumerate(lines):
        prev_t = lines[i - 1].get("tts", lines[i - 1]["text"]) if i else None
        next_t = lines[i + 1].get("tts", lines[i + 1]["text"]) if i + 1 < len(lines) else None
        p = synth(ln, prev_t, next_t)
        a = pcm(p)
        d = len(a) / 2 / RATE
        sc["lines"].append({"id": ln["id"], "text": ln["text"], "start": round(local, 3), "duration": round(d, 3)})
        chunks.append(a)
        local += d
        if i + 1 < len(lines):
            chunks.append(silence(cfg["gap"]))
            local += cfg["gap"]
    local += cfg["tail"]
    chunks.append(silence(cfg["tail"]))
    sc["duration"] = round(local, 3)
    t += local
    timing["scenes"].append(sc)
timing["total"] = round(t, 3)

with wave.open(os.path.join(ROOT, "assets", "narration.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(b"".join(chunks))
json.dump(timing, open(os.path.join(ROOT, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps({s["id"]: [s["start"], s["duration"]] for s in timing["scenes"]}, ensure_ascii=False), "total", timing["total"])
