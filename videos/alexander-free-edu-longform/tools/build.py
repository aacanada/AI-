"""Build index.html (1920x1080 YouTube longform) from timing.json. Captions in the bottom band.
Pipeline: python3 tools/from_recording.py → bash ../_kit/make.sh → render."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from pyk import kt, odo, bg, captions, sfx_tags, install, page, r, esc

T = json.loads((ROOT / "timing.json").read_text())
M, S, TOTAL = T["marks"], T["scenes"], T["total"]
W, H = 1920, 1080
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
  <div class="fn" id="s2-fn" style="left:0;right:0;top:846px">* BC Ministry of Education · Eligibility of Students for Operating Grant Funding · 거주 교육청별 서류·절차 상이</div>
""",
"s03-degree": f"""
  <svg class="sky3" viewBox="0 0 1920 340" width="1920" height="340"><path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#4cc9f0" stroke-width="5" stroke-linejoin="round"/></svg>
  <div class="pin pin-dt" id="s3-dt">{PIN}<span>다운타운 캠퍼스</span></div>
  <div class="pin pin-bb" id="s3-bb">{PIN}<span>버나비 캠퍼스</span></div>
  <div class="persp p3"><div class="deg" id="s3-deg"><div class="dg-t">ASSOCIATE DEGREE</div><div class="dg-k">알렉산더 컬리지 준학사</div>
    <div class="dg-s">Associate of Arts · Associate of Science</div><i class="sweep" id="s3-sw"></i></div></div>
  <div class="stamp st-mint" id="s3-stamp" data-layout-allow-overlap>DEGREE ✓</div>
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
    <div class="hrs" id="s4-hrs">주 <b>4~6시간</b>대부터</div><div class="summer" id="s4-sum">여름 학기 <b>OFF</b> 가능</div></div>
  <div class="bars" id="s4-bars">
    <div class="bar-r" id="s4-br1"><span>편입 준비생</span><div class="bb">{"".join('<i class="bk5"></i>' for _ in range(5))}</div><em>5과목</em></div>
    <div class="bar-r me" id="s4-br2"><span>자녀무상교육 부모님</span><div class="bb">{"".join('<i class="bk5"></i>' for _ in range(3))}</div><em>3과목씩 꾸준히</em></div></div>
""",
"s05-online": f"""
  <div class="lap" id="s5-lap"><div class="lap-s"><div class="lv"><i class="rec" id="s5-rec"></i>LIVE</div><div class="lv-t">ENGL 099 · 실시간 강의</div>
    <div class="tiles">{"".join('<i class="tile"></i>' for _ in range(6))}</div></div><div class="lap-b"></div></div>
  <div class="vs" id="s5-vs"><div class="vs-r x" id="s5-x"><i class="mk no">{XMARK}</i>녹화 강의</div><div class="vs-r o" id="s5-o"><i class="mk ok">{CHECK}</i>실시간 수업</div>
    <div class="vs-c" id="s5-c">학점 <b>똑같이 인정</b></div></div>
  <div class="day" id="s5-day"><i class="day-l" id="s5-line"></i>
    <div class="dn" id="s5-n1"><b>8:00</b>{KID}<span>아이 등교</span></div>
    <div class="dn dn-me" id="s5-n2"><b>10:00</b>{MOM}<span>집에서 라이브 수업</span></div>
    <div class="dn" id="s5-n3"><b>15:00</b>{KID}<span>픽업</span></div></div>
  <div class="fn" id="s5-fn" style="left:0;right:0;top:846px">* 온라인으로 개설된 과목에 한함 · 학생비자 규정에 맞춰 온·오프라인 비율 설계</div>
""",
"s06-english": f"""
  <div class="gg" id="s6-gg"><div class="gg-l">듀오링고 점수</div>
    <div class="gg-bar"><i id="s6-fill"></i><span class="tick" style="left:{90 / 160 * 100:.2f}%"></span><span class="tick" style="left:{110 / 160 * 100:.2f}%"></span></div>
    <div class="flag f90" id="s6-f90" style="left:{90 / 160 * 100:.2f}%"><b>90</b>조건부 입학</div>
    <div class="flag f110" id="s6-f110" style="left:{110 / 160 * 100:.2f}%"><b>110</b>본과 바로 입학</div></div>
  <div class="sem" id="s6-sem"><div class="sem-l">첫 학기</div><i class="sb sb-e" id="s6-e">ENGL 099</i><i class="pl">+</i><i class="sb" id="s6-m1">전공</i><i class="pl">+</i><i class="sb" id="s6-m2">전공</i>
    <i class="pl">=</i><i class="sb sb-t" id="s6-t">3과목 풀타임</i></div>
  <div class="vs2" id="s6-vs"><div class="vs-r x" id="s6-x"><i class="mk no">{XMARK}</i>어학연수</div><div class="vs-r o" id="s6-o"><i class="mk ok">{CHECK}</i>첫 학기부터 학위 과정 학생</div></div>
  <div class="ticket" id="s6-tk"><b>DUOLINGO</b>응시 코드 제공<span>1인 1회 · 학교 제공</span></div>
""",
"s07-tuition": f"""
  <div class="rcpt-clip" id="s7-rc"><div class="rcpt" id="s7-rcpt">
    <div class="rc-h">알렉산더 컬리지 · 한 학기</div><div class="rc-dash"></div>
    <div class="rc-row"><span>학점당</span><span>$660</span></div><div class="rc-row"><span>3과목 × 3학점</span><span>× 9</span></div>
    <div class="rc-big"><span class="odo odo-p" data-layout-allow-overflow data-layout-allow-overlap>{odo("$5,940", "p")}</span><span class="rc-cad">CAD</span></div></div></div>
  <div class="scale" id="s7-scale"><div class="beam" id="s7-beam"><i class="pan pl1" id="s7-pl"><span class="pan-t">아이 유학생 학비</span><span class="pan-v" id="s7-v1">1,700만 원</span>
      <span class="kids2">{KID}<span class="k2" id="s7-k2">{KID}</span></span></i>
    <i class="pan pr1" id="s7-pr"><span class="pan-t">부모님이 공부하면</span><span class="pan-v gold">아이 0원</span></i></div><i class="post"></i></div>
  <div class="dep" id="s7-dep">입학 보증금 <s id="s7-old">$10,000<i id="s7-strike"></i></s><b id="s7-new">$6,000</b></div>
  <div class="fn" id="s7-fn" style="left:0;right:0;top:846px">* CAD · 2026.10 학교 안내 · 교재·의료보험 등 별도 · 아이 유학생 학비는 교육청별 대략치 · 환율·정책 변동 가능</div>
""",
"s08-pgwp": f"""
  <div class="tline" id="s8-tl"><i class="tl-line" id="s8-line"></i>
    <div class="tn n1" id="s8-n1"><b>준학사</b><span>한 학기 3과목씩</span></div>
    <div class="tn n2" id="s8-n2"><b>{CAP}</b><span>졸업</span></div>
    <div class="tn n3" id="s8-n3"><b>PGWP</b><span>졸업 후 취업비자 최대 3년</span></div></div>
  <div class="walk" id="s8-walk"><div class="kidw" id="s8-kid">{KID}</div>{"".join(f'<i class="gr" style="left:{140 + k * 260}px">G{g}</i>' for k, g in enumerate([3, 4, 5, 6, 7, 8]))}<span class="walk-l">아이의 캐나다 학교생활</span></div>
  <div class="br1" id="s8-br">1년만 공부하고 <b>귀국도 OK</b></div>
  <div class="fn" id="s8-fn" style="left:0;right:0;top:846px">* PGWP는 IRCC 요건 충족 시 · 취업비자 기간의 자녀 학비는 부모 워크퍼밋 기준으로 교육청 재확인</div>
""",
"s09-check": f"""
  <div class="persp p9"><div class="clip9" id="s9-clip"><i class="clipt"></i><div class="cl-h">출국 전 꼭 확인할 3가지</div>
    <div class="cl-r" id="s9-r1"><i class="cbx">{CHECK}</i><div><b>PGWP 요건</b><span>2024.11 이후 학생비자 · 전공 분야 + 영어 점수</span></div></div>
    <div class="cl-r" id="s9-r2"><i class="cbx">{CHECK}</i><div><b>배우자 오픈워크퍼밋</b><span>현재 규정상 준학사 과정은 대상 아님</span></div></div>
    <div class="cl-r" id="s9-r3"><i class="cbx">{CHECK}</i><div><b>거주 교육청 등록</b><span>서류·절차를 미리 확인</span></div></div></div></div>
  <div class="stamp st-red" id="s9-stamp" data-layout-allow-overlap>AA CANADA · 출국 전 확인</div>
""",
"s10-compare": f"""
  <div class="cmp" id="s10-cmp">
    <div class="cc cc-l" id="s10-l"><div class="cc-h">공립 컬리지</div>
      <div class="cr">과목에 따라 <b>대형 강의</b></div><div class="cr">학업 관리 <b>본인 주도</b></div><div class="cr">상담 <b>영어</b></div></div>
    <div class="cc cc-r" id="s10-r"><div class="cc-h">알렉산더 컬리지</div>
      <div class="cr" id="s10-r1"><i class="mk ok">{CHECK}</i>일반 수업 <b>35명 이하</b> · 랩 22명</div>
      <div class="cr" id="s10-r2"><i class="mk ok">{CHECK}</i><b>1:1 학업 플래닝</b></div>
      <div class="cr" id="s10-r3"><i class="mk ok">{CHECK}</i>캠퍼스 <b>한국인 담당자 상주</b></div><i class="sweep" id="s10-sw"></i></div></div>
  <div class="care" id="s10-care">{MOM}<span>아이 케어가 우선인 부모님께 <b>맞는 환경</b></span></div>
""",
"s11-cta": f"""
  <svg class="sky11" viewBox="0 0 1920 340" width="1920" height="340"><path class="ln" pathLength="1" d="{MOUNT}" fill="none" stroke="#4cc9f0" stroke-opacity="0.6" stroke-width="4"/>
    <path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#4cc9f0" stroke-width="5" stroke-linejoin="round"/></svg>
  <div class="leak" id="s11-leak"></div>
  <div class="cta-q" id="s11-q">"사립이라서 안 된다" → <b>기준으로 확인하세요</b></div>
  <div class="cta-logo" id="s11-logo">{kt("AA CANADA", "kt logo-kt")}</div>
  <div class="cta-sub" id="s11-sub">밴쿠버 자녀무상교육 · 알렉산더 컬리지 준학사</div>
  <div class="cta-cities" id="s11-cities">캐나다 자녀무상교육 · 유학 후 이민 · 영주권 &nbsp;|&nbsp; 밴쿠버 · 몬트리올 · 토론토 · 런던</div>
  <div class="cta-btns"><div class="cta-btn" id="s11-btn"><i class="btn-ring" id="s11-bring"></i>카카오톡 <b>canlog</b></div><div class="cta-btn tel" id="s11-tel">☎ <b>02-567-4345</b></div></div>
""",
}

scene_divs = [f'<section id="{s["id"]}" class="scene" style="width:{W}px;height:{H}px;background-color:#0a1a33">{bg(i + 1, W, H, MESH, DOTS, n_dots=3)}'
              f'<div class="cam" id="{s["id"]}-cam">{SCENES[s["id"]]}</div>{chip(i)}</section>' for i, s in enumerate(S)]
HL = ["밴쿠버 자녀무상교육", "사립 컬리지", "완전히 달라집니다", "1년 이상", "학위", "디플로마", "사립학교라도", "자녀무상교육 대상", "어떤 과정", "준학사", "승인한",
      "몇 안 되는", "공부량", "세 과목", "9학점", "풀타임", "14주", "4~6시간", "쉬셔도", "꾸준히", "라이브 온라인", "실시간", "똑같이", "픽업", "110점", "90점", "조건부 입학",
      "잉글리시 099", "첫 학기", "응시 코드", "660", "5,940", "1,700만 원", "0원", "6천 달러", "PGWP", "최대 3년", "1년만", "첫째", "둘째", "셋째", "전공 분야",
      "오픈워크퍼밋", "교육청", "AA캐나다", "소규모 수업", "1대1", "한국인 담당자", "맞는 환경", "기준으로", "canlog", "02-567-4345"]
cap_divs = captions(T, HL)


def C(i, j): return S[i]["captions"][j]["start"]
def E(i, j): return S[i]["captions"][j]["speech_end"]
TR = [S[i]["start"] - 0.3 for i in range(1, len(S))]
WH = ["whoosh", "swell", "whoosh-short", "glitch-1", "whoosh", "swell", "whoosh-short", "whoosh", "glitch-2", "swell"]
sfx = [(n, TR[k] - (0.9 if n == "swell" else 0.05), 0.24 if n == "swell" else 0.28) for k, n in enumerate(WH)]
sfx += [("pop", M["h_priv"] + 0.1, 0.24), ("pop", M["h_may"] + 0.2, 0.24), ("pop", M["h_pub"], 0.24), ("glitch-2", M["h_but"] + 0.3, 0.2), ("impact-bass-1", M["h_diff"] + 0.3, 0.3),
        ("swell", M["r_doc"] - 0.9, 0.2), ("click-soft", M["r_1yr"], 0.2), ("click-soft", M["r_pub"] + 0.2, 0.2), ("click-soft", M["r_priv"] + 0.2, 0.2),
        ("ping", M["r_pub"] + 0.9, 0.2), ("ping", M["r_pub"] + 1.3, 0.2), ("error", M["r_dipx"] + 0.4, 0.14), ("sparkle", M["r_privdeg"] + 0.5, 0.22), ("impact-bass-2", M["r_privdeg"] + 0.5, 0.24),
        ("stamp", M["r_crit"] + 0.25, 0.3),
        ("swell", M["d_ac"] - 0.6, 0.2), ("stamp", M["d_ok"] + 0.35, 0.32), ("pop", M["d_dt"] + 0.1, 0.24), ("pop", M["d_bby"] + 0.1, 0.24), ("chime", M["d_few"] + 0.2, 0.2)]
sfx += [("click", M["l_three"] + k * 0.25, 0.24) for k in range(3)]
sfx += [("ding", M["l_nine"] + 0.6, 0.28), ("pop", M["l_14"], 0.22), ("typing", M["l_hours"] - 2.2, 0.12), ("impact-bass-2", M["l_hours"] + 0.3, 0.22), ("pop", M["l_summer"] + 0.1, 0.22),
        ("whoosh-short", M["l_five"] - 0.2, 0.22), ("pop", M["l_steady"], 0.24),
        ("notification", M["o_live"] + 0.2, 0.16), ("error", M["o_rec"] + 0.2, 0.12), ("ping", M["o_realt"] + 0.2, 0.22), ("ding", M["o_cred"] + 0.3, 0.24),
        ("pop", M["o_kid"], 0.22), ("pop", M["o_home"], 0.22), ("pop", M["o_pick"], 0.22),
        ("riser-short", M["e_110"] - 1.7, 0.14), ("ping", M["e_110"] + 0.3, 0.22), ("ping", M["e_90"] + 0.3, 0.24), ("click", M["e_engl"], 0.24), ("click", M["e_major"], 0.24), ("click", M["e_major"] + 0.3, 0.24),
        ("ding", M["e_three"] + 0.5, 0.26), ("error", M["e_notesl"] + 0.2, 0.12), ("ping", M["e_deg"] + 0.1, 0.22), ("whoosh-short", M["e_code"] - 0.2, 0.22),
        ("click-soft", C(6, 0), 0.2), ("ding", M["t_5940"] + 1.1, 0.3), ("swell", M["t_kid"] - 0.6, 0.18), ("impact-bass-1", M["t_1700"] + 0.3, 0.24), ("sparkle", M["t_zero"] + 0.2, 0.22),
        ("pop", M["t_two"] + 0.2, 0.24), ("whoosh-short", M["t_6000"] - 0.6, 0.2), ("impact-bass-2", M["t_6000"] + 0.2, 0.22),
        ("whoosh", M["p_assoc"], 0.2), ("sparkle", M["p_pgwp"] + 0.2, 0.2), ("impact-bass-1", M["p_3yr"] + 0.3, 0.24), ("pop", M["p_kid"], 0.2), ("pop", M["p_1yr"] + 0.2, 0.22),
        ("swell", C(8, 0) - 0.6, 0.18), ("typing", M["c_1"], 0.14), ("pop", M["c_1"] + 1.0, 0.22), ("typing", M["c_2"], 0.14), ("pop", M["c_2"] + 1.0, 0.22),
        ("typing", M["c_3"], 0.14), ("pop", M["c_3"] + 1.0, 0.22), ("stamp", M["c_aa"] + 0.3, 0.32),
        ("whoosh-short", M["v_q"], 0.2), ("pop", M["v_small"] + 0.1, 0.22), ("pop", M["v_11"] + 0.1, 0.22), ("pop", M["v_kor"] + 0.1, 0.22), ("chime", M["v_care"] + 0.3, 0.18),
        ("riser-short", M["z_ac"] - 1.6, 0.16), ("impact-bass-2", M["z_ac"] + 0.4, 0.24), ("sparkle", M["z_kakao"], 0.22), ("chime", M["z_tel"] + 0.3, 0.2)]

install(ROOT)
page(ROOT, "template.html", TOTAL=r(TOTAL), SCENES="\n      ".join(scene_divs), CAPTIONS="\n      ".join(cap_divs),
     SFX="\n      ".join(sfx_tags(ROOT, sfx, TOTAL)), TIMING=T)
print("index.html written; total", TOTAL)
