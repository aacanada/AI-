"""Use the owner's own recording (assets/audio/recording/original.m4a) as the narration.

Times below are from the original recording, read off a local Korean ASR pass (sherpa-onnx zipformer-ko,
token timestamps) and the energy envelope. The take is kept as recorded: no pauses are inserted.
Edits: the leading filler ("응") is cut, and the three silences longer than 0.8 s are shortened to 0.6 s.
Writes assets/audio/narration.wav and timing.json (scenes, captions, and word marks for the motion)."""
import json, subprocess, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "audio" / "recording" / "original.m4a"
SR = 48000
LEAD = 0.3          # silence kept before the first word
TAIL_HOLD = 2.8     # CTA stays up after the last word

# (start of filler / dead air, end) in original time → removed
REMOVE = [(0.0, 4.45 - LEAD),          # "응" + lead-in
          (8.54, 9.18), (16.73, 17.24), (50.06, 50.98)]  # long gaps → 0.6 s

# scene id → [(caption as spoken, chunk start in original time)]
SCENES = [
    ("s1-hook", [("부모가 어학원만 다녀도", 4.75), ("아이 학비가 0원?", 6.84)]),
    ("s2-rule", [("캐나다 노바스코샤주 핼리팩스", 9.40), ("부모님 학생비자만 있으면", 11.78), ("자녀 공립학교가 무상교육이에요", 14.08)]),
    ("s3-school", [("대학이나 컬리지에", 17.47), ("다닐 필요가 없어요", 18.50), ("사설 어학원도 OK!", 20.30), ("학교 종류 조건이 없거든요", 23.18)]),
    ("s4-weeks", [("핵심은 40주 학비로", 26.30), ("50주 입학허가서를 받고", 28.38), ("방학 10주는 학비 0원", 31.12), ("이걸로 약 1년 학생비자 진행합니다", 33.66)]),
    ("s5-price", [("학비는 40주에", 37.15), ("11,400 캐나다 달러", 39.05), ("정가에서 25% 할인된 금액입니다", 41.90)]),
    ("s6-parents", [("아이 등교 후 9시 반 시작", 45.66), ("하교 전 수업 끝", 48.10), ("반 친구들도 모두 학부모", 51.22), ("대학 부설 과정보다 저렴하고 편해요", 53.93)]),
    ("s7-cta", [("핼리팩스 자녀무상교육", 57.50), ("AA Canada와 상담하세요", 59.13)]),
]
SPEECH_END = 61.20
# word marks the motion lands on (original time of the word onset)
MARKS = {"zero": 7.70, "halifax": 10.66, "visa": 12.28, "free": 15.47, "ok": 21.80, "nocond": 24.34,
         "fifty": 28.42, "vac": 31.17, "zero4": 33.18, "year": 34.62, "roll": 39.15, "pct": 42.66,
         "930": 46.74, "end": 49.48, "parents": 52.74, "cheap": 55.94, "aa": 59.15}

def new_t(t):
    return t - sum(min(b, t) - a for a, b in REMOVE if a < t)

# ---------- audio: cut, clean, level ----------
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(SRC), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
x = np.frombuffer(raw, dtype=np.float32).copy()
keep, last = [], 0.0
for a, b in REMOVE:
    if a > last: keep.append((last, a))
    last = b
keep.append((last, SPEECH_END + 0.5))
xf = int(0.02 * SR)
out = np.zeros(0, dtype=np.float32)
for a, b in keep:
    seg = x[int(a * SR):int(b * SR)].copy()
    r = np.linspace(0, 1, xf, dtype=np.float32)
    seg[:xf] *= r; seg[-xf:] *= r[::-1]
    out = np.concatenate([out, seg])
total = round(new_t(SPEECH_END) + TAIL_HOLD, 3)
out = np.concatenate([out, np.zeros(max(0, int(total * SR) - len(out)), dtype=np.float32)])[: int(total * SR)]
tmp = ROOT / "assets" / "audio" / "recording" / "edited.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)], input=out.tobytes(), check=True)
# gentle cleanup: rumble cut, light de-noise, soft compression, broadcast loudness, peak ceiling
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-af",
                "highpass=f=80,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
                "loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", "44100", "-ac", "1",
                str(ROOT / "assets" / "audio" / "narration.wav")], check=True)

# ---------- timing ----------
timing = {"voice": "owner recording", "scenes": [], "marks": {k: round(new_t(v), 3) for k, v in MARKS.items()}}
starts = [0.0] + [round(new_t(chs[0][1]) - 0.3, 3) for _, chs in SCENES[1:]]
for i, (sid, chs) in enumerate(SCENES):
    end = starts[i + 1] if i + 1 < len(SCENES) else total
    caps = []
    for j, (txt, t) in enumerate(chs):
        nxt = new_t(chs[j + 1][1]) if j + 1 < len(chs) else end
        caps.append({"text": txt, "start": round(new_t(t), 3), "end": round(nxt, 3)})
    for j in range(len(caps)):
        caps[j]["speech_end"] = round(caps[j + 1]["start"] - 0.05, 3) if j + 1 < len(caps) else round(min(end, new_t(SPEECH_END) if i == len(SCENES) - 1 else end - 0.35), 3)
    timing["scenes"].append({"id": sid, "start": starts[i], "duration": round(end - starts[i], 3),
                             "audio_end": caps[-1]["speech_end"], "captions": caps})
timing["total"] = total
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print("total", total)
for s in timing["scenes"]:
    print(s["id"], s["start"], s["duration"], [c["start"] for c in s["captions"]])
print("marks", timing["marks"])
