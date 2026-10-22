"""Shared CSS/JS for the 영유 vs 몬트리올 scenes (brand template "메이플 레드").
Every scene is a self-contained 1920x1080 sub-composition with no captions/logo inside, so the 9:16 shorts can
host the same scene file (optionally starting mid-scene, see OFF in scene_html)."""
import re

RED, DARK, CREAM, PINK, WINE = "#C8102E", "#2B2B2B", "#FFF8F2", "#FFD6CF", "#7A1B26"



def fonts_css():
    """@font-face rules written by tools/fonts.py (subset to the characters the film uses)."""
    import os
    p = os.path.join("assets", "fonts", "fonts.css")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

MAPLE = ("M50 4 L58 22 L70 16 L66 40 L80 30 L84 40 L96 38 L88 54 L94 58 L72 74 L76 84 L54 80 L54 98 L46 98 "
         "L46 80 L24 84 L28 74 L6 58 L12 54 L4 38 L16 40 L20 30 L34 40 L30 16 L42 22 Z")


def maple(cls="", size=100, color=RED, extra=""):
    return (f'<svg class="{cls}" {extra} width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<path d="{MAPLE}" fill="{color}"/></svg>')


def kid(color=RED, size=90, cls="kid"):
    """Simple child pictogram (no face)."""
    return (f'<svg class="{cls}" width="{size}" height="{size * 1.4:.0f}" viewBox="0 0 100 140">'
            f'<circle cx="50" cy="30" r="22" fill="{color}"/>'
            f'<path d="M22 62 Q50 50 78 62 L74 112 L26 112 Z" fill="{color}"/>'
            f'<rect x="30" y="108" width="14" height="30" rx="6" fill="{color}"/><rect x="56" y="108" width="14" height="30" rx="6" fill="{color}"/></svg>')


def adult(color=DARK, size=110, cls="adult"):
    return (f'<svg class="{cls}" width="{size}" height="{size * 1.6:.0f}" viewBox="0 0 100 160">'
            f'<circle cx="50" cy="26" r="20" fill="{color}"/>'
            f'<path d="M18 58 Q50 44 82 58 L78 120 L22 120 Z" fill="{color}"/>'
            f'<rect x="28" y="116" width="16" height="42" rx="7" fill="{color}"/><rect x="56" y="116" width="16" height="42" rx="7" fill="{color}"/></svg>')


# R is replaced by #<scene id>. Never give a GSAP-tweened node a CSS transform.
BASE_CSS = """
R{position:absolute;inset:0;overflow:hidden;color:#2B2B2B;font-family:'Noto Sans KR',sans-serif}
R *{box-sizing:border-box}
R .bg{position:absolute;inset:0;background:#FFF8F2}
R .bgdots{position:absolute;inset:0;background-image:radial-gradient(rgba(200,16,46,.10) 2px,transparent 2.5px);background-size:44px 44px;opacity:.6}
R .bgleaf{position:absolute;opacity:.07}
R .stage{position:absolute;inset:0}
R .ph{position:absolute;inset:0}
R .abs{position:absolute}
R .bhs{font-family:'Black Han Sans','Noto Sans KR',sans-serif;font-weight:400;letter-spacing:-.01em;line-height:1.12}
R .h{font-weight:900;letter-spacing:-.03em;line-height:1.15}
R .hd{font-weight:700;letter-spacing:-.02em;line-height:1.3}
R .b{font-weight:500;line-height:1.45}
R .num{font-family:'Black Han Sans','Noto Sans KR',sans-serif;letter-spacing:-.01em;line-height:1;font-variant-numeric:tabular-nums}
R .red{color:#C8102E}
R .wine{color:#7A1B26}
R .hl{background:linear-gradient(0deg,#FFD6CF 0 42%,transparent 42%);padding:0 .08em}
R .center{left:0;right:0;text-align:center}
R .card{position:absolute;background:#fff;border-radius:28px;box-shadow:0 18px 40px rgba(122,27,38,.14);border:3px solid rgba(200,16,46,.10)}
R .card.red{background:#C8102E;color:#fff;border-color:#C8102E}
R .card.pink{background:#FFD6CF;border-color:#FFD6CF}
R .card.dark{background:#2B2B2B;color:#fff;border-color:#2B2B2B}
R .chip{position:absolute;white-space:nowrap;border-radius:99px;padding:12px 30px;font-weight:700;font-size:32px;background:#fff;border:3px solid #C8102E;color:#C8102E}
R .chip.solid{background:#C8102E;color:#fff}
R .chip.pink{background:#FFD6CF;border-color:#FFD6CF;color:#7A1B26}
R .chip.dark{background:#2B2B2B;border-color:#2B2B2B;color:#fff}
R .tag{position:absolute;left:120px;top:96px;display:flex;align-items:center;gap:14px;font-weight:900;font-size:30px;color:#7A1B26;letter-spacing:.02em}
R .tag i{display:block;width:44px;height:6px;border-radius:3px;background:#C8102E}
R .stamp{position:absolute;white-space:nowrap;border:8px solid #C8102E;color:#C8102E;border-radius:18px;padding:10px 34px;font-family:'Black Han Sans','Noto Sans KR',sans-serif;background:rgba(255,248,242,.92)}
R .bar{position:absolute;border-radius:14px 14px 0 0}
R .line{position:absolute;height:6px;border-radius:3px;background:#C8102E}
R .reel{display:inline-block;height:1.2em;line-height:1.2em;overflow:hidden;vertical-align:-0.1em}
R .strip{display:block}
R .strip i{display:block;height:1.2em;line-height:1.2em;font-style:normal}
R .ch{display:inline-block;white-space:pre}
R .check{display:inline-flex;align-items:center;justify-content:center;width:58px;height:58px;border-radius:50%;background:#C8102E;color:#fff;font-weight:900;font-size:34px;flex:none}
R .bubble{position:absolute;white-space:nowrap;background:#fff;border-radius:30px;padding:16px 30px;font-weight:700;font-size:34px;box-shadow:0 10px 24px rgba(122,27,38,.12)}
R .bubble.red{background:#C8102E;color:#fff}
R .bubble.pink{background:#FFD6CF;color:#7A1B26}
R svg{overflow:visible}
"""

JS_HELPERS = r"""
const q=s=>root.querySelector(s), qa=s=>Array.from(root.querySelectorAll(s));
const tl=gsap.timeline({paused:true});
const E=el=>typeof el==='string'?qa(el):el, E1=el=>typeof el==='string'?q(el):el;
function inn(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,x:o.x||0,y:(o.y===undefined?30:o.y),scale:(o.s===undefined?1:o.s)},
  {opacity:1,x:0,y:0,scale:1,duration:o.d||0.6,ease:o.e||'power3.out',stagger:o.st||0},at);}
function outt(el,at,o){o=o||{};tl.to(E(el),{opacity:0,y:o.y||0,x:o.x||0,scale:(o.s===undefined?1:o.s),duration:o.d||0.4,ease:'power2.in'},at);}
function dim(el,at,v){tl.to(E(el),{opacity:v===undefined?0.25:v,duration:0.4,ease:'power2.out'},at);}
function phase(el,at,prev){if(prev)tl.to(E(prev),{opacity:0,y:-30,duration:0.45,ease:'power2.in'},at-0.45);tl.fromTo(E(el),{opacity:0},{opacity:1,duration:0.01},at);}
function shake(at){const s=q('.stage');tl.to(s,{x:10,y:-6,duration:1/30,ease:'none'},at);tl.to(s,{x:-8,y:5,duration:1/30,ease:'none'},at+1/30);tl.to(s,{x:0,y:0,duration:1/30,ease:'none'},at+2/30);}
function slam(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,scale:o.s||2.0},{opacity:1,scale:1,duration:o.d||0.38,ease:'power4.in'},at);if(o.shake!==false)shake(at+(o.d||0.38));}
function stamp(el,at,rot){rot=(rot===undefined?-8:rot);tl.fromTo(E(el),{opacity:0,scale:2.6,rotation:rot},{opacity:1,scale:1,rotation:rot,duration:0.3,ease:'power4.in'},at);shake(at+0.3);}
function pop(el,at,st){tl.fromTo(E(el),{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.45,ease:'back.out(2)',stagger:(st===undefined?0.1:st)},at);}
function grow(el,at,d,axis,origin){tl.fromTo(E(el),axis==='y'?{scaleY:0,transformOrigin:origin||'50% 100%'}:{scaleX:0,transformOrigin:origin||'0% 50%'},axis==='y'?{scaleY:1,duration:d||0.8,ease:'power3.out'}:{scaleX:1,duration:d||0.8,ease:'power3.inOut'},at);}
function draw(path,at,d){qa(path).forEach(p=>{const L=p.getTotalLength();p.style.strokeDasharray=L+' '+L;tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:d||0.9,ease:'power2.inOut'},at);});}
function mask(el,at,d,dir){const from={l:'inset(0% 100% 0% 0%)',r:'inset(0% 0% 0% 100%)',u:'inset(100% 0% 0% 0%)',d:'inset(0% 0% 100% 0%)'}[dir||'l'];
  tl.fromTo(E(el),{clipPath:from},{clipPath:'inset(0% 0% 0% 0%)',duration:d||0.7,ease:'power3.inOut'},at);}
function kin(el,at,st){qa(el).forEach(e=>{const out=[];
  (function walk(n){Array.from(n.childNodes).forEach(c=>{if(c.nodeType===3){const f=document.createDocumentFragment();
    for(const ch of c.textContent){const s=document.createElement('span');s.className='ch';s.textContent=ch;f.appendChild(s);out.push(s);}
    c.replaceWith(f);}else if(c.nodeType===1&&c.tagName!=='svg'){walk(c);}});})(e);
  tl.fromTo(out,{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:'back.out(1.6)',stagger:st||0.035},at);});}
function odo(el,at,dur){el=E1(el);const t=el.textContent;el.textContent='';const reels=[];let k=0;
  for(const c of t){if(c>='0'&&c<='9'){const d=+c,r=document.createElement('span');r.className='reel';const s=document.createElement('span');s.className='strip';
      const n=10+d+1;for(let i=0;i<n;i++){const x=document.createElement('i');x.textContent=String(i%10);s.appendChild(x);}r.appendChild(s);el.appendChild(r);reels.push([s,n,k++]);}
    else{const s=document.createElement('span');s.textContent=c;el.appendChild(s);}}
  const m=reels.length;reels.forEach(([s,n,i])=>tl.fromTo(s,{yPercent:0},{yPercent:-100*(n-1)/n,duration:(dur||1.4)*(0.6+0.4*(i+1)/m),ease:'power3.out'},at));}
function pulse(el,at,n){for(let i=0;i<(n||1);i++){tl.to(E(el),{scale:1.08,duration:0.18,ease:'power2.out'},at+i*0.5);tl.to(E(el),{scale:1,duration:0.25,ease:'power2.in'},at+i*0.5+0.18);}}
function drift(){
  qa('.bgleaf').forEach((g,i)=>tl.fromTo(g,{rotation:0,y:0},{rotation:(i%2?-14:16),y:(i%2?30:-26),duration:D,ease:'sine.inOut'},0));
  tl.fromTo(q('.stage'),{scale:1,transformOrigin:'50% 45%'},{scale:1.02,duration:D,ease:'none'},0);
}
"""

T_RE = re.compile(r"T\('([^']*)'\)")


def scene_html(cid, duration, css, body, js, audio="", off=0.0):
    """off > 0: the host starts this scene `off` seconds in (shorts). The authored timeline is built as usual and
    a wrapper timeline scrubs it from `off`, so every cue stays at its real speech time."""
    css_all = re.sub(r"(?m)(^|[,}])R(?=[ {])", lambda m: m.group(1) + f"#{cid}", BASE_CSS + css)
    full = duration + off
    if off:
        reg = (f"const outer=gsap.timeline({{paused:true}});"
               f"outer.add(tl.tweenFromTo({off},{full:.3f},{{duration:{duration},ease:'none'}}),0);"
               f'window.__timelines["{cid}"]=outer;')
    else:
        reg = f'window.__timelines["{cid}"] = tl;'
    leaves = (maple("bgleaf", 520, "#C8102E", 'style="left:1500px;top:-120px"') +
              maple("bgleaf", 360, "#C8102E", 'style="left:-110px;top:640px"'))
    return f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{fonts_css()}
{css_all}
      </style>
      <div id="{cid}" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{duration}">
        <div class="bg"></div><div class="bgdots"></div>
        {leaves}
        <div class="stage">
{body}
        </div>
{audio}
      </div>
      <script>
        (function () {{
          const root = document.getElementById("{cid}");
          const D = {full:.3f};
{JS_HELPERS}
{js}
          drift();
          {reg}
        }})();
      </script>
    </template>
  </body>
</html>
"""
