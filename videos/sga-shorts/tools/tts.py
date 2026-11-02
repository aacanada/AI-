"""ElevenLabs narration for one short: python3 -I tools/tts.py <N> [--force]   (run from videos/sga-shorts)

Voice "일곱번째" (vxpRrQegUpenYtez6hz1), eleven_multilingual_v2, one call per sentence row with character
timestamps (cached per row; re-called only when that row's TTS text changes or with --force).
Rows are joined with GAP seconds of silence after a HOOK lead -> assets/voice/sN.wav + sN.timing.json.
"""
import base64
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts import SHORTS  # noqa: E402

VOICE_ID, VOICE_NAME, MODEL = "vxpRrQegUpenYtez6hz1", "일곱번째", "eleven_multilingual_v2"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}
GAP = 0.5


def call(text, mp3):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY missing")
    body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS})
    r = subprocess.run(["curl", "-sS", "-f", "-X", "POST",
                        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
                        "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json", "-d", body],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("ElevenLabs failed: " + r.stderr[:300])
    d = json.loads(r.stdout)
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    assert "".join(d["alignment"]["characters"]) == text
    return d["alignment"]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def main():
    n = int(sys.argv[1])
    sp = SHORTS[n]
    os.makedirs("assets/voice", exist_ok=True)
    t, rows, parts = sp.get("hook", 2.0), [], []
    for k, (disp, text) in enumerate(sp["rows"]):
        mp3, aj = f"assets/voice/s{n}-r{k + 1}.mp3", f"assets/voice/s{n}-r{k + 1}.align.json"
        cached = os.path.exists(aj) and json.load(open(aj, encoding="utf-8")).get("text") == text
        if "--force" in sys.argv or not cached:
            al = call(text, mp3)
            json.dump(dict(text=text, alignment=al), open(aj, "w", encoding="utf-8"), ensure_ascii=False)
        al = json.load(open(aj, encoding="utf-8"))["alignment"]
        st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
        speech0, speech1 = st[0], en[-1]
        rows.append(dict(text=disp, tts=text, at=round(t, 3), t=round(t + speech0, 3), end=round(t + speech1, 3), dur=round(dur(mp3), 3),
                         tts_starts=[round(t + x, 3) for x in st]))
        parts.append((mp3, t))
        t += dur(mp3) + GAP
    voice_end = round(t - GAP, 3)
    inputs, filt = [], []
    for i, (p, off) in enumerate(parts):
        inputs += ["-i", p]
        filt.append(f"[{i}:a]adelay={int(off * 1000)}|{int(off * 1000)}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,atrim=0:{voice_end + 0.3}[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-ac", "1",
                    f"assets/voice/s{n}.wav"], check=True)
    json.dump(dict(voice=VOICE_NAME, voice_id=VOICE_ID, model=MODEL, hook=sp.get("hook", 2.0), voice_end=voice_end, rows=rows),
              open(f"assets/voice/s{n}.timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"s{n}: voice ends {voice_end}s")


if __name__ == "__main__":
    main()
