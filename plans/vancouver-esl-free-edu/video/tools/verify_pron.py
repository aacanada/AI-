# Final check on delivered files: ASR votes on each 'AA Canada' clip + onset HF-share of '17,000' (nasal 만 vs fricative 십).
import json, subprocess, os, sys
import numpy as np
P = '/home/user/AI-/plans/vancouver-esl-free-edu'
S = '/tmp/claude-0/-home-user-AI-/40fc8476-b736-5595-8a0e-1f68d10be95d/scratchpad/verify'
os.makedirs(S, exist_ok=True)
T = {s['id']: s for s in json.load(open(P + '/video/timing.json'))['scenes']}
KEY = os.environ['ELEVENLABS_API_KEY']

def asr(f, model):
    r = subprocess.run(['curl', '-sS', 'https://api.elevenlabs.io/v1/speech-to-text', '-H', f'xi-api-key: {KEY}', '-F', f'model_id={model}',
                        '-F', 'language_code=kor', '-F', f'file=@{f}'], capture_output=True, text=True).stdout
    return json.loads(r)['text']

def clip(src, t0, t1, name):
    out = f'{S}/{name}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.2f}', '-to', f'{t1:.2f}', '-i', src, '-vn', '-ac', '1', '-ar', '16000', out], check=True)
    return out

def hf(src, st):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{st - 0.2:.2f}', '-t', '0.5', '-i', src, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32); best = 0
    for off in np.arange(0.14, 0.27, 0.01):
        a = int(off * 16000); seg = x[a:a + 1440] * np.hanning(1440)
        sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(1440, 1 / 16000)
        best = max(best, sp[fr > 3500].sum() / max(sp.sum(), 1e-9))
    return round(float(best), 3)

def aa_votes(src, t0, t1, name):
    f = clip(src, t0, t1, name)
    v = [asr(f, m) for m in ('scribe_v1', 'scribe_v2', 'scribe_v1')]
    ok = sum(('캐나다' in x) and ('카나다' not in x) for x in v)
    return ok, v

W = lambda sc, rel: T[sc]['audio_start'] + rel
items = {
  'longform video_pronfix.mp4': (P + '/renders/video_pronfix.mp4',
     [('s01', W('s01', 20.5), W('s01', 22.8)), ('s07', W('s07', 0.0), W('s07', 5.0)), ('s09', W('s09', 14.9), W('s09', 16.8))],
     [W('s07', 44.76)]),
  'longform video.mp4 (기존 공개본)': (P + '/renders/video.mp4',
     [('s01', W('s01', 20.5), W('s01', 23.0)), ('s07', W('s07', 0.0), W('s07', 4.9)), ('s09', W('s09', 14.9), W('s09', 16.8))],
     [W('s07', 44.6)]),
}
cw = [w for w in json.load(open(P + '/shorts/c/asr.json'))['words'] if w['type'] == 'word']
c17 = next(w['start'] for w in cw if '17' in w['text'])
items['short c (2026-11-02)'] = ('/home/user/AI-/publish-staging/2026-11-02-vancouver-esl-short-c/video.mp4', [('c', 0.2, 3.0)], [c17])
res = {}
for name, (src, aas, n17) in items.items():
    r = {'aa': [], 'n17': [hf(src, t) for t in n17]}
    for sc, a, b in aas:
        ok, v = aa_votes(src, a, b, (name.split()[0] + sc).replace('/', '_'))
        r['aa'].append({'where': sc, 'ok_votes': f'{ok}/3', 'asr': v})
    res[name] = r
    print(name, json.dumps(r, ensure_ascii=False))
json.dump(res, open(P + '/video/pron_verify.json', 'w'), ensure_ascii=False, indent=1)
