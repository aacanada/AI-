"""Compare what the director said (whisper, assets/voice/_asr.json) with the script rows (tools/script.py).
Run from project root:  python3 -I tools/asr_check.py > ASR_CHECK.md
Lists every stretch where the transcript differs from the script (ASR errors included - read by ear before acting)
and flags the brief's must-check words: 관리형 / 만 5세 (must NOT be said), 만 4세 (must be said in s08)."""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES  # noqa: E402

asr = json.load(open(os.path.join("assets", "voice", "_asr.json"), encoding="utf-8"))
SKIP = re.compile(r"[\s.,?!\"'“”‘’·~|\-]")


def norm(t):
    return SKIP.sub("", t).lower()


print("# ASR 대조 (원장님 녹음 vs SCRIPT.txt)\n")
print("whisper(turbo) 받아쓰기와 대본을 글자 단위로 맞춰 다른 부분만 적었습니다. ASR 오인식도 섞여 있으니 판정 칸을 함께 보세요.\n")
for sc in SCENES:
    sid = sc["id"]
    if sid not in asr or not asr[sid].get("whisper"):
        print(f"## {sid} - ASR 없음\n")
        continue
    said = asr[sid]["whisper"]
    a, b = norm(" ".join(sc["rows"])), norm(said)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    print(f"## {sid} {sc['name']}  (일치율 {sm.ratio():.0%}, 길이 {asr[sid]['src_dur']}s → 트림 {asr[sid]['dur']}s)\n")
    flags = []
    for w in ("관리형", "조기유학"):
        if w in said:
            flags.append(f"**'{w}'** 이(가) 녹음에 있음")
    if re.search(r"(만\s*5\s*세|만\s*다섯\s*살|다섯\s*살|5세)", said):
        flags.append("**'만 5세/다섯 살'** 이(가) 녹음에 있음")
    if sid == "s08":
        flags.append("'만 4세' 확인: " + ("녹음에 있음 ✅" if re.search(r"(4\s*세|네\s*살)", said) else "**녹음에서 못 찾음**"))
    for f in flags:
        print(f"- {f}")
    rows = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        ctx = a[max(0, i1 - 6):i1]
        rows.append(f"| …{ctx}[{a[i1:i2] or '∅'}] | [{b[j1:j2] or '∅'}] |")
    if rows:
        print("\n| 대본 (…앞 문맥[대본]) | 녹음 받아쓰기 |\n|---|---|")
        print("\n".join(rows))
    print(f"\n<details><summary>받아쓰기 전문</summary>\n\n{said}\n\n</details>\n")
