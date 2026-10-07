#!/usr/bin/env python3
"""Generates index.html + compositions/sNN.html from the narration-aligned script.

Timing source: build/units.json — each script sentence aligned (pause-detection + DP)
to the recorded narration. Real voice timing drives every scene boundary and beat.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = json.load(open(os.path.join(ROOT, "build", "units.json")))
TOTAL = 415.69
W, H = 1920, 1080


def us(i, f=0.0):
    """global time inside unit i at fraction f of its spoken span"""
    u = U[i]
    return u["start"] + f * (u["end"] - u["start"])


# ---------------------------------------------------------------- scenes
# (id, first unit, last unit, transition-in kind, chapter label)
SCENES = [
    ("s01", 0, 2, None, None),
    ("s02", 3, 3, "push", None),
    ("s03", 4, 5, "push", None),
    ("s04", 6, 8, "chapter", ("PART 01", "배우자 오픈 워크퍼밋이 뭔가요?")),
    ("s05", 9, 11, "push", None),
    ("s06", 12, 14, "chapter", ("PART 02", "규정이 어떻게 바뀌었나")),
    ("s07", 15, 16, "push", None),
    ("s08", 17, 18, "chapter", ("PART 03", "주 신청자가 취업비자일 때")),
    ("s09", 19, 24, "push", None),
    ("s10", 25, 28, "push", None),
    ("s11", 29, 34, "chapter", ("PART 04", "주 신청자가 학생비자일 때")),
    ("s12", 35, 38, "push", None),
    ("s13", 39, 42, "push", None),
    ("s14", 43, 46, "chapter", ("PART 05", "자주 하는 오해 3가지")),
    ("s15", 47, 48, "push", None),
    ("s16", 49, 53, "chapter", ("PART 06", "그래서 어떻게 준비하나요?")),
    ("s17", 54, 55, "chapter", ("SUMMARY", "한 장으로 정리")),
    ("s18", 56, 58, "blur", None),
]
CHAPTER_OF = {"s04": 0, "s05": 0, "s06": 1, "s07": 1, "s08": 2, "s09": 2, "s10": 2,
              "s11": 3, "s12": 3, "s13": 3, "s14": 4, "s15": 4, "s16": 5}
CHAPTERS = ["기본 원리", "규정 변화", "취업비자", "학생비자", "오해", "준비"]

LEAD = 0.45      # scene starts this long before its first word
XF = 0.7         # transition overlap
starts = []
for k, (sid, a, b, kind, chap) in enumerate(SCENES):
    starts.append(0.0 if k == 0 else round(U[a]["start"] - LEAD - (0.5 if kind == "chapter" else 0), 2))
ends = starts[1:] + [TOTAL]


# ---------------------------------------------------------------- shared css
FONT_FACE = "".join(
    f'@font-face{{font-family:"Pretendard";src:url("assets/fonts/Pretendard-{n}.woff2") format("woff2");font-weight:{w};font-style:normal;}}'
    for n, w in [("Light", 300), ("Regular", 400), ("Medium", 500), ("SemiBold", 600),
                 ("Bold", 700), ("ExtraBold", 800), ("Black", 900)])

SHARED_CSS = """
:root{--paper:#F4EFE6;--paper-2:#EAE2D4;--paper-3:#DED3C0;--ink:#18233A;--ink-soft:#4A5468;
--red:#C8281E;--green:#1F7A4D;--amber:#9A6212;--line:#C9BBA3;}
.sc{position:absolute;inset:0;font-family:"Pretendard",sans-serif;color:var(--ink);word-break:keep-all;}
.sc .mono{font-family:"JetBrains Mono",monospace;}
.sc .ghost{position:absolute;font-family:"Pretendard",sans-serif;font-weight:900;font-size:420px;letter-spacing:-0.04em;
  color:var(--ink);opacity:.07;white-space:nowrap;line-height:1;pointer-events:none;}
.sc .glow{position:absolute;width:900px;height:900px;border-radius:50%;
  background:radial-gradient(circle,rgba(200,40,30,.16) 0%,rgba(200,40,30,0) 65%);}
.sc .kicker{position:absolute;left:120px;top:150px;font-family:"JetBrains Mono",monospace;font-size:24px;font-weight:700;
  letter-spacing:.12em;color:var(--red);display:flex;align-items:center;gap:16px;}
.sc .kicker::before{content:"";display:block;width:56px;height:4px;background:var(--red);}
.sc .h1{position:absolute;left:120px;top:196px;font-size:84px;font-weight:900;letter-spacing:-0.035em;line-height:1.12;width:1680px;}
.sc .h1 em{font-style:normal;color:var(--red);}
.sc .card{position:absolute;background:#FBF8F2;border:3px solid var(--ink);border-radius:22px;box-shadow:10px 10px 0 var(--paper-3);}
.sc .pill{display:inline-flex;align-items:center;padding:12px 26px;border-radius:999px;border:3px solid var(--ink);
  font-size:32px;font-weight:700;background:#FBF8F2;white-space:nowrap;}
.sc .stamp{position:absolute;display:flex;align-items:center;justify-content:center;padding:10px 30px;border:7px solid currentColor;
  border-radius:16px;font-size:52px;font-weight:900;letter-spacing:.02em;white-space:nowrap;background:rgba(251,248,242,.85);}
.sc .ok{color:var(--green);} .sc .no{color:var(--red);} .sc .warn{color:var(--amber);}
.sc .tag{font-family:"JetBrains Mono",monospace;font-size:24px;font-weight:700;letter-spacing:.08em;color:var(--ink-soft);}
.sc .body{font-size:40px;font-weight:500;line-height:1.45;color:var(--ink);}
.sc .muted{color:var(--ink-soft);}
.sc .row{display:flex;align-items:center;gap:24px;}
.sc .ic{flex:none;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:38px;font-weight:900;color:#FBF8F2;}
.sc .ic.ok{background:var(--green);color:#FBF8F2;} .sc .ic.no{background:var(--red);color:#FBF8F2;} .sc .ic.warn{background:var(--amber);color:#FBF8F2;}
.sc .ic.ink{background:var(--ink);color:#FBF8F2;}
.sc svg .draw{fill:none;stroke-linecap:round;stroke-linejoin:round;}
"""

# ---------------------------------------------------------------- helpers injected in every scene script
JS_HELPERS = """
const R='[data-composition-id="%(id)s"] ';
const tl=gsap.timeline({paused:true});
const $=(s)=>R+s;
function rise(s,t,o){o=o||{};tl.fromTo($(s),{opacity:0,y:o.y==null?40:o.y,x:o.x||0,scale:o.s||1},{opacity:1,y:0,x:0,scale:1,duration:o.d||0.6,ease:o.e||'power3.out',stagger:o.st||0},t);}
function popin(s,t,o){o=o||{};tl.fromTo($(s),{opacity:0,scale:o.s||0.6},{opacity:1,scale:1,duration:o.d||0.55,ease:o.e||'back.out(1.7)',stagger:o.st||0},t);}
function slide(s,t,dx,o){o=o||{};tl.fromTo($(s),{opacity:0,x:dx},{opacity:1,x:0,duration:o.d||0.7,ease:o.e||'expo.out',stagger:o.st||0},t);}
function stamp(s,t,rot){tl.fromTo($(s),{opacity:0,scale:1.9,rotation:rot-14},{opacity:1,scale:1,rotation:rot,duration:0.42,ease:'power4.in'},t);
  tl.fromTo($(s),{y:0},{y:4,duration:0.08,yoyo:true,repeat:1,ease:'none',immediateRender:false},t+0.42);}
function draw(s,t,d,e){tl.fromTo($(s),{strokeDashoffset:1},{strokeDashoffset:0,duration:d||0.9,ease:e||'power2.inOut'},t);}
function bar(s,t,o){o=o||{};tl.fromTo($(s),{scaleX:0},{scaleX:1,duration:o.d||0.8,ease:o.e||'power3.out',stagger:o.st||0},t);}
function barY(s,t,o){o=o||{};tl.fromTo($(s),{scaleY:0},{scaleY:1,duration:o.d||0.9,ease:o.e||'power3.out',stagger:o.st||0},t);}
function strike(s,t){tl.fromTo($(s),{scaleX:0},{scaleX:1,duration:0.35,ease:'power2.in'},t);}
function dim(s,t,v){tl.fromTo($(s),{opacity:1},{opacity:v==null?0.28:v,duration:0.5,ease:'power1.inOut'},t);}
function count(s,t,from,to,d,suffix){const el=document.querySelector($(s));const o={v:from};
  tl.fromTo(o,{v:from},{v:to,duration:d||1,ease:'power2.out',onUpdate:()=>{el.textContent=Math.round(o.v)+(suffix||'');}},t);}
function ambient(dur){if(document.querySelector($('.ghost')))tl.fromTo($('.ghost'),{x:0},{x:-160,duration:dur,ease:'none'},0);
  if(document.querySelector($('.glow')))tl.fromTo($('.glow'),{scale:0.9,opacity:0.7},{scale:1.08,opacity:1,duration:dur/4,ease:'sine.inOut',yoyo:true,repeat:3},0);}
"""


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- scene bodies
# each returns (html, js) ; L(t) converts global seconds -> scene-local
def scene_bodies():
    B = {}

    # S01 ── hook
    B["s01"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:760px;top:420px;">SPOUSE</div>
<div class="glow" style="left:980px;top:120px;"></div>
<div class="kicker">AA CANADA · 캐나다 유학 &amp; 이민</div>
<div style="position:absolute;left:120px;top:228px;font-size:150px;font-weight:900;letter-spacing:-0.045em;line-height:1.05;" class="t1">캐나다</div>
<div style="position:absolute;left:120px;top:390px;font-size:150px;font-weight:900;letter-spacing:-0.045em;line-height:1.05;" class="t2">배우자 <span style="color:var(--red)">워크퍼밋</span></div>
<div style="position:absolute;left:126px;top:580px;font-size:42px;font-weight:500;color:var(--ink-soft);" class="t3">누가 가능하고, 누가 안 되는지 — 한 번에 정리</div>
<div class="rule" style="position:absolute;left:126px;top:560px;width:900px;height:5px;background:var(--ink);transform-origin:left center;"></div>
<div class="card qcard" style="left:1060px;top:640px;width:740px;padding:36px 44px 40px;">
  <div class="mono" style="font-size:22px;font-weight:700;color:var(--red);letter-spacing:.12em;">상담에서 가장 많이 듣는 질문</div>
  <div style="font-size:52px;font-weight:800;line-height:1.3;margin-top:14px;letter-spacing:-0.02em;">“배우자도 캐나다에서<br/>일할 수 있나요?”</div>
</div>
<div class="qtail" style="position:absolute;left:1690px;top:850px;width:0;height:0;border-left:44px solid transparent;border-top:50px solid var(--ink);"></div>
""",
        f"""
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.t1',0.5,{{y:60,e:'expo.out',d:0.9}});
rise('.t2',0.75,{{y:60,e:'expo.out',d:0.9}});
bar('.rule',1.3,{{d:0.9}});
rise('.t3',1.6,{{y:20}});
popin('.qcard',{L(us(2))-0.25},{{s:0.7}});
rise('.qtail',{L(us(2))+0.15},{{y:-20,d:0.3}});
""")

    # S02 ── income → burden
    B["s02"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:900px;top:470px;">INCOME</div>
<div class="kicker">왜 다들 궁금해할까?</div>
<div class="h1">배우자가 일할 수 있으면<br/>가족 <em>생활비 부담</em>이 확 줄어듭니다</div>
<div class="card" style="left:120px;top:480px;width:1680px;height:360px;"></div>
<div class="tag" style="position:absolute;left:180px;top:520px;">한 달 생활비를 누가 채우나 (개념도)</div>
<div style="position:absolute;left:180px;top:590px;width:1560px;">
  <div class="row" style="gap:28px;">
    <div style="width:300px;font-size:34px;font-weight:700;">주 신청자 수입만</div>
    <div style="flex:1;height:64px;background:var(--paper-2);border-radius:12px;position:relative;overflow:hidden;">
      <div class="b1" style="position:absolute;left:0;top:0;bottom:0;width:48%;background:var(--ink);transform-origin:left center;"></div>
      <div class="b1g" style="position:absolute;left:48%;top:0;bottom:0;right:0;background:repeating-linear-gradient(135deg,rgba(200,40,30,.35) 0 14px,rgba(200,40,30,.12) 14px 28px);transform-origin:left center;"></div>
    </div>
    <div class="b1t" style="width:200px;font-size:34px;font-weight:800;color:var(--red);">부족분 ↑</div>
  </div>
  <div class="row r2" style="gap:28px;margin-top:44px;">
    <div style="width:300px;font-size:34px;font-weight:700;">+ 배우자 수입</div>
    <div style="flex:1;height:64px;background:var(--paper-2);border-radius:12px;position:relative;overflow:hidden;">
      <div class="b2" style="position:absolute;left:0;top:0;bottom:0;width:48%;background:var(--ink);transform-origin:left center;"></div>
      <div class="b3" style="position:absolute;left:48%;top:0;bottom:0;width:44%;background:var(--green);transform-origin:left center;"></div>
    </div>
    <div class="b3t" style="width:200px;font-size:34px;font-weight:800;color:var(--green);">부담 ↓</div>
  </div>
</div>
""", f"""
ambient({L(ends[1])});
rise('.kicker',0.25,{{y:0,x:-30}});
rise('.h1',0.45,{{y:50,e:'expo.out',d:0.9}});
rise('.card',1.2,{{y:30}});
rise('.tag',1.4,{{y:10}});
bar('.b1',1.6);
bar('.b1g',2.2,{{d:0.6}});
rise('.b1t',2.6,{{y:10}});
rise('.r2',{L(us(3,0.45))},{{y:20}});
bar('.b2',{L(us(3,0.45))+0.2});
bar('.b3',{L(us(3,0.55))},{{d:1.0,e:'power2.out'}});
popin('.b3t',{L(us(3,0.7))});
""")

    # S03 ── rule changed + agenda
    B["s03"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:700px;top:440px;">2025</div>
<div class="kicker">그런데</div>
<div class="h1 hA">규정이 크게 바뀌었습니다</div>
<div class="card cA" style="left:120px;top:340px;width:620px;height:300px;display:flex;flex-direction:column;justify-content:center;align-items:center;">
  <div class="mono" style="font-size:30px;font-weight:700;color:var(--ink-soft);">규정 대폭 변경</div>
  <div class="mono" style="font-size:110px;font-weight:700;color:var(--red);letter-spacing:-0.03em;">2025.01</div>
</div>
<div class="cB" style="position:absolute;left:800px;top:350px;width:1000px;">
  <div class="row cb1"><div class="ic ink">+</div><div class="body">이후에도 세부 지침이 조금씩 업데이트</div></div>
  <div class="row cb2" style="margin-top:36px;"><div class="ic no">!</div><div class="body">예전 정보를 보고 오신 분들 사이에 <b style="color:var(--red)">혼선</b></div></div>
</div>
<div class="agenda" style="position:absolute;left:120px;top:700px;width:1680px;">
  <div class="tag ag0" style="margin-bottom:20px;">오늘 영상에서 정리할 내용</div>
  <div class="row" style="gap:18px;flex-wrap:nowrap;">
    {''.join(f'<div class="pill ag" style="font-size:30px;padding:12px 22px;"><span class="mono" style="color:var(--red);margin-right:10px;font-size:24px;">0{i+1}</span>{c}</div>' for i, c in enumerate(["기본 원리", "규정 변화", "취업비자", "학생비자", "자주 하는 오해", "준비 방법"]))}
  </div>
</div>
""", f"""
ambient({L(ends[2])});
rise('.kicker',0.25,{{y:0,x:-30}});
rise('.hA',0.4,{{y:50,e:'expo.out',d:0.9}});
popin('.cA',{L(us(4,0.05))},{{s:0.8}});
slide('.cb1',{L(us(4,0.35))},60);
slide('.cb2',{L(us(4,0.62))},60);
rise('.ag0',{L(us(5))-0.2},{{y:10}});
rise('.ag',{L(us(5))},{{y:30,st:0.09,e:'back.out(1.6)'}});
""")

    # S04 ── what is an OWP
    feats = [("특정 회사에 묶이지 않음", 7, 0.0), ("LMIA(노동시장영향평가) 필요 없음", 7, 0.25),
             ("캐나다 어느 지역 · 어느 직장이든", 7, 0.6), ("풀타임 근무도 가능", 8, 0.0)]
    B["s04"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:640px;top:470px;">OPEN</div>
<div class="glow" style="left:1100px;top:120px;"></div>
<div class="kicker">PART 01 · 기본 개념</div>
<div class="h1">배우자 오픈 워크퍼밋 = <em>열려 있는</em> 취업 허가</div>
<div style="position:absolute;left:120px;top:380px;width:980px;">
  {''.join(f'<div class="row f{i}" style="margin-bottom:34px;"><div class="ic ok">✓</div><div class="body" style="font-weight:700;">{esc(t)}</div></div>' for i, (t, _, _) in enumerate(feats))}
</div>
<div class="card permit" style="left:1180px;top:360px;width:620px;height:430px;padding:40px;">
  <div class="row" style="justify-content:space-between;">
    <div class="mono" style="font-size:22px;font-weight:700;letter-spacing:.14em;color:var(--ink-soft);">WORK PERMIT</div>
    <svg width="64" height="64" viewBox="0 0 64 64"><path fill="#C8281E" d="M32 4l5 11 7-4-2 14 9-6 2 6 9-2-5 12 4 3-15 9 2 8-14-3v12h-4V52l-14 3 2-8-15-9 4-3-5-12 9 2 2-6 9 6-2-14 7 4z"/></svg>
  </div>
  <div style="font-size:64px;font-weight:900;letter-spacing:-0.03em;margin-top:26px;">OPEN</div>
  <div style="font-size:30px;font-weight:600;color:var(--ink-soft);margin-top:6px;">고용주 · 직종 · 지역 제한 없음</div>
  <div style="margin-top:34px;height:4px;background:var(--line);"></div>
  <div class="row" style="margin-top:26px;gap:16px;">
    <div style="width:120px;height:18px;border-radius:9px;background:var(--paper-3);"></div>
    <div style="width:220px;height:18px;border-radius:9px;background:var(--paper-3);"></div>
  </div>
  <div class="row" style="margin-top:16px;gap:16px;">
    <div style="width:260px;height:18px;border-radius:9px;background:var(--paper-3);"></div>
  </div>
</div>
<div class="stamp ok st" style="left:1470px;top:690px;font-size:46px;">LMIA 면제</div>
""", f"""
ambient({L(ends[3])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.h1',1.05,{{y:50,e:'expo.out',d:0.9}});
tl.fromTo($('.permit'),{{opacity:0,y:80,rotation:6}},{{opacity:1,y:0,rotation:-2,duration:1.0,ease:'expo.out'}},1.5);
tl.fromTo($('.permit'),{{y:0}},{{y:-14,duration:3,ease:'sine.inOut',yoyo:true,repeat:5,immediateRender:false}},2.5);
""" + "".join(f"slide('.f{i}',{L(us(u, f))},-60);\n" for i, (_, u, f) in enumerate(feats)) + f"stamp('.st',{L(us(7,0.3))},-8);\n")

    # S05 ── core principle diagram
    B["s05"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:520px;top:480px;">PRINCIPLE</div>
<div class="kicker">가장 중요한 원리</div>
<div class="h1 hh">배우자 본인이 아니라 <em>주 신청자</em>의 자격을 봅니다</div>
<div class="nodeA card" style="left:150px;top:400px;width:560px;height:330px;padding:40px;">
  <div class="tag">주 신청자 · PRINCIPAL</div>
  <div style="font-size:54px;font-weight:900;margin-top:14px;letter-spacing:-0.02em;">캐나다에 와 있는<br/>배우자</div>
  <div class="muted" style="font-size:30px;margin-top:14px;font-weight:500;">학생비자 또는 취업비자</div>
</div>
<div class="nodeB card" style="left:1240px;top:400px;width:530px;height:330px;padding:40px;border-color:var(--green);">
  <div class="tag" style="color:var(--green);">배우자 · SPOUSE</div>
  <div style="font-size:54px;font-weight:900;margin-top:14px;letter-spacing:-0.02em;">오픈<br/>워크퍼밋</div>
  <div class="muted" style="font-size:30px;margin-top:14px;font-weight:500;">자격은 주 신청자에게서 나옴</div>
</div>
<svg style="position:absolute;left:720px;top:470px;" width="510" height="200" viewBox="0 0 510 200">
  <path class="draw arr" pathLength="1" stroke-dasharray="1" d="M10 100 C 160 20, 340 20, 480 100" stroke="#C8281E" stroke-width="10"/>
  <path class="draw arrh" pathLength="1" stroke-dasharray="1" d="M440 70 L 486 104 L 436 128" stroke="#C8281E" stroke-width="10"/>
</svg>
<div class="lbl" style="position:absolute;left:820px;top:430px;width:310px;text-align:center;font-size:32px;font-weight:800;color:var(--red);">문을 열어 줌</div>
<div class="chips" style="position:absolute;left:150px;top:770px;" >
  <div class="row" style="gap:20px;"><div class="pill c1">숙련된 인력</div><div class="muted" style="font-size:34px;font-weight:700;">또는</div><div class="pill c2">고급 학위 과정</div></div>
</div>
""", f"""
ambient({L(ends[4])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.hh',{L(us(10))},{{y:50,e:'expo.out',d:0.9}});
slide('.nodeA',{L(us(10,0.25))},-80);
slide('.nodeB',{L(us(10,0.6))},80);
popin('.c1',{L(us(11,0.15))});
popin('.c2',{L(us(11,0.3))});
draw('.arr',{L(us(11,0.55))},0.9);
draw('.arrh',{L(us(11,0.55))+0.8},0.3);
rise('.lbl',{L(us(11,0.6))+0.6},{{y:20}});
tl.fromTo($('.nodeB'),{{boxShadow:'10px 10px 0 #DED3C0'}},{{boxShadow:'10px 10px 0 #1F7A4D',duration:0.4}},{L(us(11,0.75))});
""")

    # S06 ── before / after 2025-01-21
    B["s06"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:700px;top:470px;">BEFORE</div>
<div class="kicker">PART 02 · 규정 변화</div>
<div class="h1">대상이 <em>크게 줄었습니다</em></div>
<div style="position:absolute;left:120px;top:470px;width:1680px;height:8px;background:var(--ink);transform-origin:left center;" class="axis"></div>
<div class="before" style="position:absolute;left:140px;top:340px;width:700px;">
  <div class="tag">예전</div>
  <div style="font-size:40px;font-weight:700;margin-top:8px;">학생이든 취업비자든</div>
</div>
<div class="before2 card" style="left:140px;top:520px;width:700px;padding:32px 36px;">
  <div class="body" style="font-weight:700;">대부분의 배우자가<br/>오픈 워크퍼밋 가능</div>
</div>
<div class="mark" style="position:absolute;left:960px;top:446px;width:56px;height:56px;border-radius:50%;background:var(--red);border:8px solid var(--paper);"></div>
<div class="date mono" style="position:absolute;left:880px;top:360px;font-size:44px;font-weight:700;color:var(--red);">2025.01.21</div>
<div class="after card" style="left:1100px;top:520px;width:700px;padding:32px 36px;border-color:var(--red);">
  <div class="body" style="font-weight:700;">일부 경우에만 가능<br/><span class="muted" style="font-weight:500;font-size:34px;">→ 다음 파트에서 자세히</span></div>
</div>
<div class="stamp no st" style="left:1440px;top:340px;">대상 축소</div>
<div class="warnrow row" style="position:absolute;left:140px;top:770px;gap:22px;">
  <div class="ic warn">!</div>
  <div class="body" style="font-weight:600;">예전 블로그·유튜브 보고 <s style="color:var(--red)">“나도 되겠지”</s> → 뒤늦게 안 된다는 걸 알게 되는 경우</div>
</div>
""", f"""
ambient({L(ends[5])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.h1',{L(us(13))-0.3},{{y:50,e:'expo.out',d:0.9}});
bar('.axis',1.1,{{d:1.2,e:'power2.inOut'}});
rise('.before',1.4,{{y:20}});
rise('.before2',{L(us(12,0.4))},{{y:30}});
popin('.mark',{L(us(13))},{{s:0.2}});
rise('.date',{L(us(13))+0.15},{{y:20}});
slide('.after',{L(us(13,0.5))},80);
stamp('.st',{L(us(13,0.7))},-7);
rise('.warnrow',{L(us(14,0.1))},{{y:30}});
""")

    # S07 ── evaluation date
    B["s07"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:640px;top:470px;">DATE</div>
<div class="kicker">한 가지 더 중요한 점</div>
<div class="h1">심사 기준은 <em>IRCC가 신청서를 받은 날</em>의 규정</div>
{''.join(f'''<div class="card cal c{i}" style="left:{140 + i * 570}px;top:420px;width:500px;height:380px;{'border-color:var(--red);' if i == 2 else ''}">
  <div style="height:90px;background:{'var(--red)' if i == 2 else 'var(--ink)'};border-radius:18px 18px 0 0;display:flex;align-items:center;justify-content:center;color:#FBF8F2;font-size:30px;font-weight:700;" class="mono">{lab}</div>
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:280px;">
    <div style="font-size:60px;font-weight:900;">{name}</div>
  </div>
</div>''' for i, (lab, name) in enumerate([("ENROL", "입학한 날"), ("HIRED", "취업한 날"), ("RECEIVED", "IRCC 접수일")]))}
<div class="stamp no x0" style="left:290px;top:730px;font-size:44px;">기준 아님</div>
<div class="stamp no x1" style="left:860px;top:730px;font-size:44px;">기준 아님</div>
<div class="stamp ok x2" style="left:1470px;top:730px;font-size:44px;">이 날 기준</div>
""", f"""
ambient({L(ends[6])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',{L(us(16,0.3))},{{y:50,e:'expo.out',d:0.9}});
rise('.c0',{L(us(16,0.05))},{{y:60}});
rise('.c1',{L(us(16,0.15))},{{y:60}});
stamp('.x0',{L(us(16,0.25))},-8);
stamp('.x1',{L(us(16,0.32))},6);
rise('.c2',{L(us(16,0.45))},{{y:60,e:'back.out(1.5)'}});
stamp('.x2',{L(us(16,0.62))},-6);
""")

    # S08 ── TEER staircase intro
    teer = [("0", "관리직"), ("1", "학사 이상 전문직"), ("2", "컬리지 · 기술직"), ("3", "컬리지 · 기술직"),
            ("4", "고졸 수준"), ("5", "단순 노무")]
    B["s08"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:760px;top:470px;">TEER</div>
<div class="kicker">PART 03 · 주 신청자가 취업비자</div>
<div class="h1 hh">직종의 숙련도 = <em>NOC TEER</em> 레벨</div>
<div class="sub muted" style="position:absolute;left:124px;top:310px;font-size:34px;font-weight:500;">NOC: 캐나다 직업 분류 · TEER 숫자가 낮을수록 숙련도 높음</div>
{''.join(f'''<div class="step s{i}" style="position:absolute;left:{140 + i * 275}px;top:{400 + i * 52}px;width:255px;height:{440 - i * 52}px;background:{'var(--ink)' if i < 2 else ('#3A4A66' if i < 4 else '#8A93A3')};border-radius:16px 16px 0 0;transform-origin:center bottom;padding:26px 22px;color:#FBF8F2;">
  <div class="mono" style="font-size:30px;font-weight:700;">TEER</div>
  <div style="font-size:{92 - i * 6}px;font-weight:900;line-height:1;">{n}</div>
  <div style="font-size:26px;font-weight:600;margin-top:12px;line-height:1.3;">{esc(d) if i in (0, 1, 2, 4) else ''}</div>
</div>''' for i, (n, d) in enumerate(teer))}
""", f"""
ambient({L(ends[7])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.hh',{L(us(18))},{{y:50,e:'expo.out',d:0.9}});
rise('.sub',{L(us(18,0.35))},{{y:20}});
barY('.step',{L(us(18,0.4))},{{st:0.12,e:'back.out(1.3)'}});
""")

    # S09 ── TEER verdicts
    B["s09"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:820px;top:480px;">TEER</div>
<div class="kicker">취업비자 · 직종 레벨별 판정</div>
<div class="h1" style="font-size:72px;">주 신청자의 직종이 어디에 해당하나요?</div>
<div class="card r0" style="left:120px;top:330px;width:1680px;height:150px;"></div>
<div class="card r1" style="left:120px;top:510px;width:1680px;height:200px;"></div>
<div class="card r2" style="left:120px;top:740px;width:1680px;height:120px;"></div>
<div class="t0" style="position:absolute;left:170px;top:362px;"><div class="mono" style="font-size:52px;font-weight:700;">TEER 0·1</div></div>
<div class="d0 body" style="position:absolute;left:520px;top:340px;width:820px;font-weight:600;line-height:1.35;">관리직 · 학사 이상 전문직<br/><span class="muted" style="font-size:34px;">직종 제한 없이 배우자 신청 가능</span></div>
<div class="stamp ok v0" style="left:1440px;top:358px;">가능</div>
<div class="t1" style="position:absolute;left:170px;top:540px;"><div class="mono" style="font-size:52px;font-weight:700;">TEER 2·3</div></div>
<div class="d1 body" style="position:absolute;left:520px;top:530px;width:860px;font-weight:600;line-height:1.35;">컬리지 · 기술 수준 직종<br/><span class="muted" style="font-size:34px;">IRCC가 지정한 직종 목록에 있을 때만</span></div>
<div class="row chips" style="position:absolute;left:520px;top:640px;gap:16px;">
  <div class="pill k0" style="font-size:28px;padding:8px 20px;">보건의료</div><div class="pill k1" style="font-size:28px;padding:8px 20px;">건설</div><div class="pill k2" style="font-size:28px;padding:8px 20px;">자연·응용과학</div><div class="muted k3" style="font-size:28px;font-weight:600;">등 인력 부족·우선순위 분야</div>
</div>
<div class="stamp warn v1" style="left:1400px;top:560px;font-size:44px;">지정 목록만</div>
<div class="t2" style="position:absolute;left:170px;top:768px;"><div class="mono" style="font-size:52px;font-weight:700;">TEER 4·5</div></div>
<div class="d2 body" style="position:absolute;left:520px;top:772px;width:820px;font-weight:600;">저숙련 직종 <span class="muted" style="font-size:34px;">— 원칙적으로 불가</span></div>
<div class="stamp no v2" style="left:1460px;top:752px;">불가</div>
""", f"""
ambient({L(ends[8])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',0.4,{{y:40,e:'expo.out',d:0.8}});
rise('.r0',{L(us(19))-0.2},{{y:30}});
slide('.t0',{L(us(19))},-40);
rise('.d0',{L(us(19,0.3))},{{y:20}});
stamp('.v0',{L(us(20,0.3))},-7);
rise('.r1',{L(us(21))-0.2},{{y:30}});
slide('.t1',{L(us(21))},-40);
rise('.d1',{L(us(21,0.3))},{{y:20}});
stamp('.v1',{L(us(22,0.3))},-5);
popin('.k0',{L(us(23,0.05))});
popin('.k1',{L(us(23,0.15))});
popin('.k2',{L(us(23,0.25))});
rise('.k3',{L(us(23,0.5))},{{y:10}});
rise('.r2',{L(us(24))-0.2},{{y:30}});
slide('.t2',{L(us(24))},-40);
rise('.d2',{L(us(24,0.3))},{{y:20}});
stamp('.v2',{L(us(24,0.6))},-8);
""")

    # S10 ── 16-month remaining rule
    B["s10"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:900px;top:470px;">16</div>
<div class="kicker">많은 분들이 놓치는 조건</div>
<div class="h1">주 신청자 워크퍼밋이 <em>16개월 이상</em> 남아 있어야</div>
<div class="tag" style="position:absolute;left:140px;top:350px;">신청서 접수일 기준 · 남은 허가 기간</div>
<div class="axisline" style="position:absolute;left:400px;top:410px;width:1360px;height:4px;background:var(--line);"></div>
<div class="thr" style="position:absolute;left:1124px;top:390px;width:6px;height:420px;background:var(--red);transform-origin:center top;"></div>
<div class="thrl mono" style="position:absolute;left:1046px;top:330px;font-size:40px;font-weight:700;color:var(--red);">16개월</div>
<div class="la" style="position:absolute;left:140px;top:470px;width:240px;font-size:34px;font-weight:700;line-height:1.25;">예시 A<br/><span class="muted" style="font-size:28px;">20개월 남음</span></div>
<div class="ba" style="position:absolute;left:400px;top:480px;width:905px;height:90px;border-radius:12px;background:var(--green);transform-origin:left center;"></div>
<div class="stamp ok sa" style="left:1440px;top:470px;font-size:46px;">신청 가능</div>
<div class="lb" style="position:absolute;left:140px;top:640px;width:240px;font-size:34px;font-weight:700;line-height:1.25;">예시 B<br/><span class="muted" style="font-size:28px;">TEER 0·1이라도<br/>12개월 남음</span></div>
<div class="bb" style="position:absolute;left:400px;top:650px;width:543px;height:90px;border-radius:12px;background:var(--red);transform-origin:left center;"></div>
<div class="stamp no sb" style="left:1440px;top:640px;font-size:46px;">신청 불가</div>
<div class="tip card" style="left:400px;top:830px;width:1400px;height:0;padding:0;border:none;box-shadow:none;background:transparent;">
  <div class="row" style="gap:20px;"><div class="ic ink" style="width:56px;height:56px;font-size:30px;">→</div>
  <div style="font-size:38px;font-weight:700;">워크퍼밋 <span style="color:var(--red)">연장 시점</span>과 배우자 <span style="color:var(--red)">신청 시점</span>을 함께 설계</div></div>
</div>
""", f"""
ambient({L(ends[9])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',{L(us(26))-0.1},{{y:50,e:'expo.out',d:0.9}});
rise('.tag',{L(us(26,0.4))},{{y:10}});
bar('.axisline',{L(us(26,0.4))},{{d:0.8}});
barY('.thr',{L(us(26,0.65))},{{d:0.7}});
rise('.thrl',{L(us(26,0.7))},{{y:-20}});
rise('.la',{L(us(26,0.85))},{{y:20}});
bar('.ba',{L(us(26,0.9))},{{d:1.1,e:'power2.out'}});
stamp('.sa',{L(us(26,0.9))+1.0},-6);
rise('.lb',{L(us(27))},{{y:20}});
bar('.bb',{L(us(27,0.2))},{{d:1.0,e:'power2.out'}});
stamp('.sb',{L(us(27,0.6))},-6);
rise('.tip',{L(us(28))},{{y:30}});
""")

    # S11 ── student: eligible degrees
    B["s11"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:760px;top:480px;">DEGREE</div>
<div class="kicker">PART 04 · 주 신청자가 학생비자</div>
<div class="h1 hh">직종이 아니라 <em>학위 과정의 수준</em>을 봅니다</div>
<div class="tag lab" style="position:absolute;left:124px;top:330px;color:var(--green);">가능한 경우 · 3가지</div>
{''.join(f'''<div class="card d{i}" style="left:{120 + i * 570}px;top:380px;width:520px;height:250px;padding:34px 36px;border-color:var(--green);">
  <div class="row" style="gap:16px;"><div class="ic ok" style="width:54px;height:54px;font-size:30px;">✓</div><div style="font-size:52px;font-weight:900;">{t}</div></div>
  <div class="muted" style="font-size:30px;font-weight:600;margin-top:22px;line-height:1.35;">{s}</div>
</div>''' for i, (t, s) in enumerate([("석사", "16개월 이상 과정"), ("박사", "박사 과정"), ("전문학위", "IRCC가 인정한 과정")]))}
<div class="prof" style="position:absolute;left:1180px;top:660px;width:640px;">
  <div class="tag">전문학위 예시</div>
  <div class="row" style="gap:12px;flex-wrap:wrap;margin-top:14px;">
    {''.join(f'<div class="pill p" style="font-size:28px;padding:8px 20px;">{p}</div>' for p in ["법학", "의학", "약학", "간호", "교육", "공학"])}
  </div>
</div>
<div class="note row" style="position:absolute;left:120px;top:690px;width:1020px;gap:20px;">
  <div class="ic warn">!</div><div class="body" style="font-weight:600;">정확한 목록은 <b>IRCC 공식 사이트</b>에서 꼭 확인하세요</div>
</div>
""", f"""
ambient({L(ends[10])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.hh',{L(us(30))},{{y:50,e:'expo.out',d:0.9}});
rise('.lab',{L(us(31))},{{y:10}});
rise('.d0',{L(us(32,0.0))},{{y:60,e:'back.out(1.4)'}});
rise('.d1',{L(us(32,0.3))},{{y:60,e:'back.out(1.4)'}});
rise('.d2',{L(us(32,0.55))},{{y:60,e:'back.out(1.4)'}});
rise('.prof .tag',{L(us(33))},{{y:10}});
popin('.p',{L(us(33,0.15))},{{st:0.1}});
slide('.note',{L(us(34))},-60);
""")

    # S12 ── student: not eligible
    B["s12"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:700px;top:480px;">NOT</div>
<div class="kicker" style="color:var(--red);">반대로</div>
<div class="h1">이런 과정은 <em>해당이 안 됩니다</em></div>
{''.join(f'''<div class="card n{i}" style="left:{120 + i * 570}px;top:360px;width:520px;height:380px;padding:40px 38px;">
  <div class="tag">{tg}</div>
  <div style="font-size:60px;font-weight:900;margin-top:16px;letter-spacing:-0.02em;">{t}</div>
  <div class="muted" style="font-size:32px;font-weight:600;margin-top:16px;line-height:1.35;">{s}</div>
</div>
<div class="stamp no sn{i}" style="left:{300 + i * 570}px;top:620px;">불가</div>''' for i, (tg, t, s) in enumerate([("COLLEGE", "컬리지", "디플로마 · 어드밴스드 디플로마 모두"), ("BACHELOR", "일반 학사", "학사 과정"), ("LANGUAGE", "어학 과정", "어학원 · 언어 과정")]))}
""", f"""
ambient({L(ends[11])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',0.4,{{y:50,e:'expo.out',d:0.9}});
rise('.n0',{L(us(36))},{{y:60}});
stamp('.sn0',{L(us(36,0.7))},-8);
rise('.n1',{L(us(37))},{{y:60}});
stamp('.sn1',{L(us(37,0.6))},6);
rise('.n2',{L(us(38))},{{y:60}});
stamp('.sn2',{L(us(38,0.6))},-6);
""")

    # S13 ── last semester + children
    B["s13"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:820px;top:480px;">2026</div>
<div class="kicker" style="color:var(--amber);">최근 추가된 조건</div>
<div class="h1"><span class="mono" style="color:var(--amber);font-size:76px;">2026.03</span> 지침 업데이트</div>
<div class="tag" style="position:absolute;left:124px;top:340px;">학생의 학기 진행</div>
{''.join(f'<div class="sem m{i}" style="position:absolute;left:{120 + i * 330}px;top:390px;width:310px;height:110px;border-radius:14px;background:{"var(--amber)" if i == 4 else "var(--paper-3)"};display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800;color:{"#FBF8F2" if i == 4 else "var(--ink)"};">{"마지막 학기" if i == 4 else f"{i+1}학기"}</div>' for i in range(5))}
<div class="warnc card" style="left:1000px;top:540px;width:800px;padding:30px 36px;border-color:var(--amber);">
  <div style="font-size:40px;font-weight:800;line-height:1.35;">마지막 학기에 신청하면<br/><span style="color:var(--amber);">배우자 신청이 거절될 수 있음</span></div>
  <div class="muted" style="font-size:30px;font-weight:600;margin-top:12px;">졸업 앞두고는 신청 타이밍 반드시 확인</div>
</div>
<div class="arrowdn" style="position:absolute;left:1440px;top:500px;width:0;height:0;border-left:22px solid transparent;border-right:22px solid transparent;border-top:34px solid var(--amber);"></div>
<div class="kids card" style="left:120px;top:560px;width:820px;padding:30px 36px;">
  <div class="tag">함께 기억하세요</div>
  <div style="font-size:40px;font-weight:800;margin-top:12px;line-height:1.35;">자녀는 이 카테고리로<br/>오픈 워크퍼밋을 받을 수 <span style="color:var(--red)">없습니다</span></div>
</div>
""", f"""
ambient({L(ends[12])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',{L(us(40))-0.2},{{y:50,e:'expo.out',d:0.9}});
rise('.tag',{L(us(40,0.2))},{{y:10}});
rise('.sem',{L(us(40,0.25))},{{y:30,st:0.1}});
tl.fromTo($('.m4'),{{scale:1}},{{scale:1.08,duration:0.35,yoyo:true,repeat:1,ease:'power2.out',immediateRender:false}},{L(us(40,0.45))});
rise('.arrowdn',{L(us(40,0.6))},{{y:-20}});
rise('.warnc',{L(us(40,0.62))},{{y:40}});
slide('.kids',{L(us(42))},-80);
""")

    # S14 ── myths 1 & 2
    B["s14"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:760px;top:480px;">MYTH</div>
<div class="kicker">PART 05 · 자주 하는 오해</div>
<div class="h1 hh">상담에서 자주 나오는 <em>오해 3가지</em></div>
{''.join(f'''<div class="card m{i}" style="left:120px;top:{330 + i * 270}px;width:1680px;height:240px;"></div>
<div class="mq{i}" style="position:absolute;left:170px;top:{360 + i * 270}px;">
  <div class="mono" style="font-size:26px;font-weight:700;color:var(--red);">오해 0{i+1}</div>
  <div style="font-size:46px;font-weight:800;margin-top:8px;">“{q}”</div>
</div>
<div class="ma{i} row" style="position:absolute;left:170px;top:{480 + i * 270}px;gap:18px;"><div class="ic ok" style="width:52px;height:52px;font-size:28px;">→</div><div style="font-size:38px;font-weight:700;">{a}</div></div>
<div class="stamp no mx{i}" style="left:1500px;top:{380 + i * 270}px;font-size:48px;">아닙니다</div>''' for i, (q, a) in enumerate([("취업비자니까 무조건 되겠지", "직종 레벨(TEER) + 16개월 조건, 둘 다 봅니다"), ("학사 공부하면 되는 걸로 알았는데요", "일반 학사 ✗ · 인정된 전문학위만 해당")]))}
""", f"""
ambient({L(ends[13])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.hh',{L(us(43))},{{y:50,e:'expo.out',d:0.9}});
rise('.m0',{L(us(44))-0.2},{{y:40}});
slide('.mq0',{L(us(44))},-40);
stamp('.mx0',{L(us(44,0.75))},-7);
rise('.ma0',{L(us(45))},{{y:20}});
rise('.m1',{L(us(46))-0.2},{{y:40}});
slide('.mq1',{L(us(46))},-40);
stamp('.mx1',{L(us(46,0.45))},6);
rise('.ma1',{L(us(46,0.55))},{{y:20}});
""")

    # S15 ── myth 3 flow
    B["s15"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:760px;top:480px;">PGWP</div>
<div class="kicker">오해 03</div>
<div class="h1" style="font-size:66px;">“컬리지 졸업하면 그때 배우자 워크퍼밋 받으면 되죠?”</div>
{''.join(f'''<div class="card f{i}" style="left:{120 + i * 580}px;top:380px;width:520px;height:250px;padding:34px 36px;{bc}">
  <div class="tag">{tg}</div>
  <div style="font-size:50px;font-weight:900;margin-top:12px;">{t}</div>
  <div class="muted" style="font-size:30px;font-weight:600;margin-top:10px;">{s}</div>
</div>''' for i, (tg, t, s, bc) in enumerate([("지금", "학생비자", "컬리지 재학", ""), ("졸업 후", "PGWP", "졸업 후 취업비자", ""), ("판단 기준", "직종 TEER", "취업비자 기준으로 다시 판단", "border-color:var(--red);")]))}
<svg style="position:absolute;left:640px;top:470px;" width="1200" height="80" viewBox="0 0 1200 80">
  <path class="draw a0" pathLength="1" stroke-dasharray="1" d="M4 40 H 56 M 36 20 L 58 40 L 36 60" stroke="#18233A" stroke-width="8"/>
  <path class="draw a1" pathLength="1" stroke-dasharray="1" d="M584 40 H 636 M 616 20 L 638 40 L 616 60" stroke="#18233A" stroke-width="8"/>
</svg>
<div class="stamp no big" style="left:540px;top:700px;font-size:60px;">학생일 때와 기준이 완전히 달라짐</div>
""", f"""
ambient({L(ends[14])});
rise('.kicker',0.3,{{y:0,x:-30}});
rise('.h1',0.45,{{y:40,e:'expo.out',d:0.9}});
rise('.f0',{L(us(47,0.35))},{{y:50}});
draw('.a0',{L(us(47,0.45))},0.5);
rise('.f1',{L(us(47,0.5))},{{y:50}});
draw('.a1',{L(us(47,0.65))},0.5);
rise('.f2',{L(us(47,0.7))},{{y:50,e:'back.out(1.5)'}});
stamp('.big',{L(us(48))},-3);
""")

    # S16 ── budget planning
    B["s16"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:640px;top:480px;">BUDGET</div>
<div class="kicker">PART 06 · 준비 방법</div>
<div class="h1 hh">가족 예산, <em>이렇게</em> 짜세요</div>
<div class="rule0 card" style="left:120px;top:330px;width:1680px;padding:30px 40px;border-color:var(--red);">
  <div class="row" style="gap:22px;"><div class="ic no">✕</div>
  <div style="font-size:42px;font-weight:800;">배우자 워크퍼밋을 <span style="position:relative;display:inline-block;">‘당연히’<span class="strk" style="position:absolute;left:-4px;right:-4px;top:52%;height:6px;background:var(--red);transform-origin:left center;"></span></span> 받는다고 가정하고 생활비 계산하지 않기</div></div>
</div>
<div class="s1 card" style="left:120px;top:500px;width:520px;height:220px;padding:30px 34px;">
  <div class="tag">STEP 1</div><div style="font-size:38px;font-weight:800;margin-top:10px;line-height:1.3;">주 신청자의 과정·직종이<br/>해당되는지 확인</div>
</div>
<div class="s2 card" style="left:700px;top:500px;width:520px;height:220px;padding:30px 34px;">
  <div class="tag">해당 안 되면</div><div style="font-size:38px;font-weight:800;margin-top:10px;line-height:1.3;">배우자 수입 <span style="color:var(--red)">0원</span>을<br/>기준으로 예산</div>
</div>
<div class="s3 card" style="left:1280px;top:500px;width:520px;height:220px;padding:30px 34px;border-color:var(--green);">
  <div class="tag" style="color:var(--green);">수입이 생기면</div><div style="font-size:38px;font-weight:800;margin-top:10px;line-height:1.3;">그건 <span style="color:var(--green)">여유 자금</span></div>
</div>
<div class="chk" style="position:absolute;left:120px;top:770px;width:1680px;">
  <div class="row" style="gap:26px;">
    <div class="tag" style="width:260px;">해당돼도 꼭 확인</div>
    {''.join(f'<div class="pill c{i}" style="font-size:32px;"><span style="color:var(--green);margin-right:12px;">✓</span>{t}</div>' for i, t in enumerate(["신청 시점", "남은 허가 기간", "마지막 학기 여부"]))}
  </div>
</div>
""", f"""
ambient({L(ends[15])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.hh',{L(us(49,0.2))},{{y:50,e:'expo.out',d:0.9}});
rise('.rule0',{L(us(50,0.15))},{{y:30}});
strike('.strk',{L(us(50,0.5))});
rise('.s1',{L(us(51))},{{y:40}});
rise('.s2',{L(us(51,0.55))},{{y:40}});
rise('.s3',{L(us(52))},{{y:40,e:'back.out(1.5)'}});
rise('.chk .tag',{L(us(53))},{{y:10}});
popin('.c0',{L(us(53,0.35))});
popin('.c1',{L(us(53,0.5))});
popin('.c2',{L(us(53,0.7))});
""")

    # S17 ── summary
    B["s17"] = lambda L: (f"""
<div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="left:640px;top:480px;">SUMMARY</div>
<div class="kicker">정리하면</div>
<div class="h1 hh">배우자 워크퍼밋은 <em>주 신청자</em>를 보고 결정</div>
<div class="cL card" style="left:120px;top:340px;width:810px;height:360px;padding:40px 44px;">
  <div class="tag">주 신청자가</div>
  <div style="font-size:66px;font-weight:900;margin-top:6px;">취업비자</div>
  <div style="margin-top:26px;" class="row"><div class="ic ink" style="width:52px;height:52px;font-size:28px;">1</div><div style="font-size:38px;font-weight:700;">직종 레벨 (TEER)</div></div>
  <div style="margin-top:18px;" class="row"><div class="ic ink" style="width:52px;height:52px;font-size:28px;">2</div><div style="font-size:38px;font-weight:700;">남은 기간 (16개월 이상)</div></div>
</div>
<div class="cR card" style="left:990px;top:340px;width:810px;height:360px;padding:40px 44px;">
  <div class="tag">주 신청자가</div>
  <div style="font-size:66px;font-weight:900;margin-top:6px;">학생비자</div>
  <div style="margin-top:26px;" class="row"><div class="ic ink" style="width:52px;height:52px;font-size:28px;">1</div><div style="font-size:38px;font-weight:700;">학위 수준</div></div>
  <div style="margin-top:18px;" class="muted"><div style="font-size:32px;font-weight:600;padding-left:76px;">석사(16개월+) · 박사 · 인정 전문학위</div></div>
</div>
<div class="ban row" style="position:absolute;left:120px;top:750px;width:1680px;height:110px;background:var(--ink);border-radius:18px;padding:0 44px;gap:22px;color:#FBF8F2;">
  <div class="ic" style="background:var(--red);">!</div>
  <div style="font-size:40px;font-weight:700;">규정이 자주 바뀝니다 — 내 상황에 맞는지 <span style="color:#F2B8B2;">신청 전에 꼭 확인</span></div>
</div>
""", f"""
ambient({L(ends[16])});
rise('.kicker',0.9,{{y:0,x:-30}});
rise('.hh',1.0,{{y:50,e:'expo.out',d:0.9}});
slide('.cL',{L(us(54,0.2))},-80);
slide('.cR',{L(us(54,0.6))},80);
rise('.ban',{L(us(55))},{{y:40}});
""")

    # S18 ── CTA / outro
    B["s18"] = lambda L: (f"""
<div class="glow" style="left:510px;top:60px;width:900px;height:900px;"></div>
<div class="logo" style="position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center;align-items:center;gap:30px;">
  <svg width="120" height="120" viewBox="0 0 64 64"><path fill="#C8281E" d="M32 4l5 11 7-4-2 14 9-6 2 6 9-2-5 12 4 3-15 9 2 8-14-3v12h-4V52l-14 3 2-8-15-9 4-3-5-12 9 2 2-6 9 6-2-14 7 4z"/></svg>
  <div style="font-size:130px;font-weight:900;letter-spacing:-0.03em;">AA Canada</div>
</div>
<div class="line1" style="position:absolute;left:0;right:0;top:440px;text-align:center;font-size:50px;font-weight:700;">유학 단계부터 영주권까지, <span style="color:var(--red);">가족 맞춤 경로 설계</span></div>
<div class="line2 row" style="position:absolute;left:0;right:0;top:560px;justify-content:center;gap:24px;">
  <div class="pill" style="font-size:36px;">💬 댓글로 질문</div><div class="pill" style="font-size:36px;background:var(--ink);color:#FBF8F2;">1:1 상담 문의</div>
</div>
<div class="line3" style="position:absolute;left:0;right:0;top:720px;text-align:center;font-size:44px;font-weight:600;color:var(--ink-soft);">시청해 주셔서 감사합니다</div>
""", f"""
tl.fromTo($('.glow'),{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:2,ease:'sine.out'}},0.2);
rise('.logo',0.6,{{y:40,s:0.92,e:'expo.out',d:1.0}});
rise('.line1',{L(us(56,0.2))},{{y:30}});
rise('.line2',{L(us(57))},{{y:30,e:'back.out(1.5)'}});
rise('.line3',{L(us(58))},{{y:20}});
tl.to($('.sc'),{{opacity:0,duration:1.2,ease:'power1.in'}},{TOTAL - starts[-1] - 1.4:.2f});
""")
    return B


def write_scene(k, sid, body):
    start, end = starts[k], ends[k]
    has_out = k < len(SCENES) - 1
    dur = round(end - start + (XF if has_out else 0), 2)
    L = lambda t: round(t - start, 2)
    markup, js = body(L)
    doc = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
        [data-composition-id="{sid}"]{{position:absolute;inset:0;}}
      </style>
      <div id="{sid}-root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
        <div class="sc">
{markup}
        </div>
      </div>
      <script>
{JS_HELPERS % {'id': sid}}
{js}
window.__timelines["{sid}"]=tl;
      </script>
    </template>
  </body>
</html>
"""
    open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w").write(doc)
    return dur


# ---------------------------------------------------------------- captions
def n(s):
    return len(re.sub(r'[\s"“”.,?!·()]', "", s))


def caption_chunks():
    out = []
    for u in U:
        t = u["text"]
        # split at sentence-internal commas / quote boundaries into readable chunks (≤ ~30 chars)
        parts = [p.strip() for p in re.split(r'(?<=,)\s+|(?<=[.?!]")\s+|(?<=[.?!])\s+(?=")', t) if p.strip()]
        merged = []
        for p in parts:
            if merged and n(merged[-1]) + n(p) <= 24:
                merged[-1] += " " + p
            else:
                merged.append(p)
        final = []
        for p in merged:
            if n(p) > 34:  # split long chunk at a word boundary near its middle
                w = p.split(" ")
                best, acc = 0, 0
                for i, ww in enumerate(w[:-1]):
                    acc += n(ww)
                    if acc >= n(p) / 2:
                        best = i + 1
                        break
                final += [" ".join(w[:best]), " ".join(w[best:])]
            else:
                final.append(p)
        tot = sum(n(p) for p in final)
        t0, span, acc = u["start"], u["end"] - u["start"], 0
        for p in final:
            a = t0 + span * acc / tot
            acc += n(p)
            b = t0 + span * acc / tot
            out.append((round(a, 2), round(b, 2), p))
    # extend each caption to the next one's start when the gap is short (avoid flicker)
    res = []
    for i, (a, b, p) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else TOTAL
        if nxt - b < 0.9:
            b = nxt
        else:
            b = b + 0.3
        res.append((a, round(b - a, 2), p))
    return res


# ---------------------------------------------------------------- index
def build_index(durs):
    hosts = []
    for k, (sid, a, b, kind, chap) in enumerate(SCENES):
        hosts.append(
            f'      <div id="host-{sid}" class="host" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
            f'data-start="{starts[k]}" data-duration="{durs[k]}" data-track-index="1" data-width="{W}" data-height="{H}"'
            f'{"" if k == 0 else " style=\"opacity:0\""}></div>')
    caps = caption_chunks()
    cap_items = "\n".join(
        f'        <div id="cap{i:03d}" class="clip cap" data-start="{a}" data-duration="{d}" data-track-index="0"><span>{esc(t)}</span></div>'
        for i, (a, d, t) in enumerate(caps))
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(f'''<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
        {FONT_FACE}
        [data-composition-id="captions"]{{position:absolute;inset:0;}}
        .cap{{position:absolute;left:160px;right:160px;bottom:62px;display:flex;justify-content:center;}}
        .cap span{{font-family:"Pretendard",sans-serif;font-size:46px;font-weight:700;line-height:1.3;color:#18233A;text-align:center;letter-spacing:-0.01em;
          background:#FBF8F2;padding:10px 28px;border-radius:14px;border:3px solid #18233A;word-break:keep-all;}}
      </style>
      <div id="captions-root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-duration="{TOTAL}">
{cap_items}
      </div>
      <script>
        const tl = gsap.timeline({{paused:true}});
        window.__timelines["captions"] = tl;
      </script>
    </template>
  </body>
</html>
''')
    cap_html = f'      <div id="host-captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-track-kind="captions" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-width="{W}" data-height="{H}" style="position:absolute;inset:0;z-index:30;"></div>'

    # transitions on main timeline
    tjs = []
    wipes = []
    for k in range(1, len(SCENES)):
        sid, a, b, kind, chap = SCENES[k]
        prev = SCENES[k - 1][0]
        T = starts[k]
        if kind == "push":
            tjs.append(f"tl.set('#host-{sid}',{{opacity:1}},{T});")
            tjs.append(f"tl.fromTo('#host-{prev}',{{x:0}},{{x:-{W},duration:{XF},ease:'power3.inOut',immediateRender:false}},{T});")
            tjs.append(f"tl.fromTo('#host-{sid}',{{x:{W}}},{{x:0,duration:{XF},ease:'power3.inOut'}},{T});")
        elif kind == "chapter":
            num, title = chap
            wipes.append((num, title)); tjs.append(f"chapterWipe({T},'#host-{prev}','#host-{sid}','#wt{len(wipes)-1}');")
        elif kind == "blur":
            tjs.append(f"tl.fromTo('#host-{prev}',{{opacity:1,filter:'blur(0px)'}},{{opacity:0,filter:'blur(14px)',duration:0.8,ease:'sine.inOut'}},{T});")
            tjs.append(f"tl.fromTo('#host-{sid}',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:0.8,ease:'sine.inOut'}},{T});")
    # chapter indicator
    for k, (sid, *_r) in enumerate(SCENES):
        if sid in CHAPTER_OF and (k == 0 or CHAPTER_OF.get(SCENES[k - 1][0]) != CHAPTER_OF[sid]):
            c = CHAPTER_OF[sid]
            tjs.append(f"setChapter({starts[k] + 0.6},{c});")
    first_ch = starts[3] + 0.6
    last_ch = starts[16]
    tjs.append(f"tl.fromTo('#chapters',{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.6,ease:'power3.out'}},{first_ch - 0.4});")
    tjs.append(f"tl.fromTo('#chapters',{{opacity:1}},{{opacity:0,duration:0.5,immediateRender:false}},{last_ch});")
    tjs.append(f"tl.fromTo('#brand',{{opacity:1}},{{opacity:0,duration:0.6}},{starts[-1]});")

    chap_html = "".join(
        f'<div class="ch" id="ch{i}"><span class="mono">0{i+1}</span>{c}</div>' for i, c in enumerate(CHAPTERS))

    doc = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>캐나다 배우자 워크퍼밋 — AA Canada</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      {FONT_FACE}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1920px; height:1080px; overflow:hidden; background:#F4EFE6; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:"Pretendard",sans-serif; color:#18233A; }}
      {SHARED_CSS}
      #paper {{ position:absolute; inset:0; background:#F4EFE6; }}
      #grid {{ position:absolute; inset:-80px; opacity:.55;
        background-image:linear-gradient(rgba(24,35,58,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(24,35,58,.06) 2px,transparent 2px);
        background-size:80px 80px; }}
      #grain {{ position:absolute; inset:0; opacity:.35; mix-blend-mode:multiply;
        background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' seed='7'/><feColorMatrix values='0 0 0 0 .55 0 0 0 0 .48 0 0 0 0 .38 0 0 0 .55 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }}
      #edge {{ position:absolute; left:0; top:0; bottom:0; width:14px; background:#C8281E; }}
      .host {{ position:absolute; inset:0; }}
      #brand {{ position:absolute; right:80px; top:56px; display:flex; align-items:center; gap:14px; font-weight:900; font-size:30px; letter-spacing:-0.01em; z-index:20; }}
      #chapters {{ position:absolute; left:120px; top:60px; display:flex; gap:10px; z-index:20; }}
      #chapters .ch {{ font-size:22px; font-weight:700; padding:8px 16px; border-radius:999px; color:#4A5468; background:rgba(222,211,192,.55); display:flex; gap:8px; align-items:center; }}
      #chapters .ch .mono {{ font-family:"JetBrains Mono",monospace; font-size:18px; }}
      #capbar {{ position:absolute; left:0; right:0; bottom:0; height:190px; z-index:29;
        background:linear-gradient(to top, rgba(244,239,230,.98) 0%, rgba(244,239,230,.9) 70%, rgba(244,239,230,0) 100%); }}
      .cap {{ position:absolute; left:160px; right:160px; bottom:62px; z-index:30; display:flex; justify-content:center; }}
      .cap span {{ font-size:46px; font-weight:700; line-height:1.3; color:#18233A; text-align:center; letter-spacing:-0.01em;
        background:#FBF8F2; padding:10px 28px; border-radius:14px; border:3px solid #18233A; word-break:keep-all; }}
      #wipe {{ position:absolute; inset:0; z-index:40; pointer-events:none; }}
      #wipe .pn {{ position:absolute; left:0; top:0; bottom:0; width:100%; transform-origin:left center; }}
      #wipe .pnR {{ background:#C8281E; }}
      #wipe .pnN {{ background:#18233A; }}
      .wt {{ position:absolute; left:140px; top:410px; color:#F4EFE6; opacity:0; }}
      .wipeNum {{ font-family:"JetBrains Mono",monospace; font-size:40px; font-weight:700; color:#F2B8B2; letter-spacing:.14em; }}
            .wipeTitle {{ font-size:110px; font-weight:900; letter-spacing:-0.04em; margin-top:10px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      <div id="paper"></div>
      <div id="grid"></div>
      <div id="grain"></div>
      <div id="edge"></div>
{chr(10).join(hosts)}
      <div id="brand"><svg width="40" height="40" viewBox="0 0 64 64"><path fill="#C8281E" d="M32 4l5 11 7-4-2 14 9-6 2 6 9-2-5 12 4 3-15 9 2 8-14-3v12h-4V52l-14 3 2-8-15-9 4-3-5-12 9 2 2-6 9 6-2-14 7 4z"/></svg>AA CANADA</div>
      <div id="chapters" style="opacity:0">{chap_html}</div>
      <div id="capbar"></div>
{cap_html}
      <div id="wipe"><div class="pn pnR" id="pnR"></div><div class="pn pnN" id="pnN"></div>
{''.join(f'<div class="wt" id="wt{i}"><div class="wipeNum">{a}</div><div class="wipeTitle">{b}</div></div>' for i,(a,b) in enumerate(wipes))}</div>
      <audio id="narration" src="assets/narration.m4a" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      function chapterWipe(T, outSel, inSel, txt) {{
        // red then navy panel sweep in from the left, chapter title holds, panels sweep off to the right
        const a = T - 0.55;
        tl.fromTo('#pnR', {{scaleX:0, transformOrigin:'left center'}}, {{scaleX:1, duration:0.45, ease:'power3.in'}}, a);
        tl.fromTo('#pnN', {{scaleX:0, transformOrigin:'left center'}}, {{scaleX:1, duration:0.45, ease:'power3.in'}}, a + 0.1);
        tl.set(outSel, {{opacity:0}}, a + 0.56);
        tl.set(inSel, {{opacity:1}}, a + 0.56);
        tl.fromTo(txt, {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:'power3.out'}}, a + 0.55);
        tl.fromTo(txt, {{opacity:1, x:0}}, {{opacity:0, x:40, duration:0.3, ease:'power2.in', immediateRender:false}}, a + 1.55);
        tl.set('#pnR', {{transformOrigin:'right center'}}, a + 1.7);
        tl.set('#pnN', {{transformOrigin:'right center'}}, a + 1.7);
        tl.to('#pnN', {{scaleX:0, duration:0.5, ease:'power3.inOut'}}, a + 1.7);
        tl.to('#pnR', {{scaleX:0, duration:0.5, ease:'power3.inOut'}}, a + 1.8);
      }}
      function setChapter(t, idx) {{
        for (let i = 0; i < {len(CHAPTERS)}; i++) {{
          const on = i === idx;
          tl.to('#ch' + i, {{backgroundColor: on ? '#18233A' : 'rgba(222,211,192,0.55)', color: on ? '#F4EFE6' : '#4A5468', duration:0.3}}, t);
        }}
      }}
      tl.set(['#pnR','#pnN'], {{scaleX:0}}, 0);
      tl.fromTo('#grid', {{x:0, y:0}}, {{x:-80, y:-40, duration:{TOTAL}, ease:'none'}}, 0);
{chr(10).join('      ' + j for j in tjs)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(doc)
    return caps


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    B = scene_bodies()
    durs = []
    for k, (sid, *_r) in enumerate(SCENES):
        durs.append(write_scene(k, sid, B[sid]))
    caps = build_index(durs)
    for k, (sid, *_r) in enumerate(SCENES):
        print(sid, starts[k], ends[k], durs[k])
    print("captions", len(caps))
