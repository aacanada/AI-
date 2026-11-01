"""Synthesise the two transition sounds used in the mix (original work, no samples; released CC0 with this repo).
    python3 -I tools/sfx_synth.py  -> assets/sfx/soft-whoosh.wav, assets/sfx/soft-click.wav
whoosh: pink-ish noise through a resonant band-pass whose centre sweeps 300 Hz -> 2.4 kHz -> 900 Hz, bell envelope, 0.55 s.
click : 2.2 kHz + 3.3 kHz sine burst with 18 ms exponential decay and a 2 ms noise transient, 0.09 s."""
import subprocess
import numpy as np

SR = 48000
rng = np.random.default_rng(20261101)


def write(path, x):
    x = (x / np.max(np.abs(x)) * 0.5).astype(np.float32)  # -6 dBFS peak; level is set in the mix
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", path],
                   input=x.tobytes(), check=True)


# whoosh
n = int(0.55 * SR)
t = np.arange(n) / SR
white = rng.standard_normal(n)
pink = np.cumsum(white) * 0.02 + white  # tilt toward low end
pink -= np.convolve(pink, np.ones(200) / 200, mode="same")  # remove DC drift
u = t / t[-1]
fc = np.where(u < 0.6, 300 * (2400 / 300) ** (u / 0.6), 2400 * (900 / 2400) ** ((u - 0.6) / 0.4))
q = 2.5
y = np.zeros(n)
lp = bp = 0.0
for i in range(n):  # state-variable filter, band-pass output
    f = 2 * np.sin(np.pi * fc[i] / SR)
    hp = pink[i] - lp - bp / q
    bp += f * hp
    lp += f * bp
    y[i] = bp
env = np.sin(np.pi * np.clip(u, 0, 1)) ** 2 * (1 - 0.35 * u)
write("assets/sfx/soft-whoosh.wav", y * env)

# click
n = int(0.09 * SR)
t = np.arange(n) / SR
tone = (np.sin(2 * np.pi * 2200 * t) + 0.5 * np.sin(2 * np.pi * 3300 * t)) * np.exp(-t / 0.018)
trans = rng.standard_normal(n) * np.exp(-t / 0.002) * 0.6
write("assets/sfx/soft-click.wav", tone + trans)
print("ok")
