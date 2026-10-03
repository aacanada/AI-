#!/usr/bin/env python3
"""Narrate SCRIPT.md with the user's ElevenLabs clone voice and emit HyperFrames audio metadata.

Usage:
  python3 tts_elevenlabs.py --project videos/<slug> [--voice-name "네 번째"] [--speed 1.1]
                            [--caption-map caption_map.json]

What it does (sequential calls — the Starter plan rejects >3 concurrent requests):
  1. Reads every "## Line N — ... (Frame N)" block's indented text from SCRIPT.md.
  2. Resolves the voice by name (falls back to the known id of "네 번째").
  3. Calls /v1/text-to-speech/{voice}/with-timestamps per line, so word timings come
     back with the audio (no Whisper / forced-alignment needed — both are blocked here).
  4. Writes assets/voice/NN.wav (44.1k mono PCM), assets/voice/alignment.json,
     audio_engine_meta.json, audio_meta.json (frame-keyed, what captions.mjs /
     assemble-index.mjs read) and narration-preview.mp3.
  5. --caption-map rewrites caption word text (e.g. "삼천삼십" -> "$3,030") so the
     narration can say numbers in Hangul while captions show figures.
"""
import argparse, base64, json, os, re, subprocess, sys, time, urllib.request, urllib.error

FALLBACK_VOICE_ID = "9qtE9eIaqHMUAfRp4QTW"  # "네 번째" (user's Korean clone)
API = "https://api.elevenlabs.io/v1"


def api(path, body=None, method=None):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method or ("POST" if data else "GET"),
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(2 ** (attempt + 1)); continue
            sys.exit(f"ElevenLabs {e.code} on {path}: {msg}")


def resolve_voice(name):
    try:
        for v in api("/voices")["voices"]:
            if v["name"].strip() == name.strip():
                return v["voice_id"]
    except SystemExit:
        pass
    print(f"· voice '{name}' not found by name — using fallback id {FALLBACK_VOICE_ID}", file=sys.stderr)
    return FALLBACK_VOICE_ID


def parse_script(text):
    lines = []
    for m in re.finditer(r"## Line \d+ — .*?\(Frame (\d+)\).*?\n\n((?:    .+\n?)+)", text, re.S):
        spoken = " ".join(l.strip() for l in m.group(2).splitlines() if l.strip())
        lines.append({"id": f"{int(m.group(1)):02d}", "text": spoken})
    return lines


def words_from_alignment(a):
    out, cur, s, e = [], "", None, None
    for c, a0, a1 in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c.isspace():
            if cur: out.append((cur, s, e)); cur = ""
            continue
        if not cur: s = a0
        cur += c; e = a1
    if cur: out.append((cur, s, e))
    return [{"id": f"w{i}", "text": t, "start": round(a0, 3), "end": round(a1, 3)} for i, (t, a0, a1) in enumerate(out)]


def apply_caption_map(words, cmap):
    for w in words:
        core = w["text"].rstrip(",.?!")
        tail = w["text"][len(core):]
        if core in cmap:
            w["text"] = cmap[core] + tail
    # "$3,030 달러," -> "$3,030," (drop the spoken unit after a figure)
    keep = []
    for w in words:
        if keep and keep[-1]["text"].startswith("$") and w["text"].startswith("달러"):
            keep[-1]["text"] = keep[-1]["text"].rstrip(",.") + w["text"][2:]
            keep[-1]["end"] = w["end"]; continue
        keep.append(w)
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice-name", default="네 번째")
    ap.add_argument("--speed", type=float, default=1.1, help="0.7–1.2; 1.1 = a little faster than conversation")
    ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--caption-map", default=None)
    ap.add_argument("--only", default=None, help="comma list of line ids to (re)generate, e.g. 03,05")
    a = ap.parse_args()

    proj = os.path.abspath(a.project)
    lines = parse_script(open(os.path.join(proj, "SCRIPT.md"), encoding="utf-8").read())
    if not lines:
        sys.exit("no '## Line N — … (Frame N)' blocks with indented text found in SCRIPT.md")
    voice = resolve_voice(a.voice_name)
    settings = api(f"/voices/{voice}/settings")
    settings["speed"] = max(0.7, min(1.2, a.speed))
    cmap = json.load(open(a.caption_map, encoding="utf-8")) if a.caption_map else {}
    only = set(a.only.split(",")) if a.only else None

    vdir = os.path.join(proj, "assets", "voice"); os.makedirs(vdir, exist_ok=True)
    align_path = os.path.join(vdir, "alignment.json")
    align = json.load(open(align_path, encoding="utf-8")) if os.path.exists(align_path) else {}
    for ln in lines:
        if only and ln["id"] not in only:
            continue
        d = api(f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
                {"text": ln["text"], "model_id": a.model, "voice_settings": settings})
        mp3 = os.path.join(vdir, f"{ln['id']}.mp3")
        open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "44100", "-ac", "1",
                        "-c:a", "pcm_s16le", os.path.join(vdir, f"{ln['id']}.wav")], check=True)
        os.remove(mp3)
        align[ln["id"]] = {"text": ln["text"], "alignment": d["alignment"]}
        print(f"  voice {ln['id']}: {d['alignment']['character_end_times_seconds'][-1]:.2f}s", file=sys.stderr)
    json.dump(align, open(align_path, "w", encoding="utf-8"), ensure_ascii=False)

    voices, frames = [], []
    for ln in lines:
        p = f"assets/voice/{ln['id']}.wav"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", os.path.join(proj, p)]))
        words = apply_caption_map(words_from_alignment(align[ln["id"]]["alignment"]), cmap)
        voices.append({"id": ln["id"], "path": p, "duration_s": round(dur, 3), "words": words})
        frames.append({"frame": int(ln["id"]), "path": p, "duration_s": round(dur, 3), "words": words})
    total = round(sum(v["duration_s"] for v in voices), 3)
    json.dump({"voices": voices, "tts_provider": "elevenlabs", "voice_id": voice, "bgm": None, "sfx": [],
               "total_voice_duration_s": total},
              open(os.path.join(proj, "audio_engine_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({"bgm": None, "bgm_pending": False, "voices": frames, "sfx": []},
              open(os.path.join(proj, "audio_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    ins = sum([["-i", os.path.join(proj, v["path"])] for v in voices], [])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex",
                    "".join(f"[{i}]" for i in range(len(voices))) + f"concat=n={len(voices)}:v=0:a=1",
                    "-b:a", "192k", os.path.join(proj, "narration-preview.mp3")], check=True)
    print(json.dumps({"voice_id": voice, "speed": settings["speed"], "lines": len(voices), "total_s": total}))


if __name__ == "__main__":
    main()
