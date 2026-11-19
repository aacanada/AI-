#!/usr/bin/env python3
"""ElevenLabs TTS per scene (s01~s14) with character timestamps.

Reads plans/french-why-longform/NARRATION.txt verbatim (no edits), prepends [calm],
writes audio/vo/sNN.mp3 + audio/vo/sNN.json (alignment).
Usage: python3 tools/tts.py [s01 s02 ...]
"""
import base64, json, os, re, sys, urllib.request, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARR = os.path.join(ROOT, "..", "..", "plans", "french-why-longform", "NARRATION.txt")
OUT = os.path.join(ROOT, "audio", "vo")
VOICE = "S2nra0Bd5UeFVzGK3oaH"
KEY = os.environ["ELEVENLABS_API_KEY"]


def scenes():
    txt = open(NARR, encoding="utf-8").read()
    parts = re.split(r"^=== (s\d\d) ===\s*$", txt, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        lines = [l.strip() for l in parts[i + 1].strip().splitlines() if l.strip()]
        out[parts[i]] = lines
    return out


def tts(sid, lines):
    text = "[calm] " + "\n".join(lines)
    body = {
        "text": text,
        "model_id": "eleven_v4",
        "voice_settings": {"stability": 0.8, "similarity_boost": 0.75},
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")[:500]
            print(sid, "HTTP", e.code, msg, file=sys.stderr)
            if e.code in (400, 401, 403, 422):
                raise
            time.sleep(5 * (attempt + 1))
    open(os.path.join(OUT, f"{sid}.mp3"), "wb").write(base64.b64decode(data["audio_base64"]))
    meta = {"id": sid, "text": text, "lines": lines,
            "alignment": data.get("alignment"), "normalized_alignment": data.get("normalized_alignment")}
    json.dump(meta, open(os.path.join(OUT, f"{sid}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(sid, "ok", flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sc = scenes()
    ids = sys.argv[1:] or sorted(sc)
    for sid in ids:
        tts(sid, sc[sid])
