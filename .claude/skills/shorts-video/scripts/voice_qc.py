# Usage: python3 voice_qc.py <project-dir> [--takes N] [--force] [--report-only]
"""Automatic voice QC for ElevenLabs narration (the voice can't be listened to, so it is measured).

For every scene in script.json it makes N takes (different seeds) with character timestamps,
splits each take into its caption chunks, scores every chunk, and keeps the best chunk per
position across takes. Writes assets/audio/chunks/<scene>-<j>.wav (+ .json timing) and
voice_qc.json / voice_qc.md (what was checked, what was flagged, which take won).

Checks per chunk:
  text     ElevenLabs STT (scribe) vs the script → character error rate (wrong / dropped / extra words)
  stretch  a syllable held unnaturally long
  gap      an unexpected pause inside the chunk
  rate     speaking rate far from the scene's median (rushed / dragging)
  loud     loudness jump vs the other chunks
  pitch    pitch far from the voice's median (squeaky / growly)
  ending   ending pitch rises on a statement (or falls flat on a '?')
  clip     digital clipping
  noise    sound where there should be silence (breath, click, artifact) around the speech
"""
import base64, json, os, re, subprocess, sys, pathlib
import numpy as np

ROOT = pathlib.Path(sys.argv[1]).resolve()
TAKES = int(sys.argv[sys.argv.index("--takes") + 1]) if "--takes" in sys.argv else 3
FORCE = "--force" in sys.argv
REPORT_ONLY = "--report-only" in sys.argv
spec = json.loads((ROOT / "script.json").read_text())
AUD = ROOT / "assets" / "audio"
TK = AUD / "takes"; TK.mkdir(parents=True, exist_ok=True)
CH = AUD / "chunks"; CH.mkdir(parents=True, exist_ok=True)
KEY = os.environ["ELEVENLABS_API_KEY"]
SR = 44100
SEEDS = [11, 2024, 777, 31337, 4242, 90210]
VOICE = spec.get("voice_settings", {"stability": 0.5, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True})

def curl(args, data=None):
    r = subprocess.run(["curl", "-sS", "-f", *args], input=data, capture_output=True)
    if r.returncode:
        sys.exit(f"ElevenLabs call failed: {r.stderr.decode()[:300]}")
    return json.loads(r.stdout)

def tts(text, seed, mp3):
    body = json.dumps({"text": text, "model_id": spec["model_id"], "seed": seed, "voice_settings": VOICE}).encode()
    d = curl(["-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{spec['voice_id']}/with-timestamps?output_format=mp3_44100_128",
              "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json", "--data-binary", "@-"], body)
    mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    return d["alignment"]

def stt(path):
    return curl(["-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", f"xi-api-key: {KEY}",
                 "-F", "model_id=scribe_v1", "-F", "language_code=kor", "-F", "timestamps_granularity=word",
                 "-F", "tag_audio_events=true", "-F", f"file=@{path}"])

def decode(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()

def norm(s):
    s = s.lower().replace("ok", "오케이").replace("aa", "에이에이").replace("canada", "캐나다")
    return re.sub(r"[^0-9a-z가-힣%$,]", "", s).replace(",", "")

def cer(a, b):
    a, b = norm(a), norm(b)
    if not b: return 1.0
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[len(b)] / len(b)

FILLERS = {"어", "음", "아", "으", "에", "흠", "엄", "이", "그", "저", "응", "흐", "하"}

def find_fillers(words, expected):
    """STT words that are hesitation sounds, not script: leading/trailing words the script doesn't start/end with,
    and standalone filler tokens ('어,', '음~') anywhere the script has no such word."""
    exp, exp_words = norm(expected), {norm(w) for w in expected.split()}
    out, i = [], 0
    while i < len(words) and norm(words[i]["text"]) in FILLERS and not exp.startswith(norm(words[i]["text"])):
        out.append(words[i]); i += 1
    j = len(words) - 1
    while j > i and norm(words[j]["text"]) and not exp.endswith(norm(words[j]["text"])[-2:]) and norm(words[j]["text"]) in FILLERS:
        out.append(words[j]); j -= 1
    for w in words[i:j + 1]:
        t = norm(w["text"])
        if t in FILLERS and t not in exp_words and re.search(r"[,~…]|\.\.", w["text"]):
            out.append(w)
    return out

def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)

def f0_track(x):
    """autocorrelation pitch, 40 ms frames / 10 ms hop; returns voiced F0 values in order"""
    n, hop, out = int(0.04 * SR), int(0.01 * SR), []
    lo, hi = int(SR / 400), int(SR / 70)
    gate = db(x) - 18
    for s in range(0, len(x) - n, hop):
        f = x[s:s + n] - np.mean(x[s:s + n])
        if db(f) < gate: continue
        ac = np.correlate(f, f, "full")[n - 1:]
        if ac[0] <= 0: continue
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.45: out.append(SR / k)
    return np.array(out)

def analyze(sid, take):
    """split one scene take into chunks and measure each"""
    sc = next(s for s in spec["scenes"] if s["id"] == sid)
    mp3, aj, sj = TK / f"{sid}.t{take}.mp3", TK / f"{sid}.t{take}.align.json", TK / f"{sid}.t{take}.stt.json"
    text = " ".join(c[1] for c in sc["chunks"])
    if FORCE or not mp3.exists():
        aj.write_text(json.dumps(tts(text, SEEDS[take], mp3), ensure_ascii=False))
    if FORCE or not sj.exists():
        sj.write_text(json.dumps(stt(mp3), ensure_ascii=False))
    al, tr = json.loads(aj.read_text()), json.loads(sj.read_text())
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    pcm = decode(mp3); dur = len(pcm) / SR
    ranges, pos = [], 0
    for _, tt in sc["chunks"]:
        ranges.append((pos, pos + len(tt) - 1)); pos += len(tt) + 1
    cuts = [0.0] + [(en[ranges[i][1]] + st[ranges[i + 1][0]]) / 2 for i in range(len(ranges) - 1)] + [dur]
    words = [w for w in tr.get("words", []) if w.get("type") == "word"]
    events = [w for w in tr.get("words", []) if w.get("type") == "audio_event"]
    res = []
    for i, (disp, tt) in enumerate(sc["chunks"]):
        a, b = ranges[i]
        s0, s1 = st[a], en[b]
        seg = pcm[int(cuts[i] * SR):int(cuts[i + 1] * SR)]
        speech = pcm[int(s0 * SR):int(s1 * SR)]
        heard = " ".join(w["text"] for w in words if cuts[i] <= (w["start"] + w["end"]) / 2 < cuts[i + 1])
        syl = [k for k in range(a, b + 1) if re.match(r"[가-힣0-9a-zA-Z]", al["characters"][k])]
        durs = [(al["characters"][k], en[k] - st[k], k == syl[-1]) for k in syl if k != 0]  # char 0 absorbs leading silence
        gaps = [st[syl[q + 1]] - en[syl[q]] for q in range(len(syl) - 1) if al["characters"][syl[q] + 1] != " "] + \
               [st[syl[q + 1]] - en[syl[q]] - 0.18 for q in range(len(syl) - 1) if al["characters"][syl[q] + 1] == " "]
        f0 = f0_track(speech)
        tail = f0[-max(3, len(f0) // 4):] if len(f0) >= 8 else f0
        quiet = np.concatenate([pcm[int(cuts[i] * SR):int(max(cuts[i], s0 - 0.06) * SR)],
                                pcm[int(min(cuts[i + 1], s1 + 0.12) * SR):int(cuts[i + 1] * SR)]])
        res.append({
            "chunk": i, "text": disp, "heard": heard,
            "cer": round(min(cer(heard, disp), cer(heard, tt)), 3),
            "rate": round(len(syl) / max(0.1, s1 - s0), 2),
            "max_syl": round(max([d for _, d, last in durs if not last] or [0]), 3),
            "max_syl_char": max([(d, ch) for ch, d, last in durs if not last] or [(0, "")])[1],
            "last_syl": round(durs[-1][1], 3) if durs else 0.0,
            "max_gap": round(max(gaps or [0]), 3),
            "loud": round(float(db(speech)), 1),
            "f0": round(float(np.median(f0)), 1) if len(f0) else None,
            "end_slope": round(float(np.median(tail) / np.median(f0) - 1), 3) if len(f0) >= 8 else 0.0,
            "clip": int(np.sum(np.abs(seg) > 0.985)),
            "noise": round(float(db(quiet)), 1) if len(quiet) > SR * 0.03 else -99.0,
            "events": [e["text"] for e in events if cuts[i] <= e["start"] < cuts[i + 1]],
            "fillers": [[w["text"], w["start"], w["end"]] for w in find_fillers(
                [w for w in words if cuts[i] <= (w["start"] + w["end"]) / 2 < cuts[i + 1]], disp)],
            "words": [[w["text"], w["start"], w["end"]] for w in words if cuts[i] <= (w["start"] + w["end"]) / 2 < cuts[i + 1]],
            "question": disp.strip().endswith("?"),
            "seg": [cuts[i], cuts[i + 1]], "speech": [s0, s1],
        })
    return res

def flags(c, med):
    f = []
    if c.get("fillers"): f.append(f"filler {[w[0] for w in c['fillers']]}")
    if c["cer"] > 0: f.append(f"text: heard '{c['heard']}'")
    if c["max_syl"] > 0.42: f.append(f"stretch '{c['max_syl_char']}' {c['max_syl']}s")
    if c["last_syl"] > 0.75: f.append(f"stretched ending {c['last_syl']}s")
    if c["max_gap"] > 0.3: f.append(f"gap {c['max_gap']}s")
    if c["rate"] > med["rate"] * 1.3: f.append(f"rushed {c['rate']} syl/s")
    if c["rate"] < med["rate"] * 0.72: f.append(f"dragging {c['rate']} syl/s")
    if abs(c["loud"] - med["loud"]) > 4.5: f.append(f"loudness {c['loud'] - med['loud']:+.1f} dB")
    if c["f0"] and abs(c["f0"] / med["f0"] - 1) > 0.22: f.append(f"pitch {c['f0']} Hz (median {med['f0']})")
    if not c["question"] and c["end_slope"] > 0.18: f.append(f"ending rises {c['end_slope']:+.0%}")
    if c["question"] and c["end_slope"] < -0.12: f.append(f"question ending falls {c['end_slope']:+.0%}")
    if c["clip"] > 20: f.append(f"clipping {c['clip']} samples")
    if c["noise"] > -38: f.append(f"noise around speech {c['noise']} dB")
    if c["events"]: f.append(f"audio events {c['events']}")
    return f

def score(c, f):
    return c["cer"] * 10 + len(f) + (0.5 if c["cer"] > 0 else 0)

# ---------- run ----------
def speech_bounds(x, gate_db=-38):
    """first/last 10 ms frame whose level is within 25 dB of the loudest, and above gate_db"""
    hop = int(0.01 * SR); fr = [db(x[k:k + hop]) for k in range(0, len(x) - hop, hop)]
    thr = max(gate_db, max(fr) - 25)
    on = [k for k, v in enumerate(fr) if v > thr]
    return (on[0] * 0.01, (on[-1] + 1) * 0.01) if on else (0.0, len(x) / SR)

def repair(seg, c, a):
    """cut filler words out of the chunk; returns new audio + removed spans (take time)"""
    removed = []
    words = sorted(c["words"], key=lambda w: w[1])
    for f in sorted(c.get("fillers", []), key=lambda w: w[1]):
        nxt = [w for w in words if w[1] >= f[2] - 1e-3 and w not in c["fillers"]]
        prv = [w for w in words if w[2] <= f[1] + 1e-3 and w not in c["fillers"]]
        t0 = max(a, (prv[-1][2] + 0.04) if prv else f[1] - 0.06)
        t1 = (nxt[0][1] - 0.05) if nxt else f[2] + 0.08
        if t1 > t0: removed.append([t0, t1])
    out, last = [], a
    for t0, t1 in removed:
        out.append(seg[int((last - a) * SR):int((t0 - a) * SR)]); last = t1
    out.append(seg[int((last - a) * SR):])
    y = np.concatenate(out) if out else seg
    nf = int(0.012 * SR); r = np.linspace(0, 1, nf, dtype=np.float32); y[:nf] *= r; y[-nf:] *= r[::-1]
    return y, removed

takes = {sc["id"]: [analyze(sc["id"], t) for t in range(TAKES if not REPORT_ONLY else 1)] for sc in spec["scenes"]}
allc = [c for v in takes.values() for tk in v for c in tk]
med = {k: float(np.median([c[k] for c in allc if c[k] is not None])) for k in ("rate", "loud", "f0")}
report, md = {"median": med, "scenes": []}, ["# Voice QC", "", f"median rate {med['rate']:.2f} syl/s · loudness {med['loud']:.1f} dB · pitch {med['f0']:.0f} Hz · takes per scene {TAKES}", ""]
fixable = ("filler",)  # problems repair() removes, so they don't count against a take
for sid, tks in takes.items():
    md.append(f"## {sid}")
    srep = []
    for i in range(len(tks[0])):
        cands = []
        for t, tk in enumerate(tks):
            f = flags(tk[i], med)
            hard = [x for x in f if not x.startswith(fixable) and not (x.startswith("text") and tk[i]["fillers"])]
            cands.append((tk[i]["cer"] * 10 * (0 if tk[i]["fillers"] and not hard else 1) + len(hard) + 0.2 * len(f), t, tk[i], f))
        best = min(cands, key=lambda x: (x[0], x[1]))
        for s_, t, c, f in sorted(cands, key=lambda x: x[1]):
            md.append(f"- chunk {i} take {t}{' ✅' if t == best[1] else ''} · \"{c['text']}\" → heard \"{c['heard']}\" · "
                      f"{', '.join(f) if f else 'clean'}")
        c, t = best[2], best[1]
        pcm = decode(TK / f"{sid}.t{t}.mp3")
        a, b = c["seg"]
        seg, removed = repair(pcm[int(a * SR):int(b * SR)].copy(), c, a)
        seg *= 10 ** (float(np.clip(med["loud"] - c["loud"], -4, 4)) / 20)  # level-match chunks from different takes
        seg = np.clip(seg, -0.98, 0.98)
        out = CH / f"{sid}-{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out)], input=seg.tobytes(), check=True)
        s0, s1 = speech_bounds(seg)
        final = flags(c, med)
        if removed:  # verify the repaired chunk by ear-substitute: STT it again
            pad = CH / f"{sid}-{i}.stt.wav"  # STT rejects very short clips: verify on a padded copy
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-af", "adelay=500,apad=pad_dur=0.5", str(pad)], check=True)
            v = stt(pad); pad.unlink(); vw = [w for w in v.get("words", []) if w.get("type") == "word"]
            heard = " ".join(w["text"] for w in vw)
            c2 = dict(c, heard=heard, cer=round(min(cer(heard, c["text"]), cer(heard, next(x[1] for x in next(s for s in spec["scenes"] if s["id"] == sid)["chunks"] if x[0] == c["text"]))), 3),
                      fillers=[[w["text"], w["start"], w["end"]] for w in find_fillers(vw, c["text"])])
            final = [x for x in flags(c2, med) if not x.startswith("stretch")]
            md.append(f"  - repaired chunk {i}: cut {len(removed)} filler span(s) → heard \"{heard}\" · {', '.join(final) if final else 'clean'}")
        (CH / f"{sid}-{i}.json").write_text(json.dumps({"take": t, "src_start": a, "removed": removed, "speech_start": s0, "speech_end": s1,
            "duration": len(seg) / SR, "flags": final}, ensure_ascii=False))
        srep.append({"chunk": i, "take": t, "removed": removed, "flags": final, "metrics": c})
    report["scenes"].append({"id": sid, "chunks": srep})
    md.append("")
left = [(s_["id"], c["chunk"], c["flags"]) for s_ in report["scenes"] for c in s_["chunks"] if c["flags"]]
md += ["## Result", "All chosen chunks clean." if not left else "Still flagged after choosing the best take:"]
md += [f"- {sid} chunk {i}: {', '.join(f)}" for sid, i, f in left]
(ROOT / "voice_qc.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
(ROOT / "voice_qc.md").write_text("\n".join(md) + "\n")
print("\n".join(md[-(len(left) + 2):]))
