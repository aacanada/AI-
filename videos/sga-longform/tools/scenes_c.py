"""Scenes s21-s32 (CH6 foundation, CH7 life, CH8 university, CH9 wrap + CTA)."""
import math

from scenes_a import MAP_SVG, PIN, PIN_CSS
from scenes_b import CHECK

S = {}

# ---------------------------------------------------------------- S21 foundation question (mascot 2/4)
S["s21"] = dict(
    css="""
R #s21-oly{left:150px;top:150px;width:470px;height:592px}
R #s21-t{left:720px;top:480px;font-size:96px;white-space:nowrap}
""",
    bg="",
    body="""
          <div class="ph frame" id="s21-oly"><img src="@B/oly-question-card.jpg" alt="" /></div>
          <div class="abs hd" id="s21-q" style="left:720px;top:170px;font-size:64px;white-space:nowrap">영어가 아직 부족하다면?</div>
          <div class="chip" id="s21-c1" style="left:720px;top:290px">영어로 수학 학점</div>
          <div class="chip" id="s21-c2" style="left:1040px;top:290px">영어로 과학 학점</div>
          <div class="chip red" id="s21-c3" style="left:1360px;top:290px">버티기 어려움</div>
          <div class="abs l gold" id="s21-k" style="left:726px;top:420px;font-size:32px">SGA</div>
          <div class="abs h" id="s21-t">FOUNDATION PROGRAM</div>
          <div class="abs hd" id="s21-s" style="left:724px;top:610px;font-size:48px;color:#e8b931">파운데이션 프로그램</div>""",
    js="""
tl.fromTo('#s21-oly',{opacity:0,scale:0.6,rotation:-8},{opacity:1,scale:1,rotation:-3,duration:0.7,ease:'back.out(1.8)'},T('영어가 아직'));
inn('#s21-q',T('영어가 아직')+0.3,{x:-20,y:0});
pop('#s21-c1',T('수학'));pop('#s21-c2',T('과학 학점'));pop('#s21-c3',T('버티기 어렵죠'));
inn('#s21-k',T('그래서 SGA에는'),{y:10});mask('#s21-t',T('그래서 SGA에는')+0.2,0.9,'l');inn('#s21-s',T('파운데이션 프로그램'),{y:14});
""",
    sfx=[("pop", "T('영어가 아직')"), ("whoosh", "T('그래서 SGA에는')+0.2")],
)

# ---------------------------------------------------------------- S22 foundation day timetable
bars = [("1교시", "9:30~12:00", "정규 수업", False), ("2교시", "12:40~3:10", "정규 수업", False), ("3교시", "3:15~4:45", "파운데이션", True)]
bh = "".join(
    f'<div class="tb{" g" if g else ""}" id="s22-b{i}" style="top:{190 + i * 120}px"><span class="p">{a}</span><span class="tm">{b}</span><span class="k">{c}</span></div>'
    for i, (a, b, c, g) in enumerate(bars))
mini = "".join(f'<div class="ms" id="s22-m{i}" style="left:{1180 + i * 190}px;top:{760 - (i + 1) * 70}px;height:{(i + 1) * 70}px">{n}</div>' for i, n in enumerate(["ESL C", "ESL D", "ESL E"]))
S["s22"] = dict(
    css="""
R #s22-bgp img{filter:saturate(.5)}
R .tb{position:absolute;left:150px;width:960px;height:96px;border-radius:18px;background:#f5efe3;color:#14254a;display:flex;align-items:center;padding:0 30px;gap:30px;font-weight:900;font-size:36px}
R .tb.g{background:#e8b931}
R .tb .tm{font-weight:700;font-size:32px;width:260px}
R .tb .p{width:120px}
R .ms{position:absolute;width:180px;border-radius:14px 14px 0 0;background:#f5efe3;color:#14254a;font-weight:900;font-size:30px;display:flex;justify-content:center;padding-top:14px}
""",
    bg="""        <div class="full" id="s22-bgp" style="opacity:.2"><img src="@P/campus-01-class-whiteboard.jpg" alt="" /></div>""",
    body=f"""
          <div class="abs hd" id="s22-h" style="left:150px;top:120px;font-size:40px">하루 시간표</div>{bh}
          <div class="chip cream" id="s22-c1" style="left:150px;top:570px">아카데믹 라이팅</div>
          <div class="chip cream" id="s22-c2" style="left:470px;top:570px">파워 스피킹</div>
          <div class="chip" id="s22-c3" style="left:150px;top:660px">학점 과목 아님</div>
          <div class="chip gold" id="s22-c4" style="left:450px;top:660px">조건에 따라 무료</div>
          <div class="abs" id="s22-mini" style="inset:0">{mini}
            <svg class="abs" style="left:1260px;top:420px;width:400px;height:200px" viewBox="0 0 400 200"><path id="s22-skip" d="M10 190 C 80 20, 300 0, 380 120 M350 96 L382 124 L392 84" fill="none" stroke="#e8b931" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <div class="abs hd" id="s22-up" style="left:1220px;top:340px;font-size:34px;color:#e8b931;white-space:nowrap">다음 단계로 더 빨리</div></div>""",
    js="""
kb('#s22-bgp img',0,D,{s:1.0},{s:1.08});
inn('#s22-h',T('오전과 오후'),{y:10});grow('#s22-b0',T('오전과 오후'),0.6);grow('#s22-b1',T('오전과 오후')+0.4,0.6);
grow('#s22-b2',T('3교시에'),0.6);tl.fromTo('#s22-b2',{scale:1},{scale:1.04,duration:0.3,yoyo:true,repeat:1},T('3교시에')+0.7);
pop('#s22-c1',T('아카데믹 라이팅'));pop('#s22-c2',T('파워 스피킹'));
pop('#s22-c3',T('학점 과목은'));
grow(['#s22-m0','#s22-m1','#s22-m2'].map(s=>q(s)),T('다음 영어 단계로'),0.5,'50% 100%','y');
draw('#s22-skip',T('더 빨리'),0.8);inn('#s22-up',T('더 빨리')+0.4,{y:10});
pop('#s22-c4',T('무료로'));
""",
    sfx=[("pop", "T('3교시에')"), ("pop", "T('무료로')")],
)

# ---------------------------------------------------------------- S23 residences (5)
houses = "".join(f'<div class="ph frame hs" id="s23-h{i}" style="left:{130 + i * 345}px"><img src="@B/res-h{i + 1}.jpg" alt="" /></div>' for i in range(5))
S["s23"] = dict(
    css="""
R .hs{top:190px;width:300px;height:420px}
R #s23-cnt{left:130px;top:640px}
""",
    bg="",
    body=f"""
          {houses}<div class="sweep" id="s23-sw" style="top:150px;bottom:auto;height:520px"></div>
          <div class="abs" id="s23-cnt"><span class="num gold" style="font-size:140px" id="s23-n">5</span><span class="hd" style="font-size:56px">곳</span></div>
          <div class="chip cream" id="s23-k1" style="left:460px;top:690px">도보 통학</div>
          <div class="chip cream" id="s23-k2" style="left:700px;top:690px">여학생 전용 하우스</div>
          <div class="ph frame" id="s23-big" style="left:130px;top:150px;width:900px;height:620px"><img src="@P/res-02-house.jpg" alt="" /></div>
          <div class="ph frame" id="s23-kit" style="left:1080px;top:150px;width:480px;height:620px"><img src="@P/res-01-kitchen.jpg" alt="" /></div>
          <div class="chip gold" id="s23-k3" style="left:1100px;top:700px">사감 24시간 상주</div>""",
    js="""
const H=['#s23-h0','#s23-h1','#s23-h2','#s23-h3','#s23-h4'];
tl.fromTo(H.map(s=>q(s)),{opacity:0,y:-140,rotation:(i)=>[-8,5,-4,7,-6][i]},{opacity:1,y:0,rotation:(i)=>[-3,2,-2,3,-2][i],duration:0.75,ease:'power3.out',stagger:0.18},T('생활도 볼게요'));
sweep('#s23-sw',T('생활도 볼게요')+1.0);
slam('#s23-cnt',T('다섯 곳'));odo('#s23-n',T('다섯 곳'),0.7);
pop('#s23-k1',T('걸어서'));pop('#s23-k2',T('여학생 전용'));
outt(H.concat(['#s23-cnt','#s23-k1','#s23-k2']).map(s=>q(s)),T('모든 레지던스에')-0.3,{s:0.9});
inn('#s23-big',T('모든 레지던스에'),{x:-60,y:0});kb('#s23-big img',T('모든 레지던스에'),D,{s:1.0},{s:1.1});
inn('#s23-kit',T('사감 선생님이'),{x:60,y:0});pop('#s23-k3',T('24시간'));
""",
    sfx=[("impact", "T('다섯 곳')+0.42"), ("pop", "T('여학생 전용')"), ("pop", "T('24시간')")],
)

# ---------------------------------------------------------------- S24 meals + morning snack (mascot 3/4)
S["s24"] = dict(
    css="""
R #s24-meal{left:130px;top:150px;width:1180px;height:502px}
R #s24-snk{left:1000px;top:200px;width:800px;height:198px}
R #s24-oly{left:1290px;top:430px;width:300px;height:318px}
""",
    bg="",
    body="""
          <div class="ph frame" id="s24-meal"><img src="@B/meals-grid.jpg" alt="" /></div>
          <div class="chip gold" id="s24-k1" style="left:1380px;top:180px">하루 3식</div>
          <div class="chip cream" id="s24-k2" style="left:1380px;top:280px">한식 메뉴</div>
          <div class="chip cream" id="s24-k3" style="left:1380px;top:380px">알레르기 맞춤</div>
          <div class="ph frame" id="s24-snk"><img src="@B/snack-items.jpg" alt="" /></div>
          <div class="abs" id="s24-oly"><img src="@B/oly-4.png" alt="" style="width:100%;height:100%;object-fit:contain" /></div>
          <div class="chip gold" id="s24-k4" style="left:1000px;top:440px">매일 아침 간식</div>
          <div class="abs hd" id="s24-t" style="left:1000px;top:540px;font-size:44px;width:300px">작은 배려</div>""",
    js="""
mask('#s24-meal',T('식사는'),0.9,'d');kb('#s24-meal img',T('식사는'),D,{s:1.0},{s:1.07});
pop('#s24-k1',T('하루 세 끼'));pop('#s24-k2',T('한식 메뉴'));pop('#s24-k3',T('알레르기'));
tl.to('#s24-meal',{x:-60,scale:0.78,opacity:0.5,transformOrigin:'0% 50%',duration:0.6,ease:'power2.inOut'},T('학교에서는'));
outt(['#s24-k1','#s24-k2','#s24-k3'],T('학교에서는'));
inn('#s24-snk',T('아침 간식')-0.2,{x:60,y:0});pop('#s24-k4',T('아침 간식')+0.2);
tl.fromTo('#s24-oly',{opacity:0,y:80,scale:0.8},{opacity:1,y:0,scale:1,duration:0.6,ease:'back.out(1.8)'},T('아침 간식')+0.4);
inn('#s24-t',T('작은 배려'),{y:14});
""",
    sfx=[("pop", "T('하루 세 끼')"), ("pop", "T('아침 간식')+0.2")],
)

# ---------------------------------------------------------------- S25 YMCA + life montage
mont = ["life-07-island-banner", "life-08-soccer", "life-09-picnic", "life-01-island-cntower", "life-04-group-hall", "campus-04-lounge-pingpong"]
rot = [-5, 4, -3, 6, -4, 3]
mx = [180, 520, 860, 300, 640, 980]
my = [150, 180, 140, 400, 430, 390]
mh = "".join(f'<div class="ph frame mo" id="s25-m{i}" style="left:{mx[i]}px;top:{my[i]}px"><img src="@P/{n}.jpg" alt="" /></div>' for i, n in enumerate(mont))
S["s25"] = dict(
    css="""
R .mo{width:520px;height:360px}
R #s25-pool{left:150px;top:150px;width:820px;height:540px}
R #s25-fit{left:1010px;top:220px;width:760px;height:370px}
""",
    bg="",
    body=f"""
          <div class="ph frame" id="s25-pool"><img src="@P/town-16-pool.jpg" alt="" /><div class="lab">수영장</div></div>
          <div class="ph frame" id="s25-fit"><img src="@P/town-15-fitness.jpg" alt="" /><div class="lab">체육관</div></div>
          <div class="chip gold" id="s25-k0" style="left:1010px;top:630px">YMCA 365일</div>
          {mh}
          <div class="chip cream" id="s25-k1" style="left:1560px;top:200px">봉사활동</div>
          <div class="chip cream" id="s25-k2" style="left:1560px;top:300px">동아리</div>
          <div class="chip cream" id="s25-k3" style="left:1560px;top:400px">학교 행사</div>
          <div class="pill" id="s25-p" style="left:1520px;top:560px;font-size:32px">→ 대학 에세이 재료</div>""",
    js="""
flip('#s25-pool',T('YMCA'));kb('#s25-pool img',T('YMCA'),D,{s:1.0},{s:1.1});
flip('#s25-fit',T('수영장과 체육관'));pop('#s25-k0',T('1년 내내'));
outt(['#s25-pool','#s25-fit','#s25-k0'],T('학생회')-0.3,{s:0.9});
const MR=[-5,4,-3,6,-4,3];
for(let i=0;i<6;i++){const at=T('학생회')+i*((T('꾸준합니다')-T('학생회'))/6);
  tl.fromTo('#s25-m'+i,{opacity:0,y:-160,rotation:MR[i]*2.4,scale:1.06},{opacity:1,y:0,rotation:MR[i],scale:1,duration:0.6,ease:'power3.out'},at);}
pop('#s25-k1',T('봉사활동'));pop('#s25-k2',T('동아리'));pop('#s25-k3',T('소풍'));
pop('#s25-p',T('대학 에세이'));
""",
    sfx=[("whoosh", "T('학생회')"), ("pop", "T('대학 에세이')")],
)

# ---------------------------------------------------------------- S26 donut + universities
segs = [(57, "#e8b931", "캐나다"), (25, "#f5efe3", "미국"), (10, "#c8102e", "영국"), (8, "#6b7a99", "기타")]
C = 2 * math.pi * 200
acc, donut, dl = 0, "", ""
for i, (v, c, n) in enumerate(segs):
    donut += (f'<circle class="dn" id="s26-d{i}" cx="260" cy="260" r="200" fill="none" stroke="{c}" stroke-width="90" '
              f'stroke-dasharray="{C * v / 100 - 4:.1f} {C:.1f}" stroke-dashoffset="{-C * acc / 100:.1f}" transform="rotate(-90 260 260)"/>')
    a = math.radians(-90 + 360 * (acc + v / 2) / 100)
    lx, ly = 230 + 260 + 350 * math.cos(a), 220 + 260 + 335 * math.sin(a)
    dl += f'<div class="dl" id="s26-l{i}" style="left:{lx - 90:.0f}px;top:{ly - 40:.0f}px"><b>{n}</b> <span id="s26-v{i}">{v}</span>%</div>'
    acc += v
unis1 = ["University of Toronto", "McMaster", "Waterloo", "UBC", "Queen's", "Western"]
unis2 = ["UC Berkeley", "UCLA", "NYU", "UCL", "King's College London", "University of Toronto"]
row = lambda xs, cls: "".join(f'<div class="chip {cls} uc">{u}</div>' for u in xs)
S["s26"] = dict(
    css="""
R #s26-bgp img{filter:saturate(.6)}
R .dl{position:absolute;width:180px;text-align:center;font-weight:800;font-size:34px;white-space:nowrap}
R .dl b{font-weight:800}
R .uflow{position:absolute;display:flex;gap:18px;white-space:nowrap}
R .uc{position:relative}
""",
    bg="""        <div class="full" id="s26-bgp" style="opacity:.18"><img src="@P/grad-01-2025-stage.jpg" alt="" /></div>""",
    body=f"""
          <div class="abs hd" id="s26-h" style="left:1020px;top:150px;font-size:52px">SGA 대학 지원 비율</div>
          <svg class="abs" style="left:230px;top:220px;width:520px;height:520px" viewBox="0 0 520 520">{donut}</svg>{dl}
          <div class="abs b" id="s26-s" style="left:1020px;top:230px;font-size:30px;color:rgba(255,255,255,.75)">학교 공개 자료 · 연간</div>
          <div class="abs hd" id="s26-uh" style="left:1020px;top:380px;font-size:38px;color:#e8b931">진학 사례</div>
          <div class="abs" style="left:1020px;top:440px;width:860px;height:200px;overflow:hidden" data-layout-allow-overflow>
            <div class="uflow" id="s26-u1" style="left:0;top:10px">{row(unis1, "cream")}</div>
            <div class="uflow" id="s26-u2" style="left:0;top:110px">{row(unis2, "")}</div></div>""",
    js="""
kb('#s26-bgp img',0,D,{s:1.0},{s:1.08});
inn('#s26-h',T('결국 중요한'),{y:16});inn('#s26-s',T('학교가 공개한'),{y:10});
const DT=[T('캐나다가 57%'),T('미국 25%'),T('영국 10%'),T('영국 10%')+0.7];
for(let i=0;i<4;i++){const c=q('#s26-d'+i);const L=parseFloat(c.getAttribute('stroke-dasharray'));const C=parseFloat(c.getAttribute('stroke-dasharray').split(' ')[1]);
  tl.fromTo(c,{attr:{'stroke-dasharray':'0 '+C}},{attr:{'stroke-dasharray':L+' '+C},duration:0.7,ease:'power2.out'},DT[i]);
  inn('#s26-l'+i,DT[i]+0.3,{s:0.7,y:0});if(i<3)odo('#s26-v'+i,DT[i]+0.3,0.8);}
inn('#s26-uh',T('토론토대'),{y:10});
tl.fromTo('#s26-u1',{opacity:0,x:500},{opacity:1,x:-900,duration:Math.max(4,D-T('토론토대')),ease:'none'},T('토론토대'));
tl.fromTo('#s26-u2',{opacity:0,x:800},{opacity:1,x:-700,duration:Math.max(4,D-T('미국 UC')),ease:'none'},T('미국 UC'));
""",
    sfx=[("impact", "T('캐나다가 57%')+0.3")],
)

# ---------------------------------------------------------------- S27 scholarships + AP
aps = ["AP Calculus", "AP Biology", "AP Chemistry", "AP Statistics"]
S["s27"] = dict(
    css="""
R #s27-bgp img{filter:saturate(.6)}
R .sch{position:absolute;top:200px;width:760px;height:340px;padding:40px;display:flex;flex-direction:column;justify-content:center}
R .sch .num{font-size:130px;color:#14254a}
R .sch .u{font-weight:800;font-size:40px;color:#c8102e;margin-top:10px}
""",
    bg="""        <div class="full" id="s27-bgp" style="opacity:.18"><img src="@P/grad-02-gowns.jpg" alt="" /></div>""",
    body=f"""
          <div class="abs hd" id="s27-h" style="left:150px;top:120px;font-size:44px">2026 장학금 소식</div>
          <div class="card sch" id="s27-c1" style="left:150px"><div class="num" id="s27-n1">$100,000</div><div class="u">University of Toronto</div></div>
          <div class="card sch" id="s27-c2" style="left:1010px"><div class="num" id="s27-n2">$60,000</div><div class="u">Queen's University</div></div>
          {''.join(f'<div class="chip cream" id="s27-a{i}" style="left:{150 + i * 330}px;top:620px">{a}</div>' for i, a in enumerate(aps))}
          <div class="pill" id="s27-may" style="left:1500px;top:700px;background:#c8102e;color:#fff;font-size:36px;padding:14px 32px">매년 5월 시험</div>""",
    js="""
kb('#s27-bgp img',0,D,{s:1.0},{s:1.08});
inn('#s27-h',T('2026년에도'),{y:12});
slam('#s27-c1',T('토론토대 10만'));odo('#s27-n1',T('토론토대 10만'),1.3);
slam('#s27-c2',T('퀸즈대 6만'));odo('#s27-n2',T('퀸즈대 6만'),1.3);
tl.to(['#s27-c1','#s27-c2'].map(s=>q(s)),{y:-40,scale:0.9,duration:0.5,ease:'power2.inOut'},T('미국 대학을'));
pop(['#s27-a0','#s27-a1','#s27-a2','#s27-a3'],T('AP 과정'),0.12);
stamp('#s27-may',T('5월 시험'),-6);
""",
    sfx=[("impact", "T('토론토대 10만')+0.42"), ("impact", "T('퀸즈대 6만')+0.42"), ("pop", "T('AP 과정')"), ("stamp", "T('5월 시험')+0.3")],
)

# ---------------------------------------------------------------- S28 UofT three campuses
S["s28"] = dict(
    css=PIN_CSS + """
R .pl{position:absolute;font-weight:800;font-size:32px;white-space:nowrap}
""",
    bg="",
    body=MAP_SVG.format(id="s28", x=560, y=180) + """
          <div class="pill" id="s28-tip" style="left:150px;top:150px;font-size:34px">TIP</div>
          <div class="abs hd" id="s28-q" style="left:150px;top:240px;font-size:52px;width:420px">"토론토대 합격!"</div>
          <div class="abs hd" id="s28-cc" style="left:150px;top:400px;font-size:56px;white-space:nowrap">캠퍼스 확인</div>
          <div class="abs" id="s28-ul" style="left:150px;top:478px;width:310px;height:10px;border-radius:5px;background:#c8102e"></div>
""" + PIN.format(id="s28-p0", x=1048, y=630, c="#e8b931") + PIN.format(id="s28-p1", x=1440, y=420, c="#f5efe3") + PIN.format(id="s28-p2", x=560, y=560, c="#f5efe3") + """
          <div class="pl gold" id="s28-l0" style="left:930px;top:800px">St. George · 다운타운 본교</div>
          <div class="pl" id="s28-l1" style="left:1440px;top:520px">Scarborough</div>
          <div class="pl" id="s28-l2" style="left:470px;top:660px">Mississauga</div>""",
    js="""
pop('#s28-tip',T('팁 하나'));
draw('#s28-map .mp-out',T('팁 하나'),1.2);draw('#s28-map .mp-lake',T('팁 하나')+0.3,1.0);
inn('#s28-q',T('토론토대 합격'),{y:16});
inn('#s28-cc',T('어느 캠퍼스인지'),{y:12});grow('#s28-ul',T('꼭 확인하세요'),0.5);
const PT=[T('다운타운 본교'),T('스카보로'),T('미시사가')];
for(let i=0;i<3;i++){tl.fromTo('#s28-p'+i,{y:-240,opacity:0},{y:0,opacity:1,duration:0.6,ease:'bounce.out'},PT[i]);inn('#s28-l'+i,PT[i]+0.4,{y:10});}
tl.fromTo('#s28-p0-g',{scale:0.5,opacity:0},{scale:1.4,opacity:1,duration:0.9,yoyo:true,repeat:3,ease:'sine.inOut'},PT[0]+0.5);
""",
    sfx=[("pop", "T('다운타운 본교')+0.45"), ("pop", "T('스카보로')+0.45"), ("pop", "T('미시사가')+0.45")],
)

# ---------------------------------------------------------------- S30 fit checklist
fits = ["대학 목표 + 영어 부족", "관리가 필요한 학생", "학년 손해 없이 빠른 시작"]
fh = "".join(f'<div class="card ft" id="s30-c{i}" style="top:{260 + i * 170}px"><div class="cw">{CHECK.format(w=90)}</div><div class="h" style="font-size:56px">{f}</div></div>' for i, f in enumerate(fits))
S["s30"] = dict(
    css="""
R #s30-bgp img{filter:saturate(.6)}
R .ft{position:absolute;left:330px;width:1260px;height:140px;display:flex;align-items:center;gap:40px;padding:0 50px}
""",
    bg="""        <div class="full" id="s30-bgp" style="opacity:.2"><img src="@P/grad-04-2025-group.jpg" alt="" /></div>""",
    body=f"""
          <div class="abs hd" id="s30-h" style="left:330px;top:150px;font-size:56px">SGA가 <span class="gold">잘 맞는 학생</span></div>{fh}""",
    js="""
kb('#s30-bgp img',0,D,{s:1.0},{s:1.08});
inn('#s30-h',T('정리해 볼게요'),{y:16});
const FT=[T('캐나다나 미국'),T('혼자 관리하는'),T('학년 손해')];
for(let i=0;i<3;i++){inn('#s30-c'+i,FT[i],{x:-60,y:0});draw('#s30-c'+i+' .ck',FT[i]+0.4,0.4);}
""",
    sfx=[("pop", "T('캐나다나 미국')+0.4"), ("pop", "T('혼자 관리하는')+0.4"), ("pop", "T('학년 손해')+0.4")],
)

# ---------------------------------------------------------------- S31 balance scale
S["s31"] = dict(
    css="""
R .pan{position:absolute;top:500px;width:420px;height:170px;border-radius:0 0 200px 200px;background:#f5efe3;color:#14254a;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:44px}
R .pan .s{font-weight:700;font-size:26px;margin-top:6px}
R #s31-msg{left:0;right:0;top:748px;text-align:center;font-size:76px;color:#e8b931;perspective:900px}
""",
    bg="",
    body="""
          <div class="abs" id="s31-post" style="left:952px;top:250px;width:16px;height:420px;background:#f5efe3;border-radius:8px"></div>
          <div class="abs" id="s31-base" style="left:820px;top:660px;width:280px;height:24px;background:#f5efe3;border-radius:12px"></div>
          <div class="abs" id="s31-beam" style="left:500px;top:244px;width:920px;height:16px;background:#e8b931;border-radius:8px"></div>
          <div class="abs" id="s31-lw" style="left:298px;top:252px;width:420px;height:420px">
            <svg class="abs" style="left:0;top:0;width:420px;height:250px" viewBox="0 0 420 250"><path d="M210 0 L20 248 M210 0 L400 248" stroke="rgba(245,239,227,.6)" stroke-width="4" fill="none"/></svg>
            <div class="pan" style="left:0;top:248px">공립<span class="s">비용 최소 · 스스로 부딪히며</span></div></div>
          <div class="abs" id="s31-rw" style="left:1202px;top:252px;width:420px;height:420px">
            <svg class="abs" style="left:0;top:0;width:420px;height:250px" viewBox="0 0 420 250"><path d="M210 0 L20 248 M210 0 L400 248" stroke="rgba(245,239,227,.6)" stroke-width="4" fill="none"/></svg>
            <div class="pan" style="left:0;top:248px">관리형 사립<span class="s">관리 · 대학 준비</span></div></div>
          <div class="abs h" id="s31-msg">정답은 아이마다 다릅니다</div>""",
    js="""
inn(['#s31-post','#s31-base','#s31-beam','#s31-lw','#s31-rw'].map(s=>q(s)),T('반대로'),{y:30,st:0.08});
// beam tilt: + = right side down. pans follow the beam ends (half-length 460px).
function tilt(deg,at,d){const dy=460*Math.sin(deg*Math.PI/180);
  tl.to('#s31-beam',{rotation:deg,duration:d,ease:'sine.inOut'},at);tl.to('#s31-lw',{y:-dy,duration:d,ease:'sine.inOut'},at);tl.to('#s31-rw',{y:dy,duration:d,ease:'sine.inOut'},at);}
tilt(-7,T('비용을'),1.2);tilt(5,T('현지 학생들'),1.2);tilt(-6,T('공립이 더'),1.2);tilt(0,T('정답은'),1.0);
kin('#s31-msg',T('정답은')+0.2,0.04);
""",
    sfx=[],
)

# ---------------------------------------------------------------- S32 CTA (mascot 4/4, particles)
S["s32"] = dict(
    css="""
R .q1{position:absolute;font-weight:900;font-size:60px;white-space:nowrap}
R #s32-btn{left:560px;top:600px;width:800px;height:110px;border-radius:60px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:48px;box-shadow:0 16px 40px rgba(200,16,46,.45)}
R .pt{position:absolute;left:960px;top:420px;width:12px;height:12px;border-radius:50%;background:#e8b931}
R #s32-oly{left:1580px;top:500px;width:280px;height:296px}
""",
    bg="",
    body="""
          <div class="q1" id="s32-q1" style="left:200px;top:200px">우리 아이, <span class="gold">몇 학점</span> 필요할까?</div>
          <div class="q1" id="s32-q2" style="left:420px;top:320px"><span class="gold">언제</span> 입학하는 게 좋을까?</div>
          <div class="card" id="s32-doc" style="left:640px;top:450px;width:640px;height:110px;display:flex;align-items:center;justify-content:center"><div class="t" style="font-size:44px">성적표 → AA Canada</div></div>
          <div class="abs" id="s32-cta" style="inset:0">
            <div class="abs" id="s32-pts" style="inset:0"></div>
            <div class="abs h" id="s32-aa" style="left:0;right:0;top:200px;text-align:center;font-size:150px;letter-spacing:.02em">AA CANADA</div>
            <div class="abs hd" id="s32-l1" style="left:0;right:0;top:390px;text-align:center;font-size:44px">캐나다 관리형 조기유학 · 자녀무상교육 · 유학 후 이민</div>
            <div class="abs hd" id="s32-l2" style="left:0;right:0;top:470px;text-align:center;font-size:38px;color:#e8b931">토론토 · 몬트리올 · 버논 · 밴쿠버</div>
            <div class="abs" id="s32-btn">무료 학점 계산 · 카톡 canlog</div>
            <div class="abs b" id="s32-tel" style="left:0;right:0;top:735px;text-align:center;font-size:34px;color:rgba(255,255,255,.85)">02-567-4345</div>
            <div class="abs" id="s32-oly"><img src="@B/oly-1.png" alt="" style="width:100%;height:100%;object-fit:contain" /></div></div>""",
    js="""
inn('#s32-q1',T('우리 아이에게'),{x:-40,y:0});inn('#s32-q2',T('언제 입학하는'),{x:40,y:0});
inn('#s32-doc',T('성적표를'),{y:30});
outt(['#s32-q1','#s32-q2','#s32-doc'].map(s=>q(s)),T('SGA와 함께')-0.3,{y:-30});
const CT=T('SGA와 함께');
mask('#s32-aa',CT,0.8,'l');inn('#s32-l1',CT+0.5,{y:14});inn('#s32-l2',CT+0.8,{y:14});
slam('#s32-btn',T('카카오톡'),{s:1.6});inn('#s32-tel',T('카카오톡')+0.4,{y:10});
const pulseAt=T('카카오톡')+0.6;tl.fromTo('#s32-btn',{scale:1},{scale:1.06,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:Math.max(1,Math.floor((D-pulseAt)/0.6)-1)},pulseAt);
let seed=11;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
for(let i=0;i<46;i++){const d=document.createElement('div');d.className='pt';d.style.opacity='0';q('#s32-pts').appendChild(d);const a=rnd()*Math.PI*2,r=300+rnd()*600;
  tl.fromTo(d,{x:0,y:0,opacity:1,scale:0.6+rnd()},{x:Math.cos(a)*r,y:Math.sin(a)*r*0.6+120,opacity:0,duration:1.4+rnd()*0.8,ease:'power3.out',immediateRender:false},T('카카오톡')+0.1);}
tl.fromTo('#s32-oly',{opacity:0,y:80},{opacity:1,y:0,duration:0.6,ease:'back.out(1.8)'},T('카카오톡')+0.3);
tl.fromTo('#s32-oly',{rotation:0,transformOrigin:'50% 90%'},{rotation:8,duration:0.35,ease:'sine.inOut',yoyo:true,repeat:5},T('카카오톡')+0.9);
""",
    sfx=[("impact", "T('카카오톡')+0.42"), ("whoosh", "T('SGA와 함께')")],
)
