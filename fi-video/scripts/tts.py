"""Generate per-line ElevenLabs narration, build one narration track, and write timing.

Usage: python3 scripts/tts.py [--redo line-id,...]
Writes assets/voice/<line-id>.mp3 (cached), assets/narration.wav, timing.json.

Each take is transcribed with ElevenLabs speech-to-text; filler sounds ("어", "음"...) and
non-speech events are cut out, leading/trailing silence is trimmed, and a take whose
transcript drifts from the script is re-generated (up to 3 tries) and reported.
"""
import difflib, json, os, re, subprocess, sys, urllib.request, uuid, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, "narration.json"), encoding="utf-8"))
voice = os.environ[cfg["voice_id_env"]]
key = os.environ["ELEVENLABS_API_KEY"]
vdir = os.path.join(ROOT, "assets", "voice")
os.makedirs(vdir, exist_ok=True)
redo = set(sys.argv[2].split(",")) if len(sys.argv) > 2 and sys.argv[1] == "--redo" else set()
scenes = cfg["scenes"]
FILLERS = {"어", "음", "아", "으", "흠", "엄", "어어", "음음", "에", "읍"}


def synth(line, prev_text, next_text, force=False):
    out = os.path.join(vdir, line["id"] + ".mp3")
    spoken = line.get("tts", line["text"])
    stamp = out + ".txt"
    if not force and os.path.exists(out) and os.path.exists(stamp) and open(stamp, encoding="utf-8").read() == spoken:
        return out
    body = {
        "text": spoken,
        "model_id": cfg["model_id"],
        "voice_settings": cfg.get("voice_settings", {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}),
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


def stt(path):
    """ElevenLabs scribe transcript with word timings (cached next to the take)."""
    cache = path + ".stt.json"
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(path):
        return json.load(open(cache, encoding="utf-8"))
    boundary = uuid.uuid4().hex
    fields = {"model_id": "scribe_v1", "language_code": "kor", "tag_audio_events": "true", "timestamps_granularity": "word"}
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\n"
             "Content-Type: audio/mpeg\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
                                 headers={"xi-api-key": key, "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    json.dump(d, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return d


def norm(t):
    return re.sub(r"[^0-9A-Za-z가-힣]", "", t)


# Words this voice tends to improvise. A transcribed word is only treated as one when the
# script itself does not contain it as a word (STT mishearings like 불어→부러 stay intact).
IMPROVISED = {"저", "뭐", "이제", "그", "막", "좀", "교우", "이", "자", "그냥", "약간"}


def is_filler(w, line=None):
    """Filler sound, audio event, or an improvised word the script never says."""
    if w["type"] == "audio_event":
        return True
    if w["type"] != "word":
        return False
    t = norm(w["text"])
    if t in FILLERS:
        return True
    if line is not None and t in IMPROVISED:
        tokens = {norm(x) for x in (line.get("tts", line["text"]) + " " + line["text"]).split()}
        return t not in tokens
    return False


def inner_fillers(words, line):
    """Fillers between real words (edge ones are trimmed anyway), plus long silent gaps
    where the transcriber dropped a hesitation."""
    real = [i for i, w in enumerate(words) if w["type"] == "word" and not is_filler(w, line)]
    if not real:
        return []
    found = [w for w in words[real[0]:real[-1]] if is_filler(w, line)]
    for a, b in zip(real, real[1:]):
        if words[b]["start"] - words[a]["end"] > 0.75:
            found.append({"text": f"<gap {words[b]['start'] - words[a]['end']:.1f}s>"})
    return found


def similarity(transcript, line):
    got = norm(transcript)
    return max(difflib.SequenceMatcher(None, got, norm(line.get("tts", line["text"]))).ratio(),
               difflib.SequenceMatcher(None, got, norm(line["text"])).ratio())


def clean(path, words, line):
    """Decode, cut filler spans, trim edges. Returns (pcm bytes, list of cut spans)."""
    a = pcm(path)
    n = len(a) // 2
    real = [w for w in words if w["type"] == "word" and not is_filler(w, line)]
    cuts = [(max(0, w["start"] - 0.04), w["end"] + 0.04) for w in words if is_filler(w, line)]
    head = max(0.0, real[0]["start"] - 0.12) if real else 0.0
    tail = min(n / RATE, real[-1]["end"] + 0.3) if real else n / RATE
    keep, t = [], head
    for c0, c1 in sorted(cuts):
        if c1 <= t or c0 >= tail:
            continue
        keep.append((t, max(t, c0)))
        t = c1
    keep.append((t, tail))
    out = b"".join(a[int(x * RATE) * 2:int(y * RATE) * 2] for x, y in keep if y > x)
    return out, [c for c in cuts if c[0] < tail and c[1] > head]


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
        tries = 0
        p = synth(ln, prev_t, next_t, force=ln["id"] in redo)
        best = None
        while True:
            tr = stt(p)
            sim = similarity(tr.get("text", ""), ln)
            fill = inner_fillers(tr.get("words", []), ln)
            score = (sim >= 0.7, -len(fill), sim)
            if best is None or score > best[0]:
                best = (score, p, tr, sim)
                if p.endswith(".mp3"):
                    keep = p[:-4] + ".best.mp3"
                    subprocess.check_call(["cp", p, keep])
                    subprocess.check_call(["cp", p + ".stt.json", keep + ".stt.json"])
            if (sim >= 0.7 and not fill) or tries >= 3:
                break
            tries += 1
            why = f"fillers {[w['text'] for w in fill]}" if fill else f"similarity {sim:.2f}"
            print(f"  retake {ln['id']} ({why}): {tr.get('text')}")
            p = synth(ln, prev_t, next_t, force=True)
        _, p, tr, sim = best
        p = p[:-4] + ".best.mp3"
        a, cuts = clean(p, tr.get("words", []), ln)
        for c in cuts:
            print(f"  cut {ln['id']} {c[0]:.2f}-{c[1]:.2f}s")
        if sim < 0.7:
            print(f"  CHECK {ln['id']} similarity {sim:.2f}: {tr.get('text')}")
        d = len(a) / 2 / RATE
        sc["lines"].append({"id": ln["id"], "text": ln["text"], "start": round(local, 3), "duration": round(d, 3)})
        chunks.append(a)
        local += d
        if i + 1 < len(lines):
            chunks.append(silence(cfg["gap"]))
            local += cfg["gap"]
    tail = s.get("tail", cfg["tail"])
    local += tail
    chunks.append(silence(tail))
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
