#!/usr/bin/env python3
"""Build index.html for the Francophone Mobility long-form.

Re-run after dropping HeyGen clips into ../heygen/S1_face.mp4 and ../heygen/S9_face.mp4:
the S1/S9 placeholders are swapped for the face videos (their own audio is used, the
S1/S9 narration mp3 is dropped) and every later scene shifts to the clip length.
"""
import json, os, re, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GAP = 0.6
LEAD = 0.4
ENDCARD = 4.0


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                 '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)


def silences(p):
    err = subprocess.run(['ffmpeg', '-i', p, '-af', 'silencedetect=noise=-30dB:d=0.15', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    return [(a + b) / 2 for a, b in zip(st, en)]


def scene_texts():
    t = open(os.path.join(ROOT, 'SCRIPT.md'), encoding='utf-8').read()
    out = {}
    for sid, body in re.findall(r'^## (S\d)\..*?\n(.*?)(?=^## |^---|\Z)', t, flags=re.S | re.M):
        lines = [l for l in body.strip().split('\n') if l and not l.startswith('- 화면')]
        out[sid] = ' '.join(lines).replace('[calm]', '').strip()
    return out


def chunk(sentence, limit=34):
    if len(sentence) <= limit:
        return [sentence]
    parts, cur = [], ''
    for tok in re.split(r'(?<=,)\s+|\s+', sentence):
        if cur and len(cur) + 1 + len(tok) > limit:
            parts.append(cur)
            cur = tok
        else:
            cur = (cur + ' ' + tok).strip()
    if cur:
        parts.append(cur)
    # avoid a tiny orphan last chunk
    if len(parts) > 1 and len(parts[-1]) < 8:
        last = parts.pop()
        parts[-1] += ' ' + last
    return parts


def captions_for(text, audio):
    d = dur(audio)
    sil = silences(audio)
    sents = [s for s in re.split(r'(?<=[.?!])\s+', text) if s.strip()]
    w = [len(s.replace(' ', '')) for s in sents]
    total = sum(w)
    speech0, speech1 = 0.15, d - 0.25
    bounds, acc = [speech0], 0
    for x in w[:-1]:
        acc += x
        guess = speech0 + (speech1 - speech0) * acc / total
        near = [s for s in sil if abs(s - guess) < 1.6 and s > bounds[-1] + 0.6]
        bounds.append(min(near, key=lambda s: abs(s - guess)) if near else guess)
    bounds.append(speech1)
    caps = []
    for i, s in enumerate(sents):
        a, b = bounds[i], bounds[i + 1]
        parts = chunk(s)
        pw = [len(p.replace(' ', '')) for p in parts]
        t = a
        for p, x in zip(parts, pw):
            e = t + (b - a) * x / sum(pw)
            caps.append({'t': round(t, 2), 'e': round(e, 2), 'text': p, 'sent': i})
            t = e
    return caps


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    texts = scene_texts()
    ids = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
    faces = {}
    for sid in ('S1', 'S9'):
        src = os.path.join(ROOT, 'heygen', f'{sid}_face.mp4')
        if os.path.exists(src):
            dst = os.path.join(HERE, 'assets', 'heygen', f'{sid}_face.mp4')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
            faces[sid] = f'assets/heygen/{sid}_face.mp4'
    scenes, t = {}, LEAD
    for sid in ids:
        audio = os.path.join(HERE, 'assets', 'audio', f'{sid}.mp3')
        media = os.path.join(HERE, faces[sid]) if sid in faces else audio
        d = dur(media)
        caps = captions_for(texts[sid], audio)
        if sid in faces:  # stretch caption timing to the face clip
            k = d / dur(audio)
            for c in caps:
                c['t'] = round(c['t'] * k, 2)
                c['e'] = round(c['e'] * k, 2)
        scenes[sid] = {'start': round(t, 2), 'dur': round(d, 2), 'caps': caps}
        t += d + GAP
    end_start = round(t - GAP + 0.6, 2)
    total = round(end_start + ENDCARD, 2)

    tpl = open(os.path.join(HERE, 'template.html.tpl'), encoding='utf-8').read()

    # audio + face media
    media_html = []
    for i, sid in enumerate(ids):
        sc = scenes[sid]
        if sid in faces:
            media_html.append(
                f'<video id="face-{sid}" class="face-video" src="{faces[sid]}" playsinline data-has-audio="true" '
                f'data-start="{sc["start"]}" data-duration="{sc["dur"]}" data-track-index="1" data-volume="1"></video>')
        else:
            media_html.append(
                f'<audio id="vo-{sid}" src="assets/audio/{sid}.mp3" data-start="{sc["start"]}" '
                f'data-duration="{sc["dur"]}" data-track-index="20" data-volume="1"></audio>')
    # music bed with ducking lane
    pts = [{'t': 0, 'v': 0.0}, {'t': 1.2, 'v': 0.55}]
    for sid in ids:
        sc = scenes[sid]
        a, b = sc['start'], sc['start'] + sc['dur']
        pts += [{'t': round(max(a - 0.35, 1.3), 2), 'v': 0.55}, {'t': round(a, 2), 'v': 0.16},
                {'t': round(b, 2), 'v': 0.16}, {'t': round(b + 0.35, 2), 'v': 0.55}]
    pts += [{'t': round(total - 1.8, 2), 'v': 0.55}, {'t': total, 'v': 0.0}]
    pts.sort(key=lambda p: p['t'])
    lane = json.dumps({'version': 1, 'lanes': [{'target': 'volume', 'points': pts}]})
    media_html.append(
        f'<audio id="music-bed" src="assets/bgm.mp3" data-start="0" data-duration="{total}" '
        f'data-track-index="30" data-volume="1" data-automation=\'{lane}\'></audio>')

    # scene slots
    slot_html = []
    for sid in ids:
        sc = scenes[sid]
        slot_html.append(f'<section id="slot-{sid}" class="clip scene" data-start="{sc["start"]}" '
                         f'data-duration="{sc["dur"]}" data-track-index="2">'
                         f'<div class="scene-inner" id="in-{sid}">{{{{{sid}}}}}</div></section>')
    slot_html.append(f'<section id="slot-END" class="clip scene" data-start="{end_start}" '
                     f'data-duration="{ENDCARD}" data-track-index="2"><div class="scene-inner" id="in-END">{{{{END}}}}</div></section>')

    # captions
    cap_html = []
    n = 0
    for sid in ids:
        sc = scenes[sid]
        for c in sc['caps']:
            n += 1
            a = round(sc['start'] + c['t'], 2)
            d = round(max(c['e'] - c['t'], 0.4), 2)
            cap_html.append(f'<div id="cap{n}" class="clip cap" data-start="{a}" data-duration="{d}" '
                            f'data-track-index="5"><span class="cap-text">{esc(c["text"])}</span></div>')

    timing = {sid: {'start': scenes[sid]['start'], 'dur': scenes[sid]['dur'],
                    'caps': [[c['t'], c['text']] for c in scenes[sid]['caps']]} for sid in ids}
    timing['END'] = {'start': end_start, 'dur': ENDCARD, 'caps': []}

    parts = json.load(open(os.path.join(HERE, 'scenes.json'), encoding='utf-8'))
    html = tpl.replace('/*TOTAL*/', str(total))
    html = html.replace('<!--MEDIA-->', '\n      '.join(media_html))
    html = html.replace('<!--SLOTS-->', '\n      '.join(slot_html))
    html = html.replace('<!--CAPS-->', '\n      '.join(cap_html))
    html = html.replace('/*TIMING*/', json.dumps(timing, ensure_ascii=False))
    html = html.replace('/*FACES*/', json.dumps(sorted(faces)))
    for sid in ids + ['END']:
        key = sid + ('_face' if sid in faces else '')
        html = html.replace('{{' + sid + '}}', parts.get(key, parts.get(sid, '')))
    open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)
    json.dump(timing, open(os.path.join(HERE, 'timing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total', total, 'faces', sorted(faces))
    for sid in ids:
        print(sid, scenes[sid]['start'], scenes[sid]['dur'], len(scenes[sid]['caps']))


if __name__ == '__main__':
    main()
