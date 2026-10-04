"""Scenes 1–8: hook, agenda, chapter 1 (Work permit / LMIA), chapter 2 (LMIA hurdles)."""
from kit import build

# ---------------------------------------------------------------- 01 hook
build(1, 0, "WORK PERMIT", css="""
#§q { position: absolute; left: 120px; top: 150px; width: 1680px; font-size: 92px; }
#§q .sm { display:block; font-family:"IBM Plex Sans KR"; font-weight:700; font-size:40px; letter-spacing:0; margin-bottom:18px; }
#§cardA, #§cardB { top: 430px; width: 560px; height: 300px; padding: 44px 48px; }
#§cardA { left: 160px; }
#§cardB { left: 1200px; background: #C8102E; color: #FBF8F2; }
#§cardA .t, #§cardB .t { font-family:"Black Han Sans"; font-size: 88px; line-height:1; }
#§cardA .e, #§cardB .e { font-family:"Space Mono"; font-weight:700; font-size: 28px; margin-top: 22px; letter-spacing:.06em; }
#§vs { position:absolute; left: 860px; top: 520px; width: 200px; text-align:center; font-family:"Black Han Sans"; font-size: 80px; }
#§crowd { position:absolute; left: 820px; top: 790px; width: 360px; height: 60px; }
#§crowd i { position:absolute; top:0; width:44px; height:44px; border-radius:50%; background:#1E1C24; }
#§wall { position:absolute; left: 1060px; top: 120px; width: 820px; height: 760px; background:#1E1C24; color:#F4EFE6;
  display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow: 0 30px 0 rgba(30,28,36,.18); }
#§wall .big { font-family:"Black Han Sans"; font-size: 300px; line-height: .9; letter-spacing: .02em; }
#§wall .bricks { position:absolute; inset: 0; background-image:
  linear-gradient(rgba(244,239,230,.10) 3px, transparent 3px), linear-gradient(90deg, rgba(244,239,230,.10) 3px, transparent 3px);
  background-size: 160px 80px; }
#§wall .full { font-family:"Space Mono"; font-weight:700; font-size: 30px; letter-spacing:.04em; margin-top: 26px; color:#F4EFE6; }
#§wall .ko { font-size: 38px; font-weight: 700; margin-top: 14px; color:#F4EFE6; }
""", html="""
  <h1 id="§q" class="hl"><span class="sm muted">캐나다에 간다면, 하나만 고르세요</span>학생비자 <span class="red">vs</span> 취업비자?</h1>
  <div id="§cardA" class="card"><div class="t">학생비자</div><div class="e">STUDY PERMIT</div></div>
  <div id="§vs" class="red">VS</div>
  <div id="§cardB" class="card"><div class="t">취업비자</div><div class="e">WORK PERMIT</div></div>
  <div id="§crowd"><i style="left:0"></i><i style="left:62px"></i><i style="left:124px"></i><i style="left:186px"></i><i style="left:248px"></i><i style="left:310px"></i></div>
  <div id="§wall"><div class="bricks"></div><div class="big">LMIA</div>
    <div class="full">LABOUR MARKET IMPACT ASSESSMENT</div><div class="ko">노동시장영향평가</div></div>
""", js="""
up("#§q", 0.3, 0.7);
left("#§cardA", 1.2); pop("#§vs", 1.6); right("#§cardB", 1.9);
// 5.2 most people choose work permit
tl.to("#§cardB", { scale: 1.08, duration: 0.5, ease: E.b }, 5.2);
dim("#§cardA", 5.2, 0.35);
stag("#§crowd i", 5.5, 0.08, 20);
tl.to("#§crowd i", { x: 420, duration: 2.6, ease: "power1.inOut", stagger: 0.08 }, 6.1);
// 8.4 the wall
tl.fromTo("#§wall", { y: -1000 }, { y: 0, duration: 0.55, ease: "bounce.out" }, 8.4);
tl.fromTo("#§wall .big", { scale: 1.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: E.o }, 8.9);
tl.to("#§crowd i", { x: 230, duration: 0.4, ease: "power2.out", stagger: 0.03 }, 8.9);
tl.to("#§cardB", { opacity: 0, duration: 0.15 }, 8.75);
// 13.0 spell it out
up("#§wall .full", 12.9, 0.5, 24); up("#§wall .ko", 13.3, 0.5, 24);
""", glow=(1000, 200))

# ---------------------------------------------------------------- 02 agenda
build(2, 0, "TODAY", css="""
#§h { position:absolute; left:120px; top:170px; font-size: 120px; }
#§h .k { display:block; font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.12em; color:#C8102E; margin-bottom: 20px; }
#§list { position:absolute; left: 820px; top: 210px; width: 980px; }
.§row { display:flex; align-items:flex-start; gap: 40px; padding: 34px 0; position:relative; }
.§row .n { font-family:"Black Han Sans"; font-size: 120px; line-height: .9; width: 130px; color:#C8102E; }
.§row .t { font-size: 50px; font-weight: 700; line-height: 1.25; padding-top: 10px; }
.§row .t small { display:block; font-size: 32px; font-weight: 400; color:#6A645C; margin-top: 8px; }
.§row .rule { position:absolute; left:0; right:0; bottom:0; }
""", html="""
  <h1 id="§h" class="hl"><span class="k">TODAY'S ROADMAP</span>오늘의<br>내용</h1>
  <div id="§list">
    <div class="§row" id="§r1"><div class="n">1</div><div class="t">Work permit과 LMIA<small>캐나다 취업의 첫 번째 벽</small></div><span class="rule"></span></div>
    <div class="§row" id="§r2"><div class="n">2</div><div class="t">LMIA를 피하는 두 가지 방법<small>PGWP · Francophone Mobility</small></div><span class="rule"></span></div>
    <div class="§row" id="§r3"><div class="n">3</div><div class="t">불어 레벨별 영주권 로드맵<small>취업비자에서 영주권까지</small></div><span class="rule"></span></div>
  </div>
""", js="""
up("#§h", 0.3, 0.7);
const T = [4.5, 7.2, 9.9];
[1,2,3].forEach((k, i) => {
  draw("#§r" + k + " .rule", T[i] - 0.2, 0.6);
  pop("#§r" + k + " .n", T[i]);
  left("#§r" + k + " .t", T[i] + 0.15);
});
tl.to("#§r1, #§r2", { opacity: 0.45, duration: 0.5 }, 11.2);
tl.to("#§r3", { x: 20, duration: 0.5, ease: E.o }, 11.2);
""", glow=(-200, 300))

# ---------------------------------------------------------------- 03 chapter 1
build(3, 1, "LMIA", css="""
#§cc { position:absolute; left:120px; top:160px; }
#§cc .k { font-family:"Space Mono"; font-weight:700; font-size: 30px; letter-spacing:.14em; color:#C8102E; }
#§cc h1 { font-size: 110px; margin-top: 14px; }
#§f1, #§f2 { position:absolute; left: 120px; width: 1680px; display:flex; align-items:center; gap: 40px; }
#§f1 { top: 520px; } #§f2 { top: 740px; }
.§box { font-size: 52px; font-weight: 700; padding: 26px 40px; border: 4px solid #1E1C24; background:#FBF8F2; white-space:nowrap; }
.§box.red { background:#C8102E; color:#FBF8F2; border-color:#C8102E; }
.§box.ink { background:#1E1C24; color:#F4EFE6; }
.§arr { font-family:"Black Han Sans"; font-size: 80px; color:#1E1C24; }
#§mark { position:relative; display:inline-block; }
#§mark::after { content:""; }
#§ul { position:absolute; left: 0; right: 0; bottom: -6px; height: 14px; background: rgba(200,16,46,.35); transform-origin:left center; }
""", html="""
  <div id="§cc"><div class="k">CHAPTER 1</div><h1 class="hl">Work permit과 LMIA</h1></div>
  <div id="§f1"><div class="§box">캐나다에서 일하려면</div><div class="§arr">→</div><div class="§box red">Work Permit (취업비자)</div></div>
  <div id="§f2"><div class="§box red">Work Permit</div><div class="§arr">→</div>
    <div class="§box ink"><span id="§mark">원칙적으로<span id="§ul"></span></span> LMIA 필요</div></div>
""", js="""
left("#§cc .k", 0.2); up("#§cc h1", 0.4, 0.7);
const T1 = 2.5, T2 = 7.6;
left("#§f1 .§box:nth-child(1)", T1); fade("#§f1 .§arr", T1 + 0.4); pop("#§f1 .§box.red", T1 + 0.7);
left("#§f2 .§box:nth-child(1)", T2); fade("#§f2 .§arr", T2 + 0.4); pop("#§f2 .§box.ink", T2 + 0.7);
draw("#§ul", T2 + 1.6, 0.6);
""", glow=(1100, 400))

# ---------------------------------------------------------------- 04 chef analogy
build(4, 1, "SEOUL", css="""
#§stage { position:absolute; left:120px; top:150px; width: 1000px; height: 780px; border: 4px solid #1E1C24; background:#FBF8F2; }
#§stage .lab { position:absolute; left: 30px; top: 22px; font-family:"Space Mono"; font-weight:700; font-size: 24px; letter-spacing:.1em; }
#§rest { position:absolute; left: 40px; top: 90px; display:flex; gap: 22px; }
#§rest div { width: 132px; height: 110px; border: 4px solid #1E1C24; background:#F4EFE6; position: relative; }
#§rest div::before { content:""; position:absolute; left: 10px; right:10px; top:-4px; height: 26px; background:
  repeating-linear-gradient(90deg, #C8102E 0 22px, #FBF8F2 22px 44px); border: 4px solid #1E1C24; top: -28px; }
#§chefs { position:absolute; left: 40px; top: 300px; width: 900px; height: 200px; }
.§chef { position:absolute; width: 66px; height: 110px; }
.§chef .h { position:absolute; left: 13px; top: 0; width: 40px; height: 30px; background:#FBF8F2; border: 4px solid #1E1C24; border-radius: 14px 14px 4px 4px; }
.§chef .f { position:absolute; left: 13px; top: 30px; width: 40px; height: 40px; border-radius:50%; background:#1E1C24; }
.§chef .b { position:absolute; left: 3px; top: 74px; width: 60px; height: 36px; border-radius: 20px 20px 0 0; background:#1E1C24; }
.§chef.fx .f, .§chef.fx .b { background:#C8102E; }
#§pay { position:absolute; left: 40px; top: 560px; width: 920px; }
.§bar { display:flex; align-items:center; gap: 20px; margin-bottom: 18px; font-size: 30px; font-weight:700; }
.§bar .l { width: 170px; }
.§bar .track { flex: 1; height: 44px; position: relative; }
.§bar .fill { position:absolute; left:0; top:0; bottom:0; transform-origin:left center; background:#1E1C24; }
.§bar.fx .fill { background:#C8102E; }
.§bar .v { width: 110px; text-align:right; font-family:"Space Mono"; }
#§side { position:absolute; left: 1190px; top: 170px; width: 620px; }
.§cap { position:absolute; left: 0; top: 0; width: 620px; font-size: 52px; font-weight:700; line-height: 1.3; }
.§cap small { display:block; font-size: 32px; font-weight: 400; color:#6A645C; margin-top: 14px; line-height: 1.45; }
#§final { position:absolute; left: 1190px; top: 560px; width: 620px; padding: 36px 40px; background:#1E1C24; color:#F4EFE6; }
#§final .a { font-family:"Black Han Sans"; font-size: 110px; line-height: 1; color:#F4EFE6; }
#§final .b { font-size: 40px; font-weight:700; margin-top: 12px; }
#§final .c { font-family:"Space Mono"; font-size: 22px; letter-spacing:.03em; margin-top: 12px; color:#d8d2c8; }
""", html="""
  <div id="§stage"><div class="lab">SEOUL · 요리사 노동시장</div>
    <div id="§rest"><div></div><div></div><div></div><div></div><div></div><div></div></div>
    <div id="§chefs"></div>
    <div id="§pay">
      <div class="§bar" id="§p1"><div class="l">한국인</div><div class="track"><div class="fill" style="width:100%"></div></div><div class="v">100%</div></div>
      <div class="§bar fx" id="§p2"><div class="l red">외국인</div><div class="track"><div class="fill" style="width:50%"></div></div><div class="v red">50%</div></div>
    </div>
  </div>
  <div id="§side">
    <div class="§cap" id="§c1">자국민의 일자리는<br>보호되어야 합니다<small>어느 나라든 마찬가지예요</small></div>
    <div class="§cap" id="§c2">식당은 한정,<br>요리사는 이미 많다면?<small>서울을 예로 들어볼게요</small></div>
    <div class="§cap" id="§c3">그런데 외국인 요리사가<br><span class="red">계속 들어온다면?</span></div>
    <div class="§cap" id="§c4">월급 <span class="red">절반</span>만 받고도<br>일하겠다고 한다면?</div>
    <div class="§cap" id="§c5">그래서 노동시장 상황에 맞게<br>외국 인력을 <span class="red">조절</span>합니다</div>
  </div>
  <div id="§final"><div class="a">LMIA</div><div class="b">노동시장영향평가</div><div class="c">LABOUR MARKET IMPACT ASSESSMENT</div></div>
""", js="""
// build chef icons (deterministic layout)
const host = document.querySelector("#§chefs");
const pos = [];
for (let i = 0; i < 12; i++) pos.push([ (i % 12) * 74, 0, false ]);
for (let i = 0; i < 5; i++) pos.push([ 140 + i * 150, 120, true ]);
pos.forEach((p, i) => {
  const c = document.createElement("div");
  c.className = "§chef" + (p[2] ? " fx" : "");
  c.id = "§chef" + i;
  c.style.left = p[0] + "px"; c.style.top = (p[1] - 30) + "px";
  c.innerHTML = '<div class="h"></div><div class="f"></div><div class="b"></div>';
  host.appendChild(c);
});
const S = [0, 4.9, 9.6, 13.2, 19.3, 24.2];
fade("#§stage", 0.1, 0.5); left("#§stage .lab", 0.3);
up("#§c1", 0.4);
// 4.9 restaurants limited, chefs many
tl.to("#§c1", { opacity: 0, duration: 0.3 }, S[1] - 0.3);
up("#§c2", S[1]);
stag("#§rest div", S[1] + 0.2, 0.08, 30);
for (let i = 0; i < 12; i++) pop("#§chef" + i, S[1] + 1.2 + i * 0.09, 0.4);
// 9.6 foreigners keep arriving
tl.to("#§c2", { opacity: 0, duration: 0.3 }, S[2] - 0.3);
up("#§c3", S[2]);
for (let i = 12; i < 17; i++) tl.fromTo("#§chef" + i, { opacity: 0, x: 900 }, { opacity: 1, x: 0, duration: 0.8, ease: E.e }, S[2] + 0.4 + (i - 12) * 0.35);
// 13.2 half pay
tl.to("#§c3", { opacity: 0, duration: 0.3 }, S[3] - 0.3);
up("#§c4", S[3]);
fade("#§pay", S[3] + 0.2, 0.3);
draw("#§p1 .fill", S[3] + 0.5, 0.8); draw("#§p2 .fill", S[3] + 1.4, 0.8);
// 19.3 regulate
tl.to("#§c4", { opacity: 0, duration: 0.3 }, S[4] - 0.3);
up("#§c5", S[4]);
dim(".§chef.fx", S[4] + 0.6, 0.35);
// 24.2 that's LMIA
tl.fromTo("#§final", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: E.e }, S[5]);
tl.fromTo("#§final .a", { scale: 0.7 }, { scale: 1, duration: 0.6, ease: E.b }, S[5] + 0.1);
""", glow=(1300, 500))

# ---------------------------------------------------------------- 05 employer applies
build(5, 1, "EMPLOYER", css="""
#§k { position:absolute; left: 120px; top: 160px; font-size: 92px; }
#§k .pt { display:inline-block; background:#C8102E; color:#FBF8F2; padding: 4px 24px; margin-right: 24px; }
#§emp, #§gov { top: 430px; width: 520px; height: 300px; padding: 40px; display:flex; flex-direction:column; justify-content:center; }
#§emp { left: 160px; } #§gov { left: 1240px; background:#1E1C24; color:#F4EFE6; box-shadow: 12px 12px 0 #C8102E; }
#§emp .t, #§gov .t { font-family:"Black Han Sans"; font-size: 84px; line-height:1; }
#§emp .s, #§gov .s { font-size: 30px; margin-top: 16px; }
#§gov .s { font-family:"Space Mono"; font-weight:700; letter-spacing:.03em; color:#e2dccf; }
#§arrow { position:absolute; left: 720px; top: 560px; width: 480px; height: 8px; background:#C8102E; transform-origin:left center; }
#§arrow::after { content:""; position:absolute; right:-6px; top:-18px; border-left: 34px solid #C8102E; border-top: 22px solid transparent; border-bottom: 22px solid transparent; }
#§alab { position:absolute; left: 760px; top: 490px; width: 400px; text-align:center; font-size: 34px; font-weight:700; color:#C8102E; }
#§me { position:absolute; left: 160px; top: 800px; display:flex; align-items:center; gap: 24px; font-size: 36px; font-weight: 700; color:#6A645C; }
#§me .x { font-family:"Black Han Sans"; color:#C8102E; font-size: 44px; }
#§chk { position:absolute; left: 1080px; top: 790px; width: 720px; padding: 26px 34px; border: 4px solid #1E1C24; background:#FBF8F2;
  font-size: 34px; font-weight: 700; line-height: 1.35; }
#§chk .q { color:#C8102E; }
""", html="""
  <h1 id="§k" class="hl"><span class="pt">POINT</span>신청하는 사람은 <span class="red">고용주</span></h1>
  <div id="§emp" class="card"><div class="t">고용주</div><div class="s">나를 채용하려는 회사</div></div>
  <div id="§alab">LMIA 신청</div>
  <div id="§arrow"></div>
  <div id="§gov" class="card"><div class="t">캐나다 정부</div><div class="s">ESDC / SERVICE CANADA</div></div>
  <div id="§me">나 (구직자) <span class="x">✕</span> 직접 신청 불가</div>
  <div id="§chk"><span class="q">사전 검증 ▸</span> 이 외국인을 뽑아도 이 지역, 이 직종의 노동시장에 괜찮을까?</div>
""", js="""
up("#§k", 0.3, 0.7);
const T = 3.3;
left("#§emp", T); draw("#§arrow", T + 0.6, 0.8); fade("#§alab", T + 1.0); right("#§gov", T + 1.3);
up("#§me", T + 3.2);
tl.fromTo("#§chk", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.6, ease: E.e }, 12.0);
tl.fromTo("#§gov", { boxShadow: "12px 12px 0 #C8102E" }, { boxShadow: "22px 22px 0 #C8102E", duration: 0.6, ease: E.s, yoyo: true, repeat: 1 }, 12.4);
""", glow=(1200, -200))

# ---------------------------------------------------------------- 06 chapter 2 checklist
build(6, 2, "1,000 $", css="""
#§cc { position:absolute; left:120px; top:150px; width: 900px; }
#§cc .k { font-family:"Space Mono"; font-weight:700; font-size: 28px; letter-spacing:.14em; color:#C8102E; }
#§cc h1 { font-size: 92px; margin-top: 10px; }
#§cc p { font-size: 36px; color:#6A645C; margin-top: 18px; font-weight: 700; }
#§list { position:absolute; left: 960px; top: 150px; width: 840px; }
.§it { display:flex; align-items:center; gap: 26px; padding: 18px 26px; margin-bottom: 18px; background:#FBF8F2; border: 4px solid #1E1C24; }
.§it .bx { flex: none; width: 52px; height: 52px; border: 4px solid #1E1C24; position:relative; }
.§it .ck { position:absolute; left: 8px; top: -6px; font-family:"Black Han Sans"; font-size: 54px; color:#C8102E; line-height:1; }
.§it .tx { font-size: 34px; font-weight:700; line-height: 1.25; }
.§it .tx em { font-style:normal; color:#C8102E; }
.§it .tx small { display:block; font-size: 26px; font-weight:400; color:#6A645C; }
#§gauge { position:absolute; left: 120px; top: 640px; width: 720px; }
#§gauge .lab { font-family:"Space Mono"; font-weight:700; font-size: 24px; letter-spacing:.1em; margin-bottom: 16px; }
#§gauge .tr { height: 64px; border: 4px solid #1E1C24; background:#FBF8F2; position:relative; }
#§gauge .fl { position:absolute; left:0; top:0; bottom:0; width:100%; background:#C8102E; transform-origin:left center; }
#§gauge .pct { font-family:"Black Han Sans"; font-size: 120px; margin-top: 10px; color:#C8102E; line-height: 1; }
""", html="""
  <div id="§cc"><div class="k">CHAPTER 2</div><h1 class="hl">고용주가 해야 할 일</h1><p>LMIA 한 번을 위해 필요한 것들</p></div>
  <div id="§list">
    <div class="§it" id="§i1"><div class="bx"><span class="ck">✓</span></div><div class="tx">캐나다인 대상 구인광고 <em>4주 이상</em></div></div>
    <div class="§it" id="§i2"><div class="bx"><span class="ck">✓</span></div><div class="tx">신청비 <em id="§fee">$1,000</em> + 컨설턴트 비용<small>보통 수천 달러 추가</small></div></div>
    <div class="§it" id="§i3"><div class="bx"><span class="ck">✓</span></div><div class="tx">지원자가 왜 부적합했는지 설명</div></div>
    <div class="§it" id="§i4"><div class="bx"><span class="ck">✓</span></div><div class="tx">재무제표 · 정규직 고용 이력 제출</div></div>
    <div class="§it" id="§i5"><div class="bx"><span class="ck">✓</span></div><div class="tx">심사 대기 <em>길면 1년 이상</em></div></div>
    <div class="§it" id="§i6"><div class="bx"><span class="ck">✓</span></div><div class="tx">필요하면 정부 담당자 인터뷰</div></div>
  </div>
  <div id="§gauge"><div class="lab">EMPLOYER BURDEN</div><div class="tr"><div class="fl"></div></div><div class="pct" id="§pct">0%</div></div>
""", js="""
left("#§cc .k", 0.2); up("#§cc h1", 0.35, 0.7); up("#§cc p", 0.7);
fade("#§gauge", 1.0);
tl.set("#§gauge .fl", { scaleX: 0 }, 0);
const T = [3.9, 11.0, 17.1, 19.5, 25.1, 30.6];
const P = [15, 35, 52, 68, 86, 100];
T.forEach((t, i) => {
  const k = "#§i" + (i + 1);
  tl.fromTo(k, { opacity: 0, x: 90 }, { opacity: 1, x: 0, duration: 0.55, ease: E.e }, t);
  tl.fromTo(k + " .ck", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: E.b }, t + 0.5);
  tl.to("#§gauge .fl", { scaleX: P[i] / 100, duration: 0.7, ease: E.o }, t + 0.4);
  count("#§pct", t + 0.4, i ? P[i - 1] : 0, P[i], 0.7, v => v + "%");
});
count("#§fee", 11.3, 0, 1000, 1.0, v => "$" + v.toLocaleString("en-US"));
""", glow=(-300, 500))

# ---------------------------------------------------------------- 07 conditions
build(7, 2, "NO", css="""
#§h { position:absolute; left:120px; top:160px; width: 1680px; font-size: 84px; }
#§row { position:absolute; left:120px; top: 430px; width: 1680px; display:flex; gap: 48px; }
.§c { flex: 1; height: 300px; border: 4px solid #1E1C24; background:#FBF8F2; padding: 40px; position:relative; box-shadow: 10px 10px 0 #1E1C24; }
.§c .ic { font-family:"Space Mono"; font-weight:700; font-size: 26px; letter-spacing:.1em; color:#6A645C; }
.§c .t { font-family:"Black Han Sans"; font-size: 72px; margin-top: 26px; }
.§c .ok { position:absolute; right: 30px; top: 26px; font-family:"Black Han Sans"; font-size: 60px; color:#1F4FA0; }
.§c .no { position:absolute; right: 26px; top: 6px; font-family:"Black Han Sans"; font-size: 120px; line-height: 1; color:#C8102E; }
#§stamp { left: 640px; top: 800px; }
""", html="""
  <h1 id="§h" class="hl">조건 중 <span class="red">하나라도</span> 맞지 않으면?</h1>
  <div id="§row">
    <div class="§c" id="§c1"><div class="ic">UNEMPLOYMENT</div><div class="t">지역 실업률</div><div class="ok">✓</div></div>
    <div class="§c" id="§c2"><div class="ic">WAGE</div><div class="t">급여 수준</div><div class="ok">✓</div><div class="no">✕</div></div>
    <div class="§c" id="§c3"><div class="ic">STAFF</div><div class="t">직원 현황</div><div class="ok">✓</div></div>
  </div>
  <div id="§stamp" class="stamp">진행 자체가 불가</div>
""", js="""
up("#§h", 0.25, 0.6);
stag(".§c", 0.8, 0.18, 60);
stag(".§c .ok", 1.8, 0.25, 10);
tl.set("#§c2 .no", { opacity: 0 }, 0);
tl.to("#§c2 .ok", { opacity: 0, duration: 0.2 }, 5.1);
tl.fromTo("#§c2 .no", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power4.in" }, 5.1);
tl.to("#§c1, #§c3", { opacity: 0.35, duration: 0.5 }, 5.6);
tl.to("#§c2", { borderColor: "#C8102E", boxShadow: "10px 10px 0 #C8102E", duration: 0.3 }, 5.4);
slam("#§stamp", 6.2, -4);
""", glow=(500, 300))

# ---------------------------------------------------------------- 08 jobseeker downside
build(8, 2, "CLOSED", css="""
#§h { position:absolute; left:120px; top:150px; width: 1000px; font-size: 76px; }
#§posts { position:absolute; left: 120px; top: 360px; width: 860px; height: 560px; }
.§post { position:absolute; width: 400px; height: 250px; background:#FBF8F2; border: 4px solid #1E1C24; padding: 28px; }
.§post .ti { font-size: 34px; font-weight:700; }
.§post .ln { height: 14px; background: rgba(30,28,36,.16); margin-top: 18px; }
.§post .ln.s { width: 60%; }
.§post .st { position:absolute; left: 30px; top: 120px; border: 6px solid #C8102E; color:#C8102E; font-family:"Space Mono"; font-weight:700;
  font-size: 26px; padding: 6px 14px; background: rgba(251,248,242,.95); white-space:nowrap; }
#§cap { position:absolute; left: 1060px; top: 380px; width: 760px; font-size: 46px; font-weight:700; line-height:1.35; }
#§chain { position:absolute; left: 1060px; top: 560px; width: 760px; height: 360px; }
#§wp { position:absolute; left: 0; top: 40px; width: 300px; padding: 26px; background:#C8102E; color:#FBF8F2; border: 4px solid #1E1C24; }
#§wp .t { font-family:"Black Han Sans"; font-size: 54px; } #§wp .s { font-family:"Space Mono"; font-size: 20px; font-weight:700; margin-top: 8px; }
#§links { position:absolute; left: 300px; top: 100px; width: 160px; height: 20px; display:flex; gap: 4px; }
#§links i { flex:1; border: 6px solid #1E1C24; border-radius: 12px; height: 26px; }
#§boss { position:absolute; left: 460px; top: 40px; width: 300px; padding: 26px; background:#1E1C24; color:#F4EFE6; }
#§boss .t { font-family:"Black Han Sans"; font-size: 54px; } #§boss .s { font-size: 24px; margin-top: 8px; }
#§loop { position:absolute; left: 0; top: 230px; width: 760px; padding: 22px 30px; border: 4px dashed #C8102E; font-size: 31px; font-weight:700; color:#C8102E; }
""", html="""
  <h1 id="§h" class="hl">결국 부담은<br><span class="red">구직자</span>에게 돌아옵니다</h1>
  <div id="§posts">
    <div class="§post" id="§p1" style="left:0; top:0"><div class="ti">Barista · Toronto</div><div class="ln"></div><div class="ln s"></div><div class="st">NO LMIA SUPPORT</div></div>
    <div class="§post" id="§p2" style="left:440px; top:40px"><div class="ti">ECE · Vancouver</div><div class="ln"></div><div class="ln s"></div><div class="st">NO LMIA SUPPORT</div></div>
    <div class="§post" id="§p3" style="left:60px; top:300px"><div class="ti">Cook · London ON</div><div class="ln"></div><div class="ln s"></div><div class="st">NO LMIA SUPPORT</div></div>
    <div class="§post" id="§p4" style="left:480px; top:320px"><div class="ti">Admin · Calgary</div><div class="ln"></div><div class="ln s"></div><div class="st">NO LMIA SUPPORT</div></div>
  </div>
  <div id="§cap"><span id="§cap1">워크퍼밋이 없으면<br>취업 자체가 <span class="red">현실적으로 어렵다</span></span></div>
  <div id="§chain">
    <div id="§wp"><div class="t">취업비자</div><div class="s">EMPLOYER-SPECIFIC</div></div>
    <div id="§links"><i></i><i></i><i></i></div>
    <div id="§boss"><div class="t">고용주 A</div><div class="s">이 회사에서만 근무 가능</div></div>
    <div id="§loop">↻ 이직하려면? 새 고용주와 LMIA를 처음부터 다시</div>
  </div>
""", js="""
up("#§h", 0.25, 0.7);
const T = 3.1;
["#§p1","#§p2","#§p3","#§p4"].forEach((p, i) => {
  tl.fromTo(p, { opacity: 0, y: 50, rotation: i % 2 ? 3 : -3 }, { opacity: 1, y: 0, rotation: i % 2 ? 2 : -2, duration: 0.5, ease: E.o }, T + i * 0.35);
  slam(p + " .st", T + 1.4 + i * 0.45, -8);
});
up("#§cap", 9.0, 0.6);
tl.to("#§cap", { y: -40, opacity: 0.0, duration: 0.4 }, 13.3);
left("#§wp", 13.6); stag("#§links i", 14.1, 0.12, 0); right("#§boss", 14.5);
tl.fromTo("#§loop", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: E.o }, 18.8);
tl.to("#§loop", { x: 12, duration: 0.12, yoyo: true, repeat: 5, ease: "none" }, 19.6);
dim("#§posts", 13.6, 0.4);
""", glow=(1300, 300))
