"""Scenes s08-s20 (CH3 diploma, CH4 intake, CH5 management)."""
import math

S = {}

CHECK = '<svg viewBox="0 0 60 60" style="width:{w}px;height:{w}px"><circle cx="30" cy="30" r="28" fill="#2ec27e"/><path class="ck" d="M16 31 L26 41 L45 20" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------------------------------------------------------------- S08 OSSD 3 conditions
S["s08"] = dict(
    css="""
R .oc{position:absolute;top:400px;width:500px;height:360px;display:flex;flex-direction:column;align-items:center;justify-content:center}
R .oc .n{font-weight:900;font-size:150px;line-height:1;color:#14254a;letter-spacing:-.04em}
R .oc .n.s{font-size:110px}
R .oc .u{font-weight:800;font-size:44px;color:#c8102e;margin-top:14px}
R .ol{top:400px;width:500px;height:360px;border-radius:28px;border:4px dashed rgba(245,239,227,.35)}
""",
    bg="",
    body="""
          <div class="abs l" id="s08-k" style="left:0;right:0;top:150px;text-align:center;font-size:30px;color:#e8b931">온타리오주 고등학교 졸업장</div>
          <div class="abs h" id="s08-o" style="left:0;right:0;top:200px;text-align:center;font-size:150px;perspective:900px">OSSD</div>
          <div class="abs ol" id="s08-o1" style="left:150px"></div><div class="abs ol" id="s08-o2" style="left:710px"></div><div class="abs ol" id="s08-o3" style="left:1270px"></div>
          <div class="card oc" id="s08-c1" style="left:150px"><div class="n" id="s08-n1">30</div><div class="u">학점</div></div>
          <div class="card oc" id="s08-c2" style="left:710px"><div class="n s">OSSLT</div><div class="u">문해력 시험</div></div>
          <div class="card oc" id="s08-c3" style="left:1270px"><div class="n"><span id="s08-n3">40</span><span style="font-size:70px">시간</span></div><div class="u">봉사활동</div></div>""",
    js="""
inn('#s08-k',T('다음은 졸업장'),{y:14});
kin('#s08-o',T('OSSD라고'),0.06);
tl.to('#s08-o',{y:-30,scale:0.8,duration:0.5,ease:'power2.inOut'},T('조건은 세 가지'));
pop(['#s08-o1','#s08-o2','#s08-o3'],T('조건은 세 가지')+0.2,0.12);
slam('#s08-c1',T('30학점'));odo('#s08-n1',T('30학점'),1.0);
slam('#s08-c2',T('OSSLT'));
slam('#s08-c3',T('봉사활동 40'));odo('#s08-n3',T('봉사활동 40'),1.0);
""",
    sfx=[("impact", "T('30학점')+0.42"), ("impact", "T('OSSLT')+0.42"), ("impact", "T('봉사활동 40')+0.42")],
)

# ---------------------------------------------------------------- S09 30-cell grid 17 + 13
cells = "".join(f'<div class="cell" id="s09-x{i}" style="left:{40 + (i % 10) * 124}px;top:{120 + (i // 10) * 124}px"></div>' for i in range(30))
S["s09"] = dict(
    css="""
R #s09-card{left:110px;top:200px;width:1320px;height:560px}
R .cell{position:absolute;width:110px;height:110px;border-radius:16px;border:3px dashed rgba(20,37,74,.35)}
R .fill{position:absolute;width:110px;height:110px;border-radius:16px}
R .cnt{position:absolute;left:1480px;width:360px}
R .cnt .num{font-size:150px}
""",
    bg="",
    body=f"""
          <div class="card" id="s09-card"><div class="t" style="position:absolute;left:40px;top:34px;font-size:40px">OSSD 30학점</div>{cells}
          {''.join(f'<div class="fill" id="s09-f{i}" style="left:{40 + (i % 10) * 124}px;top:{120 + (i // 10) * 124}px;background:{"#14254a" if i < 17 else "#e8b931"}"></div>' for i in range(30))}
          <div class="pill" id="s09-one" style="left:440px;top:26px;background:#14254a;color:#f5efe3">1학점 = 1과목</div></div>
          <div class="cnt" id="s09-a" style="top:180px"><div class="num" id="s09-na" style="color:#f5efe3">17</div><div class="hd" style="font-size:38px">필수 · <span class="gold">9~10학년</span></div></div>
          <div class="cnt" id="s09-b" style="top:480px"><div class="num gold" id="s09-nb">13</div><div class="hd" style="font-size:38px">선택 · <span class="gold">11~12학년</span></div></div>""",
    js="""
inn('#s09-card',T('계산은 쉬워요'),{y:40});
pop('#s09-f0',T('1학점이'));pop('#s09-one',T('1학점이')+0.3);
pop(Array.from({length:16},(_,i)=>'#s09-f'+(i+1)),T('17개는'),0.05);
inn('#s09-a',T('17개는'),{x:30,y:0});odo('#s09-na',T('17개는'),1.1);
pop(Array.from({length:13},(_,i)=>'#s09-f'+(i+17)),T('13개는'),0.05);
inn('#s09-b',T('13개는'),{x:30,y:0});odo('#s09-nb',T('13개는'),1.1);
""",
    sfx=[("pop", "T('1학점이')"), ("impact", "T('17개는')+0.8"), ("impact", "T('13개는')+0.8")],
)

# ---------------------------------------------------------------- S10 Korean record -> credits
k8 = "".join(f'<div class="fill" id="s10-a{i}" style="left:{i * 92}px;top:0"></div>' for i in range(8))
k4 = "".join(f'<div class="fill" id="s10-b{i}" style="left:{i * 92}px;top:0"></div>' for i in range(4))
S["s10"] = dict(
    css="""
R #s10-doc{left:150px;top:220px;width:360px;height:460px;padding:40px 36px}
R #s10-doc .ln{height:16px;border-radius:8px;background:rgba(20,37,74,.18);margin-top:22px}
R .row{position:absolute;left:880px;width:740px;height:80px}
R .fill{position:absolute;width:80px;height:80px;border-radius:14px;background:#e8b931}
R .rl{position:absolute;left:880px;font-weight:800;font-size:44px;white-space:nowrap}
""",
    bg="",
    body=f"""
          <div class="card" id="s10-doc"><div class="t" style="font-size:44px">한국 성적표</div><div class="ln" style="width:90%"></div><div class="ln" style="width:70%"></div><div class="ln" style="width:85%"></div><div class="ln" style="width:60%"></div><div class="ln" style="width:80%"></div><div class="ln" style="width:50%"></div><div class="chip navy" id="s10-g" style="left:36px;top:380px">중3부터 인정</div></div>
          <svg class="abs" style="left:560px;top:380px;width:280px;height:120px" viewBox="0 0 280 120"><path id="s10-ar" d="M10 60 L250 60 M215 24 L256 60 L215 96" fill="none" stroke="#e8b931" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div class="rl" id="s10-l1" style="top:200px">한 학년 이수 → <span class="gold">최대 8학점</span></div>
          <div class="row" id="s10-r1" style="top:280px">{k8}</div>
          <div class="rl" id="s10-l2" style="top:470px">한 학기 이수 → <span class="gold">최대 4학점</span></div>
          <div class="row" id="s10-r2" style="top:550px">{k4}</div>""",
    js="""
flip('#s10-doc',T('한국에서 공부한'));
pop('#s10-g',T('중학교 3학년부터'));
draw('#s10-ar',T('한 학년을'),0.6);
inn('#s10-l1',T('최대 8학점'),{x:-20,y:0});pop(Array.from({length:8},(_,i)=>'#s10-a'+i),T('최대 8학점')+0.2,0.07);
inn('#s10-l2',T('최대 4학점'),{x:-20,y:0});pop(Array.from({length:4},(_,i)=>'#s10-b'+i),T('최대 4학점')+0.2,0.07);
""",
    sfx=[("pop", "T('최대 8학점')+0.2"), ("pop", "T('최대 4학점')+0.2")],
)

# ---------------------------------------------------------------- S11 "6학점?" -> stairs -> 10학점~
steps = ["ESL C", "ESL D", "ESL E", "ENG 3U", "ENG 4U"]
stairs = "".join(
    f'<div class="st{" g" if i == 4 else ""}" id="s11-st{i}" style="left:{110 + i * 200}px;top:{720 - (i + 1) * 92}px;height:{(i + 1) * 92}px"><span>{n}</span></div>'
    for i, n in enumerate(steps))
g12 = "".join(f'<div class="chip cream g12" id="s11-g{i}" style="left:1320px;top:{170 + i * 84}px">12학년 과목 {i + 1}</div>' for i in range(5))
S["s11"] = dict(
    css="""
R #s11-six{left:0;right:0;top:300px;text-align:center;font-size:240px;perspective:900px}
R #s11-x{left:810px;top:250px;width:300px;height:300px}
R .st{position:absolute;width:190px;border-radius:16px 16px 0 0;background:#f5efe3;color:#14254a;display:flex;justify-content:center;padding-top:18px}
R .st span{font-weight:900;font-size:36px;white-space:nowrap}
R .st.g{background:#e8b931}
R .g12{font-size:28px;padding:10px 24px}
""",
    bg="",
    body=f"""
          <div class="abs b" id="s11-q" style="left:0;right:0;top:190px;text-align:center;font-size:40px;color:rgba(255,255,255,.75)">"몇 과목만 더 들으면 졸업"</div>
          <div class="abs h" id="s11-six">6학점?</div>
          <div class="chip cream" id="s11-six2" style="left:110px;top:150px">대학 지원 = 12학년 6과목 점수</div>
          <svg class="abs" id="s11-x" viewBox="0 0 300 300"><circle cx="150" cy="150" r="130" fill="none" stroke="#c8102e" stroke-width="18"/><path d="M85 85 L215 215 M215 85 L85 215" stroke="#c8102e" stroke-width="26" stroke-linecap="round"/></svg>
          <div class="abs" id="s11-stairs" style="inset:0">{stairs}
            <div class="abs hd" id="s11-need" style="left:910px;top:150px;font-size:28px;color:#e8b931;white-space:nowrap">대학 지원 필수</div>
            <div class="abs hd" id="s11-eng" style="left:110px;top:740px;width:990px;text-align:center;font-size:36px;border-top:4px solid #e8b931;padding-top:12px">영어만 보통 5과목</div></div>
          {g12}
          <div class="abs" id="s11-tot" style="left:1600px;top:300px;width:300px;text-align:center"><div class="num gold" style="font-size:120px"><span id="s11-tn">10</span></div><div class="hd" style="font-size:40px">학점~</div><div class="b" style="font-size:26px;color:rgba(255,255,255,.75)">현실적인 최소</div></div>""",
    js="""
inn('#s11-q',T('그런데'),{y:16});kin('#s11-six',T('몇 과목만')+0.4,0.05);
stamp('#s11-x',T('거의 맞지 않습니다'),-12);
outt(['#s11-q','#s11-six','#s11-x'],T('대학은 12학년')-0.2,{s:0.8});
grow(['#s11-st0','#s11-st1','#s11-st2','#s11-st3','#s11-st4'].map(s=>q(s)),T('ESL부터'),0.5,'50% 100%','y');
tl.fromTo(['#s11-st0','#s11-st1','#s11-st2','#s11-st3','#s11-st4'].map(s=>q(s)),{opacity:0},{opacity:1,duration:0.3,stagger:0.22},T('ESL부터'));
pop('#s11-six2',T('대학은 12학년'));
inn('#s11-need',T('단계별로'),{y:10});
inn('#s11-eng',T('영어만 보통'),{y:12});
pop(['#s11-g0','#s11-g1','#s11-g2','#s11-g3','#s11-g4'],T('12학년 과목을 더하면'),0.12);
slam('#s11-tot',T('최소 10학점'));odo('#s11-tn',T('최소 10학점'),0.9);
""",
    sfx=[("stamp", "T('거의 맞지 않습니다')+0.3"), ("pop", "T('12학년 과목을 더하면')"), ("impact", "T('최소 10학점')+0.42")],
)

# ---------------------------------------------------------------- S12 credit plan mockup
terms = [("2월", ["ESL D", "수학 11"]), ("4월", ["ESL E", "과학 11"]), ("여름", ["ENG 3U", "선택 과목"]),
         ("9월", ["ENG 4U", "수학 12"]), ("11월", ["과학 12", "선택 12"])]
cols = ""
for i, (m, subs) in enumerate(terms):
    x = 50 + i * 270
    cols += f'<div class="mh" id="s12-m{i}" style="left:{x}px">{m}</div>'
    for j, sname in enumerate(subs):
        cols += f'<div class="sc" id="s12-s{i}{j}" style="left:{x}px;top:{230 + j * 110}px">{sname}</div>'
S["s12"] = dict(
    css="""
R #s12-card{left:240px;top:150px;width:1440px;height:640px}
R .mh{position:absolute;top:130px;width:240px;height:70px;border-radius:14px;background:#14254a;color:#f5efe3;font-weight:800;font-size:34px;display:flex;align-items:center;justify-content:center}
R .sc{position:absolute;width:240px;height:90px;border-radius:14px;background:#fff;border:3px solid rgba(20,37,74,.18);color:#14254a;font-weight:800;font-size:32px;display:flex;align-items:center;justify-content:center}
R #s12-badge{left:1130px;top:470px}
""",
    bg="",
    body=f"""
          <div class="card" id="s12-card"><div class="t" style="position:absolute;left:50px;top:40px;font-size:46px">학생별 학점 계획표</div>
            <div class="tag" style="right:40px;top:44px">예시</div>{cols}
            <div class="pill" id="s12-badge" style="font-size:40px;padding:16px 34px">졸업 예정</div></div>""",
    js="""
inn('#s12-card',T('그래서 처음'),{y:40});
pop(['#s12-m0','#s12-m1','#s12-m2','#s12-m3','#s12-m4'],T('학점 계획'),0.1);
pop(['#s12-s00','#s12-s01','#s12-s10','#s12-s11','#s12-s20','#s12-s21','#s12-s30','#s12-s31','#s12-s40','#s12-s41'],T('학생 성적표를'),0.14);
stamp('#s12-badge',T('계획표로'),-8);
""",
    sfx=[("pop", "T('학생 성적표를')"), ("stamp", "T('계획표로')+0.3")],
)

# ---------------------------------------------------------------- S13 five terms ring + compare
def arc(cx, cy, r, a0, a1):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return f"M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}"


months = ["9월", "11월", "2월", "4월", "여름"]
ring = ""
labels = ""
for i, m in enumerate(months):
    a0 = -90 + i * 72 + 4
    a1 = a0 + 64
    ring += f'<path class="seg0" d="{arc(270, 270, 220, a0, a1)}"/><path class="seg" id="s13-g{i}" d="{arc(270, 270, 220, a0, a1)}"/>'
    am = math.radians((a0 + a1) / 2)
    lx, ly = 270 + 300 * math.cos(am), 270 + 300 * math.sin(am)
    labels += f'<div class="ml" id="s13-l{i}" style="left:{180 + lx - 70:.0f}px;top:{170 + ly - 30:.0f}px">{m}</div>'
books = "".join(f'<div class="bk" style="top:{190 + i * 58}px;background:{c}"></div>' for i, c in enumerate(["#6b7a99", "#55637f", "#6b7a99", "#55637f"]))
S["s13"] = dict(
    css="""
R .seg0{fill:none;stroke:rgba(245,239,227,.12);stroke-width:64}
R .seg{fill:none;stroke:#e8b931;stroke-width:64}
R .ml{position:absolute;width:140px;text-align:center;font-weight:900;font-size:40px}
R .cmp{position:absolute;top:220px;width:440px;height:540px;border-radius:28px;padding:30px}
R .bk{position:absolute;left:70px;width:300px;height:50px;border-radius:8px}
""",
    bg="",
    body=f"""
          <svg class="abs" id="s13-ring" style="left:180px;top:170px;width:540px;height:540px" viewBox="0 0 540 540">{ring}</svg>{labels}
          <div class="abs" id="s13-mid" style="left:180px;top:170px;width:540px;height:540px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="num" style="font-size:150px" id="s13-n">5</div><div class="hd" style="font-size:40px">학기 / 1년</div></div>
          <div class="cmp" id="s13-c1" style="left:880px;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.18)"><div class="hd" style="font-size:44px;color:rgba(255,255,255,.6)">한 번에 4과목</div>{books}<div class="b" style="position:absolute;left:30px;bottom:30px;font-size:30px;color:rgba(255,255,255,.55)">한 학기 내내 동시에</div></div>
          <div class="cmp card" id="s13-c2" style="left:1380px;background:#e8b931"><div class="t" style="font-size:44px">한 번에 2과목</div><div class="num" style="font-size:120px;color:#14254a;margin-top:60px">× 10주</div><div class="b" style="font-size:30px;margin-top:40px;color:#14254a">점수 관리 집중</div><div style="position:absolute;right:30px;bottom:30px">{CHECK.format(w=90)}</div></div>""",
    js="""
odo('#s13-n',T('다섯 학기로'),0.9);inn('#s13-mid',T('다섯 학기로'),{s:0.7,y:0});
const MT=[T('9월,'),T('11월,'),T('2월,'),T('4월,'),T('여름 학기')];
for(let i=0;i<5;i++){draw('#s13-g'+i,MT[i],0.45,'power2.out');pop('#s13-l'+i,MT[i]);}
tl.to(['#s13-ring','#s13-mid','#s13-l0','#s13-l1','#s13-l2','#s13-l3','#s13-l4'].map(s=>q(s)),{x:-60,scale:0.9,duration:0.6,ease:'power2.inOut'},T('한 학기는 10주'));
flip('#s13-c2',T('보통 2과목'));draw('#s13-c2 .ck',T('보통 2과목')+0.6,0.4);
inn('#s13-c1',T('4과목을 동시에'),{y:30});tl.to('#s13-c1',{opacity:0.55,duration:0.6},T('훨씬 유리합니다'));
tl.fromTo('#s13-c2',{scale:1},{scale:1.05,duration:0.4,yoyo:true,repeat:1,ease:'sine.inOut'},T('훨씬 유리합니다'));
""",
    sfx=[("pop", "T('9월,')"), ("pop", "T('11월,')"), ("pop", "T('2월,')"), ("pop", "T('4월,')"), ("pop", "T('여름 학기')")],
)

# ---------------------------------------------------------------- S14 half-year offset
mx = lambda k: 300 + k * 80  # month index 0 = Sep(prev) ... 18 months
ticks = "".join(f'<div class="tk" style="left:{mx(k) - 2}px"></div>' for k in range(0, 19))
tlabels = "".join(f'<div class="tl" style="left:{mx(k) - 40}px">{n}</div>' for k, n in [(0, "9월"), (3, "12월"), (6, "3월"), (9, "6월"), (12, "9월"), (15, "12월"), (18, "3월")])
S["s14"] = dict(
    css="""
R .tk{position:absolute;top:640px;width:4px;height:22px;background:rgba(245,239,227,.5)}
R .tl{position:absolute;top:676px;width:80px;text-align:center;font-weight:700;font-size:28px;color:rgba(245,239,227,.8)}
R .bar{position:absolute;height:90px;border-radius:16px;display:flex;align-items:center;padding-left:26px;font-weight:900;font-size:38px;white-space:nowrap}
R .rowl{position:absolute;left:90px;width:190px;font-weight:900;font-size:40px;text-align:right}
""",
    bg="",
    body=f"""
          <div class="abs" id="s14-ax" style="left:300px;top:648px;width:1440px;height:6px;background:rgba(245,239,227,.5)"></div>{ticks}{tlabels}
          <div class="rowl" id="s14-ck" style="top:300px">캐나다</div>
          <div class="bar" id="s14-cb" style="left:{mx(0)}px;top:280px;width:{mx(10) - mx(0)}px;background:#e8b931;color:#14254a">9월 시작</div>
          <div class="rowl" id="s14-kk" style="top:450px">한국</div>
          <div class="bar" id="s14-kb" style="left:{mx(6)}px;top:430px;width:{mx(18) - mx(6)}px;background:#f5efe3;color:#14254a">3월 시작</div>
          <svg class="abs" style="left:{mx(0)}px;top:200px;width:{mx(6) - mx(0)}px;height:60px" viewBox="0 0 480 60"><path id="s14-ar" d="M6 30 L474 30 M30 8 L6 30 L30 52 M450 8 L474 30 L450 52" fill="none" stroke="#e8b931" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div class="pill" id="s14-half" style="left:{mx(3) - 110}px;top:140px">반 년 빠름</div>
          <div class="card" id="s14-red" style="left:420px;top:740px;width:1080px;height:96px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:46px">9월만 입학 = 최대 1년 손해</div>""",
    js="""
grow('#s14-ax',T('입학 시기가'),1.0);
inn('#s14-kk',T('한국 학생에게'),{x:-20,y:0});grow('#s14-kb',T('한국 학생에게')+0.2,0.8);
inn('#s14-ck',T('캐나다 학년은'),{x:-20,y:0});grow('#s14-cb',T('캐나다 학년은')+0.2,0.8);
draw('#s14-ar',T('반 년'),0.6);pop('#s14-half',T('반 년')+0.3);
stamp('#s14-red',T('9월에만'),-2);
""",
    sfx=[("pop", "T('반 년')+0.3"), ("stamp", "T('9월에만')+0.3")],
)

# ---------------------------------------------------------------- S15 route 12월 -> 1월 -> 2월·4월
nodes = [("12월", "한국 성적"), ("1월", "상담"), ("2월·4월", "입학")]
nd = "".join(
    f'<div class="nd{" g" if i == 2 else ""}" id="s15-n{i}" style="left:{180 + i * 560}px"><div class="m">{a}</div><div class="s">{b}</div>'
    f'<div class="cw" id="s15-c{i}">{CHECK.format(w=64)}</div></div>' for i, (a, b) in enumerate(nodes))
S["s15"] = dict(
    css="""
R .nd{position:absolute;top:260px;width:440px;height:280px;border-radius:28px;background:#f5efe3;color:#14254a;display:flex;flex-direction:column;align-items:center;justify-content:center}
R .nd.g{background:#e8b931}
R .nd .m{font-weight:900;font-size:96px;letter-spacing:-.03em}
R .nd .s{font-weight:800;font-size:42px}
R .cw{position:absolute;right:-20px;top:-20px}
""",
    bg="",
    body=f"""
          <div class="abs hd" id="s15-h" style="left:180px;top:150px;font-size:48px">많이 쓰는 루트</div>
          <svg class="abs" style="left:620px;top:360px;width:120px;height:80px" viewBox="0 0 120 80"><path id="s15-a0" d="M6 40 L104 40 M80 16 L106 40 L80 64" fill="none" stroke="#e8b931" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <svg class="abs" style="left:1180px;top:360px;width:120px;height:80px" viewBox="0 0 120 80"><path id="s15-a1" d="M6 40 L104 40 M80 16 L106 40 L80 64" fill="none" stroke="#e8b931" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>{nd}
          <div class="chip cream" id="s15-k1" style="left:480px;top:620px">한 학기 최대 3과목</div>
          <div class="chip gold" id="s15-k2" style="left:1000px;top:620px">조기 졸업 가능</div>""",
    js="""
inn('#s15-h',T('그래서 많이'),{y:16});
pop('#s15-n0',T('12월에'));draw('#s15-c0 .ck',T('12월에')+0.5,0.35);
draw('#s15-a0',T('1월에 상담'),0.4);pop('#s15-n1',T('1월에 상담')+0.2);draw('#s15-c1 .ck',T('1월에 상담')+0.7,0.35);
draw('#s15-a1',T('2월이나 4월'),0.4);pop('#s15-n2',T('2월이나 4월')+0.2);draw('#s15-c2 .ck',T('2월이나 4월')+0.7,0.35);
pop('#s15-k1',T('최대 3과목'));pop('#s15-k2',T('늦게 시작해도'));
""",
    sfx=[("pop", "T('12월에')"), ("pop", "T('1월에 상담')+0.2"), ("pop", "T('2월이나 4월')+0.2")],
)

# ---------------------------------------------------------------- S16 2 vs 5 reports
dots1 = "".join(f'<div class="dt" id="s16-d{i}" style="left:{x}px;top:322px"></div><div class="dl" id="s16-e{i}" style="left:{x - 60}px;top:370px">{n}</div>'
                for i, (x, n) in enumerate([(900, "중간"), (1560, "기말")]))
pos5 = [(560, "2주"), (790, "2주"), (1020, "중간"), (1250, "2주"), (1560, "기말")]
dots2 = "".join(f'<div class="dt g" id="s16-f{i}" style="left:{x}px;top:552px"></div><div class="dl" id="s16-h{i}" style="left:{x - 60}px;top:600px">{n}</div>'
                for i, (x, n) in enumerate(pos5))
S["s16"] = dict(
    css="""
R .ln{position:absolute;left:420px;width:1240px;height:6px;border-radius:3px;background:rgba(245,239,227,.45)}
R .dt{position:absolute;width:40px;height:40px;margin-left:-20px;border-radius:50%;background:#f5efe3}
R .dt.g{background:#e8b931}
R .dl{position:absolute;width:120px;text-align:center;font-weight:800;font-size:28px;margin-left:-20px}
R .rl{position:absolute;left:110px;width:280px;font-weight:900;font-size:40px}
R #s16-big{left:0;right:0;top:140px;text-align:center;font-size:120px;color:#e8b931;perspective:900px}
R #s16-cnt{left:1700px;top:470px;width:180px;text-align:center}
""",
    bg="",
    body=f"""
          <div class="abs hd" id="s16-h" style="left:0;right:0;top:150px;text-align:center;font-size:56px">SGA의 핵심 = <span class="gold">관리</span></div>
          <div class="abs h" id="s16-big">2주마다</div>
          <div class="rl" id="s16-r1" style="top:315px">일반 학교</div><div class="ln" id="s16-l1" style="top:339px"></div>{dots1}
          <div class="abs num" id="s16-c1" style="left:1700px;top:300px;width:180px;text-align:center;font-size:90px;color:rgba(245,239,227,.7)">2</div>
          <div class="rl gold" id="s16-r2" style="top:545px">SGA</div><div class="ln" id="s16-l2" style="top:569px;background:#e8b931"></div>{dots2}
          <div class="abs num gold" id="s16-cnt" style="font-size:150px">5</div>
          <div class="abs hd" id="s16-cl" style="left:1660px;top:640px;width:260px;text-align:center;font-size:30px">회 / 한 학기</div>""",
    js="""
inn('#s16-h',T('이제 SGA의'),{y:20});
outt('#s16-h',T('보통 성적표는')-0.3);
inn('#s16-r1',T('보통 성적표는'),{x:-20,y:0});grow('#s16-l1',T('보통 성적표는'),0.8);
pop(['#s16-d0','#s16-d1'],T('한 학기에 두 번'),0.3);inn(['#s16-e0','#s16-e1'],T('중간과 기말'),{y:10,st:0.3});inn('#s16-c1',T('한 학기에 두 번'),{s:0.6,y:0});
kin('#s16-big',T('SGA는 2주마다'),0.05);
inn('#s16-r2',T('SGA는 2주마다')+0.4,{x:-20,y:0});grow('#s16-l2',T('SGA는 2주마다')+0.4,0.8);
pop(['#s16-f0','#s16-f1','#s16-f2','#s16-f3','#s16-f4'],T('나옵니다'),0.18);inn(['#s16-h0','#s16-h1','#s16-h2','#s16-h3','#s16-h4'],T('나옵니다')+0.1,{y:10,st:0.18});
slam('#s16-cnt',T('다섯 번'));inn('#s16-cl',T('다섯 번')+0.4,{y:10});
""",
    sfx=[("pop", "T('나옵니다')"), ("impact", "T('다섯 번')+0.42")],
)

# ---------------------------------------------------------------- S17 report card mockup + email
rows17 = [("영어 (ESL D)", "82", "출석 양호", "제출 완료", "적극적"), ("수학 11", "88", "출석 양호", "1건 지연", "보통")]
th = "".join(f'<div class="th c{i}">{h}</div>' for i, h in enumerate(["과목", "점수", "출석", "과제", "참여도"]))
trs = "".join("".join(f'<div class="td c{i}" style="top:{210 + r * 80}px">{v}</div>' for i, v in enumerate(row)) for r, row in enumerate(rows17))
ENV = '<svg viewBox="0 0 80 56" style="width:80px;height:56px"><rect x="2" y="2" width="76" height="52" rx="8" fill="#f5efe3"/><path d="M4 6 L40 32 L76 6" fill="none" stroke="#14254a" stroke-width="5" stroke-linejoin="round"/></svg>'
S["s17"] = dict(
    css="""
R #s17-rc{left:220px;top:150px;width:1200px;height:600px}
R .th,.td{position:absolute;font-weight:800;font-size:32px;color:#14254a;white-space:nowrap}
R .th{top:140px;color:#c8102e;font-size:28px;letter-spacing:.06em}
R #s17-rc .c0{left:50px} R #s17-rc .c1{left:400px} R #s17-rc .c2{left:560px} R #s17-rc .c3{left:780px} R #s17-rc .c4{left:1000px}
R .cm{position:absolute;left:50px;top:400px;width:1100px;padding:24px 28px;border-radius:16px;background:#fff;border:3px solid rgba(20,37,74,.15);font-weight:700;font-size:30px;color:#14254a}
R .env{position:absolute;width:80px;height:56px}
R #s17-bub{left:1250px;top:180px;width:560px;padding:30px 34px;border-radius:30px;background:#fff;color:#14254a;font-weight:900;font-size:44px}
""",
    bg="",
    body=f"""
          <div class="card" id="s17-rc"><div class="t" style="position:absolute;left:50px;top:44px;font-size:44px">2주 리포트</div><div class="tag" style="right:40px;top:48px">예시 화면</div>
            {th}{trs}<div class="cm" id="s17-cm"><span style="color:#c8102e">교사 코멘트 </span><span id="s17-ct">수업 참여가 좋아졌어요. 과제 기한을 지켜 주세요.</span></div></div>
          <div class="chip cream" id="s17-p1" style="left:1500px;top:330px">학부모</div>
          <div class="chip gold" id="s17-p2" style="left:1500px;top:520px">AA Canada</div>
          <div class="env" id="s17-e1" style="left:1240px;top:430px">{ENV}</div>
          <div class="env" id="s17-e2" style="left:1240px;top:430px">{ENV}</div>
          <div class="abs" id="s17-bub">우리 애, 잘하고 있나?<div style="position:absolute;right:-24px;top:-24px" id="s17-ok">{CHECK.format(w=80)}</div></div>""",
    js="""
flip('#s17-rc',T('이 성적표에는'));
inn(qa('#s17-rc .th'),T('이 성적표에는')+0.5,{y:10,st:0.06});
inn(qa('#s17-rc .td.c0'),T('과목별'),{y:10,st:0.1});inn(qa('#s17-rc .td.c1'),T('점수뿐'),{y:10,st:0.1});
inn(qa('#s17-rc .td.c2'),T('출석,'),{y:10,st:0.1});inn(qa('#s17-rc .td.c3'),T('과제 제출'),{y:10,st:0.1});
inn(qa('#s17-rc .td.c4'),T('수업 태도'),{y:10,st:0.1});inn('#s17-cm',T('선생님 코멘트'),{y:16});
tl.to('#s17-rc',{x:-120,scale:0.86,duration:0.6,ease:'power2.inOut'},T('부모님께'));
tl.fromTo('#s17-e1',{opacity:0,x:-200,y:0,scale:0.6},{opacity:1,x:150,y:-100,scale:1,duration:0.8,ease:'power2.out'},T('이메일로'));
pop('#s17-p1',T('이메일로')+0.6);
tl.fromTo('#s17-e2',{opacity:0,x:-200,y:0,scale:0.6},{opacity:1,x:150,y:90,scale:1,duration:0.8,ease:'power2.out'},T('유학원도'));
pop('#s17-p2',T('유학원도')+0.6);
outt(['#s17-e1','#s17-e2','#s17-p1','#s17-p2'],T('우리 애가')-0.3);
inn('#s17-bub',T('우리 애가'),{y:20,s:0.9});stamp('#s17-ok',T('많이 풀려요'),0);
""",
    sfx=[("whoosh", "T('이메일로')"), ("whoosh", "T('유학원도')"), ("pop", "T('많이 풀려요')+0.3")],
)

# ---------------------------------------------------------------- S18 early action graph
vals = [84, 82, 79, 76, 79, 83, 86, 88]
gx = lambda k: 80 + k * 150
gy = lambda v: 360 - (v - 70) * 16
pts1 = " ".join(f"{'M' if k == 0 else 'L'}{gx(k)} {gy(v)}" for k, v in enumerate(vals[:4]))
pts2 = " ".join(f"{'M' if k == 0 else 'L'}{gx(k + 3)} {gy(v)}" for k, v in enumerate(vals[3:]))
gdots = "".join(f'<circle class="gd" id="s18-p{k}" cx="{gx(k)}" cy="{gy(v)}" r="13" fill="{"#c8102e" if v < 80 else ("#2ec27e" if k > 3 else "#f5efe3")}"/>' for k, v in enumerate(vals))
S["s18"] = dict(
    css="""
R .nd{position:absolute;top:700px;font-weight:800;font-size:30px;white-space:nowrap;text-align:center;width:300px}
R .nd i{display:block;margin:0 auto 10px;width:26px;height:26px;border-radius:50%;background:#e8b931}
""",
    bg="",
    body=f"""
          <div class="abs hd" id="s18-h" style="left:150px;top:140px;font-size:50px">진짜 이유: <span class="gold">대학 원서</span></div>
          <svg class="abs" id="s18-g" style="left:250px;top:200px;width:1300px;height:420px" viewBox="0 0 1300 420">
            <path id="s18-tg" d="M40 {gy(80)} L1240 {gy(80)}" stroke="#e8b931" stroke-width="4" stroke-dasharray="14 12" fill="none"/>
            <path id="s18-l1" d="{pts1}" stroke="#f5efe3" stroke-width="7" fill="none" stroke-linejoin="round"/>
            <path id="s18-l2" d="{pts2}" stroke="#2ec27e" stroke-width="7" fill="none" stroke-linejoin="round"/>{gdots}</svg>
          <div class="abs hd" id="s18-tl" style="left:1500px;top:{200 + gy(80) - 50}px;font-size:26px;color:#e8b931;white-space:nowrap">목표 학과 기준</div>
          <div class="abs b" id="s18-bi" style="left:250px;top:615px;font-size:24px;color:rgba(255,255,255,.6)">2주 체크포인트</div>
          <div class="pill" id="s18-ea" style="left:{250 + gx(3) - 40}px;top:{200 + gy(76) + 30}px;background:#c8102e;color:#fff">조기 개입</div>
          <div class="abs" id="s18-ax" style="left:300px;top:712px;width:1320px;height:6px;background:rgba(245,239,227,.45)"></div>
          <div class="nd" id="s18-n0" style="left:150px"><i></i>9월 12학년 시작</div>
          <div class="nd" id="s18-n1" style="left:810px"><i></i>10~12월 원서</div>
          <div class="nd" id="s18-n2" style="left:1470px"><i></i>합격 발표</div>
          <div class="chip cream" id="s18-k" style="left:500px;top:150px;opacity:0">11학년 성적 + 12학년 중간 성적</div>""",
    js="""
inn('#s18-h',T('이걸 만든'),{y:16});
grow('#s18-ax',T('12학년 10월부터'),0.9);pop(['#s18-n0','#s18-n1','#s18-n2'],T('12학년 10월부터')+0.2,0.25);
tl.to('#s18-h',{opacity:0,duration:0.3},T('11학년 성적과')-0.3);pop('#s18-k',T('11학년 성적과'));
outt('#s18-k',T('2주마다 점수를')-0.3);
draw('#s18-tg',T('2주마다 점수를'),0.8);inn('#s18-tl',T('2주마다 점수를')+0.4,{x:-10,y:0});inn('#s18-bi',T('2주마다 점수를'),{y:8});
draw('#s18-l1',T('2주마다 점수를')+0.4,1.6,'none');pop(['#s18-p0','#s18-p1','#s18-p2','#s18-p3'],T('2주마다 점수를')+0.4,0.5);
stamp('#s18-ea',T('미리 과외'),-6);
draw('#s18-l2',T('과목을 조정'),1.6,'none');pop(['#s18-p4','#s18-p5','#s18-p6','#s18-p7'],T('과목을 조정')+0.3,0.4);
""",
    sfx=[("stamp", "T('미리 과외')+0.3"), ("pop", "T('과목을 조정')+0.3")],
)

# ---------------------------------------------------------------- S20 seven teams hub
teams = [("교육부", "학업,"), ("생활부", "생활,"), ("진학컨설팅", "진학 상담"), ("심리상담", "심리 상담"), ("국제학생지원", "국제학생"), ("기숙사관리", "기숙사,"), ("학부모소통", "학부모 소통")]
cx, cy, rr = 960, 470, 300
hub_lines, hub_nodes = "", ""
for i, (n, _) in enumerate(teams):
    a = math.radians(-90 + i * 360 / 7)
    x, y = cx + rr * math.cos(a), cy + rr * 0.92 * math.sin(a)
    hub_lines += f'<path id="s20-ln{i}" d="M{cx} {cy} L{x:.0f} {y:.0f}" stroke="#e8b931" stroke-width="5" fill="none"/>'
    hub_nodes += f'<div class="tn" id="s20-t{i}" style="left:{x - 130:.0f}px;top:{y - 40:.0f}px">{n}</div>'
S["s20"] = dict(
    css="""
R #s20-bgp img{filter:blur(16px) saturate(.6)}
R .tn{position:absolute;width:260px;height:80px;border-radius:40px;background:#f5efe3;color:#14254a;font-weight:900;font-size:34px;display:flex;align-items:center;justify-content:center}
R #s20-hub{left:840px;top:350px;width:240px;height:240px;border-radius:50%;background:#e8b931;color:#14254a;display:flex;flex-direction:column;align-items:center;justify-content:center}
""",
    bg="""        <div class="full" id="s20-bgp" style="opacity:.25"><img src="@P/campus-06-counselling.jpg" alt="" /></div>""",
    body=f"""
          <svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">{hub_lines}</svg>
          <div class="abs" id="s20-hub"><div class="hd" style="font-size:44px">학생</div><div class="num" style="font-size:64px"><span id="s20-n">7</span>개 부서</div></div>
          {hub_nodes}
          <div class="chip" id="s20-k1" style="left:150px;top:150px">9·10학년 담당</div>
          <div class="chip" id="s20-k2" style="left:1520px;top:150px">11·12학년 담당</div>""",
    js="""
kb('#s20-bgp img',0,D,{s:1.05},{s:1.12});
slam('#s20-hub',T('일곱 개 부서'));odo('#s20-n',T('일곱 개 부서'),0.8);
const TT=[T('학업,'),T('생활,'),T('진학 상담'),T('심리 상담'),T('국제학생'),T('기숙사,'),T('학부모 소통')];
for(let i=0;i<7;i++){draw('#s20-ln'+i,TT[i],0.35);pop('#s20-t'+i,TT[i]+0.2);}
pop('#s20-k1',T('9·10학년과'));pop('#s20-k2',T('11·12학년'));
""",
    sfx=[("impact", "T('일곱 개 부서')+0.42")] + [("pop", f"T('{p}')+0.2") for _, p in teams],
)
