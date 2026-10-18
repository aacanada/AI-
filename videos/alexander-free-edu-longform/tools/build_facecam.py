"""Build facecam.html (1920x1080 longform, owner on camera, OBS-style face ↔ screen) from timing-facecam.json,
plus graphics.html (the same motion-graphics scenes alone, no face/captions/audio — the source the facecam shorts crop from).
Pipeline: python3 tools/facecam_edl.py → bash tools/make_facecam.sh → render -c facecam.html.
Layouts (FACECAM_EDIT_BRIEF 2): A face full · B graphics + face PiP (bottom right 480x270) · C face left 42% / graphics right 58%."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from pyk import kt, odo, bg, sfx_tags, install, r, esc, hl_html

T = json.loads((ROOT / "timing-facecam.json").read_text())
M, S, TOTAL = T["marks"], T["scenes"], T["total"]
W, H = 1920, 1080
SID = [s["id"] for s in S]
MESH = ("radial-gradient(900px 700px at 78% 18%, rgba(40,90,170,0.85) 0%, rgba(40,90,170,0) 70%),"
        "radial-gradient(800px 600px at 12% 70%, rgba(76,201,240,0.2) 0%, rgba(76,201,240,0) 70%),"
        "linear-gradient(180deg, #0a1a33 0%, #12305c 100%)")
DOTS = ["255,200,61", "76,201,240", "46,196,166", "255,255,255"]
CHECK = '<svg viewBox="0 0 100 100" class="ck"><path d="M22 54 L42 73 L80 30" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
XMARK = '<svg viewBox="0 0 100 100" class="ck"><path d="M28 28 L72 72 M72 28 L28 72" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" pathLength="1"/></svg>'
MOM = ('<svg viewBox="0 0 120 140" class="mom"><circle cx="60" cy="42" r="26" fill="#ffd9b0"/>'
       '<path d="M30 46 C26 8 94 8 90 46 C90 30 80 22 60 22 C40 22 30 30 30 46 Z" fill="#4a2b1d"/><path d="M28 44 C26 70 36 76 40 74 L36 46 Z M92 44 C94 70 84 76 80 74 L84 46 Z" fill="#4a2b1d"/>'
       '<path d="M14 138 C14 94 34 80 60 80 C86 80 106 94 106 138 Z" fill="#2ec4a6"/></svg>')
KID = ('<svg viewBox="0 0 120 140" class="kid"><circle cx="60" cy="50" r="24" fill="#ffd9b0"/><path d="M36 46 C36 20 84 20 84 46 C76 36 44 36 36 46 Z" fill="#2b2b45"/>'
       '<path d="M22 138 C22 98 38 86 60 86 C82 86 98 98 98 138 Z" fill="#ffc83d"/><rect x="74" y="92" width="26" height="36" rx="6" fill="#d7263d"/></svg>')
CAP = ('<svg viewBox="0 0 120 80" class="gcap"><path d="M60 6 L116 28 L60 50 L4 28 Z" fill="#ffc83d"/>'
       '<path d="M28 40 V58 C28 70 92 70 92 58 V40 L60 53 Z" fill="#ffc83d"/><path d="M108 32 V58" stroke="#ffffff" stroke-width="5"/></svg>')
PIN = '<svg viewBox="0 0 24 24" class="pinsvg"><path fill="#d7263d" d="M12 2C7.6 2 4 5.6 4 10c0 5.6 8 12 8 12s8-6.4 8-12c0-4.4-3.6-8-8-8zm0 11a3 3 0 110-6 3 3 0 010 6z"/></svg>'
SKY = ("M0 340 V250 H90 V200 H150 V260 H220 V160 H270 V110 H320 V160 H360 V240 H420 V180 H470 V70 H520 V20 H570 V70 H620 V180 H680 V130 "
       "H760 V220 H820 V160 H900 V90 H950 V160 H1010 V250 H1080 V190 H1150 V270 H1230 V200 H1300 V250 H1380 V180 H1440 V230 H1520 V150 H1570 V230 H1650 V260 H1740 V210 H1820 V270 H1920 V340")
MOUNT = "M0 150 L160 60 L280 120 L430 30 L580 110 L700 60 L860 130 L1020 40 L1180 110 L1320 60 L1480 120 L1640 50 L1780 100 L1920 70"
CHAPTERS = ["사립은 안 된다?", "BC주 기준", "준학사 = 학위", "한 학기 3과목", "라이브 온라인", "듀오링고 90", "학비", "PGWP 최대 3년", "꼭 확인할 3가지", "공립 컬리지 비교", "상담"]
WEEK = ["월", "화", "수", "목", "금"]
FN = "* BC주 교육부 재정지원 자격 기준 · 거주 교육청별 서류·절차 상이 · 2026.10 기준, 변경 가능"


def chip(i):
    return f'<div class="chap" id="chap-{i}"><b>{i + 1:02d}</b>{esc(CHAPTERS[i])}</div>'


SCENES = {
"s01-hook": """
  <div class="bub b1" id="s1-b1">사립은 안 된대요</div>
  <div class="bub b2" id="s1-b2">교육청마다 달라요</div>
  <div class="bub b3" id="s1-b3">공립만 가세요</div>
  <div class="ttl" id="s1-ttl"><div class="ttl-s">자녀무상교육의 기준은</div><div class="ttl-b">'사립 vs 공립'이 <span>아닙니다</span></div></div>
""",
"s02-rule": f"""
  <div class="persp p2"><div class="doc" id="s2-doc"><div class="doc-h"><i></i>BC MINISTRY OF EDUCATION · 재정지원 자격 기준</div>
    <div class="doc-r" id="s2-d1"><b>1</b>부모 학생비자 <em>1년 이상</em><i class="marker" id="s2-m1"></i></div>
    <div class="doc-r" id="s2-d2"><b>2</b>공립 컬리지·대학: <em>학위 · 디플로마</em><i class="marker" id="s2-m2"></i></div>
    <div class="doc-r" id="s2-d3"><b>3</b>사립 컬리지·대학: <em>학위(Degree)</em><i class="marker" id="s2-m3"></i></div></div></div>
  <div class="mx" id="s2-mx">
    <div class="mx-h"></div><div class="mx-h">학위 과정</div><div class="mx-h">디플로마</div>
    <div class="mx-r">공립</div><div class="mx-c" id="s2-c1"><i class="mk ok">{CHECK}</i></div><div class="mx-c" id="s2-c2"><i class="mk ok">{CHECK}</i></div>
    <div class="mx-r">사립</div><div class="mx-c" id="s2-c4"><i class="mk ok">{CHECK}</i><span>준학사</span></div><div class="mx-c" id="s2-c3"><i class="mk no">{XMARK}</i></div>
  </div>
  <div class="crit" id="s2-crit">기준 = <b>어떤 과정이냐</b></div>
  <div class="fn" id="s2-fn">* BC Ministry of Education · Eligibility of Students for Operating Grant Funding · 거주 교육청별 서류·절차 상이</div>
""",
"s03-degree": f"""
  <svg class="sky3" viewBox="0 0 1920 340" width="1920" height="340"><path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#4cc9f0" stroke-width="5" stroke-linejoin="round"/></svg>
  <div class="pin pin-dt" id="s3-dt">{PIN}<span>다운타운 캠퍼스</span></div>
  <div class="pin pin-bb" id="s3-bb">{PIN}<span>버나비 캠퍼스</span></div>
  <div class="persp p3"><div class="deg" id="s3-deg"><div class="dg-t">ASSOCIATE DEGREE</div><div class="dg-k">알렉산더 컬리지 준학사</div>
    <div class="dg-s">Associate of Arts · Associate of Science</div><i class="sweep" id="s3-sw"></i></div></div>
  <div class="stamp st-mint" id="s3-stamp" data-layout-allow-overlap>BC주 승인 학위 ✓</div>
  <div class="few" id="s3-few">사립 컬리지 중 <b>몇 안 되는 선택지</b></div>
""",
"s04-load": f"""
  <div class="ld-a" id="s4-a">
    <div class="ft-slots">{"".join(f'<div class="ft-s"><i class="blk" id="s4-k{k}">과목 {k + 1} · 3학점</i></div>' for k in range(3))}</div>
    <div class="ft-l"><span class="odo odo-c" data-layout-allow-overflow data-layout-allow-overlap>{odo("9", "c")}</span>학점 = <b>FULL-TIME</b></div>
    <div class="wk14" id="s4-14">한 학기 약 <b>14주</b></div>
  </div>
  <div class="week" id="s4-week"><div class="wk-h"><span></span>{"".join(f'<span>{d}</span>' for d in WEEK)}</div>
    {"".join(f'<div class="wk-r"><span>{t}</span>' + "".join(f'<i class="wc {c}" style="--d:{k}">{l}</i>' for k, (c, l) in enumerate(row)) + '</div>' for t, row in [
      ("오전", [("kd", "등교"), ("kd", "등교"), ("kd", "등교"), ("kd", "등교"), ("kd", "등교")]),
      ("수업", [("momc", "수업"), ("", ""), ("momc", "수업"), ("", ""), ("momc", "수업")]),
      ("오후", [("kd", "픽업"), ("kd", "픽업"), ("kd", "픽업"), ("kd", "픽업"), ("kd", "픽업")])])}
    <div class="hrs" id="s4-hrs">강의는 주당 <b>약 9시간</b></div><div class="summer" id="s4-sum">여름방학 <b>OFF</b> 가능</div></div>
  <div class="bars" id="s4-bars">
    <div class="bar-r" id="s4-br1"><span>편입 준비생</span><div class="bb">{"".join('<i class="bk5"></i>' for _ in range(5))}</div><em>학기당 5과목</em></div>
    <div class="bar-r me" id="s4-br2"><span>자녀무상교육 부모님</span><div class="bb">{"".join('<i class="bk5"></i>' for _ in range(3))}</div><em>3과목 = 풀타임</em></div></div>
""",
"s05-online": f"""
  <div class="lap" id="s5-lap"><div class="lap-s"><div class="lv"><i class="rec" id="s5-rec"></i>LIVE</div><div class="lv-t">ENGL 099 · 실시간 강의</div>
    <div class="tiles">{"".join('<i class="tile"></i>' for _ in range(6))}</div></div><div class="lap-b"></div></div>
  <div class="vs" id="s5-vs"><div class="vs-r x" id="s5-x"><i class="mk no">{XMARK}</i>녹화 강의</div><div class="vs-r o" id="s5-o"><i class="mk ok">{CHECK}</i>라이브 실시간 수업</div>
    <div class="vs-c" id="s5-c">학점 <b>동일하게 인정</b></div></div>
  <div class="day" id="s5-day"><i class="day-l" id="s5-line"></i>
    <div class="dn" id="s5-n1"><b>8:00</b>{KID}<span>아이 등교</span></div>
    <div class="dn dn-me" id="s5-n2"><b>10:00</b>{MOM}<span>집에서 라이브 수업</span></div>
    <div class="dn" id="s5-n3"><b>15:00</b>{KID}<span>픽업</span></div></div>
  <div class="fn" id="s5-fn">* 온라인으로 개설된 과목에 한함 · 학생비자 규정에 맞춰 온·오프라인 비율 설계</div>
""",
"s06-english": f"""
  <div class="gg" id="s6-gg"><div class="gg-l">듀오링고 점수</div>
    <div class="gg-bar"><i id="s6-fill"></i><span class="tick" style="left:{90 / 160 * 100:.2f}%"></span><span class="tick" style="left:{110 / 160 * 100:.2f}%"></span></div>
    <div class="flag f90" id="s6-f90" style="left:{90 / 160 * 100:.2f}%"><b>90</b>조건부 입학<em>≈ IELTS 5.0</em></div>
    <div class="flag f110" id="s6-f110" style="left:{110 / 160 * 100:.2f}%"><b>110</b>본과 바로 입학</div></div>
  <div class="sem" id="s6-sem"><div class="sem-l">첫 학기</div><i class="sb sb-e" id="s6-e">ENGL 099</i><i class="pl">+</i><i class="sb" id="s6-m1">전공</i><i class="pl">+</i><i class="sb" id="s6-m2">전공</i>
    <i class="pl">=</i><i class="sb sb-t" id="s6-t">3과목 풀타임</i></div>
  <div class="vs2" id="s6-vs"><div class="vs-r o" id="s6-o"><i class="mk ok">{CHECK}</i>첫 학기부터 학위 과정 학생</div></div>
  <div class="warn6" id="s6-x">90점 미만이면 어학원부터 → <b>어학원 기간은 무상 인정이 어려울 수 있음</b></div>
  <div class="ticket" id="s6-tk"><b>DUOLINGO</b>응시 코드 제공<span>학교 제공</span></div>
""",
"s07-tuition": f"""
  <div class="rcpt-clip" id="s7-rc"><div class="rcpt" id="s7-rcpt">
    <div class="rc-h">알렉산더 컬리지 · 한 학기</div><div class="rc-dash"></div>
    <div class="rc-row"><span>학점당</span><span>$660</span></div><div class="rc-row"><span>3과목 × 3학점</span><span>× 9</span></div>
    <div class="rc-big"><span class="odo odo-p" data-layout-allow-overflow data-layout-allow-overlap>{odo("$5,940", "p")}</span><span class="rc-cad">CAD</span></div></div></div>
  <div class="yr7" id="s7-yr">1년 3학기 기준 <b>약 $18,000</b></div>
  <div class="scale" id="s7-scale"><div class="beam" id="s7-beam"><i class="pan pl1" id="s7-pl"><span class="pan-t">아이 유학생 학비</span><span class="pan-v pv-s" id="s7-v1"><b>1,800만~</b><b>2,000만 원</b></span>
      <span class="pan-n">아이 1명 · 연 · 안팎</span><span class="kids2">{KID}<span class="k2" id="s7-k2">{KID}</span></span></i>
    <i class="pan pr1" id="s7-pr"><span class="pan-t">부모님이 공부하면</span><span class="pan-v gold">아이 0원</span></i></div><i class="post"></i></div>
  <div class="dep" id="s7-dep">입학 보증금 <s id="s7-old">$10,000<i id="s7-strike"></i></s><b id="s7-new">$6,000</b></div>
  <div class="fn" id="s7-fn">* CAD · 학교 안내 2026.10 · 아이 학비: VSB 2027-28 $17,000 + 보험 $1,400/년 · 1달러≈1,000원 · 변동 가능</div>
""",
"s08-pgwp": f"""
  <div class="tline" id="s8-tl"><i class="tl-line" id="s8-line"></i>
    <div class="tn n1" id="s8-n1"><b>준학사</b><span>한 학기 3과목씩</span></div>
    <div class="tn n2" id="s8-n2"><b>{CAP}</b><span>졸업</span></div>
    <div class="tn n3" id="s8-n3"><b>PGWP</b><span>최대 3년 <em>(대상 전공일 때)</em></span></div></div>
  <div class="tbl8" id="s8-tbl"><div class="t8-h">PGWP 대상 전공 <span>(학교 공지 기준)</span></div>
    <div class="t8-r ok" id="s8-ok"><i class="mk ok">{CHECK}</i><b>가능</b><div class="t8-c">{"".join(f'<span>{x}</span>' for x in ["AA 심리학", "AS (Science)", "AS 컴퓨터공학", "AS 수학"])}</div></div>
    <div class="t8-r no" id="s8-no"><i class="mk no">{XMARK}</i><b>대상 아님</b><div class="t8-c">{"".join(f'<span>{x}</span>' for x in ["AA 일반", "AA 경제", "AA 국제관계", "AA 수학", "AA 사회학", "AA 사회복지 준비"])}</div></div></div>
  <div class="note8" id="s8-note">* 전공에 따라 PGWP 대상 여부가 다릅니다 (학교 공지 기준)</div>
  <div class="fn" id="s8-fn">* Alexander College "PGWP Eligibility for Programs" · IRCC 요건(전공 분야·영어 점수) 충족 시 · 2026.10 기준, 변경 가능</div>
""",
"s09-check": f"""
  <div class="persp p9"><div class="clip9" id="s9-clip"><i class="clipt"></i><div class="cl-h">출국 전 꼭 확인할 3가지</div>
    <div class="cl-r" id="s9-r1"><i class="cbx">{CHECK}</i><div><b>PGWP 요건</b><span>2024.11 이후 학생비자 · 전공 분야 + 영어 점수</span></div></div>
    <div class="cl-r" id="s9-r2"><i class="cbx">{CHECK}</i><div><b>배우자 오픈워크퍼밋</b><span>2025.1부터 석사·박사 과정 등만 → 준학사는 대상 아님</span></div></div>
    <div class="cl-r" id="s9-r3"><i class="cbx">{CHECK}</i><div><b>거주 교육청 등록</b><span>교육청마다 서류가 조금씩 다름 → 미리 확인</span></div></div></div></div>
  <div class="stamp st-red" id="s9-stamp" data-layout-allow-overlap>AA CANADA · 출국 전 확인</div>
""",
"s10-compare": f"""
  <div class="cmp" id="s10-cmp">
    <div class="cc cc-l" id="s10-l"><div class="cc-h">공립 컬리지</div>
      <div class="cr">캐나다 학생 <b>많은 환경</b></div><div class="cr">학업 관리 <b>본인 주도</b></div><div class="cr">상황에 따라 <b>맞는 분도</b></div></div>
    <div class="cc cc-r" id="s10-r"><div class="cc-h">알렉산더 컬리지</div>
      <div class="cr" id="s10-r1"><i class="mk ok">{CHECK}</i>클래스 사이즈 <b>작음</b></div>
      <div class="cr" id="s10-r2"><i class="mk ok">{CHECK}</i><b>1:1 학업 플래닝</b></div>
      <div class="cr" id="s10-r3"><i class="mk ok">{CHECK}</i>캠퍼스 <b>한국인 담당자 상주</b></div><i class="sweep" id="s10-sw"></i></div></div>
  <div class="care" id="s10-care">{MOM}<span>자녀 동반 부모님께 <b>유리한 환경</b></span></div>
""",
"s11-cta": f"""
  <svg class="sky11" viewBox="0 0 1920 340" width="1920" height="340"><path class="ln" pathLength="1" d="{MOUNT}" fill="none" stroke="#4cc9f0" stroke-opacity="0.6" stroke-width="4"/>
    <path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#4cc9f0" stroke-width="5" stroke-linejoin="round"/></svg>
  <div class="leak" id="s11-leak"></div>
  <div class="cta-q" id="s11-q">공립·사립이 아니라 → <b>어떤 프로그램이냐</b></div>
  <div class="cta-logo" id="s11-logo">{kt("AA CANADA", "kt logo-kt")}</div>
  <div class="cta-sub" id="s11-sub">밴쿠버 자녀무상교육 · 알렉산더 컬리지 준학사</div>
  <div class="cta-cities" id="s11-cities">캐나다 자녀무상교육 · 유학 후 이민 · 영주권 &nbsp;|&nbsp; 밴쿠버 · 몬트리올 · 토론토 · 런던</div>
  <div class="cta-btns"><div class="cta-btn" id="s11-btn"><i class="btn-ring" id="s11-bring"></i>카카오톡 <b>canlog</b></div><div class="cta-btn tel" id="s11-tel">☎ <b>02-567-4345</b></div></div>
""",
}

# ---------------- layout schedule ----------------
def cap(i, j): return S[i]["captions"][j]["start"]
def st(i): return S[i]["start"]
def mk(k, d=-0.15): return M[k] + d


END = S[10]["speech_end"] + 0.35          # owner finishes → logo / contact end card
LAY = [
    (0.0, "A"), (cap(0, 2) - 0.12, "B"), (mk("h_gen"), "A"),
    (st(1), "B"), (mk("r_look"), "A"), (mk("r_1yr", -0.3), "B"), (mk("r_free"), "A"), (mk("r_dipx"), "B"), (mk("r_crit0"), "A"),
    (st(2), "B"), (mk("d_prog"), "A"), (mk("d_aa", -0.2), "B"),
    (st(3), "A"), (mk("l_then"), "B"), (mk("l_week"), "A"), (cap(3, 10) - 0.12, "B"), (mk("l_five"), "A"), (mk("l_par"), "B"),
    (st(4), "A"), (mk("o_oncls"), "B"),
    (st(5), "A"), (mk("e_110", -0.8), "B"), (mk("e_deg"), "A"), (mk("e_code", -0.3), "B"),
    (st(6), "A"), (cap(6, 1) - 0.12, "B"), (mk("t_par"), "A"), (mk("t_merit"), "B"),
    (st(7), "B"), (mk("p_major"), "A"), (mk("p_which"), "B"), (mk("p_1yr"), "A"),
    (st(8), "A"), (mk("c_eng", -0.5), "B"), (mk("c_3"), "A"),
    (st(9), "A"), (mk("v_sit"), "C"), (mk("v_care"), "A"),
    (st(10), "A"), (mk("z_std"), "B"), (cap(10, 5) - 0.12, "A"), (END, "E"),
]
# drop no-op events, check the 25 s rule
lay = []
for t, l in sorted(LAY, key=lambda x: x[0]):
    if not lay or lay[-1][1] != l:
        lay.append((round(t, 3), l))
for k, (t, l) in enumerate(lay):
    nxt = lay[k + 1][0] if k + 1 < len(lay) else TOTAL
    if nxt - t > 25 and l != "E":
        print(f"WARNING layout {l} at {t:.1f} holds {nxt - t:.1f}s")


def layout_at(t):
    cur = "A"
    for a, l in lay:
        if a <= t + 0.05: cur = l
    return cur


# ---------------- captions (box follows the layout so it never sits under the PiP) ----------------
HL = ["자녀무상교육", "사립", "공립", "교육청", "정확하게", "1년 이상", "디플로마", "학위", "Degree", "어떤 과정", "BC 주정부", "승인한", "몇 안 되는",
      "공부량", "9학점", "9시간", "14주", "여름방학", "5과목", "3과목씩만", "풀타임", "라이브", "실시간", "100% 동일하게", "집에서", "픽업",
      "110점", "90점", "조건부 입학", "English 099", "첫 학기부터", "듀오링고 코드", "IELTS", "660달러", "5,940달러", "18,000달러", "20,000달러",
      "2명, 3명", "메리트", "PGWP", "최대 3년", "전공", "3년의 취업비자", "1년 정도만", "영어 점수", "배우자 오픈워크퍼밋", "석사과정", "박사과정",
      "서류", "AA캐나다", "클래스 사이즈", "1:1 학업 플래닝", "한국인 담당자", "유리한 측면", "어떤 프로그램"]
cap_divs = []
for i, s in enumerate(S):
    for j, c in enumerate(s["captions"]):
        cls = {"B": "cap-b"}.get(layout_at(c["start"]), "")
        cap_divs.append(f'<div id="cap-{i}-{j}" class="clip cap {cls}" data-start="{r(c["start"])}" data-duration="{r(c["end"] - c["start"])}" data-track-index="2">'
                        f'<div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{hl_html(c["text"], HL)}</span></div></div>')

# ---------------- SFX: a step quieter than the voice-only cut, almost none while the face is full screen ----------------
TR = [S[i]["start"] - 0.3 for i in range(1, len(S))]
WH = ["whoosh", "swell", "whoosh-short", "glitch-1", "whoosh", "swell", "whoosh-short", "whoosh", "glitch-2", "swell"]
sfx = [(n, TR[k] - (0.9 if n == "swell" else 0.05), 0.16 if n == "swell" else 0.18) for k, n in enumerate(WH)]
sfx += [("pop", M["h_priv"] + 0.1, 0.16), ("pop", M["h_pub"] + 0.1, 0.16), ("pop", M["h_may"] + 0.1, 0.16), ("impact-bass-1", M["h_diff"] + 0.3, 0.2),
        ("click-soft", M["r_1yr"], 0.14), ("click-soft", M["r_pub"] + 0.2, 0.14), ("click-soft", M["r_priv"] + 0.2, 0.14), ("sparkle", M["r_privdeg"] + 0.5, 0.16),
        ("stamp", M["d_ok"] + 0.35, 0.2), ("pop", M["d_dt"] + 0.1, 0.16), ("pop", M["d_bby"] + 0.4, 0.16),
        ("click", M["l_three"], 0.16), ("click", M["l_three"] + 0.25, 0.16), ("click", M["l_three"] + 0.5, 0.16), ("ding", M["l_nine"] + 0.6, 0.18),
        ("impact-bass-2", M["l_hours"] + 0.3, 0.15), ("pop", M["l_steady"], 0.16),
        ("notification", M["o_oncls"] + 0.4, 0.12), ("ping", M["o_realt"] + 0.2, 0.15), ("ding", M["o_cred"] + 0.3, 0.16),
        ("pop", M["o_kid"], 0.15), ("pop", M["o_home"], 0.15), ("pop", M["o_pick"], 0.15),
        ("ping", M["e_110"] + 0.3, 0.15), ("ping", M["e_90"] + 0.3, 0.16), ("click", M["e_engl"], 0.16), ("click", M["e_major"], 0.16), ("ding", M["e_three"] + 0.5, 0.17),
        ("whoosh-short", M["e_code"] - 0.2, 0.15),
        ("ding", M["t_5940"] + 1.1, 0.2), ("impact-bass-1", M["t_fee"] + 0.3, 0.16), ("sparkle", M["t_per"] + 0.2, 0.15),
        ("whoosh", M["p_assoc"], 0.14), ("sparkle", M["p_pgwp"] + 0.2, 0.14), ("pop", M["p_which"] + 0.3, 0.15), ("pop", M["p_list"], 0.15),
        ("click-soft", M["c_1"] + 0.3, 0.12), ("typing", M["c_2"], 0.1), ("pop", M["c_2"] + 1.0, 0.14), ("click-soft", M["c_3"] + 0.3, 0.12), ("stamp", M["c_aa"] + 0.3, 0.16),
        ("pop", M["v_small"] + 0.1, 0.15), ("pop", M["v_11"] + 0.1, 0.15), ("pop", M["v_kor"] + 0.1, 0.15),
        ("riser-short", END - 1.2, 0.14), ("impact-bass-2", END + 0.5, 0.2), ("sparkle", END + 1.6, 0.16), ("chime", END + 2.2, 0.16)]
# full-screen face: keep only transitions and soft clicks
sfx = [x for x in sfx if layout_at(x[1]) != "A" or x[0] in ("whoosh", "swell", "whoosh-short", "glitch-1", "glitch-2", "click-soft", "stamp")]

# scenes are plain timed clips; the incoming one starts 0.3 s early and whips/zooms in over the outgoing one (GSAP, seek-safe)
def scene_div(i, s):
    a = 0.0 if i == 0 else s["start"] - 0.3
    b = S[i + 1]["start"] + 0.1 if i + 1 < len(S) else TOTAL
    return (f'<section id="{s["id"]}" class="scene clip" data-start="{r(a)}" data-duration="{r(b - a)}" data-track-index="1" style="width:{W}px;height:{H}px">'
            f'<div class="sx" id="{s["id"]}-sx">{bg(i + 1, W, H, MESH, DOTS, n_dots=3)}'
            f'<div class="lay" id="{s["id"]}-lay"><div class="cam" id="{s["id"]}-cam">{SCENES[s["id"]]}</div></div>{chip(i)}</div></section>')


scene_divs = [scene_div(i, s) for i, s in enumerate(S)]

FACE = (f'<div id="face" data-layout-allow-overlap><div id="face-in"><video id="face-v" class="clip" src="assets/facecam/face_l.mp4" muted '
        f'data-start="0" data-duration="{r(T["segments"][-1]["at"] + (T["segments"][-1]["src"][1] - T["segments"][-1]["src"][0]) + 0.4)}" data-track-index="4"></video></div></div>')
OVER = """
      <div id="ov" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="7" data-layout-allow-overlap>
        <div class="ov-open" id="ov-open"><div class="op-k">VANCOUVER</div><div class="op-t">""" + kt("밴쿠버 ") + "<b>" + kt("자녀무상교육") + """</b></div><div class="op-s">알렉산더 컬리지 준학사로 시작하는 방법</div></div>
        <div class="ovc" id="ov-c1"><i class="cbx">""" + CHECK + """</i><div><b>① PGWP 요건</b><span>2024.11 이후 학생비자 · 전공 분야 + 영어 점수</span></div></div>
        <div class="ovc" id="ov-c2"><i class="cbx">""" + CHECK + """</i><div><b>② 배우자 오픈워크퍼밋</b><span>2025.1부터 석사·박사 등만 → 준학사 X</span></div></div>
        <div class="ovc" id="ov-c3"><i class="cbx">""" + CHECK + """</i><div><b>③ 거주 교육청 등록</b><span>교육청마다 서류가 조금씩 다름</span></div></div>
        <div class="stamp st-red ov-stamp" id="ov-stamp" data-layout-allow-overlap>AA CANADA · 출국 전 확인</div>
        <div class="ov-pill" id="ov-1yr">1년만 공부하고 <b>귀국도 OK</b></div>
        <div class="ov-pill" id="ov-q">"공립 컬리지가 <b>낫지 않나요?</b>"</div>
        <div id="facechip"><b>AA</b> CANADA</div>
      </div>"""


def page(out, layer):
    s = (ROOT / "tools" / "template-facecam.html").read_text()
    graphics = layer == "graphics"
    # graphics layer: the shorts only use S01–S07
    parts = dict(TOTAL=r(S[7]["start"]) if graphics else r(TOTAL), SCENES="\n      ".join(scene_divs), FACE="" if graphics else FACE, OVERLAYS="" if graphics else OVER,
                 CAPTIONS="" if graphics else "\n      ".join(cap_divs), SFX="" if graphics else "\n      ".join(sfx_tags(ROOT, sfx, TOTAL)),
                 TIMING=json.dumps(T, ensure_ascii=False), LAYOUT=json.dumps(lay), LAYER=json.dumps(layer), END=r(END),
                 AUDIO="" if graphics else ('<audio id="narration" class="clip" src="assets/audio/narration-facecam.wav" data-start="0" data-duration="__TOTAL__" data-track-index="9" data-volume="1"></audio>\n'
                                             '      <audio id="music-bed" class="clip" src="assets/bgm/bed-facecam.wav" data-start="0" data-duration="__TOTAL__" data-track-index="10" data-volume="0.22"></audio>'),
                 BRAND="" if graphics else '<div id="brand" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="6"><span id="brand-in"><b>AA</b> CANADA · 밴쿠버 자녀무상교육</span></div>',
                 ROOTCLS="layer-graphics" if graphics else "layer-full")
    for k in ["SCENES", "FACE", "OVERLAYS", "CAPTIONS", "SFX", "AUDIO", "BRAND", "TIMING", "LAYOUT", "LAYER", "END", "ROOTCLS", "TOTAL"]:
        s = s.replace(f"__{k}__", parts[k])
    (ROOT / out).write_text(s)


install(ROOT)
page("facecam.html", "full")
page("graphics.html", "graphics")
print("facecam.html + graphics.html written; total", TOTAL, "end card at", round(END, 2))
for t, l in lay: print(f"  {t:7.2f} {l}")
