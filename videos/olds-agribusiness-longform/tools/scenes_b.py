"""Scenes S05 admission, S06 statement of interest, S07 paid DFS, S08 cost table."""
from common import arrow, check

S = {}

# ---------------------------------------------------------------- S05 admission checklist
req = [("① 디플로마 또는 학위", "첫째,"), ("② GPA 2.5 이상", "둘째,"), ("③ 전공 무관", "셋째,"),
       ("④ 영어: IELTS Academic 각 6.0+ 또는 Duolingo 110+", "넷째,")]
S["s05"] = dict(
    css="""
R #s05-bgp img{filter:blur(10px) saturate(.5)}
R #s05-cd{left:240px;top:120px;width:1440px;height:670px}
R .row{left:70px;font-size:46px}
R #s05-plus{left:40px;top:540px;width:1360px;height:96px;border-radius:20px;background:#e8b931;color:#0f3d2e;display:flex;align-items:center;padding:0 34px;font-weight:900;font-size:38px;white-space:nowrap}
""",
    bg='        <div class="full" id="s05-bgp" style="opacity:.22"><img src="@P/campus-04-students-walking.jpg" alt="" /></div>',
    body=f"""
          <div class="card" id="s05-cd">
            <div class="l" id="s05-h" style="position:absolute;left:70px;top:40px;font-size:30px;color:#00875a">ADMISSION · 입학 조건</div>
{''.join(f'            <div class="row" id="s05-r{i}" style="top:{110 + i * 105}px">{check(f"s05-k{i}")}<span>{t}</span></div>' + chr(10) for i, (t, _) in enumerate(req))}
            <div class="chip green" id="s05-j0" style="left:720px;top:118px;font-size:30px">한국 전문대</div>
            <div class="chip green" id="s05-j1" style="left:960px;top:118px;font-size:30px">4년제 대학</div>
            <div class="abs" id="s05-plus">+ 비농업 전공: 관심서(Statement of Interest) + 이력서</div></div>""",
    js="""
kb('#s05-bgp img',0,D,{s:1.05},{s:1.15});
inn('#s05-cd',T('입학 조건은'),{y:40,s:0.97});inn('#s05-h',T('입학 조건은')+0.2,{y:10});
""" + "".join(f"inn('#s05-r{i}',T('{cue}'),{{x:-30,y:0}});draw('#s05-k{i}',T('{cue}')+0.3,0.45);" for i, (_, cue) in enumerate(req)) + """
pop('#s05-j0',T('한국 전문대'));pop('#s05-j1',T('4년제'));
tl.fromTo('#s05-r2',{scale:1},{scale:1.04,duration:0.25,yoyo:true,repeat:1,transformOrigin:'0% 50%'},T('상관없습니다'));
mask('#s05-plus',T('다만 농업과'),0.7,'l');
""",
    sfx=[("pop", "T('첫째,')"), ("pop", "T('둘째,')"), ("pop", "T('셋째,')"), ("pop", "T('넷째,')"), ("whoosh", "T('다만 농업과')")],
)

# ---------------------------------------------------------------- S06 statement of interest
items = [("① 옮겨 쓸 수 있는 농업 관련 기술·지식", "농업에 옮겨"), ("② 농업·농촌 봉사·경험", "농업이나 농촌"),
         ("③ 커리어 목표와의 연결", "이 과정이 내 목표"), ("④ 8개월 DFS 계획", "8개월 실습 계획")]
links = [("식품 회사", "유통·품질 관리", "식품 회사"), ("은행·보험", "농업 금융", "은행이나 보험"),
         ("영업·마케팅", "농자재·농산물 판매", "영업 경력은"), ("주말농장·농촌 봉사", "경험 소재", "주말농장이나")]
S["s06"] = dict(
    css="""
R #s06-q{left:0;right:0;top:250px;text-align:center;font-size:84px;color:rgba(255,255,255,.75)}
R #s06-strike{left:640px;top:300px;width:640px;height:12px;background:#c8102e;border-radius:6px}
R #s06-k{left:0;right:0;top:420px;text-align:center;font-size:130px;white-space:nowrap}
R #s06-doc{left:160px;top:140px;width:560px;height:650px;padding:60px 50px}
R .ln{height:22px;border-radius:11px;background:rgba(15,61,46,.16);margin-bottom:26px}
R .hl{position:absolute;left:40px;width:480px;height:84px;border-radius:14px;background:rgba(232,185,49,.55)}
R .it{position:absolute;left:820px;font-weight:800;font-size:42px;white-space:nowrap;padding:18px 28px;border-radius:18px;background:rgba(6,30,22,.6);border-left:8px solid #e8b931}
R #s06-g3 .full img{filter:saturate(.6)}
R .lb{position:absolute;width:520px;height:96px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px}
R .lb.a{left:200px;background:#f5efe3;color:#0f3d2e}
R .lb.b{left:1150px;background:rgba(6,30,22,.8);border:3px solid #e8b931;color:#e8b931}
""",
    bg="",
    body=f"""
          <div class="grp" id="s06-g1">
            <div class="abs hd" id="s06-q">농사 경력 필수?</div>
            <div class="abs" id="s06-strike"></div>
            <div class="abs h" id="s06-k"><span class="gold" id="s06-k1">관심서가</span> <span id="s06-k2">합격을 가른다</span></div></div>
          <div class="grp" id="s06-g2">
            <div class="card" id="s06-doc">
              <div class="t" style="font-size:40px;margin-bottom:34px">Statement of Interest</div>
              {''.join('<div class="ln" style="width:' + str(w) + '%"></div>' for w in (100, 92, 96, 70, 100, 88, 94, 60, 100, 84, 90, 66))}
{''.join(f'              <div class="hl" id="s06-h{i}" style="top:{150 + i * 144}px"></div>' + chr(10) for i in range(4))}
              <div class="tag" id="s06-ex" style="right:30px;top:30px">예시</div></div>
            <div class="abs hd" id="s06-t2" style="left:820px;top:150px;font-size:48px">학교가 요구하는 <span class="gold">4가지</span></div>
{''.join(f'            <div class="it" id="s06-i{i}" style="top:{250 + i * 112}px">{t}</div>' + chr(10) for i, (t, _) in enumerate(items))}
            <div class="chip cream" id="s06-cv" style="left:820px;top:700px;font-size:34px">+ 이력서로 뒷받침</div></div>
          <div class="grp" id="s06-g3">
            <div class="full" id="s06-p3" style="opacity:.25"><img src="@P/prog-10-pasture-to-plate.jpg" alt="" /></div>
            <div class="abs hd" id="s06-t3" style="left:200px;top:140px;font-size:52px">농사 경험이 없어도 <span class="gold">소재는 있다</span></div>
{''.join(f'            <div class="lb a" id="s06-a{i}" style="top:{250 + i * 120}px">{a}</div>{arrow(f"s06-ar{i}", 760, 268 + i * 120, 350, 60)}<div class="lb b" id="s06-b{i}" style="top:{250 + i * 120}px">{b}</div>' + chr(10) for i, (a, b, _) in enumerate(links))}
            <div class="pill" id="s06-cta" style="left:200px;top:740px;font-size:32px">관심서 소재 정리 · AA Canada 무료 상담</div></div>""",
    js="""
inn('#s06-q',T('농사 경력이'),{y:20});grow('#s06-strike',T('꼭 있어야')+0.3,0.4);
kin('#s06-k1',T('관심서가 합격을'),0.05);kin('#s06-k2',T('관심서가 합격을')+0.3,0.04);
outt('#s06-g1',T('학교가 관심서에')-0.4,{d:0.4});
tl.set('#s06-g2',{opacity:0},0);tl.set('#s06-g2',{opacity:1},T('학교가 관심서에')-0.05);
inn('#s06-doc',T('학교가 관심서에'),{y:40,r0:-4});inn('#s06-t2',T('학교가 관심서에')+0.2,{x:30,y:0});stamp('#s06-ex',T('네 가지예요')-0.2,-8);
""" + "".join(f"grow('#s06-h{i}',T('{cue}'),0.5);inn('#s06-i{i}',T('{cue}'),{{x:40,y:0}});" for i, (_, cue) in enumerate(items)) + """
pop('#s06-cv',T('8개월 실습 계획')+1.2);
outt('#s06-g2',T('농사 경험이 없어도 소재는')-0.4,{d:0.4});
tl.set('#s06-g3',{opacity:0},0);tl.set('#s06-g3',{opacity:1},T('농사 경험이 없어도 소재는')-0.05);
kb('#s06-p3 img',T('농사 경험이 없어도 소재는'),D-T('농사 경험이 없어도 소재는'));inn('#s06-t3',T('농사 경험이 없어도 소재는'),{y:14});
""" + "".join(f"inn('#s06-a{i}',T('{cue}'),{{x:-30,y:0}});draw('#s06-ar{i}',T('{cue}')+0.4,0.5);inn('#s06-b{i}',T('{cue}')+0.8,{{x:30,y:0}});" for i, (_, _, cue) in enumerate(links)) + """
pop('#s06-cta',T('어떤 이야기를'));
""",
    sfx=[("whoosh", "T('관심서가 합격을')"), ("stamp", "T('네 가지예요')-0.2"), ("pop", "T('농업에 옮겨')"), ("pop", "T('8개월 실습 계획')"),
         ("whoosh", "T('농사 경험이 없어도 소재는')"), ("pop", "T('어떤 이야기를')")],
)

# ---------------------------------------------------------------- S07 paid DFS
cards7 = [("01", "자리는 학생이<br/>직접 구함", "학교 배정 아님", "학생이 직접"), ("02", "필요 서류", "Study Permit<br/>+ Co-op Permit + SIN", "국제학생은"),
          ("03", "유급 또는 무급", "학교 WIL 정책", "유급일 수도")]
flow7 = [("3학년<br/>업계 프로젝트", 200), ("인맥", 820), ("DFS 자리", 1340)]
COIN = '<svg width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="#e8b931"/><circle cx="60" cy="60" r="40" fill="none" stroke="#0f3d2e" stroke-width="5"/><text x="60" y="80" text-anchor="middle" font-size="56" font-weight="900" fill="#0f3d2e" font-family="Pretendard">$</text></svg>'
PIN = '<svg width="96" height="128" viewBox="0 0 60 80"><path d="M30 78 C30 78 4 46 4 30 A26 26 0 1 1 56 30 C56 46 30 78 30 78 Z" fill="#00b373"/><circle cx="30" cy="30" r="10" fill="#f5efe3"/></svg>'
S["s07"] = dict(
    css="""
R #s07-g1 .full img,R #s07-g4 .full img{filter:saturate(.7)}
R #s07-t{left:0;right:0;top:380px;text-align:center;font-size:130px;white-space:nowrap}
R .c7{position:absolute;top:200px;width:500px;height:420px;padding:44px 40px}
R .c7 .n{font-weight:900;font-size:40px;color:#14563f}
R .c7 .t{font-size:50px;margin-top:16px;line-height:1.2}
R .c7 .s{font-weight:700;font-size:32px;margin-top:20px;color:#14563f;line-height:1.35}
R #s07-st{left:1330px;top:560px;padding:18px 38px;border:8px solid #e8b931;border-radius:18px;color:#e8b931;background:rgba(6,30,22,.85);font-weight:900;font-size:60px;white-space:nowrap}
R .half{position:absolute;top:170px;width:790px;height:560px;border-radius:30px;background:rgba(6,30,22,.55);border:3px solid rgba(245,239,227,.3);padding:50px}
R .half .n{font-weight:900;font-size:64px;color:#e8b931}
R .half .t{font-weight:800;font-size:46px;line-height:1.35;margin-top:24px}
R .fb{position:absolute;top:360px;height:150px;border-radius:26px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:46px;line-height:1.2}
""",
    bg="",
    body=f"""
          <div class="grp" id="s07-g1">
            <div class="full" id="s07-p1" style="opacity:.3"><img src="@P/prog-06-wsat-ag-students.jpg" alt="" /></div>
            <div class="abs h" id="s07-t">8개월 실습의 <span class="gold">진실</span></div></div>
          <div class="grp" id="s07-g2">
{''.join(f'            <div class="card c7" id="s07-c{i}" style="left:{150 + i * 560}px"><div class="n">{n}</div><div class="t">{t}</div><div class="s">{s}</div><div style="position:absolute;right:36px;top:36px">{check(f"s07-k{i}", 60)}</div></div>' + chr(10) for i, (n, t, s, _) in enumerate(cards7))}
            <div class="abs" id="s07-st">유급이 핵심</div></div>
          <div class="grp" id="s07-g3">
            <div class="abs hd" id="s07-h3" style="left:140px;top:80px;font-size:48px">유급이어야 하는 <span class="gold">이유 2가지</span></div>
            <div class="half" id="s07-l" style="left:140px"><div class="n">①</div><div class="t">실습 기간 등록금<br/>→ <span class="gold">급여로 충당</span></div><div style="position:absolute;right:50px;bottom:50px">{COIN}</div></div>
            <div class="half" id="s07-r" style="left:990px"><div class="n">②</div><div class="t">알버타 · 주 30시간+ · 유급<br/>→ <span class="gold">영주권 경력 가능</span></div><div style="position:absolute;right:60px;bottom:40px">{PIN}</div></div></div>
          <div class="grp" id="s07-g4">
            <div class="full" id="s07-p4" style="opacity:.28"><img src="@P/prog-01-student-with-crops.jpg" alt="" /></div>
            <div class="fb" id="s07-f0" style="left:200px;width:480px;background:#f5efe3;color:#0f3d2e">3학년<br/>업계 프로젝트</div>
            {arrow('s07-a0', 690, 405, 120, 60)}
            <div class="fb" id="s07-f1" style="left:820px;width:360px;background:#00b373;color:#0f3d2e">인맥</div>
            {arrow('s07-a1', 1190, 405, 140, 60)}
            <div class="fb" id="s07-f2" style="left:1340px;width:400px;background:#e8b931;color:#0f3d2e">DFS 자리</div></div>""",
    js="""
kb('#s07-p1 img',0,T('실습 자리는'));kin('#s07-t',T('이제 핵심')+0.1,0.04);
outt('#s07-g1',T('실습 자리는')-0.4,{d:0.4});
tl.set('#s07-g2',{opacity:0},0);tl.set('#s07-g2',{opacity:1},T('실습 자리는')-0.05);
""" + "".join(f"flip('#s07-c{i}',T('{cue}'));draw('#s07-k{i}',T('{cue}')+0.6,0.45);" for i, (_, _, _, cue) in enumerate(cards7)) + """
stamp('#s07-st',T('그래서 유급 자리를'),-6);
outt('#s07-g2',T('이유는 두 가지')-0.4,{d:0.4});
tl.set('#s07-g3',{opacity:0},0);tl.set('#s07-g3',{opacity:1},T('이유는 두 가지')-0.05);
inn('#s07-h3',T('이유는 두 가지'),{y:14});inn('#s07-l',T('하나, 실습'),{x:-50,y:0});inn('#s07-r',T('둘, 알버타'),{x:50,y:0});
outt('#s07-g3',T('그래서 3학년')-0.4,{d:0.4});
tl.set('#s07-g4',{opacity:0},0);tl.set('#s07-g4',{opacity:1},T('그래서 3학년')-0.05);
kb('#s07-p4 img',T('그래서 3학년'),D-T('그래서 3학년'));
pop('#s07-f0',T('그래서 3학년'));draw('#s07-a0',T('업계 인맥')-0.3,0.4);pop('#s07-f1',T('업계 인맥'));draw('#s07-a1',T('업계 인맥')+0.5,0.4);pop('#s07-f2',T('업계 인맥')+0.9);
""",
    sfx=[("whoosh", "T('이제 핵심')"), ("pop", "T('학생이 직접')"), ("pop", "T('국제학생은')"), ("pop", "T('유급일 수도')"),
         ("stamp", "T('그래서 유급 자리를')"), ("whoosh", "T('이유는 두 가지')"), ("pop", "T('업계 인맥')")],
)

# ---------------------------------------------------------------- S08 cost table
rows8 = [("1학기 Fall", "2026.09.08 ~ 12.18", "$11,714.70", "가을 학기"), ("2학기 Winter", "2027.01.11 ~ 04.30", "$7,268.20", "겨울 학기"),
         ("DFS 8개월", "실습 기간", "$16,242.50", "8개월 실습 기간")]
S["s08"] = dict(
    css="""
R #s08-cd{left:150px;top:120px;width:1240px;height:570px}
R .tr{position:absolute;left:40px;width:1160px;height:76px;display:flex;align-items:center;font-weight:800;font-size:36px;color:#0f3d2e}
R .tr .a{width:330px;padding-left:22px}
R .tr .b{width:430px;font-weight:600;font-size:32px;color:#14563f}
R .tr .c{width:400px;text-align:right;padding-right:26px;font-weight:900;font-variant-numeric:tabular-nums}
R .tr.hd{font-size:26px;letter-spacing:.08em;color:#00875a;height:56px}
R .tr.tot{background:#0f3d2e;color:#fff;border-radius:16px;font-size:42px}
R .tr.tot .c{color:#e8b931;font-size:52px}
R .hr{position:absolute;left:40px;width:1160px;height:2px;background:rgba(15,61,46,.15)}
R #s08-red{left:34px;top:256px;width:1172px;height:84px;border-radius:16px;border:6px solid #c8102e}
R #s08-note{left:1440px;top:350px;width:380px;padding:24px 28px;border-radius:20px;background:#e8b931;color:#0f3d2e;font-weight:900;font-size:38px;line-height:1.3}
""",
    bg="",
    body=f"""
          <div class="card" id="s08-cd">
            <div class="tr hd" style="top:24px"><span class="a">구분</span><span class="b">기간</span><span class="c">금액 (CAD)</span></div>
{''.join(f'            <div class="tr" id="s08-r{i}" style="top:{100 + i * 84}px"><span class="a">{a}</span><span class="b">{b}</span><span class="c" id="s08-v{i}">{c}</span></div><div class="hr" style="top:{180 + i * 84}px"></div>' + chr(10) for i, (a, b, c, _) in enumerate(rows8))}
            <div class="abs" id="s08-red"></div>
            <div class="tr tot" id="s08-tot" style="top:370px"><span class="a">합계</span><span class="b" style="color:rgba(255,255,255,.7)">수업료 + 필수 비용</span><span class="c">약 $<span id="s08-tv">35,225</span></span></div>
            <div class="tr" id="s08-bk" style="top:466px"><span class="a">교재 (별도)</span><span class="b"></span><span class="c">약 $1,210</span></div></div>
          <div class="chip cream" id="s08-k0" style="left:150px;top:722px;font-size:32px">지원비 $90</div>
          <div class="chip" id="s08-k1" style="left:400px;top:722px;font-size:32px">합격 후 디파짓 $5,000 (수업료에 포함)</div>
          <div class="chip gray" id="s08-k2" style="left:1060px;top:722px;font-size:32px">생활비·집값 별도</div>
          {arrow('s08-ar', 1395, 285, 70, 50, 'M64 25 L8 25 M30 4 L6 25 L30 46')}
          <div class="abs" id="s08-note">유급 실습 급여로 충당</div>""",
    js="""
inn('#s08-cd',T('비용은'),{y:40,s:0.97});
""" + "".join(f"inn('#s08-r{i}',T('{cue}'),{{x:-20,y:0}});odo('#s08-v{i}',T('{cue}'),1.2);" for i, (_, _, _, cue) in enumerate(rows8)) + """
slam('#s08-tot',T('합치면'),{s:1.3,d:0.35});odo('#s08-tv',T('합치면')+0.2,1.2);
inn('#s08-bk',T('교재비'),{x:-20,y:0});
pop('#s08-k0',T('지원비는'));pop('#s08-k1',T('디파짓'));
tl.fromTo('#s08-red',{opacity:0,scale:1.08},{opacity:1,scale:1,duration:0.4,ease:'power3.out'},T('가장 큰 등록금'));
draw('#s08-ar',T('유급 실습 급여로'),0.4);inn('#s08-note',T('유급 실습 급여로')+0.2,{x:30,y:0});
pop('#s08-k2',T('생활비와'));
""",
    sfx=[("pop", "T('가을 학기')"), ("pop", "T('겨울 학기')"), ("pop", "T('8개월 실습 기간')"), ("impact", "T('합치면')+0.35"),
         ("stamp", "T('가장 큰 등록금')"), ("pop", "T('유급 실습 급여로')")],
)
