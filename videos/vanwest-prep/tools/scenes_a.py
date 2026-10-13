"""Scenes 01-07. Coordinates are 1920x1080 px.
R = row start times, M = keyword times (from `marks`), both relative to the scene."""

P = "assets/photos/"
S = {}

# ---------------------------------------------------------------- 01 hook
BUBBLES = [("Hi! Where are you from?", 150, 210, -3), ("Open your textbook to page 42.", 980, 170, 2),
           ("Group project due Friday!", 260, 430, 2), ("Want to sit with us at lunch?", 1060, 400, -2)]
_bub = "\n".join(
    f'          <div class="bub" id="s01-b{i}" style="left:{x}px;top:{y}px">{t}</div>' for i, (t, x, y, r) in enumerate(BUBBLES))
S["01-hook"] = dict(
    bg=f"""        <div class="full" id="s01-photo"><img src="{P}15-classroom-teacher.jpg" alt="" /></div>
        <div class="abs" id="s01-shade" style="inset:0;background:linear-gradient(180deg,rgba(22,50,79,.35) 0%,rgba(22,50,79,.55) 55%,rgba(22,50,79,.9) 100%)"></div>""",
    css="""
R .bub{position:absolute;background:#FAF6EF;color:#16324F;font-weight:700;font-size:38px;padding:20px 34px;border-radius:30px;white-space:nowrap;box-shadow:0 14px 30px rgba(0,0,0,.25)}
R .place{position:absolute;top:620px;width:420px;height:150px;border-radius:26px;background:rgba(250,246,239,.95);padding:24px 30px}
R .place .k{font-weight:700;font-size:24px;letter-spacing:.08em;color:#146A77}
R .place .v{font-weight:800;font-size:44px;margin-top:6px;color:#16324F}
""",
    body=f"""
{_bub}
          <div class="place" id="s01-p0" style="left:150px"><div class="k">SEAT</div><div class="v">옆자리</div></div>
          <div class="place" id="s01-p1" style="left:610px"><div class="k">HALLWAY</div><div class="v">복도</div></div>
          <div class="place" id="s01-p2" style="left:1070px"><div class="k">CAFETERIA</div><div class="v">점심시간 식당</div></div>
          <div class="abs" id="s01-zero" style="left:1530px;top:560px;width:260px;height:260px;border-radius:50%;background:#E8572B;color:#fff;text-align:center">
            <div class="l" style="margin-top:62px;font-size:24px">한국어 대화</div><div class="h" style="font-size:110px">0</div></div>
          <div class="abs h" id="s01-t1" style="left:150px;top:300px;font-size:96px;color:#FAF6EF">출발 전의 준비가</div>
          <div class="abs h" id="s01-t2" style="left:150px;top:430px;font-size:96px;color:#FAF6EF"><span style="color:#F3C969">첫 학기</span>를 결정합니다</div>
          <div class="abs l" id="s01-t0" style="left:156px;top:240px;font-size:28px;color:#95DAE4">버논 조기유학</div>""",
    marks={"seat": "옆자리", "hall": "복도", "cafe": "식당", "none": "거의 없습니다"},
    js="""
kb('#s01-photo img',0,D,{s:1.12},{s:1.0});
qa('.bub').forEach((b,i)=>{tl.fromTo(b,{opacity:0,scale:0.4,rotation:0},{opacity:1,scale:1,rotation:[-3,2,2,-2][i],duration:0.5,ease:'back.out(2)'},R[0]+0.5+i*0.9);});
tl.to(qa('.bub'),{opacity:0,y:-40,duration:0.4,ease:'power2.in',stagger:0.05},R[1]-0.3);
inn('#s01-p0',M.seat,{y:40});inn('#s01-p1',M.hall,{y:40});inn('#s01-p2',M.cafe,{y:40});
inn('#s01-zero',M.none,{s:0.3,y:0,e:'back.out(2)'});
tl.to(['#s01-p0','#s01-p1','#s01-p2','#s01-zero'],{opacity:0,y:40,duration:0.4,ease:'power2.in'},R[2]-0.3);
tl.to('#s01-shade',{opacity:1,duration:0.1},0);
tl.to('#s01-photo',{opacity:0.45,duration:0.8},R[2]-0.3);
inn('#s01-t0',R[2],{y:16});inn('#s01-t1',R[2]+0.3,{y:30});inn('#s01-t2',R[2]+2.2,{y:30});
""",
)

# ---------------------------------------------------------------- 02 english-only
S["02-english-only"] = dict(
    bg="""        <div class="glow" style="left:-200px;top:200px;width:900px;height:900px"></div>""",
    css="""
R .dot{position:absolute;width:26px;height:26px;border-radius:50%;background:#1F8A99}
R .dot.k{background:#E8572B}
R .cmp{position:absolute;top:250px;width:390px;height:430px;border-radius:28px;padding:34px}
R .cmp .k{font-weight:700;font-size:24px;letter-spacing:.08em}
R .cmp .n{font-weight:900;font-size:56px;margin:6px 0 24px}
R .cmp .i{font-weight:600;font-size:32px;line-height:1.55}
R .seat{position:absolute;top:0;width:58px;height:58px;border-radius:14px;background:rgba(22,50,79,.14)}
R .seat.on{background:#E8572B}
""",
    body=f"""
          <div class="sticker" id="s02-st" style="left:120px;top:96px">추천 포인트 01</div>
          <div class="abs hd" id="s02-t" style="left:120px;top:150px;font-size:66px">영어만 쓰는 환경</div>
          <div class="abs" id="s02-grid" style="left:124px;top:290px;width:330px;height:330px"></div>
          <div class="abs h" id="s02-pct" style="left:500px;top:300px;font-size:150px;color:#146A77;font-variant-numeric:tabular-nums">0%</div>
          <div class="abs hd" id="s02-pctl" style="left:506px;top:480px;font-size:40px">현지 캐나다 학생</div>
          <div class="abs b" id="s02-src" style="left:508px;top:540px;font-size:26px;color:#4A5F78">버논 교육청(SD22) 공립학교</div>
          <div class="pol" id="s02-ph" style="left:1180px;top:200px;width:560px;height:560px"><div class="ph"><img src="{P}18-students-lockers.jpg" alt="" /></div><div class="cap">Vernon classroom</div></div>
          <div class="cmp" id="s02-c1" style="left:1000px;background:#F1EADF"><div class="k" style="color:#4A5F78">VANCOUVER · TORONTO</div><div class="n" style="color:#4A5F78">대도시</div><div class="i" style="color:#4A5F78">한국·아시아계<br />학생이 많은 학교<br />한국어 쓸 일이 많음</div></div>
          <div class="cmp" id="s02-c2" style="left:1420px;background:#16324F;color:#FAF6EF"><div class="k" style="color:#7FD3DE">VERNON</div><div class="n">버논</div><div class="i">교실도, 복도도,<br />식당도<br /><span style="color:#F3C969">모두 영어</span></div></div>
          <div class="abs" id="s02-seats" style="left:124px;top:700px;width:760px;height:160px">
            <div class="abs l" style="left:0;top:0;font-size:24px;color:#146A77">학교별 한국 학생 정원 상한</div>
            <div class="abs" style="left:0;top:50px;width:760px;height:60px" id="s02-row"></div>
          </div>
          <div class="chip sand" id="s02-few" style="left:1000px;top:760px">한국 학생은 학교마다 손에 꼽을 정도</div>""",
    marks={"van": "밴쿠버", "cap": "상한"},
    js="""
(function(){const g=q('#s02-grid');for(let i=0;i<100;i++){const d=document.createElement('div');d.className='dot'+(i>=95?' k':'');d.style.left=(i%10)*33+'px';d.style.top=Math.floor(i/10)*33+'px';g.appendChild(d);}
const r=q('#s02-row');for(let i=0;i<10;i++){const s=document.createElement('div');s.className='seat'+(i<2?' on':'');s.style.left=(i*72)+'px';r.appendChild(s);}})();
inn('#s02-st',R[0]-0.3,{r0:-14,r:-4,s:0.6,y:0});inn('#s02-t',R[0],{y:24});
qa('#s02-grid .dot').forEach((d,i)=>tl.fromTo(d,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.35,ease:'power3.out'},R[0]+0.3+((i%10)+Math.floor(i/10))*0.045));
count('#s02-pct',0,95,R[0]+0.5,2.4,v=>Math.round(v)+'%');inn('#s02-pctl',R[0]+1.4,{y:12});inn('#s02-src',R[0]+1.8,{y:10});
pol('#s02-ph',R[0]+0.8,4);kb('#s02-ph img',R[0]+0.8,R[1]-R[0],{s:1},{s:1.08});
tl.to('#s02-ph',{opacity:0,x:300,rotation:12,duration:0.5,ease:'power2.in'},R[1]-0.4);
inn('#s02-c1',M.van,{y:50});inn('#s02-c2',M.van+1.4,{y:50});
tl.to('#s02-c1',{opacity:0.55,scale:0.96,duration:0.6},M.van+2.6);
inn('#s02-seats',M.cap-0.6,{y:30});
qa('#s02-row .seat').forEach((s,i)=>tl.fromTo(s,{scale:0},{scale:1,duration:0.35,ease:'back.out(2)'},M.cap-0.3+i*0.07));
inn('#s02-few',M.cap+1.4,{s:0.7,y:0});
""",
)

# ---------------------------------------------------------------- 03 double edge (scale)
S["03-double-edge"] = dict(
    bg=f"""        <div class="abs" style="inset:0;opacity:.10"><img src="{P}16-classroom-overhead.jpg" alt="" style="width:100%;height:100%;object-fit:cover;filter:blur(16px)" /></div>""",
    css="""
R .pan{position:absolute;top:470px;width:520px;height:190px;border-radius:26px;padding:26px 30px;color:#fff}
R .pan .k{font-weight:700;font-size:24px;letter-spacing:.08em;opacity:.9}
R .pan .v{font-weight:800;font-size:40px;line-height:1.3;margin-top:8px}
""",
    body="""
          <div class="abs hd" id="s03-t" style="left:120px;top:92px;font-size:66px">장점이자, 숙제</div>
          <div class="abs" id="s03-post" style="left:952px;top:330px;width:16px;height:420px;background:#16324F;border-radius:8px"></div>
          <div class="abs" id="s03-base" style="left:820px;top:740px;width:280px;height:22px;background:#16324F;border-radius:11px"></div>
          <div class="abs" id="s03-beam" style="left:400px;top:318px;width:1120px;height:18px;background:#16324F;border-radius:9px"></div>
          <div class="abs" id="s03-cap" style="left:930px;top:298px;width:60px;height:60px;border-radius:50%;background:#E8572B"></div>
          <div class="pan" id="s03-L" style="left:220px;background:#4E8A1E"><div class="k">MERIT</div><div class="v">영어가 가장 빨리<br />느는 환경</div></div>
          <div class="pan" id="s03-Rp" style="left:1180px;background:#E8572B"><div class="k">CHALLENGE</div><div class="v">준비 없이 가면<br />첫 몇 달은 혼자</div></div>
          <div class="abs" id="s03-w" style="left:760px;top:150px;width:400px;height:120px;border-radius:24px;background:#1F8A99;color:#fff;text-align:center;padding-top:26px"><div class="hd" style="font-size:46px">출발 전 영어 준비</div></div>
          <div class="abs h" id="s03-k" style="left:120px;top:800px;width:1680px;text-align:center;font-size:58px">초기 적응을 <span style="background:linear-gradient(transparent 60%,#F3C969 60%)">좌우합니다</span></div>""",
    marks={"alone": "혼자"},
    js="""
const L=560;function tilt(deg,at,d){const r=deg*Math.PI/180;
  tl.to('#s03-beam',{rotation:deg,transformOrigin:'50% 50%',duration:d,ease:'power2.inOut'},at);
  tl.to('#s03-L',{y:-Math.sin(r)*L,duration:d,ease:'power2.inOut'},at);
  tl.to('#s03-Rp',{y:Math.sin(r)*L,duration:d,ease:'power2.inOut'},at);}
inn('#s03-t',R[0]-0.2,{y:24});
inn(['#s03-post','#s03-base','#s03-beam','#s03-cap'],R[0],{y:30});
inn('#s03-L',R[0]+0.6,{y:-60});
tilt(-7,R[0]+1.0,0.9);
inn('#s03-Rp',R[1],{y:-60});
tilt(9,M.alone-0.6,1.0);
inn('#s03-w',R[2],{y:-120,d:0.7,e:'bounce.out'});
tilt(0,R[2]+0.6,1.0);
inn('#s03-k',R[2]+2.0,{y:24});
""",
)

# ---------------------------------------------------------------- 04 graduation
S["04-graduation"] = dict(
    bg="",
    css="""
R .seg{position:absolute;top:0;height:120px;transform-origin:0 50%}
R .sl{position:absolute;top:150px;font-weight:700;font-size:28px;white-space:nowrap}
""",
    body="""
          <div class="sticker" id="s04-st" style="left:120px;top:96px">추천 포인트 02</div>
          <div class="abs hd" id="s04-t" style="left:120px;top:150px;font-size:66px">졸업까지의 시간</div>
          <div class="abs h" id="s04-n" style="left:1500px;top:130px;font-size:120px;color:#146A77;font-variant-numeric:tabular-nums">0</div>
          <div class="abs hd" id="s04-nl" style="left:1500px;top:270px;font-size:30px">BC주 졸업 학점</div>
          <div class="abs" id="s04-bar" style="left:120px;top:400px;width:1680px;height:120px">
            <div class="abs" id="s04-frame" style="inset:0;border:4px solid #16324F;border-radius:18px"></div>
            <div class="seg" id="s04-a" style="left:0;width:840px;background:#1F8A99;border-radius:16px 0 0 16px"></div>
            <div class="seg" id="s04-b" style="left:840px;width:336px;background:#7FB236"></div>
            <div class="seg" id="s04-c" style="left:1176px;width:336px;background:#4E8A1E"></div>
            <div class="seg" id="s04-d" style="left:1512px;width:168px;background:#3A7016;border-radius:0 16px 16px 0"></div>
            <div class="abs h" id="s04-at" style="left:40px;top:26px;font-size:56px;color:#fff">≈ 40</div>
            <div class="sl" id="s04-al" style="left:0;color:#146A77">한국 고1 성적으로 인정</div>
            <div class="sl" id="s04-bl" style="left:860px">1학기 16</div>
            <div class="sl" id="s04-cl" style="left:1196px">2학기 16</div>
            <div class="sl" id="s04-dl" style="left:1520px">3학기</div>
          </div>
          <div class="abs h" id="s04-k" style="left:120px;top:680px;font-size:88px">계산상 <span style="color:#3A7016">3학기</span>면 졸업 요건 충족</div>""",
    marks={"40": "약 40학점", "16": "16학점씩", "three": "세 학기"},
    js="""
inn('#s04-st',R[0]-0.3,{r0:-14,r:-4,s:0.6,y:0});inn('#s04-t',R[0],{y:24});
inn('#s04-frame',R[0]+0.4,{y:0,s:0.98});inn('#s04-n',R[0]+0.4,{y:20});count('#s04-n',0,80,R[0]+0.6,1.6,v=>Math.round(v));inn('#s04-nl',R[0]+1.0,{y:10});
grow('#s04-a',M['40']-0.2,0.9);inn('#s04-at',M['40']+0.5,{y:10});inn('#s04-al',M['40']+0.6,{y:10});
grow('#s04-b',M['16'],0.6);inn('#s04-bl',M['16']+0.3,{y:10});
grow('#s04-c',M['16']+0.8,0.6);inn('#s04-cl',M['16']+1.1,{y:10});
grow('#s04-d',M.three-0.2,0.6);inn('#s04-dl',M.three+0.1,{y:10});
inn('#s04-k',M.three+0.6,{y:30});
""",
)

# ---------------------------------------------------------------- 05 ESL
def _sem(prefix, x, y, esl):
    cells = "".join(
        f'<div class="slot{" esl" if k < esl else ""}" style="top:{k * 52}px"><span class="sa">정규 과목</span><span class="sb">ESL</span></div>' for k in range(4))
    return f'<div class="sem" id="{prefix}" style="left:{x}px;top:{y}px">{cells}</div>'


_rowA = "\n".join("          " + _sem(f"s05-a{i}", 520 + i * 240, 260, 0) for i in range(3))
_rowB = "\n".join("          " + _sem(f"s05-b{i}", 520 + i * 240, 560, 2 if i < 2 else 0) for i in range(4))
S["05-esl"] = dict(
    bg="",
    css="""
R .sem{position:absolute;width:210px;height:200px}
R .slot{position:absolute;left:0;width:210px;height:44px;border-radius:10px;background:#1F8A99;color:#fff;font-weight:700;font-size:22px;text-align:center;line-height:44px}
R .slot span{position:absolute;left:0;right:0;top:0}
R .slot .sb{opacity:0}
R .rl{position:absolute;left:120px;width:360px}
R .rl .k{font-weight:700;font-size:24px;letter-spacing:.06em;color:#146A77}
R .rl .v{font-weight:800;font-size:38px;line-height:1.3;margin-top:6px}
R .res{position:absolute;font-weight:900;font-size:56px;white-space:nowrap}
""",
    body=f"""
          <div class="abs hd" id="s05-t" style="left:120px;top:92px;font-size:66px">ESL이 정규 과목 자리를 차지하면</div>
          <div class="rl" id="s05-la" style="top:290px"><div class="k">한 학기 4과목</div><div class="v">영어 준비가<br />된 경우</div></div>
          <div class="rl" id="s05-lb" style="top:590px"><div class="k">레벨에 따라</div><div class="v">ESL을<br />들어야 하는 경우</div></div>
{_rowA}
{_rowB}
          <div class="res" id="s05-ra" style="left:1280px;top:320px;color:#3A7016">3학기</div>
          <div class="res" id="s05-rb" style="left:1500px;top:830px;color:#E8572B;font-size:48px">2년 가까이</div>
          <div class="abs" id="s05-yr" style="left:520px;top:780px;width:450px;height:8px;background:#E8572B;border-radius:4px"></div>
          <div class="abs l" id="s05-yrl" style="left:520px;top:800px;font-size:24px;color:#E8572B">최대 1년 · ESL 2과목</div>""",
    marks={"esl": "ESL,", "lvl": "레벨에", "three": "세 학기", "two": "2년"},
    js="""
inn('#s05-t',R[0]-0.2,{y:24});
inn('#s05-la',R[0]+0.6,{x:-30,y:0});
['#s05-a0','#s05-a1','#s05-a2'].forEach((s,i)=>inn(s,R[0]+0.9+i*0.25,{y:30}));
inn('#s05-lb',M.esl-0.4,{x:-30,y:0});
inn('#s05-b0',M.esl-0.2,{y:30});
const e0=qa('#s05-b0 .slot.esl');
function flip(el,at){tl.to(el,{backgroundColor:'#E8572B',duration:0.3},at);tl.to(el.querySelector('.sa'),{opacity:0,duration:0.2},at);tl.to(el.querySelector('.sb'),{opacity:1,duration:0.2},at+0.1);}
flip(e0[0],M.esl+0.3);
['#s05-b1','#s05-b2','#s05-b3'].forEach((s,i)=>inn(s,M.lvl+i*0.3,{y:30}));
qa('#s05-b0 .slot.esl,#s05-b1 .slot.esl').forEach((el,i)=>{if(el!==e0[0])flip(el,M.lvl+1.4+i*0.25);});
grow('#s05-yr',M.lvl+2.4,0.8);inn('#s05-yrl',M.lvl+2.8,{y:10});
inn('#s05-ra',M.three,{x:-30,y:0});
inn('#s05-rb',M.two,{x:-30,y:0});
""",
)

# ---------------------------------------------------------------- 06 reveal
S["06-reveal"] = dict(
    bg="",
    css="""
R .vp{position:absolute;width:52px;height:52px;border-radius:50% 50% 50% 0}
R .ct{position:absolute;font-weight:800;font-size:40px;white-space:nowrap}
""",
    body=f"""
          <div class="full" id="s06-hero"><img src="{P}50-vanwest-students.jpg" alt="" style="object-position:30% 30%" /></div>
          <div class="abs" id="s06-heros" style="inset:0;background:linear-gradient(90deg,rgba(22,50,79,.0) 30%,rgba(22,50,79,.88) 75%)"></div>
          <div class="abs l" id="s06-h0" style="left:1140px;top:330px;font-size:28px;color:#F3C969">그 차이를 줄이는 방법</div>
          <div class="abs h" id="s06-h1" style="left:1140px;top:380px;font-size:84px;color:#FAF6EF;line-height:1.15">버논에 가기 전,<br />영어를 미리</div>
          <div class="abs" id="s06-map" style="left:0;top:0;width:1920px;height:1080px">
            <svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">
              <path id="s06-lake" d="M520 240 C 560 330, 470 420, 520 520 C 560 600, 600 680, 560 820" fill="none" stroke="#1F8A99" stroke-width="54" stroke-linecap="round" opacity=".55"/>
              <path id="s06-road" d="M640 760 C 720 620, 700 420, 640 300" fill="none" stroke="#16324F" stroke-width="8" stroke-dasharray="4 16" stroke-linecap="round"/>
            </svg>
            <div class="abs b" id="s06-lk" style="left:300px;top:540px;font-size:28px;color:#146A77">오카나간 호수</div>
            <div class="vp" id="s06-pv" style="left:614px;top:236px;background:#16324F"></div>
            <div class="ct" id="s06-tv" style="left:690px;top:240px">버논</div>
            <div class="vp" id="s06-pk" style="left:614px;top:720px;background:#E8572B"></div>
            <div class="ct" id="s06-tk" style="left:690px;top:724px">켈로나</div>
            <div class="chip" id="s06-dr" style="left:720px;top:480px">차로 약 40분</div>
          </div>
          <div class="pol" id="s06-ext" style="left:960px;top:170px;width:640px;height:540px"><div class="ph"><img src="{P}60-campus-exterior.jpg" alt="" /></div><div class="cap">VanWest College · Kelowna</div></div>
          <div class="pol" id="s06-lob" style="left:1420px;top:580px;width:380px;height:320px"><div class="ph"><img src="{P}61-campus-lobby.jpg" alt="" /></div><div class="cap">campus lobby</div></div>
          <div class="chip solid" id="s06-cn" style="left:960px;top:90px">밴웨스트 컬리지 켈로나 캠퍼스</div>
          <div class="abs" id="s06-prog" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs" id="s06-pp" style="left:120px;top:210px;width:1680px;height:420px;border-radius:32px;background:#16324F"></div>
            <div class="abs l" id="s06-p0" style="left:200px;top:270px;font-size:28px;color:#7FD3DE">VANWEST COLLEGE · KELOWNA</div>
            <div class="abs h" id="s06-p1" style="left:200px;top:320px;font-size:110px;color:#FAF6EF">공립학교 준비 과정</div>
            <div class="abs" id="s06-f0" style="left:200px;top:500px;width:520px;height:84px;border-radius:20px;background:#1F8A99;color:#fff;font-weight:800;font-size:36px;text-align:center;line-height:84px">켈로나에서 영어 준비</div>
            <svg class="abs" id="s06-ar" style="left:740px;top:512px;width:180px;height:60px" viewBox="0 0 180 60"><path d="M6 30 H160 M136 8 L166 30 L136 52" fill="none" stroke="#F3C969" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <div class="abs" id="s06-f1" style="left:940px;top:500px;width:420px;height:84px;border-radius:20px;background:#FAF6EF;color:#16324F;font-weight:800;font-size:36px;text-align:center;line-height:84px">버논 공립학교 입학</div>
            <div class="chip sand" id="s06-esl" style="left:200px;top:700px">현지 학교에서 ESL을 따로 듣지 않는 경우가 많습니다</div>
          </div>""",
    marks={"kel": "켈로나에", "camp": "캠퍼스가"},
    js="""
kb('#s06-hero img',0,R[1],{s:1.0},{s:1.08,x:-1});
inn('#s06-h0',R[0]+0.2,{y:16});inn('#s06-h1',R[0]+0.5,{y:30});
tl.to(['#s06-hero','#s06-heros','#s06-h0','#s06-h1'],{opacity:0,duration:0.6},R[1]-0.4);
tl.fromTo('#s06-map',{opacity:0},{opacity:1,duration:0.4},R[1]-0.2);
draw('#s06-lake',R[1]-0.2,1.0);inn('#s06-lk',R[1]+0.6,{y:10});
inn('#s06-pv',R[1]+0.1,{y:-80});inn('#s06-tv',R[1]+0.3,{x:-20,y:0});
draw('#s06-road',R[1]+0.8,1.0);inn('#s06-dr',R[1]+1.4,{s:0.7,y:0});
inn('#s06-pk',M.kel-0.3,{y:-80});inn('#s06-tk',M.kel-0.1,{x:-20,y:0});
tl.fromTo('#s06-pk',{scale:1},{scale:1.25,duration:0.4,yoyo:true,repeat:3,ease:'sine.inOut'},M.kel+0.4);
pol('#s06-ext',M.camp-1.2,-3);kb('#s06-ext img',M.camp-1.2,R[2]-M.camp+1.2,{s:1},{s:1.1});
inn('#s06-cn',M.camp-0.6,{y:-20});
pol('#s06-lob',M.camp+1.0,4);
tl.to(['#s06-map','#s06-ext','#s06-lob','#s06-cn'],{opacity:0,duration:0.5},R[2]-0.4);
tl.fromTo('#s06-prog',{opacity:0},{opacity:1,duration:0.1},R[2]-0.2);
tl.fromTo('#s06-pp',{scaleY:0,transformOrigin:'50% 50%'},{scaleY:1,duration:0.6,ease:'power3.out'},R[2]-0.2);
inn('#s06-p0',R[2]+0.3,{y:16});inn('#s06-p1',R[2]+0.5,{y:30});
inn('#s06-f0',R[2]+2.2,{x:-30,y:0});draw('#s06-ar path',R[2]+2.8,0.5);inn('#s06-f1',R[2]+3.2,{x:-30,y:0});
inn('#s06-esl',R[3]+0.6,{s:0.7,y:0});
""",
)

# ---------------------------------------------------------------- 07 terms
WORDS = [("equation", "방정식", 1200, 240, -4), ("perimeter", "둘레", 1480, 380, 3), ("denominator", "분모", 1150, 520, 2), ("coefficient", "계수", 1450, 660, -3)]
_words = "\n".join(
    f'          <div class="wc" id="s07-w{i}" style="left:{x}px;top:{y}px"><b>{e}</b><span>{k}</span></div>' for i, (e, k, x, y, r) in enumerate(WORDS))
WEEKS = ["쓰기·공부 요령", "수학", "진로·생활·실용 역량", "캐나다 역사와 문화", "영어 읽기·쓰기", "응용 디자인·예술", "과학", "건강과 체력"]
_weeks = "\n".join(
    f'          <div class="wk" id="s07-k{i}" style="left:{120 + (i % 4) * 425}px;top:{430 + (i // 4) * 200}px"><div class="n">{i + 1}주</div><div class="v">{w}</div></div>'
    for i, w in enumerate(WEEKS))
S["07-terms"] = dict(
    bg="",
    css="""
R .wc{position:absolute;background:#fff;border-radius:20px;padding:18px 30px;box-shadow:0 12px 28px rgba(22,50,79,.16);white-space:nowrap}
R .wc b{font-weight:800;font-size:44px;color:#16324F;margin-right:18px}
R .wc span{font-weight:700;font-size:32px;color:#146A77}
R .subj{position:absolute;top:470px;width:300px;height:200px;border-radius:28px;background:#16324F;color:#FAF6EF;text-align:center}
R .subj .v{font-weight:900;font-size:76px;margin-top:46px}
R .wk{position:absolute;width:395px;height:170px;border-radius:24px;background:#fff;border:3px solid rgba(22,50,79,.14);padding:24px 28px}
R .wk .n{font-weight:800;font-size:26px;color:#146A77;letter-spacing:.04em}
R .wk .v{font-weight:800;font-size:38px;margin-top:10px;line-height:1.2}
R .wk.on{background:#1F8A99;border-color:#1F8A99}
""",
    body=f"""
          <div class="sticker" id="s07-st" style="left:120px;top:96px">추천 포인트 03</div>
          <div class="abs hd" id="s07-t" style="left:120px;top:150px;font-size:66px">과목 용어</div>
          <div class="abs h" id="s07-a" style="left:120px;top:330px;font-size:76px;color:#4A5F78">수학을 못 하는 게 아니라</div>
          <div class="abs" id="s07-strike" style="left:110px;top:372px;width:930px;height:10px;background:#E8572B;border-radius:5px"></div>
          <div class="abs h" id="s07-b" style="left:120px;top:460px;font-size:96px"><span style="background:linear-gradient(transparent 62%,#F3C969 62%)">용어</span>를 모르는 것</div>
{_words}
          <div class="abs hd" id="s07-hl" style="left:120px;top:330px;font-size:44px">캐나다에서 학교를 다닌 학생들이 꼽은 어려운 과목</div>
          <div class="subj" id="s07-s0" style="left:120px"><div class="v">역사</div></div>
          <div class="subj" id="s07-s1" style="left:460px"><div class="v">지리</div></div>
          <div class="subj" id="s07-s2" style="left:800px"><div class="v">문학</div></div>
          <div class="pol" id="s07-ph" style="left:1240px;top:300px;width:520px;height:440px"><div class="ph"><img src="{P}63-campus-classroom.jpg" alt="" /></div><div class="cap">VanWest classroom</div></div>
          <div class="abs hd" id="s07-wt" style="left:120px;top:330px;font-size:48px">8주 과정 · 매주 다른 과목의 핵심 용어</div>
{_weeks}""",
    marks={"term": "수학 용어를", "hist": "역사", "geo": "지리", "lit": "문학", "w0": "쓰기와 공부", "w1": "수학, 캐나다",
           "w3": "캐나다 역사와", "w4": "영어 읽기", "w6": "과학", "w7": "건강과"},
    js="""
inn('#s07-st',R[0]-0.3,{r0:-14,r:-4,s:0.6,y:0});inn('#s07-t',R[0],{y:24});
inn('#s07-a',R[0]+0.3,{y:24});
tl.fromTo('#s07-strike',{scaleX:0,transformOrigin:'0% 50%'},{scaleX:1,duration:0.5,ease:'power2.inOut'},M.term-0.6);
inn('#s07-b',M.term-0.2,{y:30});
qa('.wc').forEach((w,i)=>tl.fromTo(w,{opacity:0,scale:0.5,rotation:0},{opacity:1,scale:1,rotation:[-4,3,2,-3][i],duration:0.4,ease:'back.out(2)'},M.term+0.2+i*0.22));
tl.to(['#s07-a','#s07-strike','#s07-b'].concat(qa('.wc')),{opacity:0,y:-30,duration:0.35,ease:'power2.in'},R[1]-0.2);
inn('#s07-hl',R[1],{y:20});
inn('#s07-s0',M.hist,{y:40,s:0.8});inn('#s07-s1',M.geo,{y:40,s:0.8});inn('#s07-s2',M.lit,{y:40,s:0.8});
pol('#s07-ph',R[1]+0.4,3);kb('#s07-ph img',R[1]+0.4,R[2]-R[1],{s:1},{s:1.1});
tl.to(['#s07-hl','#s07-s0','#s07-s1','#s07-s2','#s07-ph'],{opacity:0,y:-30,duration:0.4,ease:'power2.in'},R[2]-0.4);
inn('#s07-wt',R[2],{y:20});
qa('.wk').forEach((w,i)=>inn(w,R[2]+0.4+i*0.12,{y:30,d:0.5}));
const WT=[M.w0,M.w1,(M.w1+M.w3)/2,M.w3,M.w4,(M.w4+M.w6)/2,M.w6,M.w7];
WT.forEach((t,i)=>{tl.to('#s07-k'+i,{backgroundColor:'#1F8A99',borderColor:'#1F8A99',color:'#fff',duration:0.3},t);
  tl.to('#s07-k'+i+' .n',{color:'#FAF6EF',duration:0.3},t);});
""",
)
