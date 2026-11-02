# Splice re-generated sentences (NARRATION_TTS.txt) into the original audio_v2 scene files at the
# original sentence start times, so the already-rendered picture and subtitles stay in sync.
# Usage: python3 splice.py s01=<new.mp3>:<new_asr.json> s06=... ; writes audio_v2_pron/ (all 9 scenes)
import json, re, sys, os, shutil, difflib, subprocess
import numpy as np

P = '/home/user/AI-/plans/vancouver-esl-free-edu'
SR = 44100
KEYS = ['AA Canada', '17,000달러', '5,000달러', '1,400달러', '2027-28']
OUT = P + '/audio_v2_pron'
os.makedirs(OUT, exist_ok=True)


def blocks(path):
    t = open(path, encoding='utf-8').read()
    return dict(re.findall(r'\[(s\d\d)\]\n(.*?)(?=\n\[s\d\d\]|\Z)', t, re.S))


ORIG, TTS = blocks(P + '/NARRATION.txt'), blocks(P + '/NARRATION_TTS.txt')
def norm(s):
    # make 'AA Canada' / ASR 'AA 캐나다' / TTS '에이에이 캐나다' comparable for alignment
    for x, y in (('Canada', '캐나다'), ('AEA', '에이에이'), ('AAA', '에이에이'), ('AA', '에이에이')):
        s = s.replace(x, y)
    return re.sub(r'[^0-9A-Za-z가-힣]', '', s)


def sentences(b):
    return [s for line in b.strip().split('\n') for s in re.split(r'(?<=[.?])\s', line) if s.strip()]


def spans(text_sents, asr_json):
    words = [w for w in json.load(open(asr_json))['words'] if w['type'] == 'word']
    a, at = '', []
    for w in words:
        n = norm(w['text'])
        for i, ch in enumerate(n):
            a += ch; d = (w['end'] - w['start']) / max(1, len(n))
            at.append((w['start'] + d * i, w['start'] + d * (i + 1)))
    s = ''.join(norm(x) for x in text_sents)
    mp = {}
    for b in difflib.SequenceMatcher(None, s, a, autojunk=False).get_matching_blocks():
        for i in range(b.size): mp[b.a + i] = b.b + i
    out, pos = [], 0
    for x in text_sents:
        n = len(norm(x)); idx = [mp[i] for i in range(pos, pos + n) if i in mp]; pos += n
        out.append((at[min(idx)][0], at[max(idx)][1]))
    return out


def load(f):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32).copy()


def atempo(x, r):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={r:.4f}', '-f', 'f32le', '-'],
                       input=x.tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(p, np.float32).copy()


report = {}
args = dict(a.split('=', 1) for a in sys.argv[1:])
for k in sorted(ORIG):
    src = f'{P}/audio_v2/vanesl_{k}.mp3'
    if k not in args:
        shutil.copy(src, f'{OUT}/vanesl_{k}.mp3'); continue
    # "<mp3>:<asr.json>" or several "<mp3>:<asr.json>@<sentence idx>" joined by ';' (per-sentence take choice)
    so, st = sentences(ORIG[k]), sentences(TTS[k])
    assert len(so) == len(st), k
    takes = {}
    for part in args[k].split(';'):
        fj, _, ix = part.partition('@')
        nf, nj = fj.split(':')
        takes[int(ix) if ix else -1] = (load(nf), spans(st, nj))
    sp_o = spans(so, f'{P}/video/asr_v2/{k}.json')
    x = load(src)
    x = np.concatenate([x, np.zeros(int(0.8 * SR), np.float32)])  # allow a little tail room
    rep = []
    for i, s in enumerate(so):
        if not any(key in s for key in KEYS): continue
        y, sp_n = takes.get(i, takes.get(-1))
        o0, o1 = sp_o[i]; n0, n1 = sp_n[i]
        lead, tail = 0.06, 0.15
        prev_end = sp_o[i - 1][1] if i else 0.0
        nxt = sp_o[i + 1][0] if i + 1 < len(so) else (len(x) / SR - 0.1)
        a = max(prev_end + 0.02, o0 - lead)
        seg = y[int(max(0, n0 - lead) * SR):int(min(len(y) / SR, n1 + tail) * SR)].copy()
        slot = (nxt - 0.06) - a
        r = 1.0
        if len(seg) / SR > slot:
            r = (len(seg) / SR) / slot
            seg = atempo(seg, r)
        f = int(0.012 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        b = int(a * SR); e = int(min(nxt - 0.03, max(o1 + tail, a + len(seg) / SR)) * SR)
        x[b:e] = 0.0
        x[b:b + len(seg)] += seg
        rep.append({'sentence': s, 'orig': [round(o0, 2), round(o1, 2)], 'new_len': round((n1 - n0), 2),
                    'placed_at': round(a, 2), 'tempo': round(r, 3)})
    # trim the added tail back to original length + whatever the last splice needs
    end = max(len(load(src)), int((max([r_['placed_at'] for r_ in rep] + [0]) + 0.1) * SR))
    last_nz = np.nonzero(np.abs(x) > 1e-4)[0]
    end = max(end, (last_nz[-1] + int(0.1 * SR)) if len(last_nz) else end)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'libmp3lame', '-b:a', '192k',
                    f'{OUT}/vanesl_{k}.mp3'], input=x[:end].tobytes(), check=True)
    report[k] = rep
json.dump(report, open(P + '/video/splice_report.json', 'w'), ensure_ascii=False, indent=1)
for k, v in report.items():
    for r_ in v: print(k, r_)
