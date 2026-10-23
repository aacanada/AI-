"""S01-S03 (opening, where is the South Shore, REM). Cues: T('phrase') = when that phrase is spoken."""
import json
import os

import geo
from clips import dur as clip_dur
from common import maple
from mapkit import cam_html, cam_move_js, cam_set_js, clock, icon, label, pin, reel, seq

S = {}
_MAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canada_map.json")))

V_ISL = geo.view(45.535, -73.60, 64, cy=380)
V_S = geo.view(45.522, -73.47, 44, cy=460)
V_REM = geo.view(45.468, -73.50, 21, cx=1000, cy=440)


def canada_svg(cls, hi="qc"):
    paths = "".join(f'<path class="pv pv-{k}" d="{p}" fill="{"#C8102E" if k == hi else "#E9CFCB"}" stroke="#FFF8F2" stroke-width="2"/>'
                    for k, p in _MAP["paths"].items())
    return f'<svg class="{cls}" viewBox="{_MAP["viewBox"]}">{paths}</svg>'


def south_overlay():
    d = geo._smooth(geo.SOUTH + [(45.20, -74.06), (45.20, -73.10), (45.76, -73.10)])
    return f'<path class="southglow" d="{d}" fill="#FFD6CF" opacity="0"/>'


def cross_arrow(v):
    x0, y0 = geo.map_xy(*geo.DOWNTOWN)
    x1, y1 = geo.map_xy(45.492, -73.478)
    w = 9 / v["scale"]
    return (f'<path class="xarrow" d="M{x0:.0f},{y0:.0f} Q{(x0 + x1) / 2:.0f},{min(y0, y1) - 160:.0f} {x1:.0f},{y1:.0f}" '
            f'fill="none" stroke="#C8102E" stroke-width="{w:.1f}" stroke-linecap="round" stroke-dasharray="{3 * w:.1f} {2 * w:.1f}"/>')


# ---------------------------------------------------------------- S01 opening
_hook, _hook_len = seq(["her-foyer", "cen-stage", "sli-garden", "stj-entrance"], "T('수업을 영어로')", 1.5, clip_dur)
S["s01"] = dict(
    css="""
R .q1{top:250px;font-size:190px}
R .q1 .eq{color:#C8102E}
R .q2{top:520px;font-size:66px;color:#7A1B26}
R .st1{left:1240px;top:150px;font-size:58px}
R .p2 .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,248,242,0) 50%,rgba(255,248,242,.86) 64%)}
R .ch-en{left:1170px;top:150px;font-size:36px}
R .t-box{left:220px;top:190px;width:1480px;height:520px;padding:70px 90px}
R .t1{font-size:120px}
R .t2{font-size:56px;color:#7A1B26;margin-top:24px}
R .t3{position:absolute;right:80px;bottom:56px;display:flex;align-items:center;gap:16px;font-size:34px;font-weight:900;color:#2B2B2B}
R .t3 img{width:70px;height:68px}
R .goals{position:absolute;left:220px;top:690px;width:1480px;display:flex;justify-content:center;gap:30px}
R .goals .chip{position:relative;font-size:40px;padding:14px 40px}
""",
    body=f"""
<div class="ph p1">
  <div class="abs center bhs q1">몬트리올 <span class="eq">=</span> 불어?</div>
  <div class="abs center hd q2">그래서 조기유학 후보에서 빼셨나요?</div>
  <div class="stamp st1">후보 제외?</div>
</div>
<div class="ph p2" style="opacity:0">
  {cam_html(
      label("l-isl", "몬트리올 섬", 45.585, -73.735, V_ISL, 46, dot=False) +
      label("l-dt", "다운타운", *geo.DOWNTOWN, V_S, 30, dx=-150, dy=-34) +
      label("l-ss", "강 건너 남쪽", 45.565, -73.40, V_S, 40, dot=False, kind="mtag"),
      overlay=south_overlay() + cross_arrow(V_S))}
  <div class="shade"></div>
  <div class="chip solid ch-en">수업을 영어로 하는 공립학교</div>
  {reel("s01", "hook", 1170, 230, 640, 360, _hook)}
</div>
<div class="ph p3" style="opacity:0">
  <div class="card t-box">
    <div class="bhs t1">몬트리올 <span class="red">사우스쇼어</span></div>
    <div class="hd t2">지도로 보는 영어 공립학교 동네</div>
    <div class="t3"><img src="@I/aa-canada-logo-transparent.png" alt="" />AA Canada 원장</div>
  </div>
  <div class="goals"><div class="chip g1">① 어디에 있나</div><div class="chip g2">② 다운타운까지</div><div class="chip solid g3">③ 어떤 학교</div></div>
</div>
""",
    js=f"""
kin('.q1',0.4,0.06);inn('.q2',T('조기유학 후보에서'),{{y:24}});stamp('.st1',T('조기유학 후보에서')+0.9,-8);
{cam_set_js(V_ISL)}
phase('.p2',T('그런데'),'.p1');inn('.l-isl',T('그런데')+0.2,{{y:16}});
{cam_move_js(V_S, "T('강 하나만')-0.4", 2.4)}
outt('.l-isl',T('강 하나만')-0.6);
tl.to(q('.southglow'),{{opacity:0.75,duration:0.8,ease:'power2.out'}},T('강 하나만')+1.6);
inn('.l-dt',T('강 하나만')+1.2,{{y:12}});draw('.xarrow',T('강 하나만')+1.6,1.1);pop('.l-ss',T('강 하나만')+2.4);
pop('.ch-en',T('수업을 영어로'));inn('.hook',T('수업을 영어로')-0.2,{{x:60,y:0}});
phase('.p3',T('안녕하세요'),'.p2');inn('.t-box',T('안녕하세요'),{{s:0.92}});kin('.t1',T('안녕하세요')+0.2);inn('.t2',T('안녕하세요')+1.0,{{y:20}});
inn('.t3',T('AA Canada 원장입니다'),{{x:40,y:0}});
pop('.g1',T('어디에 있는지'));pop('.g2',T('다운타운까지 어떻게'));pop('.g3',T('어떤 학교들이'));
""",
    sfx=[("stamp", "T('조기유학 후보에서')+1.2"), ("whoosh", "T('그런데')-0.3"), ("whoosh", "T('강 하나만')-0.3"),
         ("pop", "T('수업을 영어로')"), ("whoosh", "T('안녕하세요')-0.3"), ("pop", "T('어디에 있는지')"),
         ("pop", "T('다운타운까지 어떻게')"), ("pop", "T('어떤 학교들이')")],
)

# ---------------------------------------------------------------- S02 where
_city_labels = "".join(label(f"c-{k}", n, la, lo, V_S, 34) for k, n, la, lo in geo.CITIES)
_city_js = "".join(f"inn('.c-{k}',T('{n}'),{{y:14,d:0.45}});" for k, n, _, _ in geo.CITIES)
_cpin_x = 120 + 585 * 560 / 793
_cpin_y = 110 + 905 * 729 / 1032
S["s02"] = dict(
    css=f"""
R .cmap{{position:absolute;left:120px;top:110px;width:560px;height:729px}}
R .cpin{{position:absolute;left:{_cpin_x - 22:.0f}px;top:{_cpin_y - 60:.0f}px;width:44px;height:60px}}
R .cpinl{{position:absolute;left:{_cpin_x + 34:.0f}px;top:{_cpin_y - 70:.0f}px;font-family:'Black Han Sans',sans-serif;font-size:44px;color:#C8102E;white-space:nowrap;background:#fff;border:4px solid #C8102E;border-radius:16px;padding:4px 18px}}
R .qcl{{position:absolute;left:760px;top:240px;font-size:54px}}
R .qcs{{position:absolute;left:760px;top:330px;font-size:36px;color:#7A1B26;font-weight:700}}
R .life{{left:120px;top:140px;width:640px;padding:30px 36px}}
R .life .ic{{display:flex;gap:18px;margin-bottom:14px}}
R .life .tx{{font-weight:900;font-size:40px;line-height:1.35}}
R .dtic{{position:absolute}}
""",
    body=f"""
<div class="tag"><b>1</b>사우스쇼어는 어디?</div>
<div class="ph p1">
  {canada_svg("cmap")}
  <svg class="cpin" viewBox="0 0 44 60"><path d="M22 58 C 8 38, 2 30, 2 22 A20 20 0 0 1 42 22 C 42 30, 36 38, 22 58 Z" fill="#7A1B26"/><circle cx="22" cy="22" r="8" fill="#fff"/></svg>
  <div class="cpinl">몬트리올</div>
  <div class="abs bhs qcl">캐나다 <span class="red">퀘벡주</span></div>
  <div class="abs qcs">밴쿠버·토론토와 같은 캐나다, 동쪽의 퀘벡주</div>
</div>
<div class="ph p2" style="opacity:0">
  {cam_html(
      label("l-isl2", "몬트리올 섬", 45.585, -73.735, V_ISL, 50, dot=False) +
      label("l-river", "세인트로렌스 강", 45.418, -73.70, V_ISL, 36, dot=False, kind="water-lab") +
      label("l-ss2", "사우스쇼어 · Rive-Sud", 45.585, -73.36, V_S, 40, dot=False, kind="mtag") +
      _city_labels +
      label("l-dt2", "다운타운", *geo.DOWNTOWN, V_S, 30, dx=-150, dy=-34),
      overlay=south_overlay())}
  <div class="card life"><div class="ic">{icon("house", 76)}{icon("tree", 76, "#7A1B26")}{icon("house", 76)}</div>
    <div class="tx">마당 있는 주택 · 공원</div><div class="tx red">조용한 교외</div></div>
</div>
""",
    js=f"""
inn('.cmap',0.3,{{s:0.94}});tl.fromTo(q('.cpin'),{{opacity:0,y:-80}},{{opacity:1,y:0,duration:0.6,ease:'bounce.out'}},T('먼저 위치부터')+0.6);
inn('.cpinl',T('먼저 위치부터')+1.0,{{x:-20,y:0}});inn('.qcl',T('먼저 위치부터')+0.3,{{x:40,y:0}});inn('.qcs',T('먼저 위치부터')+0.8,{{x:40,y:0}});
{cam_set_js(V_ISL)}
phase('.p2',T('몬트리올은 세인트로렌스'),'.p1');inn('.l-isl2',T('몬트리올은 세인트로렌스')+0.3,{{y:16}});inn('.l-river',T('한가운데에 있는 섬'),{{x:-30,y:0}});
outt('.l-isl2,.l-river',T('이 강 건너')-0.5);
{cam_move_js(V_S, "T('이 강 건너')-0.3", 2.2)}
tl.to(q('.southglow'),{{opacity:0.8,duration:0.9,ease:'power2.out'}},T('남쪽을'));pop('.l-ss2',T('사우스쇼어,'));pulse('.l-ss2',T('리브쉬드'));
{_city_js}
inn('.l-dt2',T('다운타운 빌딩'),{{y:12}});
inn('.life',T('마당 있는'),{{x:-60,y:0}});
""",
    sfx=[("pop", "T('먼저 위치부터')+1.1"), ("whoosh", "T('몬트리올은 세인트로렌스')-0.3"), ("whoosh", "T('이 강 건너')-0.3"),
         ("pop", "T('사우스쇼어,')"), ("pop", "T('브로사드')"), ("pop", "T('생브루노')"), ("whoosh", "T('마당 있는')-0.2")],
)

# ---------------------------------------------------------------- S03 REM
def _rem_overlay(v):
    w = 14 / v["scale"]
    cw = 30 / v["scale"]
    return (f'<path class="champ" d="{geo.champlain_d()}" fill="none" stroke="#FFFFFF" stroke-width="{cw:.1f}" stroke-linecap="round" opacity="0"/>'
            f'<path class="remline" d="{geo.rem_path_d()}" fill="none" stroke="#C8102E" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle class="train" r="{16 / v["scale"]:.1f}" cx="0" cy="0" fill="#2B2B2B" stroke="#fff" stroke-width="{5 / v["scale"]:.1f}" opacity="0"/>')


def _stations(v):
    out = []
    for k, n, la, lo in geo.REM_STATIONS:
        x, y = geo.map_xy(la, lo)
        r = 13 / v["scale"]
        out.append(f'<svg class="stn stn-{k}" viewBox="0 0 {geo.W} {geo.H}" width="{geo.W}" height="{geo.H}" style="position:absolute;left:0;top:0">'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" stroke="#C8102E" stroke-width="{6 / v["scale"]:.1f}"/></svg>')
    off = {"brossard": (24, 16), "quartier": (24, -26), "panama": (-40, -70), "ids": (-60, 30), "gare": (24, -6)}
    for k, n, la, lo in geo.REM_STATIONS:
        dx, dy = off[k]
        out.append(label(f"sl-{k}", n + ("역" if k != "gare" else ""), la, lo, v, 30, dot=False, dx=dx, dy=dy, kind="mtag"))
    return "".join(out)


S["s03"] = dict(
    css="""
R .rt{left:120px;top:330px;width:520px;padding:28px 34px}
R .rt .a{font-family:'Black Han Sans',sans-serif;font-size:96px;color:#C8102E;line-height:1}
R .rt .b{font-weight:900;font-size:36px;margin-top:10px}
R .badge{left:120px;top:580px;font-size:32px}
R .stats{position:absolute;left:1360px;top:150px;width:440px;display:flex;flex-direction:column;gap:18px}
R .stats .card{position:relative;padding:18px 30px;display:flex;align-items:baseline;justify-content:space-between}
R .stats .k{font-weight:900;font-size:34px;color:#7A1B26}
R .stats .v{font-size:84px;color:#C8102E}
R .stats .v small{font-size:44px}
R .freq{left:120px;top:690px;font-size:30px}
R .champ-l{left:0;top:0}
R .p2 .col{position:absolute;top:220px;width:520px;height:440px;padding:40px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
R .p2 .col .ic{display:flex;gap:16px;margin-bottom:22px}
R .p2 .col .h{font-size:44px}
R .p2 .col .s{font-size:32px;font-weight:700;color:#7A1B26;margin-top:8px}
R .p2 .c1{left:120px}.p2 .c3{left:1280px}
R .p2 .mid{position:absolute;left:700px;top:330px;width:520px;text-align:center}
R .p2 .mid .n{font-size:150px;color:#C8102E}
R .p2 .mid .line{left:40px;top:250px;width:440px}
""",
    body=f"""
<div class="tag"><b>2</b>REM, 다운타운까지 18분</div>
<div class="ph p1">
  {cam_html(_stations(V_REM) + label("champ-tag", "샹플랭 다리", 45.4605, -73.522, V_REM, 30, dot=False, kind="mtag", dy=46),
            overlay=_rem_overlay(V_REM))}
  <div class="card rt"><div class="a">REM</div><div class="b">몬트리올의 새 <span class="red">무인 경전철</span></div></div>
  <div class="chip solid badge">2023.07.31 개통 · 첫 구간이 사우스쇼어</div>
  <div class="stats">
    <div class="card s1"><span class="k">역</span><span class="v num"><span class="n1">5</span><small>개</small></span></div>
    <div class="card s2"><span class="k">거리</span><span class="v num">16.6<small>km</small></span></div>
    <div class="card red s3"><span class="k" style="color:#fff">시간</span><span class="v num" style="color:#fff"><span class="n3">18</span><small>분</small></span></div>
  </div>
  <div class="chip pink freq">출퇴근 3분 45초 간격 (개통 당시)</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card col c1"><div class="ic">{icon("house", 90)}{icon("school", 90, "#7A1B26")}</div><div class="h bhs">평일</div><div class="s">조용한 교외에서 학교</div></div>
  <div class="mid"><div>{icon("train", 120)}</div><div class="num n">18분</div></div>
  <div class="card col c3"><div class="ic">{icon("museum", 90)}{icon("theatre", 90, "#7A1B26")}</div><div class="h bhs">주말</div><div class="s">다운타운 박물관·공연장</div></div>
</div>
""",
    js=f"""
{cam_set_js(V_REM)}
inn('.rt',T('바로 REM'),{{x:-40,y:0}});kin('.rt .a',T('바로 REM')+0.1);
pop('.badge',T('2023년 7월 31일'));pulse('.badge',T('사우스쇼어 노선이에요'));
(function(){{const p=q('.remline'),L=p.getTotalLength();p.style.strokeDasharray=L+' '+L;tl.fromTo(p,{{strokeDashoffset:L}},{{strokeDashoffset:0,duration:Math.max(2.5,T('중앙역까지')-T('브로사드역에서')+0.4),ease:'none'}},T('브로사드역에서'));}})();
tl.set(q('.train'),{{opacity:1}},T('브로사드역에서'));
(function(){{const p=q('.remline'),c=q('.train'),L=p.getTotalLength(),o={{v:0}};
  const put=()=>{{const pt=p.getPointAtLength(o.v*L);c.setAttribute('cx',pt.x);c.setAttribute('cy',pt.y);}};put();
  tl.to(o,{{v:1,duration:Math.max(2.5,T('중앙역까지')-T('브로사드역에서')+0.4),ease:'none',onUpdate:put}},T('브로사드역에서'));}})();
pop('.stn-brossard,.sl-brossard',T('브로사드역에서'),0.05);pop('.stn-quartier,.sl-quartier',T('뒤 카르티에'),0.05);
pop('.stn-panama,.sl-panama',T('파나마'),0.05);pop('.stn-ids,.sl-ids',T('일데쇠르'),0.05);pop('.stn-gare,.sl-gare',T('중앙역까지'),0.05);
inn('.s1',T('역은 다섯 개'),{{x:60,y:0}});inn('.s2',T('16.6킬로미터'),{{x:60,y:0}});slam('.s3',T('18분에'),{{s:1.6}});
tl.to(q('.champ'),{{opacity:0.95,duration:0.5}},T('샹플랭 다리'));pop('.champ-tag',T('샹플랭 다리'));pulse('.champ-tag',T('강을 건너고'));
pop('.freq',T('3, 4분마다'));
phase('.p2',T('그러니까 아이는'),'.p1');inn('.c1',T('그러니까 아이는'),{{x:-60,y:0}});pop('.mid',T('18분 만에'));inn('.c3',T('다운타운 박물관'),{{x:60,y:0}});
""",
    sfx=[("pop", "T('바로 REM')"), ("pop", "T('2023년 7월 31일')"), ("whoosh", "T('브로사드역에서')"), ("pop", "T('중앙역까지')"),
         ("impact", "T('18분에')+0.38"), ("pop", "T('샹플랭 다리')"), ("whoosh", "T('그러니까 아이는')-0.3"), ("pop", "T('18분 만에')")],
)
