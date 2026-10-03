# Generates compositions/frames/*.html for the Montreal Shorts (1080x1920).
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = {}
sb = open(os.path.join(ROOT, "STORYBOARD.md")).read()
for m in re.finditer(r"- duration: ([\d.]+)s\n.*?- src: compositions/frames/(\S+)\.html", sb, re.S):
    DUR[m.group(2)] = float(m.group(1))

FONTS = "".join(
    f"@font-face{{font-family:'Pretendard';src:url('assets/fonts/Pretendard-{n}.woff2') format('woff2');font-weight:{w};font-style:normal;}}"
    for n, w in [("Regular", 400), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800), ("Black", 900)]
)
C = dict(bg="#0e1a3a", p="#ffc531", t="#ffffff", m="#b8c0d9", l="#8d97b5",
         al="rgba(255,197,49,0.14)", am="rgba(255,197,49,0.30)", bd="rgba(255,255,255,0.18)", cb="rgba(255,255,255,0.06)")
import json
if os.environ.get("THEME"):
    C.update(json.loads(os.environ["THEME"]))

def base_css(px):
    return f"""{FONTS}
#root{{position:relative;width:100%;height:100%;overflow:hidden;font-family:'Pretendard',sans-serif;color:{C['t']};}}
.{px}-bg{{position:absolute;inset:0;background:{C['bg']};}}
.{px}-abs{{position:absolute;}}
.{px}-eyebrow{{position:absolute;left:60px;top:120px;font-size:34px;font-weight:700;letter-spacing:0.08em;color:{C['p']};}}
.{px}-tag{{position:absolute;right:60px;top:108px;padding:12px 28px;border-radius:100px;background:{C['al']};color:{C['p']};font-size:30px;font-weight:700;}}
.{px}-track{{position:absolute;left:60px;right:60px;top:1556px;height:6px;border-radius:6px;background:{C['al']};}}
.{px}-fill{{position:absolute;left:0;top:0;height:6px;border-radius:6px;background:{C['p']};transform-origin:left center;}}
.{px}-card{{position:absolute;background:{C['cb']};border:1.5px solid {C['bd']};border-radius:14px;}}
.{px}-pill{{position:absolute;border-radius:100px;background:{C['p']};color:{C['bg']};font-weight:800;white-space:nowrap;}}
.{px}-num{{position:absolute;left:60px;top:170px;font-size:190px;line-height:1;font-weight:900;color:{C['p']};letter-spacing:-0.04em;}}
.{px}-num-eyebrow{{position:absolute;left:330px;top:200px;font-size:40px;font-weight:700;letter-spacing:0.06em;color:{C['p']};}}
.{px}-num-sub{{position:absolute;left:330px;top:258px;font-size:34px;font-weight:600;color:{C['m']};}}
.{px}-title{{position:absolute;left:60px;right:60px;top:400px;font-size:92px;line-height:1.1;font-weight:900;letter-spacing:-0.02em;}}
.{px}-w{{display:inline-block;}}
"""

def chrome(px, n, eyebrow=None, tag=True):
    h = ""
    if eyebrow:
        h += f'<div class="{px}-eyebrow" id="{px}-eyebrow">{eyebrow}</div>'
    if tag:
        h += f'<div class="{px}-tag" id="{px}-tag">AA Canada</div>'
    h += f'<div class="{px}-track"><div class="{px}-fill" id="{px}-fill" style="width:{n/7*100:.3f}%"></div></div>'
    return h

def chrome_js(px, n):
    return f"""
tl.fromTo("#{px}-fill",{{scaleX:{(n-1)/n:.4f}}},{{scaleX:1,duration:0.8,ease:"power3.out"}},0.1);
"""

def words(px, key, text):
    return "".join(f'<span class="{px}-w {px}-{key}-w">{w}</span>' + (" " if i < len(text.split())-1 else "") for i, w in enumerate(text.split()))

def write(fid, n, css, html, js):
    px = "f%02d" % n
    d = DUR[fid]
    out = f"""<template>
<style>
{base_css(px)}
{css}
</style>
<div id="root" data-composition-id="{fid}" data-width="1080" data-height="1920" data-duration="{d}">
<div class="clip {px}-bg" id="{px}-bg" data-start="0" data-duration="{d}" data-track-index="0"></div>
{html}
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const fmt = (v) => String(Math.round(v)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ",");
{js}
window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""
    open(os.path.join(ROOT, "compositions/frames", fid + ".html"), "w").write(out)

E = "power3.out"

# ---------- Frame 1 — hook ----------
px = "f01"
css = f"""
.{px}-band{{position:absolute;left:-10%;top:0;width:120%;height:340px;background:{C['al']};clip-path:polygon(0 0,100% 0,100% 55%,0 100%);}}
.{px}-dots{{position:absolute;right:70px;top:150px;width:120px;height:120px;background-image:radial-gradient({C['am']} 7px,transparent 8px);background-size:40px 40px;}}
#{px}-l1{{position:absolute;left:0;right:0;top:470px;text-align:center;font-size:96px;font-weight:800;color:{C['m']};}}
#{px}-herowrap{{position:absolute;left:0;right:0;top:640px;height:280px;display:flex;justify-content:center;}}
#{px}-hero{{position:relative;font-size:236px;line-height:280px;font-weight:900;letter-spacing:-0.03em;color:{C['t']};}}
#{px}-strike{{position:absolute;left:-20px;right:-20px;top:136px;height:26px;border-radius:13px;background:{C['t']};transform-origin:left center;}}
#{px}-l3{{position:absolute;left:0;right:0;top:960px;text-align:center;font-size:116px;font-weight:900;color:{C['t']};}}
#{px}-again{{left:50%;top:1210px;margin-left:-230px;width:460px;height:116px;line-height:116px;text-align:center;font-size:56px;}}
"""
html = f"""<div class="{px}-band" id="{px}-band"></div><div class="{px}-dots"></div>
<div id="{px}-l1">{words(px,'l1','불어 때문에')}</div>
<div id="{px}-herowrap"><div id="{px}-hero">몬트리올<div id="{px}-strike"></div></div></div>
<div id="{px}-l3">빼셨나요?</div>
<div class="{px}-pill" id="{px}-again">다시 보세요</div>
{chrome(px,1)}"""
js = f"""
tl.fromTo("#{px}-band",{{yPercent:-100}},{{yPercent:0,duration:0.7,ease:"{E}"}},0);
tl.fromTo(".{px}-l1-w",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.45,stagger:0.35,ease:"{E}"}},0.0);
tl.fromTo("#{px}-hero",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.6,ease:"{E}"}},0.75);
tl.fromTo("#{px}-l3",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"{E}"}},1.55);
tl.fromTo("#{px}-strike",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power2.inOut"}},1.6);
tl.to("#{px}-hero",{{color:"{C['l']}",duration:0.3}},1.75);
tl.set("#{px}-strike",{{transformOrigin:"right center"}},2.6);
tl.to("#{px}-strike",{{scaleX:0,duration:0.45,ease:"power2.inOut"}},2.65);
tl.to("#{px}-hero",{{color:"{C['p']}",duration:0.35}},2.8);
tl.to("#{px}-hero",{{scale:1.06,duration:0.25,ease:"power2.out"}},2.8);
tl.to("#{px}-hero",{{scale:1,duration:0.35,ease:"{E}"}},3.05);
tl.fromTo("#{px}-again",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.4)"}},3.1);
""" + chrome_js(px,1)
write("01-hook", 1, css, html, js)

# ---------- Frame 2 — thesis ----------
px = "f02"
css = f"""
#{px}-cardA{{left:60px;right:60px;top:300px;height:400px;}}
#{px}-a1{{position:absolute;left:0;right:0;top:70px;text-align:center;font-size:150px;line-height:1;font-weight:900;color:{C['p']};letter-spacing:-0.03em;}}
#{px}-a2{{position:absolute;left:0;right:0;top:240px;text-align:center;font-size:104px;line-height:1;font-weight:800;}}
#{px}-arrow{{position:absolute;left:490px;top:722px;width:100px;height:120px;}}
#{px}-cardB{{left:60px;right:60px;top:862px;height:400px;}}
#{px}-b1{{position:absolute;left:0;right:0;top:66px;text-align:center;font-size:66px;font-weight:700;color:{C['m']};}}
#{px}-b2wrap{{position:absolute;left:0;right:0;top:190px;display:flex;justify-content:center;}}
#{px}-b2{{position:relative;font-size:120px;line-height:1.1;font-weight:900;letter-spacing:-0.02em;}}
#{px}-hl{{position:absolute;left:-6px;top:54%;width:calc(4em + 12px);height:36%;background:{C['am']};border-radius:8px;transform-origin:left center;}}
#{px}-b2t{{position:relative;}}
#{px}-badge{{left:50%;top:1340px;margin-left:-420px;width:840px;height:130px;line-height:130px;text-align:center;font-size:58px;}}
"""
html = f"""{chrome(px,2,'WHY MONTRÉAL')}
<div class="{px}-card" id="{px}-cardA"><div id="{px}-a1">캐나다 2위</div><div id="{px}-a2">대도시</div></div>
<svg id="{px}-arrow" viewBox="0 0 100 120"><path id="{px}-arrowp" d="M50 6 V100 M18 70 L50 104 L82 70" fill="none" stroke="{C['p']}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="{px}-card" id="{px}-cardB"><div id="{px}-b1">그런데 생활비는</div><div id="{px}-b2wrap"><div id="{px}-b2"><div id="{px}-hl"></div><span id="{px}-b2t">중소도시 수준</span></div></div></div>
<div class="{px}-pill" id="{px}-badge">자녀 무상교육 가성비 No.1</div>"""
js = chrome_js(px,2) + f"""
tl.fromTo("#{px}-eyebrow",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.5,ease:"{E}"}},0);
tl.fromTo("#{px}-tag",{{opacity:0}},{{opacity:1,duration:0.5}},0);
tl.fromTo("#{px}-cardA",{{y:120,opacity:0}},{{y:0,opacity:1,duration:0.6,ease:"{E}"}},0.05);
tl.fromTo("#{px}-a1",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"{E}"}},0.95);
tl.fromTo("#{px}-a2",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"{E}"}},1.75);
const ap = document.getElementById("{px}-arrowp"); const al = 230;
ap.style.strokeDasharray = al;
tl.fromTo(ap,{{strokeDashoffset:al}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut"}},2.1);
tl.fromTo("#{px}-cardB",{{y:120,opacity:0}},{{y:0,opacity:1,duration:0.6,ease:"{E}"}},2.35);
tl.fromTo("#{px}-b1",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"{E}"}},2.5);
tl.fromTo("#{px}-b2",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"{E}"}},2.95);
tl.fromTo("#{px}-hl",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},3.35);
tl.fromTo("#{px}-badge",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.5,ease:"back.out(1.5)"}},5.35);
"""
write("02-thesis", 2, css, html, js)

def list_head(px, num, eb, sub, title):
    return (f'<div class="{px}-num" id="{px}-num">{num}</div><div class="{px}-num-eyebrow" id="{px}-ne">{eb}</div>'
            f'<div class="{px}-num-sub" id="{px}-ns">{sub}</div><div class="{px}-title" id="{px}-title">{words(px,"t",title)}</div>')
def list_head_js(px, t_title):
    return f"""
tl.fromTo("#{px}-tag",{{opacity:0}},{{opacity:1,duration:0.4}},0);
tl.fromTo("#{px}-num",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.55,ease:"{E}"}},0);
tl.fromTo(["#{px}-ne","#{px}-ns"],{{x:-30,opacity:0}},{{x:0,opacity:1,duration:0.45,stagger:0.12,ease:"{E}"}},0.15);
tl.fromTo(".{px}-t-w",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.45,stagger:0.18,ease:"{E}"}},{t_title});
"""

CHECK = f'<svg viewBox="0 0 40 40" width="40" height="40"><path d="M10 21 L17 28 L30 13" fill="none" stroke="{C["bg"]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------- Frame 3 — college ----------
px = "f03"
css = f"""
#{px}-parent{{left:60px;right:60px;top:560px;height:190px;}}
#{px}-child{{left:60px;right:60px;top:880px;height:170px;}}
.{px}-nodelabel{{position:absolute;left:40px;top:0;height:100%;display:flex;align-items:center;gap:20px;font-size:60px;font-weight:900;}}
.{px}-ico{{width:84px;height:84px;border-radius:50%;background:{C['al']};display:flex;align-items:center;justify-content:center;}}
.{px}-chips{{position:absolute;right:30px;top:0;height:100%;display:flex;flex-direction:column;justify-content:center;gap:14px;}}
.{px}-chip{{padding:10px 30px;border-radius:100px;background:{C['al']};color:{C['p']};font-size:44px;font-weight:800;text-align:center;}}
#{px}-arrow{{position:absolute;left:500px;top:758px;width:80px;height:118px;}}
#{px}-free{{right:30px;top:42px;height:86px;line-height:86px;padding:0 36px;font-size:46px;}}
.{px}-ben{{left:60px;right:60px;height:118px;display:flex;align-items:center;gap:28px;padding-left:34px;font-size:56px;font-weight:800;}}
.{px}-step{{width:64px;height:64px;border-radius:50%;background:{C['p']};display:flex;align-items:center;justify-content:center;flex:none;}}
"""
PERSON = f'<svg viewBox="0 0 48 48" width="52" height="52"><circle cx="24" cy="16" r="9" fill="{C["p"]}"/><path d="M8 44c0-9 7-15 16-15s16 6 16 15z" fill="{C["p"]}"/></svg>'
KID = f'<svg viewBox="0 0 48 48" width="46" height="46"><circle cx="24" cy="18" r="8" fill="{C["p"]}"/><path d="M12 44c0-7 5-12 12-12s12 5 12 12z" fill="{C["p"]}"/></svg>'
bens = [("학비 저렴",1090,5.75),("학업 부담 적당",1240,7.15),("등하교 케어 OK",1390,8.85)]
html = f"""{chrome(px,3)}
{list_head(px,'01','장점 ①','부모 학교 등록','자녀 공립 무상교육')}
<div class="{px}-card" id="{px}-parent"><div class="{px}-nodelabel"><div class="{px}-ico">{PERSON}</div>부모</div>
<div class="{px}-chips"><div class="{px}-chip" id="{px}-c1">사설어학원</div><div class="{px}-chip" id="{px}-c2">사립컬리지</div></div></div>
<svg id="{px}-arrow" viewBox="0 0 80 118"><path id="{px}-arrowp" d="M40 6 V100 M14 74 L40 104 L66 74" fill="none" stroke="{C['p']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="{px}-card" id="{px}-child"><div class="{px}-nodelabel"><div class="{px}-ico">{KID}</div>자녀</div><div class="{px}-pill" id="{px}-free">공립학교 무상교육</div></div>
""" + "".join(f'<div class="{px}-card {px}-ben" id="{px}-b{i}" style="top:{y}px"><div class="{px}-step">{CHECK}</div>{t}</div>' for i,(t,y,_) in enumerate(bens))
js = chrome_js(px,3) + list_head_js(px,0.35) + f"""
tl.fromTo("#{px}-parent",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.55,ease:"{E}"}},1.0);
tl.fromTo("#{px}-c1",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.6)"}},1.2);
tl.fromTo("#{px}-c2",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.6)"}},2.2);
const ap = document.getElementById("{px}-arrowp"); ap.style.strokeDasharray = 220;
tl.fromTo(ap,{{strokeDashoffset:220}},{{strokeDashoffset:0,duration:0.55,ease:"power2.inOut"}},3.5);
tl.fromTo("#{px}-child",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.55,ease:"{E}"}},3.8);
tl.fromTo("#{px}-free",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.5)"}},4.5);
""" + "".join(f'tl.fromTo("#{px}-b{i}",{{x:-120,opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"{E}"}},{t});\n' for i,(_,_,t) in enumerate(bens))
write("03-college", 3, css, html, js)

# ---------- Frame 4 — big city (user's population chart image) ----------
px = "f04"
# window shows the chart part of population-chart.png (native 1081x608; chart starts at x=270)
W4, H4 = 1000, 750
K4 = W4 / 811                      # overview scale: native x 270..1081 fills the window
ZX4, ZY4, ZS4 = 610, 88, 1.65       # Montréal row (native) and zoom scale
css = f"""
#{px}-win{{position:absolute;left:40px;top:520px;width:{W4}px;height:{H4}px;overflow:hidden;border-radius:14px;border:1.5px solid {C['bd']};background:#fff;}}
#{px}-stage{{position:absolute;left:0;top:0;width:1081px;height:608px;transform-origin:0 0;}}
#{px}-img{{position:absolute;left:0;top:0;width:1081px;height:608px;display:block;}}
.{px}-dim{{position:absolute;background:#ffffff;}}
#{px}-hl{{position:absolute;left:0;top:0;width:1081px;height:608px;overflow:visible;}}
#{px}-rank{{left:870px;top:540px;height:64px;line-height:64px;padding:0 26px;font-size:38px;}}
#{px}-statwrap{{position:absolute;left:60px;right:60px;top:1278px;height:130px;display:flex;align-items:baseline;justify-content:center;gap:20px;}}
#{px}-statlab{{font-size:50px;font-weight:800;color:{C['m']};}}
#{px}-stat{{display:inline-block;font-size:128px;line-height:1;font-weight:900;color:{C['p']};font-variant-numeric:tabular-nums;transform-origin:center bottom;}}
#{px}-statu{{font-size:72px;font-weight:900;color:{C['p']};}}
.{px}-chip{{top:1420px;width:300px;height:116px;display:flex;align-items:center;justify-content:center;gap:14px;font-size:42px;font-weight:800;}}
"""
ICONS = {
 "교육수준": f'<svg viewBox="0 0 48 48" width="52" height="52"><path d="M4 18 L24 8 L44 18 L24 28 Z" fill="{C["p"]}"/><path d="M12 23 V33 C12 37 36 37 36 33 V23 L24 29 Z" fill="{C["p"]}" opacity="0.7"/></svg>',
 "생활편의": f'<svg viewBox="0 0 48 48" width="52" height="52"><path d="M6 10 H12 L17 32 H38 L42 16 H14" fill="none" stroke="{C["p"]}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/><circle cx="19" cy="40" r="3.5" fill="{C["p"]}"/><circle cx="35" cy="40" r="3.5" fill="{C["p"]}"/></svg>',
 "문화환경": f'<svg viewBox="0 0 48 48" width="52" height="52"><path d="M18 34 V10 L40 6 V30" fill="none" stroke="{C["p"]}" stroke-width="4.5" stroke-linejoin="round"/><ellipse cx="13" cy="35" rx="6" ry="5" fill="{C["p"]}"/><ellipse cx="35" cy="31" rx="6" ry="5" fill="{C["p"]}"/></svg>',
}
chips = [("교육수준",60,5.35),("생활편의",390,6.45),("문화환경",720,7.35)]
html = f"""{chrome(px,4)}
{list_head(px,'02','장점 ②','도시별 인구 (천 명)','캐나다 2위 대도시')}
<div id="{px}-win"><div id="{px}-stage">
<img id="{px}-img" src="assets/images/population-chart.png" alt="캐나다 주요 도시별 인구"/>
<div class="{px}-dim" id="{px}-dimA" style="left:0;top:0;width:1081px;height:64px"></div>
<div class="{px}-dim" id="{px}-dimB" style="left:0;top:112px;width:1081px;height:496px"></div>
<svg id="{px}-hl" viewBox="0 0 1081 608"><rect id="{px}-hlr" x="322" y="64" width="578" height="48" rx="12" fill="none" stroke="{C['p']}" stroke-width="5"/></svg>
</div></div>
<div class="{px}-pill" id="{px}-rank">2위</div>
<div id="{px}-statwrap"><span id="{px}-statlab">인구 약</span><span id="{px}-stat">0</span><span id="{px}-statu">만</span></div>
""" + "".join(f'<div class="{px}-card {px}-chip" id="{px}-ch{i}" style="left:{x}px">{ICONS[t]}{t}</div>' for i,(t,x,_) in enumerate(chips))
zx = max(W4 - 1081*ZS4, min(0, W4/2 - ZX4*ZS4)); zy = max(H4 - 608*ZS4, min(0, H4/2 - ZY4*ZS4))
js = chrome_js(px,4) + list_head_js(px,0.6) + f"""
tl.fromTo("#{px}-win",{{clipPath:"inset(0% 0% 100% 0% round 14px)"}},{{clipPath:"inset(0% 0% 0% 0% round 14px)",duration:0.8,ease:"power2.inOut"}},1.45);
tl.fromTo("#{px}-stage",{{x:{-270*K4:.1f},y:24,scale:{K4*0.96:.4f}}},{{x:{-270*K4:.1f},y:0,scale:{K4:.4f},duration:0.85,ease:"{E}"}},1.45);
tl.fromTo(".{px}-dim",{{opacity:0}},{{opacity:0.72,duration:0.5,ease:"power2.out"}},2.45);
tl.to("#{px}-stage",{{x:{zx:.1f},y:{zy:.1f},scale:{ZS4},duration:0.9,ease:"power3.inOut"}},2.35);
const hr = document.getElementById("{px}-hlr"); const hp = 2*(578+48);
hr.style.strokeDasharray = hp;
tl.fromTo(hr,{{strokeDashoffset:hp}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut"}},2.9);
tl.fromTo("#{px}-rank",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.6)"}},3.0);
tl.fromTo("#{px}-statwrap",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"{E}"}},2.5);
const st = {{v:0}}; const se = document.getElementById("{px}-stat");
tl.fromTo(st,{{v:0}},{{v:460,duration:1.3,ease:"power2.out",onUpdate:()=>{{se.textContent=fmt(st.v);}}}},2.6);
tl.fromTo(se,{{scale:0.55}},{{scale:1,duration:1.3,ease:"power2.out",immediateRender:false}},2.6);
tl.to("#{px}-stage",{{x:{-270*K4:.1f},y:0,scale:{K4:.4f},duration:1.0,ease:"power3.inOut"}},4.8);
tl.to("#{px}-rank",{{opacity:0,duration:0.3}},4.8);
tl.to(".{px}-dim",{{opacity:0.55,duration:0.6}},4.9);
""" + "".join(f'tl.fromTo("#{px}-ch{i}",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"{E}"}},{t});\n' for i,(_,_,t) in enumerate(chips))
write("04-big-city", 4, css, html, js)

# ---------- Frame 5 — rent (user's Statistics Canada image) ----------
px = "f05"
W5, H5 = 960, 900
K5 = W5 / 1054
OVY = -100                          # overview: native y ~110..1098 (title + map)
CITIES = [("van",122,822,2.0,1.95),("tor",895,1027,2.0,3.75),("mtl",650,762,2.3,5.5)]
def tgt(cx, cy, sc):
    return (max(W5 - 1054*sc, min(0, W5/2 - cx*sc)), max(H5 - 1349*sc, min(0, H5/2 - cy*sc)))
css = f"""
#{px}-win{{position:absolute;left:60px;top:500px;width:{W5}px;height:{H5}px;overflow:hidden;border-radius:14px;border:1.5px solid {C['bd']};background:#f2f2f2;}}
#{px}-stage{{position:absolute;left:0;top:0;width:1054px;height:1349px;transform-origin:0 0;}}
#{px}-img{{position:absolute;left:0;top:0;width:1054px;height:1349px;display:block;}}
#{px}-rings{{position:absolute;left:0;top:0;width:1054px;height:1349px;overflow:visible;}}
#{px}-badge{{left:50%;top:1424px;margin-left:-440px;width:880px;height:112px;line-height:112px;text-align:center;font-size:52px;}}
#{px}-ns{{color:{C['m']};}}
"""
html = f"""{chrome(px,5)}
{list_head(px,'03','장점 ③','출처: Statistics Canada · 2026년 2분기','가성비')}
<div id="{px}-win"><div id="{px}-stage">
<img id="{px}-img" src="assets/images/statcan-rent-2026q2.jpg" alt="Statistics Canada 2베드룸 평균 렌트 2026년 2분기"/>
<svg id="{px}-rings" viewBox="0 0 1054 1349">
<rect id="{px}-r-van" x="20" y="758" width="204" height="128" rx="18" fill="none" stroke="#0e1a3a" stroke-width="6"/>
<rect id="{px}-r-tor" x="793" y="963" width="204" height="128" rx="18" fill="none" stroke="#0e1a3a" stroke-width="6"/>
<rect id="{px}-r-mtlg" x="540" y="690" width="220" height="144" rx="22" fill="{C['am']}" stroke="none"/>
<rect id="{px}-r-mtl" x="548" y="698" width="204" height="128" rx="18" fill="none" stroke="{C['p']}" stroke-width="9"/>
</svg>
</div></div>
<div class="{px}-pill" id="{px}-badge">3대 대도시 중 압도적으로 저렴</div>"""
js = chrome_js(px,5) + list_head_js(px,0.45) + f"""
tl.fromTo("#{px}-win",{{clipPath:"inset(0% 0% 100% 0% round 14px)"}},{{clipPath:"inset(0% 0% 0% 0% round 14px)",duration:0.8,ease:"power2.inOut"}},0.7);
tl.fromTo("#{px}-stage",{{x:0,y:{OVY+30},scale:{K5*0.96:.4f}}},{{x:0,y:{OVY},scale:{K5:.4f},duration:1.1,ease:"{E}"}},0.7);
"""
for key,cx,cy,sc,t in CITIES:
    zx,zy = tgt(cx,cy,sc)
    per = 2*(204+128)
    js += f'tl.to("#{px}-stage",{{x:{zx:.1f},y:{zy:.1f},scale:{sc},duration:0.75,ease:"power3.inOut"}},{t});\n'
    js += f'(function(){{const r=document.getElementById("{px}-r-{key}"); r.style.strokeDasharray={per}; tl.fromTo(r,{{strokeDashoffset:{per}}},{{strokeDashoffset:0,duration:0.55,ease:"power2.inOut"}},{t+0.6});}})();\n'
js += f"""
tl.fromTo("#{px}-r-mtlg",{{opacity:0,scale:0.85,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.5,ease:"{E}"}},6.25);
tl.to("#{px}-stage",{{x:0,y:{OVY},scale:{K5:.4f},duration:1.0,ease:"power3.inOut"}},7.75);
tl.fromTo("#{px}-badge",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.5,ease:"back.out(1.5)"}},8.55);
"""
write("05-rent", 5, css, html, js)

# ---------- Frame 6 — landing ----------
px = "f06"
css = f"""
.{px}-ring{{position:absolute;left:50%;top:960px;border-radius:50%;border:2px solid {C['am']};}}
#{px}-l1{{position:absolute;left:0;right:0;top:470px;text-align:center;font-size:76px;font-weight:800;}}
#{px}-l2{{position:absolute;left:0;right:0;top:580px;text-align:center;font-size:76px;font-weight:800;}}
#{px}-l2 b{{color:{C['p']};font-weight:900;}}
#{px}-hero{{position:absolute;left:0;right:0;top:820px;text-align:center;font-size:236px;line-height:1.1;font-weight:900;color:{C['p']};letter-spacing:-0.03em;}}
"""
html = "".join(f'<div class="{px}-ring" style="width:{d}px;height:{d}px;margin-left:-{d//2}px;margin-top:-{d//2}px"></div>' for d in (420,640,860,1080)) + f"""
<div id="{px}-l1">교육과 경험은 대도시답게</div>
<div id="{px}-l2">비용은 <b>가볍게</b></div>
<div id="{px}-hero">몬트리올</div>
{chrome(px,6)}"""
js = chrome_js(px,6) + f"""
tl.fromTo(".{px}-ring",{{scale:0.85,opacity:0}},{{scale:1,opacity:1,duration:1.2,stagger:0.12,ease:"{E}"}},0);
tl.fromTo("#{px}-l1",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.6,ease:"{E}"}},0.05);
tl.fromTo("#{px}-l2",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.6,ease:"{E}"}},2.05);
tl.fromTo("#{px}-hero",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.7,ease:"{E}"}},3.3);
"""
write("06-landing", 6, css, html, js)

# ---------- Frame 7 — CTA ----------
px = "f07"
css = f"""
.{px}-band{{position:absolute;left:-10%;bottom:0;width:120%;height:420px;background:{C['al']};clip-path:polygon(0 45%,100% 0,100% 100%,0 100%);}}
.{px}-dots{{position:absolute;left:70px;top:170px;width:120px;height:120px;background-image:radial-gradient({C['am']} 7px,transparent 8px);background-size:40px 40px;}}
#{px}-line{{position:absolute;left:510px;top:580px;width:60px;height:4px;border-radius:2px;background:{C['p']};}}
#{px}-mark{{position:absolute;left:0;right:0;top:630px;text-align:center;font-size:172px;line-height:1.1;font-weight:900;letter-spacing:-0.03em;white-space:nowrap;}}
.{px}-ch{{display:inline-block;}}
.{px}-aa{{color:{C['p']};}}
#{px}-sub{{position:absolute;left:0;right:0;top:860px;text-align:center;font-size:58px;font-weight:700;color:{C['m']};}}
#{px}-cta{{left:50%;top:1010px;margin-left:-410px;width:820px;height:128px;line-height:128px;text-align:center;font-size:52px;}}
"""
mark = "".join(f'<span class="{px}-ch{" "+px+"-aa" if i<2 else ""}">{"&nbsp;" if c==" " else c}</span>' for i,c in enumerate("AA Canada"))
html = f"""<div class="{px}-band"></div><div class="{px}-dots"></div>
<div id="{px}-line"></div><div id="{px}-mark">{mark}</div>
<div id="{px}-sub">몬트리올 자녀무상교육 전문</div>
<div class="{px}-pill" id="{px}-cta">프로필 링크에서 상담 신청 →</div>
{chrome(px,7,tag=False)}"""
js = chrome_js(px,7) + f"""
tl.fromTo("#{px}-line",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"{E}"}},0);
tl.fromTo(".{px}-ch",{{y:90,opacity:0,rotation:8}},{{y:0,opacity:1,rotation:0,duration:0.5,stagger:0.06,ease:"{E}"}},0.05);
tl.fromTo("#{px}-sub",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"{E}"}},0.7);
tl.fromTo("#{px}-cta",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.5)"}},1.3);
tl.to("#{px}-cta",{{scale:0.95,duration:0.12,ease:"power2.in"}},2.8);
tl.to("#{px}-cta",{{scale:1,duration:0.35,ease:"back.out(2)"}},2.92);
"""
write("07-cta", 7, css, html, js)
print("frames written:", sorted(DUR))
