# Build scene timing + subtitle cues from NARRATION.txt and Scribe word timestamps.
import json, re, sys, difflib, subprocess
P = '/home/user/AI-/plans/vancouver-esl-free-edu'
ASR = sys.argv[1]
txt = open(P + '/NARRATION.txt', encoding='utf-8').read()
blocks = dict(re.findall(r'\[(s\d\d)\]\n(.*?)(?=\n\[s\d\d\]|\Z)', txt, re.S))
LEAD, TAIL = 0.6, 0.8
norm = lambda s: re.sub(r'[\s\.,\?\!\'"·~\-]', '', s)

def chunks(sentence, maxlen=30):
    s = sentence.strip()
    if len(s) <= maxlen: return [s]
    # split at commas first, then at spaces near the middle
    parts = [p.strip() for p in re.split(r'(?<=,)\s', s)]
    out = []
    for p in parts:
        while len(p) > maxlen:
            mid = len(p) // 2
            sp = [i for i, c in enumerate(p) if c == ' ']
            cut = min(sp, key=lambda i: abs(i - mid))
            out.append(p[:cut]); p = p[cut + 1:]
        out.append(p)
    # merge tiny pieces
    merged = []
    for p in out:
        if merged and (len(p) < 8 or len(merged[-1]) < 8) and len(merged[-1]) + len(p) < maxlen + 6:
            merged[-1] += ' ' + p
        else: merged.append(p)
    return merged

scenes, cues, t = [], [], 0.0
for k in sorted(blocks):
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{P}/audio/vanesl_{k}.mp3']))
    words = [w for w in json.load(open(f'{ASR}/{k}.json'))['words'] if w['type'] == 'word']
    # char-level time map for ASR text
    a_chars, a_t = '', []
    for w in words:
        n = norm(w['text'])
        for i, c in enumerate(n):
            a_chars += c
            a_t.append((w['start'] + (w['end'] - w['start']) * i / max(1, len(n)), w['start'] + (w['end'] - w['start']) * (i + 1) / max(1, len(n))))
    sents = [s for line in blocks[k].strip().split('\n') for s in re.split(r'(?<=[\.\?])\s', line) if s.strip()]
    pieces = [c for s in sents for c in chunks(s)]
    s_chars = ''.join(norm(p) for p in pieces)
    sm = difflib.SequenceMatcher(None, s_chars, a_chars, autojunk=False)
    mp = {}
    for b in sm.get_matching_blocks():
        for i in range(b.size): mp[b.a + i] = b.b + i
    def at(idx, end=False):
        # nearest mapped char
        for d in range(0, 40):
            for j in ((idx - d, idx + d) if end else (idx + d, idx - d)):
                if j in mp: return a_t[mp[j]][1 if end else 0]
        return None
    start = t + LEAD
    pos = 0
    sc = {'id': k, 'start': round(t, 3), 'audio_start': round(start, 3), 'audio_dur': round(dur, 3)}
    for p in pieces:
        n = len(norm(p)); b, e = at(pos), at(pos + n - 1, True); pos += n
        cues.append({'scene': k, 'text': p, 'start': round(start + b, 3), 'end': round(start + e, 3)})
    extra = 3.5 if k == 's09' else 0
    sc['dur'] = round(LEAD + dur + TAIL + extra, 3)
    scenes.append(sc); t += sc['dur']
# extend cue ends to next cue start (max 0.6s gap fill), no overlaps
for a, b in zip(cues, cues[1:]):
    if b['start'] - a['end'] < 0.6 and b['scene'] == a['scene']: a['end'] = b['start']
    a['end'] = min(a['end'], b['start'])
json.dump({'total': round(t, 3), 'scenes': scenes, 'cues': cues}, open(P + '/video/timing.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(t, 2))
for s in scenes: print(s['id'], s['start'], s['dur'])
for c in cues: print(c['start'], c['end'], c['text'])
