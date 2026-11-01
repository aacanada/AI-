"""Final audio mix (ffmpeg + numpy), then mux onto the HyperFrames render.
    python3 -I tools/mix.py [renders/video_hf.mp4]  -> renders/mix.wav, renders/video.mp4, renders/loudness.json

Order (owner rule after the Vancouver long-form, where narration ended up at -24 LUFS under the music):
 1) narration: every scene wav is already normalised alone to -16 LUFS by tools/tts.py; scenes are placed on the
    timeline (mix_cues.json) and the stem gets one small linear trim to -16.0 LUFS.
 2) BGM (assets/music/bgm_vanesl.mp3, looped with 3 s crossfades): linear gain so that under narration it sits
    BGM_UNDER dB below the narration (-16 - 19 = -35 LUFS); ducking envelope raises it +DUCK_LIFT dB only where nobody
    speaks (title cards, scene gaps), 0.35 s ramps; 2 s fade-in, 3 s fade-out.
 3) SFX: soft whoosh on each title-card transition, soft click when the scene fades in after the card (synthesised,
    tools/sfx_synth.py).
 4) sum -> final linear gain to -16 LUFS + true-peak limiter. Each stem is also measured alone with that final gain.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SR = 48000
NARR, UNDER, DUCK_LIFT, MIX = -16.0, 19.0, 6.0, -16.0
SFX_GAIN = {"whoosh": -12.0, "click": -18.0}
SFX_FILE = {"whoosh": "assets/sfx/soft-whoosh.wav", "click": "assets/sfx/soft-click.wav"}
SFX_LEAD = {"whoosh": 0.18, "click": 0.0}  # whoosh peaks a little after its start
ST = os.path.join("renders", "stems")
os.makedirs(ST, exist_ok=True)
C = json.load(open("mix_cues.json", encoding="utf-8"))
TOTAL = C["total"]
N = int(round(TOTAL * SR))


def load(path, extra=()):
    pcm = subprocess.run(["ffmpeg", "-v", "error", *extra, "-i", path, "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(pcm, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def save(path, x, codec="pcm_f32le"):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", codec, path],
                   input=x.astype(np.float32).tobytes(), check=True)


def meas(path, af="anull"):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", af + ",ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    tail = r[r.rindex("Summary:"):]
    g = lambda k: float(re.search(k + r":\s+(-?[\d.]+|-inf)", tail).group(1).replace("-inf", "-200"))
    return {"I": g("I"), "LRA": g("LRA"), "TP": g("Peak")}


db = lambda v: 10 ** (v / 20)

# 1) narration stem
narr = np.zeros((N, 2))
for v in C["voice"]:
    x = load(os.path.join("assets", "voice", v["id"] + ".wav"))
    a = int(round(v["t"] * SR))
    b = min(N, a + len(x))
    narr[a:b] += x[:b - a]
save(ST + "/narration_placed.wav", narr)
placed = meas(ST + "/narration_placed.wav")
narr *= db(NARR - placed["I"])
save(ST + "/narration.wav", narr)
n_meas = meas(ST + "/narration.wav")

# 2) BGM: crossfade-loop to TOTAL, gain to NARR-UNDER, duck envelope
src = load("assets/music/bgm_vanesl.mp3")
XF = int(3 * SR)
ramp = np.linspace(0, 1, XF)[:, None]
bed = src.copy()
while len(bed) < N + SR:
    bed = np.concatenate([bed[:-XF], bed[-XF:] * (1 - ramp) + src[:XF] * ramp, src[XF:]])
bed = bed[:N]
save(ST + "/bgm_raw.wav", bed)
bed *= db(NARR - UNDER - meas(ST + "/bgm_raw.wav")["I"])
t = np.arange(N) / SR
speak = np.zeros(N, dtype=bool)
for v in C["voice"]:
    speak[int(v["t"] * SR):int((v["t"] + v["d"]) * SR)] = True
# smooth the on/off mask into 0.35 s ramps (centred moving average), then map to gain
k = int(0.35 * SR)
cs = np.concatenate([[0.0], np.cumsum(speak.astype(float))])
lo = np.clip(np.arange(N) - k // 2, 0, N)
hi = np.clip(np.arange(N) + k - k // 2, 0, N)
sm = (cs[hi] - cs[lo]) / k
gain = db(DUCK_LIFT) + (1 - db(DUCK_LIFT)) * sm  # 1.0 while speaking, +6 dB when silent
fade = np.clip(t / 2.0, 0, 1) * np.clip((TOTAL - t) / 3.0, 0, 1)
bed *= (gain * fade)[:, None]
save(ST + "/bgm.wav", bed)
# BGM measured only where narration plays (what the listener hears under the voice)
under = bed.copy()
under[~speak] = 0
save(ST + "/bgm_under_voice.wav", under)

# 3) SFX
sfx = np.zeros((N, 2))
for e in C["sfx"]:
    x = load(SFX_FILE[e["kind"]]) * db(SFX_GAIN[e["kind"]])
    a = max(0, int(round((e["t"] - SFX_LEAD[e["kind"]]) * SR)))
    b = min(N, a + len(x))
    sfx[a:b] += x[:b - a]
save(ST + "/sfx.wav", sfx)

# 4) sum + final gain + limiter
mix = narr + bed + sfx
save(ST + "/mix_pre.wav", mix)
fg = MIX - meas(ST + "/mix_pre.wav")["I"]
for _ in range(6):
    af = f"volume={fg:.2f}dB,alimiter=limit=0.79:attack=1:release=60:level=false"
    got = meas(ST + "/mix_pre.wav", af)
    if abs(got["I"] - MIX) < 0.1:
        break
    fg += MIX - got["I"]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", ST + "/mix_pre.wav", "-af", af, "-ar", str(SR), "-c:a", "pcm_s16le", "renders/mix.wav"], check=True)
fin = f"volume={fg:.2f}dB"
rep = {"final_gain_db": round(fg, 2),
       "narration_per_scene_normalised_target": NARR,
       "narration_alone_normalised": n_meas,
       "narration_alone_in_final": meas(ST + "/narration.wav", fin),
       "bgm_alone_in_final": meas(ST + "/bgm.wav", fin),
       "bgm_under_voice_in_final": meas(ST + "/bgm_under_voice.wav", fin),
       "sfx_alone_in_final": meas(ST + "/sfx.wav", fin),
       "final_mix": meas("renders/mix.wav")}
rep["narration_minus_bgm_under_voice_dB"] = round(rep["narration_alone_in_final"]["I"] - rep["bgm_under_voice_in_final"]["I"], 1)

vid = sys.argv[1] if len(sys.argv) > 1 else "renders/video_hf.mp4"
if os.path.exists(vid):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vid, "-i", "renders/mix.wav", "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", "renders/video.mp4"], check=True)
    rep["video_mp4_audio"] = meas("renders/video.mp4")
json.dump(rep, open("renders/loudness.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
