"""Scenes 01-14 (opening -> education). Times in JS are AUDIO times; A(t) adds the lead-in offset."""
import json
import os
from common import icon as I, leaf, skyline, RED, INK, HI, SUB, MUTE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = json.load(open(os.path.join(ROOT, "assets/geo/geo.json")))
S = []


def scene(id, t0, t1, chap, ghost, html, js, glow=(1250, -250)):
    S.append(dict(id=id, t0=t0, t1=t1, chap=chap, ghost=ghost, html=html, js=js, glow=glow))


# ---------------------------------------------------------------- 01 opening
scene("s01", 0.0, 7.5, "", "MONTRÉAL", f"""
<div class="abs" id="s01-sky" style="left:0;top:600px;width:1920px;height:560px">{skyline()}</div>
<div class="abs" id="s01-sun" style="left:1380px;top:170px;width:260px;height:260px;border-radius:50%;background:{HI}"></div>
<div class="abs" style="left:110px;top:120px">
  <div class="kick" id="s01-k">AA CANADA · 몬트리올 기본 안내</div>
  <div class="bhs red" id="s01-t1" style="font-size:210px;line-height:1.05;margin-top:18px">몬트리올,</div>
  <div class="bhs" style="font-size:150px;line-height:1.1;color:{INK}"><span class="mkw"><span class="mk" id="s01-mk"></span><span id="s01-t2a">이것만</span></span> <span id="s01-t2b">보세요</span></div>
</div>
<div class="abs row" id="s01-chips" style="left:110px;top:560px;gap:18px">
  <span class="chip">자녀무상교육</span><span class="chip o">생활비</span><span class="chip o">교육 환경</span><span class="chip d">진행 절차</span>
</div>
<div class="abs" id="s01-snow" style="left:0;top:0;width:1920px;height:1080px">{''.join(f'<i class="sn" style="position:absolute;left:{(i * 137) % 1900}px;top:{(i * 71) % 500}px;width:{8 + i % 3 * 4}px;height:{8 + i % 3 * 4}px;border-radius:50%;background:#F1C7BE"></i>' for i in range(26))}</div>
""", """
tl.fromTo("#s01 .sk-back", { y: 160 }, { y: 0, duration: 1.4, ease: "power3.out" }, A(0));
tl.fromTo("#s01 .sk-mid", { y: 260 }, { y: 0, duration: 1.3, ease: "power3.out" }, A(0.15));
tl.fromTo("#s01 .sk-front", { y: 360 }, { y: 0, duration: 1.2, ease: "power4.out" }, A(0.3));
tl.fromTo("#s01 .sk-back", { x: 0 }, { x: -40, duration: 7.5, ease: "none", immediateRender: false }, A(0));
tl.fromTo("#s01 .sk-front", { x: 0 }, { x: -110, duration: 7.5, ease: "none", immediateRender: false }, A(0));
tl.fromTo("#s01 .win", { opacity: 0 }, { opacity: 1, duration: 0.2, stagger: { each: 0.012, from: "random" } }, A(1.0));
draw("#s01 .bridge", 1.4, 1.4);
tl.fromTo("#s01-sun", { y: 220, scale: 0.6 }, { y: 0, scale: 1, duration: 2.2, ease: "power2.out" }, A(0));
chars("#s01-t1", 0.25, { y: -160, rot: -12, st: 0.06 });
slide("#s01-t2a, #s01-t2b", 1.0, -140, { st: 0.15 });
mark("#s01-mk", 1.6);
tl.fromTo("#s01-k", { opacity: 0, letterSpacing: "0.6em" }, { opacity: 1, letterSpacing: "0.14em", duration: 0.9, ease: "power3.out" }, A(0.1));
pop("#s01-chips .chip", 3.5, { st: 0.28, y: 40 });
pulse("#s01-chips .chip", 5.8, { st: 0.12, s: 1.08 });
$$("#s01 .sn").forEach((s, i) => tl.fromTo(s, { y: -60 }, { y: 520 + (i % 5) * 40, x: ((i % 4) - 1.5) * 30, duration: 7.5, ease: "none" }, A(0)));
""", glow=(1100, -350))

# ---------------------------------------------------------------- 02 three merits
def merit(n, ic, l1, l2, x, idx):
    return f"""<div class="card ctr" id="s02-c{idx}" style="left:{x}px;top:250px;width:520px;height:440px;flex-direction:column;gap:16px">
  <div class="num red" style="font-size:110px;line-height:1">{n}</div>{I(ic, 92, RED, 4)}
  <div class="bhs" style="font-size:56px;line-height:1.15">{l1}</div><div class="body" style="font-size:36px;color:{SUB}">{l2}</div></div>"""


scene("s02", 7.5, 12.67, "몬트리올의 장점", "3 POINTS", f"""
<div class="abs" style="left:110px;top:120px"><span class="kick" id="s02-k">몬트리올, 이런 장점이 있어요</span></div>
{merit('01', 'child', '자녀 무상교육', '부모 학교 등록으로', 110, 1)}
{merit('02', 'pin', '캐나다 2위', '대도시', 700, 2)}
{merit('03', 'coin', '생활비', '가성비', 1290, 3)}
<div class="abs row" id="s02-ch" style="left:150px;top:730px;gap:16px"><span class="chip" id="s02-p1">사설어학원</span><span class="chip o" id="s02-p2">사립컬리지</span></div>
""", """
rise("#s02-k", 0.1, { y: 30 });
drop("#s02-c1", 0.4);
slam("#s02-c2", 0.95, { from: 1.8 });
slide("#s02-c3", 1.5, 700, { ease: "back.out(1.3)" });
draw("#s02 .ic", 0.6, 0.9, { st: 0.12 });
cam("#s02-c1", 3.0, 0.5, { scale: 1.07, y: -24 }, "back.out(2)");
dim("#s02-c2, #s02-c3", 3.0, 0.35);
pop("#s02-p1", 3.2, { y: 40 });
pop("#s02-p2", 4.2, { y: 40 });
""", glow=(-300, 300))

# ---------------------------------------------------------------- 03 structure
scene("s03", 12.67, 20.72, "몬트리올의 장점", "FREE", f"""
<div class="abs" id="s03-w" style="left:0;top:0;width:1920px;height:1080px">
 <div class="abs ctr" id="s03-n1" style="left:180px;top:200px;width:420px;height:420px;border-radius:50%;background:#FFFFFF;border:5px solid {INK};flex-direction:column">{I('parent', 150, INK, 4)}<div class="bhs" style="font-size:64px">부모님</div></div>
 <div class="abs" id="s03-tags" style="left:150px;top:650px;width:500px;display:flex;flex-direction:column;align-items:center;gap:14px">
   <span class="chip d" id="s03-v">학생비자</span>
   <div class="row" style="gap:12px"><span class="chip o" id="s03-a">사설어학원</span><span class="chip o" id="s03-b">사립컬리지</span></div></div>
 <svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="s03-arr" d="M620 410 C 820 300, 1040 300, 1230 400" stroke="{RED}" stroke-width="12" fill="none" stroke-linecap="round"/>
  <path id="s03-head" d="M1196 360 L1240 404 L1184 424" stroke="{RED}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
 <div class="abs body" id="s03-via" style="left:770px;top:250px;color:{SUB}">동반자녀 혜택</div>
 <div class="abs ctr" id="s03-n2" style="left:1260px;top:200px;width:420px;height:420px;border-radius:50%;background:{HI};border:5px solid {RED};flex-direction:column">{I('child', 140, RED, 4)}<div class="bhs" style="font-size:60px">동반자녀</div><div class="body" style="font-size:34px">공립학교</div></div>
 <div class="abs ctr" id="s03-st" style="left:1190px;top:600px;width:560px;height:190px;border:8px solid {RED};border-radius:26px;background:#FFFFFF;transform:rotate(-6deg)"><span class="bhs red" style="font-size:118px">학비 0원</span></div>
 <div class="abs" id="s03-bu" style="left:1470px;top:690px">{''.join(f'<i class="sp" style="position:absolute;width:{14 + i % 3 * 6}px;height:{14 + i % 3 * 6}px;border-radius:50%;background:{RED if i % 2 else HI}"></i>' for i in range(16))}</div>
</div>
""", """
tl.fromTo("#s03-w", { x: 260, scale: 1.12 }, { x: 260, scale: 1.12, duration: 0.01 }, A(12.67));
pop("#s03-n1", 12.8, { from: 0.5 });
draw("#s03-n1 .ic", 12.9, 0.8);
pop("#s03-v", 13.9, { y: 30 });
pop("#s03-a", 14.5, { y: 30 });
pop("#s03-b", 16.1, { y: 30 });
cam("#s03-w", 16.6, 1.0, { x: 0, scale: 1 }, "power3.inOut");
draw("#s03-arr", 16.9, 0.8);
draw("#s03-head", 17.6, 0.25);
fade("#s03-via", 17.2);
pop("#s03-n2", 17.7, { from: 0.4 });
draw("#s03-n2 .ic", 17.8, 0.7);
slam("#s03-st", 18.7, { from: 3, rot: -20, to: -6 });
burst("#s03-bu .sp", 18.8);
pulse("#s03-n2", 19.6, { s: 1.05 });
""", glow=(1300, 0))

# ---------------------------------------------------------------- 04 parent benefits
def tile(i, ic, title, sub, x, y):
    return f"""<div class="card row" id="s04-t{i}" style="left:{x}px;top:{y}px;width:860px;height:170px;gap:30px;padding:0 40px">
 {I(ic, 100, RED, 4)}<div><div class="bhs" style="font-size:58px">{title}</div><div class="body" style="font-size:32px;color:{SUB}">{sub}</div></div>
 <div style="margin-left:auto">{I('check', 84, RED, 5, cls='ck')}</div></div>"""


scene("s04", 20.72, 28.5, "몬트리올의 장점", "PARENTS", f"""
<div class="abs" style="left:110px;top:120px"><div class="kick" id="s04-k">부모님 입장에서도</div><div class="h2" id="s04-h" style="margin-top:8px">부담은 <span class="red">낮고</span>, 생활은 <span class="red">편하게</span></div></div>
{tile(1, 'coin', '부모님 학비 저렴', '사설어학원 · 사립컬리지', 110, 340)}
{tile(2, 'book', '학업 부담 적당', '너무 높지 않은 수업 강도', 560, 540)}
{tile(3, 'clock', '등하교 케어에 유리', '수업 스케줄', 950, 740)}
""", """
rise("#s04-k, #s04-h", 20.8, { st: 0.12 });
slide("#s04-t1", 21.6, -900);
slide("#s04-t2", 22.6, 900);
tl.fromTo("#s04-t3", { y: 300, opacity: 0, rotation: 6 }, { y: 0, opacity: 1, rotation: 0, duration: 0.7, ease: "back.out(1.5)" }, A(25.1));
draw("#s04-t1 .ck .ic", 22.2, 0.5);
draw("#s04-t2 .ck .ic", 23.8, 0.5);
draw("#s04-t3 .ck .ic", 27.3, 0.5);
cam("#s04 .stage", 24.2, 3.5, { scale: 1.03 }, "power1.inOut");
""", glow=(-200, 500))

# ---------------------------------------------------------------- 05 big city map
canada = "".join(f'<path class="pv pv-{k}" d="{d}"/>' for k, d in GEO["canada"].items())
cx, cy = GEO["cities"]["montreal"]


def ibox(i, ic, t, y):
    return f'<div class="card row" id="s05-i{i}" style="left:1180px;top:{y}px;width:640px;height:160px;gap:28px;padding:0 36px">{I(ic, 92, RED, 4)}<div class="bhs" style="font-size:58px">{t}</div></div>'


scene("s05", 28.5, 40.75, "캐나다 2위 대도시", "CANADA", f"""
<div class="abs" id="s05-map" style="left:60px;top:100px;width:1100px;height:860px;transform-origin:{cx}px {cy}px">
 <svg width="1100" height="860" viewBox="0 0 1100 860" style="overflow:visible">
  <g id="s05-pv" fill="#FBE9E4" stroke="{SUB}" stroke-width="2" stroke-linejoin="round">{canada}</g>
  <circle id="s05-r1" cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{RED}" stroke-width="4"/>
  <circle id="s05-r2" cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{RED}" stroke-width="4"/>
  <circle id="s05-dot" cx="{cx}" cy="{cy}" r="16" fill="{RED}" stroke="#FFFFFF" stroke-width="5"/>
 </svg>
 <div class="abs" id="s05-lbl" style="left:{cx - 250}px;top:{cy - 150}px"><span class="chip">몬트리올 Montréal</span></div>
</div>
<div class="abs" id="s05-badge" style="left:1180px;top:200px;width:640px">
 <div class="kick">CANADA</div>
 <div class="bhs" style="font-size:150px;line-height:1"><span class="red num" id="s05-n">2</span>위</div>
 <div class="h3">캐나다 대도시</div>
 <div class="body" style="margin-top:14px;font-size:34px;color:{SUB}">도시권 인구 약 460만 명</div>
 <div class="small" style="font-size:28px;font-weight:500">통계청 2025.7.1 추정(CMA)</div></div>
<div class="abs kick" id="s05-k2" style="left:1180px;top:150px">대도시라서 좋은 점</div>
{ibox(1, 'school', '교육 수준', 220)}{ibox(2, 'bag', '생활 편의성', 410)}{ibox(3, 'music', '문화 환경', 600)}
""", """
tl.fromTo("#s05-pv path", { fillOpacity: 0 }, { fillOpacity: 1, duration: 1.2, ease: "power1.out" }, A(29.3));
draw("#s05-pv path", 28.55, 1.6, { st: 0.04 });
tl.fromTo("#s05 .pv-QC", { fill: "#FBE9E4" }, { fill: "#FFD6CF", duration: 0.6 }, A(29.9));
tl.fromTo("#s05-dot", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.5, ease: "back.out(3)" }, A(30.0));
[0, 0.6].forEach((d, i) => tl.fromTo(["#s05-r1", "#s05-r2"][i], { attr: { r: 16 }, opacity: 1 }, { attr: { r: 90 }, opacity: 0, duration: 1.6, ease: "power2.out", repeat: 3, repeatDelay: 0.4 }, A(30.0 + d)));
pop("#s05-lbl", 30.3, { y: 30 });
slide("#s05-badge", 30.5, 300);
count("#s05-n", 30.6, 0.8, 10, 2, (v) => String(Math.round(v)));
cam("#s05-map", 32.8, 1.6, { scale: 1.9, x: -230, y: -200 }, "power3.inOut");
tl.to("#s05-badge", { opacity: 0, x: 80, duration: 0.4 }, A(35.2));
rise("#s05-k2", 35.4, { y: 20 });
slide("#s05-i1", 36.1, 700); draw("#s05-i1 .ic", 36.2, 0.8);
slide("#s05-i2", 37.3, 700); draw("#s05-i2 .ic", 37.4, 0.8);
slide("#s05-i3", 38.7, 700); draw("#s05-i3 .ic", 38.8, 0.8);
pulse("#s05-i1, #s05-i2, #s05-i3", 39.8, { st: 0.12, s: 1.05 });
""", glow=(400, 200))

# ---------------------------------------------------------------- 06 balance: cost of living
scene("s06", 40.75, 51.0, "가성비", "COST", f"""
<div class="abs" style="left:110px;top:120px"><div class="kick" id="s06-k">캐나다 2위 대도시인데</div><div class="h2" id="s06-h" style="margin-top:6px">생활비는?</div></div>
<div class="abs" id="s06-bal" style="left:360px;top:420px;width:1200px;height:440px">
 <div class="abs" style="left:560px;top:80px;width:80px;height:360px;background:{INK};clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"></div>
 <div class="abs" id="s06-beam" style="left:0;top:60px;width:1200px;height:40px;transform-origin:600px 20px">
   <div class="abs" style="left:0;top:0;width:1200px;height:22px;background:{INK};border-radius:11px"></div>
   <div class="abs" id="s06-pl" style="left:-40px;top:22px;width:420px;height:260px;transform-origin:210px 0">
     <div class="abs" style="left:205px;top:0;width:10px;height:120px;background:{INK}"></div>
     <div class="abs" style="left:0;top:120px;width:420px;height:16px;background:{INK};border-radius:8px"></div>
     <div class="abs row" style="left:10px;top:-50px;gap:10px;transform:translateY(0)">
       <div class="card ctr" id="s06-van" style="position:relative;width:195px;height:160px;flex-direction:column;box-shadow:8px 8px 0 #FFD6CF">{I('house', 64, INK, 4)}<div class="bhs" style="font-size:40px">밴쿠버</div></div>
       <div class="card ctr" id="s06-tor" style="position:relative;width:195px;height:160px;flex-direction:column;box-shadow:8px 8px 0 #FFD6CF">{I('house', 64, INK, 4)}<div class="bhs" style="font-size:40px">토론토</div></div></div>
     <div class="abs bhs" id="s06-dd" style="left:120px;top:150px;font-size:76px;color:{INK}">$$$</div>
   </div>
   <div class="abs" id="s06-pr" style="left:820px;top:22px;width:420px;height:260px;transform-origin:210px 0">
     <div class="abs" style="left:205px;top:0;width:10px;height:120px;background:{INK}"></div>
     <div class="abs" style="left:0;top:120px;width:420px;height:16px;background:{INK};border-radius:8px"></div>
     <div class="card ctr" id="s06-mtl" style="left:95px;top:-50px;width:230px;height:160px;flex-direction:column;border-color:{RED}">{I('house', 64, RED, 4)}<div class="bhs red" style="font-size:40px">몬트리올</div></div>
     <div class="abs bhs red" id="s06-d" style="left:180px;top:150px;font-size:76px">$</div>
   </div>
 </div>
</div>
<div class="abs" id="s06-res" style="left:1080px;top:140px;transform:rotate(-3deg)"><div class="card ctr" style="position:relative;padding:22px 40px;flex-direction:column;border-color:{RED}"><div class="body" style="color:{SUB}">아파트 렌트비 등 생활비</div><div class="bhs red" style="font-size:86px"><span class="mkw"><span class="mk" id="s06-mk"></span>중소도시 수준</span></div></div></div>
""", """
rise("#s06-k", 41.0, { y: 30 }); chars("#s06-h", 41.3, { st: 0.07 });
rise("#s06-bal", 42.4, { y: 120, d: 0.8 });
drop("#s06-van", 45.0, { y: -420 });
drop("#s06-tor", 45.7, { y: -420, rot: 12 });
tl.fromTo("#s06-beam", { rotation: 0 }, { rotation: -9, duration: 1.0, ease: "elastic.out(1, 0.5)" }, A(45.9));
tl.fromTo(["#s06-pl", "#s06-pr"], { rotation: 0 }, { rotation: 9, duration: 1.0, ease: "elastic.out(1, 0.5)" }, A(45.9));
pop("#s06-dd", 46.4, { y: 30 });
drop("#s06-mtl", 46.8, { y: -420 });
pop("#s06-d", 47.4, { y: 30 });
slam("#s06-res", 48.6, { from: 2.2, rot: 8, to: -3 });
mark("#s06-mk", 49.1);
""", glow=(700, 300))

# ---------------------------------------------------------------- 07 cost vs experience
scene("s07", 51.0, 64.8, "가성비", "VALUE", f"""
<div class="abs" id="s07-top" style="left:110px;top:120px;transform-origin:0 0"><div class="kick" id="s07-k">자녀 동반 · 자녀무상교육 플랜 도시 중</div>
 <div class="h1" id="s07-h" style="margin-top:6px">몬트리올은 <span class="mkw"><span class="mk" id="s07-mk"></span><span class="red">가성비</span></span></div></div>
<div class="abs" id="s07-m1" style="left:150px;top:400px;width:760px">
 <div class="row" style="gap:20px">{I('coin', 84, INK, 4)}<div class="bhs" style="font-size:64px">비용</div><div class="chip d" id="s07-c1" style="margin-left:auto">저렴</div></div>
 <div style="margin-top:26px;width:760px;height:64px;border:5px solid {INK};border-radius:32px;overflow:hidden;background:#FFFFFF"><div id="s07-f1" style="width:100%;height:100%;background:{INK};transform-origin:0 50%"></div></div></div>
<div class="abs" id="s07-m2" style="left:1010px;top:400px;width:760px">
 <div class="row" style="gap:20px">{I('star', 84, RED, 4)}<div class="bhs" style="font-size:64px">교육 · 경험</div><div class="chip" id="s07-c2" style="margin-left:auto">훌륭</div></div>
 <div style="margin-top:26px;width:760px;height:64px;border:5px solid {RED};border-radius:32px;overflow:hidden;background:#FFFFFF"><div id="s07-f2" style="width:100%;height:100%;background:{RED};transform-origin:0 50%"></div></div>
 <div class="row" id="s07-ics" style="gap:26px;margin-top:30px">{I('book', 76, RED, 4)}{I('music', 76, RED, 4)}{I('globe', 76, RED, 4)}{I('people', 76, RED, 4)}</div></div>
<div class="abs" id="s07-pop" style="left:620px;top:700px"><div class="card row" style="position:relative;padding:18px 40px;gap:22px;border-color:{RED}">{I('heart', 80, RED, 5)}<div class="bhs" style="font-size:66px">그래서 <span class="red">인기!</span></div></div></div>
""", """
rise("#s07-k", 51.1, { y: 30 });
chars("#s07-h", 51.5, { st: 0.05, y: 90 });
mark("#s07-mk", 52.8);
tl.to("#s07-top", { scale: 0.62, duration: 0.6, ease: "power3.inOut" }, A(55.9));
slide("#s07-m1", 56.2, -500);
tl.fromTo("#s07-f1", { scaleX: 1 }, { scaleX: 0.22, duration: 1.4, ease: "power3.inOut" }, A(57.4));
pop("#s07-c1", 58.3);
slide("#s07-m2", 59.0, 500);
tl.fromTo("#s07-f2", { scaleX: 0.05 }, { scaleX: 0.95, duration: 1.6, ease: "power3.out" }, A(59.8));
pop("#s07-ics .icon", 60.4, { st: 0.18 });
pop("#s07-c2", 62.2);
tl.fromTo("#s07-pop", { y: 260, opacity: 0, scale: 0.6 }, { y: 0, opacity: 1, scale: 1, duration: 0.7, ease: "back.out(2)" }, A(63.1));
pulse("#s07-pop", 63.9, { s: 1.08 });
""", glow=(1400, 400))

# ---------------------------------------------------------------- 08 population chart (director's image) -> pillars
def pillar(i, ic, t, x):
    return f"""<div class="abs" id="s08-p{i}" style="left:{x}px;top:470px;width:380px;height:400px;transform-origin:50% 100%">
 <div class="ctr" style="width:380px;height:400px;background:#FFFFFF;border:5px solid {INK};border-radius:24px 24px 0 0;flex-direction:column;gap:20px">{I(ic, 110, RED, 4)}<div class="bhs" style="font-size:56px">{t}</div></div></div>"""


PW8, PH8 = 1300, 720
scene("s08", 64.8, 76.0, "캐나다 2위 대도시", "NO.2", f"""
<div class="abs" id="s08-chart" style="left:0;top:0;width:1920px;height:1080px;transform-origin:700px 470px">
 <div class="win" id="s08-win" style="left:90px;top:110px;width:{PW8}px;height:{PH8}px">
  <div class="pic" id="s08-pic" style="width:1081px;height:608px">
   <img src="assets/img/owner/city-population.png" style="left:0;top:0;width:1081px;height:608px" alt="캐나다 주요 도시별 인구">
   <div class="abs" id="s08-dimA" style="left:280px;top:36px;width:801px;height:36px;background-color:rgba(255,255,255,0.62)"></div>
   <div class="abs" id="s08-dimB" style="left:280px;top:108px;width:801px;height:500px;background-color:rgba(255,255,255,0.62)"></div>
   <div class="hl" id="s08-hl" style="left:294px;top:70px;width:604px;height:40px"></div>
   <div class="abs" id="s08-b2" style="left:902px;top:70px"><span class="chip" style="font-size:22px;padding:4px 14px">2위</span></div>
  </div></div>
 <div class="abs" id="s08-pan" style="left:1440px;top:150px;width:440px">
  <div class="kick" style="font-size:30px">몬트리올 도시권 인구</div>
  <div class="num red" id="s08-n" style="font-size:104px;line-height:1.05;margin-top:12px">0</div>
  <div class="bhs" style="font-size:44px">천 명 · <span class="red">캐나다 2위</span></div>
  <div style="margin-top:22px"><span class="chip d" id="s08-c" style="font-size:34px">약 460만 명</span></div>
  <div class="small" id="s08-src" style="margin-top:40px;font-size:28px;font-weight:500">출처: 캐나다 통계청 Table 17-10-0148-01, 2025년 7월 1일 인구 추정(도시권 CMA)</div>
 </div>
</div>
<div class="abs ctr" id="s08-top" style="left:0;top:130px;width:1920px;flex-direction:column"><div class="kick">캐나다 2위 대도시라서</div><div class="h2">갖춘 것들</div></div>
<div class="abs" id="s08-roof" style="left:300px;top:330px;width:1320px;height:140px;background:{RED};clip-path:polygon(4% 100%,96% 100%,100% 70%,50% 0,0 70%)"></div>
<div class="abs ctr bhs" id="s08-rt" style="left:300px;top:380px;width:1320px;font-size:64px;color:#FFFFFF">최고의 조건</div>
{pillar(1, 'school', '교육 환경', 330)}{pillar(2, 'music', '문화 환경', 770)}{pillar(3, 'bag', '생활 편의성', 1210)}
<div class="abs" id="s08-sp" style="left:960px;top:400px">{''.join(f'<i class="sp" style="position:absolute;width:18px;height:18px;background:{RED if i % 2 else HI};transform:rotate(45deg)"></i>' for i in range(14))}</div>
""", f"""
setView("#s08-pic", 64.8, 1.184, 540.5, 304, {PW8}, {PH8});
tl.fromTo("#s08-win", {{ scale: 0.85, opacity: 0, rotation: -2 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.6, ease: "back.out(1.6)" }}, A(64.9));
fade("#s08-dimA, #s08-dimB", 66.0, {{ d: 0.4 }});
view("#s08-pic", 65.9, 1.0, 1.75, 690, 150, {PW8}, {PH8});
tl.fromTo("#s08-hl", {{ scaleX: 0, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, A(66.2));
pop("#s08-b2", 66.7, {{ from: 0 }});
slide("#s08-pan", 65.6, 300);
count("#s08-n", 65.9, 1.6, 0, 4597.84, (v) => v.toLocaleString("en-US", {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}));
pop("#s08-c", 67.3, {{ y: 20 }});
pulse("#s08-hl", 67.6, {{ s: 1.03 }});
tl.to("#s08-chart", {{ opacity: 0, scale: 0.9, duration: 0.45, ease: "power2.in" }}, A(68.3));
rise("#s08-top", 68.7, {{ y: 40 }});
growY("#s08-p1", 70.0); draw("#s08-p1 .ic", 70.3, 0.7);
growY("#s08-p2", 70.8); draw("#s08-p2 .ic", 71.1, 0.7);
growY("#s08-p3", 71.8); draw("#s08-p3 .ic", 72.1, 0.7);
tl.to("#s08-top", {{ opacity: 0, duration: 0.3 }}, A(72.8));
tl.fromTo("#s08-roof", {{ y: -400, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "bounce.out" }}, A(73.0));
tl.fromTo("#s08-rt", {{ y: -400, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "bounce.out" }}, A(73.05));
burst("#s08-sp .sp", 73.6);
cam("#s08 .stage", 73.8, 2.2, {{ scale: 1.04 }}, "sine.inOut");
""", glow=(660, -100))

# ---------------------------------------------------------------- 09 rent: StatCan infographic (director's image)
RR = json.load(open(os.path.join(ROOT, "assets/img/owner/rects.json")))["rent"]
PW9, PH9 = 1060, 770
sprites = "".join(f'<img class="rs" id="s09-{k}" src="assets/img/owner/rent-{k}.png" style="left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px" alt="">'
                  for k, (x0, y0, x1, y1) in RR.items())
scene("s09", 76.0, 91.0, "렌트비 비교", "RENT", f"""
<div class="win" id="s09-win" style="left:90px;top:100px;width:{PW9}px;height:{PH9}px;background-color:#F2F2F2">
 <div class="pic" id="s09-pic" style="width:1054px;height:1349px">
  <img src="assets/img/owner/rent-base.jpg" style="left:0;top:0;width:1054px;height:1349px" alt="캐나다 통계청 인포그래픽: 방 2개 아파트 평균 호가 월세">
  {sprites}
  <div class="hl" id="s09-ring" style="left:568px;top:748px;width:162px;height:68px;border-width:6px;border-radius:10px"></div>
 </div></div>
<div class="abs" id="s09-pan" style="left:1210px;top:120px;width:660px">
 <div class="kick" id="s09-k">캐나다 통계청 · 2026년 2분기</div>
 <div class="h3" id="s09-h" style="margin-top:8px;font-size:56px">방 2개 아파트<br>평균 호가 월세</div>
 <div id="s09-big" style="margin-top:34px"><div class="bhs" style="font-size:50px">몬트리올</div><div class="num red" id="s09-n" style="font-size:150px;line-height:1">$0</div></div>
 <div id="s09-call" style="margin-top:26px;transform:rotate(-2deg);transform-origin:0 50%"><div class="card" style="position:relative;display:inline-block;padding:14px 28px;border-color:{RED}"><div class="body" style="font-size:30px;color:{SUB}">캘거리·핼리팩스보다 낮은 월세</div><div class="bhs red" style="font-size:60px"><span class="mkw"><span class="mk" id="s09-mk"></span>중소도시 수준</span></div></div></div>
</div>
<div class="abs small" id="s09-src" style="left:1210px;top:790px;width:660px;font-size:28px;font-weight:500">출처: 캐나다 통계청 Table 46-10-0092-01, 2026년 2분기 (2026.09.09 발표)</div>
""", f"""
setView("#s09-pic", 76.0, 0.571, 527, 674.5, {PW9}, {PH9});
tl.fromTo("#s09-win", {{ y: 120, opacity: 0, rotation: 2 }}, {{ y: 0, opacity: 1, rotation: 0, duration: 0.7, ease: "back.out(1.5)" }}, A(76.1));
tl.set("#s09 .rs, #s09-ring", {{ opacity: 0 }}, A(76.0));
slam("#s09-k", 76.8, {{ from: 1.6 }});
rise("#s09-h", 77.4, {{ y: 30 }});
fade("#s09-src", 78.2);
view("#s09-pic", 78.6, 1.1, 1.08, 520, 790, {PW9}, {PH9});
const POP = [["van", 79.6], ["tor", 80.9], ["hal", 81.5], ["ott", 81.9], ["cal", 82.3], ["edm", 82.7]];
POP.forEach(([k, t], i) => tl.fromTo("#s09-" + k, {{ opacity: 0, scale: 0.4, y: -30, transformOrigin: "50% 30%" }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2.2)" }}, A(t)));
pulse("#s09-van, #s09-tor", 83.1, {{ s: 1.12, st: 0.18 }});
view("#s09-pic", 84.2, 1.0, 1.9, 690, 820, {PW9}, {PH9});
tl.to("#s09-van, #s09-tor, #s09-hal, #s09-ott, #s09-cal, #s09-edm", {{ opacity: 0.35, duration: 0.4 }}, A(84.3));
tl.fromTo("#s09-mtl", {{ opacity: 0, scale: 2.4, transformOrigin: "50% 25%" }}, {{ opacity: 1, scale: 1, duration: 0.55, ease: "expo.out" }}, A(84.7));
tl.fromTo("#s09-ring", {{ opacity: 0, scale: 1.5, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, A(85.2));
fade("#s09-big", 84.8, {{ d: 0.2 }});
count("#s09-n", 84.8, 1.2, 0, 1820, (v) => "$" + Math.round(v).toLocaleString("en-US"));
pulse("#s09-n", 86.2, {{ s: 1.12 }});
pulse("#s09-ring", 86.6, {{ s: 1.08 }});
view("#s09-pic", 87.8, 1.0, 1.15, 520, 800, {PW9}, {PH9});
tl.to("#s09-van, #s09-tor, #s09-hal, #s09-ott, #s09-cal, #s09-edm", {{ opacity: 1, duration: 0.4 }}, A(87.9));
slam("#s09-call", 88.2, {{ from: 2, rot: 6, to: -2 }});
mark("#s09-mk", 88.9);
pulse("#s09-ring", 89.6, {{ s: 1.1 }});
""", glow=(1500, 500))

# ---------------------------------------------------------------- 10 language + math
def kbox(i, t, x, col):
    return f'<div class="abs ctr bhs" id="s10-k{i}" style="left:{x}px;top:330px;width:330px;height:330px;border-radius:40px;border:6px solid {INK};background:{col};font-size:200px;color:{INK}">{t}</div>'


scene("s10", 91.0, 96.6, "교육 환경", "LANGUAGE", f"""
<div class="abs" style="left:110px;top:120px"><div class="kick" id="s10-kk">한국은 국·영·수, 캐나다는?</div></div>
<div id="s10-kr">{kbox(1, '국', 330, '#FFFFFF')}{kbox(2, '영', 795, '#FFFFFF')}{kbox(3, '수', 1260, '#FFFFFF')}</div>
<div class="abs ctr" id="s10-l" style="left:250px;top:330px;width:640px;height:330px;border-radius:40px;background:{INK};flex-direction:column"><div class="bhs" style="font-size:110px;color:#FFFFFF">랭귀지</div><div class="body" style="color:{HI}">Language</div></div>
<div class="abs ctr bhs red" id="s10-plus" style="left:900px;top:400px;width:120px;font-size:150px">+</div>
<div class="abs ctr" id="s10-m" style="left:1030px;top:330px;width:640px;height:330px;border-radius:40px;background:{RED};flex-direction:column"><div class="bhs" style="font-size:110px;color:#FFFFFF">수학</div><div class="body" style="color:{HI}">Math</div></div>
<div class="abs ctr" id="s10-imp" style="left:0;top:720px;width:1920px"><span class="chip d" style="font-size:44px">가장 중요한 두 과목</span></div>
""", """
rise("#s10-kk", 91.2, { y: 30 });
slam("#s10-k1", 91.5, { from: 2.2 }); slam("#s10-k2", 91.8, { from: 2.2 }); slam("#s10-k3", 92.1, { from: 2.2 });
tl.to("#s10-kr", { opacity: 0, scale: 0.8, duration: 0.35, ease: "power2.in" }, A(93.6));
flipIn("#s10-l", 94.1); pop("#s10-plus", 94.7); flipIn("#s10-m", 94.95);
pop("#s10-imp", 95.5, { y: 30 });
""", glow=(700, 100))

# ---------------------------------------------------------------- 11 PCAP 2023 (director's image)
PW11, PH11 = 1300, 760
scene("s11", 96.6, 101.4, "교육 환경", "PCAP", f"""
<div class="win" id="s11-win" style="left:90px;top:100px;width:{PW11}px;height:{PH11}px;background-color:#F2EFEA">
 <div class="pic" id="s11-pic" style="width:874px;height:491px">
  <img src="assets/img/owner/pcap2023-math.png" style="left:0;top:0;width:874px;height:491px" alt="PCAP 2023 수학 평균 점수">
  <div class="abs" id="s11-line" style="left:372px;top:352px;width:466px;height:0;border-top:2px dashed #C8102E;transform-origin:0 50%"></div>
  <div class="hl" id="s11-qc" style="left:596px;top:298px;width:42px;height:176px;border-width:3px;border-radius:6px"></div>
  <div class="hl" id="s11-can" style="left:788px;top:328px;width:44px;height:146px;border-width:3px;border-radius:6px;border-color:#2B2B2B"></div>
 </div></div>
<div class="abs" id="s11-pan" style="left:1440px;top:130px;width:440px">
 <div class="kick" style="font-size:30px">CMEC PCAP 2023</div>
 <div class="body" style="font-size:34px;margin-top:6px">중2(Secondary II) 수학 평균</div>
 <div id="s11-q" style="margin-top:26px"><div class="bhs" style="font-size:50px">퀘벡</div><div class="num red" id="s11-qn" style="font-size:150px;line-height:1">0</div></div>
 <div id="s11-c" style="margin-top:14px"><div class="bhs" style="font-size:40px">캐나다 평균 <span class="num" id="s11-cn">0</span></div></div>
 <div style="margin-top:22px"><span class="chip" id="s11-top" style="font-size:34px">10개 주 중 최고</span></div>
</div>
<div class="abs small" id="s11-src" style="left:1440px;top:800px;width:440px;font-size:28px;font-weight:500">출처: CMEC PCAP 2023</div>
""", f"""
setView("#s11-pic", 96.6, 1.487, 437, 245.5, {PW11}, {PH11});
tl.fromTo("#s11-win", {{ scale: 0.88, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, A(96.65));
view("#s11-pic", 97.0, 0.9, 2.6, 605, 360, {PW11}, {PH11});
slide("#s11-pan", 97.1, 300);
fade("#s11-src", 97.4);
fade("#s11-c", 97.8, {{ d: 0.2 }});
count("#s11-cn", 97.8, 0.8, 400, 510, (v) => String(Math.round(v)) + "점");
grow("#s11-line", 97.9, {{ d: 0.6, ease: "power2.out" }});
tl.fromTo("#s11-can", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, A(98.0));
tl.fromTo("#s11-qc", {{ opacity: 0, scale: 1.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, A(99.1));
count("#s11-qn", 99.1, 1.0, 400, 537, (v) => String(Math.round(v)) + "점");
pop("#s11-top", 99.9, {{ y: 20 }});
pulse("#s11-qc", 100.5, {{ s: 1.08 }});
""", glow=(1600, 100))

# ---------------------------------------------------------------- 12 bilingual
scene("s12", 101.4, 109.0, "교육 환경", "BONJOUR", f"""
<div class="abs" style="left:110px;top:120px"><div class="kick" id="s12-k">몬트리올 아이들은</div><div class="h2" id="s12-h" style="margin-top:6px">영어 + 불어, <span class="red">둘 다 자연스럽게</span></div></div>
<div class="abs" id="s12-ven" style="left:0;top:0;width:1920px;height:1080px">
 <div class="abs ctr" id="s12-en" style="left:440px;top:330px;width:560px;height:480px;border-radius:50%;background:rgba(43,43,43,0.88);flex-direction:column"><div class="bhs" style="font-size:96px;color:#FFFFFF">Hello!</div><div class="body" style="color:#FFFFFF">영어</div></div>
 <div class="abs ctr" id="s12-fr" style="left:920px;top:330px;width:560px;height:480px;border-radius:50%;background:rgba(200,16,46,0.88);flex-direction:column"><div class="bhs" style="font-size:96px;color:#FFFFFF">Bonjour!</div><div class="body" style="color:#FFFFFF">불어</div></div>
 <div class="abs ctr" id="s12-kid" style="left:880px;top:700px;width:160px;height:160px;border-radius:50%;background:#FFFFFF;border:5px solid {INK}">{I('child', 110, INK, 4)}</div>
</div>
<div class="abs" id="s12-many" style="left:0;top:0">{''.join(f'<div class="abs kd" style="left:{120 + (i % 6) * 64 if i < 6 else 1480 + (i % 6) * 64}px;top:{820 if i < 6 else 300}px">{I("child", 56, RED if i % 2 else INK, 5)}</div>' for i in range(12))}</div>
""", """
rise("#s12-k", 101.7, { y: 30 }); rise("#s12-h", 102.0, { y: 40 });
tl.fromTo("#s12-en", { x: -600, scale: 0.5, opacity: 0 }, { x: 0, scale: 1, opacity: 1, duration: 0.7, ease: "back.out(1.6)" }, A(103.5));
tl.fromTo("#s12-fr", { x: 600, scale: 0.5, opacity: 0 }, { x: 0, scale: 1, opacity: 1, duration: 0.7, ease: "back.out(1.6)" }, A(104.4));
pop("#s12-kid", 105.4, { from: 0 }); draw("#s12-kid .ic", 105.5, 0.6);
pulse("#s12-en, #s12-fr", 106.5, { s: 1.05, st: 0.15 });
pop("#s12-many .kd", 107.4, { st: 0.07, y: 30 });
""", glow=(960, 300))

# ---------------------------------------------------------------- 13 investment: bus / 3D printer / smartboard
def inv(i, ic, t1, t2, x):
    return f"""<div class="card ctr" id="s13-c{i}" style="left:{x}px;top:330px;width:520px;height:470px;flex-direction:column;gap:18px">
 <div class="ctr" style="width:220px;height:220px;border-radius:50%;background:{HI}">{I(ic, 140, RED, 4)}</div>
 <div class="bhs" style="font-size:58px">{t1}</div><div class="body" style="font-size:34px;color:{SUB}">{t2}</div></div>"""


scene("s13", 109.0, 119.5, "교육 환경", "QUÉBEC", f"""
<div class="abs" id="s13-top" style="left:110px;top:120px;transform-origin:0 0"><div class="kick" id="s13-k">퀘벡주는</div><div class="h1" id="s13-h" style="margin-top:6px">교육 <span class="mkw"><span class="mk" id="s13-mk"></span><span class="red">투자</span></span>가 크다</div></div>
{inv(1, 'bus', '전기 스쿨버스', '스쿨버스 전기화', 110, )}{inv(2, 'printer', '3D 프린터', '초등학교', 700)}{inv(3, 'board', '스마트보드', '교실', 1290)}
<div class="abs" id="s13-cube" style="left:925px;top:470px;width:70px;height:70px">{''.join(f'<i class="ly" style="position:absolute;left:0;bottom:{k * 12}px;width:70px;height:11px;background:{RED};transform-origin:50% 100%"></i>' for k in range(5))}</div>
""", """
rise("#s13-k", 109.1, { y: 30 }); chars("#s13-h", 109.8, { st: 0.06, y: 100 });
mark("#s13-mk", 111.4);
tl.to("#s13-top", { scale: 0.55, duration: 0.6, ease: "power3.inOut" }, A(112.6));
tl.fromTo("#s13-c1", { x: -1200 }, { x: 0, duration: 1.0, ease: "power4.out" }, A(113.0)); draw("#s13-c1 .ic", 113.3, 0.9);
pop("#s13-c2", 115.8); draw("#s13-c2 .ic", 116.0, 0.9);
growY("#s13-cube .ly", 116.6, { st: 0.15, d: 0.25, ease: "power2.out" });
fade("#s13-cube", 116.5, { d: 0.1 });
flipIn("#s13-c3", 117.8); draw("#s13-c3 .ic", 118.0, 0.9);
""", glow=(-200, 600))

# ---------------------------------------------------------------- 14 result: top level
scene("s14", 119.5, 124.7, "교육 환경", "TOP", f"""
<div class="abs ctr" style="left:0;top:150px;width:1920px;flex-direction:column">
 <div class="kick" id="s14-k">결과적으로</div>
 <div id="s14-tr" style="margin-top:20px">{I('trophy', 230, RED, 3.5)}</div>
 <div class="h2" id="s14-h1" style="margin-top:10px">몬트리올의 학업 환경</div>
 <div class="bhs red" id="s14-h2" style="font-size:136px;line-height:1.1"><span class="mkw"><span class="mk" id="s14-mk"></span>캐나다 최고 수준</span></div></div>
<div class="abs" id="s14-cf" style="left:960px;top:420px">{''.join(f'<i class="sp" style="position:absolute;width:{12 + i % 4 * 5}px;height:{20 + i % 3 * 6}px;background:{[RED, HI, INK, SUB][i % 4]}"></i>' for i in range(24))}</div>
""", """
rise("#s14-k", 119.8, { y: 30 });
pop("#s14-tr", 120.2, { from: 0.2, rot: -20 }); draw("#s14-tr .ic", 120.3, 1.0);
rise("#s14-h1", 121.2, { y: 50 });
slam("#s14-h2", 122.4, { from: 2.6 });
mark("#s14-mk", 122.9);
burst("#s14-cf .sp", 122.5);
cam("#s14 .stage", 123.0, 1.7, { scale: 1.05 }, "sine.inOut");
""", glow=(660, 0))
