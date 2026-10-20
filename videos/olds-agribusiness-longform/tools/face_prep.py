"""Prepare the director's face videos (S01 opening, S12 closing). Run from project root:
    python3 -I tools/face_prep.py      (OLDS_FACE_DIR overrides the source folder)
then:  python3 -I tools/build.py

Input : ../../plans/olds-agribusiness-longform/face/olds_face_open.mp4, olds_face_close.mp4
        (phone landscape 1080p30; may arrive downscaled to 720p for the GitHub 25 MB limit -> upscaled here)
Steps : trim head/tail stillness (silence > 0.6 s at the ends, keeps 0.3 s) -> 1920x1080 30 fps (scale+crop to fill,
        lanczos) -> light colour lift -> H.264 CRF 16 + AAC, original sound with highpass/afftdn + loudnorm I=-16.
Output: assets/face/open.mp4, close.mp4 + <name>.words.json (caption/cue timing, same method as audio_prep.py).
Captions follow what was actually said: if the director paraphrased, edit the S01/S12 rows in script.py to the
spoken words (never numbers/facts) and rebuild.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_prep import dur, row_words, silences, transcribe  # noqa: E402
from script import SCENES  # noqa: E402

SRC = os.environ.get("OLDS_FACE_DIR", os.path.join("..", "..", "plans", "olds-agribusiness-longform", "face"))
OUT = os.path.join("assets", "face")
TMP = os.path.join(".hyperframes", "face-tmp")


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    for sc in [s for s in SCENES if s.get("kind") == "face"]:
        name = sc["face"]
        src = os.path.join(SRC, f"olds_face_{name}.mp4")
        if not os.path.exists(src):
            print(f"{name}: {src} not found - placeholder stays")
            continue
        probe = os.path.join(TMP, f"{name}.wav")
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "48000", probe])
        D = dur(probe)
        sil = silences(probe, "-38dB", 0.6)
        a = max(0.0, sil[0][1] - 0.3) if sil and sil[0][0] < 0.05 else 0.0
        b = min(D, sil[-1][0] + 0.3) if sil and sil[-1][1] > D - 0.05 else D
        vf = "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,fps=30,setsar=1,eq=brightness=0.02:saturation=1.05"
        af = "highpass=f=70,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11"
        dst = os.path.join(OUT, f"{name}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src, "-vf", vf, "-af", af,
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-movflags", "+faststart", dst])
        wav = os.path.join(TMP, f"{name}-clean.wav")
        run(["ffmpeg", "-y", "-v", "error", "-i", dst, "-vn", "-ac", "1", "-ar", "48000", wav])
        words = transcribe(wav) or row_words(sc["rows"], wav)
        json.dump(words, open(os.path.join(OUT, f"{name}.words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name}: {D:.1f}s -> {dur(dst):.1f}s (trim {a:.2f}~{b:.2f})")


if __name__ == "__main__":
    main()
