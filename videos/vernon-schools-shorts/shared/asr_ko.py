"""Korean ASR with token timestamps (sherpa-onnx zipformer-korean, offline) -> JSON on stdout.

Usage: python3 shared/asr_ko.py <audio> <model-dir>
Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-korean-2024-06-24.tar.bz2
(huggingface is blocked in this environment; GitHub release assets are reachable.)  pip install sherpa-onnx.
Long takes are decoded in VAD-free fixed windows split at pauses so timestamps stay absolute.
"""
import json, pathlib, subprocess, sys, wave

import numpy as np
import sherpa_onnx

audio, mdir = sys.argv[1], pathlib.Path(sys.argv[2])
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", audio, "-af", "highpass=f=80,afftdn=nf=-25", "-ar", "16000", "-ac", "1",
                               "-f", "s16le", "-"])
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=str(mdir / "encoder-epoch-99-avg-1.int8.onnx"), decoder=str(mdir / "decoder-epoch-99-avg-1.onnx"),
    joiner=str(mdir / "joiner-epoch-99-avg-1.int8.onnx"), tokens=str(mdir / "tokens.txt"), num_threads=4, decoding_method="greedy_search")

# split at quiet frames roughly every <=12 s
sr, win = 16000, 400
energy = np.array([np.sqrt(np.mean(x[i:i + win] ** 2) + 1e-12) for i in range(0, len(x), win)])
db = 20 * np.log10(energy)
cuts, start = [0], 0
while len(x) - start > 12 * sr:
    lo, hi = (start + 6 * sr) // win, min(len(energy), (start + 12 * sr) // win)
    k = lo + int(np.argmin(db[lo:hi]))
    start = k * win
    cuts.append(start)
cuts.append(len(x))
toks = []
for a, b in zip(cuts, cuts[1:]):
    s = rec.create_stream()
    s.accept_waveform(sr, x[a:b])
    rec.decode_stream(s)
    r = s.result
    for t, ts in zip(r.tokens, r.timestamps):
        toks.append({"tok": t, "t": round(a / sr + ts, 3)})
print(json.dumps({"text": "".join(t["tok"] for t in toks).replace("▁", " ").strip(), "tokens": toks}, ensure_ascii=False))
