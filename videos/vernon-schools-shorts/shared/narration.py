"""Owner-recorded narration as one file PER SCENE (short-N_s1.m4a ... short-N_sK.m4a) -> narration.wav + timing.json.

Usage: python3 shared/narration.py <short-dir> <audio-dir> [--max-pause 0.5] [--tempo 1.0]

The scene files are joined (with 1.5 s of silence) into one take whose scene cuts are known exactly, then
narration_full.py does the rest with the same rules as the one-take recordings: clean (highpass, afftdn,
loudnorm I=-16), trim silence, cap pauses inside a scene, 0.35 s between scenes, chunk windows aligned to
pauses.  Stops if a scene file is missing or cannot be decoded.
"""
import json, pathlib, subprocess, sys, tempfile

SHARED = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
SRC = pathlib.Path(sys.argv[2]).resolve()
spec = json.loads((ROOT / "script.json").read_text())
files = [SRC / f"short-{spec['n']}_s{k + 1}.m4a" for k in range(len(spec["scenes"]))]
missing = [f.name for f in files if not f.exists()]
if missing:
    sys.exit("missing recordings: " + ", ".join(missing))
SIL = 1.5
tmp = pathlib.Path(tempfile.mkdtemp())
wavs, cuts, t = [], [], 0.0
for f in files:
    w = tmp / (f.stem + ".wav")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-ar", "44100", "-ac", "1", str(w)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"cannot decode {f.name}: {r.stderr.strip()}")
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(w)]))
    wavs.append(w)
    t += d
    cuts.append(round(t + SIL / 2, 3))
    t += SIL
cuts = cuts[:-1]
inputs, labels = [], []
for k, w in enumerate(wavs):
    inputs += ["-i", str(w)]
    labels.append(f"[{k}:a]")
    if k + 1 < len(wavs):
        labels.append(f"[g{k}]")
gens = ";".join(f"aevalsrc=0:d={SIL}:s=44100[g{k}]" for k in range(len(wavs) - 1))
take = tmp / f"short-{spec['n']}_scenes.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
                gens + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]", "-map", "[out]", str(take)], check=True)
spec_files = ", ".join(f.name for f in files)
spec["narration_files"] = spec_files
subprocess.run([sys.executable, str(SHARED / "narration_full.py"), str(ROOT), str(SRC), "--take", str(take),
                "--cuts", ",".join(map(str, cuts)), *sys.argv[3:]], check=True)
tj = json.loads((ROOT / "timing.json").read_text())
tj["source"]["file"] = spec_files
tj["source"]["method"] = "per-scene files (exact scene cuts) + pause/script-ratio chunk alignment"
(ROOT / "timing.json").write_text(json.dumps(tj, ensure_ascii=False, indent=1))
