"""Scenes rebuilt for the final recording (no face video):
S01 opening, s08b jobs + wage (S09), s09 PGWP 3 years (S10), s11 RRS exemption (S12), s12 closing + CTA (S13)."""
from common import ab_map, arrow, check

S = {}

# ---------------------------------------------------------------- S01 opening (voice + photos)
route = [("2년 학사", "2년 만에"), ("8개월 유급 실습", "8개월은"), ("알버타 영주권", "알버타 영주권")]
S["s01"] = dict(
    css="""
R #s01-g1 .full img,R #s01-g2 .full img{filter:saturate(.9)}
R #s01-q{left:0;right:0;top:330px;text-align:center;font-size:120px;white-space:nowrap}
R #s01-x{left:0;right:0;top:520px;display:flex;justify-content:center}
R .rn{position:absolute;top:400px;width:440px;height:170px;margin-left:-220px;border-radius:30px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:50px}
R #s01-ban{left:160px;top:150px;width:1600px;height:400px}
R #s01-title{left:0;right:0;top:600px;text-align:center;font-size:96px;white-space:nowrap}
R #s01-sub{left:0;right:0;top:730px;text-align:center;font-size:40px;color:#e8b931;white-space:nowrap}
""",
    bg="",
    body=f"""
          <div class="grp" id="s01-g1">
            <div class="full" id="s01-p1"><img src="@P/sf-02-banner.jpg" alt="" /></div><div class="dim" style="opacity:.55"></div>
            <div class="abs h" id="s01-q">전문대 · 대학 <span class="gold">졸업하셨나요?</span></div>
            <div class="abs" id="s01-x"><div class="chip red" id="s01-no" style="position:relative;font-size:56px;padding:18px 44px">농사 경험 X · 괜찮습니다</div></div></div>
          <div class="grp" id="s01-g2">
            <div class="full" id="s01-p2"><img src="@P/sf-11-canola.jpg" alt="" /></div><div class="dim" style="opacity:.62"></div>
            <svg class="abs" style="left:260px;top:440px;width:1400px;height:90px" viewBox="0 0 1400 90"><path id="s01-line" d="M0 45 L1400 45" stroke="#e8b931" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 22"/></svg>
{''.join(f'            <div class="rn" id="s01-r{i}" style="left:{360 + i * 600}px;background:{["#f5efe3", "#e8b931", "#00b373"][i]};color:#0f3d2e">{t}</div>' + chr(10) for i, (t, _) in enumerate(route))}
            <div class="abs hd" id="s01-rh" style="left:0;right:0;top:250px;text-align:center;font-size:52px">캐나다에서 이어지는 <span class="gold">한 줄의 길</span></div></div>
          <div class="grp" id="s01-g3">
            <div class="abs" id="s01-pts" style="inset:0"></div>
            <div class="ph frame" id="s01-ban"><img src="@P/campus-02-aerial-full.jpg" alt="" /></div>
            <div class="abs h" id="s01-title">올즈 컬리지 <span class="gold">농업경영 학사</span></div>
            <div class="abs hd" id="s01-sub">Olds College · Bachelor of Applied Science - Agribusiness</div></div>""",
    js="""
kb('#s01-p1 img',0,T('2년 만에'),{s:1.0},{s:1.1,x:-2});
kin('#s01-q',T('전문대나 대학'),0.03);
stamp('#s01-no',T('농사 경험이'),-4);
outt('#s01-g1',T('2년 만에')-0.35,{d:0.35});
tl.set('#s01-g2',{opacity:0},0);tl.set('#s01-g2',{opacity:1},T('2년 만에')-0.05);
kb('#s01-p2 img',T('2년 만에'),T('오늘은 알버타')-T('2년 만에'),{s:1.05},{s:1.15,x:2});
inn('#s01-rh',T('2년 만에'),{y:14});draw('#s01-line',T('2년 만에'),T('알버타 영주권')-T('2년 만에')+0.4,'none');
""" + "".join(f"tl.fromTo('#s01-r{i}',{{opacity:0,scale:0.3,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.5,ease:'back.out(2)'}},T('{cue}'));" for i, (_, cue) in enumerate(route)) + """
tl.to('#s01-r2',{scale:1.08,duration:0.3,yoyo:true,repeat:1},T('알버타 영주권')+0.6);
outt('#s01-g2',T('오늘은 알버타')-0.35,{d:0.35});
tl.set('#s01-g3',{opacity:0},0);tl.set('#s01-g3',{opacity:1},T('오늘은 알버타')-0.05);
tl.fromTo('#s01-ban',{opacity:0,scale:0.9,rotationX:30,transformPerspective:1400},{opacity:1,scale:1,rotationX:0,duration:0.8,ease:'power3.out'},T('오늘은 알버타'));
kb('#s01-ban img',T('오늘은 알버타'),D-T('오늘은 알버타'));
mask('#s01-title',T('농업경영 학사를'),0.7,'l');inn('#s01-sub',T('농업경영 학사를')+0.4,{y:12});
burst('#s01-pts',T('농업경영 학사를')+0.5,40,960,650,700,5);
""",
    sfx=[("stamp", "T('농사 경험이')"), ("whoosh", "T('2년 만에')"), ("pop", "T('2년 만에')"), ("pop", "T('8개월은')"), ("pop", "T('알버타 영주권')"),
         ("whoosh", "T('오늘은 알버타')"), ("impact", "T('농업경영 학사를')+0.3")],
)

# ---------------------------------------------------------------- s08b (S09) jobs + wage
jobs = [("농업 컨설턴트·전문가", "Agricultural reps, consultants &amp; specialists", "$42.03", "$87,400", "농업 컨설턴트"),
        ("정부 기관", "Government Agency", "$45.63", "$94,900", "정부 기관은"),
        ("농업 금융", "Financial Services", "$33.48", "$69,600", "농업 금융 분야도")]
X0, PX = 330, 10.0  # bar chart: $1,000 = 10 px
S["s08b"] = dict(
    css="""
R #s08b-g1 .full img{filter:saturate(.85)}
R #s08b-q{left:0;right:0;top:170px;text-align:center;font-size:64px;white-space:nowrap}
R #s08b-pc{left:0;right:0;top:270px;text-align:center;font-size:330px;color:#e8b931;line-height:1}
R #s08b-pl{left:0;right:0;top:620px;text-align:center;font-size:44px;white-space:nowrap}
R .jc{position:absolute;top:250px;width:520px;height:440px;padding:40px 40px}
R .jc .k{font-weight:900;font-size:44px;color:#0f3d2e;line-height:1.15}
R .jc .e{font-weight:600;font-size:22px;color:#14563f;margin-top:8px;min-height:56px}
R .jc .w{font-weight:900;font-size:76px;color:#00875a;margin-top:26px;font-variant-numeric:tabular-nums}
R .jc .w small{font-size:30px;color:#14563f}
R .jc .y{font-weight:900;font-size:46px;color:#0f3d2e;margin-top:14px;font-variant-numeric:tabular-nums}
R .jc .y small{font-size:26px;font-weight:700;color:#14563f}
R .bl{position:absolute;left:150px;width:170px;text-align:right;font-weight:800;font-size:32px;line-height:1.2}
R .br{position:absolute;height:110px;border-radius:0 20px 20px 0}
R .bv{position:absolute;font-weight:900;font-size:46px;white-space:nowrap;font-variant-numeric:tabular-nums}
R #s08b-ax{left:330px;top:250px;width:4px;height:420px;background:rgba(245,239,227,.6)}
R #s08b-msg{left:0;right:0;top:700px;text-align:center;font-size:62px;white-space:nowrap}
""",
    bg="",
    body=f"""
          <div class="grp" id="s08b-g1">
            <div class="full" id="s08b-p1" style="opacity:.32"><img src="@P/sf-09-cattle.jpg" alt="" /></div>
            <div class="abs hd" id="s08b-q">투자하면 <span class="gold">얼마나 돌아올까?</span></div>
            <div class="abs num" id="s08b-pc">95%</div>
            <div class="abs hd" id="s08b-pl">졸업생 취업률 · <span class="gold">알버타 칼리지 중 2위</span></div>
            <div class="chip gray" id="s08b-src" style="left:820px;top:720px;font-size:26px">Olds College 학교 자료</div></div>
          <div class="grp" id="s08b-g2">
            <div class="abs hd" id="s08b-h2" style="left:150px;top:140px;font-size:52px">대표 직업과 <span class="gold">평균 시급</span> <span style="font-size:30px;color:rgba(255,255,255,.65)">· 학교 자료 (Talent.com 2023)</span></div>
{''.join(f'            <div class="card jc" id="s08b-j{i}" style="left:{150 + i * 560}px"><div class="k">{k}</div><div class="e">{e}</div><div class="w"><span id="s08b-w{i}">{w}</span><small> /시간</small></div><div class="y"><small>연봉 환산 ≈ </small><span id="s08b-y{i}">{y}</span></div></div>' + chr(10) for i, (k, e, w, y, _) in enumerate(jobs))}
            <div class="abs b" id="s08b-n2" style="left:150px;top:715px;font-size:28px;color:rgba(255,255,255,.7)">주 40시간 · 연 2,080시간 기준 환산</div></div>
          <div class="grp" id="s08b-g3">
            <div class="abs hd" id="s08b-h3" style="left:150px;top:140px;font-size:52px">같은 2년, <span class="gold">연봉 비교</span></div>
            <div class="abs" id="s08b-ax"></div>
            <div class="bl" id="s08b-l0" style="top:300px">2년제<br/>디플로마</div>
            <div class="br" id="s08b-b0" style="left:{X0}px;top:290px;width:{55 * PX:.0f}px;background:rgba(245,239,227,.45)"></div>
            <div class="bv" id="s08b-v0" style="left:{X0 + 55 * PX + 24:.0f}px;top:316px">$<span id="s08b-n0">55,000</span> <span style="font-size:28px;color:rgba(255,255,255,.7)">중간값</span></div>
            <div class="bl" id="s08b-l1" style="top:470px">학사<br/>직업군</div>
            <div class="br" id="s08b-b1" style="left:{X0}px;top:460px;width:{70 * PX:.0f}px;background:rgba(232,185,49,.55)"></div>
            <div class="br" id="s08b-b2" style="left:{X0 + 70 * PX:.0f}px;top:460px;width:{25 * PX:.0f}px;background:#e8b931"></div>
            <div class="bv gold" id="s08b-v1" style="left:{X0 + 95 * PX + 24:.0f}px;top:486px">$70,000~$95,000</div>
            <div class="abs h" id="s08b-msg"><span class="gold">연봉 앞자리</span>가 달라진다</div></div>""",
    js="""
kb('#s08b-p1 img',0,T('연봉도 볼게요'));
kin('#s08b-q',T('그럼 이만큼'),0.03);
odo('#s08b-pc',T('취업률은 95%'),1.3);slam('#s08b-pc',T('취업률은 95%'),{s:2.2});
inn('#s08b-pl',T('알버타 칼리지 중 2위'),{y:14});pop('#s08b-src',T('알버타 칼리지 중 2위')+0.4);
outt('#s08b-g1',T('연봉도 볼게요')-0.35,{d:0.35});
tl.set('#s08b-g2',{opacity:0},0);tl.set('#s08b-g2',{opacity:1},T('연봉도 볼게요')-0.05);
inn('#s08b-h2',T('연봉도 볼게요'),{x:-30,y:0});
""" + "".join(f"flip('#s08b-j{i}',T('{cue}')-0.2);odo('#s08b-w{i}',T('{cue}')+0.3,1.0);odo('#s08b-y{i}',T('{cue}')+0.9,1.1);" for i, (*_, cue) in enumerate(jobs)) + """
inn('#s08b-n2',T('농업 금융 분야도')+1.2,{y:10});
outt('#s08b-g2',T('비교해 볼까요')-0.35,{d:0.35});
tl.set('#s08b-g3',{opacity:0},0);tl.set('#s08b-g3',{opacity:1},T('비교해 볼까요')-0.05);
inn('#s08b-h3',T('비교해 볼까요'),{y:14});grow('#s08b-ax',T('비교해 볼까요')+0.2,0.5,'50% 0%','y');
inn('#s08b-l0',T('알버타 주정부 조사'),{x:-20,y:0});grow('#s08b-b0',T('알버타 주정부 조사'),1.0);
inn('#s08b-v0',T('알버타 주정부 조사')+0.8,{x:-20,y:0});odo('#s08b-n0',T('알버타 주정부 조사')+0.8,1.0);
inn('#s08b-l1',T('같은 2년을'),{x:-20,y:0});grow('#s08b-b1',T('같은 2년을'),1.0);grow('#s08b-b2',T('같은 2년을')+1.0,0.6);
inn('#s08b-v1',T('같은 2년을')+1.4,{x:-20,y:0});
slam('#s08b-msg',T('연봉 앞자리'),{s:1.8});
""",
    sfx=[("whoosh", "T('그럼 이만큼')"), ("impact", "T('취업률은 95%')+0.42"), ("whoosh", "T('연봉도 볼게요')"),
         ("pop", "T('농업 컨설턴트')"), ("pop", "T('정부 기관은')"), ("pop", "T('농업 금융 분야도')"),
         ("whoosh", "T('비교해 볼까요')"), ("impact", "T('연봉 앞자리')+0.42")],
)

# ---------------------------------------------------------------- s09 (S10) PGWP up to 3 years
GLASS = ('<svg width="200" height="300" viewBox="0 0 200 300"><path d="M30 10 H170 M30 290 H170" stroke="#f5efe3" stroke-width="14" stroke-linecap="round"/>'
         '<path d="M44 16 C44 110 100 120 100 150 C100 180 44 190 44 284 H156 C156 190 100 180 100 150 C100 120 156 110 156 16 Z" fill="none" stroke="#f5efe3" stroke-width="8"/>'
         '<path d="M62 280 C62 230 100 210 100 196 C100 210 138 230 138 280 Z" fill="#e8b931"/></svg>')
terms = [("3학년", "가을 학기"), ("3학년", "겨울 학기"), ("4학년", "현장 실습 (DFS)"), ("4학년", "현장 실습 (DFS)")]
flow9 = [("실습 중 잡오퍼", 160, "#f5efe3"), ("졸업", 760, "#00b373"), ("바로 영주권 경력", 1200, "#e8b931")]
S["s09"] = dict(
    css="""
R #s09-cd{left:160px;top:160px;width:820px;height:330px;padding:48px 56px}
R .tm{position:absolute;top:300px;width:360px;height:170px;border-radius:24px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900}
R .tm b{font-size:44px}
R .tm span{font-size:30px;font-weight:800;margin-top:8px}
R #s09-br{left:160px;top:500px;width:1560px;height:16px;border-radius:8px;background:#f5efe3}
R #s09-big{left:0;right:0;top:580px;text-align:center;font-size:130px;white-space:nowrap}
R #s09-hg{left:200px;top:200px;width:200px;height:300px}
R #s09-p3{left:500px;top:250px;font-size:60px;white-space:nowrap}
R .f9{position:absolute;top:470px;height:130px;padding:0 40px;border-radius:26px;display:flex;align-items:center;font-weight:900;font-size:46px;color:#0f3d2e;white-space:nowrap}
""",
    bg="",
    body=f"""
          <div class="grp" id="s09-g1">
            <div class="card" id="s09-cd">
              <div class="l" style="font-size:28px;color:#00875a">POST-GRADUATION WORK PERMIT</div>
              <div class="t" style="font-size:120px;line-height:1.1;margin-top:10px">PGWP</div>
              <div class="t" style="font-size:44px;margin-top:6px">졸업 후 취업 비자</div></div>
            <div class="row" id="s09-c0" style="left:1060px;top:230px;font-size:46px;color:#fff">{check("s09-k0", 64)}<span>학사: 전공 제한 없음</span></div>
            <div class="row" id="s09-c1" style="left:1060px;top:360px;font-size:46px;color:#fff">{check("s09-k1", 64, "#e8b931")}<span>영어 <span class="gold">CLB 7</span> 필요</span></div></div>
          <div class="grp" id="s09-g2">
            <div class="abs hd" id="s09-h2" style="left:160px;top:150px;font-size:56px">그리고 <span class="gold">반가운 점</span></div>
{''.join(f'            <div class="tm" id="s09-t{i}" style="left:{160 + i * 400}px;background:{"#f5efe3" if i < 2 else "#e8b931"};color:#0f3d2e"><b>{a}</b><span>{b}</span></div>' + chr(10) for i, (a, b) in enumerate(terms))}
            <div class="abs" id="s09-br"></div>
            <div class="abs hd" id="s09-2y" style="left:0;right:0;top:530px;text-align:center;font-size:40px">네 학기 = <span class="gold">2년 과정</span></div>
            <div class="abs h" id="s09-big">PGWP <span class="gold">최대 3년</span></div></div>
          <div class="grp" id="s09-g3">
            <div class="abs" id="s09-hg">{GLASS}</div>
            <div class="abs h" id="s09-p3">3년 = <span class="gold">영주권 준비에 충분한 시간</span></div>
{''.join(f'            <div class="f9" id="s09-f{i}" style="left:{x}px;background:{c}">{t}</div>' + chr(10) for i, (t, x, c) in enumerate(flow9))}
            {arrow('s09-a0', 620, 505, 120, 60)}
            {arrow('s09-a1', 1000, 505, 180, 60)}</div>""",
    js="""
inn('#s09-cd',T('졸업하면'),{y:40,s:0.96});
inn('#s09-c0',T('전공 제한은'),{x:40,y:0});draw('#s09-k0',T('전공 제한은')+0.3,0.45);
inn('#s09-c1',T('CLB 7'),{x:40,y:0});draw('#s09-k1',T('CLB 7')+0.3,0.45);
outt('#s09-g1',T('그리고 반가운 점')-0.35,{d:0.35});
tl.set('#s09-g2',{opacity:0},0);tl.set('#s09-g2',{opacity:1},T('그리고 반가운 점')-0.05);
inn('#s09-h2',T('그리고 반가운 점'),{y:14});
pop(qa('.tm'),T('3학년과 4학년 네 학기'),0.18);
grow('#s09-br',T('2년 과정이라'),0.7);inn('#s09-2y',T('2년 과정이라')+0.3,{y:12});
tl.to('#s09-2y',{opacity:0,duration:0.3},T('PGWP가 3년까지')-0.1);
slam('#s09-big',T('PGWP가 3년까지'),{s:2.2});
outt('#s09-g2',T('3년이면 영주권을')-0.35,{d:0.35});
tl.set('#s09-g3',{opacity:0},0);tl.set('#s09-g3',{opacity:1},T('3년이면 영주권을')-0.05);
inn('#s09-hg',T('3년이면 영주권을'),{y:30});tl.fromTo('#s09-hg',{rotation:0},{rotation:180,duration:0.7,ease:'power3.inOut'},T('3년이면 영주권을')+0.6);
kin('#s09-p3',T('3년이면 영주권을')+0.2,0.03);
pop('#s09-f0',T('실습 기간에 잡오퍼'));draw('#s09-a0',T('졸업하자마자')-0.4,0.4);pop('#s09-f1',T('졸업하자마자'));
draw('#s09-a1',T('졸업하자마자')+0.6,0.4);pop('#s09-f2',T('졸업하자마자')+1.0);
""",
    sfx=[("pop", "T('전공 제한은')"), ("pop", "T('CLB 7')"), ("whoosh", "T('그리고 반가운 점')"), ("pop", "T('3학년과 4학년 네 학기')"),
         ("impact", "T('PGWP가 3년까지')+0.42"), ("whoosh", "T('3년이면 영주권을')"), ("pop", "T('졸업하자마자')+1.0")],
)

# ---------------------------------------------------------------- s11 (S12) RRS: 2-year program -> 12-month exemption
CAL = ('<svg width="150" height="150" viewBox="0 0 150 150"><rect x="8" y="22" width="134" height="120" rx="18" fill="#f5efe3"/>'
       '<rect x="8" y="22" width="134" height="36" rx="18" fill="#c8102e"/><rect x="8" y="40" width="134" height="18" fill="#c8102e"/>'
       '<path d="M42 8 V36 M108 8 V36" stroke="#0f3d2e" stroke-width="10" stroke-linecap="round"/>'
       '<text x="75" y="118" text-anchor="middle" font-size="48" font-weight="900" fill="#0f3d2e" font-family="Pretendard">매년</text></svg>')
flow11 = [("올즈 졸업", "올즈에서 졸업하고"), ("올즈 잡오퍼", "올즈에서 잡오퍼를"), ("경력 1년 없이 신청", "경력 1년을")]
S["s11"] = dict(
    css="""
R #s11-t{left:760px;top:150px;font-size:60px;white-space:nowrap}
R #s11-ring{left:0;top:0;width:110px;height:110px;border-radius:50%;border:6px solid #e8b931;background:rgba(232,185,49,.18)}
R .c11{position:absolute;left:760px;width:1000px;padding:30px 40px}
R .c11 .t{font-size:42px}
R .c11 .s{font-weight:700;font-size:32px;margin-top:10px;color:#14563f}
R #s11-plus{left:760px;top:300px;font-size:64px;white-space:nowrap}
R #s11-stamp{left:1180px;top:630px;padding:16px 34px;border:8px solid #e8b931;border-radius:18px;color:#e8b931;background:rgba(6,30,22,.88);font-weight:900;font-size:46px;white-space:nowrap}
R .f11{position:absolute;left:760px;width:620px;height:84px;border-radius:20px;display:flex;align-items:center;padding:0 30px;font-weight:900;font-size:40px;white-space:nowrap}
R #s11-cal{left:1580px;top:560px;width:150px;height:150px}
""",
    bg="",
    body=f"""
          <div class="grp" id="s11-g1">
            {ab_map('s11-map', 150, 130, 420, ("Edmonton", "Red Deer", "Calgary"))}
            <div class="abs" id="s11-ring" style="left:{150 + 255 * 1.05 - 55}px;top:{130 + 440 * 1.05 - 55}px"></div>
            <div class="abs hd" id="s11-rl" style="left:150px;top:780px;font-size:30px;color:#e8b931;white-space:nowrap">Innisfail 지정 커뮤니티 (Olds 포함)</div>
            <div class="abs h" id="s11-t">AAIP · Rural Renewal Stream <span class="gold">(RRS)</span></div>
            <div class="abs hd" id="s11-ts" style="left:764px;top:240px;font-size:38px;color:rgba(255,255,255,.8)">농촌 지역 이민 · 두 번째 길</div></div>
          <div class="grp" id="s11-g2">
            <div class="card c11" id="s11-a" style="top:340px"><div class="t">지정 커뮤니티 추천서 (Endorsement)</div><div class="s" id="s11-as">2026년부터 유효 1년</div></div>
            <div class="card c11" id="s11-b" style="top:510px"><div class="t">커뮤니티 안 고용주 풀타임 잡오퍼</div></div></div>
          <div class="grp" id="s11-g3">
            <div class="abs h" id="s11-plus">여기서 <span class="gold">큰 장점</span></div>
            <div class="card c11" id="s11-ex" style="top:400px;height:200px"><div class="l" style="font-size:26px;color:#00875a">경력 면제 조항</div>
              <div class="t" style="margin-top:14px;line-height:1.3">지정 커뮤니티 안 학교 2년 과정 + PGWP<br/>→ <span style="color:#00875a">12개월 경력 요건 면제</span></div></div>
            <div class="abs" id="s11-stamp">이 과정 = 2년 과정 인정</div></div>
          <div class="grp" id="s11-g3b">
{''.join(f'            <div class="f11" id="s11-f{i}" style="top:{330 + i * 120}px;background:{["#f5efe3", "#00b373", "#e8b931"][i]};color:#0f3d2e">{"①②③"[i]} {t}</div>' + chr(10) for i, (t, _) in enumerate(flow11))}          </div>
          <div class="grp" id="s11-g4">
            <div class="card c11" id="s11-q0" style="top:340px"><div class="t">2026년부터 커뮤니티별 쿼터</div></div>
            <div class="card c11" id="s11-q1" style="top:480px;width:780px"><div class="t">Olds 2026 고용주 접수 <span style="color:#c8102e">마감</span></div></div>
            <div class="abs" id="s11-cal">{CAL}</div></div>""",
    js="""
draw('#s11-map-out',0.1,1.0);tl.fromTo('#s11-map-fill',{opacity:0},{opacity:1,duration:0.6},0.6);
pop(qa('[id^="s11-map-d"],[id^="s11-map-n"]'),0.8,0.06);
mask('#s11-t',T('두 번째 길은')+0.2,0.8,'l');inn('#s11-ts',T('농촌 지역 이민'),{y:12});
tl.fromTo('#s11-map-pin',{opacity:0,y:-200},{opacity:1,y:0,duration:0.5,ease:'bounce.out'},T('올즈 타운은'));inn('#s11-map-pl',T('올즈 타운은')+0.3,{x:-10,y:0});
tl.fromTo('#s11-ring',{opacity:0,scale:0.2},{opacity:1,scale:1,duration:0.6,ease:'back.out(2)'},T('이니스페일'));inn('#s11-rl',T('이니스페일')+0.3,{y:10});
inn('#s11-a',T('커뮤니티 추천서와'),{x:40,y:0});inn('#s11-b',T('그 지역 고용주의'),{x:40,y:0});
tl.fromTo('#s11-as',{color:'#14563f'},{color:'#c8102e',duration:0.3},T('유효기간은'));
outt('#s11-g2',T('여기서 큰 장점')-0.35,{d:0.35});
tl.set('#s11-g3',{opacity:0},0);tl.set('#s11-g3',{opacity:1},T('여기서 큰 장점')-0.05);
slam('#s11-plus',T('여기서 큰 장점'),{s:1.8});
inn('#s11-ex',T('지정 커뮤니티 안 학교에서'),{x:40,y:0});
tl.fromTo('#s11-ex',{scale:1},{scale:1.04,duration:0.25,yoyo:true,repeat:1},T('12개월 경력 요건이'));
stamp('#s11-stamp',T('이 과정이 바로'),-4);
outt('#s11-g3',T('올즈에서 졸업하고')-0.35,{d:0.35});
tl.set('#s11-g3b',{opacity:0},0);tl.set('#s11-g3b',{opacity:1},T('올즈에서 졸업하고')-0.05);
""" + "".join(f"inn('#s11-f{i}',T('{cue}'),{{x:40,y:0}});" for i, (_, cue) in enumerate(flow11)) + """
outt('#s11-g3b',T('다만 2026년부터')-0.35,{d:0.35});
tl.set('#s11-g4',{opacity:0},0);tl.set('#s11-g4',{opacity:1},T('다만 2026년부터')-0.05);
inn('#s11-q0',T('다만 2026년부터'),{x:40,y:0});inn('#s11-q1',T('올즈는 2026년'),{x:40,y:0});
tl.fromTo('#s11-cal',{opacity:0,scale:0.3,rotation:-12},{opacity:1,scale:1,rotation:0,duration:0.5,ease:'back.out(2)'},T('매년 쿼터가'));
""",
    sfx=[("whoosh", "T('두 번째 길은')"), ("pop", "T('이니스페일')"), ("pop", "T('커뮤니티 추천서와')"), ("impact", "T('여기서 큰 장점')+0.42"),
         ("stamp", "T('이 과정이 바로')"), ("pop", "T('경력 1년을')"), ("whoosh", "T('다만 2026년부터')"), ("pop", "T('매년 쿼터가')")],
)

# ---------------------------------------------------------------- s12 (S13) closing + CTA
who = [("전문대·대학 졸업", "전문대나 대학을"), ("20대 후반~30대 직장인", "20대 후반"), ("커리어 전환", "커리어를 바꾸고")]
S["s12"] = dict(
    css="""
R #s12-bgp img{filter:saturate(.8)}
R .wc{position:absolute;left:160px;display:flex;align-items:center;gap:22px;padding:18px 40px 18px 22px;border-radius:99px;background:rgba(6,30,22,.85);font-weight:800;font-size:46px;white-space:nowrap}
R #s12-h{left:160px;top:150px;font-size:58px;white-space:nowrap}
R #s12-bub{left:1060px;top:300px;padding:34px 44px;border-radius:30px;background:#f5efe3;color:#0f3d2e;font-weight:900;font-size:48px;white-space:nowrap}
R #s12-tail{left:1130px;top:410px;width:0;height:0;border-left:28px solid transparent;border-right:28px solid transparent;border-top:44px solid #f5efe3}
R #s12-band{position:absolute;inset:0;background:rgba(8,42,31,.9)}
R #s12-aa{left:0;right:0;top:210px;text-align:center;font-size:150px;letter-spacing:.02em;white-space:nowrap}
R #s12-l1{left:0;right:0;top:400px;text-align:center;font-size:46px;color:#e8b931;white-space:nowrap}
R #s12-btn{left:560px;top:520px;width:800px;height:116px;border-radius:60px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:50px;box-shadow:0 16px 40px rgba(200,16,46,.45)}
R #s12-tel{left:0;right:0;top:660px;text-align:center;font-size:36px;color:rgba(255,255,255,.88)}
""",
    bg='        <div class="full" id="s12-bgp" style="opacity:.4"><img src="@P/campus-05-central-gardens.jpg" alt="" /></div>',
    body="""
          <div class="abs hd" id="s12-h">이런 분께 <span class="gold">추천합니다</span></div>""" + "".join(
        f'\n          <div class="wc" id="s12-w{i}" style="top:{280 + i * 130}px">{check(f"s12-k{i}", 58)}<span>{t}</span></div>' for i, (t, _) in enumerate(who)) + """
          <div class="abs" id="s12-bub">관심서에 뭘 쓸지 <span style="color:#00875a">댓글로!</span></div>
          <div class="abs" id="s12-tail"></div>
          <div class="abs" id="s12-cta" style="inset:0">
            <div class="abs" id="s12-band"></div>
            <div class="abs" id="s12-pts" style="inset:0"></div>
            <div class="abs h" id="s12-aa">AA CANADA</div>
            <div class="abs hd" id="s12-l1">캐나다 유학 · 유학 후 이민</div>
            <div class="abs" id="s12-btn">무료 상담 · 카톡 canlog</div>
            <div class="abs b" id="s12-tel">02-567-4345</div></div>""",
    js="""
kb('#s12-bgp img',0,D,{s:1.0},{s:1.1,x:-2});
inn('#s12-h',T('전문대나 대학을')-0.2,{y:14});
""" + "".join(f"inn('#s12-w{i}',T('{cue}'),{{x:-40,y:0}});draw('#s12-k{i}',T('{cue}')+0.3,0.4);" for i, (_, cue) in enumerate(who)) + """
inn(['#s12-bub','#s12-tail'].map(s=>q(s)),T('댓글로'),{y:20,s:0.85});
const CT=T('내 경력으로');
outt(['#s12-h','#s12-bub','#s12-tail'].concat(qa('.wc').map(e=>'#'+e.id)).map(s=>q(s)),CT-0.3,{y:-20,d:0.3});
tl.fromTo('#s12-band',{opacity:0},{opacity:1,duration:0.5},CT-0.2);
mask('#s12-aa',CT+0.1,0.7,'l');inn('#s12-l1',CT+0.5,{y:12});
slam('#s12-btn',T('무료 상담으로'),{s:1.5,shake:false});inn('#s12-tel',T('무료 상담으로')+0.3,{y:10});
const PU=T('무료 상담으로')+0.6;tl.fromTo('#s12-btn',{scale:1},{scale:1.06,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:Math.max(1,Math.floor((D-PU)/0.6)-1)},PU);
burst('#s12-pts',T('무료 상담으로')+0.2,46,960,578,620,11);
""",
    sfx=[("pop", "T('전문대나 대학을')"), ("pop", "T('20대 후반')"), ("pop", "T('커리어를 바꾸고')"), ("pop", "T('댓글로')"),
         ("whoosh", "T('내 경력으로')-0.2"), ("impact", "T('무료 상담으로')+0.42")],
)
