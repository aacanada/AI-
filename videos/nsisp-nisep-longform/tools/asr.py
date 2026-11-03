"""ElevenLabs Scribe word timestamps for the narration (caption timing + QC).
    python3 -I tools/asr.py [S1 ...]  -> assets/voice/asr/SN.json"""
import json, os, sys, uuid, urllib.request

AUD = os.path.join("..", "..", "plans", "nsisp-nisep-longform", "audio")
OUT = os.path.join("assets", "voice", "asr")
os.makedirs(OUT, exist_ok=True)
for k in (sys.argv[1:] or [f"S{i}" for i in range(1, 10)]):
    f = os.path.join(AUD, k + ".mp3")
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"language_code\"\r\n\r\nko\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() \
        + open(f, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    json.dump(d, open(os.path.join(OUT, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"[{k}]", d["text"])
