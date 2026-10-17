"""Shared: turn the owner's own recording into narration.wav + timing.json.

process(root, removes=[...], scenes=[(id, "caption | caption | ...")], marks={key: (scene_id, "substring")}, ...)
- removes: (start, end) spans in ORIGINAL time to cut (lead-in, retakes, long pauses). 20 ms crossfades.
- scenes: the script AS SPOKEN after the cuts; '|' separates caption chunks.
- Times come from a local Korean ASR pass (sherpa-onnx zipformer-ko, token timestamps) of the original,
  aligned to the script text character-by-character (difflib), so ASR spelling mistakes don't matter.
"""
import json, subprocess, pathlib, difflib, re, sys
import numpy as np

SR = 48000
ASR_PY = "/home/user/asr/asr.py"


def _asr(src, out):
    if not out.exists():
        subprocess.run([sys.executable, ASR_PY, str(src), str(out)], check=True, stdout=subprocess.DEVNULL)
    return json.loads(out.read_text())


def _norm(s):
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def process(root, removes, scenes, marks, lead=0.3, tail=2.6, speech_end=None, scene_lead=0.3, loudness=-16):
    root = pathlib.Path(root)
    rec = root / "assets" / "audio" / "recording"
    src = rec / "original.m4a"
    A = _asr(src, rec / "asr.json")
    removes = sorted(removes)

    def keep_t(t):
        return not any(a <= t < b for a, b in removes)

    def new_t(t):
        return t - sum(min(b, t) - a for a, b in removes if a < t)

    # ---- ASR chars with original times (drop the ones inside cut spans) ----
    chars = []  # (char, t)
    toks = A["tokens"]
    for k, (tok, ts) in enumerate(toks):
        nxt = toks[k + 1][1] if k + 1 < len(toks) else ts + 0.3
        s = _norm(tok)
        for m, c in enumerate(s):
            t = ts + (nxt - ts) * m / max(1, len(s))
            if keep_t(t):
                chars.append((c, t))
    asr_s = "".join(c for c, _ in chars)

    # ---- script chars ----
    script = []  # (scene_idx, chunk_idx, text)
    for i, (sid, txt) in enumerate(scenes):
        for j, ch in enumerate([c.strip() for c in txt.split("|")]):
            script.append((i, j, ch))
    flat, owner = [], []  # normalized script chars + (script item index, pos in raw text)
    for n, (_, _, ch) in enumerate(script):
        for p, c in enumerate(ch):
            if _norm(c):
                flat.append(c); owner.append((n, p))
    scr_s = "".join(flat)
    sm = difflib.SequenceMatcher(None, scr_s, asr_s, autojunk=False)
    tmap = [None] * len(scr_s)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            tmap[a + k] = chars[b + k][1]
    # interpolate gaps
    known = [k for k, v in enumerate(tmap) if v is not None]
    if not known:
        raise SystemExit("alignment failed")
    for k in range(len(tmap)):
        if tmap[k] is None:
            lo = max([q for q in known if q < k], default=None)
            hi = min([q for q in known if q > k], default=None)
            if lo is None: tmap[k] = tmap[hi] - 0.1 * (hi - k)
            elif hi is None: tmap[k] = tmap[lo] + 0.1 * (k - lo)
            else: tmap[k] = tmap[lo] + (tmap[hi] - tmap[lo]) * (k - lo) / (hi - lo)
    ratio = sm.ratio()

    def item_start(n):
        k = next(q for q, (o, _) in enumerate(owner) if o == n)
        return tmap[k]

    def item_end(n):
        k = max(q for q, (o, _) in enumerate(owner) if o == n)
        return tmap[k] + 0.18

    # ---- audio: cut, clean, level ----
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(src), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    x = np.frombuffer(raw, dtype=np.float32).copy()
    dur = len(x) / SR
    first = item_start(0)
    se = speech_end if speech_end is not None else min(dur, item_end(len(script) - 1) + 0.35)
    cuts = [(0.0, max(0.0, first - lead))] + [r for r in removes if r[1] > first - lead]
    cuts = sorted(cuts)
    # merge
    mc = []
    for a, b in cuts:
        if mc and a <= mc[-1][1]: mc[-1] = (mc[-1][0], max(mc[-1][1], b))
        else: mc.append((a, b))
    removes = mc

    def new_t(t):  # noqa: F811  (recompute with the lead cut)
        return t - sum(min(b, t) - a for a, b in removes if a < t)

    keep, last = [], 0.0
    for a, b in removes:
        if a > last: keep.append((last, a))
        last = max(last, b)
    keep.append((last, min(dur, se + 0.4)))
    xf = int(0.02 * SR)
    segs = []
    for a, b in keep:
        seg = x[int(a * SR):int(b * SR)].copy()
        if len(seg) > 2 * xf:
            r = np.linspace(0, 1, xf, dtype=np.float32)
            seg[:xf] *= r; seg[-xf:] *= r[::-1]
        segs.append(seg)
    out = np.concatenate(segs)
    total = round(new_t(se) + tail, 3)
    out = np.concatenate([out, np.zeros(max(0, int(total * SR) - len(out)), dtype=np.float32)])[: int(total * SR)]
    tmp = rec / "edited.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)], input=out.tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-af",
                    "highpass=f=80,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
                    f"loudnorm=I={loudness}:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", "44100", "-ac", "1",
                    str(root / "assets" / "audio" / "narration.wav")], check=True)

    # ---- timing ----
    T = {"voice": "owner recording", "align_ratio": round(ratio, 3), "scenes": [], "marks": {}}
    by_scene = {}
    for n, (i, j, ch) in enumerate(script):
        by_scene.setdefault(i, []).append({"text": ch, "start": round(new_t(item_start(n)), 3), "_end": round(new_t(item_end(n)), 3)})
    starts = [0.0] + [round(by_scene[i][0]["start"] - scene_lead, 3) for i in range(1, len(scenes))]
    for i, (sid, _) in enumerate(scenes):
        end = starts[i + 1] if i + 1 < len(scenes) else total
        caps = by_scene[i]
        for j, c in enumerate(caps):
            c["end"] = caps[j + 1]["start"] if j + 1 < len(caps) else round(end, 3)
            c["speech_end"] = min(c.pop("_end"), c["end"])
        T["scenes"].append({"id": sid, "start": starts[i], "duration": round(end - starts[i], 3),
                            "audio_end": caps[-1]["speech_end"], "captions": caps})
    for key, (sid, sub) in marks.items():
        i = [s for s, _ in scenes].index(sid)
        n0 = next(n for n, it in enumerate(script) if it[0] == i)
        # find substring in the scene's concatenated normalized text
        idx = [q for q, (o, _) in enumerate(owner) if script[o][0] == i]
        sc_s = "".join(flat[q] for q in idx)
        p = sc_s.find(_norm(sub))
        if p < 0:
            raise SystemExit(f"mark {key}: '{sub}' not in scene {sid}")
        T["marks"][key] = round(new_t(tmap[idx[p]]), 3)
    T["total"] = total
    (root / "timing.json").write_text(json.dumps(T, ensure_ascii=False, indent=1))
    print("align ratio", round(ratio, 3), "total", total)
    for s in T["scenes"]:
        print(s["id"], s["start"], s["duration"], [(c["text"][:12], c["start"]) for c in s["captions"]])
    print("marks", T["marks"])
    return T
