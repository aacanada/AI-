"""Prepare the 4 student testimonial clips (SGA official YouTube "Students' Voice", reuse permitted).
Run from project root:
    python3 -I tools/clip_prep.py      (SGA_CLIPS_DIR overrides the source folder)
then:  python3 -I tools/build.py

Sources (plans/sga-longform/assets/clips/, on main): <src>_video720.mp4 (silent 720p) + <src>_audio.m4a.
Steps per clip: mux video+audio (-c:v copy -c:a aac) -> cut the exact `cuts` from script.py (several cuts are
joined with 60 ms audio fades) -> crop the 16:9 window above the burned-in subtitles -> 1920x1080 30 fps
H.264 + AAC, loudnorm -16 LUFS. Output: assets/clips/Tn.mp4.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import CLIPS  # noqa: E402

UP = os.environ.get("SGA_CLIPS_DIR", os.path.join("..", "..", "plans", "sga-longform", "assets", "clips"))
OUT = os.path.join("assets", "clips")
TMP = os.path.join(".hyperframes", "clip-tmp")


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def muxed(src):
    out = os.path.join(TMP, f"{src}.mp4")
    if not os.path.exists(out):
        v, a = os.path.join(UP, f"{src}_video720.mp4"), os.path.join(UP, f"{src}_audio.m4a")
        if not (os.path.exists(v) and os.path.exists(a)):
            return None
        run(["ffmpeg", "-y", "-v", "error", "-i", v, "-i", a, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    for cid, info in CLIPS.items():
        src = muxed(info["src"])
        if not src:
            print(f"{cid}: source {info['src']}_video720.mp4 / _audio.m4a not found in {UP} - placeholder stays")
            continue
        w, h, x, y = info["crop"]
        vf = f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,fps=30,setsar=1"
        parts = []
        for k, (a, b) in enumerate(info["cuts"]):
            seg = os.path.join(TMP, f"{cid}-{k}.mp4")
            d = b - a
            af = f"afade=t=in:d=0.06,afade=t=out:st={d - 0.06:.3f}:d=0.06"
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-i", src, "-t", f"{d:.3f}", "-vf", vf, "-af", af,
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", seg.replace(".mp4", ".mov")])
            parts.append(seg.replace(".mp4", ".mov"))
        lst = os.path.join(TMP, f"{cid}.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        dst = os.path.join(OUT, f"{cid}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", dst])
        print(f"{cid}: {dur(dst):.2f}s ({sum(b - a for a, b in info['cuts']):.2f}s planned) -> {dst}")


if __name__ == "__main__":
    main()
