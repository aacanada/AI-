"""Shared CSS/JS for the Olds Agribusiness long-form scenes (from the SGA long-form pipeline). Every scene is a self-contained sub-composition
(no brand chrome / captions inside) so shorts can reuse it."""
import re

FONTS = """
@font-face{font-family:Pretendard;font-weight:500;src:url(assets/fonts/Pretendard-Medium.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:700;src:url(assets/fonts/Pretendard-Bold.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:800;src:url(assets/fonts/Pretendard-ExtraBold.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:900;src:url(assets/fonts/Pretendard-Black.woff2) format("woff2")}
"""

DEEP, DEEP2, OLDS, RED, GOLD, CREAM = "#0f3d2e", "#14563f", "#00b373", "#c8102e", "#e8b931", "#f5efe3"

# R is replaced by #<scene id>. Never give a GSAP-tweened node a CSS transform.
BASE_CSS = """
R{position:absolute;inset:0;overflow:hidden;color:#fff;font-family:Pretendard,sans-serif}
R *{box-sizing:border-box}
R .bg{position:absolute;inset:0;background:linear-gradient(135deg,#0f3d2e 0%,#124a37 55%,#14563f 100%)}
R .blob{position:absolute;border-radius:50%;width:1100px;height:1100px}
R .blob.a{left:-300px;top:-420px;background:radial-gradient(circle,rgba(0,179,115,.32) 0%,rgba(0,179,115,0) 68%)}
R .blob.b{left:1050px;top:380px;background:radial-gradient(circle,rgba(0,179,115,.16) 0%,rgba(0,179,115,0) 66%)}
R .blob.c{left:500px;top:520px;width:900px;height:900px;background:radial-gradient(circle,rgba(232,185,49,.12) 0%,rgba(232,185,49,0) 66%)}
R .stage{position:absolute;inset:0}
R .abs{position:absolute}
R .h{font-weight:900;letter-spacing:-.03em;line-height:1.08}
R .hd{font-weight:800;letter-spacing:-.02em;line-height:1.2}
R .b{font-weight:500;line-height:1.45}
R .l{font-weight:700;letter-spacing:.14em}
R .num{font-weight:900;letter-spacing:-.04em;line-height:1;font-variant-numeric:tabular-nums}
R .gold{color:#e8b931}
R .red{color:#c8102e}
R .full{position:absolute;inset:0;overflow:hidden}
R .full img,R .ph img{display:block;width:100%;height:100%;object-fit:cover}
R .dim{position:absolute;inset:0;background:#082a1f}
R .ph{position:absolute;overflow:hidden;border-radius:22px;box-shadow:0 24px 50px rgba(0,0,0,.38);background:#082a1f}
R .ph.frame{border:6px solid #f5efe3}
R .ph .lab{position:absolute;left:0;right:0;bottom:0;padding:14px 20px;background:linear-gradient(0deg,rgba(6,30,22,.88),rgba(6,30,22,0));font-weight:800;font-size:28px}
R .card{position:absolute;background:#f5efe3;color:#0f3d2e;border-radius:28px;box-shadow:0 22px 46px rgba(0,0,0,.30)}
R .card .t{font-weight:800;color:#0f3d2e}
R .chip{position:absolute;white-space:nowrap;border-radius:99px;padding:12px 28px;font-weight:700;font-size:30px;background:rgba(255,255,255,.08);border:2px solid rgba(232,185,49,.75);color:#fff}
R .chip.cream{background:#f5efe3;border-color:#f5efe3;color:#0f3d2e}
R .chip.gold{background:#e8b931;border-color:#e8b931;color:#0f3d2e}
R .chip.red{background:#c8102e;border-color:#c8102e;color:#fff}
R .chip.green{background:#00b373;border-color:#00b373;color:#0f3d2e}
R .chip.gray{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.35);color:rgba(255,255,255,.85)}
R .chip.rel{position:relative}
R .chip.navy{background:#0f3d2e;border-color:#0f3d2e;color:#f5efe3}
R .pill{position:absolute;white-space:nowrap;border-radius:99px;padding:10px 26px;font-weight:800;font-size:28px;background:#e8b931;color:#0f3d2e}
R .sweep{position:absolute;top:-20%;bottom:-20%;left:0;width:34%;background:linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.38) 50%,rgba(255,255,255,0) 100%);mix-blend-mode:screen}
R .reel{display:inline-block;height:1em;overflow:hidden;vertical-align:top}
R .strip{display:block}
R .strip i{display:block;height:1em;font-style:normal}
R .ch{display:inline-block;white-space:pre}
R .tag{position:absolute;font-weight:700;font-size:22px;letter-spacing:.12em;padding:6px 16px;border-radius:8px;background:#c8102e;color:#fff}
R svg{overflow:visible}
R .grp{position:absolute;inset:0}
R .flow{position:absolute;display:flex;flex-wrap:wrap;gap:22px}
R .row{position:absolute;display:flex;align-items:center;gap:26px;font-weight:800;color:#0f3d2e;white-space:nowrap}
R .row svg{flex:none}
R .ar path{fill:none;stroke:#e8b931;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
"""

JS_HELPERS = r"""
const q=s=>root.querySelector(s), qa=s=>Array.from(root.querySelectorAll(s));
const tl=gsap.timeline({paused:true});
const E=el=>typeof el==='string'?qa(el):el, E1=el=>typeof el==='string'?q(el):el;
function inn(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,x:o.x||0,y:(o.y===undefined?30:o.y),scale:(o.s===undefined?1:o.s),rotation:(o.r0===undefined?(o.r||0):o.r0)},
  {opacity:1,x:0,y:0,scale:1,rotation:o.r||0,duration:o.d||0.6,ease:o.e||'power3.out',stagger:o.st||0},at);}
function outt(el,at,o){o=o||{};tl.to(E(el),{opacity:o.o||0,y:o.y||0,x:o.x||0,scale:(o.s===undefined?1:o.s),duration:o.d||0.4,ease:'power2.in'},at);}
function kb(el,at,dur,a,b){a=a||{};b=b||{};
  tl.fromTo(E(el),{scale:a.s||1,xPercent:a.x||0,yPercent:a.y||0},{scale:b.s||1.10,xPercent:b.x||0,yPercent:b.y||0,duration:Math.max(0.1,dur),ease:'none'},at);}
function shake(at){const s=q('.stage');tl.to(s,{x:12,y:-7,duration:1/30,ease:'none'},at);tl.to(s,{x:-9,y:6,duration:1/30,ease:'none'},at+1/30);tl.to(s,{x:0,y:0,duration:1/30,ease:'none'},at+2/30);}
function slam(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,scale:o.s||2.2},{opacity:1,scale:1,duration:o.d||0.42,ease:'power4.in'},at);if(o.shake!==false)shake(at+(o.d||0.42));}
function stamp(el,at,rot){rot=(rot===undefined?-12:rot);tl.fromTo(E(el),{opacity:0,scale:3,rotation:rot},{opacity:1,scale:1,rotation:rot,duration:0.32,ease:'power4.in'},at);shake(at+0.32);}
function pop(el,at,st){tl.fromTo(E(el),{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.42,ease:'back.out(2.2)',stagger:(st===undefined?0.08:st)},at);}
function flip(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,rotationY:o.r0||-90,transformPerspective:1400},{opacity:1,rotationY:0,transformPerspective:1400,duration:o.d||0.7,ease:'power3.out',stagger:o.st||0},at);}
function draw(path,at,d,e){const ps=typeof path==='string'?qa(path):[path];ps.forEach(p=>{const L=p.getTotalLength();p.style.strokeDasharray=L+' '+L;
  tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:d||0.9,ease:e||'power2.inOut'},at);});}
function grow(el,at,d,origin,axis){tl.fromTo(E(el),axis==='y'?{scaleY:0,transformOrigin:origin||'50% 100%'}:{scaleX:0,transformOrigin:origin||'0% 50%'},axis==='y'?{scaleY:1,duration:d||0.7,ease:'power3.out'}:{scaleX:1,duration:d||0.7,ease:'power3.inOut'},at);}
function mask(el,at,d,dir){const from={l:'inset(0% 100% 0% 0%)',r:'inset(0% 0% 0% 100%)',u:'inset(100% 0% 0% 0%)',d:'inset(0% 0% 100% 0%)'}[dir||'l'];
  tl.fromTo(E(el),{clipPath:from,opacity:1},{clipPath:'inset(0% 0% 0% 0%)',opacity:1,duration:d||0.8,ease:'power3.inOut'},at);}
function sweep(el,at){tl.fromTo(E(el),{xPercent:-140,opacity:1},{xPercent:330,opacity:1,duration:1.1,ease:'power2.inOut'},at);}
function kin(el,at,st){el=E1(el);const t=el.textContent;el.textContent='';
  for(const c of t){const s=document.createElement('span');s.className='ch';s.textContent=c;el.appendChild(s);}
  tl.fromTo(el.querySelectorAll('.ch'),{opacity:0,rotationX:90,transformPerspective:700,filter:'blur(12px)'},
    {opacity:1,rotationX:0,transformPerspective:700,filter:'blur(0px)',duration:0.55,ease:'power3.out',stagger:st||0.03},at);}
function odo(el,at,dur){el=E1(el);const t=el.textContent;el.textContent='';const reels=[];let k=0;
  for(const c of t){if(c>='0'&&c<='9'){const d=+c,r=document.createElement('span');r.className='reel';const s=document.createElement('span');s.className='strip';
      const n=10+d+1;for(let i=0;i<n;i++){const x=document.createElement('i');x.textContent=String(i%10);s.appendChild(x);}r.appendChild(s);el.appendChild(r);reels.push([s,n,k++]);}
    else{const s=document.createElement('span');s.textContent=c;el.appendChild(s);}}
  const m=reels.length;reels.forEach(([s,n,i])=>tl.fromTo(s,{yPercent:0},{yPercent:-100*(n-1)/n,duration:(dur||1.4)*(0.65+0.35*(i+1)/m),ease:'power3.out'},at));}
function ambient(){
  qa('.blob').forEach((g,i)=>tl.fromTo(g,{x:0,y:0},{x:(i%2?-140:160),y:(i%2?90:-70),duration:D,ease:'sine.inOut'},0));
  tl.fromTo(q('.stage'),{scale:1,transformOrigin:'50% 48%'},{scale:1.025,duration:D,ease:'none'},0);
}
"""

T_RE = re.compile(r"T\('([^']*)'\)")


def scene_html(cid, duration, css, body, js, bg_extra="", audio=""):
    css_all = (BASE_CSS + css).replace("R ", f"#{cid} ").replace("R{", f"#{cid}{{")
    return f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{FONTS}
{css_all}
      </style>
      <div id="{cid}" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{duration}">
        <div class="bg"></div>
        <div class="blob a"></div><div class="blob b"></div><div class="blob c"></div>
{bg_extra}
        <div class="stage">
{body}
        </div>
{audio}
      </div>
      <script>
        (function () {{
          const root = document.getElementById("{cid}");
          const D = {duration};
{JS_HELPERS}
{js}
          ambient();
          window.__timelines["{cid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""


# ------------------------------------------------------------------ shared graphics (reused by future shorts)
def check(cid, size=56, color="#00b373"):
    """Rounded check box; draw('#<cid>') animates the tick."""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 56 56"><rect x="3" y="3" width="50" height="50" rx="12" fill="none" '
            f'stroke="{color}" stroke-width="5"/><path id="{cid}" d="M14 29 L24 39 L43 18" fill="none" stroke="{color}" '
            f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def arrow(cid, x, y, w, h=60, d=None):
    """Gold arrow (shaft + head) drawn left->right; draw('#<cid>')."""
    d = d or f"M6 {h / 2} L{w - 10} {h / 2} M{w - 34} {h / 2 - 22} L{w - 8} {h / 2} L{w - 34} {h / 2 + 22}"
    return (f'<svg class="abs ar" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" viewBox="0 0 {w} {h}">'
            f'<path id="{cid}" d="{d}"/></svg>')


# Simplified Alberta silhouette (viewBox 400x600 = 120W..110W, 60N..49N). Not to scale; no distances shown.
AB_PATH = "M40 4 L400 4 L400 600 L254 600 L246 572 L231 545 L210 520 L191 490 L165 462 L137 436 L112 410 L90 381 L62 360 L40 338 Z"
AB_CITY = {"Edmonton": (274, 354), "Red Deer": (263, 421), "Innisfail": (258, 434), "Olds": (252, 447), "Calgary": (253, 488)}


def ab_map(cid, x, y, w, cities=("Edmonton", "Calgary"), olds=True):
    """Alberta outline + city dots (ids <cid>-out, <cid>-d<i>, <cid>-pin). h = 1.5 w."""
    k = w / 400
    dots = "".join(
        f'<div class="abs" id="{cid}-d{i}" style="left:{AB_CITY[c][0] * k - 9}px;top:{AB_CITY[c][1] * k - 9}px;width:18px;height:18px;border-radius:50%;background:#f5efe3"></div>'
        f'<div class="abs hd" id="{cid}-n{i}" style="left:{AB_CITY[c][0] * k + 18}px;top:{AB_CITY[c][1] * k - 20}px;font-size:26px;color:rgba(255,255,255,.85);white-space:nowrap">{c}</div>'
        for i, c in enumerate(cities))
    pin = ""
    if olds:
        ox, oy = AB_CITY["Olds"]
        pin = (f'<div class="abs" id="{cid}-pin" style="left:{ox * k - 30}px;top:{oy * k - 78}px;width:60px;height:80px">'
               f'<svg width="60" height="80" viewBox="0 0 60 80"><path d="M30 78 C30 78 4 46 4 30 A26 26 0 1 1 56 30 C56 46 30 78 30 78 Z" fill="#e8b931"/>'
               f'<circle cx="30" cy="30" r="10" fill="#0f3d2e"/></svg></div>'
               f'<div class="abs h" id="{cid}-pl" style="left:{ox * k - 150}px;top:{oy * k - 30}px;font-size:34px;color:#e8b931;white-space:nowrap">Olds</div>')
    return (f'<div class="abs" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{w * 1.5}px">'
            f'<svg class="abs" style="left:0;top:0;width:{w}px;height:{w * 1.5}px" viewBox="0 0 400 600">'
            f'<path id="{cid}-fill" d="{AB_PATH}" fill="rgba(0,179,115,.16)"/>'
            f'<path id="{cid}-out" d="{AB_PATH}" fill="none" stroke="#00b373" stroke-width="5" stroke-linejoin="round"/></svg>'
            f'{dots}{pin}</div>')


# Deterministic particle burst (gold). Only the S01 title, the AOS key beat and the closing CTA use it.
PARTICLES_JS = r"""
function burst(host,at,n,cx,cy,spread,seed){const H=E1(host);seed=seed||7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
  for(let i=0;i<n;i++){const d=document.createElement('div');d.style.cssText='position:absolute;width:12px;height:12px;border-radius:50%;background:#e8b931;opacity:0;left:'+cx+'px;top:'+cy+'px';H.appendChild(d);
    const a=rnd()*Math.PI*2,r=spread*(0.4+rnd()*0.8);
    tl.fromTo(d,{x:0,y:0,opacity:1,scale:0.6+rnd()},{x:Math.cos(a)*r,y:Math.sin(a)*r*0.6+60,opacity:0,duration:1.2+rnd()*0.7,ease:'power3.out',immediateRender:false},at);}}
"""
JS_HELPERS += PARTICLES_JS
