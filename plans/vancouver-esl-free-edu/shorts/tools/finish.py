# Mix (narration + BGM bed + SFX, -16 LUFS), mux with silent render, write publish-staging folder.
# Usage: python3 finish.py <sid>
import json, subprocess, sys, re, os, shutil, hashlib

ROOT = '/home/user/AI-'
P = ROOT + '/plans/vancouver-esl-free-edu'
S = P + '/shorts'
sid = sys.argv[1]
FOLDER = {'a': '2026-10-29-vancouver-esl-short-a', 'b': '2026-10-31-vancouver-esl-short-b',
          'c': '2026-11-02-vancouver-esl-short-c', 'd': '2026-11-04-vancouver-esl-short-d'}[sid]
BGM_OFF = {'a': 0, 'b': 40, 'c': 70, 'd': 100}[sid]
D = json.load(open(f'{S}/{sid}/sfx.json'))
TOTAL = D['total']

ins = ['-i', f'{S}/{sid}/narration.wav', '-ss', str(BGM_OFF), '-i', P + '/video/bgm_vanesl.mp3']
def lufs0(f):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
vg = -17.0 - lufs0(f'{S}/{sid}/narration.wav')
fl = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={vg:.2f}dB[v]',
      f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOTAL:.3f},loudnorm=I=-38:TP=-9:LRA=11,aresample=48000,'
      f'afade=t=in:d=0.5,afade=t=out:st={TOTAL - 1.2:.3f}:d=1.2[b]']
for j, e in enumerate(D['sfx']):
    ins += ['-i', f'{S}/hf/assets/{e["file"]}']
    ms = int(e['t'] * 1000)
    fl.append(f'[{j + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e["gain"] + 2}dB,adelay={ms}|{ms}[x{j}]')
n = len(D['sfx'])
fl.append('[v][b]' + ''.join(f'[x{j}]' for j in range(n)) + f'amix=inputs={n + 2}:normalize=0,atrim=0:{TOTAL:.3f}[m]')
tmp = f'{S}/{sid}/mix.pre.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl), '-map', '[m]', '-ar', '48000', tmp], check=True)


def meas(f, af=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', (af + ',' if af else '') + 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1])


g = -16.0 - meas(tmp)[0]
for _ in range(4):
    af = f'volume={g:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=false'
    got = meas(tmp, af)[0]
    if abs(got + 16.0) < 0.1: break
    g += -16.0 - got
mix = f'{S}/{sid}/mix.m4a'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', mix], check=True)
os.remove(tmp)

out = f'{ROOT}/publish-staging/{FOLDER}'
os.makedirs(out, exist_ok=True)
vid = out + '/video.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{S}/{sid}/silent.mp4', '-i', mix, '-map', '0:v', '-map', '1:a',
                '-c', 'copy', '-shortest', '-movflags', '+faststart', vid], check=True)
# cover: frame after the hook lands
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.6', '-i', vid, '-frames:v', '1', '-q:v', '2', out + '/thumbnail.jpg'], check=True)
h = hashlib.sha256(open(vid, 'rb').read()).hexdigest()
open(out + '/video.mp4.sha256', 'w').write(f'{h}  video.mp4\n')
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid]))
lufs, peak = meas(vid)
info = {'folder': FOLDER, 'duration': round(dur, 2), 'lufs': lufs, 'peak': peak, 'size_mb': round(os.path.getsize(vid) / 1e6, 1)}
json.dump(info, open(f'{S}/{sid}/final.json', 'w'))
print(info)
