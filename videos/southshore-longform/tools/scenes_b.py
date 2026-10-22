"""S04-S06 (people / census, Riverside School Board, four high schools)."""
import math

import geo
from clips import dur as clip_dur
from mapkit import cam_html, cam_move_js, cam_set_js, icon, label, pin, reel
from scenes_a import V_S

S = {}

# ---------------------------------------------------------------- S04 people (2021 census)
BARS = [  # key, label, value, cue
    ("coq", "코퀴틀람 (BC)", 11900, "T('코퀴틀람에는')"),
    ("bro", "브로사드", 590, "T('롱게일도 425명')+1.0"),
    ("lon", "롱게일", 425, "T('롱게일도 425명')"),
    ("stl", "생랑베르", 50, "T('생랑베르는 50명')"),
    ("stb", "생브루노", 35, "T('생브루노는 35명')"),
    ("bou", "부셔빌", 30, "T('부셔빌은 30명')"),
]
BMAX = 1080
ASIAN = [  # city key (geo.CITIES), share %, label
    ("brossard", 20.1, "약 20%"),
    ("longueuil", 3.3, "약 3%"),
    ("stlambert", 2.8, "약 3%"),
    ("boucherville", 2.0, "약 2%"),
    ("stbruno", 1.9, "약 2%"),
]
_CITY = {k: (la, lo) for k, _, la, lo in geo.CITIES}
V_ASIAN = geo.view(45.525, -73.44, 52, cy=400)


def _bubbles(v):
    out = []
    for k, pct, txt in ASIAN:
        la, lo = _CITY[k]
        x, y = geo.map_xy(la, lo)
        r = (30 + 20 * math.sqrt(pct)) / v["scale"]
        hot = k == "brossard"
        out.append(f'<div class="bub bub-{k}" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;'
                   f'font-size:{(40 if hot else 26) / v["scale"]:.1f}px;background:{"rgba(200,16,46,.88)" if hot else "rgba(255,214,207,.95)"};'
                   f'color:{"#fff" if hot else "#7A1B26"}">{txt}</div>')
    return "".join(out)


_bar_rows = "".join(
    f'<div class="brow br-{k}" style="top:{250 + i * 92}px"><div class="bl">{n}</div><div class="bt"><i class="bb bb-{k}" '
    f'style="width:{max(8, BMAX * val / 11900):.0f}px"></i><span class="bv num bv-{k}" style="left:{max(8, BMAX * val / 11900) + 18:.0f}px">'
    f'{val:,}명</span></div></div>' for i, (k, n, val, _) in enumerate(BARS))
_bar_js = "".join(f"grow('.bb-{k}',{cue},{1.2 if k == 'coq' else 0.5});inn('.bv-{k}',{cue}+{0.9 if k == 'coq' else 0.3},{{x:-20,y:0}});"
                  f"inn('.br-{k} .bl',{cue}-0.2,{{x:-30,y:0}});" for k, _, _, cue in BARS)

S["s04"] = dict(
    css="""
R .kids{position:absolute;left:560px;top:300px;display:flex;gap:26px}
R .worry{left:680px;top:200px;font-size:46px}
R .ttl{left:120px;top:150px;font-size:60px}
R .ttl small{font-size:30px;color:#7A1B26;font-family:'Noto Sans KR',sans-serif;font-weight:700;margin-left:18px}
R .brow{position:absolute;left:120px;width:1680px;height:72px;display:flex;align-items:center}
R .bl{width:330px;font-weight:900;font-size:38px}
R .bt{position:relative;flex:1;height:56px}
R .bb{position:absolute;left:0;top:6px;height:44px;border-radius:0 12px 12px 0;background:#C8102E}
R .br-coq .bb{background:#7A1B26}
R .bv{position:absolute;top:2px;font-size:48px;white-space:nowrap}
R .br-coq .bv{color:#7A1B26}
R .pct8{left:1200px;top:296px;font-size:34px}
R .ttl3{left:120px;top:150px;font-size:54px;z-index:5}
R .bub{position:absolute;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 10px 26px rgba(122,27,38,.18)}
R .honest{left:1290px;top:200px;font-size:54px}
R .cv1{left:1250px;top:330px;font-size:32px}
R .cv2{left:1250px;top:410px;font-size:32px}
R .pick{position:absolute;top:250px;width:780px;height:420px;padding:44px 50px}
R .pick .h{font-weight:900;font-size:44px;margin-bottom:26px}
R .pick .a{font-size:84px;line-height:1.1}
R .pk1{left:120px}.pk2{left:1020px}
""",
    body=f"""
<div class="tag"><i></i>3 · 한국 사람이 거의 없는 동네</div>
<div class="ph p1">
  <div class="bubble pink worry">“가 보니까 반에 한국 아이가 너무 많더라…”</div>
  <div class="kids">{"".join(icon("school", 120, c) for c in ["#E9CFCB", "#E9CFCB", "#C8102E", "#E9CFCB"])}</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs bhs ttl">한국계 인구 <small>2021 캐나다 인구조사</small></div>
  {_bar_rows}
  <div class="chip solid pct8">시 인구의 약 8%</div>
</div>
<div class="ph p3" style="opacity:0">
  {cam_html("".join(label(f"bc-{k}", n, la, lo, V_ASIAN, 28, dx=72 if k != 'brossard' else 130, dy=0, dot=False)
                    for k, n, la, lo in geo.CITIES if k in dict((a[0], 1) for a in ASIAN)) + _bubbles(V_ASIAN))}
  <div class="abs bhs ttl3">아시아계 비율 <span class="red">(2021 인구조사)</span></div>
  <div class="stamp honest">솔직하게</div>
  <div class="chip pink cv1">아시아 마트·식당 가까움 → 생활 편함</div>
  <div class="chip solid cv2">그래도 한국계 590명 (1% 미만)</div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="card pick pk1"><div class="h">영어만 쓰는 환경을 원하면</div><div class="a bhs red">생랑베르 · 부셔빌</div></div>
  <div class="card pick pink pk2"><div class="h">생활 편의도 같이 본다면</div><div class="a bhs">브로사드</div></div>
</div>
""",
    js=f"""
pop('.kids svg',T('두 번째 포인트는'),0.12);inn('.worry',T('가 보니까'),{{y:20}});
phase('.p2',T('2021년 캐나다'),'.p1');inn('.ttl',T('2021년 캐나다'),{{y:20}});
{_bar_js}
pop('.pct8',T('시 인구의 8%'));
{cam_set_js(V_ASIAN)}
phase('.p3',T('아시아계 전체로'),'.p2');inn('.ttl3',T('아시아계 전체로'),{{y:20}});
pop('.bub-stlambert,.bc-stlambert',T('생랑베르, 부셔빌, 생브루노는')-0.1,0.05);pop('.bub-boucherville,.bc-boucherville',T('부셔빌, 생브루노는'),0.05);
pop('.bub-stbruno,.bc-stbruno',T('생브루노는 인구의'),0.05);pop('.bub-longueuil,.bc-longueuil',T('생브루노는 인구의')+0.6,0.05);
stamp('.honest',T('솔직하게'),-6);slam('.bub-brossard',T('브로사드는 조금'),{{s:2.2}});inn('.bc-brossard',T('브로사드는 조금')+0.3,{{y:-10}});
pulse('.bub-brossard',T('20% 정도'));inn('.cv1',T('아시아 마트나'),{{x:40,y:0}});inn('.cv2',T('590명'),{{x:40,y:0}});
phase('.p4',T('그래서 아이가'),'.p3');inn('.pk1',T('영어만 쓰는'),{{x:-60,y:0}});inn('.pk2',T('생활 편의도 같이'),{{x:60,y:0}});
""",
    sfx=[("pop", "T('가 보니까')"), ("whoosh", "T('2021년 캐나다')-0.3"), ("impact", "T('코퀴틀람에는')+1.2"),
         ("pop", "T('생랑베르는 50명')"), ("whoosh", "T('아시아계 전체로')-0.3"), ("stamp", "T('솔직하게')+0.3"),
         ("impact", "T('브로사드는 조금')+0.38"), ("whoosh", "T('그래서 아이가')-0.3")],
)

# ---------------------------------------------------------------- S05 Riverside School Board
V_RSB = geo.view(45.45, -73.40, 66, cy=440)
_TERR = [(45.735, -73.47), (45.68, -73.20), (45.52, -73.08), (45.30, -73.10), (45.22, -73.28), (45.26, -73.55),
         (45.36, -73.73), (45.43, -73.55), (45.50, -73.52), (45.60, -73.47)]


def _terr_overlay():
    return f'<path class="terr" d="{geo._smooth(_TERR)}" fill="rgba(200,16,46,.20)" stroke="#C8102E" stroke-width="{6 / V_RSB["scale"]:.1f}" stroke-dasharray="{18 / V_RSB["scale"]:.1f} {12 / V_RSB["scale"]:.1f}" opacity="0"/>'


S["s05"] = dict(
    css="""
R .rsb{left:1000px;top:560px;font-size:40px}
R .rq{left:120px;top:150px;font-size:58px;z-index:5}
R .law{position:absolute;left:120px;top:250px;width:760px;height:400px;padding:44px}
R .law .h{font-weight:900;font-size:40px;margin:22px 0 10px}
R .law .b{font-size:32px;color:#7A1B26;font-weight:700}
R .arrow{position:absolute;left:910px;top:400px;font-size:90px;color:#C8102E}
R .ok{position:absolute;left:1040px;top:250px;width:760px;height:400px;padding:44px}
R .ok .h{font-weight:900;font-size:40px;margin:22px 0 10px}
R .ok .b{font-size:32px;font-weight:700}
R .nums{position:absolute;left:120px;top:200px;width:1680px;display:flex;gap:40px}
R .nums .card{position:relative;flex:1;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center}
R .nums .k{font-weight:900;font-size:40px;color:#7A1B26}
R .nums .v{font-size:150px;color:#C8102E}
R .nums .v small{font-size:60px}
R .r1st{left:1180px;top:560px;font-size:60px}
R .src{left:120px;top:600px;font-size:28px;color:#7A1B26;font-weight:700}
R .slogan{top:180px;font-size:110px;font-family:'Black Han Sans',sans-serif}
R .slk{top:330px;font-size:48px;font-weight:900;color:#7A1B26}
R .steps{position:absolute;left:520px;top:430px;width:880px;height:330px}
R .stp{position:absolute;bottom:0;width:280px;border-radius:20px 20px 0 0;background:#C8102E;color:#fff;display:flex;align-items:flex-start;justify-content:center;padding-top:22px;font-weight:900;font-size:38px}
R .st1{left:0;height:130px;background:#FFD6CF;color:#7A1B26}.st2{left:300px;height:210px;background:#E86A7E}.st3{left:600px;height:300px}
""",
    body=f"""
<div class="tag"><i></i>4 · 리버사이드 교육청</div>
<div class="ph p1">
  {cam_html(label("rsb-sjsr", "생장쉬르리슐리외", geo.SJSR[1], geo.SJSR[2], V_RSB, 28) +
            label("rsb-dt", "다운타운", *geo.DOWNTOWN, V_RSB, 28, dx=-130, dy=34), overlay=_terr_overlay())}
  <div class="abs bhs rq">사우스쇼어의 <span class="red">영어 공립학교</span>는?</div>
  <div class="chip solid rsb">리버사이드 교육청 · Riverside School Board</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card law">{icon("shield", 90, "#7A1B26")}<div class="h">퀘벡은 영어학교 입학을 법으로 제한</div><div class="b">불어헌장 · 대부분 불어학교로</div></div>
  <div class="arrow bhs">→</div>
  <div class="card red ok">{icon("school", 90, "#fff")}<div class="h">조기유학생은 OK</div><div class="b">교육청 국제학생 프로그램을 통해 영어학교 입학</div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="nums">
    <div class="card n1"><div class="k">초등학교</div><div class="v num"><span class="o1">19</span><small>곳</small></div></div>
    <div class="card n2"><div class="k">고등학교</div><div class="v num"><span class="o2">4</span><small>곳</small></div></div>
    <div class="card red n3"><div class="k" style="color:#fff">졸업·자격 취득률</div><div class="v num" style="color:#fff">88.5<small>%</small></div></div>
  </div>
  <div class="stamp r1st">몬테레지 1위</div>
  <div class="abs src">* 교육청 2026-27 브로슈어 기준</div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="abs center slogan">Success in <span class="red">both</span> languages</div>
  <div class="abs center slk">영어와 불어, 둘 다 잘하기 · 수업은 영어로</div>
  <div class="steps"><div class="stp st1">기본</div><div class="stp st2">심화</div><div class="stp st3">모국어 수준</div></div>
</div>
""",
    js=f"""
{cam_set_js(V_RSB)}
inn('.rq',0.4,{{y:20}});tl.to(q('.terr'),{{opacity:1,duration:1.0,ease:'power2.out'}},T('리버사이드 교육청이'));pop('.rsb',T('리버사이드 교육청이')+0.4);
inn('.rsb-dt',0.8,{{y:10}});inn('.rsb-sjsr',T('리버사이드 교육청이')+1.0,{{y:10}});
phase('.p2',T('퀘벡은 영어학교'),'.p1');inn('.law',T('퀘벡은 영어학교'),{{x:-60,y:0}});pop('.arrow',T('조기유학생은 교육청'));inn('.ok',T('조기유학생은 교육청')+0.2,{{x:60,y:0}});
phase('.p3',T('리버사이드는 초등학교'),'.p2');inn('.n1',T('초등학교 19곳'),{{y:30}});odo('.o1',T('초등학교 19곳'),1.2);
inn('.n2',T('고등학교 4곳'),{{y:30}});inn('.n3',T('88.5%'),{{y:30}});stamp('.r1st',T('몬테레지 지역 1위'),-6);inn('.src',T('교육청 브로슈어에'),{{y:10}});
phase('.p4',T('교육청 슬로건이'),'.p3');kin('.slogan',T('Success in both'),0.03);inn('.slk',T('영어와 불어 둘 다'),{{y:16}});
grow('.st1',T('3단계로')-0.6,0.5,'y');grow('.st2',T('3단계로')-0.3,0.5,'y');grow('.st3',T('3단계로'),0.5,'y');
""",
    sfx=[("whoosh", "T('리버사이드 교육청이')"), ("whoosh", "T('퀘벡은 영어학교')-0.3"), ("pop", "T('조기유학생은 교육청')"),
         ("whoosh", "T('리버사이드는 초등학교')-0.3"), ("stamp", "T('몬테레지 지역 1위')+0.3"), ("whoosh", "T('교육청 슬로건이')-0.3"),
         ("pop", "T('3단계로')")],
)

# ---------------------------------------------------------------- S06 four high schools
V_HS = geo.view(45.50, -73.45, 24, cy=520)
SCHOOLS = [  # key, cue, next cue, clips, card
    ("heritage", "T('생위베르의 헤리티지')", "T('그린필드파크의 센테니얼')",
     ["her-sign", "her-foyer", "her-dance", "her-gym", "her-ican", "her-studio"],
     dict(name="헤리티지", en="Heritage Regional HS", area="생위베르", size="학생 1,600명+",
          chips=["IB 중등(MYP)", "예술", "스포츠", "컴퓨터·IT"], fit="좋아하는 게 분명한 아이")),
    ("centennial", "T('그린필드파크의 센테니얼')", "T('생랑베르 인터내셔널은')",
     ["cen-sign", "cen-atrium", "cen-lab", "cen-stage", "cen-library"],
     dict(name="센테니얼", en="Centennial Regional HS", area="그린필드파크", size="학생 약 1,100명",
          chips=["영재반 TaG"], fit="Fraser 2025 · 리버사이드 4개교 중 점수 1위")),
    ("sli", "T('생랑베르 인터내셔널은')", "T('마지막으로 생장쉬르리슐리외')",
     ["sli-sign", "sli-library", "sli-garden", "sli-gym", "sli-music"],
     dict(name="생랑베르 인터내셔널", en="Saint-Lambert International HS", area="생랑베르", size="학생 약 400명",
          chips=["IB", "교복", "휴대폰 보관"], fit="작은 학교, 세심한 관리")),
    ("stjohns", "T('마지막으로 생장쉬르리슐리외')", "T('같이 가는 경우에')+2.6",
     ["stj-entrance", "stj-hub", "stj-gym", "stj-theatre", "stj-motto"],
     dict(name="세인트 존스", en="St. Johns School", area="생장쉬르리슐리외", size="4세 유치원 ~ 고등학교 한 학교",
          chips=["형제·남매"], fit="초·중·고 한 학교")),
]


def _school_items(k, cue, nxt, names):
    end = f"({nxt})-0.3"
    items, t = [], 0.0
    for i in range(12):
        nm = names[i % len(names)]
        d = clip_dur(nm) - 0.05
        items.append((nm, f"{cue}+0.3+{t:.3f}", f"max(0,min({d:.3f},{end}-({cue}+0.3+{t:.3f})))"))
        t += d
    return items


def _school_block(k, cue, nxt, names, c):
    chips = "".join(f'<span class="sch">{x}</span>' for x in c["chips"])
    return (f'<div class="ph sc sc-{k}" style="opacity:0">'
            f'{reel("s06", "rv-" + k, 110, 150, 1060, 596, _school_items(k, cue, nxt, names))}'
            f'<div class="card scard"><div class="nm bhs">{c["name"]}</div><div class="en">{c["en"]}</div>'
            f'<div class="row"><span class="ar">{c["area"]}</span></div><div class="sz">{c["size"]}</div>'
            f'<div class="chips">{chips}</div><div class="fit">{c["fit"]}</div></div></div>')


_hs_pins = "".join(pin(f"hp-{k}", la, lo, V_HS, 62) + label(f"hl-{k}", n, la, lo, V_HS, 32, dot=False, dx=34, dy=-40, kind="mtag")
                   for k, n, la, lo, _ in geo.HIGH if k != "stjohns")
_school_js = ""
_prev = ".p1"
for k, cue, nxt, names, c in SCHOOLS:
    _school_js += (f"phase('.sc-{k}',{cue}-0.2,'{_prev}');inn('.sc-{k} .broll',{cue}-0.2,{{x:-60,y:0}});inn('.sc-{k} .scard',{cue},{{x:60,y:0}});"
                   f"pop('.sc-{k} .sch',{cue}+1.2,0.15);inn('.sc-{k} .fit',{cue}+2.2,{{y:16}});")
    _prev = f".sc-{k}"

S["s06"] = dict(
    css="""
R .hst{left:120px;top:150px;font-size:58px;z-index:5}
R .sjsr{left:1290px;top:720px;font-size:32px}
R .scard{position:absolute;left:1200px;top:150px;width:610px;height:596px;padding:40px 40px}
R .scard .nm{font-size:62px;color:#C8102E;line-height:1.1}
R .scard .en{font-size:26px;font-weight:700;color:#7A1B26;margin-top:6px}
R .scard .row{margin-top:26px;font-weight:900;font-size:36px}
R .scard .sz{font-weight:700;font-size:34px;margin-top:10px}
R .scard .chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
R .scard .sch{display:inline-block;padding:8px 24px;border-radius:99px;background:#C8102E;color:#fff;font-weight:900;font-size:32px}
R .scard .fit{position:absolute;left:40px;right:40px;bottom:36px;font-weight:900;font-size:32px;color:#7A1B26;background:#FFD6CF;border-radius:16px;padding:14px 20px}
""",
    body=f"""
<div class="tag"><i></i>5 · 고등학교 4곳</div>
<div class="ph p1">
  {cam_html(_hs_pins + label("hs-dt", "다운타운", *geo.DOWNTOWN, V_HS, 28, dx=-130, dy=-30))}
  <div class="abs bhs hst">리버사이드 <span class="red">고등학교 4곳</span></div>
  <div class="chip solid sjsr">세인트 존스 ↘ 생장쉬르리슐리외</div>
</div>
{"".join(_school_block(k, cue, nxt, names, c) for k, cue, nxt, names, c in SCHOOLS)}
""",
    js=f"""
{cam_set_js(V_HS)}
inn('.hst',0.3,{{y:20}});inn('.hs-dt',0.6,{{y:10}});
tl.fromTo(qa('.hp-heritage,.hp-centennial,.hp-sli'),{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.6,ease:'bounce.out',stagger:0.35}},T('지도에 찍어'));
pop('.hl-heritage,.hl-centennial,.hl-sli',T('지도에 찍어')+0.4,0.35);pop('.sjsr',T('지도에 찍어')+1.6);
{_school_js}
""",
    sfx=[("pop", "T('지도에 찍어')"), ("whoosh", "T('생위베르의 헤리티지')-0.3"), ("whoosh", "T('그린필드파크의 센테니얼')-0.3"),
         ("whoosh", "T('생랑베르 인터내셔널은')-0.3"), ("whoosh", "T('마지막으로 생장쉬르리슐리외')-0.3")],
)
