"""Rebuild timing.json from voice files + speech-to-text word times. Run from project root."""
import difflib, json, subprocess

LEAD = {1: 1.2}
TAIL = {10: 1.0, 11: 2.5, 12: 1.5, 14: 4.0}
names = ['01-hook', '02-english-only', '03-double-edge', '04-graduation', '05-esl', '06-reveal', '07-terms',
         '08-day', '09-life', '10-duration', '11-fees', '12-one-to-one', '13-big-picture', '14-cta']
t, out = 0, []
for i, n in enumerate(names, 1):
    al = json.load(open(f'assets/voice/line{i:02d}.align.json')); text = al['text']
    stt = json.load(open(f'assets/voice/line{i:02d}.stt.json'))
    sc, stimes = [], []
    for w in stt['words']:
        if w.get('type') != 'word':
            continue
        for ch in w['text']:
            if not ch.isspace():
                sc.append(ch); stimes.append((w['start'], w['end']))
    tc = [(k, ch) for k, ch in enumerate(text) if not ch.isspace()]
    m = {}
    for a, b, size in difflib.SequenceMatcher(None, [c for _, c in tc], sc, autojunk=False).get_matching_blocks():
        for x in range(size):
            m[tc[a + x][0]] = stimes[b + x]

    def at(k, end=False):
        for j in (range(k, -1, -1) if end else range(k, len(text))):
            if j in m:
                return m[j][1] if end else m[j][0]

    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'assets/voice/line{i:02d}.mp3']))
    lead = LEAD.get(i, 0.7); tail = 1.2 + TAIL.get(i, 0)
    rows, pos = [], 0
    for row in text.split('\n'):
        rows.append({'t': round(lead + at(pos), 2), 'end': round(lead + at(pos + len(row) - 1, True), 2), 'text': row})
        pos += len(row) + 1
    ct = [round(lead + at(k), 2) if at(k) is not None else None for k in range(len(text))]
    sd = round(lead + dur + tail, 2)
    out.append({'id': n, 'idx': i, 'start': round(t, 2), 'duration': sd, 'voiceAt': lead, 'voiceDur': round(dur, 2), 'rows': rows, 'text': text, 'ct': ct})
    t += sd
json.dump(out, open('timing.json', 'w'), ensure_ascii=False)
print('scenes', len(out), 'total', round(t, 2))
for s in out:
    print(s['id'], s['duration'], [r['t'] for r in s['rows']])
