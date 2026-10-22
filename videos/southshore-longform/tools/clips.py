"""B-roll clips cut from the RSB school videos (plans/southshore-longform/assets/school-videos/).
Segments come from plans/riverside-video/01_TIMESTAMP_SHEET.md (no student face close-ups).
The source is 2.35:1 letterboxed inside 1920x1080: crop the picture band, then a centred 16:9 window.
Run from project root:  python3 -I tools/clips.py   -> assets/clips/<name>.mp4 (muted, 1280x720, 30fps)
"""
import os
import subprocess

SRC = os.path.join("..", "..", "plans", "southshore-longform", "assets", "school-videos")
OUT = os.path.join("assets", "clips")

CLIPS = {  # name: (video, in, out, label)
    "her-sign": ("heritage", 0.1, 1.9, "학교 간판"),
    "her-foyer": ("heritage", 5.0, 8.1, "중앙 홀"),
    "her-library": ("heritage", 11.4, 13.2, "도서관"),
    "her-dance": ("heritage", 24.6, 26.3, "예술반 무용"),
    "her-weights": ("heritage", 41.4, 42.8, "웨이트룸"),
    "her-gym": ("heritage", 44.4, 46.7, "체육관"),
    "her-ican": ("heritage", 46.9, 48.2, "컴퓨터반"),
    "her-studio": ("heritage", 53.6, 55.3, "방송 스튜디오"),
    "her-bus": ("heritage", 61.2, 62.9, "스쿨버스"),
    "cen-sign": ("centennial", 0.1, 2.7, "학교 입구"),
    "cen-atrium": ("centennial", 7.8, 10.1, "계단 아트리움"),
    "cen-library": ("centennial", 26.3, 28.0, "도서관"),
    "cen-stage": ("centennial", 30.8, 34.5, "대강당"),
    "cen-lab": ("centennial", 40.9, 42.7, "TaG 실험실"),
    "cen-gym": ("centennial", 55.7, 57.5, "체육관"),
    "cen-art": ("centennial", 63.6, 65.3, "미술실"),
    "sli-sign": ("sli", 0.2, 3.8, "학교 입구"),
    "sli-library": ("sli", 23.3, 24.8, "도서관"),
    "sli-garden": ("sli", 28.7, 30.5, "야외 정원"),
    "sli-gym": ("sli", 34.7, 36.4, "체육관"),
    "sli-music": ("sli", 43.0, 44.3, "음악실"),
    "sli-art": ("sli", 49.2, 50.9, "미술실"),
    "stj-entrance": ("stjohns", 0.1, 4.1, "학교 정문"),
    "stj-hub": ("stjohns", 13.4, 15.0, "학생 휴게실"),
    "stj-gym": ("stjohns", 27.9, 30.0, "큰 체육관"),
    "stj-cafe": ("stjohns", 49.5, 51.7, "카페테리아"),
    "stj-theatre": ("stjohns", 51.9, 56.2, "극장 무대"),
    "stj-motto": ("stjohns", 56.4, 61.8, "학교 표어 벽"),
}


def dur(name):
    _, a, b, _ = CLIPS[name]
    return round(b - a, 3)


def cut():
    os.makedirs(OUT, exist_ok=True)
    for name, (vid, a, b, _) in CLIPS.items():
        out = os.path.join(OUT, name + ".mp4")
        if os.path.exists(out):
            continue
        src = os.path.join(SRC, vid + ".mp4")
        vf = "crop=1444:812:238:134,scale=1280:720,fps=30,format=yuv420p"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-i", src, "-t", str(round(b - a, 3)),
                        "-vf", vf, "-an", "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-movflags", "+faststart", out],
                       check=True)
        print("cut", out)


if __name__ == "__main__":
    cut()
