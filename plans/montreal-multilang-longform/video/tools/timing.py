# Build scene timing + subtitle cues from NARRATION.txt and Scribe word timestamps.
# Usage: python3 timing.py  -> video/timing.json
import json, re, difflib, subprocess

P = '/home/user/AI-/plans/montreal-multilang-longform'
ASR = P + '/video/asr'
txt = open(P + '/NARRATION.txt', encoding='utf-8').read()
blocks = dict(re.findall(r'\[(s\d\d)\]\n(.*?)(?=\n\[s\d\d\]|\Z)', txt, re.S))
LEAD, TAIL = 0.6, 0.9
norm = lambda s: re.sub(r'[\s\.,\?\!\'"·~\-]', '', s)
# caption display only: original script word + its written form (brief: 학교 이름과 용어 병기)
GLOSS = [('클라스 아께이', "클라스 아께이(classe d'accueil)"), ('피이아이', '피이아이(PEI)'),
         ('잔 망스', '잔 망스(Jeanne-Mance)'), ('콜레주 생루이', '콜레주 생루이(Collège Saint-Louis)'),
         ('데 수르스', '데 수르스(des Sources)'), ('장 그루', '장 그루(Jean-Grou)')]


PROTECT = ['한 명이', '5, 6학년에', '4개 국어가', '일반 반에서', '세 개 언어로', '두 개 언어', '세 개 언어가', '한 시간']


def chunks(sentence, maxlen=30):
    s = sentence.strip()
    for ph in PROTECT: s = s.replace(ph, ph.replace(' ', '\u00a0'))
    if len(s) <= maxlen: return [s]
    parts = [p.strip() for p in re.split(r'(?<=,) ', s)]
    out = []
    for p in parts:
        while len(p) > maxlen:
            mid = len(p) // 2
            sp = [i for i, c in enumerate(p) if c == ' ']
            cut = min(sp, key=lambda i: abs(i - mid))
            out.append(p[:cut]); p = p[cut + 1:]
        out.append(p)
    merged = []
    for p in out:
        if merged and (len(p) < 8 or len(merged[-1]) < 8) and len(merged[-1]) + len(p) < maxlen + 6:
            merged[-1] += ' ' + p
        else: merged.append(p)
    return merged


def gloss(t):
    t = t.replace('\u00a0', ' ')
    for a, b in GLOSS: t = t.replace(a, b)
    return t


scenes, cues, t = [], [], 0.0
for k in sorted(blocks):
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{P}/audio/mlang_{k}.mp3']))
    words = [w for w in json.load(open(f'{ASR}/{k}.json'))['words'] if w['type'] == 'word']
    a_chars, a_t = '', []
    for w in words:
        n = norm(w['text'])
        for i, c in enumerate(n):
            a_chars += c
            a_t.append((w['start'] + (w['end'] - w['start']) * i / max(1, len(n)), w['start'] + (w['end'] - w['start']) * (i + 1) / max(1, len(n))))
    sents = [s for line in blocks[k].strip().split('\n') for s in re.split(r'(?<=[\.\?])\s', line) if s.strip()]
    pieces = [c for s in sents for c in chunks(s, 26 if k == 's06' else 30)]
    s_chars = ''.join(norm(p) for p in pieces)
    sm = difflib.SequenceMatcher(None, s_chars, a_chars, autojunk=False)
    mp = {}
    for b in sm.get_matching_blocks():
        for i in range(b.size): mp[b.a + i] = b.b + i

    def at(idx, end=False):
        for d in range(0, 40):
            for j in ((idx - d, idx + d) if end else (idx + d, idx - d)):
                if j in mp: return a_t[mp[j]][1 if end else 0]
        return None
    start = t + LEAD
    pos = 0
    sc = {'id': k, 'start': round(t, 3), 'audio_start': round(start, 3), 'audio_dur': round(dur, 3)}
    for p in pieces:
        n = len(norm(p)); b, e = at(pos), at(pos + n - 1, True); pos += n
        cues.append({'scene': k, 'text': p.replace('\u00a0', ' '), 'show': gloss(p), 'start': round(start + b, 3), 'end': round(start + e, 3)})
    extra = 3.5 if k == 's09' else 0
    sc['dur'] = round(LEAD + dur + TAIL + extra, 3)
    scenes.append(sc); t += sc['dur']
for a, b in zip(cues, cues[1:]):
    if b['start'] - a['end'] < 0.6 and b['scene'] == a['scene']: a['end'] = b['start']
    a['end'] = min(a['end'], b['start'])
json.dump({'total': round(t, 3), 'scenes': scenes, 'cues': cues}, open(P + '/video/timing.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(t, 2))
for s in scenes: print(s['id'], s['start'], s['dur'])
for c in cues: print(f"{c['start']:8.2f} {c['end']:8.2f} {c['show']}")
