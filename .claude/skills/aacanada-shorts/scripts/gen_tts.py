#!/usr/bin/env python3
"""ElevenLabs narration per scene, with character timestamps.

Reads scenes.json → writes assets/voice/<id>.mp3 + voice_alignment.json.
Unchanged scenes (same text/voice/speed) are reused, so edits only re-voice what changed.

  python3 gen_tts.py            # voice/speed from scenes.json settings
"""
import base64, hashlib, json, os, ssl, subprocess, sys, urllib.request

API = "https://api.elevenlabs.io/v1"
KEY = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY is not set")
CA = "/root/.ccr/ca-bundle.crt"
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, context=CTX, timeout=180))


def resolve_voice(name):
    voices = call("/voices")["voices"]
    for v in voices:
        if v["name"].strip() == name.strip():
            return v["voice_id"]
    for v in voices:  # tolerate spacing differences ("네번째" vs "네 번째")
        if v["name"].replace(" ", "") == name.replace(" ", ""):
            return v["voice_id"]
    if os.environ.get("ELEVENLABS_VOICE_ID"):
        print(f"! voice '{name}' not found, using $ELEVENLABS_VOICE_ID", file=sys.stderr)
        return os.environ["ELEVENLABS_VOICE_ID"]
    sys.exit(f"voice '{name}' not found. available: {[v['name'] for v in voices]}")


cfg = json.load(open("scenes.json"))
st = cfg.get("settings", {})
scenes = cfg["scenes"]
voice_id = st.get("voice_id") or resolve_voice(st.get("voice_name", "네 번째"))
speed = float(st.get("speed", 1.12))
model = st.get("model", "eleven_multilingual_v2")
print(f"voice {voice_id} · speed {speed} · {model}")

prev = {}
if os.path.exists("voice_alignment.json"):
    prev = {a["id"]: a for a in json.load(open("voice_alignment.json"))}

os.makedirs("assets/voice", exist_ok=True)
out = []
for i, s in enumerate(scenes):
    key = hashlib.sha1(f"{s['tts']}|{voice_id}|{speed}|{model}".encode()).hexdigest()
    mp3 = f"assets/voice/{s['id']}.mp3"
    if s["id"] in prev and prev[s["id"]].get("hash") == key and os.path.exists(mp3):
        out.append(prev[s["id"]]); print(s["id"], "cached"); continue
    body = {
        "text": s["tts"], "model_id": model,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15,
                           "use_speaker_boost": True, "speed": speed},
        "previous_text": scenes[i - 1]["tts"] if i > 0 else None,
        "next_text": scenes[i + 1]["tts"] if i + 1 < len(scenes) else None,
    }
    r = call(f"/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128", body)
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    al = r["alignment"]
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3]))
    out.append({"id": s["id"], "hash": key, "path": mp3, "duration": dur, "chars": al["characters"],
                "starts": al["character_start_times_seconds"], "ends": al["character_end_times_seconds"]})
    print(s["id"], round(dur, 2), "s")
json.dump(out, open("voice_alignment.json", "w"), ensure_ascii=False)
print("total voice", round(sum(a["duration"] for a in out), 1), "s")
