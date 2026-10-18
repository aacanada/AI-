"""Shared: owner facecam clips → edited narration + edited face video(s) + timing.json.

edit(root, clips_dir, scenes, marks, ...)
- scenes: [(scene_id, cam_name, [(t0, t1), ...], "caption | caption | ...")]
  (t0, t1) = spans to KEEP in that clip's own time (seconds). Captions are the words AS SPOKEN inside the kept spans.
- marks: {key: (scene_id, "substring of the scene's captions")} → output time of that word.
- Times come from the local Korean ASR (zipformer-ko token timestamps, assets/facecam/asr/<cam>.json),
  aligned to the caption text character-by-character (difflib), so ASR spelling mistakes don't matter.
- Every kept span is snapped to the frame grid; consecutive spans overlap by XF frames for an audio crossfade.
  The face video cuts hard in the middle of each crossfade.
"""
import json, subprocess, pathlib, difflib, re
import numpy as np

FPS = 30
SR = 48000
XF = 2  # frames of audio crossfade at every cut


def _norm(s):
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def _fr(t):
    return int(round(t * FPS))


def _pcm(src):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(src), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def _snap(x, t, win=0.12):
    """move a cut point to the quietest 10 ms inside ±win (no clicks / clipped syllables)."""
    a, b = int(max(0, t - win) * SR), int(min(len(x) / SR, t + win) * SR)
    hop = int(0.01 * SR)
    if b - a < 2 * hop:
        return t
    e = [float(np.mean(x[i:i + hop] ** 2)) for i in range(a, b - hop, hop)]
    k = int(np.argmin(e))
    return (a + k * hop + hop / 2) / SR


def items_to_scene(sid, cam, items, pre=0.15, post=0.3, keep_gap=0.6, pad_in=0.12, pad_out=0.22):
    """items: [(island_start, island_end, "text with | caption breaks")] in clip time, in speaking order.
    Islands closer than keep_gap stay joined (natural pause); longer pauses and anything not listed are cut.
    The first word gets `pre` s of lead-in and the last word `post` s of tail."""
    spans = []
    for k, (a, b, _) in enumerate(items):
        a0 = a - (pre if k == 0 else pad_in)
        b0 = b + (post if k == len(items) - 1 else pad_out)
        if spans and a - items[k - 1][1] <= keep_gap:
            spans[-1][1] = b0
        else:
            spans.append([a0, b0])
    txt = " ".join(t.strip() for _, _, t in items)
    txt = re.sub(r"\s*\|\s*", " | ", txt).strip(" |")
    return (sid, cam, [tuple(x) for x in spans], txt, [(a, b, t) for a, b, t in items])


def edit(root, clips_dir, scenes, marks, scene_gap=0.2, tail=0.0, loudness=-14, out_audio="narration-facecam.wav",
         timing="timing-facecam.json", faces=(), tail_extra=0.0):
    root, clips_dir = pathlib.Path(root), pathlib.Path(clips_dir)
    pcm, asr = {}, {}
    for _, cam, _, _, _ in scenes:
        if cam not in pcm:
            pcm[cam] = _pcm(clips_dir / f"{cam}.mp4")
            asr[cam] = json.loads((clips_dir / "asr" / f"{cam}.json").read_text())

    # ---- segments on the frame grid ----
    segs = []  # dict(scene, cam, a, b) in frames (source), p = output start frame
    pos = 0
    for si, (sid, cam, spans, _, _) in enumerate(scenes):
        for k, (t0, t1) in enumerate(spans):
            a, b = _fr(_snap(pcm[cam], t0)), _fr(_snap(pcm[cam], t1))
            if segs and segs[-1]["scene"] == si:
                pos -= XF  # overlap for the crossfade
            elif segs:
                pos += _fr(scene_gap)
            segs.append({"scene": si, "cam": cam, "a": a, "b": b, "p": pos})
            pos += b - a
    total_f = pos + _fr(tail)
    TOTAL = total_f / FPS

    def out_t(si, cam, t):
        """source time t of scene si → output time (None if t falls in a removed part)."""
        best = None
        for s in segs:
            if s["scene"] == si and s["a"] / FPS - 0.02 <= t <= s["b"] / FPS + 0.02:
                return s["p"] / FPS + (t - s["a"] / FPS)
            if s["scene"] == si and s["a"] / FPS > t and best is None:
                best = s["p"] / FPS  # in a gap → the next kept span's start
        return best

    # ---- audio: crossfaded concat, then clean + level ----
    out = np.zeros(int(TOTAL * SR) + SR, dtype=np.float32)
    xf = int(XF / FPS * SR)
    for s in segs:
        seg = pcm[s["cam"]][int(s["a"] / FPS * SR):int(s["b"] / FPS * SR)].copy()
        r = np.linspace(0, 1, xf, dtype=np.float32)
        seg[:xf] *= r
        seg[-xf:] *= r[::-1]
        p = int(s["p"] / FPS * SR)
        out[p:p + len(seg)] += seg
    out = out[:int(TOTAL * SR)]
    rec = root / "assets" / "audio"
    rec.mkdir(parents=True, exist_ok=True)
    tmp = rec / "facecam-edited.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)], input=out.tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-af",
                    "highpass=f=80,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
                    f"loudnorm=I={loudness}:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", "48000", "-ac", "1",
                    str(rec / out_audio)], check=True)
    tmp.unlink()

    # ---- face videos (one per requested framing) ----
    for f in faces:
        _face_video(clips_dir, segs, total_f, **f)

    # ---- captions: align the as-spoken text to the ASR of the kept spans ----
    T = {"voice": "owner facecam", "fps": FPS, "scenes": [], "marks": {}, "cuts": [], "segments": []}
    for si, (sid, cam, spans, txt, items) in enumerate(scenes):
        chunks = [c.strip() for c in txt.split("|") if c.strip()]
        kept = [s for s in segs if s["scene"] == si]
        flat, owner = [], []
        for j, ch in enumerate(chunks):
            for c in ch:
                if _norm(c):
                    flat.append(c); owner.append(j)
        scr_s = "".join(flat)
        # each item's characters are spread over the voiced 20 ms frames of its island (pauses get no characters)
        tmap = []
        x = pcm[cam]
        hop = int(0.02 * SR)
        for a, b, t in items:
            n = len(_norm(t.replace("|", "")))
            fr = np.arange(int(a / 0.02), int(b / 0.02))
            e = np.array([20 * np.log10(np.sqrt(np.mean(x[k * hop:(k + 1) * hop] ** 2)) + 1e-9) for k in fr])
            v = fr[e > max(-48, np.percentile(e, 30) - 2)] * 0.02 if len(e) else np.array([a])
            if len(v) == 0: v = np.array([a])
            for m in range(n):
                tmap.append(float(v[min(len(v) - 1, int(m * len(v) / max(1, n)))]))
        assert len(tmap) == len(scr_s), (sid, len(tmap), len(scr_s))
        sm = type("R", (), {"ratio": lambda self: 1.0})()
        o = [out_t(si, cam, t) for t in tmap]
        st = kept[0]["p"] / FPS
        en = (kept[-1]["p"] + kept[-1]["b"] - kept[-1]["a"]) / FPS
        caps = []
        for j, ch in enumerate(chunks):
            ks = [q for q, w in enumerate(owner) if w == j]
            caps.append({"text": ch, "start": round(max(st, o[ks[0]] - 0.08), 3), "speech_end": round(o[ks[-1]] + 0.2, 3)})
        for j, c in enumerate(caps):
            c["end"] = caps[j + 1]["start"] if j + 1 < len(caps) else round(en, 3)
            c["speech_end"] = min(c["speech_end"], c["end"])
        T["scenes"].append({"id": sid, "start": round(st, 3), "speech_end": round(en, 3), "captions": caps, "align_ratio": round(sm.ratio(), 3)})
        T["_flat_" + sid] = (scr_s, o)
        for s in kept[1:]:
            T["cuts"].append(round(s["p"] / FPS + XF / FPS / 2, 3))
    # scene windows: each scene runs until the next one starts (the gap belongs to the outgoing scene)
    for i, s in enumerate(T["scenes"]):
        nxt = T["scenes"][i + 1]["start"] if i + 1 < len(T["scenes"]) else TOTAL + tail_extra
        s["duration"] = round(nxt - s["start"], 3)
        s["captions"][-1]["end"] = round(min(s["captions"][-1]["end"] + 0.15, nxt), 3)
    for key, (sid, sub) in marks.items():
        scr_s, o = T["_flat_" + sid]
        p = scr_s.find(_norm(sub))
        if p < 0:
            raise SystemExit(f"mark {key}: '{sub}' not in scene {sid}")
        T["marks"][key] = round(o[p], 3)
    for k in [k for k in T if k.startswith("_flat_")]:
        del T[k]
    T["segments"] = [{"scene": scenes[s["scene"]][0], "cam": s["cam"], "src": [s["a"] / FPS, s["b"] / FPS], "at": s["p"] / FPS} for s in segs]
    T["total"] = round(TOTAL + tail_extra, 3)
    (root / timing).write_text(json.dumps(T, ensure_ascii=False, indent=1))
    print("total", T["total"])
    for s in T["scenes"]:
        print(s["id"], s["start"], s["duration"], "align", s["align_ratio"], [(c["text"][:10], c["start"]) for c in s["captions"]])
    print("marks", T["marks"])
    return T


def _face_video(clips_dir, segs, total_f, out, w, h, crop=None, crf=17):
    """picture-only face track: hard cuts at the middle of each audio crossfade, lanczos upscale + light sharpen.
    Each segment is encoded on its own (frame-accurate seek), then joined with the concat demuxer (no re-encode)."""
    import tempfile
    out = pathlib.Path(out)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="face-", dir=out.parent))
    cr = f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else ""
    vf = f"{cr}scale={w}:{h}:flags=lanczos,unsharp=5:5:0.45:5:5:0,fps={FPS},format=yuv420p"
    lst = []
    for k, s in enumerate(segs):
        start = s["p"] + (XF // 2 if k and segs[k - 1]["scene"] == s["scene"] else 0)
        end = segs[k + 1]["p"] + (XF // 2 if segs[k + 1]["scene"] == s["scene"] else 0) if k + 1 < len(segs) else total_f
        a = s["a"] + (start - s["p"])
        f = tmp / f"s{k:03d}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a / FPS:.4f}", "-i", str(clips_dir / f"{s['cam']}.mp4"), "-frames:v", str(end - start),
                        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-g", "30", "-r", str(FPS),
                        "-video_track_timescale", "15360", str(f)], check=True)
        lst.append(f"file '{f.name}'")
    (tmp / "list.txt").write_text("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    print("face video", out)
