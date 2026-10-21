"""Turn the director's chapter recordings into per-scene narration. Run from project root:
    python3 -I tools/audio_prep.py            # all chapters found
    python3 -I tools/audio_prep.py 3 5        # only CH3, CH5
then:  python3 -I tools/build.py

Input : ../../plans/sga-longform/audio/sga_full.m4a (one take of all chapters; cut list in tools/voice_edits.json)
        or sga_chNN.m4a (one file per chapter, ~1 s pause between scenes)
Optional: SGA_ASR_MODEL=<sherpa-onnx-zipformer-korean-2024-06-24 folder> for word timing (pip install sherpa-onnx;
model from github.com/k2-fsa/sherpa-onnx releases, asr-models).
Output: assets/voice/sNN.wav (+ sNN.words.json) and assets/voice/_split.json (what was cut where, for review)

Per chapter: afftdn light denoise -> trim head/tail silence -> loudnorm I=-16 -> silencedetect.
Scene cut = the (N-1) longest pauses (>= 0.6 s) where N = narration scenes in the chapter, checked
against the script's character proportions. Inside a scene, pauses > 0.7 s are shortened to 0.45 s and a
slow read is sped up with pitch-preserving atempo (max 1.1x).
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

SRC = os.environ.get("SGA_AUDIO_DIR", os.path.join("..", "..", "plans", "sga-longform", "audio"))
OUT = os.path.join("assets", "voice")
TMP = os.path.join(".hyperframes", "voice-tmp")
MIN_CPS, MAX_TEMPO = 4.0, 1.10  # chars/sec below MIN_CPS (a clearly slow read) gets atempo up to 1.1; numbers/acronyms read slower, so keep this low


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


def clean_chapter(ch):
    src = next((os.path.join(SRC, f"sga_ch{ch:02d}{e}") for e in (".m4a", ".mp3", ".wav", ".aac") if os.path.exists(os.path.join(SRC, f"sga_ch{ch:02d}{e}"))), None)
    if not src:
        return None
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, f"ch{ch:02d}.wav")
    trim = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05"
    af = f"highpass=f=70,afftdn=nf=-25,{trim},areverse,{trim},areverse,loudnorm=I=-16:TP=-1.5:LRA=11"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", "48000", "-ac", "1", out])
    return out


def sherpa_words(wav):
    """Offline Korean ASR (sherpa-onnx zipformer-korean) when SGA_ASR_MODEL points at the model folder."""
    mdir = os.environ.get("SGA_ASR_MODEL")
    if not mdir:
        return None
    try:
        import numpy as np
        import sherpa_onnx
    except ImportError:
        return None
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{mdir}/encoder-epoch-99-avg-1.int8.onnx", decoder=f"{mdir}/decoder-epoch-99-avg-1.onnx",
        joiner=f"{mdir}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{mdir}/tokens.txt", num_threads=4)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    words, step = [], 16000 * 20
    for off in range(0, len(x), step):  # 20 s windows keep the model in range
        st = rec.create_stream()
        st.accept_waveform(16000, x[off:off + step])
        rec.decode_stream(st)
        r = st.result
        ts = [off / 16000 + t for t in r.timestamps]
        for k, (tok, t0) in enumerate(zip(r.tokens, ts)):
            if tok.strip():
                words.append(dict(text=tok.strip(), start=round(t0, 3), end=round(ts[k + 1] if k + 1 < len(ts) else t0 + 0.2, 3)))
    return words or None


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


def finish_scene(s, raw, report, extra):
    rd = dur(raw)
    cps = nchar(" ".join(s["rows"])) / max(rd, 0.1)
    tempo = round(min(MAX_TEMPO, MIN_CPS / cps), 3) if cps < MIN_CPS else 1.0
    dst = os.path.join(OUT, f"{s['id']}.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", f"atempo={tempo}" if tempo != 1.0 else "anull", "-ar", "48000", dst])
    words = sherpa_words(dst) or transcribe(dst) or row_words(s["rows"], dst)
    json.dump(words, open(os.path.join(OUT, f"{s['id']}.words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report[s["id"]] = dict(dur=round(dur(dst), 2), cps=round(cps, 2), tempo=tempo, **extra)


def full_take(report):
    """One recording of all chapters + tools/voice_edits.json (scene bounds and re-read removals)."""
    ed = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_edits.json"), encoding="utf-8"))
    src = next((os.path.join(SRC, ed["source"] + e) for e in (".m4a", ".mp3", ".wav") if os.path.exists(os.path.join(SRC, ed["source"] + e))), None)
    if not src:
        return False
    os.makedirs(TMP, exist_ok=True)
    full = os.path.join(TMP, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", "highpass=f=70,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", "48000", "-ac", "1", full])
    for s in SCENES:
        if s.get("kind", "vo") != "vo":
            continue
        a, b = ed["scenes"][s["id"]]
        keep, t = [], a
        for x, y in sorted(ed["remove"].get(s["id"], [])):
            keep.append((t, x))
            t = y
        keep.append((t, b))
        parts = []
        for k, (x, y) in enumerate(keep):
            pth = os.path.join(TMP, f"{s['id']}-{k}.wav")
            d = y - x
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{x:.3f}", "-t", f"{d:.3f}", "-i", full,
                 "-af", f"afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03", pth])
            parts.append(pth)
        lst = os.path.join(TMP, f"{s['id']}.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        raw = os.path.join(TMP, f"{s['id']}-raw.wav")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
             "-af", "silenceremove=stop_periods=-1:stop_duration=0.7:stop_threshold=-40dB:stop_silence=0.45", raw])
        finish_scene(s, raw, report, dict(cut=[a, b], removed=ed["remove"].get(s["id"], [])))
    print(f"full take: {len(report)} scenes")
    return True


def main(only):
    os.makedirs(OUT, exist_ok=True)
    report = {}
    if not only and full_take(report):
        json.dump(report, open(os.path.join(OUT, "_split.json"), "w"), indent=1)
        return
    for ch in range(1, 10):
        if only and ch not in only:
            continue
        wav = clean_chapter(ch)
        if not wav:
            continue
        scenes = [s for s in SCENES if s["ch"] == ch and s.get("kind", "vo") == "vo"]
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
        print(f"CH{ch}: {n} scenes from {D:.1f}s{' (cut check failed - verify _split.json)' if warn else ''}")
    json.dump(report, open(os.path.join(OUT, "_split.json"), "w"), indent=1)


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
