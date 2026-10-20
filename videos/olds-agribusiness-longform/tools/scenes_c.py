"""Scenes S09 PGWP, S10 AOS (lock beat), S11 RRS, S12 closing face overlay + CTA."""
from common import ab_map, arrow, check

S = {}

# ---------------------------------------------------------------- S09 PGWP
GLASS = ('<svg width="200" height="300" viewBox="0 0 200 300"><path d="M30 10 H170 M30 290 H170" stroke="#f5efe3" stroke-width="14" stroke-linecap="round"/>'
         '<path d="M44 16 C44 110 100 120 100 150 C100 180 44 190 44 284 H156 C156 190 100 180 100 150 C100 120 156 110 156 16 Z" fill="none" stroke="#f5efe3" stroke-width="8"/>'
         '<path id="s09-sand" d="M62 280 C62 230 100 210 100 196 C100 210 138 230 138 280 Z" fill="#e8b931"/></svg>')
S["s09"] = dict(
    css="""
R #s09-cd{left:160px;top:160px;width:820px;height:330px;padding:48px 56px}
R .bar{position:absolute;left:160px;height:110px;border-radius:24px;display:flex;align-items:center;padding:0 40px;font-weight:900;font-size:44px;white-space:nowrap}
R #s09-b0{top:280px;width:1500px;background:rgba(255,255,255,.14);color:rgba(255,255,255,.75)}
R #s09-b1{top:420px;width:900px;background:#e8b931;color:#0f3d2e}
R #s09-big{left:160px;top:580px;font-size:120px;white-space:nowrap}
R #s09-hg{left:240px;top:220px;width:200px;height:300px}
R #s09-msg{left:560px;top:330px;font-size:100px;white-space:nowrap}
""",
    bg="",
    body=f"""
          <div class="grp" id="s09-g1">
            <div class="card" id="s09-cd">
              <div class="l" style="font-size:28px;color:#00b373">POST-GRADUATION WORK PERMIT</div>
              <div class="t" style="font-size:120px;line-height:1.1;margin-top:10px">PGWP</div>
              <div class="t" style="font-size:44px;margin-top:6px">졸업 후 취업 비자</div></div>
            <div class="row" id="s09-c0" style="left:1060px;top:230px;font-size:46px;color:#fff">{check("s09-k0", 64)}<span>학사: 전공 제한 없음</span></div>
            <div class="row" id="s09-c1" style="left:1060px;top:360px;font-size:46px;color:#fff">{check("s09-k1", 64, "#e8b931")}<span>영어 <span class="gold">CLB 7</span> 필요</span></div></div>
          <div class="grp" id="s09-g2">
            <div class="abs hd" id="s09-h2" style="left:160px;top:150px;font-size:56px">꼭 알아야 할 점</div>
            <div class="bar" id="s09-b0">2년 이상 과정 → 최대 3년</div>
            <div class="bar" id="s09-b1">2년 미만 과정 → 과정 길이만큼</div>
            <div class="abs h" id="s09-big">이 과정 → <span class="gold">약 16개월</span></div></div>
          <div class="grp" id="s09-g3">
            <div class="abs" id="s09-hg">{GLASS}</div>
            <div class="abs h" id="s09-msg">실습 기간에 <span class="gold">잡오퍼</span> 확보</div></div>""",
    js="""
inn('#s09-cd',T('졸업하면'),{y:40,s:0.96});
inn('#s09-c0',T('전공 제한은'),{x:40,y:0});draw('#s09-k0',T('전공 제한은')+0.3,0.45);
inn('#s09-c1',T('CLB 7'),{x:40,y:0});draw('#s09-k1',T('CLB 7')+0.3,0.45);
outt('#s09-g1',T('꼭 알아야')-0.4,{d:0.4});
tl.set('#s09-g2',{opacity:0},0);tl.set('#s09-g2',{opacity:1},T('꼭 알아야')-0.05);
inn('#s09-h2',T('꼭 알아야'),{y:14});grow('#s09-b0',T('과정이 2년이'),0.7);grow('#s09-b1',T('과정 길이만큼만'),0.6);
slam('#s09-big',T('약 16개월'),{s:2.2});
outt('#s09-g2',T('시간이 넉넉하지')-0.4,{d:0.4});
tl.set('#s09-g3',{opacity:0},0);tl.set('#s09-g3',{opacity:1},T('시간이 넉넉하지')-0.05);
inn('#s09-hg',T('시간이 넉넉하지'),{y:30});tl.fromTo('#s09-hg',{rotation:0},{rotation:180,duration:0.7,ease:'power3.inOut'},T('시간이 넉넉하지')+0.6);
kin('#s09-msg',T('실습 기간에 잡오퍼'),0.04);
""",
    sfx=[("pop", "T('전공 제한은')"), ("pop", "T('CLB 7')"), ("whoosh", "T('과정이 2년이')"), ("impact", "T('약 16개월')+0.42"), ("whoosh", "T('실습 기간에 잡오퍼')")],
)

# ---------------------------------------------------------------- S10 AOS (key beat: 4 locks)
cond = [("알버타 공립 칼리지 학사 + PGWP", "알버타 공립 칼리지"), ("최근 18개월 중 알버타 풀타임 경력 6개월", "최근 18개월"),
        ("직종 = 알버타에서 공부한 전공과 관련", "직종은 전공과"), ("알버타 고용주 풀타임 잡오퍼", "알버타 고용주의"),
        ("영어 CLB 5 (TEER 0~3) · CLB 4 (TEER 4~5)", "영어는 직종에 따라")]
locks = [("유급", "코업도 유급"), ("주 30시간+<br/>풀타임", "주 30시간 이상"), ("현재 직종<br/>관련", "지금 직종과 관련"), ("알버타 안", "알버타 안이라는")]


def lock(i):
    return (f'<div class="lk" id="s10-l{i}" style="left:{230 + i * 390}px">'
            f'<svg class="abs" id="s10-sh{i}" style="left:45px;top:0;width:110px;height:100px" viewBox="0 0 110 100"><path d="M15 100 V50 A40 40 0 0 1 95 50 V100" fill="none" stroke="#f5efe3" stroke-width="16"/></svg>'
            f'<div class="lb" id="s10-lb{i}"></div><div class="lt">{locks[i][0]}</div></div>')


SEG = "".join(f'<i style="left:{k * 60}px"></i>' for k in range(8))
S["s10"] = dict(
    css="""
R #s10-t{left:0;right:0;top:330px;text-align:center;font-size:76px;white-space:nowrap}
R #s10-ts{left:0;right:0;top:450px;text-align:center;font-size:44px;color:#e8b931}
R #s10-cd{left:160px;top:120px;width:1600px;height:660px}
R #s10-cd .row{left:70px;font-size:44px}
R .lk{position:absolute;top:200px;width:200px;height:300px}
R .lb{position:absolute;left:10px;top:84px;width:180px;height:140px;border-radius:24px;background:#c8102e}
R .lt{position:absolute;left:-60px;top:236px;width:320px;text-align:center;font-weight:900;font-size:36px;line-height:1.2}
R #s10-h3{left:0;right:0;top:120px;text-align:center;font-size:54px;white-space:nowrap}
R #s10-blk{left:220px;top:600px;width:480px;height:110px}
R #s10-blk i,R #s10-slot i{position:absolute;top:0;width:56px;height:110px;border-radius:12px;background:#e8b931}
R #s10-blk span{position:absolute;left:0;top:-50px;font-weight:900;font-size:34px;color:#e8b931;white-space:nowrap}
R #s10-slot{left:1120px;top:588px;width:384px;height:134px;border-radius:20px;border:5px dashed #f5efe3}
R #s10-slot b{position:absolute;left:0;top:-52px;font-weight:900;font-size:34px;white-space:nowrap}
R #s10-ov{left:1512px;top:740px;font-weight:800;font-size:28px;color:rgba(255,255,255,.75);white-space:nowrap}
R #s10-eoi{left:0;right:0;top:340px;display:flex;flex-direction:column;align-items:center}
""",
    bg="",
    body=f"""
          <div class="grp" id="s10-g1">
            <div class="abs h" id="s10-t">AAIP · Alberta Opportunity Stream <span class="gold">(AOS)</span></div>
            <div class="abs hd" id="s10-ts">알버타 주정부 이민 · 첫 번째 길</div></div>
          <div class="grp" id="s10-g2">
            <div class="card" id="s10-cd">
              <div class="l" style="position:absolute;left:70px;top:40px;font-size:28px;color:#00b373">AOS 주요 조건 · 알버타 공립 칼리지 학사 출신</div>
{''.join(f'              <div class="row" id="s10-r{i}" style="top:{110 + i * 104}px">{check(f"s10-k{i}")}<span>{t}</span></div>' + chr(10) for i, (t, _) in enumerate(cond))}            </div></div>
          <div class="grp" id="s10-g3">
            <div class="abs hd" id="s10-h3">4가지 조건을 채우면 <span class="gold">코업도 경력이 될 수 있다</span></div>
{''.join('            ' + lock(i) + chr(10) for i in range(4))}
            <div class="abs" id="s10-pts" style="inset:0"></div>
            <div class="abs" id="s10-slot"><b>AOS 경력 6개월</b></div>
            <div class="abs" id="s10-blk"><span>8개월 DFS (유급)</span>{SEG}</div>
            <div class="abs" id="s10-ov">+2개월 초과</div></div>
          <div class="grp" id="s10-g4">
            <div class="abs" id="s10-eoi"><div class="chip gray" style="position:relative;font-size:52px;padding:22px 50px">EOI 제출 → 선발 방식</div>
              <div class="hd" style="font-size:38px;margin-top:30px;color:rgba(255,255,255,.75)">관심 표명서 · 조건 충족 = 선발 보장 아님</div></div></div>""",
    js="""
mask('#s10-t',T('그럼 영주권은')+0.2,0.8,'l');inn('#s10-ts',T('첫 번째 길은'),{y:14});
outt('#s10-g1',T('알버타 공립 칼리지')-0.4,{d:0.4});
tl.set('#s10-g2',{opacity:0},0);tl.set('#s10-g2',{opacity:1},T('알버타 공립 칼리지')-0.05);
inn('#s10-cd',T('알버타 공립 칼리지')-0.3,{y:40,s:0.97});
""" + "".join(f"inn('#s10-r{i}',T('{cue}'),{{x:-30,y:0}});draw('#s10-k{i}',T('{cue}')+0.3,0.45);" for i, (_, cue) in enumerate(cond)) + """
outt('#s10-g2',T('그리고 오늘의 핵심')-0.4,{d:0.4});
tl.set('#s10-g3',{opacity:0},0);tl.set('#s10-g3',{opacity:1},T('그리고 오늘의 핵심')-0.05);
mask('#s10-h3',T('그리고 오늘의 핵심'),0.8,'l');
pop(qa('.lk'),T('그리고 오늘의 핵심')+0.4,0.1);
""" + "".join(f"tl.to('#s10-sh{i}',{{y:-34,rotation:-18,transformOrigin:'85% 100%',duration:0.35,ease:'back.out(2)'}},T('{cue}'));"
              f"tl.to('#s10-lb{i}',{{backgroundColor:'#00b373',duration:0.3}},T('{cue}'));" for i, (_, cue) in enumerate(locks)) + """
const UL=T('알버타 안이라는')+0.6;
inn('#s10-slot',UL,{y:20});inn('#s10-blk',UL+0.2,{x:-40,y:0});
const FLY=T('8개월 유급 실습이');
tl.to('#s10-blk span',{opacity:0,duration:0.2},FLY);tl.to('#s10-blk',{x:1128-220,duration:0.8,ease:'power3.inOut'},FLY);
tl.to(qa('#s10-blk i').slice(6),{backgroundColor:'rgba(232,185,49,.35)',duration:0.3},FLY+0.8);
inn('#s10-ov',FLY+1.0,{y:10});burst('#s10-pts',FLY+0.8,26,1310,655,420,9);
outt('#s10-g3',T('다만 AOS는')-0.4,{d:0.4});
tl.set('#s10-g4',{opacity:0},0);tl.set('#s10-g4',{opacity:1},T('다만 AOS는')-0.05);
inn('#s10-eoi',T('다만 AOS는'),{y:20,s:0.95});
""",
    sfx=[("whoosh", "T('그럼 영주권은')"), ("pop", "T('알버타 공립 칼리지')"), ("pop", "T('영어는 직종에 따라')"),
         ("pop", "T('코업도 유급')"), ("pop", "T('주 30시간 이상')"), ("pop", "T('지금 직종과 관련')"), ("pop", "T('알버타 안이라는')"),
         ("whoosh", "T('8개월 유급 실습이')"), ("impact", "T('8개월 유급 실습이')+0.8")],
)

# ---------------------------------------------------------------- S11 RRS
CAL = ('<svg width="150" height="150" viewBox="0 0 150 150"><rect x="8" y="22" width="134" height="120" rx="18" fill="#f5efe3"/>'
       '<rect x="8" y="22" width="134" height="36" rx="18" fill="#c8102e"/><rect x="8" y="40" width="134" height="18" fill="#c8102e"/>'
       '<path d="M42 8 V36 M108 8 V36" stroke="#0f3d2e" stroke-width="10" stroke-linecap="round"/>'
       '<text x="75" y="118" text-anchor="middle" font-size="48" font-weight="900" fill="#0f3d2e" font-family="Pretendard">매년</text></svg>')
S["s11"] = dict(
    css="""
R #s11-t{left:760px;top:150px;font-size:60px;white-space:nowrap}
R #s11-ring{left:0;top:0;width:110px;height:110px;border-radius:50%;border:6px solid #e8b931;background:rgba(232,185,49,.18)}
R .c11{position:absolute;left:760px;width:1000px;padding:30px 40px}
R .c11 .t{font-size:42px}
R .c11 .s{font-weight:700;font-size:32px;margin-top:10px;color:#14563f}
R #s11-warn{left:800px;top:620px;padding:16px 34px;border-radius:16px;background:#e8b931;color:#0f3d2e;font-weight:900;font-size:40px;white-space:nowrap}
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
            <div class="card c11" id="s11-ex" style="top:340px;height:250px"><div class="l" style="font-size:26px;color:#00b373">경력 면제 조항</div>
              <div class="t" style="margin-top:14px;line-height:1.3">지정 커뮤니티 안 DLI 2년 과정 + PGWP<br/>→ 12개월 경력 면제</div></div>
            <div class="abs" id="s11-warn">이 과정 적용 여부: 확인 필요 · 가능성</div></div>
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
outt('#s11-g2',T('지정 커뮤니티 안 학교에서')-0.4,{d:0.4});
tl.set('#s11-g3',{opacity:0},0);tl.set('#s11-g3',{opacity:1},T('지정 커뮤니티 안 학교에서')-0.05);
inn('#s11-ex',T('지정 커뮤니티 안 학교에서'),{x:40,y:0});stamp('#s11-warn',T('다만 이 16개월'),-3);
outt('#s11-g3',T('2026년부터 커뮤니티별')-0.4,{d:0.4});
tl.set('#s11-g4',{opacity:0},0);tl.set('#s11-g4',{opacity:1},T('2026년부터 커뮤니티별')-0.05);
inn('#s11-q0',T('2026년부터 커뮤니티별'),{x:40,y:0});inn('#s11-q1',T('올즈는 2026년'),{x:40,y:0});
tl.fromTo('#s11-cal',{opacity:0,scale:0.3,rotation:-12},{opacity:1,scale:1,rotation:0,duration:0.5,ease:'back.out(2)'},T('매년 쿼터가'));
""",
    sfx=[("whoosh", "T('두 번째 길은')"), ("pop", "T('이니스페일')"), ("pop", "T('커뮤니티 추천서와')"), ("stamp", "T('다만 이 16개월')"),
         ("whoosh", "T('2026년부터 커뮤니티별')"), ("pop", "T('매년 쿼터가')")],
)

# ---------------------------------------------------------------- S12 closing (face video underneath) + CTA
who = [("전문대·대학 졸업", "전문대나 대학을"), ("20대 후반~30대 직장인", "20대 후반"), ("커리어 전환", "커리어를 바꾸고")]
S["s12"] = dict(
    css="""
R .bg,R .blob{display:none}
R .wc{position:absolute;left:1300px;display:flex;align-items:center;gap:18px;padding:14px 30px 14px 18px;border-radius:99px;background:rgba(6,30,22,.85);font-weight:800;font-size:38px;white-space:nowrap}
R #s12-bub{left:1240px;top:300px;padding:30px 40px;border-radius:30px;background:#f5efe3;color:#0f3d2e;font-weight:900;font-size:44px;white-space:nowrap}
R #s12-tail{left:1300px;top:400px;width:0;height:0;border-left:26px solid transparent;border-right:26px solid transparent;border-top:40px solid #f5efe3}
R #s12-band{left:0;top:600px;width:1920px;height:480px;background:linear-gradient(0deg,rgba(8,42,31,.96) 0%,rgba(8,42,31,.9) 55%,rgba(8,42,31,0) 100%)}
R #s12-aa{left:120px;top:660px;font-size:96px;letter-spacing:.02em;white-space:nowrap}
R #s12-l1{left:126px;top:774px;font-size:36px;color:#e8b931;white-space:nowrap}
R #s12-btn{left:1150px;top:668px;width:660px;height:100px;border-radius:56px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;box-shadow:0 16px 40px rgba(200,16,46,.45)}
R #s12-tel{left:1150px;top:782px;width:660px;text-align:center;font-size:32px;color:rgba(255,255,255,.88)}
""",
    body="".join(f'\n          <div class="wc" id="s12-w{i}" style="top:{220 + i * 110}px">{check(f"s12-k{i}", 52)}<span>{t}</span></div>' for i, (t, _) in enumerate(who)) + """
          <div class="abs" id="s12-bub">관심서에 뭘 쓸지 <span style="color:#00b373">댓글로!</span></div>
          <div class="abs" id="s12-tail"></div>
          <div class="abs" id="s12-cta" style="inset:0">
            <div class="abs" id="s12-band"></div>
            <div class="abs" id="s12-pts" style="inset:0"></div>
            <div class="abs h" id="s12-aa">AA CANADA</div>
            <div class="abs hd" id="s12-l1">캐나다 유학 · 유학 후 이민</div>
            <div class="abs" id="s12-btn">무료 상담 · 카톡 canlog</div>
            <div class="abs b" id="s12-tel">02-567-4345</div></div>""",
    js="".join(f"inn('#s12-w{i}',T('{cue}'),{{x:40,y:0}});draw('#s12-k{i}',T('{cue}')+0.3,0.4);" for i, (_, cue) in enumerate(who)) + """
outt(qa('.wc'),T('농업 경험이 없는데')-0.3,{x:40});
inn(['#s12-bub','#s12-tail'].map(s=>q(s)),T('댓글로'),{y:20,s:0.85});
const CT=Math.max(T('댓글로')+2.0,D-5);
outt(['#s12-bub','#s12-tail'].map(s=>q(s)),CT-0.3,{y:-20});
tl.fromTo('#s12-band',{opacity:0},{opacity:1,duration:0.5},CT);
mask('#s12-aa',CT+0.1,0.7,'l');inn('#s12-l1',CT+0.5,{y:12});
slam('#s12-btn',CT+0.7,{s:1.5,shake:false});inn('#s12-tel',CT+1.0,{y:10});
const PU=CT+1.2;tl.fromTo('#s12-btn',{scale:1},{scale:1.06,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:Math.max(1,Math.floor((D-PU)/0.6)-1)},PU);
burst('#s12-pts',CT+0.8,40,1480,718,520,11);
""",
    sfx=[("pop", "T('전문대나 대학을')"), ("pop", "T('20대 후반')"), ("pop", "T('커리어를 바꾸고')"), ("pop", "T('댓글로')"),
         ("whoosh", "max(T('댓글로')+2.0,D-5)"), ("impact", "max(T('댓글로')+2.0,D-5)+1.1")],
)
