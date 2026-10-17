"""Build index.html (1080x1920 Shorts) from timing.json. Captions in the TOP band (Shorts UI covers the bottom).
Pipeline: python3 tools/from_recording.py → bash tools/make.sh → render."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from pyk import kt, odo, bg, captions, sfx_tags, install, page, r

T = json.loads((ROOT / "timing.json").read_text())
M, S, TOTAL = T["marks"], T["scenes"], T["total"]
W, H = 1080, 1920
MESH = ("radial-gradient(760px 760px at 72% 22%, rgba(58,48,150,0.85) 0%, rgba(58,48,150,0) 70%),"
        "radial-gradient(640px 640px at 18% 62%, rgba(58,134,255,0.25) 0%, rgba(58,134,255,0) 70%),"
        "radial-gradient(760px 760px at 82% 86%, rgba(110,20,50,0.7) 0%, rgba(110,20,50,0) 70%),"
        "linear-gradient(180deg, #0b0f1f 0%, #1b1f4a 100%)")
DOTS = ["255,200,61", "58,134,255", "215,38,61", "255,255,255"]

CHECK = '<svg viewBox="0 0 100 100" class="ck"><path d="M22 54 L42 73 L80 30" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
CAP = ('<svg viewBox="0 0 120 80" class="gcap"><path d="M60 6 L116 28 L60 50 L4 28 Z" fill="#ffc83d"/>'
       '<path d="M28 40 V58 C28 70 92 70 92 58 V40 L60 53 Z" fill="#ffc83d"/><path d="M108 32 V58" stroke="#ffffff" stroke-width="5"/></svg>')
STUDENT = ('<svg viewBox="0 0 120 140" class="stu"><circle cx="60" cy="40" r="26" fill="#ffd9b0"/>'
           '<path d="M34 34 C34 10 86 10 86 34 C78 24 44 24 34 34 Z" fill="#2b2b45"/>'
           '<path d="M14 138 C14 92 34 78 60 78 C86 78 106 92 106 138 Z" fill="#3a86ff"/>'
           '<path d="M48 80 L60 104 L72 80 Z" fill="#ffffff"/><path d="M56 90 L60 118 L64 90 Z" fill="#d7263d"/></svg>')
SKY = ("M0 300 V220 H60 V180 H110 V230 H150 V140 H190 V100 H230 V140 H260 V210 H300 V160 H340 V60 H380 V20 H420 V60 H460 V160 H500 V120 "
       "H560 V200 H600 V150 H660 V90 H700 V150 H740 V220 H790 V170 H840 V240 H900 V190 H950 V230 H1000 V200 H1080 V300")
COURSES = ["영어", "수학", "심리학", "경제학", "컴퓨터", "생물학", "사회학"]

SCENES = {
"s1-hook": f"""
  <div class="hs" id="s1-hs">{STUDENT}<div class="hs-t">HIGH SCHOOL</div><div class="hs-s">고등학생 · 11~12학년</div><i class="sweep" id="s1-sw"></i></div>
  <div class="blocks" id="s1-blocks">{"".join(f'<div class="cb" style="left:{(k % 4) * 240 + (60 if k >= 4 else -60) + 120}px;top:{(k // 4) * 128}px"><b>UNIV</b><span>{c}</span></div>' for k, c in enumerate(COURSES))}</div>
  <div class="cnt" id="s1-cnt"><span class="cnt-n">7</span><span class="cnt-u">과목</span></div>
  <div class="zero" id="s1-zero" data-layout-allow-overlap><span class="zero-p">+$0</span><span class="zero-u">추가 학비</span></div>
  <i class="ring" id="s1-ring" style="left:540px;top:1290px"></i>
  <div class="fn" id="s1-fn" style="left:60px;right:60px;top:1420px">* 학교 측 안내(2026.10) · 아카데미 재학 중 알렉산더 컬리지 과목 최대 7개</div>
""",
"s2-school": f"""
  <svg class="sky" viewBox="0 0 1080 300" width="1080" height="300"><path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#3a86ff" stroke-width="5" stroke-linejoin="round"/>
    <path class="ln" pathLength="1" d="M0 300 H1080" stroke="#ffc83d" stroke-width="6"/></svg>
  <div class="tower" id="s2-tower">
    <div class="tw-roof">570 DUNSMUIR · DOWNTOWN VANCOUVER</div>
    <div class="fl fl-a" id="s2-fa"><div class="fl-k">ALEXANDER ACADEMY</div><div class="fl-s">사립 고등학교 · 10~12학년</div>
      <div class="wins">{"".join('<i class="win"></i>' for _ in range(6))}</div></div>
    <div class="fl fl-c" id="s2-fc"><div class="fl-k">ALEXANDER COLLEGE</div><div class="fl-s">대학 과정 · 학점 이전</div>
      <div class="wins">{"".join('<i class="win"></i>' for _ in range(6))}</div></div>
    <i class="lift" id="s2-lift"></i><div class="dotm" id="s2-dot">{STUDENT}</div>
  </div>
  <div class="brk" id="s2-brk"><span>같은 건물</span></div>
  <div class="fn" id="s2-fn" style="left:60px;right:60px;top:1418px">* BC주 고등학교 졸업장 과정 · 자매학교 알렉산더 컬리지</div>
""",
"s3-credits": f"""
  <div class="stacks" id="s3-stacks">{"".join(f'<div class="stk" style="left:{k * 136}px">' + "".join(f'<i class="coin" style="bottom:{m * 46}px">3</i>' for m in range(3)) + '</div>' for k in range(7))}</div>
  <div class="tot" id="s3-tot">
    <div class="tot-a"><span class="odo odo-a" data-layout-allow-overflow data-layout-allow-overlap>{odo("7", "a")}</span><span class="tot-u">과목</span></div>
    <div class="tot-x">=</div>
    <div class="tot-a"><span class="odo odo-b" data-layout-allow-overflow data-layout-allow-overlap>{odo("21", "b")}</span><span class="tot-u">학점</span></div>
  </div>
  <i class="ring" id="s3-ring" style="left:540px;top:700px"></i>
  <div class="yr1" id="s3-yr1"><div class="yr1-l">캐나다 대학 <b>1학년</b> 수업량 · 보통 8~10과목</div>
    <div class="cells">{"".join(f'<i class="cell{" c7" if k < 7 else ""}"></i>' for k in range(10))}</div>
    <div class="yr1-tag" id="s3-tag">고등학교에서 미리 <b>7과목</b></div></div>
""",
"s4-race": f"""
  <div class="race" id="s4-race">
    <div class="axis">{"".join(f'<span style="left:{220 + k * 180}px">{t}</span>' for k, t in enumerate(["고교 졸업", "+1년", "+2년", "+3년", "+4년"]))}</div>
    <div class="lane ln-a" id="s4-la"><div class="lab">일반 경로</div>
      <div class="seg sg-u" style="left:220px;width:720px" id="s4-ua"><span>대학 1 → 4학년</span></div>
      <div class="run" id="s4-ra"><i></i></div><div class="flag" id="s4-fa" style="left:940px">{CAP}</div></div>
    <div class="lane ln-b" id="s4-lb"><div class="lab">알렉산더 경로</div>
      <div class="seg sg-boost" style="left:60px;width:150px" id="s4-boost"><span>7과목</span></div>
      <div class="seg sg-c" style="left:220px;width:180px" id="s4-cb"><span>컬리지</span></div>
      <div class="seg sg-t" style="left:400px;width:360px" id="s4-tb"><span>편입 → 대학</span></div>
      <div class="run run-b" id="s4-rb"><i></i></div><div class="flag" id="s4-fb" style="left:760px">{CAP}</div></div>
    <div class="gap" id="s4-gap"><i></i></div>
  </div>
  <div class="cal" id="s4-cal">{"".join(f'<div class="pg" style="z-index:{12 - k}"><b>{m}월</b></div>' for k, m in enumerate([9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]))}</div>
  <div class="stamp st-gold" id="s4-stamp" data-layout-allow-overlap>-1 YEAR</div>
  <div class="fn" id="s4-fn" style="left:60px;right:60px;top:1418px">* 대학·전공별 편입 학년과 인정 학점은 다릅니다</div>
""",
"s5-transfer": f"""
  <div class="duo" id="s5-duo">
    <div class="sc sc-l" id="s5-l"><div class="sc-h">직행 입학</div><div class="sc-s">Direct Entry</div>
      <div class="gauge"><i id="s5-gf"></i><span class="g95">95%+</span></div><div class="sc-k">고등학교 <b>내신</b> 싸움</div>
      <div class="warn" id="s5-warn">!</div></div>
    <div class="sc sc-r" id="s5-r"><div class="sc-h">편입</div><div class="sc-s">Transfer</div>
      <div class="gpa"><span class="gpa-n">3.0+</span><span class="gpa-d">/ 4.33</span></div><div class="sc-k">컬리지 <b>대학 성적</b>으로</div>
      <div class="ok" id="s5-ok">{CHECK}</div></div>
  </div>
  <div class="persp p5"><div class="dip" id="s5-dip"><div class="dip-t">BACHELOR'S DEGREE</div><div class="dip-k">똑같은 UBC 학위</div>
    <div class="dip-s">직행이든 편입이든 졸업장은 같습니다</div><div class="seal">{CAP}</div><i class="sweep" id="s5-sw"></i></div></div>
  <div class="fn" id="s5-fn" style="left:60px;right:60px;top:1418px">* GPA 3.0+는 학교 측 일반 안내 · 학과별 기준 상이</div>
""",
"s6-cta": f"""
  <div class="clk" id="s6-clk"><svg viewBox="0 0 300 300" width="300" height="300"><circle cx="150" cy="150" r="138" fill="#14183a" stroke="#ffffff" stroke-width="9"/>
    {"".join(f'<path d="M150 18 V{40 if h % 3 == 0 else 30}" stroke="#ffffff" stroke-width="{7 if h % 3 == 0 else 3}" transform="rotate({h * 30} 150 150)"/>' for h in range(12))}
    <path id="s6-hh" d="M150 150 V78" stroke="#ffc83d" stroke-width="12" stroke-linecap="round"/><path id="s6-mh" d="M150 150 V40" stroke="#3a86ff" stroke-width="8" stroke-linecap="round"/>
    <circle cx="150" cy="150" r="11" fill="#d7263d"/></svg></div>
  <div class="word w-late" id="s6-late">1년 늦어짐</div>
  <div class="word w-ahead" id="s6-ahead">1년 앞당김</div>
  <div class="gate" id="s6-gate"><i class="gl" id="s6-gl"></i><i class="gr" id="s6-gr"></i><div class="gate-t">UNIVERSITY</div></div>
  <div class="leak" id="s6-leak"></div>
  <div class="cta-logo" id="s6-logo">{kt("AA CANADA", "kt logo-kt")}</div>
  <div class="cta-sub" id="s6-sub">알렉산더 아카데미 · 밴쿠버 조기유학</div>
  <div class="cta-btn" id="s6-btn"><i class="btn-ring" id="s6-bring"></i>무료 상담 · 카톡 <b>canlog</b></div>
  <div class="fn" id="s6-fn" style="left:60px;right:60px;top:1418px">* 학비·수강 과목·편입 기준은 변경될 수 있습니다 · 2026.10 기준</div>
""",
}

scene_divs = [f'<section id="{s["id"]}" class="scene" style="width:{W}px;height:{H}px;background-color:#0b0f1f">{bg(i + 1, W, H, MESH, DOTS, speed_lines=14)}'
              f'<div class="cam" id="{s["id"]}-cam">{SCENES[s["id"]]}</div></section>' for i, s in enumerate(S)]
HL = ["7개나", "추가 학비", "알렉산더 아카데미", "알렉산더 컬리지", "7과목", "21학점", "1학년", "대부분", "1년", "UBC", "편입",
      "내신", "대학 성적", "똑같은", "앞당기는", "조기유학", "AA캐나다"]
cap_divs = captions(T, HL)

def C(i, j): return S[i]["captions"][j]["start"]
TR = [S[i]["start"] - 0.25 for i in range(1, len(S))]
sfx = [("whoosh", TR[0] - 0.05, 0.3), ("swell", TR[1] - 0.9, 0.24), ("glitch-1", TR[2], 0.2), ("whoosh", TR[3] - 0.05, 0.3), ("whoosh-short", TR[4], 0.3),
       ("click-soft", 0.35, 0.25)]
sfx += [("pop", M["k7"] - 0.25 + k * 0.09, 0.18) for k in range(7)]
sfx += [("impact-bass-1", M["free"] + 0.3, 0.34), ("sparkle", M["free"] + 0.32, 0.18),
        ("ping", M["aca"] + 0.05, 0.22), ("ping", M["col"] + 0.05, 0.22), ("stamp", M["bldg"] + 0.25, 0.32), ("whoosh-short", M["early"] - 0.2, 0.22)]
sfx += [("click", M["m7"] - 0.4 + k * 0.06, 0.16) for k in range(0, 21, 3)]
sfx += [("ding", M["m21"] + 0.55, 0.3), ("impact-bass-2", M["m21"] + 0.3, 0.26), ("riser-short", M["most"] - 1.6, 0.18), ("ding", M["most"] + 0.6, 0.26),
        ("whoosh", M["grad"] - 0.05, 0.22), ("riser-short", M["fast"] - 2.05, 0.2), ("sparkle", M["fast"] - 0.3, 0.2), ("stamp", M["fast"] + 0.25, 0.36), ("impact-bass-1", M["fast"] + 0.28, 0.28),
        ("notification", M["naesin"] + 0.3, 0.16), ("pop", M["gpa"] + 0.35, 0.26), ("swell", M["same"] - 0.9, 0.22), ("chime", M["same"] + 0.3, 0.22),
        ("glitch-2", M["ahead"] - 0.05, 0.2), ("riser-short", C(5, 3) - 1.85, 0.2), ("impact-bass-2", C(5, 3) + 0.05, 0.26), ("sparkle", M["aa"] + 0.3, 0.22), ("chime", M["aa"] + 0.5, 0.2)]

install(ROOT)
page(ROOT, "template.html", TOTAL=r(TOTAL), SCENES="\n      ".join(scene_divs), CAPTIONS="\n      ".join(cap_divs),
     SFX="\n      ".join(sfx_tags(ROOT, sfx, TOTAL)), TIMING=T)
print("index.html written; total", TOTAL)
