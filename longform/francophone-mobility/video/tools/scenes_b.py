"""Scenes 9–19: chapter 3 (routes), chapter 4 (Montreal), chapter 5 (levels), summary, CTA."""
from kit import build

# ---------------------------------------------------------------- 09 route 1: PGWP
build(9, 3, "PGWP", css="""
#§cc { position:absolute; left:120px; top:150px; }
#§cc .k { font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.14em; color:#C8102E; }
#§cc h1 { font-size: 100px; margin-top: 10px; }
#§path { position:absolute; left: 120px; top: 520px; width: 1680px; height: 220px; }
#§line { position:absolute; left: 60px; right: 60px; top: 96px; height: 10px; background:#1E1C24; transform-origin:left center; }
.§node { position:absolute; top: 0; width: 360px; text-align:center; }
.§node .dot { width: 120px; height: 120px; margin: 40px auto 0; border-radius: 50%; border: 8px solid #1E1C24; background:#FBF8F2;
  display:flex; align-items:center; justify-content:center; font-family:"Black Han Sans"; font-size: 46px; }
.§node .t { font-size: 40px; font-weight: 700; margin-top: 22px; }
.§node.end .dot { background:#C8102E; color:#FBF8F2; border-color:#C8102E; }
#§n1 { left: 0; } #§n2 { left: 660px; } #§n3 { left: 1320px; }
#§badges { position:absolute; left: 1000px; top: 840px; display:flex; gap: 24px; }
#§badges .chip { background:#1E1C24; color:#F4EFE6; border-color:#1E1C24; }
#§badges .chip.r { background:#C8102E; border-color:#C8102E; color:#FBF8F2; }
#§lab { position:absolute; left: 120px; top: 840px; font-family:"Space Mono"; font-weight:700; font-size: 26px; letter-spacing:.08em; padding-top: 16px; }
""", html="""
  <div id="§cc"><div class="k">CHAPTER 3 · ROUTE 1</div><h1 class="hl">유학 후 <span class="red">PGWP</span></h1></div>
  <div id="§path"><div id="§line"></div>
    <div class="§node" id="§n1"><div class="dot">1</div><div class="t">캐나다 유학</div></div>
    <div class="§node" id="§n2"><div class="dot">2</div><div class="t">졸업</div></div>
    <div class="§node end" id="§n3"><div class="dot">✓</div><div class="t">PGWP 취업비자</div></div>
  </div>
  <div id="§lab">POST-GRADUATION WORK PERMIT</div>
  <div id="§badges"><span class="chip r">LMIA 면제</span><span class="chip">고용주 제한 없는 오픈 워크퍼밋</span></div>
""", js="""
left("#§cc .k", 0.2); up("#§cc h1", 0.4, 0.7);
const T = 4.3;
draw("#§line", T, 2.2);
pop("#§n1", T); pop("#§n2", T + 1.1); pop("#§n3", T + 2.2, 0.7);
fade("#§lab", T + 2.6);
tl.fromTo("#§badges .chip", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: E.b, stagger: 0.5 }, 11.8);
""", glow=(1200, 300))

# ---------------------------------------------------------------- 10 time & cost
build(10, 3, "TIME · COST", css="""
#§h { position:absolute; left:120px; top:160px; font-size: 96px; }
#§a, #§b { top: 420px; width: 780px; height: 440px; padding: 50px; }
#§a { left: 120px; } #§b { left: 1020px; }
.§k { font-family:"Space Mono"; font-weight:700; font-size: 26px; letter-spacing:.1em; color:#6A645C; }
.§big { font-family:"Black Han Sans"; font-size: 180px; line-height: 1; margin-top: 30px; color:#C8102E; }
.§s { font-size: 36px; font-weight:700; margin-top: 20px; }
#§stack { position:absolute; left: 50px; bottom: 50px; right: 50px; display:flex; align-items:flex-end; gap: 22px; height: 210px; }
#§stack div { flex: 1; background:#1E1C24; transform-origin: bottom center; position: relative; }
#§stack div.r { background:#C8102E; }
#§stack span { position:absolute; left: 0; right: 0; top: -46px; text-align:center; font-size: 28px; font-weight:700; color:#1E1C24; }
""", html="""
  <h1 id="§h" class="hl">문제는 <span class="red">시간</span>과 <span class="red">비용</span></h1>
  <div id="§a" class="card"><div class="§k">TIME</div><div class="§big" id="§yr">2년+</div><div class="§s">정규 과정 이수 기간</div></div>
  <div id="§b" class="card"><div class="§k">COST</div>
    <div id="§stack"><div style="height:46%"><span>학비</span></div><div style="height:62%"><span>생활비</span></div><div class="r" style="height:100%"><span>가족 동반</span></div></div></div>
""", js="""
up("#§h", 0.25, 0.6);
left("#§a", 2.1); count("#§yr", 2.4, 0, 2, 0.8, v => v + "년+");
right("#§b", 2.6);
tl.fromTo("#§stack div", { scaleY: 0 }, { scaleY: 1, duration: 0.7, ease: E.o, stagger: 0.35 }, 3.2);
tl.set("#§stack div.r", { scaleY: 0 }, 0);
tl.to("#§stack div.r", { scaleY: 1, duration: 0.8, ease: E.b }, 6.7);
""", glow=(-100, 400))

# ---------------------------------------------------------------- 11 Francophone mobility
build(11, 3, "FRANCOPHONE", css="""
#§cc { position:absolute; left:120px; top:150px; width: 1680px; }
#§cc .k { font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.14em; color:#1F4FA0; }
#§cc h1 { font-size: 104px; margin-top: 10px; }
#§map { position:absolute; left: 120px; top: 440px; width: 1680px; display:flex; gap: 14px; }
.§pv { flex: 1; height: 170px; border: 4px solid #1E1C24; background:#FBF8F2; display:flex; flex-direction:column;
  align-items:center; justify-content:center; font-family:"Space Mono"; font-weight:700; font-size: 38px; position:relative; }
.§pv small { font-family:"IBM Plex Sans KR"; font-size: 20px; font-weight:700; margin-top: 6px; }
.§pv.qc { background:#1F4FA0; color:#FBF8F2; border-color:#1F4FA0; }
.§pv .ex { position:absolute; left: -10px; right: -10px; top: 78px; height: 8px; background:#1E1C24; transform: rotate(-24deg); }
#§eq { position:absolute; left: 120px; top: 700px; display:flex; align-items:center; gap: 30px; }
.§tok { font-size: 46px; font-weight: 700; padding: 20px 34px; border: 4px solid #1E1C24; background:#FBF8F2; white-space:nowrap; }
.§tok.b { background:#1F4FA0; color:#FBF8F2; border-color:#1F4FA0; }
.§tok.r { background:#C8102E; color:#FBF8F2; border-color:#C8102E; }
.§op { font-family:"Black Han Sans"; font-size: 70px; }
#§why { position:absolute; left: 120px; top: 870px; font-size: 36px; font-weight:700; color:#6A645C; }
#§why b { color:#1E1C24; }
""", html="""
  <div id="§cc"><div class="k">ROUTE 2</div><h1 class="hl"><span class="blue">Francophone</span> Mobility</h1></div>
  <div id="§map">
    <div class="§pv" id="§bc">BC<small>밴쿠버</small></div><div class="§pv">AB</div><div class="§pv">SK</div><div class="§pv">MB</div>
    <div class="§pv" id="§on">ON<small>토론토 · 런던</small></div>
    <div class="§pv qc" id="§qc">QC<small>퀘벡 · 제외</small><div class="ex"></div></div>
    <div class="§pv">NB</div><div class="§pv">NS</div><div class="§pv">PE</div><div class="§pv">NL</div>
  </div>
  <div id="§eq"><div class="§tok">퀘벡 밖 영어권 지역</div><div class="§op">+</div><div class="§tok b">불어 가능</div><div class="§op">=</div><div class="§tok r">LMIA 면제</div></div>
  <div id="§why">왜? 퀘벡 밖에서는 <b>불어 가능자가 워낙 적어서</b> 노동시장영향평가가 필요 없다는 것</div>
""", js="""
left("#§cc .k", 0.2); up("#§cc h1", 0.4, 0.7);
stag(".§pv", 4.8, 0.08, 40);
tl.fromTo("#§qc .ex", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, 6.2);
tl.to(".§pv:not(.qc)", { backgroundColor: "#C8102E", color: "#FBF8F2", borderColor: "#C8102E", duration: 0.4, stagger: 0.05 }, 7.0);
tl.fromTo("#§eq > *", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: E.o, stagger: 0.35 }, 10.4);
up("#§why", 14.5);
""", glow=(400, 300))

# ---------------------------------------------------------------- 12 $230 compare
build(12, 3, "$230", css="""
#§L, #§R { top: 150px; width: 820px; height: 470px; padding: 40px 48px; }
#§L { left: 120px; } #§R { left: 980px; border-color:#1F4FA0; box-shadow: 12px 12px 0 #1F4FA0; }
.§k { font-family:"Space Mono"; font-weight:700; font-size: 26px; letter-spacing:.08em; }
#§R .§k { color:#1F4FA0; }
#§L ul { list-style:none; padding:0; margin: 26px 0 0; }
#§L li { font-size: 36px; font-weight: 700; padding: 10px 0; position:relative; }
#§L li .st { position:absolute; left: -6px; right: -6px; top: 34px; height: 6px; background:#C8102E; transform-origin:left center; }
#§R .t { font-size: 40px; font-weight:700; margin-top: 30px; line-height:1.35; }
#§R .big { font-family:"Black Han Sans"; font-size: 200px; line-height: 1; color:#1F4FA0; margin-top: 16px; }
#§quote { position:absolute; left: 120px; top: 680px; width: 1040px; padding: 30px 40px; background:#1E1C24; color:#F4EFE6; }
#§quote .en { font-family:"Space Mono"; font-size: 24px; line-height: 1.5; }
#§quote .ko { font-size: 30px; font-weight:700; margin-top: 16px; line-height: 1.45; color:#F4EFE6; }
#§quote .src { font-family:"Space Mono"; font-size: 18px; color:#cfc8bb; margin-top: 12px; letter-spacing:.06em; }
#§key { position:absolute; left: 1220px; top: 680px; width: 580px; padding: 30px 36px; border: 4px solid #1E1C24; background:#FBF8F2; }
#§key .a { font-size: 40px; font-weight:700; line-height:1.4; }
#§key .a .b { color:#1F4FA0; } #§key .a .r { color:#C8102E; }
""", html="""
  <div id="§L" class="card"><div class="§k">LMIA</div>
    <ul><li>구인광고 8주 이상<span class="st"></span></li><li>신청비 $1,000 + 컨설턴트<span class="st"></span></li>
      <li>길면 1년 이상 심사<span class="st"></span></li><li>복잡한 서류 · 인터뷰<span class="st"></span></li></ul></div>
  <div id="§R" class="card"><div class="§k">FRANCOPHONE MOBILITY</div>
    <div class="t">이민성 고용주 포털에 잡오퍼 등록 +</div><div class="big" id="§fee">$230</div></div>
  <div id="§quote"><div class="en">"…it does not necessarily mean that the worker is required to speak French at work…"</div>
    <div class="ko">실제 근무 중 불어 사용이 필수는 아니며, 불어 근무 환경을 만들 필요도 없다</div>
    <div class="src">— IRCC, EMPLOYER GUIDANCE</div></div>
  <div id="§key"><div class="a">불어는 <span class="b">비자를 위한 열쇠</span>,<br>업무는 <span class="r">영어로</span></div></div>
""", js="""
left("#§L", 0.2); right("#§R", 0.5);
stag("#§L li", 0.8, 0.15, 20);
count("#§fee", 1.2, 0, 230, 1.0, v => "$" + v);
tl.fromTo("#§R .big", { scale: 0.8 }, { scale: 1, duration: 0.6, ease: E.b }, 1.2);
tl.fromTo("#§L li .st", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out", stagger: 0.45 }, 6.2);
tl.to("#§L", { opacity: 0.55, duration: 0.5 }, 8.2);
tl.fromTo("#§quote", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6, ease: E.e }, 10.2);
tl.set("#§quote .ko", { opacity: 0 }, 0);
fade("#§quote .ko", 13.7, 0.6);
tl.fromTo("#§key", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 25.3);
""", glow=(1300, -200))

# ---------------------------------------------------------------- 13 Montreal
build(13, 4, "MONTREAL", css="""
#§k { position:absolute; left:120px; top:150px; font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.14em; color:#1F4FA0; }
#§q { position:absolute; left:120px; top: 200px; font-size: 64px; }
#§city { position:absolute; left:110px; top: 300px; font-family:"Black Han Sans"; font-size: 260px; line-height: 1; color:#1E1C24; letter-spacing:-0.02em; }
#§fear { left: 1100px; top: 340px; transform-origin: center; }
#§fearx { position:absolute; left: 1080px; top: 380px; width: 640px; height: 12px; background:#1E1C24; transform-origin:left center; }
#§bub { position:absolute; left: 120px; top: 640px; width: 1000px; height: 180px; }
.§bb { position:absolute; top: 0; padding: 22px 40px; font-family:"Black Han Sans"; font-size: 72px; border: 4px solid #1E1C24; }
.§bb::after { content:""; position:absolute; left: 50px; bottom: -30px; border-top: 30px solid #1E1C24; border-right: 30px solid transparent; }
#§b1 { left: 0; background:#1F4FA0; color:#FBF8F2; } #§b2 { left: 470px; background:#C8102E; color:#FBF8F2; }
#§both { position:absolute; left: 120px; top: 850px; font-size: 42px; font-weight:700; }
#§tl { position:absolute; left: 1100px; top: 470px; width: 720px; }
.§st { display:flex; gap: 24px; align-items:flex-start; margin-bottom: 26px; }
.§st .d { flex:none; width: 54px; height: 54px; border-radius: 50%; background:#1E1C24; color:#F4EFE6; display:flex; align-items:center; justify-content:center;
  font-family:"Black Han Sans"; font-size: 30px; margin-top: 4px; }
.§st .tx { font-size: 36px; font-weight:700; line-height:1.3; }
.§st .tx small { display:block; font-size: 26px; font-weight:400; color:#6A645C; }
.§st.b .d { background:#1F4FA0; } .§st.r .d { background:#C8102E; }
#§pay { position:absolute; left: 0; right: 0; bottom: 0; height: 170px; background:#1E1C24; color:#F4EFE6; display:flex; align-items:center; padding: 0 120px; }
#§pay .t { font-size: 52px; font-weight:700; }
#§pay .t b { color:#ff8a98; font-weight:700; }
""", html="""
  <div id="§k">CHAPTER 4</div>
  <h1 id="§q" class="hl">불어는 어디서 준비할까?</h1>
  <div id="§city">몬트리올</div>
  <div id="§fear" class="stamp">"불어권이라 부담돼요"</div>
  <div id="§fearx"></div>
  <div id="§bub"><div class="§bb" id="§b1">Bonjour</div><div class="§bb" id="§b2">Hi!</div></div>
  <div id="§both">영어와 불어를 <span class="red">함께</span> 쓰는 도시 · 영어만으로도 생활 가능</div>
  <div id="§tl">
    <div class="§st b" id="§t1"><div class="d">1</div><div class="tx">몬트리올 어학연수 1~2년<small>영어 + 불어 동시에</small></div></div>
    <div class="§st r" id="§t2"><div class="d">2</div><div class="tx">토론토 · 밴쿠버 · 런던 등<small>영어권 지역에서 취업</small></div></div>
    <div class="§st" id="§t3"><div class="d">3</div><div class="tx">LMIA 면제 취업비자로 전환<small>Francophone Mobility</small></div></div>
  </div>
  <div id="§pay"><div class="t">피했던 몬트리올이, 사실은 <b>영어권 취업으로 가는 가장 빠른 길</b></div></div>
""", js="""
left("#§k", 0.2); up("#§q", 0.4, 0.6);
tl.fromTo("#§city", { opacity: 0, y: 80, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: E.e }, 5.3);
slam("#§fear", 10.7, -5);
draw("#§fearx", 12.9, 0.4);
tl.to("#§fear", { opacity: 0.4, duration: 0.4 }, 13.4);
pop("#§b1", 16.7); pop("#§b2", 17.2);
tl.to("#§b1", { y: -14, duration: 1.2, ease: E.s, yoyo: true, repeat: 7 }, 17.9);
tl.to("#§b2", { y: -14, duration: 1.2, ease: E.s, yoyo: true, repeat: 7 }, 18.5);
up("#§both", 18.3);
tl.to("#§fear, #§fearx", { opacity: 0, duration: 0.4 }, 26.0);
left("#§t1", 26.7); left("#§t2", 27.8); left("#§t3", 28.9);
tl.fromTo("#§pay", { yPercent: 100 }, { yPercent: 0, duration: 0.7, ease: E.e }, 31.9);
""", glow=(1200, 100))

# ---------------------------------------------------------------- stairs shared
STAIRS_CSS = """
#§stairs { position:absolute; left: 120px; bottom: 120px; width: 900px; height: 600px; }
.§sp { position:absolute; bottom: 0; width: 300px; background:#E6DFD3; border: 4px solid #1E1C24; display:flex; flex-direction:column;
  justify-content:flex-start; padding: 24px; }
.§sp .lv { font-family:"Black Han Sans"; font-size: 64px; line-height:1; color:#1E1C24; }
.§sp .sk { font-size: 24px; font-weight:700; margin-top: 8px; color:#1E1C24; }
#§sp1 { left: 0; height: 200px; } #§sp2 { left: 300px; height: 360px; } #§sp3 { left: 600px; height: 520px; }
.§sp.on { background:#1F4FA0; border-color:#1F4FA0; }
.§sp.on .lv, .§sp.on .sk { color:#FBF8F2; }
.§sp.done { background:#C9D3E6; }
#§flag { position:absolute; left: 820px; bottom: 520px; width: 8px; height: 150px; background:#1E1C24; }
#§flag i { position:absolute; left: 8px; top: 0; width: 110px; height: 70px; background:#C8102E; }

#§info { position:absolute; left: 1110px; top: 160px; width: 700px; }
#§info .k { font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.12em; color:#1F4FA0; }
#§info h1 { font-size: 70px; margin-top: 12px; }
#§info .res { margin-top: 30px; font-size: 44px; font-weight: 700; padding: 22px 30px; background:#1E1C24; color:#F4EFE6; }
#§info .res b { color:#9fb8e8; }
#§skills { display:flex; gap: 14px; margin-top: 28px; }
#§skills span { flex:1; text-align:center; font-size: 30px; font-weight:700; padding: 14px 0; border: 4px solid #1E1C24; background:#FBF8F2; }
#§skills span.on { background:#1F4FA0; border-color:#1F4FA0; color:#FBF8F2; }
"""


def stairs_html(lit):
    cls = lambda i: "on" if i == lit else ("done" if i < lit else "")
    return f"""
  <div id="§stairs">
    <div class="§sp {cls(1)}" id="§sp1"><div class="lv">NCLC 5</div><div class="sk">말하기 · 듣기</div></div>
    <div class="§sp {cls(2)}" id="§sp2"><div class="lv">NCLC 5</div><div class="sk">네 영역 모두</div></div>
    <div class="§sp {cls(3)}" id="§sp3"><div class="lv">NCLC 7</div><div class="sk">네 영역 모두</div></div>
    {'<div id="§flag"><i></i></div>' if lit == 3 else ''}
  </div>"""


STAIRS_JS = """
tl.fromTo(".§sp", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.5, ease: E.o, stagger: 0.12 }, 0.2);
tl.fromTo(".§sp.on", { scale: 1 }, { scale: 1.05, duration: 0.5, ease: E.b, yoyo: true, repeat: 1, transformOrigin: "bottom center" }, 0.9);
left("#§info .k", 0.4); up("#§info h1", 0.6, 0.6);
"""

# ---------------------------------------------------------------- 14 language levels
build(14, 5, "CLB · NCLC", css="""
#§k { position:absolute; left:120px; top:150px; font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.14em; color:#1F4FA0; }
#§h { position:absolute; left:120px; top:200px; font-size: 92px; }
#§sk { position:absolute; left:120px; top: 380px; display:flex; gap: 22px; }
#§sk div { width: 250px; padding: 24px 0; text-align:center; border: 4px solid #1E1C24; background:#FBF8F2; font-size: 40px; font-weight:700; }
#§scale { position:absolute; left: 120px; top: 560px; width: 1680px; display:flex; gap: 8px; }
#§scale div { flex: 1; height: 90px; border: 3px solid #1E1C24; display:flex; align-items:center; justify-content:center;
  font-family:"Space Mono"; font-weight:700; font-size: 34px; background:#FBF8F2; }
#§scale div.l5 { background:#1F4FA0; color:#FBF8F2; border-color:#1F4FA0; }
#§scale div.l7 { background:#C8102E; color:#FBF8F2; border-color:#C8102E; }
#§names { position:absolute; left: 120px; top: 720px; display:flex; gap: 40px; }
.§nm { padding: 22px 34px; border: 4px solid #1E1C24; font-size: 38px; font-weight:700; background:#FBF8F2; }
.§nm .m { font-family:"Space Mono"; font-weight:700; margin-right: 14px; }
.§nm.fr { border-color:#1F4FA0; color:#1F4FA0; }
#§road { position:absolute; left: 1180px; top: 720px; width: 620px; padding: 26px 34px; background:#1E1C24; color:#F4EFE6; font-size: 40px; font-weight:700; }
""", html="""
  <div id="§k">CHAPTER 5</div>
  <h1 id="§h" class="hl">불어는 <span class="blue">어느 정도</span> 해야 할까?</h1>
  <div id="§sk"><div>말하기</div><div>듣기</div><div>읽기</div><div>쓰기</div></div>
  <div id="§scale"><div>1</div><div>2</div><div>3</div><div>4</div><div class="l5">5</div><div>6</div><div class="l7">7</div><div>8</div><div>9</div><div>10</div><div>11</div><div>12</div></div>
  <div id="§names"><div class="§nm"><span class="m">EN</span>CLB</div><div class="§nm fr"><span class="m">FR</span>NCLC</div></div>
  <div id="§road">→ 레벨별로 열리는 3단계 로드맵</div>
""", js="""
left("#§k", 0.2); up("#§h", 0.4, 0.6);
stag("#§sk div", 2.3, 0.15, 30);
tl.fromTo("#§scale div", { opacity: 0, scaleY: 0.3 }, { opacity: 1, scaleY: 1, duration: 0.35, ease: E.o, stagger: 0.07 }, 3.4);
pop("#§names .§nm:nth-child(1)", 8.1); pop("#§names .§nm:nth-child(2)", 8.6);
tl.fromTo("#§road", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 11.1);
""", glow=(1300, 400))

# ---------------------------------------------------------------- 15 step 1
build(15, 5, "STEP 1", css=STAIRS_CSS + """
#§cefr { display:flex; gap: 20px; margin-top: 26px; }
#§cefr div { flex: 1; padding: 18px 20px; border: 4px solid #1E1C24; background:#FBF8F2; font-size: 30px; font-weight:700; }
#§cefr div .m { display:block; font-family:"Space Mono"; font-size: 20px; color:#6A645C; margin-bottom: 6px; }
#§jobs { display:flex; gap: 14px; margin-top: 26px; flex-wrap: wrap; }
#§jobs .chip { font-size: 30px; }
#§jobs .chip.r { background:#C8102E; color:#FBF8F2; border-color:#C8102E; }
""", html=stairs_html(1) + """
  <div id="§info"><div class="k">STEP 1</div><h1 class="hl">NCLC 5 · 말하기 + 듣기</h1>
    <div class="res" id="§res">→ <b>Francophone Mobility</b><br>LMIA 면제 취업비자</div>
    <div id="§cefr"><div><span class="m">CEFR</span>A2 ~ B1 수준</div><div><span class="m">MONTRÉAL</span>현실적으로 도전 가능</div></div>
    <div id="§jobs"><span class="chip r">유아교육(ECE)</span><span class="chip">취업에 유리한 직종</span></div>
  </div>
""", js=STAIRS_JS + """
tl.fromTo("#§res", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 3.9);
stag("#§cefr div", 9.9, 0.25, 30);
tl.fromTo("#§cefr div:nth-child(2)", { backgroundColor: "#FBF8F2" }, { backgroundColor: "#E6DFD3", duration: 0.5 }, 13.7);
stag("#§jobs .chip", 19.8, 0.3, 30);
""", glow=(-200, 500))

# ---------------------------------------------------------------- 16 step 2
build(16, 5, "STEP 2", css=STAIRS_CSS + """
#§cards { display:flex; flex-direction:column; gap: 18px; margin-top: 26px; }
#§cards div { padding: 20px 26px; border: 4px solid #1E1C24; background:#FBF8F2; font-size: 32px; font-weight:700; line-height:1.35; }
#§cards div .m { display:block; font-family:"Space Mono"; font-size: 20px; color:#1F4FA0; margin-bottom: 4px; }
#§cards div b { color:#C8102E; }
""", html=stairs_html(2) + """
  <div id="§info"><div class="k">STEP 2</div><h1 class="hl">NCLC 5 · 네 영역 모두</h1>
    <div id="§skills"><span class="on">말하기</span><span class="on">듣기</span><span id="§s3">읽기</span><span id="§s4">쓰기</span></div>
    <div class="res" id="§res">→ <b>영주권</b>으로 가는 길이 넓어집니다</div>
    <div id="§cards"><div id="§c1"><span class="m">PROVINCIAL NOMINEE</span>주정부이민 · 불어 가능자 연방 쿼터 <b>5,000명</b></div>
      <div id="§c2"><span class="m">FCIP</span>프랑코폰 커뮤니티 이민 파일럿</div></div>
  </div>
""", js=STAIRS_JS + """
stag("#§skills span", 1.2, 0.12, 20);
tl.to("#§s3, #§s4", { backgroundColor: "#1F4FA0", borderColor: "#1F4FA0", color: "#FBF8F2", duration: 0.35, stagger: 0.3 }, 2.6);
tl.fromTo("#§res", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 5.8);
left("#§c1", 9.1); left("#§c2", 12.6);
""", glow=(-200, 500))

# ---------------------------------------------------------------- 17 step 3
build(17, 5, "STEP 3", css=STAIRS_CSS + """
#§up { margin-top: 26px; display:flex; align-items:center; gap: 22px; font-size: 40px; font-weight:700; }
#§up .ar { font-family:"Black Han Sans"; font-size: 110px; color:#C8102E; line-height: 1; }
""", html=stairs_html(3) + """
  <div id="§info"><div class="k">STEP 3</div><h1 class="hl">NCLC 7 · 네 영역 모두</h1>
    <div id="§skills"><span class="on">말하기</span><span class="on">듣기</span><span class="on">읽기</span><span class="on">쓰기</span></div>
    <div class="res" id="§res">→ 연방 <b>Express Entry</b><br>불어 능력자 카테고리 추첨</div>
    <div id="§up"><span class="ar">↑</span>영주권 가능성이 크게 올라갑니다</div>
  </div>
""", js=STAIRS_JS + """
stag("#§skills span", 1.2, 0.1, 20);
tl.fromTo("#§flag", { scaleY: 0, transformOrigin: "bottom center" }, { scaleY: 1, duration: 0.6, ease: E.b }, 1.4);
tl.fromTo("#§res", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 3.5);
tl.fromTo("#§up", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: E.o }, 9.2);
tl.fromTo("#§up .ar", { y: 30 }, { y: -10, duration: 0.8, ease: E.s, yoyo: true, repeat: 2 }, 9.6);
""", glow=(-200, 500))

# ---------------------------------------------------------------- 18 summary roadmap
build(18, 6, "ROADMAP", css="""
#§h { position:absolute; left:120px; top:150px; font-size: 84px; }
#§grid { position:absolute; left: 120px; top: 300px; width: 1680px; display:grid; grid-template-columns: repeat(3, 1fr); gap: 26px 30px; }
.§n { padding: 26px 30px; border: 4px solid #1E1C24; background:#FBF8F2; min-height: 250px; position:relative; }
.§n .i { font-family:"Space Mono"; font-weight:700; font-size: 24px; color:#6A645C; }
.§n .t { font-family:"Black Han Sans"; font-size: 50px; margin-top: 12px; line-height:1.15; }
.§n .s { font-size: 28px; font-weight:700; margin-top: 12px; color:#6A645C; line-height:1.35; }
.§n.r { background:#C8102E; border-color:#C8102E; color:#FBF8F2; }
.§n.r .i, .§n.r .s { color:#FBF8F2; }
.§n.b { background:#1F4FA0; border-color:#1F4FA0; color:#FBF8F2; }
.§n.b .i, .§n.b .s { color:#FBF8F2; }
.§n.k { background:#1E1C24; border-color:#1E1C24; color:#F4EFE6; }
.§n.k .i, .§n.k .s { color:#e2dccf; }
""", html="""
  <h1 id="§h" class="hl">오늘의 <span class="red">로드맵</span> 정리</h1>
  <div id="§grid">
    <div class="§n" id="§n1"><div class="i">01</div><div class="t">Work permit = LMIA</div><div class="s">워크퍼밋에는 원칙적으로 LMIA 필요</div></div>
    <div class="§n" id="§n2"><div class="i">02</div><div class="t">LMIA는 너무 어렵다</div><div class="s">고용주도 구직자도 부담</div></div>
    <div class="§n" id="§n3"><div class="i">03</div><div class="t">유학 후 PGWP</div><div class="s">가능하지만 시간과 비용 ↑</div></div>
    <div class="§n b" id="§n4"><div class="i">04</div><div class="t">몬트리올 영어 + 불어</div><div class="s">1~2년 어학연수로 함께 준비</div></div>
    <div class="§n r" id="§n5"><div class="i">05</div><div class="t">NCLC 5 → 취업 · PNP · FCIP</div><div class="s">말하기·듣기 5 → Francophone Mobility<br>네 영역 5 → 주정부이민 · FCIP</div></div>
    <div class="§n k" id="§n6"><div class="i">06</div><div class="t">NCLC 7 → Express Entry</div><div class="s">불어 능력자 카테고리 추첨</div></div>
  </div>
""", js="""
up("#§h", 0.2, 0.6);
const T = [0.8, 8.6, 12.8, 17.0, 20.7, 26.5];
T.forEach((t, i) => tl.fromTo("#§n" + (i + 1), { opacity: 0, y: 50, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: E.b }, t));
tl.to("#§n1, #§n2, #§n3", { opacity: 0.5, duration: 0.5 }, 17.0);
""", glow=(700, 300))

# ---------------------------------------------------------------- 19 CTA
build(19, 6, "AA CANADA", css="""
#§logo { position:absolute; left:120px; top:170px; }
#§logo .w { font-family:"Black Han Sans"; font-size: 132px; line-height: .95; }
#§logo .w b { color:#C8102E; font-weight:400; }
#§logo .s { font-size: 40px; font-weight:700; margin-top: 18px; }
#§logo .s span { color:#C8102E; }
#§ct { position:absolute; left: 1040px; top: 180px; width: 760px; }
.§row { display:flex; align-items:center; gap: 24px; padding: 22px 0; border-bottom: 4px solid #1E1C24; }
.§row .m { width: 170px; font-family:"Space Mono"; font-weight:700; font-size: 24px; letter-spacing:.08em; color:#6A645C; }
.§row .v { font-size: 42px; font-weight:700; }
#§night { position:absolute; left: 1040px; top: 660px; padding: 16px 30px; background:#1F4FA0; color:#FBF8F2; font-size: 36px; font-weight:700; }
#§btns { position:absolute; left: 120px; top: 760px; display:flex; gap: 26px; }
.§btn { padding: 26px 48px; font-size: 44px; font-weight:700; border: 4px solid #1E1C24; background:#FBF8F2; }
.§btn.r { background:#C8102E; border-color:#C8102E; color:#FBF8F2; }
#§fadeout { position:absolute; inset: 0; background:#F4EFE6; opacity: 0; }
""", html="""
  <div id="§logo"><div class="w">AA <b>CANADA</b></div><div class="s">몬트리올 현지 직영 · <span>어학연수부터 영주권까지</span></div></div>
  <div id="§ct">
    <div class="§row"><div class="m">TEL</div><div class="v">02-567-4345</div></div>
    <div class="§row"><div class="m">MOBILE</div><div class="v">010-4857-4345</div></div>
    <div class="§row"><div class="m">KAKAO</div><div class="v">canlog</div></div>
    <div class="§row"><div class="m">CAFE</div><div class="v">cafe.naver.com/aamontreal</div></div>
  </div>
  <div id="§night">야간 · 주말 상담 가능</div>
  <div id="§btns"><div class="§btn r">구독</div><div class="§btn">좋아요</div></div>
  <div id="§fadeout"></div>
""", js="""
tl.fromTo("#§logo .w", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.7, ease: E.b }, 0.3);
up("#§logo .s", 1.0);
stag("#§ct .§row", 6.0, 0.25, 30);
pop("#§night", 11.8);
stag("#§btns .§btn", 15.5, 0.3, 40);
tl.to("#§btns .§btn.r", { scale: 1.08, duration: 0.4, ease: E.s, yoyo: true, repeat: 3 }, 16.6);
tl.fromTo("#§fadeout", { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "power1.in" }, D - 1.1);
""", glow=(1000, 200))
