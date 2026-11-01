"""EP2 scenes S01~S09 (voice "일곱번째" over Olds College photos + graphics).
Each major keeps one colour + icon everywhere (script.MAJORS). Facts and numbers only from SCRIPT.txt section 2."""
from common import ab_map, arrow, check
from script import MAJORS
from templates import icon

S = {}
T_, H_, M_ = MAJORS["tech"], MAJORS["horti"], MAJORS["mgmt"]


def tag(cid, m, x, y, size=58):
    """Major name plate: icon + name in the major colour."""
    return (f'<div class="abs mtag" id="{cid}" style="left:{x}px;top:{y}px;font-size:{size}px;color:{m["color"]}">'
            f'<span class="mi">{icon(m["icon"], m["color"], int(size * 1.3))}</span>{m["name"]}</div>')


COMMON_CSS = """
R .mtag{display:flex;align-items:center;gap:22px;font-weight:900;letter-spacing:-.02em;white-space:nowrap}
R .mi{display:flex}
R .plot{position:absolute;border-radius:6px 26px 6px 26px;padding:30px 34px;color:#0e2a22}
R .plot b{display:block;font-weight:900;font-size:44px;line-height:1.15}
R .plot span{display:block;font-weight:700;font-size:28px;margin-top:10px}
R .furrow{position:absolute;inset:0;opacity:.10}
"""


def furrow(color):
    return f'        <div class="furrow" style="background:repeating-linear-gradient(118deg,{color} 0 3px,transparent 3px 46px)"></div>'


# ---------------------------------------------------------------- S01 opening
plots1 = [(T_, "데이터 · 드론"), (H_, "식물 · 온실"), (M_, "경영 · 영업")]
S["s01"] = dict(
    css=COMMON_CSS + """
R #s01-eq{left:0;right:0;top:300px;display:flex;justify-content:center;align-items:center;gap:40px;font-weight:900;font-size:96px;white-space:nowrap}
R #s01-eq .k{color:#e8b931}
R #s01-no{left:0;right:0;top:520px;text-align:center}
R #s01-doc{left:560px;top:180px;width:800px;height:560px;padding:50px 60px}
R .dl{display:flex;align-items:center;gap:22px;font-weight:800;font-size:40px;margin-top:26px}
R .dl i{display:block;height:20px;border-radius:10px;background:rgba(14,42,34,.16)}
R .p1{top:300px;width:500px;height:330px}
""",
    bg="",
    body=f"""
          <div class="grp" id="s01-g1">
            <div class="abs" id="s01-eq"><span>2년 공부</span><span style="color:rgba(255,255,255,.5)">+</span><span class="k">워크퍼밋 최대 3년</span></div>
            <div class="abs" id="s01-no"><div class="chip red" id="s01-x" style="position:relative;display:inline-block;font-size:52px;padding:16px 42px">아무 전공이나 되는 게 아니에요</div></div></div>
          <div class="grp" id="s01-g2">
            <div class="card" id="s01-doc">
              <div class="t" style="font-size:46px">졸업 후 워크퍼밋이 나오는 전공</div>
              <div class="b" style="font-size:28px;color:#14563f;margin-top:8px">컬리지 디플로마, 2024년 말부터 정부가 정한 목록</div>
              <div class="dl">{check("s01-k0", 48, "#14563f")}<i style="width:420px"></i></div>
              <div class="dl">{check("s01-k1", 48, "#14563f")}<i style="width:360px"></i></div>
              <div class="dl">{check("s01-k2", 48, "#14563f")}<i style="width:470px"></i></div>
              <div class="dl">{check("s01-k3", 48, "#14563f")}<i style="width:300px"></i></div></div></div>
          <div class="grp" id="s01-g3">
            <div class="abs hd" id="s01-h3" style="left:0;right:0;top:170px;text-align:center;font-size:56px">올즈컬리지 2년 디플로마 세 가지</div>
{''.join(f'            <div class="plot p1" id="s01-p{i}" style="left:{150 + i * 560}px;background:{m["color"]}"><div style="display:flex">{icon(m["icon"], "#0e2a22", 84)}</div><b style="margin-top:26px">{m["name"]}</b><span>{d}</span></div>' + chr(10) for i, (m, d) in enumerate(plots1))}
            <div class="chip cream" id="s01-ok" style="left:740px;top:690px;font-size:38px">농사 경험 없어도 괜찮아요</div></div>""",
    js="""
inn('#s01-eq',T('캐나다에서 2년'),{y:30});tl.fromTo('#s01-eq .k',{color:'#ffffff'},{color:'#e8b931',duration:0.4},T('최대 3년'));
stamp('#s01-x',T('아무 전공이나'),-3);
outt('#s01-g1',T('2024년 말부터')-0.35,{d:0.35});
tl.set('#s01-g2',{opacity:0},0);tl.set('#s01-g2',{opacity:1},T('2024년 말부터')-0.05);
inn('#s01-doc',T('2024년 말부터'),{y:40,r0:-3});
['#s01-k0','#s01-k1','#s01-k2','#s01-k3'].forEach((k,i)=>draw(k,T('정부가 정한 전공만')+i*0.18,0.4));
outt('#s01-g2',T('오늘은 그 목록에')-0.35,{d:0.35});
tl.set('#s01-g3',{opacity:0},0);tl.set('#s01-g3',{opacity:1},T('오늘은 그 목록에')-0.05);
inn('#s01-h3',T('오늘은 그 목록에'),{y:14});
tl.fromTo(['#s01-p0','#s01-p1','#s01-p2'].map(s=>q(s)),{opacity:0,y:120,rotation:-4},{opacity:1,y:0,rotation:0,duration:0.6,ease:'back.out(1.6)',stagger:0.22},T('2년 디플로마 세 가지'));
pop('#s01-ok',T('농사 경험 없어도'));
""",
    sfx=[("whoosh", "T('캐나다에서 2년')"), ("stamp", "T('아무 전공이나')"), ("pop", "T('정부가 정한 전공만')"),
         ("whoosh", "T('오늘은 그 목록에')"), ("pop", "T('2년 디플로마 세 가지')"), ("pop", "T('농사 경험 없어도')")],
)

# ---------------------------------------------------------------- S02 why agriculture
fields = [("농업 · 농식품", "농업과 농식품"), ("교육", "교육,"), ("보건", "보건,"), ("이공계", "이공계,"), ("기술직", "기술직,"), ("운송", "운송이요")]
tech3 = [("sf-03-drone-flying", "드론", "드론,"), ("sf-06-precision-ag", "자율주행 트랙터", "자율주행 트랙터"), ("sf-05-screens", "데이터 분석", "데이터 분석까지")]
S["s02"] = dict(
    css=COMMON_CSS + """
R .fd{position:absolute;width:500px;height:150px;border-radius:6px 26px 6px 26px;display:flex;align-items:center;padding:0 36px;font-weight:900;font-size:50px;background:rgba(243,236,220,.1);border:2px solid rgba(243,236,220,.25)}
R #s02-f0{background:#e8b931;border-color:#e8b931;color:#0e2a22}
R .t3{position:absolute;top:240px;width:520px;height:390px}
""",
    bg="",
    body=f"""
          <div class="grp" id="s02-g1">
            <div class="abs hd" id="s02-h" style="left:150px;top:140px;font-size:56px">컬리지 졸업 후 워크퍼밋이 나오는 분야</div>
{''.join(f'            <div class="fd" id="s02-f{i}" style="left:{150 + (i % 3) * 560}px;top:{270 + (i // 3) * 200}px">{t}</div>' + chr(10) for i, (t, _) in enumerate(fields))}
            <div class="chip gold" id="s02-op" style="left:150px;top:690px;font-size:38px">한국 분들이 잘 안 보는 분야라 오히려 기회</div></div>
          <div class="grp" id="s02-g2">
            <div class="abs hd" id="s02-h2" style="left:150px;top:140px;font-size:56px">요즘 농업은 기술 회사에 가깝다</div>
{''.join(f'            <div class="ph frame t3" id="s02-t{i}" style="left:{150 + i * 560}px"><img src="@P/{p}.jpg" alt="" /><div class="lab">{l}</div></div>' + chr(10) for i, (p, l, _) in enumerate(tech3))}          </div>""",
    js="""
inn('#s02-h',T('캐나다 정부가'),{y:14});
""" + "".join(f"pop('#s02-f{i}',T('{cue}'));" for i, (_, cue) in enumerate(fields)) + """
tl.to(['#s02-f1','#s02-f2','#s02-f3','#s02-f4','#s02-f5'].map(s=>q(s)),{opacity:0.3,duration:0.4},T('이 중에서 농업은'));
tl.to('#s02-f0',{scale:1.08,duration:0.3,yoyo:true,repeat:1},T('이 중에서 농업은'));
inn('#s02-op',T('기회가'),{y:20});
outt('#s02-g1',T('그리고 요즘 농업은')-0.35,{d:0.35});
tl.set('#s02-g2',{opacity:0},0);tl.set('#s02-g2',{opacity:1},T('그리고 요즘 농업은')-0.05);
inn('#s02-h2',T('그리고 요즘 농업은'),{y:14});
""" + "".join(f"flip('#s02-t{i}',T('{cue}'));kb('#s02-t{i} img',T('{cue}'),D-T('{cue}'));" for i, (_, _, cue) in enumerate(tech3)),
    sfx=[("pop", "T('농업과 농식품')"), ("pop", "T('운송이요')"), ("whoosh", "T('그리고 요즘 농업은')"), ("pop", "T('드론,')"), ("pop", "T('데이터 분석까지')")],
)

# ---------------------------------------------------------------- S03 Olds College
fair = ["카길", "뉴트리엔", "BASF"]
S["s03"] = dict(
    css=COMMON_CSS + """
R #s03-p1{left:700px;top:140px;width:1080px;height:470px}
R #s03-yr{left:700px;top:630px;font-size:120px;color:#e8b931}
R #s03-g2 .full img{filter:saturate(.9)}
R #s03-cnt{left:150px;top:200px;font-size:200px;color:#e8b931}
R .fc{position:absolute;top:470px;width:420px;height:150px;border-radius:6px 26px 6px 26px;background:#f3ecdc;color:#0e2a22;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px}
""",
    bg="",
    body=f"""
          <div class="grp" id="s03-g1">
            {ab_map('s03-map', 150, 140, 400)}
            <div class="abs hd" id="s03-dist" style="left:150px;top:760px;font-size:32px;color:#e8b931;white-space:nowrap">캘거리에서 북쪽으로 약 1시간</div>
            <div class="ph frame" id="s03-p1"><img src="@P/campus-03-aerial-water-tower.jpg" alt="" /></div>
            <div class="abs num" id="s03-yr">1913</div>
            <div class="abs hd" id="s03-ys" style="left:1040px;top:670px;font-size:40px;white-space:nowrap">문을 연 알버타 공립 컬리지</div></div>
          <div class="grp" id="s03-g2">
            <div class="full" id="s03-p2"><img src="@P/sf-15-crop-research.jpg" alt="" /></div><div class="dim" style="opacity:.55"></div>
            <div class="abs num" id="s03-cnt">3,300+</div>
            <div class="abs hd" id="s03-ac" style="left:160px;top:420px;font-size:56px;white-space:nowrap">에이커 스마트팜, 실제 농장에서 배워요</div>
            <div class="abs b" id="s03-src" style="left:160px;top:500px;font-size:28px;color:rgba(255,255,255,.75)">학교 자료 기준</div></div>
          <div class="grp" id="s03-g3">
            <div class="abs hd" id="s03-h3" style="left:150px;top:200px;font-size:56px">학교 커리어페어에 오는 농업 대기업</div>
{''.join(f'            <div class="fc" id="s03-c{i}" style="left:{150 + i * 470}px">{n}</div>' + chr(10) for i, n in enumerate(fair))}
            <div class="abs b" id="s03-s3" style="left:150px;top:660px;font-size:28px;color:rgba(255,255,255,.75)">학교 자료 기준 (2024 커리어페어 참가 기업 중 일부)</div></div>""",
    js="""
draw('#s03-map-out',0.1,1.0);tl.fromTo('#s03-map-fill',{opacity:0},{opacity:1,duration:0.6},0.6);
tl.fromTo('#s03-p1',{opacity:0,x:60},{opacity:1,x:0,duration:0.6,ease:'power3.out'},T('올즈컬리지는 1913년'));kb('#s03-p1 img',T('올즈컬리지는 1913년'),T('3,300에이커')-T('올즈컬리지는 1913년'));
odo('#s03-yr',T('올즈컬리지는 1913년')+0.3,1.0);inn('#s03-ys',T('공립 컬리지'),{y:12});
pop(['#s03-map-d0','#s03-map-d1','#s03-map-n0','#s03-map-n1'].map(s=>q(s)),T('캘거리에서 북쪽으로'));
tl.fromTo('#s03-map-pin',{opacity:0,y:-220},{opacity:1,y:0,duration:0.5,ease:'bounce.out'},T('캘거리에서 북쪽으로')+0.4);inn('#s03-map-pl',T('캘거리에서 북쪽으로')+0.8,{x:-10,y:0});
inn('#s03-dist',T('캘거리에서 북쪽으로')+0.9,{y:10});
outt('#s03-g1',T('3,300에이커')-0.6,{d:0.35});
tl.set('#s03-g2',{opacity:0},0);tl.set('#s03-g2',{opacity:1},T('3,300에이커')-0.3);
kb('#s03-p2 img',T('3,300에이커')-0.3,T('커리어페어에는')-T('3,300에이커'),{s:1.0},{s:1.12,x:-2});
odo('#s03-cnt',T('3,300에이커'),1.3);inn('#s03-ac',T('실제 농장에서'),{y:12});inn('#s03-src',T('실제 농장에서')+0.4,{y:10});
outt('#s03-g2',T('커리어페어에는')-0.35,{d:0.35});
tl.set('#s03-g3',{opacity:0},0);tl.set('#s03-g3',{opacity:1},T('커리어페어에는')-0.05);
inn('#s03-h3',T('커리어페어에는'),{y:14});pop('#s03-c0',T('카길'));pop('#s03-c1',T('뉴트리엔'));pop('#s03-c2',T('BASF'));inn('#s03-s3',T('BASF')+0.5,{y:10});
""",
    sfx=[("whoosh", "T('올즈컬리지는 1913년')"), ("pop", "T('캘거리에서 북쪽으로')+0.4"), ("impact", "T('3,300에이커')+0.4"),
         ("whoosh", "T('커리어페어에는')"), ("pop", "T('카길')"), ("pop", "T('BASF')")],
)

# ---------------------------------------------------------------- S04 Techgronomy (sky blue, drone)
GRID = "".join(
    f'<i style="left:{(k % 10) * 62}px;top:{(k // 10) * 62}px;background:rgba(95,178,255,{0.18 + 0.75 * (((k * 37) % 11) / 10):.2f})"></i>'
    for k in range(50))
S["s04"] = dict(
    css=COMMON_CSS + """
R #s04-eq{left:150px;top:300px;display:flex;align-items:center;gap:30px;font-weight:900;font-size:72px;white-space:nowrap}
R #s04-eq .op{color:rgba(255,255,255,.45)}
R #s04-grid{left:150px;top:220px;width:620px;height:310px}
R #s04-grid i{position:absolute;width:56px;height:56px;border-radius:8px}
R #s04-ph{left:880px;top:200px;width:880px;height:400px}
R #s04-bar{left:150px;top:330px;width:1620px;height:110px;border-radius:6px 26px 6px 26px;background:rgba(243,236,220,.12);overflow:hidden}
R #s04-int{position:absolute;right:0;top:0;width:{w}px;height:110px;background:#5fb2ff;color:#0b2a45;font-size:0}
R #s04-il{left:1100px;top:450px;width:670px;text-align:right;font-weight:900;font-size:40px;color:#5fb2ff;white-space:nowrap}
R #s04-aia{left:150px;top:540px;width:1000px;padding:30px 40px}
""".replace("{w}", str(round(1620 * 4 / 24))),
    bg=furrow(T_["color"]),
    body=f"""
          {tag('s04-tag', T_, 150, 140)}
          <div class="grp" id="s04-g1">
            <div class="abs" id="s04-eq"><span>Technology</span><span class="op">+</span><span>Agronomy</span><span class="op">=</span><span style="color:#5fb2ff">Techgronomy</span></div>
            <div class="abs hd" id="s04-eqk" style="left:150px;top:420px;font-size:44px;color:rgba(255,255,255,.8);white-space:nowrap">기술 + 작물학</div></div>
          <div class="grp" id="s04-g2">
            <div class="abs" id="s04-grid">{GRID}</div>
            <div class="abs hd" id="s04-gl" style="left:150px;top:560px;font-size:38px;width:640px">드론·센서 데이터로 정하는 비료량</div>
            <div class="ph frame" id="s04-ph"><img src="@P/sf-04-sensor.jpg" alt="" /></div></div>
          <div class="grp" id="s04-g3">
            <div class="abs hd" id="s04-h3" style="left:150px;top:250px;font-size:44px">2년 과정</div>
            <div class="abs" id="s04-bar"><div id="s04-int"></div></div>
            <div class="abs" id="s04-il">그중 4개월은 급여를 받는 인턴십</div>
            <div class="card" id="s04-aia"><div class="t" style="font-size:40px">졸업 후 알버타 농업전문가협회(AIA) 자격 과정 도전 가능</div></div>
            <div class="chip" id="s04-rec" style="left:150px;top:700px;font-size:38px;border-color:#5fb2ff">컴퓨터·데이터에 관심 있는 분께</div></div>""",
    js="""
inn('#s04-tag',T('첫 번째는'),{x:-30,y:0});
inn('#s04-eq',T('기술, 테크놀로지와'),{y:20});tl.fromTo('#s04-eq span:last-child',{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.5,ease:'back.out(2)'},T('합친 말이에요'));
inn('#s04-eqk',T('작물학, 애그로노미를'),{y:12});
outt('#s04-g1',T('드론과 센서로')-0.35,{d:0.35});
tl.set('#s04-g2',{opacity:0},0);tl.set('#s04-g2',{opacity:1},T('드론과 센서로')-0.05);
tl.fromTo(qa('#s04-grid i'),{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.35,ease:'back.out(2)',stagger:{each:0.025,from:'start'}},T('드론과 센서로'));
inn('#s04-gl',T('어디에 비료를'),{y:12});flip('#s04-ph',T('드론과 센서로')+0.3);kb('#s04-ph img',T('드론과 센서로'),T('2년 과정 중에')-T('드론과 센서로'));
outt('#s04-g2',T('2년 과정 중에')-0.35,{d:0.35});
tl.set('#s04-g3',{opacity:0},0);tl.set('#s04-g3',{opacity:1},T('2년 과정 중에')-0.05);
inn('#s04-h3',T('2년 과정 중에'),{y:12});grow('#s04-bar',T('2년 과정 중에'),0.7);
tl.fromTo('#s04-int',{xPercent:100},{xPercent:0,duration:0.6,ease:'power3.out'},T('4개월은'));inn('#s04-il',T('4개월은')+0.3,{y:10});
inn('#s04-aia',T('졸업하면 알버타'),{y:30});pop('#s04-rec',T('컴퓨터나 데이터에'));
""",
    sfx=[("whoosh", "T('첫 번째는')"), ("pop", "T('합친 말이에요')"), ("whoosh", "T('드론과 센서로')"), ("pop", "T('4개월은')"), ("pop", "T('컴퓨터나 데이터에')")],
)

# ---------------------------------------------------------------- S05 Horticulture (blossom pink, leaf)
learn5 = [("식물 재배", "식물 재배"), ("온실 관리", "온실 관리"), ("조경 설계", "조경 설계"), ("원예 창업", "원예 창업까지")]
campus5 = [("campus-05-central-gardens", "식물원"), ("sf-13-indoor-ag", "온실")]
S["s05"] = dict(
    css=COMMON_CSS + """
R .lc{position:absolute;top:290px;width:380px;height:170px;border-radius:6px 26px 6px 26px;background:#ff8fb4;color:#4a0f26;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:52px}
R .c5{position:absolute;top:240px;width:640px;height:400px}
R #s05-fs{left:150px;top:300px;width:1100px;padding:40px 50px}
""",
    bg=furrow(H_["color"]),
    body=f"""
          {tag('s05-tag', H_, 150, 140)}
          <div class="grp" id="s05-g1">
{''.join(f'            <div class="lc" id="s05-l{i}" style="left:{150 + i * 410}px">{t}</div>' + chr(10) for i, (t, _) in enumerate(learn5))}          </div>
          <div class="grp" id="s05-g2">
{''.join(f'            <div class="ph frame c5" id="s05-c{i}" style="left:{150 + i * 680}px"><img src="@P/{p}.jpg" alt="" /><div class="lab">{l}</div></div>' + chr(10) for i, (p, l) in enumerate(campus5))}
            <div class="chip" id="s05-wet" style="left:1500px;top:300px;font-size:38px;border-color:#ff8fb4">+ 습지</div>
            <div class="abs hd" id="s05-cl" style="left:150px;top:680px;font-size:46px">캠퍼스 자체가 실습장</div></div>
          <div class="grp" id="s05-g3">
            <div class="card" id="s05-fs"><div class="t" style="font-size:52px">필드스쿨</div>
              <div class="t" style="font-size:40px;margin-top:16px;color:#4a0f26">업체에서 급여를 받으면서 실습</div></div>
            <div class="chip" id="s05-rec" style="left:150px;top:600px;font-size:38px;border-color:#ff8fb4">식물·손으로 만드는 일 좋아하는 분께</div></div>""",
    js="""
inn('#s05-tag',T('두 번째는'),{x:-30,y:0});
""" + "".join(f"pop('#s05-l{i}',T('{cue}'));" for i, (_, cue) in enumerate(learn5)) + """
outt('#s05-g1',T('학교 안에 습지')-0.35,{d:0.35});
tl.set('#s05-g2',{opacity:0},0);tl.set('#s05-g2',{opacity:1},T('학교 안에 습지')-0.05);
pop('#s05-wet',T('학교 안에 습지'));flip('#s05-c0',T('학교 안에 습지')+0.4);flip('#s05-c1',T('학교 안에 습지')+0.8);
kb('#s05-c0 img',T('학교 안에 습지'),T('중간에 필드스쿨이')-T('학교 안에 습지'));kb('#s05-c1 img',T('학교 안에 습지'),T('중간에 필드스쿨이')-T('학교 안에 습지'));
inn('#s05-cl',T('캠퍼스 자체가'),{y:14});
outt('#s05-g2',T('중간에 필드스쿨이')-0.35,{d:0.35});
tl.set('#s05-g3',{opacity:0},0);tl.set('#s05-g3',{opacity:1},T('중간에 필드스쿨이')-0.05);
inn('#s05-fs',T('중간에 필드스쿨이'),{y:30});pop('#s05-rec',T('손으로 만드는 일'));
""",
    sfx=[("whoosh", "T('두 번째는')"), ("pop", "T('식물 재배')"), ("pop", "T('원예 창업까지')"), ("whoosh", "T('학교 안에 습지')"), ("pop", "T('중간에 필드스쿨이')")],
)

# ---------------------------------------------------------------- S06 Agricultural management (harvest amber, chart)
biz = [("회계", "회계, 마케팅"), ("마케팅", "회계, 마케팅")]
farm = [("작물", "작물과 가축"), ("가축", "작물과 가축"), ("농기계", "농기계까지")]
S["s06"] = dict(
    css=COMMON_CSS + """
R .col{position:absolute;top:260px;width:780px;height:400px;border-radius:6px 26px 6px 26px;padding:36px 40px;border:3px solid rgba(243,236,220,.25)}
R .col h4{font-weight:900;font-size:44px;margin:0 0 26px}
R .col .chip{position:relative;display:inline-block;margin:0 14px 16px 0;font-size:40px}
R .tr6{position:absolute;top:330px;width:700px;height:200px;border-radius:6px 26px 6px 26px;padding:36px 44px;color:#3f2604}
R .tr6 b{display:block;font-weight:900;font-size:58px}
R .tr6 span{display:block;font-weight:800;font-size:34px;margin-top:10px}
R #s06-ua{left:150px;top:300px;width:1200px;padding:40px 50px}
""",
    bg=furrow(M_["color"]),
    body=f"""
          {tag('s06-tag', M_, 150, 140)}
          <div class="grp" id="s06-g1">
            <div class="col" id="s06-a" style="left:150px"><h4>경영 과목</h4>{''.join(f'<div class="chip cream" id="s06-b{i}">{t}</div>' for i, (t, _) in enumerate(biz))}</div>
            <div class="col" id="s06-b" style="left:990px"><h4 style="color:#f4a63c">농업 전반</h4>{''.join(f'<div class="chip" id="s06-f{i}" style="border-color:#f4a63c">{t}</div>' for i, (t, _) in enumerate(farm))}</div></div>
          <div class="grp" id="s06-g2">
            <div class="abs hd" id="s06-h2" style="left:150px;top:250px;font-size:44px">전공은 두 가지 중에 선택</div>
            <div class="tr6" id="s06-t0" style="left:150px;background:#f4a63c"><b>AgriCommerce</b><span>애그리커머스 · 농업 비즈니스</span></div>
            <div class="tr6" id="s06-t1" style="left:900px;background:#f3ecdc"><b>Production</b><span>프로덕션 · 생산</span></div></div>
          <div class="grp" id="s06-g3">
            <div class="card" id="s06-ua"><div class="t" style="font-size:44px">앨버타 대학교로 이어서 공부할 수 있는 편입 협약</div>
              <div class="b" style="font-size:30px;margin-top:14px;color:#3f2604">학교 자료 기준 · 인정 학점은 학교 확인</div></div>
            {arrow('s06-ar', 1380, 340, 300, 60)}
            <div class="chip" id="s06-rec" style="left:150px;top:600px;font-size:38px;border-color:#f4a63c">경영·영업 경력이 있는 분께</div></div>""",
    js="""
inn('#s06-tag',T('세 번째는'),{x:-30,y:0});
inn('#s06-a',T('회계, 마케팅'),{x:-30,y:0});pop(['#s06-b0','#s06-b1'].map(s=>q(s)),T('회계, 마케팅')+0.3);
inn('#s06-b',T('작물과 가축'),{x:30,y:0});pop(['#s06-f0','#s06-f1'].map(s=>q(s)),T('작물과 가축')+0.2);pop('#s06-f2',T('농기계까지'));
outt('#s06-g1',T('전공은 두 가지')-0.35,{d:0.35});
tl.set('#s06-g2',{opacity:0},0);tl.set('#s06-g2',{opacity:1},T('전공은 두 가지')-0.05);
inn('#s06-h2',T('전공은 두 가지'),{y:12});flip('#s06-t0',T('애그리커머스'));flip('#s06-t1',T('프로덕션이에요'));
outt('#s06-g2',T('학교 자료에 따르면')-0.35,{d:0.35});
tl.set('#s06-g3',{opacity:0},0);tl.set('#s06-g3',{opacity:1},T('학교 자료에 따르면')-0.05);
inn('#s06-ua',T('학교 자료에 따르면'),{y:30});draw('#s06-ar',T('편입 협약도'),0.6);pop('#s06-rec',T('경영이나 영업'));
""",
    sfx=[("whoosh", "T('세 번째는')"), ("pop", "T('회계, 마케팅')"), ("pop", "T('농기계까지')"), ("whoosh", "T('전공은 두 가지')"),
         ("pop", "T('애그리커머스')"), ("pop", "T('프로덕션이에요')"), ("whoosh", "T('학교 자료에 따르면')")],
)

# ---------------------------------------------------------------- S07 tuition
fees = [(T_, "19,172", "19,172"), (H_, "19,220", "19,220"), (M_, "19,172", "19,185")]
S["s07"] = dict(
    css=COMMON_CSS + """
R #s07-cd{left:150px;top:140px;width:1180px;height:520px}
R .tr{position:absolute;left:40px;width:1100px;height:96px;display:flex;align-items:center;font-weight:800;font-size:36px;color:#0e2a22}
R .tr .a{width:520px;display:flex;align-items:center;gap:16px}
R .tr .a i{display:block;width:18px;height:52px;border-radius:9px}
R .tr .c{width:290px;text-align:right;font-weight:900;font-variant-numeric:tabular-nums}
R .tr.hd{font-size:26px;color:#14563f;height:60px}
R .hr{position:absolute;left:40px;width:1100px;height:2px;background:rgba(14,42,34,.14)}
R #s07-sum{left:1380px;top:140px;width:400px;padding:34px 36px}
R .bar7{position:absolute;left:1380px;height:70px;border-radius:0 18px 18px 0}
""",
    bg="",
    body=f"""
          <div class="card" id="s07-cd">
            <div class="tr hd" style="top:30px"><span class="a">전공 (유학생 학비+필수비용)</span><span class="c">1년차 CAD</span><span class="c">2년차 CAD</span></div>
{''.join(f'            <div class="tr" id="s07-r{i}" style="top:{110 + i * 110}px"><span class="a"><i style="background:{m["color"]}"></i>{m["name"]}</span><span class="c" id="s07-y{i}">${a}</span><span class="c">${b}</span></div><div class="hr" style="top:{205 + i * 110}px"></div>' + chr(10) for i, (m, a, b) in enumerate(fees))}
            <div class="b" id="s07-src" style="position:absolute;left:40px;top:450px;font-size:26px;color:#14563f">2026-27 학교 학비표(2026-08-10판) · 책값 별도 · 농업경영은 AgriCommerce 기준</div></div>
          <div class="card" id="s07-sum"><div class="t" style="font-size:32px">1년 약</div><div class="t num" style="font-size:72px;color:#14563f">$19,000</div>
            <div class="t" style="font-size:32px;margin-top:18px">2년 약</div><div class="t num" style="font-size:72px;color:#14563f">$38,000</div></div>
          <div class="abs b" id="s07-cl" style="left:1380px;top:560px;font-size:28px;color:rgba(255,255,255,.8)">1년 학비 비교</div>
          <div class="bar7" id="s07-b0" style="top:610px;width:{round(400 * 19.2 / 35.2)}px;background:#e8b931"></div>
          <div class="abs b" id="s07-l0" style="left:1390px;top:690px;font-size:26px">디플로마 약 $19,200</div>
          <div class="bar7" id="s07-b1" style="top:730px;width:400px;background:rgba(243,236,220,.4)"></div>
          <div class="abs b" id="s07-l1b" style="left:1390px;top:740px;font-size:26px;color:#0e2a22;font-weight:800">EP1 학사 3년차 약 $35,225</div>
          <div class="chip cream" id="s07-in" style="left:150px;top:700px;font-size:36px">입학: 세 전공 모두 가을 9월</div>""",
    js="""
inn('#s07-cd',T('학비는 세 전공이'),{y:40,s:0.97});
""" + "".join(f"inn('#s07-r{i}',T('학비는 세 전공이')+{0.4 + i * 0.25:.2f},{{x:-20,y:0}});" for i in range(3)) + """
odo('#s07-y0',T('학비는 세 전공이')+0.4,1.0);odo('#s07-y1',T('학비는 세 전공이')+0.65,1.0);odo('#s07-y2',T('학비는 세 전공이')+0.9,1.0);
inn('#s07-src',T('2026년 학교 학비표')+0.6,{y:10});
inn('#s07-sum',T('1년에 약 1만 9천'),{x:40,y:0});
tl.fromTo('#s07-sum .num:last-of-type',{opacity:0},{opacity:1,duration:0.4},T('2년이면 약 3만 8천'));
inn('#s07-cl',T('학사 과정보다'),{y:10});grow('#s07-b0',T('학사 과정보다'),0.6);inn('#s07-l0',T('학사 과정보다')+0.3,{y:8});
grow('#s07-b1',T('학사 과정보다')+0.5,0.8);inn('#s07-l1b',T('학사 과정보다')+0.9,{y:8});
pop('#s07-in',T('입학은 세 전공'));
""",
    sfx=[("pop", "T('2026년 학교 학비표')"), ("impact", "T('1년에 약 1만 9천')+0.3"), ("whoosh", "T('학사 과정보다')"), ("pop", "T('입학은 세 전공')")],
)

# ---------------------------------------------------------------- S08 after graduation
cips = [(T_, "CIP 01.0000"), (H_, "CIP 01.0601"), (M_, "CIP 01.0101 / 01.0301")]
S["s08"] = dict(
    css=COMMON_CSS + """
R .cp{position:absolute;left:150px;display:flex;align-items:center;gap:24px;font-weight:900;font-size:44px;white-space:nowrap}
R .cp small{font-weight:700;font-size:30px;color:rgba(255,255,255,.7)}
R #s08-pg{left:1080px;top:230px;width:690px;padding:40px 44px}
R #s08-wage{left:150px;top:300px;width:1620px;height:120px;border-radius:6px 26px 6px 26px;background:rgba(243,236,220,.1);border:2px solid rgba(243,236,220,.25)}
R #s08-rng{position:absolute;left:{a}px;width:{w}px;top:0;height:116px;border-radius:6px 26px 6px 26px;background:#e8b931;color:#0e2a22;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;white-space:nowrap}
R .city{position:absolute;top:560px;width:500px;height:150px;border-radius:6px 26px 6px 26px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:46px}
R .city span{font-size:28px;font-weight:700;margin-top:8px}
""".replace("{a}", str(round(1620 * 0.30))).replace("{w}", str(round(1620 * 0.45))),
    bg="",
    body=f"""
          <div class="grp" id="s08-g1">
            <div class="abs hd" id="s08-h1" style="left:150px;top:140px;font-size:52px">워크퍼밋 대상 전공 목록에 있어요</div>
{''.join(f'            <div class="cp" id="s08-c{i}" style="top:{260 + i * 120}px">{check(f"s08-k{i}", 64, m["color"])}<span style="color:{m["color"]}">{m["short"]}</span><small>{c}</small></div>' + chr(10) for i, (m, c) in enumerate(cips))}
            <div class="card" id="s08-pg"><div class="t" style="font-size:40px">2년 과정이라</div><div class="t" style="font-size:78px;color:#14563f;margin-top:8px">워크퍼밋 최대 3년</div></div></div>
          <div class="grp" id="s08-g2">
            <div class="abs hd" id="s08-h2" style="left:150px;top:200px;font-size:48px">이 분야 직업들의 평균 시급</div>
            <div class="abs" id="s08-wage"><div id="s08-rng">$30대 초반 ~ $40대 후반 / 시간</div></div>
            <div class="abs b" id="s08-ws" style="left:150px;top:440px;font-size:28px;color:rgba(255,255,255,.75)">학교 자료 기준 · 직업별 평균</div>
            <div class="city" id="s08-y0" style="left:150px;background:rgba(243,236,220,.12)">밴쿠버 · 토론토<span>집값·렌트 부담 큼</span></div>
            <div class="city" id="s08-y1" style="left:700px;background:#e8b931;color:#0e2a22">알버타<span>부담이 덜한 편</span></div></div>""",
    js="""
inn('#s08-h1',T('세 전공 모두 정부의'),{y:14});
""" + "".join(f"inn('#s08-c{i}',T('세 전공 모두 정부의')+{0.4 + i * 0.3:.1f},{{x:-30,y:0}});draw('#s08-k{i}',T('세 전공 모두 정부의')+{0.6 + i * 0.3:.1f},0.4);" for i in range(3)) + """
inn('#s08-pg',T('2년 과정이라'),{x:40,y:0});slam('#s08-pg .t:last-child',T('최대 3년까지'),{s:1.6});
outt('#s08-g1',T('학교 자료로 보면')-0.35,{d:0.35});
tl.set('#s08-g2',{opacity:0},0);tl.set('#s08-g2',{opacity:1},T('학교 자료로 보면')-0.05);
inn('#s08-h2',T('학교 자료로 보면'),{y:12});grow('#s08-wage',T('학교 자료로 보면')+0.2,0.6);
grow('#s08-rng',T('30달러대 초반'),0.9);inn('#s08-ws',T('40달러대 후반'),{y:8});
inn('#s08-y0',T('밴쿠버나 토론토보다'),{y:20});inn('#s08-y1',T('밴쿠버나 토론토보다')+0.4,{y:20});
""",
    sfx=[("pop", "T('세 전공 모두 정부의')+0.4"), ("impact", "T('최대 3년까지')+0.42"), ("whoosh", "T('학교 자료로 보면')"), ("pop", "T('30달러대 초반')")],
)

# ---------------------------------------------------------------- S09 closing + CTA
pick = [("데이터와 기술이 좋으면", T_, "데이터와 기술이"), ("식물과 손으로 하는 일이 좋으면", H_, "식물과 손으로"), ("경영 경력을 살리고 싶으면", M_, "경영 경력을")]
S["s09"] = dict(
    css=COMMON_CSS + """
R .pk{position:absolute;left:150px;width:1620px;height:130px;border-radius:6px 26px 6px 26px;background:rgba(243,236,220,.08);display:flex;align-items:center;padding:0 40px;gap:30px;font-weight:800;font-size:44px}
R .pk b{margin-left:auto;font-weight:900;font-size:52px;display:flex;align-items:center;gap:18px}
R #s09-band{position:absolute;inset:0;background:rgba(9,30,24,.94)}
R #s09-aa{left:0;right:0;top:210px;text-align:center;font-size:140px;letter-spacing:.02em;white-space:nowrap}
R #s09-l1{left:0;right:0;top:390px;text-align:center;font-size:44px;color:#e8b931;white-space:nowrap}
R #s09-btn{left:560px;top:500px;width:800px;height:112px;border-radius:60px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:48px;box-shadow:0 16px 40px rgba(200,16,46,.45)}
R #s09-tel{left:0;right:0;top:640px;text-align:center;font-size:36px;color:rgba(255,255,255,.88)}
""",
    bg="",
    body=f"""
          <div class="abs hd" id="s09-h" style="left:150px;top:140px;font-size:52px">나에게 맞는 전공은</div>
{''.join(f'          <div class="pk" id="s09-p{i}" style="top:{250 + i * 160}px;border-left:12px solid {m["color"]}">{t}<b style="color:{m["color"]}">{icon(m["icon"], m["color"], 60)}{m["short"]}</b></div>' + chr(10) for i, (t, m, _) in enumerate(pick))}
          <div class="abs" id="s09-cta" style="inset:0">
            <div class="abs" id="s09-band"></div>
            <div class="abs" id="s09-pts" style="inset:0"></div>
            <div class="abs h" id="s09-aa">AA CANADA</div>
            <div class="abs hd" id="s09-l1">학력·영어 점수에 맞는 전공부터 같이 골라 드려요</div>
            <div class="abs" id="s09-btn">무료 상담 · 카톡 canlog</div>
            <div class="abs b" id="s09-tel">02-567-4345</div></div>""",
    js="""
inn('#s09-h',T('정리해 볼게요'),{y:14});
""" + "".join(f"inn('#s09-p{i}',T('{cue}'),{{x:-40,y:0}});" for i, (_, _, cue) in enumerate(pick)) + """
const CT=T('내 학력과 경력으로');
outt(['#s09-h','#s09-p0','#s09-p1','#s09-p2'].map(s=>q(s)),CT-0.3,{y:-20,d:0.3});
tl.fromTo('#s09-band',{opacity:0},{opacity:1,duration:0.5},CT-0.2);
mask('#s09-aa',CT+0.1,0.7,'l');inn('#s09-l1',T('고등학교 성적과'),{y:12});
slam('#s09-btn',T('AA Canada에'),{s:1.5,shake:false});inn('#s09-tel',T('AA Canada에')+0.3,{y:10});
const PU=T('AA Canada에')+0.6;tl.to('#s09-btn',{scale:1.05,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:Math.max(1,Math.floor((D-PU)/0.6)-1)},PU);
burst('#s09-pts',T('AA Canada에')+0.2,40,960,556,600,11);
""",
    sfx=[("pop", "T('데이터와 기술이')"), ("pop", "T('식물과 손으로')"), ("pop", "T('경영 경력을')"), ("whoosh", "T('내 학력과 경력으로')-0.2"), ("impact", "T('AA Canada에')+0.42")],
)
