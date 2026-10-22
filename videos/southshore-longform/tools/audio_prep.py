"""Clean the director's recordings and get word timing. Run from project root:
    YV_ASR_DIR=<folder with sherpa-onnx models> python3 -I tools/audio_prep.py
Input : ../../plans/southshore-longform/audio/ss_sNN.m4a (one file per scene)
Output: assets/voice/sNN.wav            head/tail trimmed to 0.3 s (edge clicks ignored), inner pauses > 1.0 s cut to 0.7 s,
                                        highpass + light denoise, loudnorm -16 LUFS
        assets/voice/sNN.words.json     [{"text","start","end"}] token timing (sherpa-onnx zipformer-korean)
        assets/voice/_asr.json          per scene: kept spans, whisper phrases in raw time, transcripts (script check)
Models (github.com/k2-fsa/sherpa-onnx releases, asr-models; huggingface is blocked in the cloud sandbox):
    sherpa-onnx-zipformer-korean-2024-06-24 (timing + text), sherpa-onnx-whisper-turbo (text cross-check, optional)
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SRC = os.path.join("..", "..", "plans", "southshore-longform", "audio")
OUT = os.path.join("assets", "voice")
ASR = os.environ.get("YV_ASR_DIR", "")
PAD = 0.3
KEEP_ASR = os.environ.get("YV_REDO_ASR") != "1"  # re-clean without re-running ASR unless asked


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def silences(p, noise="-38dB", d=0.25):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en))


MAX_PAUSE, KEEP_PAUSE, BLIP = 1.0, 0.7, 0.3


EDITS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_edits.json"), encoding="utf-8"))


def keep_spans(src, sid):
    """Raw-time spans to keep: speech from the first to the last real sound (blips < BLIP s at the edges dropped)
    plus PAD, with every inner pause longer than MAX_PAUSE shortened to KEEP_PAUSE and the retakes/stumbles listed
    in voice_edits.json cut out (a cut is treated as silence)."""
    D = dur(src)
    sil = silences(src, "-40dB", 0.3) + [(a, b) for a, b, _ in EDITS.get(sid, [])]
    merged = []
    for a, b in sorted(sil):
        if merged and a <= merged[-1][1] + 0.05:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    sil = merged
    speech, t = [], 0.0
    for a, b in sil:
        if a > t:
            speech.append([t, a])
        t = b
    if t < D:
        speech.append([t, D])
    while speech and speech[0][1] - speech[0][0] < BLIP:
        speech.pop(0)
    while speech and speech[-1][1] - speech[-1][0] < BLIP:
        speech.pop()
    cuts = [(a, b) for a, b, _ in EDITS.get(sid, [])]
    spans = [[max(0.0, speech[0][0] - PAD), None]]
    for (a0, b0), (a1, b1) in zip(speech, speech[1:]):
        cut = [(a, b) for a, b in cuts if b0 - 0.06 <= a and b <= a1 + 0.06]
        if cut:  # never let the pause margin reach back into the cut audio
            spans[-1][1] = min(b0 + KEEP_PAUSE / 2, cut[0][0])
            spans.append([max(a1 - KEEP_PAUSE / 2, cut[-1][1]), None])
        elif a1 - b0 > MAX_PAUSE:
            half = KEEP_PAUSE / 2
            spans[-1][1] = b0 + half
            spans.append([a1 - half, None])
    spans[-1][1] = min(D, speech[-1][1] + PAD)
    return [(round(a, 3), round(b, 3)) for a, b in spans]


def raw_to_out(t, spans):
    """Map a raw-recording time to the cleaned wav's time."""
    acc = 0.0
    for a, b in spans:
        if t < a:
            return acc
        if t <= b:
            return acc + t - a
        acc += b - a
    return acc


def clean(sid):
    src = os.path.join(SRC, f"ss_{sid}.m4a")
    out = os.path.join(OUT, f"{sid}.wav")
    spans = keep_spans(src, sid)
    parts = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.02:.3f}:d=0.02[p{i}];"
                    for i, (a, b) in enumerate(spans))
    fc = (parts + "".join(f"[p{i}]" for i in range(len(spans))) + f"concat=n={len(spans)}:v=0:a=1,"
          "highpass=f=70,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11[o]")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", fc, "-map", "[o]", "-ar", "48000", "-ac", "1", out])
    return src, out, spans


def pcm(wav):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def chunks(wav, maxlen=18.0):
    """Cut points in the middle of pauses so no window splits a word; windows <= maxlen s."""
    D = dur(wav)
    mids = [(a + b) / 2 for a, b in silences(wav)]
    cuts, start = [0.0], 0.0
    while D - start > maxlen:
        cand = [m for m in mids if start + 3 < m <= start + maxlen]
        c = cand[-1] if cand else start + maxlen
        cuts.append(c)
        start = c
    cuts.append(D)
    return list(zip(cuts[:-1], cuts[1:]))


_REC = {}


def zipformer():
    if "z" not in _REC:
        import sherpa_onnx
        m = os.path.join(ASR, "sherpa-onnx-zipformer-korean-2024-06-24")
        _REC["z"] = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=f"{m}/encoder-epoch-99-avg-1.onnx", decoder=f"{m}/decoder-epoch-99-avg-1.onnx",
            joiner=f"{m}/joiner-epoch-99-avg-1.onnx", tokens=f"{m}/tokens.txt", num_threads=4,
            decoding_method="modified_beam_search")
    return _REC["z"]


_BYTES = {}


def whisper_text(result):
    """sherpa-onnx drops whisper byte-level tokens that are not valid UTF-8 on their own (half a Hangul syllable),
    so the recognizer is loaded with a tokens file whose entries are "<id>"; rebuild the bytes here."""
    ids = [int(x) for x in re.findall(r"<(\d+)>", "".join(result.tokens))]
    return b"".join(_BYTES.get(i, b"") for i in ids).decode("utf-8", "replace").strip()


def whisper():
    m = os.path.join(ASR, "sherpa-onnx-whisper-turbo")
    if os.environ.get("YV_NO_WHISPER") or not os.path.isdir(m):
        return None
    if "w" not in _REC:
        import base64
        import sherpa_onnx
        ids = os.path.join(m, "turbo-tokens-ids.txt")
        if not os.path.exists(ids):
            with open(os.path.join(m, "turbo-tokens.txt"), encoding="utf-8") as f, open(ids, "w") as g:
                for ln in f:
                    p = ln.split()
                    g.write((base64.b64encode(f"<{p[1]}>".encode()).decode() + " " + p[1] if len(p) == 2 else ln.strip()) + "\n")
        for ln in open(os.path.join(m, "turbo-tokens.txt"), encoding="utf-8"):
            p = ln.split()
            if len(p) == 2:
                _BYTES[int(p[1])] = base64.b64decode(p[0])
        _REC["w"] = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=f"{m}/turbo-encoder.int8.onnx", decoder=f"{m}/turbo-decoder.int8.onnx", tokens=f"{m}/turbo-tokens-ids.txt",
            language="ko", task="transcribe", num_threads=4)
    return _REC["w"]


def phrases(wav, lo=2.5, hi=9.0):
    """Speech phrases split at every pause, merged so each is lo..hi s (whisper text + timing per phrase)."""
    D = dur(wav)
    sil = silences(wav, "-38dB", 0.18)
    segs, t = [], 0.0
    for a, b in sil:
        if a > t:
            segs.append([t, a])
        t = b
    if t < D:
        segs.append([t, D])
    segs = [s for s in segs if s[1] - s[0] > 0.12]
    out = []
    for s in segs:
        if out and (s[0] - out[-1][0] < lo or (s[1] - out[-1][0] <= hi and out[-1][1] - out[-1][0] < lo)):
            out[-1][1] = s[1]
        else:
            out.append(list(s))
    return [(max(0, a - 0.08), min(D, b + 0.08)) for a, b in out]


def asr(wav):
    x = pcm(wav)
    words, ztext, wtext = [], [], []
    w = whisper()
    if w:  # whisper per phrase: text for the script check, phrase start/end for caption timing
        for a, b in phrases(wav):
            sw = w.create_stream()
            sw.accept_waveform(16000, x[int(a * 16000):int(b * 16000)])
            w.decode_stream(sw)
            t = whisper_text(sw.result)
            wtext.append(t)
            words.append(dict(text=t, start=round(a, 3), end=round(b, 3)))
        wlong = []  # long windows give whisper more context: this is the text used for the script check
        for a, b in chunks(wav, 25):
            sw = w.create_stream()
            sw.accept_waveform(16000, x[int(a * 16000):int(b * 16000)])
            w.decode_stream(sw)
            wlong.append(whisper_text(sw.result))
        wtext = [" ".join(wlong), " | ".join(wtext)]
    zwords = []
    for a, b in chunks(wav):
        seg = x[int(a * 16000):int(b * 16000)]
        st = zipformer().create_stream()
        st.accept_waveform(16000, seg)
        zipformer().decode_stream(st)
        r = st.result
        ztext.append(r.text.strip())
        ts = [a + t for t in r.timestamps]
        for k, (tok, t0) in enumerate(zip(r.tokens, ts)):
            t1 = ts[k + 1] if k + 1 < len(ts) else min(b, t0 + 0.25)
            zwords.append(dict(text=tok.replace("▁", " "), start=round(t0, 3), end=round(t1, 3)))
    return (words or zwords), " ".join(ztext), wtext


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    report = {}
    p = os.path.join(OUT, "_asr.json")
    if os.path.exists(p):
        report = json.load(open(p, encoding="utf-8"))
    for n in range(1, 12):
        sid = f"s{n:02d}"
        if only and sid not in only:
            continue
        src, out, spans = clean(sid)
        rec = report.get(sid, {})
        rec.update(src_dur=round(dur(src), 3), dur=round(dur(out), 3), spans=spans)
        if ASR and not (KEEP_ASR and rec.get("words_raw")):
            words, z, wt = asr(src)
            rec.update(words_raw=words, whisper=wt[0] if wt else "", phrases=wt[1] if wt else "", zipformer=z)
        if rec.get("words_raw"):
            def kept(w):  # drop phrases that were (mostly) cut out as retakes
                ln = max(0.01, w["end"] - w["start"])
                return sum(max(0.0, min(b, w["end"]) - max(a, w["start"])) for a, b in spans) / ln > 0.5
            words = [dict(w, start=round(raw_to_out(w["start"], spans), 3), end=round(raw_to_out(w["end"], spans), 3))
                     for w in rec["words_raw"] if kept(w)]
            json.dump(words, open(os.path.join(OUT, f"{sid}.words.json"), "w", encoding="utf-8"), ensure_ascii=False)
        report[sid] = rec
        print(sid, rec["src_dur"], "->", rec["dur"], flush=True)
        json.dump(report, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
