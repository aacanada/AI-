"""Build index.html (1080x1920 Shorts) from timing.json. Captions in the TOP band (Shorts UI covers the bottom).
Pipeline: python3 tools/from_recording.py → bash ../_kit/make.sh → render."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from pyk import kt, odo, bg, captions, sfx_tags, install, page, r

T = json.loads((ROOT / "timing.json").read_text())
M, S, TOTAL = T["marks"], T["scenes"], T["total"]
W, H = 1080, 1920
MESH = ("radial-gradient(760px 760px at 72% 22%, rgba(40,90,170,0.85) 0%, rgba(40,90,170,0) 70%),"
        "radial-gradient(640px 640px at 18% 62%, rgba(76,201,240,0.22) 0%, rgba(76,201,240,0) 70%),"
        "radial-gradient(760px 760px at 82% 86%, rgba(46,196,166,0.22) 0%, rgba(46,196,166,0) 70%),"
        "linear-gradient(180deg, #0a1a33 0%, #12305c 100%)")
DOTS = ["255,200,61", "76,201,240", "46,196,166", "255,255,255"]
CHECK = '<svg viewBox="0 0 100 100" class="ck"><path d="M22 54 L42 73 L80 30" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
XMARK = '<svg viewBox="0 0 100 100" class="ck"><path d="M28 28 L72 72 M72 28 L28 72" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" pathLength="1"/></svg>'
MOM = ('<svg viewBox="0 0 120 140" class="mom"><circle cx="60" cy="42" r="26" fill="#ffd9b0"/>'
       '<path d="M30 46 C26 8 94 8 90 46 C90 30 80 22 60 22 C40 22 30 30 30 46 Z" fill="#4a2b1d"/><path d="M28 44 C26 70 36 76 40 74 L36 46 Z M92 44 C94 70 84 76 80 74 L84 46 Z" fill="#4a2b1d"/>'
       '<path d="M14 138 C14 94 34 80 60 80 C86 80 106 94 106 138 Z" fill="#2ec4a6"/></svg>')
KID = ('<svg viewBox="0 0 120 140" class="kid"><circle cx="60" cy="50" r="24" fill="#ffd9b0"/><path d="M36 46 C36 20 84 20 84 46 C76 36 44 36 36 46 Z" fill="#2b2b45"/>'
       '<path d="M22 138 C22 98 38 86 60 86 C82 86 98 98 98 138 Z" fill="#ffc83d"/><rect x="74" y="92" width="26" height="36" rx="6" fill="#d7263d"/></svg>')
SKY = ("M0 300 V230 H70 V190 H120 V240 H170 V150 H210 V110 H250 V150 H280 V220 H320 V170 H360 V70 H400 V30 H440 V70 H480 V170 H520 V130 "
       "H580 V210 H620 V160 H680 V100 H720 V160 H760 V230 H810 V180 H860 V250 H920 V200 H970 V240 H1080 V300")
MOUNT = "M0 120 L120 40 L210 100 L320 20 L430 90 L520 50 L640 110 L760 30 L880 90 L980 50 L1080 100"

SCENES = {
"s1-hook": f"""
  <div class="tagwrap" id="s1-tag" data-layout-allow-overlap><div class="tag"><i class="hole"></i>
    <div class="tag-l">밴쿠버 공립학교 · 아이 유학생 학비</div>
    <div class="tag-p"><span class="tag-big">1,700만 원</span><span class="tag-u">/ 1년 (아이 1명)</span></div>
    <i class="sweep" id="s1-sw"></i><i class="slash" id="s1-slash"></i></div></div>
  <div class="zero" id="s1-zero" data-layout-allow-overlap><span class="zero-n">0원</span><span class="zero-u">아이 공립학교 학비</span></div>
  <div class="momrow" id="s1-mom">{MOM}<div class="mr-b">{"".join(f'<i class="mb">{k}</i>' for k in ["과목 1", "과목 2", "과목 3"])}</div><div class="mr-l">엄마는 한 학기 3과목</div></div>
  <div class="doubt" id="s1-doubt">사립 컬리지도?</div>
  <i class="ring" id="s1-ring" style="left:540px;top:820px"></i>
  <div class="fn" id="s1-fn" style="left:60px;right:60px;top:1410px">* 유학생 학비는 교육청별로 다르며 대략치 · 부모 학생비자 1년 이상 + 학위 과정 기준</div>
""",
"s2-rule": f"""
  <div class="bub b1" id="s2-b1">사립은 안 된대요</div>
  <div class="bub b2" id="s2-b2">교육청마다 달라요</div>
  <div class="bub b3" id="s2-b3">공립만 가세요</div>
  <div class="mx" id="s2-mx">
    <div class="mx-h"></div><div class="mx-h">학위 과정</div><div class="mx-h">디플로마</div>
    <div class="mx-r">공립</div><div class="mx-c" id="s2-c1"><i class="mk ok">{CHECK}</i></div><div class="mx-c" id="s2-c2"><i class="mk ok">{CHECK}</i></div>
    <div class="mx-r">사립</div><div class="mx-c mx-g" id="s2-c4"><i class="mk ok">{CHECK}</i><span>준학사 OK</span></div><div class="mx-c" id="s2-c3"><i class="mk no">{XMARK}</i></div>
  </div>
  <div class="mx-t" id="s2-mxt">BC주 기준: <b>어떤 과정이냐</b></div>
  <div class="stamp st-mint" id="s2-stamp" data-layout-allow-overlap>자녀무상교육 대상</div>
  <div class="fn" id="s2-fn" style="left:60px;right:60px;top:1410px">* BC주 교육부 공립학교 재정지원 자격 기준 · 부모 학생비자 1년 이상 · 거주 교육청 서류 확인</div>
""",
"s3-ac": f"""
  <div class="persp p3"><div class="deg" id="s3-deg"><div class="dg-t">ASSOCIATE DEGREE</div><div class="dg-k">알렉산더 컬리지 준학사</div>
    <div class="dg-s">Associate of Arts · Associate of Science</div><div class="dg-chip" id="s3-chip">BC주 승인 학위 과정</div><i class="sweep" id="s3-sw"></i></div></div>
  <div class="ftbar" id="s3-ft"><div class="ft-slots">{"".join(f'<div class="ft-s"><i class="blk" id="s3-k{k}">3학점</i></div>' for k in range(3))}</div>
    <div class="ft-l"><span class="odo odo-c" data-layout-allow-overflow data-layout-allow-overlap>{odo("9", "c")}</span>학점 = <b>FULL-TIME</b></div></div>
  <div class="lap" id="s3-lap"><div class="lap-s"><div class="lv"><i class="rec"></i>LIVE</div>
    <div class="tiles">{"".join('<i class="tile"></i>' for _ in range(6))}</div></div><div class="lap-b"></div></div>
""",
"s4-eng": f"""
  <div class="gg" id="s4-gg"><div class="gg-l">듀오링고 점수</div>
    <div class="gg-bar"><i id="s4-fill"></i><span class="tick" style="left:{90 / 160 * 100:.2f}%"></span><span class="tick" style="left:{110 / 160 * 100:.2f}%"></span></div>
    <div class="flag f90" id="s4-f90" style="left:{90 / 160 * 100:.2f}%"><b>90</b>조건부 입학</div>
    <div class="flag f110" id="s4-f110" style="left:{110 / 160 * 100:.2f}%"><b>110</b>본과 입학</div>
    <div class="gg-k" id="s4-k"><i>ENGL 099</i>+<i>전공</i>+<i>전공</i>= 3과목 풀타임</div></div>
  <div class="rcpt-clip" id="s4-rc"><div class="rcpt" id="s4-rcpt">
    <div class="rc-h">알렉산더 컬리지 · 한 학기</div><div class="rc-dash"></div>
    <div class="rc-row"><span>학점당</span><span>$660</span></div><div class="rc-row"><span>3과목 × 3학점</span><span>9학점</span></div>
    <div class="rc-big"><span class="odo odo-p" data-layout-allow-overflow data-layout-allow-overlap>{odo("$5,940", "p")}</span><span class="rc-cad">CAD</span></div></div></div>
  <div class="fn" id="s4-fn" style="left:60px;right:60px;top:1410px">* 2026.10 학교 안내 · 교재·보험 등 별도 · 환율·정책 변동 가능</div>
""",
"s5-pgwp": f"""
  <div class="tline" id="s5-tl"><i class="tl-line" id="s5-line"></i>
    <div class="tn n1" id="s5-n1"><b>준학사</b><span>한 학기 3과목씩</span></div>
    <div class="tn n2" id="s5-n2"><b>졸업</b><span>Associate Degree</span></div>
    <div class="tn n3" id="s5-n3"><b>PGWP</b><span>최대 3년</span></div></div>
  <div class="kids" id="s5-kids">{KID}<span>아이는 그동안 공립학교</span></div>
  <div class="chk" id="s5-chk"><div class="chk-h">출국 전 꼭 확인</div>
    <div class="chk-r" id="s5-r1"><i class="cb">{CHECK}</i>거주 교육청 등록 서류</div>
    <div class="chk-r" id="s5-r2"><i class="cb">{CHECK}</i>PGWP 전공·영어 요건</div></div>
  <div class="fn" id="s5-fn" style="left:60px;right:60px;top:1410px">* 2024.11 이후 학생비자는 PGWP 전공 분야·영어 요건 적용 · 2026.10 기준</div>
""",
"s6-cta": f"""
  <svg class="skyl" viewBox="0 0 1080 300" width="1080" height="300"><path class="ln" pathLength="1" d="{MOUNT}" fill="none" stroke="#4cc9f0" stroke-opacity="0.6" stroke-width="4"/>
    <path class="ln" pathLength="1" d="{SKY}" fill="none" stroke="#4cc9f0" stroke-width="5" stroke-linejoin="round"/></svg>
  <div class="leak" id="s6-leak"></div>
  <div class="cta-logo" id="s6-logo">{kt("AA CANADA", "kt logo-kt")}</div>
  <div class="cta-sub" id="s6-sub">밴쿠버 자녀무상교육 · 알렉산더 컬리지 준학사</div>
  <div class="cta-cities" id="s6-cities">캐나다 자녀무상교육 · 유학 후 이민 · 영주권</div>
  <div class="cta-btn" id="s6-btn"><i class="btn-ring" id="s6-bring"></i>무료 상담 · 카톡 <b>canlog</b></div>
""",
}

scene_divs = [f'<section id="{s["id"]}" class="scene" style="width:{W}px;height:{H}px;background-color:#0a1a33">{bg(i + 1, W, H, MESH, DOTS)}'
              f'<div class="cam" id="{s["id"]}-cam">{SCENES[s["id"]]}</div></section>' for i, s in enumerate(S)]
HL = ["세 과목", "0원", "사립 컬리지", "안 된다고요?", "학위 과정", "사립이라도", "대상입니다", "준학사", "3과목", "풀타임", "라이브 온라인",
      "듀오링고 90점", "조건부 입학", "5,940", "PGWP 최대 3년", "교육청 서류", "자녀무상교육", "AA캐나다"]
cap_divs = captions(T, HL)

def C(i, j): return S[i]["captions"][j]["start"]
def E(i, j): return S[i]["captions"][j]["speech_end"]
TR = [S[i]["start"] - 0.25 for i in range(1, len(S))]
sfx = [("whoosh", TR[0] - 0.05, 0.3), ("swell", TR[1] - 0.9, 0.22), ("whoosh", TR[2] - 0.05, 0.3), ("glitch-1", TR[3], 0.2), ("whoosh-short", TR[4], 0.3),
       ("click-soft", 0.3, 0.22)]
sfx += [("pop", M["three0"] - 0.1 + k * 0.12, 0.2) for k in range(3)]
sfx += [("whoosh-short", E(0, 0) - 0.15, 0.25), ("impact-bass-1", M["zero"] + 0.25, 0.34), ("sparkle", M["zero"] + 0.28, 0.18),
        ("pop", M["priv"], 0.26), ("pop", S[1]["start"] + 0.15, 0.24), ("pop", M["no"] - 0.25, 0.24), ("pop", M["no"] + 0.15, 0.24), ("glitch-2", M["no"] + 0.75, 0.2),
        ("ping", M["deg"] + 0.1, 0.2), ("ping", M["deg"] + 0.35, 0.2), ("error", M["privdeg"] - 0.3, 0.14), ("sparkle", M["privdeg"] + 0.45, 0.22), ("impact-bass-2", M["privdeg"] + 0.45, 0.24),
        ("stamp", M["free"] + 0.25, 0.36),
        ("swell", M["ac"] - 0.9, 0.2), ("chime", M["assoc"] + 0.2, 0.2)]
sfx += [("click", M["three"] - 0.1 + k * 0.22, 0.24) for k in range(3)]
sfx += [("ding", M["ft"] + 0.2, 0.3), ("typing", M["live"], 0.16), ("notification", M["live"] + 0.6, 0.14),
        ("riser-short", M["cond"] - 2.0 + 0.3, 0.16), ("ping", M["duo"] + 0.9, 0.22), ("ping", M["cond"] + 0.1, 0.24), ("pop", M["cond"] + 0.9, 0.2),
        ("click-soft", M["fee"] - 0.1, 0.22), ("ding", M["price"] + 1.05, 0.3), ("impact-bass-2", M["price"] + 1.0, 0.2),
        ("whoosh", M["grad"] - 0.05, 0.22), ("sparkle", M["grad"] + 1.0, 0.2), ("impact-bass-1", M["pgwp"] + 0.3, 0.26),
        ("pop", M["check"] - 0.1, 0.22), ("pop", M["check"] + 0.5, 0.22), ("stamp", M["sure"] + 0.3, 0.3),
        ("riser-short", C(5, 0) - 1.6, 0.16), ("impact-bass-2", C(5, 0) + 0.4, 0.24), ("sparkle", M["aa"] + 0.3, 0.22), ("chime", M["aa"] + 0.5, 0.2)]

install(ROOT)
page(ROOT, "template.html", TOTAL=r(TOTAL), SCENES="\n      ".join(scene_divs), CAPTIONS="\n      ".join(cap_divs),
     SFX="\n      ".join(sfx_tags(ROOT, sfx, TOTAL)), TIMING=T)
print("index.html written; total", TOTAL)
