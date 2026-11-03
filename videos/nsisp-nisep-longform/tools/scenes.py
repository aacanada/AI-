"""Scene builders. Each returns (css, body_html, js). T(phrase) = local time (s) when the phrase is spoken."""
import json
import os

from common import J

MAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canada_map.json"), encoding="utf-8"))

PERSON = ('<svg viewBox="0 0 40 64" width="{w}" height="{h}"><circle cx="20" cy="12" r="10" fill="{c}"/>'
          '<path d="M4 62 V36 Q4 24 20 24 Q36 24 36 36 V62 Z" fill="{c}"/></svg>')
SCHOOL = ('<svg viewBox="0 0 120 100" width="{w}" height="{h}"><path d="M10 44 L60 14 L110 44" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round"/>'
          '<rect x="20" y="44" width="80" height="50" fill="none" stroke="{c}" stroke-width="7"/><rect x="50" y="64" width="20" height="30" fill="{c}"/>'
          '<line x1="60" y1="14" x2="60" y2="2" stroke="{c}" stroke-width="5"/><path d="M60 2 L76 7 L60 12Z" fill="{c}"/></svg>')
PIN = ('<svg viewBox="0 0 40 56" width="{w}" height="{h}"><path d="M20 54 C20 54 2 32 2 20 A18 18 0 0 1 38 20 C38 32 20 54 20 54Z" fill="{c}" stroke="#07131f" stroke-width="3"/>'
       '<circle cx="20" cy="20" r="7" fill="#07131f"/></svg>')
HOUSE = ('<svg viewBox="0 0 300 260" width="{w}" height="{h}"><path class="hs" d="M20 120 L150 20 L280 120" fill="none" stroke="#f5f0e6" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>'
         '<path class="hs" d="M50 100 V245 H250 V100" fill="none" stroke="#f5f0e6" stroke-width="10" stroke-linejoin="round"/>'
         '<path class="hs" d="M125 245 V175 H175 V245" fill="none" stroke="#f2a33a" stroke-width="10" stroke-linejoin="round"/>'
         '<path class="hs" d="M75 135 H110 V165 H75 Z M190 135 H225 V165 H190 Z" fill="none" stroke="#f5f0e6" stroke-width="8"/></svg>')
SHIELD = ('<svg viewBox="0 0 100 120" width="{w}" height="{h}"><path d="M50 4 L94 20 V58 C94 88 72 108 50 116 C28 108 6 88 6 58 V20 Z" fill="#2fb5a5"/>'
          '<path d="M28 60 L44 76 L74 44" fill="none" stroke="#07131f" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def header(kick, title, cid):
    return (f'<div class="abs kick" id="{cid}-kick">{kick}</div>'
            f'<div class="abs h title" id="{cid}-title">{title}</div>')


# ------------------------------------------------------------------ S1 overlay (face)
def s01(T, D):
    css = """
R .lt{left:96px;top:640px;padding:20px 40px 24px;border-radius:26px;background:rgba(7,19,31,.80);border-left:12px solid #2fb5a5;box-shadow:0 20px 40px rgba(0,0,0,.35)}
R .lt .k{font-weight:700;font-size:28px;letter-spacing:.12em;color:#2fb5a5}
R .lt .t{font-weight:900;font-size:88px;letter-spacing:-.02em;line-height:1.05;margin-top:6px;white-space:nowrap}
R .lt .t i{font-style:normal;font-weight:800;font-size:64px;color:rgba(245,240,230,.75);margin:0 22px}
R .lt .s{font-weight:700;font-size:30px;color:rgba(245,240,230,.85);margin-top:10px}
"""
    body = """<div class="abs lt" id="s01-lt"><div class="k">캐나다 공립 조기유학 비교</div>
<div class="t"><span class="ns-c" id="s01-a">NSISP</span><i>vs</i><span class="nl-c" id="s01-b">NISEP</span></div>
<div class="s">노바스코샤 · 뉴펀들랜드 래브라도</div></div>"""
    js = [J("inn", "#s01-lt", 0.6, x=-60, y=0, d=0.8),
          J("pulse", "#s01-a", T("NSISP"), s=1.1),
          J("pulse", "#s01-b", T("NISEP입니다"), s=1.12)]
    return css, body, js


# ------------------------------------------------------------------ S2 map + school counts
def s02(T, D):
    full, zoom = "0 0 793 1032", "585 860 230 159"
    sc = 1100 / 230
    px = lambda x, y: (round(40 + (x - 585) * sc), round(110 + (y - 860) * sc))
    hx, hy = px(695, 994)
    sx, sy = px(791, 955)
    paths = "".join(f'<path class="pv pv-{k}" d="{p}" fill="#1d3d5c" stroke="#0a1c30" stroke-width="1.2"/>'
                    for k, p in MAP["paths"].items())
    css = f"""
R .map{{left:40px;top:110px;width:1100px;height:760px}}
R .pin{{position:absolute;width:44px;height:62px;margin-left:-22px;margin-top:-60px}}
R .plab{{position:absolute;white-space:nowrap;font-weight:900;font-size:38px;text-shadow:0 3px 10px rgba(0,0,0,.6)}}
R .plab small{{display:block;font-weight:700;font-size:24px;color:rgba(245,240,230,.8)}}
R .sea{{left:700px;top:812px;font-weight:700;font-style:italic;font-size:34px;letter-spacing:.2em;color:rgba(160,205,235,.55)}}
R .pc{{left:1180px;width:680px;padding:30px 40px}}
R .pc .row{{display:flex;align-items:flex-end;gap:16px;margin-top:20px}}
R .pc .big{{font-size:120px}}
R .pc .unit{{font-weight:800;font-size:40px;padding-bottom:12px}}
R .pc .sub{{font-weight:700;font-size:28px;color:rgba(245,240,230,.8);margin-top:14px}}
R .pc .plus{{font-weight:900;font-size:64px;color:rgba(245,240,230,.5);padding:0 6px 26px}}
R .pc .lab{{font-weight:700;font-size:26px;color:rgba(245,240,230,.75);display:block}}
R #s02-c1{{top:120px}}
R #s02-c2{{top:440px}}
R .grades{{left:1180px;top:780px;display:flex;gap:16px}}
R .grades .chip{{position:relative;font-size:28px;padding:10px 24px}}
"""
    body = f"""<svg class="abs map" id="s02-map" viewBox="{full}" preserveAspectRatio="xMidYMid meet">{paths}</svg>
<div class="abs sea" id="s02-sea">ATLANTIC  대서양</div>
<div class="pin" id="s02-p1" style="left:{hx}px;top:{hy}px">{PIN.format(w=44, h=62, c="#4aa3df")}</div>
<div class="plab" id="s02-l1" style="left:{hx - 330}px;top:{hy - 20}px">핼리팩스<small>노바스코샤 Nova Scotia</small></div>
<div class="pin" id="s02-p2" style="left:{sx}px;top:{sy}px">{PIN.format(w=44, h=62, c="#f2a33a")}</div>
<div class="plab" id="s02-l2" style="left:{sx - 170}px;top:{sy + 96}px">세인트존스<small>뉴펀들랜드 래브라도</small></div>
<div class="dcard pc" id="s02-c1"><span class="pill ns">NSISP <small>노바스코샤</small></span>
  <div class="row"><span class="num big ns-c" id="s02-n1">0</span><span class="unit">개 학교</span></div>
  <div class="sub" id="s02-c1s">여러 지역 교육청이 함께 참여</div></div>
<div class="dcard pc" id="s02-c2"><span class="pill nl">NISEP <small>뉴펀들랜드 래브라도</small></span>
  <div class="row"><span><span class="lab">고등학교 약</span><span class="num big nl-c" id="s02-n2">0</span></span><span class="unit">곳</span>
  <span class="plus">+</span><span><span class="lab">중학교 약</span><span class="num big nl-c" id="s02-n3">0</span></span><span class="unit">곳</span></div>
  <div class="sub" id="s02-c2s">영어 교육청 1곳 · 공립학교 유학은 NISEP</div></div>
<div class="abs grades" id="s02-g"><span class="chip cream">7~12학년</span><span class="chip cream">만 12~18세</span><span class="chip teal">9월 · 2월 입학</span></div>"""
    t_atl = T("대서양")
    js = [J("inn", "#s02-map", 0.2, s=1.04, y=0, d=1.0),
          J("fromto", "#s02-map", t_atl - 0.3, f={"attr": {"viewBox": full}}, t={"attr": {"viewBox": zoom}, "duration": 2.2, "ease": "power3.inOut"}),
          J("to", "#s02-map .pv-ns, #s02-map .pv-nl, #s02-map .pv-nb, #s02-map .pv-pe", t_atl + 1.0, fill="#2c5a80", duration=0.8),
          J("inn", "#s02-sea", t_atl + 1.6, y=0, x=-30),
          J("to", "#s02-map .pv-ns", T("NSISP는"), fill="#4aa3df", duration=0.6),
          J("fromto", "#s02-p1", T("NSISP는") + 0.2, f={"opacity": 0, "y": -120}, t={"opacity": 1, "y": 0, "duration": 0.6, "ease": "bounce.out"}),
          J("inn", "#s02-l1", T("NSISP는") + 0.5, x=30, y=0),
          J("inn", "#s02-c1", T("NSISP는"), x=60, y=0),
          J("inn", "#s02-c1s", T("여러 지역"), y=14),
          J("count", "#s02-n1", T("65개"), a=0, b=65, d=1.3),
          J("pulse", "#s02-n1", T("65개") + 1.3),
          J("to", "#s02-map .pv-nl", T("NISEP은"), fill="#f2a33a", duration=0.6),
          J("fromto", "#s02-p2", T("NISEP은") + 0.2, f={"opacity": 0, "y": -120}, t={"opacity": 1, "y": 0, "duration": 0.6, "ease": "bounce.out"}),
          J("inn", "#s02-l2", T("NISEP은") + 0.5, x=30, y=0),
          J("inn", "#s02-c2", T("NISEP은"), x=60, y=0),
          J("inn", "#s02-c2s", T("영어 교육청"), y=14),
          J("count", "#s02-n2", T("고등학교 약"), a=0, b=30, d=1.2),
          J("count", "#s02-n3", T("중학교 약"), a=0, b=20, d=1.2),
          J("pop", "#s02-g .chip:nth-child(1)", T("7학년부터"), st=0),
          J("pop", "#s02-g .chip:nth-child(2)", T("만 12세"), st=0),
          J("pop", "#s02-g .chip:nth-child(3)", T("9월과"), st=0),
          J("pulse", "#s02-p1, #s02-p2", T("9월과") + 0.4, s=1.25, st=0.1)]
    return css, body, js


# ------------------------------------------------------------------ S3 school placement
def s03(T, D):
    region = ('<svg viewBox="0 0 160 120" width="150" height="112"><path d="M10 30 L60 10 L100 26 L150 12 V92 L100 110 L60 92 L10 108 Z" fill="none" stroke="#4aa3df" stroke-width="7" stroke-linejoin="round"/>'
              '<path d="M60 10 V92 M100 26 V110" stroke="#4aa3df" stroke-width="5" stroke-dasharray="8 8"/>'
              '<circle cx="80" cy="58" r="16" fill="#4aa3df"/></svg>')
    css = """
R .q{left:0;right:0;top:120px;text-align:center;font-size:76px}
R .cc{top:270px;width:780px;height:500px;padding:40px 48px}
R #s03-L{left:130px}
R #s03-R{left:1010px}
R .cc .ic{position:absolute;right:44px;top:34px}
R .cc .big{font-weight:900;font-size:74px;letter-spacing:-.03em;margin-top:34px}
R .cc .ln{display:flex;align-items:center;gap:18px;font-weight:700;font-size:34px;margin-top:26px;color:#0b1f33}
R .cc .ln i{display:block;width:16px;height:16px;border-radius:50%;flex:none}
R .vs{left:910px;top:470px;width:100px;height:100px;border-radius:50%;background:#0a1c30;border:4px solid rgba(245,240,230,.4);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:36px}
R .ban{left:0;right:0;top:800px;text-align:center}
R .ban span{display:inline-block;padding:14px 40px;border-radius:99px;background:rgba(47,181,165,.18);border:2px solid #2fb5a5;font-weight:800;font-size:34px}
"""
    body = f"""<div class="abs h q" id="s03-q">학교를 고를 수 있을까?</div>
<div class="card cc" id="s03-L"><span class="pill ns">NSISP</span><div class="ic">{region}</div>
  <div class="big" style="color:#1f6fa8">지역 배정</div>
  <div class="ln" id="s03-L1"><i style="background:#4aa3df"></i>배치 지역은 NSISP가 정함</div>
  <div class="ln" id="s03-L2"><i style="background:#4aa3df"></i>1년 후 지역 변경 신청 가능</div></div>
<div class="card cc" id="s03-R"><span class="pill nl">NISEP</span><div class="ic">{SCHOOL.format(w=150, h=125, c="#f2a33a")}</div>
  <div class="big" style="color:#b86a07">학교 희망 요청</div>
  <div class="ln" id="s03-R1"><i style="background:#f2a33a"></i>특정 학교 희망 요청 가능</div>
  <div class="ln" id="s03-R2"><i style="background:#f2a33a"></i>도시 · 시골 학교 중 선택</div></div>
<div class="abs vs" id="s03-vs">VS</div>
<div class="abs ban" id="s03-ban"><span>원하는 동네 · 학교가 분명하다면, 이 차이부터 확인</span></div>"""
    js = [J("kin", "#s03-q", 0.5),
          J("pulse", "#s03-q", T("학교를 고를"), s=1.06),
          J("flip", "#s03-L", T("NSISP는 배치"), r=-80),
          J("inn", "#s03-L1", T("NSISP는 배치") + 0.6, x=-20, y=0),
          J("inn", "#s03-L2", T("1년이"), x=-20, y=0),
          J("pop", "#s03-vs", T("NISEP은 특정") - 0.3, st=0),
          J("flip", "#s03-R", T("NISEP은 특정"), r=80),
          J("inn", "#s03-R1", T("NISEP은 특정") + 0.6, x=-20, y=0),
          J("inn", "#s03-R2", T("도시 학교"), x=-20, y=0),
          J("to", "#s03-q", T("원하는 동네") - 0.2, opacity=0.35, duration=0.5),
          J("inn", "#s03-ban", T("원하는 동네"), y=20),
          J("pulse", "#s03-L, #s03-R", T("이 차이"), s=1.03, st=0.15)]
    return css, body, js


# ------------------------------------------------------------------ S4 people icons / 2.5%
def s04(T, D):
    people = "".join(f'<span class="pp">{PERSON.format(w=58, h=92, c="#4aa3df")}</span>' for _ in range(7))
    lit = {17, 58, 96, 131, 172, 214, 251, 288, 333, 377}
    dots = "".join(f'<i class="dt{" on" if i in lit else ""}"></i>' for i in range(400))
    css = """
R .pn{top:230px;width:820px;height:560px;padding:36px 44px}
R #s04-L{left:110px}
R #s04-R{left:990px}
R .pn .t{font-weight:800;font-size:36px;margin-top:18px}
R .pn .t b{font-weight:900}
R .ppl{display:flex;gap:20px;margin-top:46px;align-items:flex-end}
R .ppl .sch{margin-right:10px}
R .pp{display:block}
R .pn .big{font-weight:900;font-size:110px;line-height:1;margin-top:34px}
R .pn .big small{font-size:44px;font-weight:800;margin-left:8px}
R .pn .s{font-weight:700;font-size:28px;color:rgba(245,240,230,.75);margin-top:12px}
R .grid{position:absolute;right:44px;top:120px;display:grid;grid-template-columns:repeat(20,14px);gap:6px}
R .dt{display:block;width:14px;height:14px;border-radius:50%;background:rgba(245,240,230,.22)}
R .dt.on{background:#f2a33a;box-shadow:0 0 10px rgba(242,163,58,.9)}
R .rx{position:absolute;left:44px;top:250px;width:330px}
R .rx .big{font-size:96px}
R .ban{left:0;right:0;top:818px;text-align:center}
R .ban span{display:inline-flex;align-items:center;gap:16px;padding:14px 40px;border-radius:99px;background:#f5f0e6;color:#0b1f33;font-weight:900;font-size:36px}
"""
    body = f"""<div class="abs kick" id="s04-kick">ENGLISH ENVIRONMENT</div>
<div class="abs h title" id="s04-title">한 학교에 유학생은 몇 명?</div>
<div class="dcard pn" id="s04-L"><span class="pill ns">NSISP</span>
  <div class="t">한 학교 · <b class="ns-c">같은 나라 학생</b></div>
  <div class="ppl"><span class="sch">{SCHOOL.format(w=120, h=100, c="#f5f0e6")}</span>{people}</div>
  <div class="big ns-c">최대 <span id="s04-n7">0</span><small>명</small></div>
  <div class="s">국가별 인원 제한</div></div>
<div class="dcard pn" id="s04-R"><span class="pill nl">NISEP</span>
  <div class="t">한 학교 · <b class="nl-c">전교생 대비</b></div>
  <div class="grid" id="s04-grid">{dots}</div>
  <div class="rx"><div class="big nl-c num"><span id="s04-pc">0.0</span><small>%</small></div><div class="s">이하</div>
  <div class="s" id="s04-ex" style="margin-top:30px;color:#f5f0e6;font-size:30px">400명 학교<br>→ 유학생 10명 안팎</div></div></div>
<div class="abs ban" id="s04-ban"><span>{PERSON.format(w=26, h=40, c="#0b1f33")} 캐나다 학생들 사이에서, 영어로 생활</span></div>"""
    js = [J("inn", "#s04-kick", 0.3, y=10), J("kin", "#s04-title", 0.4),
          J("inn", "#s04-L", T("NSISP는") - 0.2, x=-50, y=0),
          J("pop", "#s04-L .sch", T("한 학교에"), st=0),
          J("pop", "#s04-L .pp", T("같은 나라"), st=0.12),
          J("count", "#s04-n7", T("7명"), a=0, b=7, d=0.9),
          J("inn", "#s04-R", T("NISEP은") - 0.2, x=50, y=0),
          J("fromto", "#s04-grid .dt", T("NISEP은") + 0.3, f={"opacity": 0, "scale": 0}, t={"opacity": 1, "scale": 1, "duration": 0.3, "stagger": {"each": 0.003, "from": "start"}}),
          J("count", "#s04-pc", T("2.5%"), a=0, b=2.5, d=1.0, dec=1),
          J("pop", "#s04-grid .dt.on", T("2.5%") + 0.3, s=3, st=0.06),
          J("inn", "#s04-ex", T("학생이 400명"), y=16),
          J("pulse", "#s04-grid .dt.on", T("10명 안팎"), s=1.6, st=0.03),
          J("inn", "#s04-ban", T("캐나다 학생들") - 0.3, y=24)]
    return css, body, js


# ------------------------------------------------------------------ S5 cost
def s05(T, D):
    items = [("학비", 9500, "#f2a33a"), ("홈스테이 (10개월)", 10850, "#f2c14e"), ("의료보험", 700, "#2fb5a5"),
             ("지원비", 400, "#4fd1c5"), ("행정비", 250, "#9bd8f0"), ("오리엔테이션", 250, "#f5f0e6")]
    W, tot = 1640, sum(v for _, v, _ in items)
    assert tot == 21950
    segs, x = "", 0
    for i, (n, v, c) in enumerate(items):
        w = round(W * v / tot) if i < len(items) - 1 else W - x
        segs += f'<div class="seg" id="s05-g{i}" style="left:{x}px;width:{w}px;background:{c}"></div>'
        x += w
    leg = "".join(f'<div class="lg" id="s05-l{i}"><i style="background:{c}"></i><span class="n">{n}</span><span class="v num">${v:,}</span></div>'
                  for i, (n, v, c) in enumerate(items))
    keys = ["학비 9", "10개월", "의료보험", "지원비", "행정비", "오리엔테이션"]
    css = """
R .tot{right:140px;top:96px;text-align:right}
R .tot .l{font-weight:700;font-size:28px;color:rgba(245,240,230,.75)}
R .tot .v{font-size:132px;color:#f2a33a}
R .tot .v small{font-size:56px;margin-right:6px}
R .bar{left:140px;top:330px;width:1640px;height:110px;border-radius:20px;overflow:hidden;background:rgba(245,240,230,.07);border:2px dashed rgba(245,240,230,.25)}
R .seg{position:absolute;top:0;height:110px;border-right:3px solid #0a1c30}
R .run{left:140px;top:452px;font-weight:800;font-size:30px;color:rgba(245,240,230,.8)}
R .run b{color:#f5f0e6;font-weight:900}
R .legend{left:140px;top:510px;width:1640px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px 30px}
R .lg{display:flex;align-items:center;gap:16px;font-weight:800;font-size:32px;padding:14px 22px;border-radius:16px;background:rgba(16,48,77,.85)}
R .lg i{display:block;width:26px;height:26px;border-radius:7px;flex:none}
R .lg .v{margin-left:auto;font-size:34px}
R .inc{left:140px;top:720px;display:flex;gap:18px}
R .inc .chip{position:relative}
R .nx{right:140px;top:262px;font-weight:800;font-size:30px;padding:8px 22px;border-radius:12px;background:rgba(245,240,230,.12);border:2px solid rgba(245,240,230,.3)}
R .p2{position:absolute;inset:0}
R .k2{width:780px;top:180px;height:310px;padding:38px 44px}
R #s05-k1{left:130px}
R #s05-k2{left:1010px}
R .k2 .big{font-weight:900;font-size:56px;margin-top:26px;line-height:1.2}
R .k2 .s{font-weight:700;font-size:30px;margin-top:16px;opacity:.85}
R .stp{position:absolute;padding:14px 34px;border:8px solid #d8473d;border-radius:18px;color:#d8473d;font-weight:900;font-size:58px;white-space:nowrap;background:rgba(245,240,230,.92);box-shadow:0 10px 30px rgba(0,0,0,.35)}
R .free{left:130px;top:650px;width:1660px;height:120px;padding:0 44px;display:flex;align-items:center;gap:22px;font-weight:800;font-size:36px}
R .free .tag{margin-left:auto;font-weight:900;font-size:52px;color:#2fb5a5}
R .opt{left:130px;top:792px;font-size:30px}
"""
    body = f"""<div class="p2a" id="s05-p1" style="position:absolute;inset:0">
<div class="abs kick" id="s05-kick">NISEP 2026-27 · CAD</div>
<div class="abs h title" id="s05-title">NISEP 1년 비용</div>
<div class="abs tot" id="s05-tot"><div class="l">1년 합계 (캐나다 달러)</div><div class="v num"><small>$</small><span id="s05-tv">0</span></div></div>
<div class="abs nx" id="s05-nx">2027-28학년도 <b class="gold">$22,450</b> · 홈스테이 인상분 반영</div>
<div class="abs bar" id="s05-bar">{segs}<div class="sweep" id="s05-sw"></div></div>
<div class="abs run" id="s05-run">항목 합계 <b>$<span id="s05-rv">0</span></b></div>
<div class="abs legend">{leg}</div>
<div class="abs inc" id="s05-inc"><span class="chip cream"><span class="tick"></span>공항 픽업 포함</span>
<span class="chip cream"><span class="tick"></span>법적 보호자: NISEP 디렉터</span><span class="chip teal">별도 가디언 비용 없음</span></div>
</div>
<div class="p2" id="s05-p2">
<div class="dcard k2" id="s05-k1"><span class="pill ns">NSISP</span><div class="big">공식 홈페이지<br>금액 미공개</div><div class="s">유학원마다 안내 금액이 다를 수 있음</div></div>
<div class="card k2" id="s05-k2"><span class="pill nl">NISEP</span><div class="big" style="color:#0b1f33">공식 가격표 공개</div><div class="s">AA Canada는 이 금액 그대로 안내</div></div>
<div class="stp" id="s05-st1" style="left:1300px;top:130px">공식 가격표 그대로</div>
<div class="stp" id="s05-st2" style="left:1460px;top:512px">수속비 0원</div>
<div class="dcard free" id="s05-fr"><span class="tick"></span>입학 수속 · 학생비자 신청 · 출국 준비<span class="tag">무료</span></div>
<div class="chip opt" id="s05-opt">선택 사항: 학부모 관리 프로그램 · 금액 미리 공개</div>
</div>"""
    js = [J("inn", "#s05-kick", 0.3, y=10), J("kin", "#s05-title", 0.4),
          J("inn", "#s05-bar", T("1년 비용"), y=0, s=0.98),
          J("inn", "#s05-tot", T("1년 비용"), x=40, y=0),
          J("count", "#s05-tv", T("21,950"), a=0, b=21950, d=1.6),
          J("pulse", "#s05-tot", T("21,950") + 1.6, s=1.06),
          J("inn", "#s05-run", T("학비 9") - 0.2, y=10)]
    run = 0
    for i, (k, (n, v, c)) in enumerate(zip(keys, items)):
        t = T(k)
        js += [J("grow", f"#s05-g{i}", t, d=0.7), J("pop", f"#s05-l{i}", t, s=0.7, st=0),
               J("count", "#s05-rv", t, a=run, b=run + v, d=0.7)]
        run += v
    t_all = T("모두 들어간")
    js += [J("sweep", "#s05-sw", t_all), J("pulse", "#s05-run", t_all + 0.2, s=1.1),
           J("pop", "#s05-inc .chip:nth-child(1)", T("공항 픽업"), st=0),
           J("pop", "#s05-inc .chip:nth-child(2)", T("법적 보호자"), st=0),
           J("pop", "#s05-inc .chip:nth-child(3)", T("가디언 비용"), st=0),
           J("inn", "#s05-nx", T("2027-28"), y=-14),
           J("pulse", "#s05-nx", T("22,450"), s=1.08)]
    t2 = T("NSISP는 공식")
    js += [J("out", "#s05-p1", t2 - 0.5, y=-40, d=0.5),
           J("inn", "#s05-k1", t2, x=-50, y=0),
           J("inn", "#s05-k1 .s", T("그래서 유학원"), y=10),
           J("inn", "#s05-k2", T("NISEP은 공식"), x=50, y=0),
           J("stamp", "#s05-st1", T("그대로 안내"), r=-8),
           J("stamp", "#s05-st2", T("붙이지 않습니다"), r=6),
           J("inn", "#s05-fr", T("입학 수속"), y=24),
           J("pop", "#s05-fr .tag", T("무료이고"), s=1.8, st=0),
           J("inn", "#s05-opt", T("추가 비용은"), y=16),
           J("pulse", "#s05-opt", T("미리 공개"), s=1.06)]
    return css, body, js


# ------------------------------------------------------------------ S6 homestay checklist
def s06(T, D):
    rows = [("지원서 → 인터뷰 → 가정 방문 후 선발", "지원서"),
            ("18세 이상 가족 전원 범죄경력조회", "18세 이상"),
            ("범죄경력조회 3년마다 다시", "3년마다"),
            ("2년마다 자진 신고서 제출", "2년마다"),
            ("한 집에 같은 모국어 유학생은 1명", "한 집에"),
            ("가족 모두 영어가 모국어", "가족은 모두 영어"),
            ("학생 또래 이성 가족이 없는 집 배정", "학생 또래"),
            ("문제 시 코디네이터 미팅 · 홈스테이 변경은 마지막 단계", "문제가 생기면")]
    lst = "".join(f'<div class="ck" id="s06-r{i}" style="top:{214 + i * 76}px"><span class="bx"><svg viewBox="0 0 40 40" width="40" height="40">'
                  f'<path class="cm" d="M8 21 L17 30 L33 11" fill="none" stroke="#07131f" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
                  f'<span class="tx">{t}</span></div>' for i, (t, _) in enumerate(rows))
    css = """
R .ck{position:absolute;left:120px;width:1080px;height:64px;display:flex;align-items:center;gap:22px;font-weight:800;font-size:33px;color:rgba(245,240,230,.38)}
R .ck .bx{display:block;width:48px;height:48px;border-radius:12px;border:3px solid rgba(245,240,230,.4);display:flex;align-items:center;justify-content:center;flex:none}
R .ck.lit{color:#f5f0e6}
R .ck .bx .bf{position:absolute}
R .house{left:1300px;top:230px}
R .shd{left:1530px;top:420px}
R .nsc{left:1250px;top:240px;width:560px;padding:36px 40px}
R .nsc .big{font-weight:900;font-size:110px;line-height:1;margin-top:24px}
R .nsc .big small{font-size:40px;margin:0 10px}
R .nsc .s{font-weight:800;font-size:32px;margin-top:16px}
R .nsc .s2{font-weight:700;font-size:28px;margin-top:12px;opacity:.8}
"""
    body = f"""<div class="abs kick" id="s06-kick">NISEP HOMESTAY</div>
<div class="abs h title" id="s06-title">홈스테이, 이렇게 관리합니다</div>
{lst}
<div class="abs house" id="s06-house">{HOUSE.format(w=420, h=364)}</div>
<div class="abs shd" id="s06-shd">{SHIELD.format(w=150, h=180)}</div>
<div class="dcard nsc" id="s06-ns"><span class="pill ns">NSISP</span><div class="s">홈스테이 직접 운영</div>
<div class="big ns-c num">20<small>:</small>1</div><div class="s">학생 20명당 코디네이터 1명</div><div class="s2">가까운 거리에서 관리</div></div>"""
    js = [J("inn", "#s06-kick", 0.3, y=10), J("kin", "#s06-title", 0.4),
          J("inn", ".ck", 0.9, x=-30, y=0, st=0.06, d=0.5),
          J("draw", "#s06-house .hs", 1.0, d=1.6, st=0.25),
          J("pop", "#s06-shd", T("선발") + 0.2, st=0)]
    for i, (_, k) in enumerate(rows):
        t = T(k)
        js += [J("fromto", f"#s06-r{i} .bx", t, f={"backgroundColor": "rgba(47,181,165,0)", "borderColor": "rgba(245,240,230,.4)"},
                 t={"backgroundColor": "#2fb5a5", "borderColor": "#2fb5a5", "duration": 0.25}),
               J("draw", f"#s06-r{i} .cm", t + 0.1, d=0.35),
               J("fromto", f"#s06-r{i}", t, f={"color": "rgba(245,240,230,.38)"}, t={"color": "#f5f0e6", "duration": 0.3}),
               J("pulse", f"#s06-r{i} .bx", t + 0.1, s=1.2)]
    t_ns = T("NSISP도")
    js += [J("pulse", "#s06-shd", T("한 명만"), s=1.12),
           J("out", "#s06-house, #s06-shd", t_ns - 0.4, x=80, d=0.4),
           J("inn", "#s06-ns", t_ns, x=60, y=0),
           J("count", "#s06-ns .big", T("20명당"), a=0, b=20, d=0.8, suf=" : 1")]
    return css, body, js


# ------------------------------------------------------------------ S7 diploma timeline + university
def s07(T, D):
    X0, YR = 520, 560  # x of year 0, px per year
    css = f"""
R .lane{{position:absolute;left:120px;height:96px;display:flex;align-items:center}}
R .lane .nm{{width:380px;font-weight:900;font-size:36px;line-height:1.15}}
R .lane .nm small{{display:block;font-weight:700;font-size:24px;opacity:.75}}
R .tb{{position:absolute;left:{X0}px;height:72px;border-radius:0 36px 36px 0;display:flex;align-items:center;justify-content:flex-end;padding-right:30px;font-weight:900;font-size:40px;color:#07131f}}
R .axis{{position:absolute;left:{X0}px;top:470px;width:{YR * 2 + 60}px;height:4px;background:rgba(245,240,230,.4)}}
R .tk{{position:absolute;top:452px;width:4px;height:40px;background:rgba(245,240,230,.6)}}
R .tl2{{position:absolute;top:500px;font-weight:800;font-size:28px;color:rgba(245,240,230,.8);transform:translateX(-50%)}}
R .uni{{left:120px;top:560px;width:1680px;height:270px;padding:30px 44px}}
R .uni .hd{{font-weight:900;font-size:40px;color:#0b1f33}}
R .uni .hd small{{font-weight:700;font-size:26px;color:#3a5670;margin-left:16px}}
R .uni .r{{display:flex;align-items:center;gap:22px;margin-top:22px;font-weight:800;font-size:34px;color:#0b1f33}}
R .uni .r .pill{{font-size:26px;padding:6px 20px}}
R .uni .r b{{font-weight:900}}
"""
    body = f"""<div class="abs kick" id="s07-kick">DIPLOMA</div>
<div class="abs h title" id="s07-title">졸업장까지 필요한 기간</div>
<div class="lane" style="top:232px" id="s07-a"><div class="nm ns-c">노바스코샤 졸업장<small>NSISP</small></div></div>
<div class="tb" id="s07-b1" style="top:244px;width:{YR}px;background:#4aa3df">최소 1년</div>
<div class="lane" style="top:350px" id="s07-b"><div class="nm nl-c">뉴펀들랜드 졸업장<small>NISEP</small></div></div>
<div class="tb" id="s07-b2" style="top:362px;width:{YR * 2}px;background:#f2a33a">최소 2년</div>
<div class="axis" id="s07-ax"></div>
{"".join(f'<div class="tk s07-tk" style="left:{X0 + i * YR - 2}px"></div><div class="tl2 s07-tk" style="left:{X0 + i * YR}px">{lab}</div>' for i, lab in enumerate(["0", "1년", "2년"]))}
<div class="card uni" id="s07-u"><div class="hd">세인트메리스 대학교<small>Saint Mary's University · 노바스코샤</small></div>
<div class="r" id="s07-u1"><span class="pill ns">NSISP 졸업생</span>캐나다 <b>국내 학생 수준</b> 학비 적용</div>
<div class="r" id="s07-u2"><span class="pill nl">NISEP 졸업생</span>과목당 <b>$1,000</b> 학비 감면 <span style="font-weight:700;font-size:26px;color:#3a5670">(2026-27학년도부터)</span></div></div>"""
    js = [J("inn", "#s07-kick", 0.3, y=10), J("kin", "#s07-title", 0.4),
          J("grow", "#s07-ax", 1.0, d=0.8), J("inn", ".s07-tk", 1.3, y=10, st=0.08),
          J("inn", "#s07-a", T("노바스코샤 고등학교") - 0.2, x=-30, y=0),
          J("grow", "#s07-b1", T("최소 1년"), d=0.9),
          J("inn", "#s07-b", T("뉴펀들랜드 졸업장") - 0.2, x=-30, y=0),
          J("grow", "#s07-b2", T("최소 2년"), d=1.3),
          J("pulse", "#s07-b1, #s07-b2", T("그 주에서"), s=1.04, st=0.2),
          J("inn", "#s07-u", T("대학 혜택"), y=40),
          J("inn", "#s07-u1", T("NSISP 졸업생"), x=-30, y=0),
          J("inn", "#s07-u2", T("같은 대학교"), x=-30, y=0),
          J("pulse", "#s07-u2 b", T("1,000달러"), s=1.15)]
    return css, body, js


# ------------------------------------------------------------------ S8 fork
def s08(T, D):
    css = """
R .me{left:150px;top:390px;width:250px;height:250px;border-radius:50%;background:#f5f0e6;color:#0b1f33;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:44px;box-shadow:0 0 0 14px rgba(245,240,230,.12)}
R .fork{left:0;top:0;width:1920px;height:1080px}
R .opt{left:930px;width:860px;padding:30px 40px}
R #s08-A{top:150px}
R #s08-B{top:560px}
R .opt .li{display:flex;align-items:center;gap:18px;font-weight:800;font-size:32px;margin-top:16px}
R .opt .vd{position:absolute;right:30px;top:26px;font-weight:900;font-size:28px;padding:8px 22px;border-radius:99px}
R .ban{left:0;right:0;top:800px;text-align:center}
R .ban span{display:inline-block;padding:14px 40px;border-radius:99px;background:rgba(47,181,165,.18);border:2px solid #2fb5a5;font-weight:800;font-size:34px}
"""
    body = f"""<div class="abs kick" id="s08-kick">SUMMARY</div>
<div class="abs h title" id="s08-title">우리 아이에게 맞는 곳은?</div>
<svg class="abs fork" viewBox="0 0 1920 1080"><path id="s08-pa" d="M400 515 C640 515 680 290 920 290" fill="none" stroke="#f2a33a" stroke-width="12" stroke-linecap="round"/>
<path id="s08-pb" d="M400 515 C640 515 680 660 920 660" fill="none" stroke="#4aa3df" stroke-width="12" stroke-linecap="round"/></svg>
<div class="abs me" id="s08-me">{PERSON.format(w=50, h=80, c="#0b1f33")}<span>우리 아이</span></div>
<div class="dcard opt" id="s08-A" style="border-color:#f2a33a"><span class="pill nl">NISEP</span><span class="vd" id="s08-Av" style="background:#f2a33a;color:#07131f">함께 보세요</span>
<div class="li" id="s08-A1"><span class="tick"></span>학교를 직접 고르고 싶다</div>
<div class="li" id="s08-A2"><span class="tick"></span>유학생이 적은 작은 학교</div>
<div class="li" id="s08-A3"><span class="tick"></span>2년 이상 지낼 계획</div></div>
<div class="dcard opt" id="s08-B" style="border-color:#4aa3df"><span class="pill ns">NSISP</span><span class="vd" id="s08-Bv" style="background:#4aa3df;color:#07131f">일정이 잘 맞음</span>
<div class="li" id="s08-B1"><span class="tick"></span>1년 안에 졸업장을 받는 계획</div></div>
<div class="abs ban" id="s08-ban"><span>두 곳 모두 · 주 프로그램이 학교와 홈스테이를 함께 관리</span></div>"""
    js = [J("inn", "#s08-kick", 0.3, y=10), J("kin", "#s08-title", 0.4),
          J("pop", "#s08-me", 0.9, st=0),
          J("draw", "#s08-pa", T("학교를 직접") - 0.3, d=0.8),
          J("inn", "#s08-A", T("학교를 직접"), x=40, y=0),
          J("inn", "#s08-A1", T("학교를 직접") + 0.3, x=-20, y=0),
          J("inn", "#s08-A2", T("유학생이 적은"), x=-20, y=0),
          J("inn", "#s08-A3", T("2년 이상"), x=-20, y=0),
          J("pop", "#s08-Av", T("함께 보세요"), st=0),
          J("draw", "#s08-pb", T("1년 안에") - 0.3, d=0.8),
          J("inn", "#s08-B", T("1년 안에"), x=40, y=0),
          J("inn", "#s08-B1", T("1년 안에") + 0.3, x=-20, y=0),
          J("pop", "#s08-Bv", T("일정이 잘"), st=0),
          J("inn", "#s08-ban", T("어느 쪽이든"), y=20),
          J("pulse", "#s08-A, #s08-B", T("안정적인"), s=1.03, st=0.12)]
    return css, body, js


# ------------------------------------------------------------------ S9 overlay (face)
def s09(T, D):
    css = """
R .lt{left:96px;top:700px;padding:18px 36px 22px;border-radius:26px;background:rgba(7,19,31,.84);border-left:12px solid #2fb5a5;box-shadow:0 20px 40px rgba(0,0,0,.35)}
R .lt .k{display:inline-block;font-weight:900;font-size:30px;padding:6px 20px;border-radius:99px;background:#2fb5a5;color:#07131f}
R .lt .t{font-weight:900;font-size:54px;letter-spacing:-.01em;margin-top:12px;white-space:nowrap}
R .lt .t i{font-style:normal;color:rgba(245,240,230,.5);margin:0 18px}
R .sem{left:96px;top:620px;font-size:28px}
"""
    body = """<div class="chip cream sem" id="s09-sem">2027년 2월 · 9월 학기 모집 중</div>
<div class="abs lt" id="s09-lt"><span class="k">무료 상담</span><div class="t">aacanada.co.kr<i>/</i>02-567-4345</div></div>"""
    js = [J("inn", "#s09-lt", 1.0, x=-60, y=0, d=0.8),
          J("pulse", "#s09-lt .k", T("무료로"), s=1.12),
          J("pop", "#s09-sem", T("2027년"), st=0)]
    return css, body, js


# ------------------------------------------------------------------ end card
def endcard(T, D):
    css = """
R .lg{left:50%;top:170px;width:300px;height:290px;margin-left:-150px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.4)}
R .lg img{width:277px;height:268px}
R .t1{left:0;right:0;top:520px;text-align:center;font-weight:900;font-size:64px}
R .t2{left:0;right:0;top:620px;text-align:center;font-weight:800;font-size:48px;color:#2fb5a5}
R .t3{left:0;right:0;top:710px;text-align:center;font-weight:700;font-size:32px;color:rgba(245,240,230,.75)}
"""
    body = """<div class="abs lg" id="ec-lg"><img src="assets/img/aa-canada-logo-transparent.png" alt="AA Canada"></div>
<div class="abs t1" id="ec-t1">무료 상담</div>
<div class="abs t2" id="ec-t2">aacanada.co.kr  ·  02-567-4345</div>
<div class="abs t3" id="ec-t3">NSISP · NISEP 캐나다 공립 조기유학</div>"""
    js = [J("pop", "#ec-lg", 0.45, st=0, s=0.6), J("inn", "#ec-t1, #ec-t2, #ec-t3", 0.7, y=24, st=0.15)]
    return css, body, js


SCENES = {1: s01, 2: s02, 3: s03, 4: s04, 5: s05, 6: s06, 7: s07, 8: s08, 9: s09}
