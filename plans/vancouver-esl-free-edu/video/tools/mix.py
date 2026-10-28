# Final audio mix: narration (per-scene) + looped BGM bed + SFX, two-pass loudnorm to -16 LUFS.
# Usage: python3 mix.py <audio_dir> <bgm.mp3> <out.m4a>
import json, subprocess, sys, re

P = '/home/user/AI-/plans/vancouver-esl-free-edu'
AUD, BGM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
D = json.load(open(P + '/video/sfx.json'))
TOTAL = D['total']

inputs, filt, labels = [], [], []
for i, s in enumerate(D['scenes']):
    inputs += ['-i', f'{P}/{AUD}/vanesl_{s["id"]}.mp3']
    ms = int(s['audio_start'] * 1000)
    filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{i}]')
    labels.append(f'[n{i}]')
n = len(inputs) // 2
# ElevenLabs v2 files come out around -36..-38 LUFS: bring each scene to about -17 LUFS first
def _lufs(f):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
for i, s in enumerate(D['scenes']):
    g0 = -17.0 - _lufs(f'{P}/{AUD}/vanesl_{s["id"]}.mp3')
    filt[i] = filt[i].replace(f'[n{i}]', f',volume={g0:.2f}dB[n{i}]')
filt.append(f'{"".join(labels)}amix=inputs={n}:normalize=0[voice]')

# BGM: loop, -38 LUFS-ish bed (pre-normalized below), fade in/out
inputs += ['-stream_loop', '-1', '-i', BGM]
b = n
filt.append(f'[{b}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOTAL:.3f},'
            f'loudnorm=I=-38:TP=-9:LRA=11,aresample=48000,afade=t=in:d=1.5,afade=t=out:st={TOTAL - 3:.3f}:d=3[bgm]')

sl = []
for j, e in enumerate(D['sfx']):
    inputs += ['-i', f'{P}/hf/assets/{e["file"]}']
    k = b + 1 + j
    ms = max(0, int(e['t'] * 1000))
    filt.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e["gain"] + 2}dB,adelay={ms}|{ms}[x{j}]')
    sl.append(f'[x{j}]')
filt.append(f'{"".join(sl)}amix=inputs={len(sl)}:normalize=0[sfx]')
filt.append(f'[voice][bgm][sfx]amix=inputs=3:normalize=0,atrim=0:{TOTAL:.3f}[mix]')
fc = ';'.join(filt)

tmp = OUT + '.pre.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc, '-map', '[mix]', '-ar', '48000', tmp], check=True)
# gain to -16 LUFS + true-peak limiter (keeps dynamics linear; loudnorm would switch to dynamic mode)
def meas(f, af=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', (af + ',' if af else '') + 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
g = -16.0 - meas(tmp)
for _ in range(3):
    af = f'volume={g:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=false'
    got = meas(tmp, af)
    if abs(got + 16.0) < 0.15: break
    g += -16.0 - got
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', OUT], check=True)
print('gain', round(g, 2), 'LUFS', got)
