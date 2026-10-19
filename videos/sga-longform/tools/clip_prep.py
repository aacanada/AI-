"""Prepare the 4 student testimonial clips (SGA official YouTube, reuse permitted). Run from project root:
    python3 -I tools/clip_prep.py
then:  python3 -I tools/build.py   (placeholder cards switch to the real clips automatically)

Source per clip, first found:
  1. ../../plans/sga-longform/assets/clips/Tn.mp4  (uploaded by Aside; full video or a pre-cut segment)
  2. yt-dlp download of the brief's ranges (blocked in the cloud sandbox: www.youtube.com is denied)
Full-length sources are cut to the brief's ranges +-1 s, then trimmed to speech start/end.
Output: assets/clips/Tn.mp4 (1920x1080, 30 fps, H.264 + AAC, loudnorm -16 LUFS).
Subtitles: provisional lines are spread over the clip. To time them exactly, write assets/clips/Tn.subs.json
[{"t": 0.4, "end": 3.1, "text": "..."}] (clip-local seconds) and fix wording to match the audio.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import CLIPS  # noqa: E402

UP = os.environ.get("SGA_CLIPS_DIR", os.path.join("..", "..", "plans", "sga-longform", "assets", "clips"))
OUT = os.path.join("assets", "clips")
TMP = os.path.join(".hyperframes", "clip-tmp")


def sec(mmss):
    m, s = mmss.split(":")
    return int(m) * 60 + float(s)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def speech_bounds(p):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silencedetect=noise=-35dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    D = dur(p)
    a = en[0] if st and st[0] < 0.05 and en else 0.0
    b = st[-1] if st and (len(en) < len(st)) else D
    return max(0, a - 0.15), min(D, b + 0.25)


def fetch(cid, info):
    os.makedirs(TMP, exist_ok=True)
    up = os.path.join(UP, f"{cid}.mp4")
    if os.path.exists(up):
        return up, dur(up) > max(sec(b) for _, b in info["ranges"]) - 1
    out = os.path.join(TMP, f"{cid}-dl.mp4")
    secs = sum((["--download-sections", f"*{sec(a) - 1:.0f}-{sec(b) + 1:.0f}"] for a, b in info["ranges"]), [])
    r = subprocess.run(["yt-dlp", "-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4", *secs, "-o", out, info["url"]], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        return None, False
    return out, False


def main():
    os.makedirs(OUT, exist_ok=True)
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30"
    for cid, info in CLIPS.items():
        src, full = fetch(cid, info)
        if not src:
            print(f"{cid}: no source (upload {UP}/{cid}.mp4) - placeholder stays")
            continue
        parts = []
        ranges = info["ranges"] if full else [(None, None)]
        for k, (a, b) in enumerate(ranges):
            seg = os.path.join(TMP, f"{cid}-{k}.mp4")
            cut = ["-ss", f"{sec(a) - 1:.2f}", "-to", f"{sec(b) + 1:.2f}"] if a else []
            subprocess.run(["ffmpeg", "-y", "-v", "error", *cut, "-i", src, "-vf", vf, "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-ar", "48000", seg], check=True)
            s0, s1 = speech_bounds(seg)
            seg2 = os.path.join(TMP, f"{cid}-{k}t.mp4")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s0:.2f}", "-to", f"{s1:.2f}", "-i", seg, "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-ar", "48000", seg2], check=True)
            parts.append(seg2)
        lst = os.path.join(TMP, f"{cid}.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        dst = os.path.join(OUT, f"{cid}.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                        "-movflags", "+faststart", dst], check=True)
        print(f"{cid}: {dur(dst):.1f}s -> {dst}")


if __name__ == "__main__":
    main()
