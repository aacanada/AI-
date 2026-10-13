"""Scenes 08-14."""

P = "assets/photos/"
S = {}

# ---------------------------------------------------------------- 08 day
S["08-day"] = dict(
    bg="",
    css="""
R .tr{position:absolute;left:120px;width:900px}
R .tm{position:absolute;left:0;top:0;width:220px;font-weight:800;font-size:30px;color:#4A5F78;font-variant-numeric:tabular-nums}
R .bk{position:absolute;left:240px;top:0;width:660px;border-radius:22px;padding:22px 30px;color:#fff}
R .bk .k{font-weight:700;font-size:22px;letter-spacing:.08em;opacity:.9}
R .bk .v{font-weight:800;font-size:40px;margin-top:6px}
R .bk .s{font-weight:600;font-size:26px;margin-top:6px;opacity:.95}
""",
    body=f"""
          <div class="abs hd" id="s08-t" style="left:120px;top:92px;font-size:66px">하루 일과</div>
          <div class="abs l" id="s08-t2" style="left:470px;top:122px;font-size:26px;color:#146A77">월요일 – 금요일 · 주 30레슨</div>
          <div class="tr" id="s08-r0" style="top:210px;height:250px"><div class="tm">08:30<br />– 12:00</div>
            <div class="bk" style="height:250px;background:#1F8A99"><div class="k">MORNING · EAP</div><div class="v">아카데믹 영어 과정</div><div class="s">듣기 · 말하기 · 읽기 · 쓰기</div><div class="s">EAP 100 기초 · 200 중급 · 300 고급</div></div></div>
          <div class="tr" id="s08-r1" style="top:480px;height:90px"><div class="tm">12:00</div>
            <div class="bk" style="height:90px;background:#F1EADF;color:#16324F;padding-top:20px"><div class="v" style="margin:0;font-size:36px">점심 시간</div></div></div>
          <div class="tr" id="s08-r2" style="top:590px;height:270px"><div class="tm">13:00<br />– 14:45</div>
            <div class="bk" style="height:270px;background:#16324F"><div class="k" style="color:#F3C969">AFTERNOON</div><div class="v">공립학교 준비 과정</div><div class="s">과목별 필수 어휘</div><div class="s">발표 · 그룹 프로젝트</div></div></div>
          <div class="chip sand" id="s08-wat" style="left:1110px;top:200px">워털루 대학 감수 프로그램</div>
          <div class="pol" id="s08-p0" style="left:1150px;top:290px;width:600px;height:470px"><div class="ph"><img src="{P}63-campus-classroom.jpg" alt="" /></div><div class="cap">morning class</div></div>
          <div class="pol" id="s08-p1" style="left:1180px;top:280px;width:560px;height:440px"><div class="ph"><img src="{P}64-campus-lounge.jpg" alt="" /></div><div class="cap">student lounge</div></div>
          <div class="pol" id="s08-p2" style="left:1130px;top:300px;width:620px;height:470px"><div class="ph"><img src="{P}16-classroom-overhead.jpg" alt="" /></div><div class="cap">group project</div></div>""",
    marks={"wat": "워털루", "lunch": "오후에는"},
    js="""
inn('#s08-t',R[0]-0.2,{y:24});inn('#s08-t2',R[0]+0.3,{y:12});
inn('#s08-r0',R[1],{x:-40,y:0});pol('#s08-p0',R[1]+0.3,-3);kb('#s08-p0 img',R[1]+0.3,6,{s:1},{s:1.1});
inn('#s08-wat',M.wat,{s:0.7,y:0});
inn('#s08-r1',R[2]-1.4,{x:-40,y:0});
tl.to('#s08-p0',{opacity:0,x:-200,rotation:-10,duration:0.4,ease:'power2.in'},R[2]-1.6);outt('#s08-wat',R[2]-1.6);
pol('#s08-p1',R[2]-1.2,4);
inn('#s08-r2',R[2],{x:-40,y:0});
tl.to('#s08-p1',{opacity:0,x:-200,rotation:-10,duration:0.4,ease:'power2.in'},R[2]+1.6);
pol('#s08-p2',R[2]+1.8,-2);kb('#s08-p2 img',R[2]+1.8,D-R[2]-1.8,{s:1},{s:1.08});
""",
)

# ---------------------------------------------------------------- 09 life
S["09-life"] = dict(
    bg="""        <div class="glow warm" style="left:1200px;top:-200px;width:800px;height:800px"></div>""",
    css="""
R .ic{position:absolute;top:470px;width:420px;height:200px;border-radius:28px;background:#fff;box-shadow:0 12px 28px rgba(22,50,79,.14);padding:30px 34px}
R .ic .k{font-weight:700;font-size:24px;letter-spacing:.08em;color:#146A77}
R .ic .v{font-weight:900;font-size:64px;margin-top:8px}
""",
    body=f"""
          <div class="abs hd" id="s09-t" style="left:120px;top:92px;font-size:66px">생활 적응</div>
          <div class="abs h" id="s09-q" style="left:120px;top:250px;font-size:72px;line-height:1.25">잘 먹고, 잘 자는 아이가<br /><span style="color:#146A77">적응도 빠릅니다</span></div>
          <div class="ic" id="s09-i0" style="left:120px"><div class="k">EAT</div><div class="v">잘 먹고</div></div>
          <div class="ic" id="s09-i1" style="left:580px"><div class="k">SLEEP</div><div class="v">잘 자고</div></div>
          <div class="pol" id="s09-p0" style="left:1150px;top:180px;width:560px;height:420px"><div class="ph"><img src="{P}20-host-family.jpg" alt="" /></div><div class="cap">host family</div></div>
          <div class="pol" id="s09-p1" style="left:1040px;top:470px;width:420px;height:340px"><div class="ph"><img src="{P}22-homestay-kitchen.jpg" alt="" /></div><div class="cap">dinner time</div></div>
          <div class="pol" id="s09-p2" style="left:1440px;top:500px;width:380px;height:320px"><div class="ph"><img src="{P}21-homestay-house.jpg" alt="" /></div><div class="cap">home</div></div>
          <div class="chip lake" id="s09-c0" style="left:120px;top:250px">어린 학생일수록 더 세심한 홈스테이 배정</div>
          <div class="chip" id="s09-c1" style="left:120px;top:330px">캐나다 가정에서 사는 법, 켈로나에서 먼저</div>
          <div class="abs" id="s09-g" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs hd" style="left:120px;top:200px;font-size:44px">첫 한 달의 적응기를, 입학 전에</div>
            <svg class="abs" style="left:120px;top:290px;width:1680px;height:520px" viewBox="0 0 1680 520">
              <rect x="0" y="0" width="760" height="460" rx="20" fill="#1F8A99" opacity=".12"/>
              <rect x="760" y="0" width="920" height="460" rx="20" fill="#16324F" opacity=".06"/>
              <line x1="0" y1="460" x2="1680" y2="460" stroke="#16324F" stroke-width="4"/>
              <path id="s09-curve" d="M20 120 C 180 120, 250 400, 400 380 C 540 360, 620 140, 760 110 C 1000 70, 1300 70, 1660 60" fill="none" stroke="#E8572B" stroke-width="10" stroke-linecap="round"/>
            </svg>
            <div class="abs l" style="left:150px;top:310px;font-size:26px;color:#146A77">켈로나 · 준비 과정</div>
            <div class="abs l" style="left:910px;top:310px;font-size:26px;color:#16324F">버논 · 공립학교 입학</div>
            <div class="abs b" style="left:330px;top:690px;font-size:30px;color:#E8572B">낯선 첫 한 달</div>
            <div class="abs b" style="left:1240px;top:430px;font-size:30px;color:#3A7016">부드러운 시작</div>
          </div>""",
    marks={"home": "홈스테이를", "kel": "켈로나에서", "first": "첫 한 달"},
    js="""
inn('#s09-t',R[0]-0.2,{y:24});
inn('#s09-q',R[0]+0.2,{y:30});
inn('#s09-i0',R[0]+3.6,{y:40});inn('#s09-i1',R[0]+4.4,{y:40});
tl.to(['#s09-q','#s09-i0','#s09-i1'],{opacity:0,y:-30,duration:0.4,ease:'power2.in'},R[1]-0.4);
inn('#s09-c0',M.home-0.4,{x:-30,y:0});
pol('#s09-p0',R[1],-3);pol('#s09-p1',R[1]+0.8,4);pol('#s09-p2',R[1]+1.6,-2);
qa('#s09-p0 img,#s09-p1 img,#s09-p2 img').forEach((im,i)=>kb(im,R[1]+i*0.8,R[2]-R[1],{s:1},{s:1.08}));
inn('#s09-c1',M.kel-0.4,{x:-30,y:0});
tl.to(['#s09-c0','#s09-c1','#s09-p0','#s09-p1','#s09-p2'],{opacity:0,y:-30,duration:0.4,ease:'power2.in'},R[2]-0.4);
tl.fromTo('#s09-g',{opacity:0},{opacity:1,duration:0.5},R[2]-0.1);
draw('#s09-curve',R[2]+0.6,3.2);
""",
)

# ---------------------------------------------------------------- 10 duration
MONTHS = ["3월", "4월", "5월", "6월", "7월", "8월", "9월"]
_mx = lambda i: 420 + i * 200  # noqa: E731
_months = "\n".join(
    f'          <div class="mo" id="s10-m{i}" style="left:{_mx(i)}px">{m}</div>' for i, m in enumerate(MONTHS))
S["10-duration"] = dict(
    bg="",
    css="""
R .mo{position:absolute;top:470px;width:200px;text-align:center;font-weight:800;font-size:30px;color:#4A5F78;border-left:2px solid rgba(22,50,79,.18)}
R .tk{position:absolute;height:76px;border-radius:18px;color:#fff;font-weight:800;font-size:30px;line-height:76px;padding-left:24px;white-space:nowrap;transform-origin:0 50%}
R .tlab{position:absolute;left:120px;width:280px;font-weight:800;font-size:30px;line-height:1.25}
""",
    body=f"""
          <div class="abs hd" id="s10-t" style="left:120px;top:92px;font-size:66px">준비 기간은 선택할 수 있습니다</div>
          <div class="abs" id="s10-sl" style="left:120px;top:250px;width:1680px;height:140px">
            <div class="abs" style="left:0;top:58px;width:1680px;height:16px;border-radius:8px;background:rgba(22,50,79,.12)"></div>
            <div class="abs" id="s10-fill" style="left:0;top:58px;width:1680px;height:16px;border-radius:8px;background:#1F8A99;transform-origin:0 50%"></div>
            <div class="abs" id="s10-knob" style="left:0;top:36px;width:60px;height:60px;border-radius:50%;background:#E8572B;box-shadow:0 6px 16px rgba(232,87,43,.4)"></div>
            <div class="abs h" style="left:0;top:96px;font-size:40px">8주</div>
            <div class="abs h" style="left:1580px;top:96px;font-size:40px">24주</div>
            <div class="abs h" id="s10-wk" style="left:720px;top:-30px;width:240px;text-align:center;font-size:56px;color:#E8572B;font-variant-numeric:tabular-nums">8주</div>
          </div>
          <div class="abs" id="s10-cal" style="left:0;top:0;width:1920px;height:1080px">
{_months}
            <div class="tlab" id="s10-la" style="top:540px">여름방학<br /><span style="color:#146A77;font-size:24px">8주 집중</span></div>
            <div class="tk" id="s10-a" style="left:{_mx(3) + 190}px;top:540px;width:{int(200 * 1.75)}px;background:#1F8A99">6.29 – 8.21</div>
            <div class="tlab" id="s10-lb" style="top:650px">3월 시작<br /><span style="color:#146A77;font-size:24px">최대 24주</span></div>
            <div class="tk" id="s10-b" style="left:{_mx(0) + 10}px;top:650px;width:{200 * 6 - 20}px;background:#16324F">3월 – 8월 · 최대 24주</div>
            <div class="abs" id="s10-flag" style="left:{_mx(6) + 20}px;top:530px;width:170px;height:200px;border-radius:20px;background:#E8572B;color:#fff;text-align:center;padding-top:40px"><div class="hd" style="font-size:30px">9월</div><div class="h" style="font-size:36px;margin-top:6px">버논<br />입학</div></div>
          </div>
          <div class="chip solid" id="s10-c0" style="left:120px;top:780px">만 13세 이상</div>
          <div class="chip solid" id="s10-c1" style="left:380px;top:780px">주 30레슨</div>
          <div class="chip" id="s10-c2" style="left:620px;top:780px">월요일 – 금요일</div>""",
    marks={"sum": "여름방학", "mar": "3월에", "sep": "9월"},
    js="""
inn('#s10-t',R[0]-0.2,{y:24});
inn('#s10-sl',R[0]+0.3,{y:30});
tl.fromTo('#s10-fill',{scaleX:0},{scaleX:1,duration:2.2,ease:'power2.inOut'},R[0]+1.2);
tl.fromTo('#s10-knob',{x:0},{x:1620,duration:2.2,ease:'power2.inOut'},R[0]+1.2);
count('#s10-wk',8,24,R[0]+1.2,2.2,v=>Math.round(v)+'주');
qa('.mo').forEach((m,i)=>inn(m,M.sum-0.6+i*0.06,{y:16,d:0.4}));
inn('#s10-la',M.sum,{x:-20,y:0});grow('#s10-a',M.sum+0.3,0.8);
inn('#s10-lb',M.mar-0.2,{x:-20,y:0});grow('#s10-b',M.mar+0.2,1.6);
inn('#s10-flag',M.sep,{y:-60,e:'back.out(2)'});
inn('#s10-c0',R[2],{s:0.7,y:0});inn('#s10-c1',R[2]+2.2,{s:0.7,y:0});inn('#s10-c2',R[2]+2.6,{s:0.7,y:0});
""",
)

# ---------------------------------------------------------------- 11 fees
FEES = [("8주", "$500"), ("9 – 24주", "$450"), ("디지털 교재비", "+ $20")]
_fees = "\n".join(
    f'          <div class="fr" id="s11-r{i}" style="top:{290 + i * 130}px"><div class="a">{a}</div><div class="b"><span>주당</span> {b}</div></div>'
    for i, (a, b) in enumerate(FEES))
EX = [("8주", "$4,160"), ("12주", "$5,640"), ("24주", "$11,280")]
_ex = "\n".join(
    f'          <div class="ex" id="s11-e{i}" style="top:{290 + i * 150}px"><div class="a">{a}</div><div class="b">{b}</div></div>' for i, (a, b) in enumerate(EX))
S["11-fees"] = dict(
    bg="",
    css="""
R .fr{position:absolute;left:120px;width:960px;height:110px;border-radius:22px;background:#fff;border:3px solid rgba(22,50,79,.14)}
R .fr .a{position:absolute;left:36px;top:28px;font-weight:800;font-size:42px}
R .fr .b{position:absolute;right:40px;top:18px;font-weight:900;font-size:60px;color:#146A77;font-variant-numeric:tabular-nums}
R .fr .b span{font-weight:700;font-size:28px;color:#4A5F78}
R .ex{position:absolute;left:1200px;width:600px;height:120px;border-radius:22px;background:#16324F;color:#FAF6EF}
R .ex .a{position:absolute;left:34px;top:36px;font-weight:800;font-size:36px}
R .ex .b{position:absolute;right:34px;top:24px;font-weight:900;font-size:58px;color:#F3C969;font-variant-numeric:tabular-nums}
""",
    body=f"""
          <div class="abs hd" id="s11-t" style="left:120px;top:92px;font-size:66px">학비</div>
          <div class="abs l" id="s11-u" style="left:300px;top:122px;font-size:26px;color:#146A77">주 단위 · 캐나다 달러(CAD)</div>
          <div class="abs l" id="s11-h0" style="left:124px;top:236px;font-size:24px;color:#4A5F78">수업료 (주 30레슨)</div>
{_fees}
          <div class="abs l" id="s11-h1" style="left:1204px;top:236px;font-size:24px;color:#4A5F78">예시 · 수업료 + 교재비</div>
{_ex}
          <div class="abs b" id="s11-note" style="left:120px;top:760px;font-size:26px;color:#4A5F78">2026년 10월 기준 · 변동 가능 · 홈스테이, 보험 등은 별도</div>""",
    marks={"500": "500달러", "450": "450달러", "20": "20달러"},
    js="""
inn('#s11-t',R[0]-0.2,{y:24});inn('#s11-u',R[0]+0.3,{y:12});
inn('#s11-h0',R[1]-0.4,{y:10});
['#s11-r0','#s11-r1','#s11-r2'].forEach((r,i)=>inn(r,R[1]-0.2+i*0.25,{x:-40,y:0}));
[['#s11-r0',M['500']],['#s11-r1',M['450']],['#s11-r2',M['20']]].forEach(([r,t])=>{tl.to(r,{borderColor:'#1F8A99',duration:0.25},t-0.2);tl.fromTo(r,{scale:1},{scale:1.03,duration:0.25,yoyo:true,repeat:1,ease:'sine.inOut'},t-0.2);tl.to(r,{borderColor:'rgba(22,50,79,.14)',duration:0.4},t+1.6);});
inn('#s11-h1',M['20']+1.4,{y:10});
qa('.ex').forEach((e,i)=>inn(e,M['20']+1.6+i*0.5,{x:40,y:0}));
inn('#s11-note',M['20']+3.0,{y:10});
""",
)

# ---------------------------------------------------------------- 12 one-to-one
OTO = [("2 – 11주", "$340"), ("12 – 23주", "$320"), ("24주", "$300")]
_oto = "\n".join(
    f'          <div class="or" id="s12-o{i}" style="top:{560 + i * 90}px"><span class="a">{a}</span><span class="b">주당 {b}</span></div>' for i, (a, b) in enumerate(OTO))
S["12-one-to-one"] = dict(
    bg="""        <div class="glow warm" style="left:-200px;top:-200px;width:900px;height:900px"></div>""",
    css="""
R .sl2{position:absolute;left:120px;height:110px;border-radius:22px;color:#fff;padding:20px 30px}
R .sl2 .k{font-weight:700;font-size:22px;letter-spacing:.08em;opacity:.9}
R .sl2 .v{font-weight:800;font-size:36px;margin-top:4px}
R .or{position:absolute;left:1180px;width:620px;height:76px;border-bottom:2px solid rgba(22,50,79,.15)}
R .or .a{position:absolute;left:10px;top:18px;font-weight:700;font-size:32px}
R .or .b{position:absolute;right:10px;top:12px;font-weight:900;font-size:42px;color:#146A77}
""",
    body="""
          <div class="abs l" id="s12-k" style="left:124px;top:110px;font-size:28px;color:#E8572B">OPTION</div>
          <div class="abs h" id="s12-big" style="left:120px;top:150px;font-size:130px">1:1 수업</div>
          <div class="abs hd" id="s12-sub" style="left:124px;top:310px;font-size:46px">단기간에 영어 실력을 <span style="background:linear-gradient(transparent 60%,#F3C969 60%)">최대한</span> 끌어올리고 싶다면</div>
          <div class="abs l" id="s12-dl" style="left:124px;top:420px;font-size:24px;color:#4A5F78">오후 일과에 더하기</div>
          <div class="sl2" id="s12-a" style="top:470px;width:620px;background:#16324F"><div class="k">13:00 – 14:45</div><div class="v">공립학교 준비 과정</div></div>
          <div class="sl2" id="s12-b" style="top:600px;width:620px;background:#E8572B"><div class="k">14:50 이후</div><div class="v">1:1 수업 · 주 4레슨</div></div>
          <div class="chip lake" id="s12-c" style="left:120px;top:760px">우리 아이의 약한 부분만 집중</div>
          <div class="abs l" id="s12-oh" style="left:1184px;top:500px;font-size:24px;color:#4A5F78">1:1 수업료 · 등록 기간별</div>
{_oto}
          <div class="abs b" id="s12-on" style="left:1184px;top:840px;font-size:24px;color:#4A5F78">교재비 주당 $20 별도</div>""".replace("{_oto}", _oto),
    marks={"after": "오후 수업이", "weak": "약한 부분", "price": "340달러"},
    js="""
inn('#s12-k',R[0]-0.2,{y:10});inn('#s12-big',R[0],{y:30,s:0.9});inn('#s12-sub',R[0]+1.0,{y:20});
inn('#s12-dl',M.after-0.6,{y:10});inn('#s12-a',M.after-0.4,{x:-40,y:0});
inn('#s12-b',M.after+0.6,{x:-40,y:0});
tl.fromTo('#s12-b',{scale:1},{scale:1.04,duration:0.3,yoyo:true,repeat:1,ease:'sine.inOut'},M.after+1.4);
inn('#s12-c',M.weak,{s:0.7,y:0});
inn('#s12-oh',M.price-0.8,{y:10});
qa('.or').forEach((o,i)=>inn(o,M.price-0.6+i*0.3,{x:40,y:0}));
inn('#s12-on',M.price+0.8,{y:10});
""",
)

# ---------------------------------------------------------------- 13 big picture
STEPS = [("켈로나", "밴웨스트 영어 준비", "#1F8A99"), ("버논", "공립고 11학년 입학", "#16324F"), ("버논", "12학년 졸업", "#4E8A1E")]
_steps = "\n".join(
    f'          <div class="stp" id="s13-s{i}" style="left:{120 + i * 470}px;background:{c}"><div class="k">{k}</div><div class="v">{v}</div></div>'
    for i, (k, v, c) in enumerate(STEPS))
S["13-big-picture"] = dict(
    bg="",
    css="""
R .dt{position:absolute;width:30px;height:30px;border-radius:50%}
R .stp{position:absolute;top:330px;width:400px;height:190px;border-radius:26px;color:#fff;padding:32px 34px}
R .stp .k{font-weight:700;font-size:26px;letter-spacing:.06em;opacity:.9}
R .stp .v{font-weight:800;font-size:42px;margin-top:10px;line-height:1.25}
R .uni{position:absolute;left:1580px;width:260px;height:110px;border-radius:22px;background:#FAF6EF;border:4px solid #16324F;text-align:center;font-weight:900;font-size:38px;line-height:102px}
""",
    body=f"""
          <div class="abs" id="s13-mix" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs hd" style="left:120px;top:92px;font-size:66px">함께 공부하는 친구들</div>
            <div class="abs" id="s13-dots" style="left:124px;top:260px;width:600px;height:300px"></div>
            <div class="abs hd" style="left:124px;top:560px;font-size:34px"><span style="color:#1F8A99">●</span> 일본 학생 &nbsp; <span style="color:#E8572B">●</span> 한국 학생</div>
            <div class="abs" id="s13-stamp" style="left:960px;top:280px;width:820px;height:260px;border:8px solid #16324F;border-radius:30px;padding:46px 50px">
              <div class="hd" style="font-size:52px;line-height:1.3">학생 수가 적어도<br /><span style="color:#E8572B">약속한 과정은 그대로</span></div></div>
            <div class="pol" id="s13-ph" style="left:1320px;top:590px;width:420px;height:300px"><div class="ph"><img src="{P}62-campus-hallway.jpg" alt="" /></div><div class="cap">VanWest Kelowna</div></div>
          </div>
          <div class="abs" id="s13-road" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs hd" style="left:120px;top:92px;font-size:66px">큰 그림</div>
{_steps}
            <svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">
              <path id="s13-a0" d="M528 425 H582" stroke="#16324F" stroke-width="8" stroke-linecap="round"/>
              <path id="s13-a1" d="M998 425 H1052" stroke="#16324F" stroke-width="8" stroke-linecap="round"/>
              <path id="s13-f0" d="M1470 425 C 1520 425, 1520 300, 1570 300" fill="none" stroke="#E8572B" stroke-width="8" stroke-linecap="round"/>
              <path id="s13-f1" d="M1470 425 C 1520 425, 1520 560, 1570 560" fill="none" stroke="#E8572B" stroke-width="8" stroke-linecap="round"/>
            </svg>
            <div class="uni" id="s13-u0" style="top:245px">한국 대학</div>
            <div class="uni" id="s13-u1" style="top:505px">영어권 대학</div>
            <div class="abs h" id="s13-k" style="left:120px;top:680px;font-size:72px">영어 기초가 탄탄하면, <span style="color:#146A77">선택의 폭이 넓어집니다</span></div>
          </div>""",
    marks={"few": "적더라도", "adm": "11학년", "grad": "12학년", "kor": "한국 대학이든", "eng": "영어권 대학"},
    js="""
(function(){const g=q('#s13-dots');for(let i=0;i<40;i++){const d=document.createElement('div');d.className='dt';d.style.background=(i%10)<5?'#1F8A99':'#E8572B';d.style.left=(i%10)*58+'px';d.style.top=Math.floor(i/10)*58+'px';g.appendChild(d);}})();
qa('#s13-dots .dt').forEach((d,i)=>tl.fromTo(d,{scale:0},{scale:1,duration:0.3,ease:'back.out(2)'},R[0]+0.3+(i%10)*0.06+Math.floor(i/10)*0.05));
inn('#s13-stamp',M.few-0.4,{s:1.4,y:0,d:0.45,e:'power4.out'});
pol('#s13-ph',M.few+1.2,3);
tl.to('#s13-mix',{opacity:0,duration:0.5},R[1]-0.4);
tl.fromTo('#s13-road',{opacity:0},{opacity:1,duration:0.4},R[1]-0.2);
inn('#s13-s0',R[1],{y:40});
draw('#s13-a0',M.adm-0.6,0.4);inn('#s13-s1',M.adm-0.4,{y:40});
draw('#s13-a1',M.grad-0.6,0.4);inn('#s13-s2',M.grad-0.4,{y:40});
draw('#s13-f0',M.kor-0.4,0.6);inn('#s13-u0',M.kor,{x:-20,y:0});
draw('#s13-f1',M.eng-0.4,0.6);inn('#s13-u1',M.eng,{x:-20,y:0});
inn('#s13-k',M.eng+1.0,{y:24});
""",
)

# ---------------------------------------------------------------- 14 CTA
S["14-cta"] = dict(
    bg="",
    css="""
R .bg{background:#16324F}
""",
    body=f"""
          <div class="full" id="s14-photo"><img src="{P}04-students-canada-flag.jpg" alt="" style="object-position:50% 30%" /></div>
          <div class="abs" id="s14-bar" style="left:0;top:600px;width:1920px;height:300px;background:rgba(22,50,79,.95)"></div>
          <div class="abs l" id="s14-k" style="left:120px;top:650px;font-size:28px;color:#7FD3DE">버논 조기유학 · 켈로나 공립학교 준비 과정</div>
          <div class="abs hd" id="s14-m" style="left:120px;top:700px;font-size:54px;color:#FAF6EF;line-height:1.3">우리 아이에게 필요한 준비 기간,<br /><span style="color:#F3C969">AA캐나다가 함께 계산해 드립니다</span></div>
          <div class="card" id="s14-aa" style="left:1300px;top:630px;width:520px;height:240px;padding:28px 34px;background:#FAF6EF"><div class="h" style="font-size:54px">AA캐나다</div><div class="hd" style="font-size:36px;margin-top:14px">전화 02-567-4345</div><div class="hd" style="font-size:36px;margin-top:6px">카카오톡 <span style="color:#146A77">canlog</span></div></div>""",
    marks={},
    js="""
tl.fromTo('#s14-photo',{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(75% at 50% 50%)',duration:1.1,ease:'power3.inOut'},0.1);
kb('#s14-photo img',0.1,D,{s:1.0},{s:1.08});
tl.fromTo('#s14-bar',{yPercent:100,opacity:0},{yPercent:0,opacity:1,duration:0.7,ease:'power3.out'},R[0]-0.3);
inn('#s14-k',R[0],{y:12});inn('#s14-m',R[0]+0.3,{y:20});
inn('#s14-aa',R[1]-0.4,{x:60,y:0,d:0.7});
tl.fromTo('#s14-aa',{scale:1},{scale:1.04,duration:0.4,yoyo:true,repeat:1,ease:'sine.inOut'},R[1]+2.0);
""",
)
