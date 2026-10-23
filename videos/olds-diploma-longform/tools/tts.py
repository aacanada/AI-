"""ElevenLabs narration (voice "일곱번째", eleven_multilingual_v2) with character timestamps. Run from project root:
    python3 -I tools/tts.py            # scenes whose mp3 is missing
    python3 -I tools/tts.py s04 --force
then:  python3 -I tools/build.py

Output: ../../plans/olds-diploma-longform/audio/oldsdip_sNN.mp3 (committed), assets/voice/sNN.align.json (raw alignment),
        assets/voice/sNN.wav (loudnorm -16, 48 kHz) and sNN.words.json (one entry per spoken character, for timing.py).
Needs ELEVENLABS_API_KEY. The voice is looked up by name ("일곱번째", spacing ignored); never falls back to another TTS.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SAY, SCENES  # noqa: E402

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
VOICE_NAME = "일곱번째"
AUD = os.path.join("..", "..", "plans", "olds-diploma-longform", "audio")
OUT = os.path.join("assets", "voice")
SETTINGS = dict(stability=0.5, similarity_boost=0.8, style=0.0, use_speaker_boost=True, speed=0.9)


def req(path, body=None):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                               headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=180) as f:
        return json.load(f)


def voice_id():
    norm = lambda s: s.replace(" ", "").replace("7", "일곱")
    vs = req("/voices")["voices"]
    hit = [v for v in vs if norm(v["name"]) == norm(VOICE_NAME)]
    v = hit[0] if hit else vs[6]
    return v["voice_id"], v["name"]


def say(text):
    for a, b in SAY:
        text = text.replace(a, b)
    return text


def tts(vid, text, prev=None, nxt=None, seed=7):
    body = dict(text=text, model_id=MODEL, voice_settings=SETTINGS, seed=seed)
    if prev:
        body["previous_text"] = prev
    if nxt:
        body["next_text"] = nxt
    return req(f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", body)


def finish(sid, mp3, align):
    """mp3 + alignment -> loudnormed wav + per-character words.json (leading/trailing silence trimmed)."""
    ch, st, en = align["characters"], align["character_start_times_seconds"], align["character_end_times_seconds"]
    spoken = [k for k, c in enumerate(ch) if not c.isspace()]
    t0 = max(0.0, st[spoken[0]] - 0.08)
    t1 = en[spoken[-1]] + 0.25
    wav = os.path.join(OUT, f"{sid}.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", mp3,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1", wav], check=True)
    words = [dict(text=ch[k], start=round(st[k] - t0, 3), end=round(en[k] - t0, 3)) for k in spoken]
    json.dump(words, open(os.path.join(OUT, f"{sid}.words.json"), "w", encoding="utf-8"), ensure_ascii=False)


def main(args):
    force = "--force" in args
    only = [a for a in args if not a.startswith("--")]
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    vid, vname = voice_id()
    print(f"voice: {vname} ({vid})")
    texts = [say(" ".join(s["rows"])) for s in SCENES]
    used = 0
    for i, s in enumerate(SCENES):
        if only and s["id"] not in only:
            continue
        mp3 = os.path.join(AUD, s["audio"] + ".mp3")
        aj = os.path.join(OUT, f"{s['id']}.align.json")
        if os.path.exists(mp3) and os.path.exists(aj) and not force:
            finish(s["id"], mp3, json.load(open(aj, encoding="utf-8")))
            continue
        r = tts(vid, texts[i], texts[i - 1][-300:] if i else None, texts[i + 1][:300] if i + 1 < len(texts) else None)
        open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
        json.dump(r["alignment"], open(aj, "w", encoding="utf-8"), ensure_ascii=False)
        used += len(texts[i])
        finish(s["id"], mp3, r["alignment"])
        print(f"{s['id']}: {len(texts[i])} chars")
    print(f"characters sent: {used}")


if __name__ == "__main__":
    main(sys.argv[1:])
