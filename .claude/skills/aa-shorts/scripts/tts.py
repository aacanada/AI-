#!/usr/bin/env python3
"""Narrate SCRIPT.md with the saved ElevenLabs voice via the API (mode A).

Each line is generated with /with-timestamps (exact word timing on the script text),
checked with speech-to-text, and retaken while the transcript shows a filler
("어,", "뭐", "음"…) or drifts from the script. Writes assets/voice/NN.wav + audio_meta.json.

  python3 tts.py --project videos/<slug> [--only 3,5] [--tries 6]
"""
import argparse, base64, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import voicelib as V

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--only", default="")
ap.add_argument("--tries", type=int, default=6)
a = ap.parse_args()

proj = os.path.abspath(a.project)
lines = V.parse_script(os.path.join(proj, "SCRIPT.md"))
frames = [l["frame"] for l in lines]
only = {int(x) for x in a.only.split(",") if x}
meta_path = os.path.join(proj, "audio_meta.json")
prev = {v["frame"]: v for v in json.load(open(meta_path))["voices"]} if os.path.exists(meta_path) and only else {}
os.makedirs(os.path.join(proj, "assets/voice"), exist_ok=True)

for i, line in enumerate(lines):
    f = line["frame"]
    if only and f not in only:
        continue
    say = V.spoken_line(line["text"])
    prev_say = V.spoken_line(lines[i - 1]["text"]) if i > 0 else None
    next_say = V.spoken_line(lines[i + 1]["text"]) if i + 1 < len(lines) else None
    wav = os.path.join(proj, f"assets/voice/{f:02d}.wav")
    clean = False
    for t in range(1, a.tries + 1):
        d = V.tts_with_timestamps(say, prev_say, next_say)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(base64.b64decode(d["audio_base64"]))
        V.to_wav(tmp.name, wav, pad=V.pad_for(f, frames))
        os.unlink(tmp.name)
        heard, _ = V.stt(wav)
        sim = max(V.similarity(line["text"], heard), V.similarity(say, heard))
        filler = bool(V.FILLER.search(" " + heard + " "))
        print(f"  line {f} take {t}: sim {sim:.2f}{' filler' if filler else ''} | {heard}")
        words = V.fold_tokens(line["text"], V.chars_from_alignment(d["alignment"]))
        take = {"frame": f, "path": f"assets/voice/{f:02d}.wav", "duration_s": round(V.ffprobe_duration(wav), 3), "words": words}
        if not filler and sim >= 0.8:
            clean = True
            break
    if not clean:
        print(f"  ⚠ line {f}: no clean take in {a.tries} tries — keeping the last one, listen to it")
    prev[f] = take
    print(f"✓ line {f}: {take['duration_s']}s")

V.write_meta(proj, list(prev.values()))
