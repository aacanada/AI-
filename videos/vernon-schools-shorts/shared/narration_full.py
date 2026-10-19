"""Owner-recorded narration as ONE file per short (short-N_full.m4a) -> per-scene audio, narration.wav, timing.json.

Usage: python3 shared/narration_full.py <short-dir> <audio-dir> [--tempo 1.0] [--max-pause 0.5]

1. Clean the whole take: highpass 80 Hz, light denoise (afftdn), loudness normalise (loudnorm I=-16).
2. Detect pauses (silencedetect -38 dB, >=0.12 s) and align the script chunks to the speech blocks between pauses
   with a small DP: every scene boundary must land on a pause; chunk durations should follow the script's
   character counts at the take's own speaking rate.  (Forced alignment with whisper is not possible here:
   model downloads from huggingface are blocked by the network policy.)
3. Rebuild the narration: chunks are cut from the cleaned take, pauses inside a scene are capped at --max-pause,
   scenes are joined with a 0.35 s gap (long silences between scenes removed).  Optional --tempo (<=1.1) uses
   pitch-preserving atempo.
4. timing.json gets scene windows + caption chunk windows from the real voice.
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
SRC = pathlib.Path(sys.argv[2]).resolve()
args = sys.argv[3:]
TEMPO = float(args[args.index("--tempo") + 1]) if "--tempo" in args else 1.0
MAXP = float(args[args.index("--max-pause") + 1]) if "--max-pause" in args else 0.5
assert 1.0 <= TEMPO <= 1.1, "tempo must stay within 1.0-1.1"
spec = json.loads((ROOT / "script.json").read_text())
out = ROOT / "assets" / "audio"
out.mkdir(parents=True, exist_ok=True)
GAP, LEAD, TAIL, PAD0, PAD1 = 0.35, 0.25, 2.4, 0.06, 0.10

src = SRC / f"short-{spec['n']}_full.m4a"
if not src.exists():
    sys.exit(f"missing recording: {src.name}")
clean = out / "take-clean.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af",
                "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1", str(clean)], check=True)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


D = dur(clean)
log = subprocess.run(["ffmpeg", "-v", "info", "-i", str(clean), "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
pauses = [(a, b) for a, b in zip(st, en + [D] * (len(st) - len(en)))]
s0 = pauses[0][1] if pauses and pauses[0][0] <= 0.05 else 0.0
e0 = pauses[-1][0] if pauses and pauses[-1][1] >= D - 0.05 else D
P = [(a, b) for a, b in pauses if a > s0 + 0.05 and b < e0 - 0.05]

chunks = []  # (scene index, chars)
for i, sc in enumerate(spec["scenes"]):
    for _, tts in sc["chunks"]:
        chunks.append((i, len(re.sub(r"[\s,.?!·]", "", tts))))
N = len(chunks)
scene_first = {c for c in range(N) if c == 0 or chunks[c][0] != chunks[c - 1][0]}
speech = (e0 - s0) - sum(b - a for a, b in P if b - a >= 0.45)
rate = sum(c for _, c in chunks) / speech  # chars per second of this take

# DP: node = pause index (-1 = speech start, len(P) = speech end); group = consecutive chunks between two nodes.
INF = float("inf")
end_of = lambda p: s0 if p == -1 else P[p][1]
start_of = lambda p: e0 if p == len(P) else P[p][0]
best = {(0, -1): (0.0, None)}
for c in range(N):
    for p in range(-1, len(P)):
        if (c, p) not in best:
            continue
        base = best[(c, p)][0]
        for c2 in range(c + 1, N + 1):
            crosses = any(k in scene_first for k in range(c + 1, c2))
            chars = sum(ch for _, ch in chunks[c:c2])
            exp = chars / rate
            for p2 in range(p + 1, len(P) + 1):
                if (c2 == N) != (p2 == len(P)):
                    continue
                a, b = end_of(p), start_of(p2)
                if b <= a:
                    continue
                d = b - a
                cost = (d - exp) ** 2 / exp
                cost += sum(2.0 for x, y in P[p + 1:p2] if y - x >= 0.45)  # a long pause left inside a group
                cost += 50.0 if crosses else 0.0
                if c2 in scene_first and c2 < N and P[p2][1] - P[p2][0] < 0.3:
                    cost += 3.0  # scene cut on a tiny pause
                v = base + cost
                if v < best.get((c2, p2), (INF,))[0]:
                    best[(c2, p2)] = (v, (c, p))
state, groups = (N, len(P)), []
while best[state][1] is not None:
    prev = best[state][1]
    groups.append((prev[0], state[0], end_of(prev[1]), start_of(state[1])))
    state = prev
groups.reverse()

# chunk windows on the original take: split a group by character ratio, snapping to an inner pause when close
win = [None] * N
for c, c2, a, b in groups:
    chars = [chunks[k][1] for k in range(c, c2)]
    t, tot, inner = a, sum(chars), [(x, y) for x, y in P if a < x and y < b]
    for k, ch in zip(range(c, c2), chars):
        if k == c2 - 1:
            win[k] = (t, b)
            break
        guess = t + (b - a) * ch / tot
        near = [pp for pp in inner if abs((pp[0] + pp[1]) / 2 - guess) < 0.6 and pp[0] > t]
        if near:
            x, y = min(near, key=lambda pp: abs((pp[0] + pp[1]) / 2 - guess))
            win[k] = (t, x); t = y
        else:
            win[k] = (t, guess); t = guess

# rebuild: per scene, chunk pieces joined by capped pauses; scenes joined by GAP
filt, labels, timing, t_out, n = [], [], {"scenes": []}, LEAD, 0
filt.append(f"[0:a]asplit={N}" + "".join(f"[s{k}]" for k in range(N)))
labels.append(f"aevalsrc=0:d={LEAD}:s=44100[lead]")
seq = ["[lead]"]
for i, sc in enumerate(spec["scenes"]):
    ks = [k for k in range(N) if chunks[k][0] == i]
    caps, a_start = [], t_out
    for j, k in enumerate(ks):
        a, b = win[k]
        lo = max(a - PAD0, win[k - 1][1] if k > 0 else 0)
        hi = min(b + PAD1, win[k + 1][0] if k + 1 < N else D)
        piece = (hi - lo) / TEMPO
        tempo = f",atempo={TEMPO}" if TEMPO != 1.0 else ""
        filt.append(f"[s{k}]atrim={lo:.3f}:{hi:.3f},asetpts=PTS-STARTPTS{tempo}[c{k}]")
        seq.append(f"[c{k}]")
        caps.append({"text": sc["chunks"][j][0], "start": round(t_out + (a - lo) / TEMPO, 3)})
        t_out += piece
        if j + 1 < len(ks):
            gap = min(MAXP, max(0.0, win[ks[j + 1]][0] - b)) / TEMPO
            gap = max(0.0, gap - (PAD0 + PAD1) / TEMPO)
            if gap > 0.01:
                labels.append(f"aevalsrc=0:d={gap:.3f}:s=44100[g{n}]"); seq.append(f"[g{n}]"); n += 1
                t_out += gap
    a_dur = t_out - a_start
    timing["scenes"].append({"id": sc["id"], "start": round(a_start - (LEAD if i == 0 else GAP / 2), 3),
                             "audio_start": round(a_start, 3), "audio_dur": round(a_dur, 3), "captions": caps,
                             "take": [round(win[ks[0]][0], 3), round(win[ks[-1]][1], 3)]})
    if i + 1 < len(spec["scenes"]):
        labels.append(f"aevalsrc=0:d={GAP}:s=44100[g{n}]"); seq.append(f"[g{n}]"); n += 1
        t_out += GAP
total = round(t_out + TAIL, 2)
labels.append(f"aevalsrc=0:d={TAIL}:s=44100[tail]"); seq.append("[tail]")
for i, s in enumerate(timing["scenes"]):
    nxt = timing["scenes"][i + 1]["start"] if i + 1 < len(timing["scenes"]) else total
    s["start"] = max(0.0, s["start"]); s["duration"] = round(nxt - s["start"], 3)
    for j in range(len(s["captions"])):
        s["captions"][j]["end"] = s["captions"][j + 1]["start"] if j + 1 < len(s["captions"]) else round(min(nxt, s["audio_start"] + s["audio_dur"] + 0.3), 3)
timing["total"] = total
timing["source"] = {"file": src.name, "tempo": TEMPO, "max_pause": MAXP, "rate_chars_per_s": round(rate, 2),
                    "method": "silencedetect + script-ratio DP alignment"}
graph = ";".join(labels + filt) + ";" + "".join(seq) + f"concat=n={len(seq)}:v=0:a=1,atrim=0:{total}[out]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clean), "-filter_complex", graph, "-map", "[out]", "-ar", "44100", "-ac", "1",
                str(out / "narration.wav")], check=True)
clean.unlink()
(ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
print(f"take {D:.2f}s  speech {s0:.2f}-{e0:.2f}  rate {rate:.2f} c/s  -> total {total}s (narration.wav {dur(out / 'narration.wav'):.2f}s)")
for s in timing["scenes"]:
    print(s["id"], "take", s["take"], "-> out", s["audio_start"], "+", s["audio_dur"], "|", " / ".join(f'{c["start"]}:{c["text"]}' for c in s["captions"]))
