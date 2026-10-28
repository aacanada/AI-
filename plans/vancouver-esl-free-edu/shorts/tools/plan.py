# Cut short narrations from audio_v2 by cue ranges; writes shorts/<id>/narration.wav + cues.json
import json, subprocess, os, sys
P = '/home/user/AI-/plans/vancouver-esl-free-edu'
T = json.load(open(P + '/video/timing.json'))
SC = {s['id']: s for s in T['scenes']}
CUES = T['cues']
GAP = 0.35
SPEC = {
 'a': [('s01', '밴쿠버', '아이 학비 면제'), ('bridge', 'BC주 교육부 규정에 이렇게 나와 있어요.'), ('s04', '1년 이상 학업이', '최대 1년까지 거주자로')],
 'b': [('s01', '밴쿠버', '밴쿠버'), ('s03', '부모가 학생일', '어소시에이트')],
 'c': [('s07', '그래서 AA', '의료보험')],
 'd': [('s01', '밴쿠버', '밴쿠버'), ('s08', '다만 꼭', '등록 서류를')],
}
def words(sc): return [w for w in json.load(open(f'{P}/video/asr_v2/{sc}.json'))['words'] if w['type'] == 'word']
def idx(sc, pre): return next(i for i, c in enumerate(CUES) if c['scene'] == sc and c['text'].startswith(pre))
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
for sid, segs in SPEC.items():
    if len(sys.argv) > 1 and sid not in sys.argv[1:]: continue
    out = f'{P}/shorts/{sid}'; os.makedirs(out, exist_ok=True)
    t, parts, cues = 0.25, [], []
    for seg in segs:
        if seg[0] == 'bridge':
            f = P + '/shorts/audio/bridge_a1.mp3'; b = json.load(open(P + '/shorts/audio/bridge_a1.json'))['words']
            a0, a1 = b[0]['start'] - 0.08, b[-1]['end'] + 0.15
            cues.append({'text': seg[1], 'start': round(t, 3), 'end': round(t + a1 - a0, 3)})
        else:
            sc, p0, p1 = seg; i0, i1 = idx(sc, p0), idx(sc, p1)
            base = SC[sc]['audio_start']; f = f'{P}/audio_v2/vanesl_{sc}.mp3'
            st = CUES[i0]['start'] - base
            en_c = CUES[i1]['end'] - base
            ws = [w for w in words(sc) if w['end'] <= en_c + 0.05]
            en = max(w['end'] for w in ws)
            a0, a1 = max(0, st - 0.08), min(dur(f), en + 0.15)
            for c in CUES[i0:i1 + 1]:
                cues.append({'text': c['text'], 'start': round(t + c['start'] - base - a0, 3), 'end': round(t + min(c['end'] - base, en) - a0, 3)})
        parts.append((f, a0, a1, t)); t += (a1 - a0) + GAP
    total = round(t - GAP + 1.2, 3)
    ins, fl = [], []
    for k, (f, a0, a1, at) in enumerate(parts):
        ins += ['-i', f]; ms = int(at * 1000)
        fl.append(f'[{k}:a]atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={a1 - a0 - 0.06:.3f}:d=0.06,adelay={ms}|{ms}[p{k}]')
    fl.append(''.join(f'[p{k}]' for k in range(len(parts))) + f'amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl), '-map', '[o]', out + '/narration.wav'], check=True)
    json.dump({'total': total, 'cues': cues}, open(out + '/cues.json', 'w'), ensure_ascii=False, indent=1)
    print(sid, 'total', total, 'cues', len(cues))
