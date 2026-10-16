"""Build index.html (1080x1920 Shorts) from timing.json + script.json + per-scene alignments.
Captions sit in the TOP band (Shorts UI covers the bottom). Re-run after tools/retime.py."""
import json, re, html, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "timing.json").read_text())
SPEC = json.loads((ROOT / "script.json").read_text())
TOTAL = T["total"]

HL = ["어학원", "0원", "노바스코샤주", "핼리팩스", "학생비자", "무상", "필요가 없어요", "OK!", "조건이 없거든요",
      "40주", "50주", "10주", "1년", "11,400", "25%", "9시 반", "수업 끝", "학부모", "저렴하고 편해요",
      "자녀무상교육", "AA Canada"]
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

# ---------- word marks: absolute time a TTS substring starts being spoken ----------
def marks():
    out = {}
    want = {
        "s1-hook": {"zero": "영 원"},
        "s2-rule": {"halifax": "핼리팩스", "visa": "학생비자", "free": "무상"},
        "s3-school": {"ok": "오케이", "nocond": "조건이"},
        "s4-weeks": {"fifty": "오십 주", "vac": "방학", "zero4": "영 원", "year": "일 년"},
        "s5-price": {"roll": "만 천사백", "pct": "이십오 퍼센트"},
        "s6-parents": {"930": "아홉 시 반", "end": "끝", "parents": "학부모", "cheap": "저렴하고"},
        "s7-cta": {"aa": "에이에이"},
    }
    for sc, tsc in zip(SPEC["scenes"], T["scenes"]):
        bounds, pos = [], 0
        for _, tt in sc["chunks"]:
            bounds.append((pos, pos + len(tt))); pos += len(tt) + 1
        text = " ".join(c[1] for c in sc["chunks"])
        for key, sub in want.get(sc["id"], {}).items():
            k = text.index(sub)
            ci = next(i for i, (a, b) in enumerate(bounds) if a <= k < b)
            cap = tsc["captions"][ci]
            al = json.loads((ROOT / "assets" / "audio" / "takes" / f"{sc['id']}.t{cap['take']}.align.json").read_text())
            tau = al["character_start_times_seconds"][k]  # take time → chunk time (minus cut fillers) → film time
            cut = sum(min(t1, tau) - t0 for t0, t1 in cap["removed"] if t0 < tau)
            out[key] = round(cap["place"] + tau - cap["src_start"] - cut, 3)
    return out

M = marks()

# ---------- reusable bits ----------
def kt(text, cls="kt"):
    """kinetic text: one inline-block span per glyph (spaces kept)."""
    return f'<span class="{cls}">' + "".join(
        '<span class="ch">&nbsp;</span>' if c == " " else f'<span class="ch">{html.escape(c)}</span>' for c in text) + "</span>"

def odo(digits, cls):
    """odometer: each digit is a column with a 0-9,0-9 strip; ',' and '$' are static."""
    parts = []
    for i, d in enumerate(digits):
        if d.isdigit():
            strip = "".join(f"<b>{n % 10}</b>" for n in range(20))
            parts.append(f'<span class="odc"><span class="strip {cls}-d{i}">{strip}</span></span>')
        else:
            parts.append(f'<span class="ods">{html.escape(d)}</span>')
    return "".join(parts)

def bg(seed):
    rnd = random.Random(seed)
    dots = []
    for k in range(12):
        s = rnd.randint(14, 70)
        col = rnd.choice(["255,210,63", "47,107,255", "31,181,201", "255,255,255"])
        a = rnd.choice([0.22, 0.28, 0.35])
        dots.append(f'<i class="bk" data-sp="{rnd.uniform(0.4, 1.6):.2f}" style="left:{rnd.randint(-20, 1060)}px;top:{rnd.randint(80, 1900)}px;'
                    f'width:{s}px;height:{s}px;background:radial-gradient(circle, rgba({col},{a}) 0%, rgba({col},0) 70%)"></i>')
    return ('<div class="bgl"><div class="mesh"></div>'
            '<svg class="gridl" width="1080" height="2400" viewBox="0 0 1080 2400"><defs><pattern id="gp' + str(seed) + '" width="90" height="90" patternUnits="userSpaceOnUse">'
            '<path d="M90 0H0V90" fill="none" stroke="#ffffff" stroke-opacity="0.07" stroke-width="2"/></pattern></defs>'
            '<rect width="1080" height="2400" fill="url(#gp' + str(seed) + ')"/></svg>' + "".join(dots) + "</div>")

CHECK = '<svg viewBox="0 0 100 100" class="{c}"><path d="M22 54 L42 73 L80 30" fill="none" stroke="#ffffff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
PERSON = ('<svg viewBox="0 0 80 100" class="person"><circle cx="40" cy="26" r="17" fill="#ffd23f"/>'
          '<path d="M10 96 C10 62 22 50 40 50 C58 50 70 62 70 96 Z" fill="#ffd23f"/></svg>')
SCHOOL = ('<svg viewBox="0 0 300 260" class="school">'
          '<path d="M150 8 V60" stroke="#ffffff" stroke-width="6"/><path d="M150 10 H200 L188 24 L200 38 H150 Z" fill="#e63946"/>'
          '<path d="M30 110 L150 50 L270 110 Z" fill="#2f6bff"/><rect x="40" y="108" width="220" height="140" rx="6" fill="#203a6b"/>'
          + "".join(f'<rect class="win" x="{x}" y="{y}" width="38" height="34" rx="4" fill="#3a4f78"/>' for y in (126, 176) for x in (58, 118, 204))
          + '<rect class="win" x="128" y="176" width="44" height="72" rx="4" fill="#3a4f78"/></svg>')
CANADA = ('M120 470 L470 470 L520 490 L560 530 L600 560 L640 545 L660 520 L700 505 L740 480 L780 470 L820 470 L840 455 '
          'L862 468 L902 482 L938 466 L906 454 L872 448 L850 440 L840 415 L800 420 L760 400 L800 380 L860 360 L880 320 '
          'L900 300 L870 250 L840 230 L810 250 L780 210 L740 240 L720 270 L700 310 L680 360 L650 385 L620 380 L600 350 '
          'L560 330 L520 300 L510 250 L530 210 L560 180 L520 170 L470 150 L420 160 L380 140 L330 150 L280 130 L240 140 '
          'L200 120 L180 130 L180 330 L140 400 Z '
          'M350 100 L420 60 L480 90 L430 120 Z M500 90 L600 40 L660 80 L590 120 Z '
          'M700 170 L760 110 L830 150 L800 200 L740 210 Z M900 390 L940 370 L962 400 L930 432 L905 420 Z')

SCENES = {
"s1-hook": """
  <div class="tagwrap" id="s1-tag" data-layout-allow-overlap>
    <div class="tag">
      <i class="hole"></i>
      <div class="tag-l">핼리팩스 공립학교 · 유학생 학비</div>
      <div class="tag-p"><span class="tag-big">$10,000</span><span class="tag-u">/ 1년</span></div>
      <i class="sweep" id="s1-sweep"></i>
      <i class="slash" id="s1-slash"></i>
    </div>
  </div>
  <div class="zero" id="s1-zero" data-layout-allow-overlap><span class="zero-n">$0</span><span class="zero-u">자녀 공립학교 학비</span></div>
  <i class="ring" id="s1-ring" style="left:540px;top:880px"></i>
  <div class="fn" id="s1-fn">* 부모 학생비자(노바스코샤) 유효 기간 기준 · HRCE Category I · 정책은 변경될 수 있음</div>
""",
"s2-rule": f"""
  <div class="geo" id="s2-geo">
  <div class="mapwrap" id="s2-map">
    <svg viewBox="0 0 1000 620" class="map" id="s2-mapsvg"><path id="s2-path" d="{CANADA}" pathLength="1" fill="#1a3466" fill-opacity="0" stroke="#5fa8ff" stroke-width="4" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
      <circle id="s2-ns" cx="905" cy="468" r="12" fill="#ffd23f" opacity="0"/></svg>
    <div class="mapcap" id="s2-mapcap">CANADA</div>
  </div>
  <div class="pin" id="s2-pin"><svg viewBox="0 0 24 24" width="130" height="130"><path fill="#e63946" d="M12 2C7.6 2 4 5.6 4 10c0 5.6 8 12 8 12s8-6.4 8-12c0-4.4-3.6-8-8-8zm0 11a3 3 0 110-6 3 3 0 010 6z"/></svg></div>
  <i class="ring" id="s2-ring" style="left:540px;top:890px;border-color:#1fb5c9"></i>
  <div class="hfx" id="s2-hfx"><div class="hfx-t">{kt("HALIFAX")}</div><div class="hfx-s">NOVA SCOTIA · 노바스코샤</div></div>
  </div>
  <div class="persp p2"><div class="permit" id="s2-card">
    <div class="pm-top"><svg viewBox="0 0 100 100" class="leaf"><path d="M50 4 L57 20 L66 14 L63 38 L76 28 L80 38 L94 36 L86 52 L92 56 L70 70 L73 80 L53 76 L53 96 L47 96 L47 76 L27 80 L30 70 L8 56 L14 52 L6 36 L20 38 L24 28 L37 38 L34 14 L43 20 Z" fill="#e63946"/></svg><span>CANADA · 학생비자</span></div>
    <div class="pm-title">STUDY PERMIT</div>
    <div class="pm-row"><div class="pm-photo"><svg viewBox="0 0 80 100"><circle cx="40" cy="34" r="18" fill="#9fb0cf"/><path d="M8 100 C8 66 22 58 40 58 C58 58 72 66 72 100Z" fill="#9fb0cf"/></svg></div>
      <div class="pm-f"><div><b>HOLDER</b> 부모님 (Parent)</div><div><b>PROVINCE</b> NOVA SCOTIA</div><div><b>STATUS</b> <span class="ok">VALID</span></div></div></div>
    <i class="sweep" id="s2-sweep"></i>
  </div></div>
  <div class="schoolwrap" id="s2-school">{SCHOOL}<div class="sch-l">자녀 · 공립학교</div></div>
  <div class="stamp st-green" id="s2-stamp" data-layout-allow-overlap>FREE</div>
  <div class="fn" id="s2-fn">* HRCE(핼리팩스 교육청) International Students · Category I 기준</div>
""",
"s3-school": f"""
  <div class="duo">
    <div class="sc sc-l" id="s3-l">
      <svg viewBox="0 0 120 100" class="sc-ic"><path d="M60 12 L114 36 L60 60 L6 36 Z" fill="#ffffff"/><path d="M28 48 V72 C28 82 92 82 92 72 V48 L60 62 Z" fill="#ffffff"/><path d="M106 40 V70" stroke="#ffd23f" stroke-width="6"/></svg>
      <div class="sc-t">대학 · 컬리지</div>
      <div class="sc-s">University / College</div>
      <div class="sc-x" id="s3-x">필수 아님</div>
    </div>
    <div class="sc sc-r" id="s3-r">
      <div class="sc-gray" id="s3-gray" data-layout-allow-overlap><div class="qm">?</div></div>
      <svg viewBox="0 0 120 100" class="sc-ic"><rect x="14" y="16" width="44" height="66" rx="6" fill="#ffd23f"/><rect x="62" y="16" width="44" height="66" rx="6" fill="#1fb5c9"/><path d="M24 34 H48 M24 46 H48 M72 34 H96 M72 46 H96" stroke="#0b1730" stroke-width="5"/></svg>
      <div class="sc-t">사설 어학원</div>
      <div class="sc-s">Private Language School</div>
      <div class="sc-ok" id="s3-ok">{CHECK.format(c="ck")}</div>
      <i class="sweep" id="s3-sweep"></i>
    </div>
  </div>
  <div class="stamp st-big" id="s3-stamp" data-layout-allow-overlap>학교 종류 조건 없음</div>
  <div class="fn" id="s3-fn">* 부모 학생비자(노바스코샤) 유효 기간 동안</div>
""",
"s4-weeks": f"""
  <div class="wk-head" id="s4-head"><span class="odo odo-w" data-layout-allow-overflow data-layout-allow-overlap>{odo("40", "w")}</span><span class="wk-u">주</span></div>
  <div class="weeks" id="s4-grid">
    {"".join(f'<i class="wb nv" style="left:{(k % 10) * 94}px;top:{(k // 10) * 86}px"></i>' for k in range(40))}
    {"".join(f'<i class="wb gd" style="left:{k * 94}px;top:344px"></i>' for k in range(10))}
    <div class="vac" id="s4-vac">방학 10주 · $0</div>
  </div>
  <i class="ring" id="s4-ring" style="left:540px;top:640px"></i>
  <div class="persp p4"><div class="loa" id="s4-loa">
    <div class="loa-h">LETTER OF ACCEPTANCE</div>
    <div class="loa-k">입학허가서 · 학부모 영어 프로그램</div>
    <div class="loa-line"><b>Tuition</b><span>40 weeks</span></div>
    <div class="loa-line"><b>Vacation</b><span>+ 10 weeks</span></div>
    <div class="loa-line big"><b>Program</b><span>50 weeks</span></div>
    <i class="sweep" id="s4-sweep"></i>
  </div></div>
  <div class="stamp st-gold" id="s4-stamp" data-layout-allow-overlap>50 WEEKS</div>
  <div class="yr" id="s4-yr"><div class="yr-l">9월 ~ 6월 · 아이 학교 1년</div><div class="yr-bar"><i id="s4-fill"></i></div><div class="yr-ck" id="s4-ck">{CHECK.format(c="ck")}</div></div>
  <div class="persp p4e"><div class="evid" id="s4-evid" data-layout-allow-overlap><div class="ev-t">학교 공식 안내 · 방학 규정</div>
    <div class="ev-img"><img src="assets/schedule.jpg" alt=""/><i class="marker" id="s4-mk"></i></div></div></div>
""",
"s5-price": f"""
  <div class="pimg" id="s5-pimg"><img src="assets/price.jpg" alt=""/></div>
  <div class="printer"><i class="slot"></i></div>
  <div class="rcpt-clip"><div class="rcpt" id="s5-rcpt">
    <div class="rc-h">학부모 영어 프로그램 · 핼리팩스</div>
    <div class="rc-s">40주 등록 · 주 26레슨</div>
    <div class="rc-dash"></div>
    <div class="rc-row"><span>정가 $380 × 40주</span><span class="old" id="s5-old">$15,200<i id="s5-strike"></i></span></div>
    <div class="rc-row"><span>할인가 $285 × 40주</span><span></span></div>
    <div class="rc-big"><span class="odo odo-p" data-layout-allow-overflow data-layout-allow-overlap>{odo("$15,200", "p")}</span><span class="rc-cad">CAD</span></div>
    <div class="rc-dash"></div>
    <div class="rc-row vac2" id="s5-vac"><span>방학 10주</span><span>$0</span></div>
  </div></div>
  <div class="badge" id="s5-badge" data-layout-allow-overlap>-25%</div>
  <div class="fn" id="s5-fn">* CAD · 2026 Oxford International 요금표 기준 · 등록비·교재비·보험 별도 · 변동 가능</div>
""",
"s6-parents": f"""
  <div class="ph-a" id="s6-a">
    <div class="clock" id="s6-clock">
      <svg viewBox="0 0 440 440" width="440" height="440">
        <circle cx="220" cy="220" r="206" fill="#10234a" stroke="#ffffff" stroke-width="10"/>
        {"".join(f'<path d="M220 26 V{50 if h % 3 == 0 else 40}" stroke="#ffffff" stroke-width="{8 if h % 3 == 0 else 4}" transform="rotate({h * 30} 220 220)"/>' for h in range(12))}
        <circle id="s6-arc" cx="220" cy="220" r="176" fill="none" stroke="#ffd23f" stroke-width="22" pathLength="360" stroke-dasharray="142.5 360" stroke-dashoffset="142.5" transform="rotate(195 220 220)" stroke-linecap="round"/>
        <path id="s6-hh" d="M220 220 V112" stroke="#ffffff" stroke-width="16" stroke-linecap="round"/>
        <path id="s6-mh" d="M220 220 V60" stroke="#1fb5c9" stroke-width="10" stroke-linecap="round"/>
        <circle cx="220" cy="220" r="14" fill="#e63946"/>
      </svg>
      <div class="ct ct1" id="s6-t1">9:30 시작</div>
      <div class="ct ct2" id="s6-t2">2:15 끝</div>
    </div>
    <div class="flow">
      <div class="fl" id="s6-f1"><svg viewBox="0 0 60 60"><path d="M6 26 L30 12 L54 26 Z" fill="#2f6bff"/><rect x="10" y="26" width="40" height="28" fill="#ffffff"/><rect x="25" y="38" width="10" height="16" fill="#2f6bff"/></svg><span>아이 등교</span></div>
      <i class="fa" id="s6-a1">→</i>
      <div class="fl fl-hl" id="s6-f2"><svg viewBox="0 0 60 60"><rect x="8" y="12" width="20" height="38" rx="3" fill="#0b1730"/><rect x="32" y="12" width="20" height="38" rx="3" fill="#0b1730"/></svg><span>부모 수업</span></div>
      <i class="fa" id="s6-a2">→</i>
      <div class="fl" id="s6-f3"><svg viewBox="0 0 60 60"><circle cx="22" cy="16" r="8" fill="#ffffff"/><path d="M10 54 C10 34 14 28 22 28 C30 28 34 34 34 54Z" fill="#ffffff"/><circle cx="42" cy="26" r="6" fill="#ffd23f"/><path d="M33 54 C33 40 36 36 42 36 C48 36 51 40 51 54Z" fill="#ffd23f"/></svg><span>함께 하교</span></div>
    </div>
  </div>
  <div class="ph-b" id="s6-b">
    <div class="ppl">{"".join(f'<div class="pp">{PERSON}</div>' for _ in range(14))}</div>
    <div class="ppl-l"><span class="pill-g">최대 14명</span> 소규모 반 · <b>모두 학부모</b></div>
  </div>
  <div class="cmp" id="s6-c">
    <div class="cmp-h"><span></span><span>대학 부설 어학과정</span><span class="cmp-me">학부모 영어 프로그램</span></div>
    <div class="cmp-r" id="s6-r1"><span>학비</span><span>상대적으로 높음</span><span class="me">40주 $11,400<i class="mc">{CHECK.format(c="ck")}</i></span></div>
    <div class="cmp-r" id="s6-r2"><span>반 구성</span><span>일반 유학생</span><span class="me">모두 학부모<i class="mc">{CHECK.format(c="ck")}</i></span></div>
    <div class="cmp-r" id="s6-r3"><span>수업 시간</span><span>일반 시간표</span><span class="me">등·하교에 맞춤<i class="mc">{CHECK.format(c="ck")}</i></span></div>
  </div>
  <div class="persp p6"><div class="flyer" id="s6-fly" data-layout-allow-overlap><div class="fly-t">Oxford International · 학부모 영어 프로그램 안내</div>
    <div class="fly-img"><img src="assets/flyer.jpg" alt=""/><i class="marker" id="s6-mk"></i></div></div></div>
""",
"s7-cta": f"""
  <div class="leak" id="s7-leak"></div>
  <div class="beam" id="s7-beam"></div>
  <div class="cta-logo" id="s7-logo">{kt("AA CANADA", "kt logo-kt")}</div>
  <div class="cta-sub" id="s7-sub">캐나다 자녀무상교육 · 유학 후 이민 · 영주권</div>
  <div class="cta-cities" id="s7-cities">핼리팩스 · 몬트리올 · 밴쿠버 · 토론토</div>
  <div class="cta-btn" id="s7-btn"><i class="btn-ring" id="s7-bring"></i>무료 상담 · 카톡 <b>canlog</b></div>
  <svg class="harbor" viewBox="0 0 1080 420" width="1080" height="420">
    <path class="ln" pathLength="1" d="M60 330 V250 H120 V210 H170 V270 H220 V190 H260 V150 H300 V190 H330 V260 H390 V230 H450 V280 H520 V240 H560 V300 H640 V330" fill="none" stroke="#5fa8ff" stroke-width="5"/>
    <path class="ln" pathLength="1" d="M800 330 L830 120 H900 L930 330 Z" fill="none" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"/>
    <path class="ln" pathLength="1" d="M822 180 H908 M814 240 H916 M806 300 H924" fill="none" stroke="#e63946" stroke-width="10"/>
    <path class="ln" pathLength="1" d="M836 120 V80 H894 V120 M828 80 L865 46 L902 80" fill="none" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"/>
    <circle id="s7-lamp" cx="865" cy="100" r="16" fill="#ffd23f" opacity="0"/>
    <path class="ln" pathLength="1" d="M0 350 Q45 335 90 350 T180 350 T270 350 T360 350 T450 350 T540 350 T630 350 T720 350 T810 350 T900 350 T990 350 T1080 350" fill="none" stroke="#1fb5c9" stroke-width="6"/>
    <path class="ln" pathLength="1" d="M40 385 Q85 370 130 385 T220 385 T310 385 T400 385 T490 385 T580 385 T670 385 T760 385 T850 385 T940 385 T1030 385" fill="none" stroke="#1fb5c9" stroke-opacity="0.6" stroke-width="5"/>
  </svg>
  <div class="fn" id="s7-fn">* 부모 학생비자(노바스코샤) 유효 기간 기준 · HRCE Category I · 정책은 변경될 수 있음</div>
""",
}

scene_divs, cap_divs = [], []
for i, s in enumerate(T["scenes"]):
    scene_divs.append(f'<section id="{s["id"]}" class="scene">{bg(i + 1)}<div class="cam" id="{s["id"]}-cam">{SCENES[s["id"]]}</div></section>')
    for j, c in enumerate(s["captions"]):
        cap_divs.append(
            f'<div id="cap-{i}-{j}" class="clip cap" data-start="{r(c["start"])}" data-duration="{r(c["end"] - c["start"])}" data-track-index="2">'
            f'<div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{cap_html(c["text"])}</span></div></div>')

# ---------- SFX (≈ -12 dB) ----------
S = T["scenes"]
def C(i, j): return S[i]["captions"][j]["start"]
TR = [S[i]["start"] - 0.25 for i in range(1, len(S))]  # shader transition starts
sfx = [("whoosh", TR[0] - 0.05, 0.3), ("whoosh", TR[1] - 0.05, 0.3), ("glitch-1", TR[2], 0.2), ("whoosh", TR[3] - 0.05, 0.3),
       ("whoosh", TR[4] - 0.05, 0.3), ("whoosh-cinematic", TR[5] - 0.35, 0.22),
       ("impact-bass-1", M["zero"] + 0.25, 0.32), ("sparkle", M["zero"] + 0.3, 0.16),
       ("pop", M["halifax"] + 0.3, 0.25), ("whoosh", M["visa"] - 0.1, 0.22), ("stamp", M["free"] + 0.3, 0.4),
       ("pop", M["ok"] + 0.15, 0.3), ("stamp", M["nocond"] + 0.3, 0.4),
       ("impact-bass-2", M["fifty"] + 0.45, 0.3), ("stamp", M["year"] + 0.15, 0.36),
       ("click-soft", C(4, 0), 0.25), ("ding", M["roll"] + 0.95, 0.32), ("ding", M["pct"] + 0.1, 0.3),
       ("pop", M["parents"], 0.22), ("pop", M["cheap"] + 0.2, 0.2), ("pop", M["cheap"] + 0.6, 0.2), ("pop", M["cheap"] + 1.0, 0.2),
       ("sparkle", C(6, 0) + 0.2, 0.22), ("chime", M["aa"] + 0.3, 0.2)]
DUR = {}
import subprocess
def dur(n):
    if n not in DUR:
        DUR[n] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                                str(ROOT / "assets" / "sfx" / f"{n}.mp3")]).strip())
    return DUR[n]
sfx_tags = []
for k, (n, t, v) in enumerate(sorted(sfx, key=lambda x: x[1])):
    d = min(dur(n), TOTAL - t)
    sfx_tags.append(f'<audio id="sfx-{k}" class="clip" src="assets/sfx/{n}.mp3" data-start="{r(t)}" data-duration="{r(d)}" data-track-index="{11 + k % 3}" data-volume="{v}"></audio>')

page = (ROOT / "tools" / "template.html").read_text()
page = (page.replace("__TOTAL__", r(TOTAL))
            .replace("__SCENES__", "\n      ".join(scene_divs))
            .replace("__CAPTIONS__", "\n      ".join(cap_divs))
            .replace("__SFX__", "\n      ".join(sfx_tags))
            .replace("__MARKS__", json.dumps(M))
            .replace("__TIMING__", json.dumps(T, ensure_ascii=False)))
(ROOT / "index.html").write_text(page)
print("index.html written; total", TOTAL, "marks", M)
