"""ElevenLabs Scribe check of the narration files. Usage: python3 -I tools/asr.py [s01 ...] [--take path.mp3]
-> assets/voice/asr/<id>.json and prints the recognised text (for pronunciation QC)."""
import json, os, sys, uuid, urllib.request

AUD = os.path.join("..", "..", "plans", "olds-diploma-longform", "audio")
OUT = os.path.join("assets", "voice", "asr")
os.makedirs(OUT, exist_ok=True)
args = sys.argv[1:]
files = [(a, a) for a in args if a.endswith(".mp3")] or \
        [(k, os.path.join(AUD, f"oldsdip_{k}.mp3")) for k in (args or [f"s{i:02d}" for i in range(1, 10)])]
for k, f in files:
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"language_code\"\r\n\r\nko\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() \
        + open(f, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    name = os.path.basename(k).replace(".mp3", "")
    json.dump(d, open(os.path.join(OUT, f"{name}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"[{name}]", d["text"])
