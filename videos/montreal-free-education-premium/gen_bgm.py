#!/usr/bin/env python3
"""Instrumental music bed from ElevenLabs Music, sized to the narration.

  python3 gen_bgm.py ["optional custom prompt"]
Writes assets/music/bgm.mp3 (build.py trims + fades it to the final length).
"""
import json, os, ssl, sys, urllib.request

DEFAULT_PROMPT = (
    "Elegant, premium instrumental for an educational short video about studying abroad in Canada. "
    "Soft felt piano motif, warm light strings, subtle pulsing synth bass and gentle percussion, "
    "confident and inspiring, steady 110 BPM, no vocals, consistent energy, clean resolved ending."
)
KEY = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY is not set")
CA = "/root/.ccr/ca-bundle.crt"
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()

cfg = json.load(open("scenes.json"))
al = json.load(open("voice_alignment.json"))
total = sum(a["duration"] for a in al) + 0.2 * len(al) + 2
prompt = sys.argv[1] if len(sys.argv) > 1 else cfg.get("settings", {}).get("bgm_prompt", DEFAULT_PROMPT)
body = {"prompt": prompt, "music_length_ms": int(min(max(total, 10), 300) * 1000), "force_instrumental": True}
req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                             data=json.dumps(body).encode(),
                             headers={"xi-api-key": KEY, "Content-Type": "application/json"})
os.makedirs("assets/music", exist_ok=True)
data = urllib.request.urlopen(req, context=ctx, timeout=300).read()
open("assets/music/bgm.mp3", "wb").write(data)
print(f"bgm {len(data)//1024} KB, {body['music_length_ms']/1000:.0f}s")
