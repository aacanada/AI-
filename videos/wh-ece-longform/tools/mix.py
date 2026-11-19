#!/usr/bin/env python3
"""Final audio mix from build/timeline.json.

VO (per-scene, leveled to -16 LUFS) placed at vo_start
BGM: ElevenLabs tracks A/B alternated with 4s crossfades, 1.5s fade-in, 3s fade-out,
     ducked under VO with sidechaincompress (VO as key)
SFX: placed at HyperFrames animation cue times, 10-14 dB under VO
Master: two-pass loudnorm -16 LUFS, true peak <= -1.5 dBTP  -> audio/mix_master.wav
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFXDIR = os.path.join(ROOT, "..", "..", "plans", "wh-ece-longform", "audio", "sfx")
BUILD = os.path.join(ROOT, "build", "audio")
SR = 48000
SFX_FILES = {"transition_ding": "transition_ding.mp3", "tick": "tick.wav", "ding": "ding.wav", "stamp": "stamp.wav"}
# gain targets relative to VO (-16 LUFS); loudness-based except tick (peak-based, too short to gate)
SFX_TARGET = {"transition_ding": ("lufs", -28.5), "ding": ("lufs", -29.0), "stamp": ("lufs", -28.0), "tick": ("peak", -17.0)}
BGM_UNDUCKED_LUFS = -26.0


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(" ".join(cmd)[:400], r.stderr[-2000:], file=sys.stderr)
        raise SystemExit(1)
    return r.stderr


def measure(path, extra_af=None):
    af = (extra_af + "," if extra_af else "") + "ebur128=peak=true"
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", af, "-f", "null", "-"])
    tail = err[err.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", tail).group(1))
    P = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail).group(1))
    return I, P


def main():
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json"), encoding="utf-8"))
    total = tl["total"]
    os.makedirs(BUILD, exist_ok=True)

    # 1) VO track
    inputs, filt, labels = [], [], []
    for i, s in enumerate(tl["scenes"]):
        p = os.path.join(ROOT, "audio", "vo", f"{s['id']}.mp3")
        I, _ = measure(p)
        g = -16.0 - I
        inputs += ["-i", p]
        d = int(round(s["vo_start"] * 1000))
        filt.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,volume={g:.2f}dB,adelay={d}|{d}[v{i}]")
        labels.append(f"[v{i}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad,atrim=0:{total}[vo]")
    vo = os.path.join(BUILD, "vo.wav")
    run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(filt), "-map", "[vo]", "-c:a", "pcm_s24le", "-ar", str(SR), vo])

    # 2) BGM bed: A B A B ... crossfaded, leveled
    A = os.path.join(ROOT, "audio", "bgm", "el_ece_acoustic_A.mp3")
    B = os.path.join(ROOT, "audio", "bgm", "el_ece_acoustic_B.mp3")
    gains = {k: -18.0 - measure(p)[0] for k, p in (("A", A), ("B", B))}
    n = int(total // 170) + 2
    seq = [("A", A) if k % 2 == 0 else ("B", B) for k in range(n)]
    inputs, filt = [], []
    for i, (k, p) in enumerate(seq):
        inputs += ["-i", p]
        filt.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,volume={gains[k]:.2f}dB[b{i}]")
    cur = "b0"
    for i in range(1, n):
        filt.append(f"[{cur}][b{i}]acrossfade=d=4:c1=tri:c2=tri[x{i}]")
        cur = f"x{i}"
    filt.append(f"[{cur}]atrim=0:{total},asetpts=N/SR/TB[bed]")
    bed = os.path.join(BUILD, "bed.wav")
    run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(filt), "-map", "[bed]", "-c:a", "pcm_s24le", "-ar", str(SR), bed])
    bedI, _ = measure(bed)
    bed_gain = BGM_UNDUCKED_LUFS - bedI

    # 3) duck bed with VO sidechain, fades
    ducked = os.path.join(BUILD, "bed_ducked.wav")
    fo = total - 3.0
    run(["ffmpeg", "-y", "-hide_banner", "-i", bed, "-i", vo, "-filter_complex",
         f"[0:a]volume={bed_gain:.2f}dB[b];[1:a]asplit=2[k][kk];[kk]anullsink;"
         f"[b][k]sidechaincompress=threshold=0.015:ratio=10:attack=60:release=700:makeup=1:knee=4[d];"
         f"[d]afade=t=in:st=0:d=1.5,afade=t=out:st={fo}:d=3[o]",
         "-map", "[o]", "-c:a", "pcm_s24le", "-ar", str(SR), ducked])

    # 4) SFX track
    sfx_gain = {}
    for k, f in SFX_FILES.items():
        mode, tgt = SFX_TARGET[k]
        I, P = measure(os.path.join(SFXDIR, f))
        sfx_gain[k] = (tgt - I) if mode == "lufs" else (tgt - P)
    inputs, filt, labels = [], [], []
    for i, e in enumerate(tl["sfx"]):
        inputs += ["-i", os.path.join(SFXDIR, SFX_FILES[e["name"]])]
        d = int(round(max(0, e["t"]) * 1000))
        filt.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,volume={sfx_gain[e['name']]:.2f}dB,adelay={d}|{d}[s{i}]")
        labels.append(f"[s{i}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad,atrim=0:{total}[sx]")
    sfxw = os.path.join(BUILD, "sfx.wav")
    run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(filt), "-map", "[sx]", "-c:a", "pcm_s24le", "-ar", str(SR), sfxw])

    # 5) sum + two-pass loudnorm
    pre = os.path.join(BUILD, "premaster.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", vo, "-i", ducked, "-i", sfxw, "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0[m]", "-map", "[m]", "-c:a", "pcm_s24le", "-ar", str(SR), pre])
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", pre, "-af", "loudnorm=I=-16:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(err[err.rfind("{"):err.rfind("}") + 1])
    ln = (f"loudnorm=I=-16:TP=-2.0:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}")
    master = os.path.join(ROOT, "audio", "mix_master.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", pre, "-af", ln + f",aresample={SR},alimiter=limit=0.79:attack=2:release=50:level=false",
         "-c:a", "pcm_s24le", "-ar", str(SR), master])

    # lightweight copy referenced by index.html (the master wav stays local; final mp4 audio is encoded from it)
    run(["ffmpeg", "-y", "-hide_banner", "-i", master, "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), os.path.join(ROOT, "audio", "mix.m4a")])
    # report
    rep = {}
    rep["master_I"], rep["master_peak"] = measure(master)
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", master, "-af", "loudnorm=I=-16:TP=-1.5:print_format=json", "-f", "null", "-"])
    rep["master_TP"] = float(json.loads(err[err.rfind("{"):err.rfind("}") + 1])["input_tp"])
    rep["vo_I"] = measure(vo)[0]
    rep["bed_unducked_I"] = measure(bed, f"volume={bed_gain:.2f}dB")[0]
    # bed level while VO speaks: measure ducked bed inside the longest VO window
    s = max(tl["scenes"], key=lambda x: x["vo_len"])
    rep["bed_under_vo_I"] = measure(ducked, f"atrim={s['vo_start'] + 1}:{s['vo_start'] + s['vo_len'] - 1}")[0]
    rep["vo_window_I"] = measure(vo, f"atrim={s['vo_start'] + 1}:{s['vo_start'] + s['vo_len'] - 1}")[0]
    rep["duck_gap_dB"] = round(rep["vo_window_I"] - rep["bed_under_vo_I"], 1)
    rep["sfx_count"] = len(tl["sfx"])
    rep["sfx_by_type"] = {k: sum(1 for e in tl["sfx"] if e["name"] == k) for k in SFX_FILES}
    rep["sfx_gain_dB"] = {k: round(v, 1) for k, v in sfx_gain.items()}
    rep["total_s"] = total
    json.dump(rep, open(os.path.join(ROOT, "build", "mix_report.json"), "w"), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
