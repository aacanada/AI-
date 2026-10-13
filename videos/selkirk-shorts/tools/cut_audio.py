#!/usr/bin/env python3
"""롱폼 녹음(narration_edit.mp3)에서 숏폼 구간을 잘라 이어 붙이고 timing.json(구간별 시작/끝, 자막)을 만든다."""
import json, subprocess, pathlib, re
here = pathlib.Path(__file__).resolve().parent; proj = here.parent
LF = proj.parent / "selkirk-rcip-longform"
W = json.load(open(LF / "assets/voice/narration_edit.words.json"))["words"]
cfg = json.load(open(here / "shorts.json"))
LEAD_IN, GAP, PAD = 0.5, 0.32, 0.10
def find(text, near, after=None):
    c = [w for w in W if w["text"] == text and (after is None or w["start"] >= after)]
    return min(c, key=lambda w: abs(w["start"] - near))
def chunks(s, maxlen=17):
    # 쉼표·마침표에서 먼저 끊고, 긴 구절만 단어 단위로 나눈다
    import re as _re
    phrases = [p.strip() for p in _re.split(r"(?<=[,.?!])\s+", s) if p.strip()]
    out = []
    for ph in phrases:
        if len(ph) <= maxlen + 3: out.append(ph); continue
        words = ph.split(" "); n = len(ph); k = -(-n // maxlen)  # 필요한 줄 수
        target = n / k; cur = ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > target + 3: out.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        if cur: out.append(cur)
    # 너무 짧은 조각은 앞에 붙인다
    res = []
    for p in out:
        if res and len(p) <= 4 and len(res[-1]) + len(p) < maxlen + 6: res[-1] += " " + p
        else: res.append(p)
    return res
for sid, sc in cfg.items():
    d = proj / sid / "assets" / "voice"; d.mkdir(parents=True, exist_ok=True)
    parts, t, segs = [], LEAD_IN, []
    for i, s in enumerate(sc["segs"]):
        w0 = find(s["from"], s["near"]); w1 = find(s["to"], s["near"] + 2, after=w0["start"])
        a = w0["start"] - s.get("lead", PAD); b = w1["end"] + 0.16
        f = d / f"seg{i}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(LF / "assets/voice/narration_edit.mp3"),
                        "-af", "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse", "-ar", "44100", "-ac", "1", str(f)], check=True)
        dur = b - a
        txt = s["text"]; pcs = chunks(txt); n = sum(len(p) for p in pcs); acc = 0; caps = []
        # 말이 실제로 시작/끝나는 구간에 자막 배분
        sa, sb = t + (w0["start"] - a), t + (w1["end"] - a)
        for p in pcs:
            pa = sa + (sb - sa) * acc / n; acc += len(p); pb = sa + (sb - sa) * acc / n
            caps.append({"t": round(pa, 2), "end": round(pb, 2), "text": p})
        segs.append({"i": i, "t": round(t, 2), "end": round(t + dur, 2), "speak": round(sa, 2), "text": txt, "captions": caps})
        parts.append(str(f)); t += dur + GAP
    # 이어 붙이기: 앞 0.5초 무음 + 구간 사이 무음
    sil = d / "sil.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono", "-t", str(GAP), str(sil)], check=True)
    lead = d / "lead.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono", "-t", str(LEAD_IN), str(lead)], check=True)
    seq = [str(lead)]
    for i, p in enumerate(parts):
        seq.append(p)
        if i < len(parts) - 1: seq.append(str(sil))
    lst = d / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in seq))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "44100", "-b:a", "160k", str(d / "voice.mp3")], check=True)
    vd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(d / "voice.mp3")]))
    for p in d.glob("*.wav"): p.unlink()
    lst.unlink()
    json.dump({"voice_dur": round(vd, 2), "segs": segs, "S": [s["t"] for s in segs]}, open(proj / sid / "timing.json", "w"), ensure_ascii=False, indent=1)
    print(sid, "voice", round(vd, 2), "S", [s["t"] for s in segs])
