"""Compare what the director said (whisper, assets/voice/_asr.json) with the script rows (tools/script.py).
Run from project root:  python3 -I tools/asr_check.py > ASR_CHECK.md
Lists every stretch where the transcript differs from the script (ASR errors included - read by ear before acting)
and flags every number / fact the scene must contain (brief 6장) that the transcript does not show."""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES  # noqa: E402

asr = json.load(open(os.path.join("assets", "voice", "_asr.json"), encoding="utf-8"))
MUST = {  # alternatives with | (digits vs Korean numerals as whisper may write either)
    "s03": ["2023년 7월 31일|2023년7월31일", "16.6|16점6", "18분|십팔분", "다섯 개|5개", "샹플랭"],
    "s04": ["2021년|2021", "코퀴틀람", "1만 1,900|11,900|만천구백|1만1900", "8%|8퍼센트|팔퍼센트", "50명|오십명", "30명|삼십명",
            "35명|삼십오명", "25만|이십오만", "425명|사백이십오명", "20%|20퍼센트|이십퍼센트", "590명|오백구십명", "1%|1퍼센트|일퍼센트"],
    "s05": ["19곳|열아홉곳|십구곳", "4곳|네곳|네 곳", "88.5|88점5|팔십팔점오", "1위|일위"],
    "s06": ["1,600|1600|천육백", "TaG|태그|티에이지", "400명|사백명"],
    "s07": ["80%|80퍼센트|팔십퍼센트", "70|칠십", "30|삼십"],
    "s08": ["2027-28|2027|이천이십칠", "3만 2천|32,000|삼만이천", "1만 8,800|18,800|만팔천팔백", "2월 2일|2월2일", "9월 8일|9월8일"],
    "s09": ["18분|십팔분"],
    "s10": ["18분|십팔분", "19곳|열아홉곳|십구곳", "4곳|네곳|네 곳", "카카오톡"],
}
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
    for w in MUST.get(sid, []):
        if not any(norm(v) in norm(said) for v in w.split("|")):
            flags.append(f"**'{w.split('|')[0]}'** 를 녹음 받아쓰기에서 못 찾음 (귀로 확인)")
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
