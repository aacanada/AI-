# Generate 'AA Canada' pronunciation candidates: 6 spellings x 2 takes, same voice/model/settings.
import json, os, subprocess, urllib.request, re
import numpy as np
P = '/home/user/AI-/plans/vancouver-esl-free-edu/pron_candidates'
KEY = os.environ['ELEVENLABS_API_KEY']
TPL = '안녕하세요, {}입니다. 밴쿠버 교육청 국제학생 학비는 1년에 만 칠천 달러입니다.'
SPELL = ['에이에이캐나다', '에이 에이 캐나다', '에이에이 캐나다', '에이에이 캐내다', '에이에이,캐나다', '에이에이, 캐나다']

def tts(text, out):
    body = {'text': text, 'model_id': 'eleven_multilingual_v2', 'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}}
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/cbVXtFGe9VfUKWtbYIty?output_format=mp3_44100_192',
                                 data=json.dumps(body).encode(), headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    open(out, 'wb').write(urllib.request.urlopen(req, timeout=120).read())

def asr(f):
    r = subprocess.run(['curl', '-sS', 'https://api.elevenlabs.io/v1/speech-to-text', '-H', f'xi-api-key: {KEY}', '-F', 'model_id=scribe_v1',
                        '-F', 'language_code=kor', '-F', f'file=@{f}'], capture_output=True, text=True).stdout
    return json.loads(r)

def hf_onset(f, st):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, st - 0.06):.2f}', '-t', '0.3', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32); best = 0
    for a in range(0, 1920, 160):
        seg = x[a:a + 1440]
        if len(seg) < 1440: break
        sp = np.abs(np.fft.rfft(seg * np.hanning(1440))) ** 2; fr = np.fft.rfftfreq(1440, 1 / 16000)
        best = max(best, sp[fr > 3500].sum() / max(sp.sum(), 1e-9))
    return round(float(best), 3)

def norm16(src, dst):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    g = -16.0 - float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'volume={g:.2f}dB,alimiter=limit=0.85:level=false', '-c:a', 'libmp3lame', '-b:a', '192k', dst], check=True)

rows = []
for i, sp in enumerate(SPELL, 1):
    takes = []
    for t in (1, 2):
        raw = f'{P}/takes/후보{i}_take{t}_raw.mp3'
        tts(TPL.format(sp), raw)
        d = asr(raw); w = [x for x in d['words'] if x['type'] == 'word']
        n17 = next((x['start'] for x in w if '17' in x['text'] or '만' in x['text']), None)
        dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', raw]))
        takes.append({'take': t, 'asr': d['text'], 'hf_17k': hf_onset(raw, n17) if n17 is not None else None, 'dur': round(dur, 2), 'raw': raw})
    # pick: ASR shows Korean '캐나다' (not 카나다) and the number starts with a nasal (low HF); then the shorter (less padded) take
    def score(t):
        return (('캐나다' in t['asr'] or '캐내다' in t['asr']) and '카나다' not in t['asr'], -(t['hf_17k'] or 1), -t['dur'])
    best = max(takes, key=score)
    norm16(best['raw'], f'{P}/후보{i}.mp3')
    for t in takes:
        norm16(t['raw'], f'{P}/takes/후보{i}_take{t["take"]}.mp3'); os.remove(t['raw'])
        t['file'] = f'takes/후보{i}_take{t["take"]}.mp3'; del t['raw']
    rows.append({'no': i, 'spelling': sp, 'text': TPL.format(sp), 'chosen_take': best['take'], 'takes': takes})
    print(i, sp, 'chosen take', best['take'], [(t['asr'][:22], t['hf_17k'], t['dur']) for t in takes])
json.dump(rows, open(f'{P}/candidates.json', 'w'), ensure_ascii=False, indent=1)
