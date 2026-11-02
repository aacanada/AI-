# Vowel check for the first syllable of '캐나다/카나다': LPC formants (F1, F2) over the vowel of '캐/카'.
# ㅐ(ae) → F2 high (~1.9 kHz+), ㅏ(a) → F2 low (~1.3-1.6 kHz). Usage: formant_check.py <audio> <word_start_s> ...
import sys, subprocess, numpy as np
f = sys.argv[1]
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '11025', '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float64); SR = 11025

def formants(seg, order=12):
    seg = np.append(seg[0], seg[1:] - 0.63 * seg[:-1]) * np.hamming(len(seg))
    r = np.correlate(seg, seg, 'full')[len(seg) - 1:len(seg) + order]
    a = np.linalg.solve(np.array([[r[abs(i - j)] for j in range(order)] for i in range(order)]), -r[1:order + 1])
    roots = [z for z in np.roots(np.concatenate([[1], a])) if z.imag > 0]
    fr = sorted(np.angle(z) * SR / (2 * np.pi) for z in roots if -np.log(abs(z)) * SR / np.pi < 400)
    return [v for v in fr if v > 200][:3]

for st in map(float, sys.argv[2:]):
    # '캐' vowel: skip the /kʰ/ burst+aspiration, then take the most voiced 30 ms frames in the next ~150 ms
    frames = []
    for off in np.arange(0.05, 0.20, 0.01):
        a = int((st + off) * SR); seg = x[a:a + int(0.03 * SR)]
        frames.append((np.sum(seg ** 2), off, formants(seg)))
    frames.sort(reverse=True)
    f2 = [fm[1] for e, o, fm in frames[:5] if len(fm) >= 2]
    f1 = [fm[0] for e, o, fm in frames[:5] if len(fm) >= 1]
    print(f'{f.split("/")[-2]}/{f.split("/")[-1]} @{st:.2f}  F1~{np.median(f1):.0f} Hz  F2~{np.median(f2):.0f} Hz')
