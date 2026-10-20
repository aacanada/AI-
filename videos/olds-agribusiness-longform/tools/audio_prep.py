"""Turn the director's recordings into per-scene narration (S02~S11). Run from project root:
    python3 -I tools/audio_prep.py            # all found
    python3 -I tools/audio_prep.py 3 5        # only S03, S05 (per-scene files)
then:  python3 -I tools/build.py

Input : ../../plans/olds-agribusiness-longform/audio/olds_chNN.m4a (NN = 02..11, one file per scene)
        or olds_voice_full.m4a (all ten scenes in one file, ~1 s pause between scenes)
Output: assets/voice/sNN.wav (+ sNN.words.json) and assets/voice/_split.json (what was cut where, for review)

Per file: highpass + afftdn light denoise -> trim head/tail silence -> loudnorm I=-16 -> silencedetect.
One full file: scene cut = the 9 longest pauses (>= 0.6 s), checked against the script's character
proportions (fallback: pause nearest each expected boundary). Inside a scene, pauses > 0.7 s are shortened to
0.45 s and a slow read is sped up with pitch-preserving atempo (max 1.1x).
Caption timing: `hyperframes transcribe` (whisper, ko) when the model can be downloaded; otherwise each
sentence row is snapped to the nearest detected pause (good enough for 22-char captions).
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES  # noqa: E402

SRC = os.environ.get("OLDS_AUDIO_DIR", os.path.join("..", "..", "plans", "olds-agribusiness-longform", "audio"))
OUT = os.path.join("assets", "voice")
TMP = os.path.join(".hyperframes", "voice-tmp")
MIN_CPS, MAX_TEMPO = 5.6, 1.10  # chars/sec below MIN_CPS gets atempo up to 1.1


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def silences(p, noise="-35dB", d=0.25):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en))


def nchar(t):
    return sum(1 for c in t if not c.isspace())


def find(stem):
    return next((os.path.join(SRC, stem + e) for e in (".m4a", ".mp3", ".wav", ".aac") if os.path.exists(os.path.join(SRC, stem + e))), None)


def clean_chapter(stem):
    src = find(stem)
    if not src:
        return None
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, f"{stem}.wav")
    trim = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05"
    af = f"highpass=f=70,afftdn=nf=-25,{trim},areverse,{trim},areverse,loudnorm=I=-16:TP=-1.5:LRA=11"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", "48000", "-ac", "1", out])
    return out


def transcribe(wav):
    try:
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.174", "transcribe", wav, "-d", ".", "--language", "ko", "--model", "small", "--json"],
                           capture_output=True, text=True, timeout=900)
        data = json.loads(r.stdout)
    except Exception:
        return None
    words = []

    def walk(o):
        if isinstance(o, dict):
            t = o.get("text", o.get("word"))
            if isinstance(t, str) and "start" in o and "end" in o and not any(isinstance(v, list) for v in o.values()):
                words.append(dict(text=t.strip(), start=float(o["start"]), end=float(o["end"])))
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    return words or None


def row_words(rows, wav):
    """Fallback alignment: snap proportional sentence boundaries to nearby pauses."""
    D = dur(wav)
    pauses = [((a + b) / 2, b - a) for a, b in silences(wav, "-38dB", 0.18)]
    tot = sum(nchar(r) for r in rows)
    out, acc, t0 = [], 0, 0.0
    for k, r in enumerate(rows):
        acc += nchar(r)
        if k == len(rows) - 1:
            t1 = D
        else:
            guess = D * acc / tot
            near = [p for p in pauses if abs(p[0] - guess) < 1.5 and p[0] > t0 + 0.4]
            t1 = min(near, key=lambda p: abs(p[0] - guess) - p[1])[0] if near else guess
        out.append(dict(text=r, start=round(t0, 3), end=round(t1, 3)))
        t0 = t1
    return out


def main(only):
    os.makedirs(OUT, exist_ok=True)
    report = {}
    vo = [s for s in SCENES if s.get("kind", "vo") == "vo"]
    if find("olds_voice_full") and not any(find(f"olds_ch{s['ch']:02d}") for s in vo):
        groups = [("olds_voice_full", vo)]
    else:
        groups = [(f"olds_ch{s['ch']:02d}", [s]) for s in vo if not only or s["ch"] in only]
    for stem, scenes in groups:
        ch = stem
        wav = clean_chapter(stem)
        if not wav:
            print(f"{stem}: not found in {SRC}")
            continue
        D = dur(wav)
        cand = [(a, b) for a, b in silences(wav, "-38dB", 0.6) if 0.3 < a < D - 0.3]
        n = len(scenes)
        cuts = sorted(sorted(cand, key=lambda x: x[1] - x[0], reverse=True)[: n - 1])
        tot = sum(nchar(" ".join(s["rows"])) for s in scenes)
        exp, acc = [], 0
        for s in scenes[:-1]:
            acc += nchar(" ".join(s["rows"]))
            exp.append(D * acc / tot)
        warn = len(cuts) != n - 1 or any(abs((a + b) / 2 - e) > max(4.0, 0.25 * D / n) for (a, b), e in zip(cuts, exp))
        if warn:  # fall back to the pause nearest each expected boundary
            cuts = [min(cand, key=lambda c: abs((c[0] + c[1]) / 2 - e)) if cand else (e, e) for e in exp]
        bounds = [0.0] + [x for c in cuts for x in (c[0] + 0.08, c[1] - 0.08)] + [D]
        for i, s in enumerate(scenes):
            a, b = bounds[2 * i], bounds[2 * i + 1]
            raw = os.path.join(TMP, f"{s['id']}-raw.wav")
            run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                 "-af", "silenceremove=stop_periods=-1:stop_duration=0.7:stop_threshold=-40dB:stop_silence=0.45", raw])
            rd = dur(raw)
            cps = nchar(" ".join(s["rows"])) / max(rd, 0.1)
            tempo = round(min(MAX_TEMPO, MIN_CPS / cps), 3) if cps < MIN_CPS else 1.0
            dst = os.path.join(OUT, f"{s['id']}.wav")
            run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", f"atempo={tempo}" if tempo != 1.0 else "anull", "-ar", "48000", dst])
            words = transcribe(dst) or row_words(s["rows"], dst)
            json.dump(words, open(os.path.join(OUT, f"{s['id']}.words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            report[s["id"]] = dict(ch=ch, cut=[round(a, 2), round(b, 2)], dur=round(dur(dst), 2), tempo=tempo, fallback_cut=warn)
        print(f"{stem}: {n} scene(s) from {D:.1f}s{' (cut check failed - verify _split.json)' if warn else ''}")
    old = json.load(open(os.path.join(OUT, "_split.json"))) if os.path.exists(os.path.join(OUT, "_split.json")) else {}
    json.dump({**old, **report}, open(os.path.join(OUT, "_split.json"), "w"), indent=1)


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
