"""Scene AOS (id s10, lock beat). PGWP / RRS / closing / opening / jobs-wage are in scenes_d.py."""
from common import ab_map, arrow, check

S = {}

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
              <div class="l" style="position:absolute;left:70px;top:40px;font-size:28px;color:#00875a">AOS 주요 조건 · 알버타 공립 칼리지 학사 출신</div>
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

