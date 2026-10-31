# ElevenLabs Scribe (speech-to-text) word timestamps for each scene file.
# Usage: python3 asr.py s01 s02 ...   (no args = all scenes) -> video/asr/<id>.json
import json, os, sys, uuid, urllib.request

P = '/home/user/AI-/plans/montreal-multilang-longform'
KEY = os.environ['ELEVENLABS_API_KEY']
ids = sys.argv[1:] or [f's{i:02d}' for i in range(1, 10)]
for k in ids:
    b = uuid.uuid4().hex
    audio = open(f'{P}/audio/mlang_{k}.mp3', 'rb').read()
    body = (f'--{b}\r\nContent-Disposition: form-data; name="model_id"\r\n\r\nscribe_v1\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="language_code"\r\n\r\nko\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{k}.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() + audio + f'\r\n--{b}--\r\n'.encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text', data=body,
                                 headers={'xi-api-key': KEY, 'Content-Type': f'multipart/form-data; boundary={b}'})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    json.dump(d, open(f'{P}/video/asr/{k}.json', 'w'), ensure_ascii=False)
    print(f'[{k}]', d['text'])
