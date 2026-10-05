# ElevenLabs TTS per SCRIPT.md line → assets/voice/NN.wav + audio_meta.json (frame-keyed, word timings).
import os, re, json, base64, subprocess, urllib.request
VOICE = os.environ.get("ELEVENLABS_VOICE_ID", "9qtE9eIaqHMUAfRp4QTW")
KEY = os.environ["ELEVENLABS_API_KEY"]
TAIL = 0.6
END_HOLD = 1.4  # extra hold on the final line  # breathing room after each line (s)
src = open("SCRIPT.md", encoding="utf8").read()
lines = []
for m in re.finditer(r"## Line (\d+).*?\(Frame (\d+)\)(.*?)(?=\n## Line|\Z)", src, re.S):
    text = " ".join(l.strip() for l in m.group(3).splitlines() if l.startswith("    ")).strip()
    lines.append((int(m.group(2)), text))
os.makedirs("assets/voice", exist_ok=True)
ONLY = {int(x) for x in os.environ.get("ONLY", "").split(",") if x}
old = {v["frame"]: v for v in json.load(open("audio_meta.json"))["voices"]} if ONLY and os.path.exists("audio_meta.json") else {}
voices = []
for i, (frame, text) in enumerate(lines):
    if ONLY and frame not in ONLY:
        voices.append(old[frame]); continue
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True}}
    if i > 0: body["previous_text"] = lines[i-1][1]
    if i + 1 < len(lines): body["next_text"] = lines[i+1][1]
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    mp3 = f"assets/voice/{frame:02d}.mp3"; wav = f"assets/voice/{frame:02d}.wav"
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", f"apad=pad_dur={TAIL + (END_HOLD if frame == lines[-1][0] else 0)}", "-ar", "48000", wav], check=True)
    os.remove(mp3)
    al = r.get("alignment") or r["normalized_alignment"]
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur = [], None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur: words.append(cur); cur = None
            continue
        if cur is None: cur = {"text": "", "start": s, "end": e}
        cur["text"] += c; cur["end"] = e
    if cur: words.append(cur)
    for j, w in enumerate(words):
        w["id"] = f"w{frame:02d}_{j}"; w["start"] = round(w["start"], 3); w["end"] = round(w["end"], 3)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).strip())
    dur = round(dur, 2)
    voices.append({"frame": frame, "path": wav, "duration_s": dur, "words": words})
    print(f"frame {frame}: {dur}s  {len(words)} words  | {text[:40]}")
json.dump({"bgm": None, "bgm_pending": False, "voices": voices, "sfx": []}, open("audio_meta.json", "w"), ensure_ascii=False, indent=2)
