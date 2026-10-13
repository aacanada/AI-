#!/usr/bin/env python3
"""SCRIPT.md 문장 ↔ 녹음 단어 타이밍(narration_edit.words.json)을 글자 단위로 정렬해 timing.json을 만든다.
- 챕터(Line)마다 영상 시작/길이, 챕터 기준 로컬 문장 시각(R), 자막 큐를 기록한다."""
import re, json, difflib, subprocess, pathlib
proj = pathlib.Path(__file__).resolve().parent.parent
IDS = ["ch00-hook", "ch01-why", "ch02-where", "ch03-nelson", "ch04-castlegar", "ch05-selkirk",
       "ch06-rcip", "ch07-data", "ch08-majors", "ch09-family", "ch10-reality", "ch11-roadmap"]
LEAD, OVER, TAIL = 0.9, 0.7, 3.0

t = (proj / "SCRIPT.md").read_text(encoding="utf-8")
parts = re.split(r"^## Line (\d+).*$", t, flags=re.M)
lines = [[l.strip() for l in parts[i + 1].splitlines() if l.startswith("    ") and l.strip()] for i in range(1, len(parts), 2)]

words = json.load(open(proj / "assets/voice/narration_edit.words.json"))["words"]
sc, st = [], []
norm = lambda c: c.lower()
for w in words:
    for ch in w["text"]:
        if ch.isalnum(): sc.append(norm(ch)); st.append((w["start"], w["end"]))
# 스크립트 글자열 (숫자는 녹음에서 한글로 읽혀 매칭이 안 될 수 있으니 주변 글자로 보간)
rows = [(li, ri, r) for li, L in enumerate(lines) for ri, r in enumerate(L)]
tc = []
for k, (li, ri, r) in enumerate(rows):
    for ci, ch in enumerate(r):
        if ch.isalnum(): tc.append((k, ci, norm(ch)))
m = {}
for a, b, size in difflib.SequenceMatcher(None, [c for *_, c in tc], sc, autojunk=False).get_matching_blocks():
    for x in range(size): m[a + x] = st[b + x]
def t_at(idx, end=False):
    rng = range(idx, -1, -1) if end else range(idx, len(tc))
    for j in rng:
        if j in m: return m[j][1] if end else m[j][0]
    return None
# row → [first tc index, last tc index]
span = {}
for i, (k, ci, c) in enumerate(tc):
    span.setdefault(k, [i, i])[1] = i
row_t = {k: (t_at(a), t_at(b, True)) for k, (a, b) in span.items()}

def chunk(s, maxlen=34):
    if len(s) <= maxlen: return [s]
    out, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > maxlen: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    if len(out) > 1 and len(out[-1]) < 8:
        last = out.pop(); out[-1] += " " + last
    return out

voice_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice/narration_edit.mp3")]))
line_start = []
for li in range(len(lines)):
    k0 = next(k for k, (l, *_ ) in enumerate(rows) if l == li)
    line_start.append(row_t[k0][0])
chapters = []
for li, cid in enumerate(IDS):
    start = 0.0 if li == 0 else round(line_start[li] - LEAD, 2)
    end = round(line_start[li + 1] - LEAD + OVER, 2) if li + 1 < len(IDS) else round(voice_dur + TAIL, 2)
    sents, caps = [], []
    for k, (l, ri, r) in enumerate(rows):
        if l != li: continue
        a, b = row_t[k]
        sents.append({"t": round(a - start, 2), "end": round(b - start, 2), "text": r})
        # 자막: 문장 안 글자 위치 비례로 조각 시간 배분
        pieces = chunk(r); n = sum(len(p) for p in pieces); acc = 0
        for p in pieces:
            pa = a + (b - a) * acc / n; acc += len(p); pb = a + (b - a) * acc / n
            caps.append({"t": round(pa, 2), "end": round(pb, 2), "text": p})
    chapters.append({"id": cid, "start": start, "duration": round(end - start, 2), "R": [s["t"] for s in sents], "sentences": sents, "captions": caps})
total = round(voice_dur + TAIL, 2)
json.dump({"total": total, "voice": "assets/voice/narration_edit.mp3", "voice_dur": round(voice_dur, 2), "chapters": chapters},
          open(proj / "timing.json", "w"), ensure_ascii=False, indent=1)
for c in chapters: print(f'{c["id"]:16s} start={c["start"]:7.2f} dur={c["duration"]:6.2f}  R={c["R"]}')
print("total", total)
