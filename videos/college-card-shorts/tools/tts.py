#!/usr/bin/env python3
"""ElevenLabs narration (voice "일곱번째") for college_a / college_b.

  python3 tools/tts.py            -> both shorts (skips existing mp3)
  python3 tools/tts.py a --force  -> regenerate one
  python3 tools/tts.py --dry      -> print spoken text, no API call

Script lines come from plans/college-card-shorts/SCRIPT.txt unchanged. Each line is cut into
caption chunks (display text); only the spoken copy of each chunk is respelled (numbers, English).
Writes <short>/assets/voice.mp3 (raw), voice.m4a (trimmed), and timing.json (chunk start/end).
No fallback TTS: any API error stops the run.
"""
import base64, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
SCRIPT = REPO / "plans/college-card-shorts/SCRIPT.txt"
VOICE = "vxpRrQegUpenYtez6hz1"
MODEL = "eleven_multilingual_v2"
LEAD, TAIL = 0.35, 0.6
# ElevenLabs voice_settings.speed per short (script text cannot change; A is long at 1.0 = 59.6 s)
SPEED = {"a": 1.2, "b": 1.1}

SAY = [
    ("1,000만 원대", "천만 원대"), ("170만 원", "백칠십만 원"), ("121만 원", "백이십일만 원"),
    ("90만 원대", "구십만 원대"), ("3,700달러", "삼천칠백 달러"), ("830달러", "팔백삼십 달러"),
    ("110달러", "백십 달러"), ("40달러", "사십 달러"), ("주 24시간", "주 이십사 시간"),
    ("약 5시간", "약 다섯 시간"), ("만 11세", "만 십일 세"), ("1년", "일 년"), ("1:1", "일대일"),
    ("0원", "영 원"), ("AA Canada", "에이에이 캐나다"), ("canlog", "캔로그"),
]

def say(s):
    for a, b in SAY:
        s = s.replace(a, b)
    return s

def voice_settings():
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{VOICE}/settings",
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=60))

def parse():
    out, cur = {}, None
    for raw in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([AB])\. college_", raw)
        if m:
            cur = m.group(1).lower(); out[cur] = []; continue
        if cur is None or not raw.strip() or raw.startswith("=") or raw.startswith("(B 학원비"):
            continue
        line = re.sub(r"\s{2,}\(.*\)\s*$", "", raw).strip()
        out[cur].append(line)
    return out

def chunks(line):
    """Caption chunks: split after sentence ends, then after commas if a piece is long."""
    sents = re.findall(r".+?(?:[.?!](?=\s|$)|$)", line)
    res = []
    for s in (x.strip() for x in sents if x.strip()):
        if len(s) <= 22:
            res.append(s); continue
        parts = re.split(r"(?<=,)\s+", s)
        buf = ""
        for p in parts:
            if buf and len(buf) + len(p) > 24:
                res.append(buf); buf = p
            else:
                buf = f"{buf} {p}".strip()
        if buf:
            res.append(buf)
    return res

def main():
    args = sys.argv[1:]
    dry, force = "--dry" in args, "--force" in args
    only = [a for a in args if not a.startswith("--")] or ["a", "b"]
    lines = parse()
    for k in only:
        out = ROOT / f"college_{k}"
        (out / "assets").mkdir(parents=True, exist_ok=True)
        items = []  # (line_idx, display, spoken)
        for li, line in enumerate(lines[k]):
            for c in chunks(line):
                items.append((li, c, say(c)))
        text = " ".join(i[2] for i in items)
        left = set(re.findall(r"[0-9A-Za-z]+", text))
        print(f"[{k}] {len(text)} chars{'  NOT RESPELLED: ' + str(left) if left else ''}\n{text}\n")
        if dry:
            continue
        mp3 = out / "assets/voice.mp3"
        aj = out / "assets/alignment.json"
        if force or not mp3.exists():
            req = urllib.request.Request(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                data=json.dumps({"text": text, "model_id": MODEL, "voice_settings": {**voice_settings(), "speed": SPEED[k]}}).encode(),
                headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "content-type": "application/json"},
            )
            try:
                res = json.load(urllib.request.urlopen(req, timeout=300))
            except urllib.error.HTTPError as e:
                sys.exit(f"ElevenLabs HTTP {e.code}: {e.read().decode()[:500]}\nstopping (no fallback TTS)")
            mp3.write_bytes(base64.b64decode(res["audio_base64"]))
            aj.write_text(json.dumps({"voice": VOICE, "model": MODEL, "text": text, "alignment": res["alignment"]}, ensure_ascii=False))
        al = json.loads(aj.read_text())["alignment"]
        st, en, ch = al["character_start_times_seconds"], al["character_end_times_seconds"], al["characters"]
        assert len(ch) == len(text), "alignment length mismatch"
        ns = [i for i, c in enumerate(ch) if not c.isspace()]
        sp0, sp1 = st[ns[0]], en[ns[-1]]
        off = sp0 - LEAD
        m4a = out / "assets/voice.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-af",
                        f"atrim=start={max(0, off):.3f}:end={sp1 + 0.05:.3f},asetpts=PTS-STARTPTS,adelay={round(max(0, -off) * 1000)}:all=1,apad=pad_dur={TAIL}",
                        "-ac", "1", "-c:a", "aac", "-b:a", "160k", str(m4a)], check=True)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(m4a)]).decode())
        pos, cues = 0, []
        for li, disp, spk in items:
            s, e = pos, pos + len(spk)
            nsi = [i for i in range(s, e) if not ch[i].isspace()]
            cues.append({"line": li, "text": disp, "spoken": spk,
                         "start": round(st[nsi[0]] - off, 3), "end": round(en[nsi[-1]] - off, 3)})
            pos = e + 1
        (out / "timing.json").write_text(json.dumps({"audioDuration": round(dur, 3), "cues": cues}, ensure_ascii=False, indent=1))
        print(f"[{k}] audio {dur:.2f}s, {len(cues)} cues")

if __name__ == "__main__":
    main()
