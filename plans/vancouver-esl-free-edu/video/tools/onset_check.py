# Waveform check: high-frequency (>3.5 kHz) energy share in the first 90 ms of a word.
# '십' starts with a fricative (high share), '만' with a nasal (low share).
# Usage: python3 onset_check.py <audio> <start_s> [<start_s> ...]
import sys, subprocess, numpy as np
f = sys.argv[1]
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32)
for st in map(float, sys.argv[2:]):
    best = None
    for off in np.arange(-0.06, 0.07, 0.01):  # ASR word starts are approximate: scan around
        a = int((st + off) * 16000); seg = x[a:a + int(0.09 * 16000)] * np.hanning(int(0.09 * 16000))
        sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(len(seg), 1 / 16000)
        r = sp[fr > 3500].sum() / max(sp.sum(), 1e-9)
        best = r if best is None else max(best, r)
    print(f'{f.split("/")[-1]} @{st:.2f}s  HF-share(max around onset) = {best:.3f}')
