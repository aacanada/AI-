#!/usr/bin/env python3
"""Generate 2 new BGM tracks with ElevenLabs Music (instrumental, ~3 min each)."""
import json, os, sys, urllib.request, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ["ELEVENLABS_API_KEY"]
PROMPTS = {
    "A": "Bright, warm, gentle instrumental background music for an early childhood education explainer video. Ukulele and acoustic guitar lead with soft piano chords, light shaker and soft hand percussion, 96 BPM, major key, cheerful but calm and unobtrusive, steady groove, no vocals, no lyrics, no big drops.",
    "B": "Warm, light-hearted instrumental background music for a calm educational video about kindergarten teachers. Soft felt piano melody with fingerpicked acoustic guitar and plucky ukulele, gentle glockenspiel accents, light brushed percussion and claps, 98 BPM, major key, friendly and hopeful, relaxed, no vocals, no lyrics.",
}
def gen(k):
    body = {"prompt": PROMPTS[k], "music_length_ms": 180000, "model_id": "music_v1", "force_instrumental": True}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", data=json.dumps(body).encode(),
                                 method="POST", headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                open(os.path.join(ROOT, "audio", "bgm", f"el_ece_acoustic_{k}.mp3"), "wb").write(r.read())
            print(k, "ok", flush=True); return
        except urllib.error.HTTPError as e:
            print(k, "HTTP", e.code, e.read().decode(errors="ignore")[:400], flush=True)
            if e.code in (400, 401, 403, 422): raise
            time.sleep(10)
for k in sys.argv[1:] or PROMPTS:
    gen(k)
