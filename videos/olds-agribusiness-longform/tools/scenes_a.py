"""Scenes S01 (opening face overlay), S02 why agribusiness, S03 Olds College, S04 structure + timeline."""
from common import ab_map, arrow

S = {}

# ---------------------------------------------------------------- S01 opening (face video underneath)
chips1 = [("농사 경험 X", "red", "농사 경험이"), ("2년 학사", "gold", "2년 만에"), ("8개월 유급 실습", "gold", "8개월은"), ("알버타 영주권", "green", "알버타 영주권")]
S["s01"] = dict(
    css="""
R .bg,R .blob{display:none}
R .fc{position:absolute;left:1400px;font-size:40px;padding:16px 34px}
R #s01-name{left:70px;top:700px;padding:14px 30px;border-radius:16px;background:rgba(6,30,22,.86);border-left:8px solid #00b373;font-weight:800;font-size:34px;white-space:nowrap}
R #s01-dim{position:absolute;inset:0;background:rgba(8,42,31,.72)}
R #s01-title{left:0;right:0;top:380px;text-align:center;font-size:150px}
""",
    body="".join(f'\n          <div class="chip fc {c}" id="s01-c{i}" style="top:{230 + i * 120}px">{t}</div>' for i, (t, c, _) in enumerate(chips1)) + """
          <div class="abs" id="s01-name">AA Canada 원장</div>
          <div class="abs" id="s01-dim"></div>
          <div class="abs" id="s01-pts" style="inset:0"></div>
          <div class="abs h" id="s01-title">농사 <span class="gold">몰라도</span> 됩니다</div>""",
    js="".join(f"pop('#s01-c{i}',T('{cue}'));\n" for i, (_, _, cue) in enumerate(chips1)) + """
inn('#s01-name',0.6,{x:-30,y:0});outt('#s01-name',3.6,{x:-30});
const TT=D-0.6-1.4;
outt(qa('.fc'),TT-0.2,{x:40});
tl.fromTo('#s01-dim',{opacity:0},{opacity:1,duration:0.4},TT);
mask('#s01-title',TT+0.1,0.7,'l');burst('#s01-pts',TT+0.6,36,960,470,700,5);
""",
    sfx=[("pop", "T('농사 경험이')"), ("pop", "T('2년 만에')"), ("pop", "T('8개월은')"), ("pop", "T('알버타 영주권')"), ("impact", "D-1.9")],
)

# ---------------------------------------------------------------- S02 why agribusiness
car1 = [("금융 서비스", "금융 서비스"), ("농업 서비스", "농업 서비스 회사"), ("영업·마케팅", "영업과 마케팅"),
        ("부가가치 생산(가공)", "부가가치 생산"), ("정부 기관", "정부 기관"), ("초급 관리자", "초급 관리자")]
mine = ["영업", "마케팅", "금융", "유통"]
S["s02"] = dict(
    css="""
R #s02-g1 .full img{filter:saturate(.85)}
R #s02-q{left:230px;top:250px;font-size:230px}
R #s02-x{left:830px;top:230px;width:270px;height:270px;border-radius:50%;border:16px solid #c8102e;color:#c8102e;font-size:200px;font-weight:900;display:flex;align-items:center;justify-content:center;line-height:1}
R #s02-eq{left:230px;top:560px;font-size:124px;white-space:nowrap}
R #s02-p2{left:130px;top:190px;width:760px;height:475px}
R .cc{position:absolute;font-size:36px;padding:14px 32px}
R #s02-g3 .full img{filter:blur(8px) saturate(.6)}
R .box{position:absolute;border-radius:28px;border:3px solid rgba(245,239,227,.5);background:rgba(6,30,22,.72)}
R #s02-to{border-color:#e8b931;background:rgba(232,185,49,.14)}
""",
    bg="",
    body=f"""
          <div class="grp" id="s02-g1">
            <div class="full" id="s02-p1"><img src="@P/prog-08-agriculture-card.jpg" alt="" /></div><div class="dim" style="opacity:.5"></div>
            <div class="abs h" id="s02-q">농사?</div>
            <div class="abs" id="s02-x">&#x2715;</div>
            <div class="abs h" id="s02-eq">농업 = <span class="gold">비즈니스</span></div></div>
          <div class="grp" id="s02-g2">
            <div class="ph frame" id="s02-p2"><img src="@P/prog-02-agribusiness-card.jpg" alt="" /></div>
            <div class="abs hd" id="s02-h2" style="left:990px;top:190px;font-size:52px;white-space:nowrap">학교가 소개하는 <span class="gold">진로</span></div>
{''.join(f'            <div class="chip cc{" gold" if i == 0 else ""}" id="s02-c{i}" style="left:{990 + (i % 2) * 420}px;top:{300 + (i // 2) * 120}px">{t}</div>' + chr(10) for i, (t, _) in enumerate(car1))}
            <div class="abs b" id="s02-src" style="left:994px;top:670px;font-size:26px;color:rgba(255,255,255,.6)">Olds College · Career Outcomes</div></div>
          <div class="grp" id="s02-g3">
            <div class="full" id="s02-p3" style="opacity:.35"><img src="@P/prog-09-ag-sales.jpg" alt="" /></div>
            <div class="box" id="s02-from" style="left:170px;top:200px;width:560px;height:520px"></div>
            <div class="abs hd" id="s02-fl" style="left:220px;top:230px;font-size:48px">내 경력</div>
{''.join(f'            <div class="chip cream cc" id="s02-m{i}" style="left:220px;top:{330 + i * 92}px">{t}</div>' + chr(10) for i, t in enumerate(mine))}
            {arrow('s02-arr', 770, 420, 380, 80)}
            <div class="box" id="s02-to" style="left:1190px;top:300px;width:580px;height:300px"></div>
            <div class="abs h" id="s02-tl" style="left:1190px;top:395px;width:580px;text-align:center;font-size:92px;color:#e8b931">농업 산업</div></div>""",
    js="""
kb('#s02-p1 img',0,T('학교가 소개하는'),{s:1.0},{s:1.10,x:-2});
inn('#s02-q',T('트랙터'),{y:40});
stamp('#s02-x',T('농사를 배우는 곳이'),-10);
inn('#s02-eq',T('비즈니스를'),{x:-40,y:0});
outt('#s02-g1',T('학교가 소개하는')-0.4,{d:0.4});
tl.fromTo('#s02-p2',{opacity:0,rotationY:-70,transformPerspective:1400},{opacity:1,rotationY:0,duration:0.7,ease:'power3.out'},T('학교가 소개하는'));
kb('#s02-p2 img',T('학교가 소개하는'),T('영업, 마케팅, 금융')-T('학교가 소개하는'),{s:1.0},{s:1.08});
inn('#s02-h2',T('학교가 소개하는')+0.2,{x:30,y:0});
""" + "".join(f"pop('#s02-c{i}',T('{cue}'));" for i, (_, cue) in enumerate(car1)) + """
inn('#s02-src',T('초급 관리자')+0.5,{y:10});
outt('#s02-g2',T('영업, 마케팅, 금융')-0.4,{d:0.4});
tl.fromTo('#s02-p3',{opacity:0},{opacity:0.35,duration:0.6},T('영업, 마케팅, 금융'));kb('#s02-p3 img',T('영업, 마케팅, 금융'),D-T('영업, 마케팅, 금융'));
inn('#s02-from',T('영업, 마케팅, 금융'),{s:0.94,y:0});inn('#s02-fl',T('영업, 마케팅, 금융')+0.1,{y:12});
pop('#s02-m0',T('영업, 마케팅, 금융'));pop('#s02-m1',T('마케팅, 금융, 유통'));pop('#s02-m2',T('금융, 유통'));pop('#s02-m3',T('유통 일을'));
draw('#s02-arr',T('그 경력을'),0.8);
inn('#s02-to',T('농업 산업으로'),{s:0.9,y:0});mask('#s02-tl',T('농업 산업으로')+0.1,0.6,'l');
tl.set('#s02-g2',{opacity:0},0);tl.set('#s02-g2',{opacity:1},T('학교가 소개하는')-0.05);
tl.set('#s02-g3',{opacity:0},0);tl.set('#s02-g3',{opacity:1},T('영업, 마케팅, 금융')-0.05);
""",
    sfx=[("stamp", "T('농사를 배우는 곳이')"), ("whoosh", "T('학교가 소개하는')"), ("pop", "T('금융 서비스')"), ("pop", "T('초급 관리자')"), ("whoosh", "T('그 경력을')")],
)

# ---------------------------------------------------------------- S03 Olds College
S["s03"] = dict(
    css="""
R #s03-p1{left:700px;top:130px;width:1080px;height:520px}
R #s03-t{left:700px;top:676px;font-size:46px;white-space:nowrap}
R #s03-yr{left:150px;top:190px;font-size:250px;color:#e8b931}
R .bw{position:absolute;width:520px;height:393px}
R .bw img{filter:grayscale(1) contrast(1.05)}
R #s03-h1{left:1060px;top:140px}
R #s03-h2{left:1220px;top:380px}
R #s03-lsc{left:1000px;top:170px;width:820px;height:392px}
R #s03-g3 .full img{filter:saturate(.9)}
R #s03-cnt{left:150px;top:200px;font-size:210px;color:#e8b931}
R .st{position:absolute;width:520px;height:330px}
R #s03-cd{left:420px;top:180px;width:1080px;height:470px;padding:56px 70px}
""",
    bg="",
    body=f"""
          <div class="grp" id="s03-g1">
            {ab_map('s03-map', 150, 130, 400)}
            <div class="ph frame" id="s03-p1"><img src="@P/campus-03-aerial-water-tower.jpg" alt="" /></div>
            <div class="abs h" id="s03-t">OLDS COLLEGE OF AGRICULTURE &amp; TECHNOLOGY</div>
            <div class="abs hd" id="s03-ts" style="left:704px;top:745px;font-size:32px;color:#e8b931;white-space:nowrap">알버타 · 공립 · 농업·농업기술 전문</div></div>
          <div class="grp" id="s03-g2">
            <div class="abs num" id="s03-yr">1913</div>
            <div class="abs hd" id="s03-ys" style="left:160px;top:460px;font-size:44px;white-space:nowrap">Olds School of Agriculture 개교</div>
            <div class="chip gold" id="s03-c100" style="left:160px;top:560px;font-size:40px">100년+</div>
            <div class="chip" id="s03-cpub" style="left:380px;top:560px;font-size:40px">농업·농업기술 전문 공립 칼리지</div>
            <div class="ph frame bw" id="s03-h1"><img src="@P/hist-02-osa.jpg" alt="" /></div>
            <div class="ph frame bw" id="s03-h2"><img src="@P/hist-03-1914-livestock-class.jpg" alt="" /></div>
            <div class="ph frame" id="s03-lsc"><img src="@P/campus-07-lsc.jpg" alt="" /></div></div>
          <div class="grp" id="s03-g3">
            <div class="full" id="s03-p3"><img src="@P/sf-03-drone-flying.jpg" alt="" /></div><div class="dim" id="s03-d3" style="opacity:.35"></div>
            <div class="abs num" id="s03-cnt">3,300+</div>
            <div class="abs hd" id="s03-ac" style="left:160px;top:420px;font-size:56px;white-space:nowrap">acres · <span class="gold">SMART FARM</span></div>
            <div class="chip green" id="s03-k0" style="left:160px;top:540px;font-size:38px">드론</div>
            <div class="chip green" id="s03-k1" style="left:330px;top:540px;font-size:38px">센서</div>
            <div class="chip green" id="s03-k2" style="left:500px;top:540px;font-size:38px">데이터</div>
            <div class="abs hd" id="s03-lab" style="left:160px;top:650px;font-size:40px;white-space:nowrap">살아 있는 실험실</div>
            <div class="ph frame st" id="s03-s0" style="left:1150px;top:120px"><img src="@P/sf-06-precision-ag.jpg" alt="" /></div>
            <div class="ph frame st" id="s03-s1" style="left:1240px;top:290px"><img src="@P/sf-04-sensor.jpg" alt="" /></div>
            <div class="ph frame st" id="s03-s2" style="left:1330px;top:460px"><img src="@P/sf-15-crop-research.jpg" alt="" /></div></div>
          <div class="grp" id="s03-g4">
            <div class="card" id="s03-cd">
              <div class="l" style="font-size:28px;color:#00b373">졸업생 현장 실습 사례</div>
              <div class="t" style="font-size:72px;margin-top:20px">Mikayla Flinn · 2017 졸업</div>
              <div class="t" style="font-size:44px;margin-top:28px">DFS: Farm Credit Canada</div>
              <div class="b" style="font-size:34px;margin-top:8px;color:#14563f">(Red Deer, Calgary)</div>
              <div class="chip green" id="s03-fcc" style="left:70px;top:350px;font-size:32px">농업 전문 금융기관</div></div>
            <div class="chip gold" id="s03-to" style="left:560px;top:690px;font-size:38px">농업경영 학위 → 금융 같은 사무직</div></div>""",
    js="""
draw('#s03-map-out',0.2,1.2);tl.fromTo('#s03-map-fill',{opacity:0},{opacity:1,duration:0.8},0.8);
pop(['#s03-map-d0','#s03-map-d1','#s03-map-n0','#s03-map-n1'].map(s=>q(s)),T('올즈 컬리지 오브')+0.3);
tl.fromTo('#s03-map-pin',{opacity:0,y:-240},{opacity:1,y:0,duration:0.55,ease:'bounce.out'},T('줄여서'));inn('#s03-map-pl',T('줄여서')+0.4,{x:-10,y:0});
tl.fromTo('#s03-p1',{opacity:0,x:60},{opacity:1,x:0,duration:0.6,ease:'power3.out'},T('학교는'));kb('#s03-p1 img',T('학교는'),T('1913년에')-T('학교는'));
mask('#s03-t',T('앤드 테크놀로지'),0.8,'l');inn('#s03-ts',T('줄여서')+0.3,{y:12});
outt('#s03-g1',T('1913년에')-0.4,{d:0.4});
tl.set('#s03-g2',{opacity:0},0);tl.set('#s03-g2',{opacity:1},T('1913년에')-0.05);
odo('#s03-yr',T('1913년에'),1.0);slam('#s03-yr',T('1913년에'),{s:1.6});inn('#s03-ys',T('농업학교로'),{y:14});
tl.set('#s03-h1',{rotation:-4},0);tl.set('#s03-h2',{rotation:3},0);flip('#s03-h1',T('농업학교로'));flip('#s03-h2',T('농업학교로')+0.3);
tl.fromTo('#s03-lsc',{opacity:0},{opacity:1,duration:1.2,ease:'sine.inOut'},T('100년이 넘은'));
pop('#s03-c100',T('100년이 넘은'));pop('#s03-cpub',T('공립 칼리지'));
outt('#s03-g2',T('캠퍼스에는')-0.4,{d:0.4});
tl.set('#s03-g3',{opacity:0},0);tl.set('#s03-g3',{opacity:1},T('캠퍼스에는')-0.05);
kb('#s03-p3 img',T('캠퍼스에는'),T('이 과정 졸업생')-T('캠퍼스에는'),{s:1.0},{s:1.12,x:-3});
odo('#s03-cnt',T('3,300'),1.4);slam('#s03-cnt',T('3,300'),{s:1.5});inn('#s03-ac',T('스마트팜'),{y:14});
tl.to('#s03-d3',{opacity:0.62,duration:0.6},T('드론과'));
pop('#s03-k0',T('드론과'));pop('#s03-k1',T('센서,'));pop('#s03-k2',T('데이터로'));inn('#s03-lab',T('살아 있는'),{y:12});
flip(['#s03-s0','#s03-s1','#s03-s2'].map(s=>q(s)),T('드론과')+0.2,{st:0.25});
outt('#s03-g3',T('이 과정 졸업생')-0.4,{d:0.4});
tl.set('#s03-g4',{opacity:0},0);tl.set('#s03-g4',{opacity:1},T('이 과정 졸업생')-0.05);
inn('#s03-cd',T('이 과정 졸업생'),{y:40,s:0.96});pop('#s03-fcc',T('농업 전문 금융기관'));
inn('#s03-to',T('농업경영 학위가'),{y:20});
""",
    sfx=[("pop", "T('줄여서')"), ("impact", "T('1913년에')+0.42"), ("whoosh", "T('캠퍼스에는')"), ("impact", "T('3,300')+0.42"), ("whoosh", "T('이 과정 졸업생')")],
)

# ---------------------------------------------------------------- S04 structure + timeline
stairs = [("1학년", False, 560), ("2학년", False, 480), ("3학년", True, 400), ("4학년", True, 320)]
subj = [("재무", "재무,"), ("마케팅", "마케팅, 전략"), ("전략경영", "전략경영"), ("인사관리(HR)", "인사관리"),
        ("응용연구", "응용연구"), ("혁신·리더십", "혁신과 리더십"), ("국제 마케팅", "국제 마케팅")]
tln = [("2027.09", "입학 · 3학년<br/>Fall 학기", 230, "2027년 9월"), ("2028.01", "Winter 학기", 560, "2028년 4월"),
       ("2028.04", "캠퍼스<br/>수업 종료", 890, "수업이 끝나고"), ("2028.12", "졸업 → PGWP 신청<br/>→ AOS / RRS", 1650, "12월에 졸업")]
S["s04"] = dict(
    css="""
R .stp{position:absolute;width:360px;border-radius:24px 24px 0 0;display:flex;flex-direction:column;align-items:center;padding-top:30px;font-weight:900;font-size:56px}
R .stp.g0{background:rgba(255,255,255,.14);color:rgba(255,255,255,.6)}
R .stp.g1{background:#e8b931;color:#0f3d2e}
R .stp small{font-size:28px;font-weight:800;margin-top:12px}
R #s04-g2 .full img,R #s04-g3 .full img{filter:saturate(.7)}
R #s04-big{left:150px;top:230px;font-size:300px;color:#e8b931}
R .tn{position:absolute;top:452px;width:36px;height:36px;margin-left:-18px;border-radius:50%;background:#f5efe3;border:7px solid #00b373}
R .td{position:absolute;top:380px;width:340px;margin-left:-170px;text-align:center;font-weight:900;font-size:40px;color:#e8b931}
R .tx{position:absolute;top:520px;width:360px;margin-left:-180px;text-align:center;font-weight:700;font-size:32px;line-height:1.35}
R #s04-dfs{left:1010px;top:446px;width:460px;height:48px;border-radius:24px;background:#e8b931}
""",
    bg="",
    body=f"""
          <div class="grp" id="s04-g1">
            <div class="chip gold" id="s04-k0" style="left:195px;top:140px;font-size:36px">2년 과정 · 최소 16개월</div>
            <div class="chip" id="s04-k1" style="left:640px;top:140px;font-size:36px">가을 입학만</div>
            <div class="chip gray" id="s04-k2" style="left:900px;top:140px;font-size:36px">CIP 01.0102</div>
{''.join(f'            <div class="stp {"g1" if g else "g0"}" id="s04-st{i}" style="left:{195 + i * 390}px;top:{top}px;height:{780 - top}px">{n}<small>{"Olds에서" if g else ""}</small></div>' + chr(10) for i, (n, g, top) in enumerate(stairs))}
            <div class="abs hd" id="s04-rep" style="left:195px;top:{400}px;width:750px;text-align:center;font-size:34px;white-space:nowrap">디플로마·학위로 대체</div></div>
          <div class="grp" id="s04-g2">
            <div class="full" id="s04-p2" style="opacity:.3"><img src="@P/prog-04-wsat-classroom.jpg" alt="" /></div>
            <div class="abs hd" id="s04-h2" style="left:160px;top:150px;font-size:60px">3학년 · <span class="gold">캠퍼스 수업</span></div>
            <div class="flow" id="s04-sub" style="left:160px;top:280px;width:1600px">
{''.join(f'              <div class="chip cream rel" id="s04-c{i}" style="font-size:40px">{t}</div>' + chr(10) for i, (t, _) in enumerate(subj))}            </div>
            <div class="chip gold" id="s04-pj0" style="left:160px;top:560px;font-size:40px">업계 클라이언트 프로젝트</div>
            <div class="chip gold" id="s04-pj1" style="left:690px;top:560px;font-size:40px">팀 프로젝트</div></div>
          <div class="grp" id="s04-g3">
            <div class="full" id="s04-p3" style="opacity:.4"><img src="@P/sf-18-agexpert-farm-mgmt.jpg" alt="" /></div>
            <div class="abs num" id="s04-big">8개월</div>
            <div class="abs hd" id="s04-b1" style="left:170px;top:560px;font-size:60px;white-space:nowrap">Directed Field Study <span class="gold">(DFS)</span></div>
            <div class="abs hd" id="s04-b2" style="left:170px;top:650px;font-size:40px;color:rgba(255,255,255,.8)">4학년 · 현장 실습</div></div>
          <div class="grp" id="s04-g4">
            <div class="abs hd" id="s04-h4" style="left:160px;top:150px;font-size:56px">입학부터 졸업까지 <span class="gold">예시</span></div>
            <svg class="abs" style="left:150px;top:440px;width:1620px;height:60px" viewBox="0 0 1620 60"><path id="s04-line" d="M0 30 L1620 30" stroke="rgba(245,239,227,.55)" stroke-width="8" stroke-linecap="round"/></svg>
            <div class="abs" id="s04-dfs"></div>
            <div class="td" id="s04-dd" style="left:1240px">2028.05~12</div>
            <div class="tx" id="s04-dx" style="left:1240px;color:#e8b931">8개월 DFS<br/>(현장 실습)</div>
{''.join(f'            <div class="tn" id="s04-n{i}" style="left:{x}px"></div><div class="td" id="s04-d{i}" style="left:{x}px">{d}</div><div class="tx" id="s04-x{i}" style="left:{x}px">{t}</div>' + chr(10) for i, (d, t, x, _) in enumerate(tln))}          </div>""",
    js="""
""" + "".join(f"grow('#s04-st{i}',T('과정 구조를')+{0.15 * i:.2f},0.6,'50% 100%','y');" for i in range(4)) + """
inn('#s04-rep',T('디플로마나 학위가'),{y:14});
tl.to(['#s04-st0','#s04-st1'].map(s=>q(s)),{opacity:0.55,duration:0.4},T('디플로마나 학위가'));
tl.fromTo(['#s04-st2','#s04-st3'].map(s=>q(s)),{scale:1},{scale:1.04,duration:0.3,yoyo:true,repeat:1,transformOrigin:'50% 100%'},T('3학년과 4학년만'));
pop('#s04-k0',T('2년 과정'));pop('#s04-k1',T('가을에만'));pop('#s04-k2',T('가을에만')+0.5);
outt('#s04-g1',T('3학년은 캠퍼스에서')-0.4,{d:0.4});
tl.set('#s04-g2',{opacity:0},0);tl.set('#s04-g2',{opacity:1},T('3학년은 캠퍼스에서')-0.05);
kb('#s04-p2 img',T('3학년은 캠퍼스에서'),T('4학년은')-T('3학년은 캠퍼스에서'));inn('#s04-h2',T('3학년은 캠퍼스에서'),{x:-30,y:0});
""" + "".join(f"pop('#s04-c{i}',T('{cue}'));" for i, (_, cue) in enumerate(subj)) + """
pop('#s04-pj0',T('업계 클라이언트'));pop('#s04-pj1',T('팀으로'));
outt('#s04-g2',T('4학년은')-0.4,{d:0.4});
tl.set('#s04-g3',{opacity:0},0);tl.set('#s04-g3',{opacity:1},T('4학년은')-0.05);
kb('#s04-p3 img',T('4학년은'),T('2027년 9월에')-T('4학년은'));
slam('#s04-big',T('8개월 현장'),{s:2.2});mask('#s04-b1',T('디렉티드'),0.7,'l');inn('#s04-b2',T('4학년은')+0.2,{y:12});
outt('#s04-g3',T('2027년 9월에')-0.4,{d:0.4});
tl.set('#s04-g4',{opacity:0},0);tl.set('#s04-g4',{opacity:1},T('2027년 9월에')-0.05);
inn('#s04-h4',T('2027년 9월에')-0.05,{y:14});draw('#s04-line',T('2027년 9월에'),T('12월에 졸업')-T('2027년 9월에'),'none');
""" + "".join(f"pop(['#s04-n{i}','#s04-d{i}','#s04-x{i}'].map(s=>q(s)),T('{cue}'){'+0.9' if i == 1 else ''},0.06);" for i, (_, _, _, cue) in enumerate(tln)) + """
grow('#s04-dfs',T('5월부터 12월'),0.9);pop(['#s04-dd','#s04-dx'].map(s=>q(s)),T('5월부터 12월')+0.3,0.06);
""",
    sfx=[("pop", "T('과정 구조를')"), ("pop", "T('2년 과정')"), ("whoosh", "T('3학년은 캠퍼스에서')"), ("impact", "T('8개월 현장')+0.42"),
         ("whoosh", "T('2027년 9월에')"), ("pop", "T('5월부터 12월')"), ("pop", "T('12월에 졸업')")],
)
