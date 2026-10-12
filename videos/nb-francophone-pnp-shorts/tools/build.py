"""Build index.html (1080x1920 Shorts) from timing.json.
Captions sit in the TOP band (Shorts UI covers the bottom). Re-run after tts.py."""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "timing.json").read_text())
TOTAL = T["total"]

HL = ["뉴브런즈윅입니다", "영주권", "불어 5레벨", "LMIA 면제", "취업!", "Strategic Initiative", "불어권 근로자",
      "정규직 풀타임", "6개월", "NCLC 5", "경력 1년", "낮다", "NCLC 7", "가능!", "물 흐르듯", "저절로 충족",
      "불어권 우대", "최대 규모", "254명", "말하기·듣기", "읽기·쓰기", "4영역", "AA Canada", "C16"]
HL_RE = re.compile("|".join(re.escape(h) for h in sorted(HL, key=len, reverse=True)))

def cap_html(text):
    out, pos = [], 0
    for m in HL_RE.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        out.append(f'<span class="hl">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)

def r(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")

# ---------- scene bodies (visual zone, below the caption band) ----------
from scenes import SCENES

scene_divs, cap_divs = [], []
for i, s in enumerate(T["scenes"]):
    scene_divs.append(
        f'<section id="{s["id"]}" class="clip scene" data-start="{r(s["start"])}" data-duration="{r(s["duration"])}" data-track-index="1">'
        f'<div class="stage" id="{s["id"]}-in">{SCENES[s["id"]]}</div></section>')
    for j, c in enumerate(s["captions"]):
        cap_divs.append(
            f'<div id="cap-{i}-{j}" class="clip cap" data-start="{r(c["start"])}" data-duration="{r(c["end"] - c["start"])}" data-track-index="2">'
            f'<div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{cap_html(c["text"])}</span></div></div>')

page = (ROOT / "tools" / "template.html").read_text()
page = (page.replace("__TOTAL__", r(TOTAL))
            .replace("__SCENES__", "\n      ".join(scene_divs))
            .replace("__CAPTIONS__", "\n      ".join(cap_divs))
            .replace("__TIMING__", json.dumps(T, ensure_ascii=False)))
(ROOT / "index.html").write_text(page)
print("index.html written; total", TOTAL)
