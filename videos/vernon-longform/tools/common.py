"""Shared pieces for the Vernon long-form scene generator."""

FONTS = """
@font-face{font-family:Pretendard;font-weight:500;src:url(assets/fonts/Pretendard-Medium.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:700;src:url(assets/fonts/Pretendard-Bold.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:800;src:url(assets/fonts/Pretendard-ExtraBold.woff2) format("woff2")}
@font-face{font-family:Pretendard;font-weight:900;src:url(assets/fonts/Pretendard-Black.woff2) format("woff2")}
@font-face{font-family:Yellowtail;font-weight:400;src:url(assets/fonts/Yellowtail-Regular.ttf) format("truetype")}
"""

# Scoped with R (replaced by #sNN). No CSS transforms on anything GSAP tweens.
BASE_CSS = """
R{position:absolute;inset:0;overflow:hidden;background:#FAF6EF;color:#16324F;font-family:Pretendard,sans-serif}
R *{box-sizing:border-box}
R .bg{position:absolute;inset:0;background:#FAF6EF}
R .grain{position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(22,50,79,.07) 1.2px,transparent 1.3px);background-size:9px 9px}
R .glow{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(31,138,153,.20) 0%,rgba(31,138,153,0) 70%)}
R .glow.warm{background:radial-gradient(circle,rgba(232,87,43,.14) 0%,rgba(232,87,43,0) 70%)}
R .ghost{position:absolute;font-weight:900;color:rgba(22,50,79,.07);font-size:300px;letter-spacing:-.04em;white-space:nowrap;line-height:1}
R .stage{position:absolute;inset:0}
R .abs{position:absolute}
R .h{font-weight:900;letter-spacing:-.03em;line-height:1.1}
R .hd{font-weight:800;letter-spacing:-.02em;line-height:1.2}
R .b{font-weight:500;line-height:1.45}
R .l{font-weight:700;letter-spacing:.08em}
R .script{font-family:Yellowtail,cursive;line-height:1.05;white-space:nowrap}
R .sticker{position:absolute;background:#E8572B;color:#fff;font-weight:800;font-size:24px;letter-spacing:.12em;padding:10px 24px;border-radius:99px;white-space:nowrap}
R .chip{position:absolute;background:#FAF6EF;border:3px solid #16324F;border-radius:99px;padding:10px 24px;font-weight:700;font-size:28px;white-space:nowrap;color:#16324F}
R .chip.lake{border-color:#1F8A99;color:#146A77}
R .chip.solid{background:#16324F;color:#FAF6EF}
R .chip.sand{background:#F3C969;border-color:#F3C969}
R .pol{position:absolute;background:#fff;padding:16px 16px 60px;box-shadow:0 20px 44px rgba(22,50,79,.26)}
R .pol .ph{position:relative;width:100%;height:100%;overflow:hidden}
R .pol img,R .ph img{display:block;width:100%;height:100%;object-fit:cover}
R .pol .cap{position:absolute;left:0;right:0;bottom:12px;text-align:center;font-family:Yellowtail,cursive;font-size:32px;color:#16324F}
R .card{position:absolute;background:#fff;border:3px solid rgba(22,50,79,.14);border-radius:24px;box-shadow:0 12px 30px rgba(22,50,79,.13)}
R .panel{position:absolute;background:rgba(22,50,79,.93);border-radius:28px;color:#FAF6EF}
R .full{position:absolute;inset:0;overflow:hidden}
R .full img{width:100%;height:100%;object-fit:cover;display:block}
R .hlbar{position:absolute;background:#F3C969;height:22px;transform-origin:0 50%}
R .wipe{position:absolute;inset:0;background:#1F8A99;z-index:50}
R .flash{position:absolute;inset:0;background:#FAF6EF;z-index:60;opacity:0}
"""

JS_HELPERS = """
const q=s=>root.querySelector(s), qa=s=>Array.from(root.querySelectorAll(s));
const tl=gsap.timeline({paused:true});
function inn(el,at,o){o=o||{};if(typeof el==='string')el=q(el);
  tl.fromTo(el,{opacity:0,x:o.x||0,y:(o.y===undefined?30:o.y),scale:(o.s===undefined?1:o.s),rotation:(o.r0===undefined?(o.r||0):o.r0)},
  {opacity:1,x:0,y:0,scale:1,rotation:o.r||0,duration:o.d||0.6,ease:o.e||'power3.out'},at);}
function outt(el,at,o){o=o||{};if(typeof el==='string')el=q(el);
  tl.to(el,{opacity:0,y:o.y||0,x:o.x||0,scale:(o.s===undefined?1:o.s),duration:o.d||0.45,ease:'power2.in'},at);}
function pol(el,at,rot){if(typeof el==='string')el=q(el);
  tl.fromTo(el,{opacity:0,y:-180,rotation:rot*2.4,scale:1.06},{opacity:1,y:0,rotation:rot,scale:1,duration:0.85,ease:'power3.out'},at);}
function kb(el,at,dur,a,b){if(typeof el==='string')el=q(el);a=a||{};b=b||{};
  tl.fromTo(el,{scale:a.s||1,xPercent:a.x||0,yPercent:a.y||0},{scale:b.s||1.07,xPercent:b.x||0,yPercent:b.y||0,duration:dur,ease:'none'},at);}
function count(el,from,to,at,dur,fmt){if(typeof el==='string')el=q(el);const st={v:from};
  tl.fromTo(st,{v:from},{v:to,duration:dur,ease:'power2.out',immediateRender:false,onUpdate:()=>{el.textContent=fmt(st.v);}},at);}
function grow(el,at,d,origin){if(typeof el==='string')el=q(el);
  tl.fromTo(el,{scaleX:0,opacity:0,transformOrigin:origin||'0% 50%'},{scaleX:1,opacity:1,duration:d||0.8,ease:'power3.inOut'},at);}
function draw(path,at,d){if(typeof path==='string')path=q(path);const L=path.getTotalLength();
  path.style.strokeDasharray=L;tl.fromTo(path,{strokeDashoffset:L},{strokeDashoffset:0,duration:d||1,ease:'power2.inOut'},at);}
function ambient(){
  qa('.ghost').forEach((g,i)=>tl.fromTo(g,{x:0},{x:(i%2?160:-160),duration:D,ease:'none'},0));
  qa('.glow').forEach((g,i)=>{const c=4+i;const n=Math.max(0,Math.floor(D/c)-1);
    tl.fromTo(g,{scale:0.92},{scale:1.08,duration:c/2,ease:'sine.inOut',yoyo:true,repeat:n},0);});
  tl.fromTo(q('.stage'),{opacity:0},{opacity:1,duration:0.45,ease:'power1.out'},0);
  tl.fromTo(q('.stage'),{scale:1,transformOrigin:'50% 45%'},{scale:1.03,duration:D,ease:'none'},0);
  if(q('.wipe'))tl.fromTo(q('.wipe'),{xPercent:0},{xPercent:-101,duration:0.75,ease:'power3.inOut'},0.05);
  tl.to(q('.stage'),{opacity:0,duration:0.5,ease:'power1.in'},D-0.55);
}
"""


GHOST_RE = __import__("re").compile(r'<div class="ghost" style="([^"]*)">([^<]*)</div>')


def _ghost(m):
    style, word = m.group(1), m.group(2)
    fs = __import__("re").search(r"font-size:(\d+)px", style)
    fs = int(fs.group(1)) if fs else 300
    col = __import__("re").search(r"color:(rgba\([^)]*\))", style)
    col = col.group(1) if col else "rgba(22,50,79,.07)"
    pos = ";".join(x for x in style.split(";") if x.strip().startswith(("left", "top")))
    return (f'<svg class="ghost" aria-hidden="true" style="{pos};width:{len(word) * fs}px;height:{int(fs * 1.1)}px;overflow:visible">'
            f'<text x="0" y="{int(fs * 0.9)}" font-family="Pretendard" font-weight="900" font-size="{fs}" fill="{col}" letter-spacing="-8">{word}</text></svg>')


def scene_html(cid, fname_id, duration, cues, css, body, js, bg_extra=""):
    bg_extra = GHOST_RE.sub(_ghost, bg_extra)
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
        <div class="grain"></div>
{bg_extra}
        <div class="stage">
{body}
        </div>
      </div>
      <script>
        (function () {{
          const root = document.getElementById("{cid}");
          const D = {duration};
          const R = {cues};
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
