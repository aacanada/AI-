# Final audio mix. Narration is normalized FIRST (stem alone -> -16 LUFS), then BGM bed well below it,
# then SFX, then the full mix is gained to -16 LUFS with a true-peak limiter.
# Every stem is measured on its own with the same final gain, so "narration alone" is reported.
# Usage: python3 mix.py  -> renders/mix.m4a + renders/loudness.json
import json, os, re, subprocess

P = '/home/user/AI-/plans/montreal-multilang-longform'
D = json.load(open(P + '/video/sfx.json'))
TOTAL = D['total']
ST = P + '/renders/stems'
os.makedirs(ST, exist_ok=True)
NARR_TARGET, BGM_TARGET, MIX_TARGET = -16.0, -34.0, -16.0


def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def meas(f, af=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', (af + ',' if af else '') + 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    tail = r[r.rindex('Summary:'):]
    g = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', tail).group(1).replace('-inf', '-200'))
    return {'I': g('I'), 'LRA': g('LRA'), 'TP': g('Peak')}


# 1) narration stem: scenes placed on the timeline, then one linear gain to -16 LUFS
inputs, filt, labels = [], [], []
for i, s in enumerate(D['scenes']):
    inputs += ['-i', f'{P}/audio/mlang_{s["id"]}.mp3']
    ms = int(round(s['audio_start'] * 1000))
    filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{i}]')
    labels.append(f'[n{i}]')
filt.append(f'{"".join(labels)}amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{TOTAL:.3f}[v]')
ff(*inputs, '-filter_complex', ';'.join(filt), '-map', '[v]', '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/narration_raw.wav')
raw = meas(ST + '/narration_raw.wav')
# TTS peaks sit ~28 dB over its loudness, so plain gain would clip: gentle compression + true-peak limiter, then
# iterate the gain until the narration stem alone reads -16 LUFS.
g = NARR_TARGET - raw['I']
for _ in range(12):
    naf = (f'volume={g - 6:.2f}dB,acompressor=threshold=-24dB:ratio=3:attack=5:release=120:knee=4,'
           f'volume=6dB,alimiter=limit=0.70:attack=1:release=80:level=false')
    narr = meas(ST + '/narration_raw.wav', naf)
    if abs(narr['I'] - NARR_TARGET) < 0.1: break
    g += NARR_TARGET - narr['I']
ff('-i', ST + '/narration_raw.wav', '-af', naf, '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/narration.wav')
narr = meas(ST + '/narration.wav')

# 2) BGM bed: looped, linear gain to -34 LUFS (18 LU under the narration), fades in/out
ff('-stream_loop', '-1', '-i', P + '/video/bgm_vanesl.mp3', '-af',
   f'aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOTAL:.3f}', '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/bgm_raw.wav')
bg = BGM_TARGET - meas(ST + '/bgm_raw.wav')['I']
ff('-i', ST + '/bgm_raw.wav', '-af', f'volume={bg:.2f}dB,afade=t=in:d=1.5,afade=t=out:st={TOTAL - 3:.3f}:d=3', '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/bgm.wav')

# 3) SFX stem
inputs, filt, labels = [], [], []
for j, e in enumerate(D['sfx']):
    inputs += ['-i', f'{P}/hf/assets/{e["file"]}']
    ms = max(0, int(round(e['t'] * 1000)))
    filt.append(f'[{j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e["gain"]}dB,adelay={ms}|{ms}[x{j}]')
    labels.append(f'[x{j}]')
filt.append(f'{"".join(labels)}amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{TOTAL:.3f}[s]')
ff(*inputs, '-filter_complex', ';'.join(filt), '-map', '[s]', '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/sfx.wav')

# 4) sum, then final gain to -16 LUFS + true-peak limiter (linear gain; limiter only catches peaks)
ff('-i', ST + '/narration.wav', '-i', ST + '/bgm.wav', '-i', ST + '/sfx.wav', '-filter_complex',
   f'[0:a][1:a][2:a]amix=inputs=3:normalize=0,atrim=0:{TOTAL:.3f}[m]', '-map', '[m]', '-ar', '48000', '-c:a', 'pcm_f32le', ST + '/mix_pre.wav')
fg = MIX_TARGET - meas(ST + '/mix_pre.wav')['I']
for _ in range(4):
    af = f'volume={fg:.2f}dB,alimiter=limit=0.75:attack=1:release=60:level=false'
    got = meas(ST + '/mix_pre.wav', af)
    if abs(got['I'] - MIX_TARGET) < 0.1: break
    fg += MIX_TARGET - got['I']
ff('-i', ST + '/mix_pre.wav', '-af', af, '-ar', '48000', '-c:a', 'aac', '-b:a', '256k', P + '/renders/mix.m4a')

rep = {'final_gain_db': round(fg, 2),
       'narration_raw_tts': raw,
       'narration_alone_normalized': narr,
       'narration_alone_in_final': meas(ST + '/narration.wav', f'volume={fg:.2f}dB'),
       'bgm_alone_in_final': meas(ST + '/bgm.wav', f'volume={fg:.2f}dB'),
       'sfx_alone_in_final': meas(ST + '/sfx.wav', f'volume={fg:.2f}dB'),
       'final_mix': meas(P + '/renders/mix.m4a')}
json.dump(rep, open(P + '/renders/loudness.json', 'w'), indent=1)
print(json.dumps(rep, indent=1))
