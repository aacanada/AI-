# ElevenLabs TTS per scene from NARRATION.txt (script text sent unchanged).
# Usage: python3 tts.py s01 s02 ...   (no args = all scenes)
# Voice "여덟번째" is looked up by name; model fixed to eleven_multilingual_v2.
import json, os, re, sys, urllib.request

P = '/home/user/AI-/plans/montreal-multilang-longform'
MODEL = 'eleven_multilingual_v2'
KEY = os.environ['ELEVENLABS_API_KEY']


def api(path, body=None):
    req = urllib.request.Request('https://api.elevenlabs.io' + path, headers={'xi-api-key': KEY, 'Content-Type': 'application/json'},
                                 data=json.dumps(body).encode() if body else None)
    return urllib.request.urlopen(req, timeout=300)


voices = json.load(api('/v1/voices'))['voices']
match = [v for v in voices if v['name'] == '여덟번째']
if len(match) != 1:
    sys.exit('voice "여덟번째" not found uniquely')
VID = match[0]['voice_id']

txt = open(P + '/NARRATION.txt', encoding='utf-8').read()
blocks = dict(re.findall(r'\[(s\d\d)\]\n(.*?)(?=\n\[s\d\d\]|\Z)', txt, re.S))
# TTS-input-only respelling (approved 2026-10-31; script/captions keep the original word)
TTS_ONLY = {'s09': [('canlog', os.environ.get('CANLOG_SAY', '캔로그'))]}
ids = sys.argv[1:] or sorted(blocks)
log = json.load(open(P + '/audio/tts_log.json')) if os.path.exists(P + '/audio/tts_log.json') else {}
for k in ids:
    text = blocks[k].strip()
    for a, b in TTS_ONLY.get(k, []):
        text = text.replace(a, b)
    r = api(f'/v1/text-to-speech/{VID}?output_format=mp3_44100_128',
            {'text': text, 'model_id': MODEL, 'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}})
    open(f'{P}/audio/mlang_{k}.mp3', 'wb').write(r.read())
    log.setdefault(k, []).append({'voice_id': VID, 'model_id': MODEL, 'request_id': r.headers.get('request-id'), 'chars': len(text), 'tts_input_overrides': TTS_ONLY.get(k, [])})
    print(k, 'ok', r.headers.get('request-id'))
json.dump(log, open(P + '/audio/tts_log.json', 'w'), ensure_ascii=False, indent=1)
