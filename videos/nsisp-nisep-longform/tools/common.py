"""Shared timing, caption alignment, scene template and the JS motion helpers."""
import difflib
import json
import os
import re
import subprocess

from script import CAPS

PLAN = os.path.join("..", "..", "plans", "nsisp-nisep-longform")
GAP, XF = 0.5, 0.4  # silence between scenes, picture crossfade
FONTS = "".join(
    f'@font-face{{font-family:Pretendard;font-weight:{w};src:url(assets/fonts/Pretendard-{n}.woff2) format("woff2")}}\n'
    for w, n in ((500, "Medium"), (700, "Bold"), (800, "ExtraBold"), (900, "Black")))

C = dict(bg="#0a1c30", bg2="#10304d", ink="#0b1f33", cream="#f5f0e6", blue="#4aa3df", amber="#f2a33a",
         teal="#2fb5a5", gold="#f2c14e", mut="rgba(245,240,230,.72)")


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout)


def timeline():
    """Voice start V, voice end E and clip ranges for every scene."""
    D = {1: dur(os.path.join(PLAN, "heygen", "S1_face.mp4")), 9: dur(os.path.join(PLAN, "heygen", "S9_face.mp4"))}
    for k in range(2, 9):
        D[k] = dur(os.path.join(PLAN, "audio", f"S{k}.mp3"))
    V, E = {1: 0.0}, {1: D[1]}
    for k in range(2, 10):
        V[k] = round(E[k - 1] + GAP, 3)
        E[k] = round(V[k] + D[k], 3)
    clip = {1: (0.0, E[1])}
    for k in range(2, 9):
        start = round(E[k - 1] - XF, 3)
        end = E[k] if k < 8 else round(V[9] + XF, 3)
        clip[k] = (start, round(end - start, 3))
    clip[1] = (0.0, E[1])
    clip[9] = (V[9], round(E[9] - V[9], 3))
    clip["end"] = (round(E[9] - XF, 3), round(3.0 + XF, 3))
    total = round(E[9] + 3.0, 3)
    return D, V, E, clip, total


NORM = re.compile(r"[0-9A-Za-z가-힣]")


def _norm_chars(s):
    return [c for c in s if NORM.match(c)]


class Align:
    """Map script characters to audio time using ElevenLabs Scribe word timestamps."""

    def __init__(self, k):
        self.k = k
        d = json.load(open(os.path.join("assets", "voice", "asr", f"S{k}.json"), encoding="utf-8"))
        a_chars, a_t, a_end = [], [], []
        for w in d["words"]:
            if w["type"] != "word":
                continue
            cs = _norm_chars(w["text"])
            for i, c in enumerate(cs):
                a_chars.append(c)
                a_t.append(w["start"] + (w["end"] - w["start"]) * i / max(1, len(cs)))
                a_end.append(w["end"])
        self.chunks = [ln.strip() for ln in CAPS[k].strip().split("\n") if ln.strip()]
        plain = [c.replace("**", "") for c in self.chunks]
        self.s_chars, self.chunk_of = [], []
        for ci, c in enumerate(plain):
            for ch in _norm_chars(c):
                self.s_chars.append(ch)
                self.chunk_of.append(ci)
        self.text = "".join(self.s_chars)
        sm = difflib.SequenceMatcher(None, self.s_chars, a_chars, autojunk=False)
        m = {}
        for b in sm.get_matching_blocks():
            for i in range(b.size):
                m[b.a + i] = b.b + i
        n = len(self.s_chars)
        self.t, self.te = [None] * n, [None] * n
        for i, j in m.items():
            self.t[i], self.te[i] = a_t[j], a_end[j]
        known = [i for i in range(n) if self.t[i] is not None]
        for i in range(n):  # interpolate unmatched characters
            if self.t[i] is None:
                lo = max([x for x in known if x < i], default=None)
                hi = min([x for x in known if x > i], default=None)
                if lo is None:
                    self.t[i] = self.te[i] = self.t[hi]
                elif hi is None:
                    self.t[i] = self.te[i] = self.te[lo]
                else:
                    f = (i - lo) / (hi - lo)
                    self.t[i] = self.te[lo] + (self.t[hi] - self.te[lo]) * f
                    self.te[i] = self.t[i]

    def at(self, phrase, after=0.0):
        p = "".join(_norm_chars(phrase))
        i = self.text.find(p)
        while i >= 0 and self.t[i] < after:
            i = self.text.find(p, i + 1)
        if i < 0:
            raise KeyError(f"S{self.k}: phrase not found: {phrase}")
        return round(self.t[i], 3)

    def captions(self):
        out, n = [], len(self.chunks)
        firsts = [self.chunk_of.index(ci) for ci in range(n)]
        lasts = [len(self.chunk_of) - 1 - self.chunk_of[::-1].index(ci) for ci in range(n)]
        for ci in range(n):
            st = self.t[firsts[ci]] - 0.08
            last_end = self.te[lasts[ci]]
            if ci + 1 < n and self.t[firsts[ci + 1]] - last_end < 1.2:
                en = self.t[firsts[ci + 1]] - 0.1
            else:
                en = last_end + 0.45
            out.append((round(max(0, st), 3), round(en, 3), self.chunks[ci]))
        return out


JS_LIB = r"""
const q=s=>root.querySelector(s), qa=s=>Array.from(root.querySelectorAll(s));
const tl=gsap.timeline({paused:true});
const E=el=>typeof el==='string'?qa(el):el, E1=el=>typeof el==='string'?q(el):el;
const fmt=v=>String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g,',');
function inn(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,x:o.x||0,y:(o.y===undefined?30:o.y),scale:(o.s===undefined?1:o.s)},
  {opacity:1,x:0,y:0,scale:1,duration:o.d||0.6,ease:o.e||'power3.out',stagger:o.st||0},at);}
function out(el,at,o){o=o||{};tl.to(E(el),{opacity:(o.o===undefined?0:o.o),y:o.y||0,x:o.x||0,scale:(o.s===undefined?1:o.s),duration:o.d||0.45,ease:'power2.in'},at);}
function pop(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,scale:o.s||0.4},{opacity:1,scale:1,duration:o.d||0.45,ease:'back.out(2.2)',stagger:(o.st===undefined?0.08:o.st)},at);}
function grow(el,at,o){o=o||{};const y=o.axis==='y';tl.fromTo(E(el),y?{scaleY:0,transformOrigin:o.origin||'50% 100%'}:{scaleX:0,transformOrigin:o.origin||'0% 50%'},
  y?{scaleY:1,duration:o.d||0.8,ease:o.e||'power3.out',stagger:o.st||0}:{scaleX:1,duration:o.d||0.8,ease:o.e||'power3.inOut',stagger:o.st||0},at);}
function draw(el,at,o){o=o||{};E(el).forEach((p,i)=>{const L=p.getTotalLength();p.style.strokeDasharray=L+' '+L;p.style.strokeDashoffset=L;
  tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:o.d||0.9,ease:o.e||'power2.inOut'},at+i*(o.st||0));});}
function shake(at){const s=q('.stage');tl.to(s,{x:10,y:-6,duration:1/30,ease:'none'},at);tl.to(s,{x:-8,y:5,duration:1/30,ease:'none'},at+1/30);tl.to(s,{x:0,y:0,duration:1/30,ease:'none'},at+2/30);}
function stamp(el,at,o){o=o||{};const r=(o.r===undefined?-10:o.r);tl.fromTo(E(el),{opacity:0,scale:2.6,rotation:r},{opacity:1,scale:1,rotation:r,duration:0.3,ease:'power4.in'},at);shake(at+0.3);}
function flip(el,at,o){o=o||{};tl.fromTo(E(el),{opacity:0,rotationY:o.r||-80,transformPerspective:1600},{opacity:1,rotationY:0,transformPerspective:1600,duration:o.d||0.75,ease:'power3.out',stagger:o.st||0},at);}
function count(el,at,o){const e=E1(el);const p={v:o.a||0};const w=v=>(o.pre||'')+(o.dec?v.toFixed(o.dec):fmt(v))+(o.suf||'');e.textContent=w(o.a||0);
  tl.fromTo(p,{v:o.a||0},{v:o.b,duration:o.d||1.2,ease:o.e||'power2.out',onUpdate:()=>{e.textContent=w(p.v);}},at);}
function kin(el,at,o){o=o||{};const e=E1(el);const t=e.textContent;e.textContent='';
  for(const c of t){const s=document.createElement('span');s.className='ch';s.textContent=c;e.appendChild(s);}
  tl.fromTo(e.querySelectorAll('.ch'),{opacity:0,y:40,rotationX:80,transformPerspective:700},{opacity:1,y:0,rotationX:0,transformPerspective:700,duration:0.55,ease:'power3.out',stagger:o.st||0.035},at);}
function to(el,at,o){const v=Object.assign({},o);v.duration=v.duration||0.6;v.ease=v.ease||'power2.inOut';tl.to(E(el),v,at);}
function fromto(el,at,o){const f=o.f,t=Object.assign({},o.t);t.duration=t.duration||0.6;t.ease=t.ease||'power2.out';tl.fromTo(E(el),f,t,at);}
function pulse(el,at,o){o=o||{};tl.fromTo(E(el),{scale:1},{scale:o.s||1.08,duration:0.18,ease:'power2.out',yoyo:true,repeat:1,stagger:o.st||0},at);}
function sweep(el,at){tl.fromTo(E(el),{xPercent:-140,opacity:1},{xPercent:340,opacity:1,duration:1.1,ease:'power2.inOut'},at);}
function ambient(D){
  qa('.glow').forEach((g,i)=>tl.fromTo(g,{x:0,y:0},{x:(i%2?-160:180),y:(i%2?90:-80),duration:D,ease:'sine.inOut'},0));
  qa('.wave').forEach((g,i)=>tl.fromTo(g,{x:0},{x:(i%2?-120:120),duration:D,ease:'none'},0));
  tl.fromTo(q('.stage'),{scale:1,transformOrigin:'50% 46%'},{scale:1.02,duration:D,ease:'none'},0);
}
"""

BASE_CSS = """
R{position:absolute;inset:0;overflow:hidden;color:#f5f0e6;font-family:Pretendard,sans-serif}
R *{box-sizing:border-box}
R .bg{position:absolute;inset:0;background:radial-gradient(ellipse at 70% 20%,#14385a 0%,#0a1c30 60%,#07131f 100%)}
R .glow{position:absolute;width:1100px;height:1100px;border-radius:50%;pointer-events:none}
R .glow.a{left:-380px;top:-460px;background:radial-gradient(circle,rgba(74,163,223,.20) 0%,rgba(74,163,223,0) 66%)}
R .glow.b{left:1100px;top:420px;background:radial-gradient(circle,rgba(242,163,58,.14) 0%,rgba(242,163,58,0) 66%)}
R .wave{position:absolute;left:-200px;width:2320px;height:120px;opacity:.10}
R .stage{position:absolute;inset:0}
R .abs{position:absolute}
R .h{font-weight:900;letter-spacing:-.03em;line-height:1.1}
R .hd{font-weight:800;letter-spacing:-.02em;line-height:1.25}
R .b{font-weight:500;line-height:1.45}
R .num{font-weight:900;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
R .ch{display:inline-block;white-space:pre}
R .card{position:absolute;background:#f5f0e6;color:#0b1f33;border-radius:28px;box-shadow:0 24px 50px rgba(0,0,0,.35)}
R .dcard{position:absolute;background:rgba(16,48,77,.82);border:2px solid rgba(245,240,230,.16);border-radius:28px;box-shadow:0 24px 50px rgba(0,0,0,.30)}
R .pill{display:inline-flex;align-items:center;gap:12px;white-space:nowrap;border-radius:99px;padding:8px 24px;font-weight:900;font-size:30px;letter-spacing:.02em}
R .pill.ns{background:#4aa3df;color:#07131f}
R .pill.nl{background:#f2a33a;color:#07131f}
R .pill.ghost{background:rgba(245,240,230,.12);color:#f5f0e6;border:2px solid rgba(245,240,230,.3)}
R .pill small{font-weight:700;font-size:22px;opacity:.85}
R .chip{position:absolute;display:inline-flex;align-items:center;gap:14px;white-space:nowrap;border-radius:99px;padding:12px 28px;font-weight:800;font-size:30px;background:rgba(245,240,230,.10);border:2px solid rgba(245,240,230,.28);color:#f5f0e6}
R .chip.cream{background:#f5f0e6;border-color:#f5f0e6;color:#0b1f33}
R .chip.teal{background:#2fb5a5;border-color:#2fb5a5;color:#07131f}
R .ns-c{color:#4aa3df}
R .nl-c{color:#f2a33a}
R .gold{color:#f2c14e}
R .tick{display:inline-block;width:38px;height:38px;border-radius:50%;background:#2fb5a5;flex:none;position:relative}
R .tick:after{content:'';position:absolute;left:13px;top:6px;width:10px;height:19px;border:solid #07131f;border-width:0 5px 5px 0;transform:rotate(45deg)}
R svg{overflow:visible}
R .sweep{position:absolute;top:-20%;bottom:-20%;left:0;width:30%;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.35),rgba(255,255,255,0));mix-blend-mode:screen;opacity:0}
R .title{left:120px;top:134px;font-size:62px}
R .kick{left:124px;top:98px;font-size:26px;font-weight:700;letter-spacing:.18em;color:#2fb5a5}
"""

WAVE = ('<svg class="wave" style="top:{top}px" viewBox="0 0 2320 120" preserveAspectRatio="none">'
        '<path d="M0 60 Q72 10 145 60 ' + " ".join(f"T{145 * i} 60" for i in range(2, 17)) +
        '" fill="none" stroke="#f5f0e6" stroke-width="3"/></svg>')


def scene_html(cid, dur_s, css, body, js, bg=True):
    base = BASE_CSS.replace("R ", f"#{cid} ").replace("R{", f"#{cid}{{")
    css = css.replace("R ", f"#{cid} ")
    deco = ('<div class="bg"></div><div class="glow a"></div><div class="glow b"></div>' +
            WAVE.format(top=900) + WAVE.format(top=980)) if bg else ""
    return f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{FONTS}
{base}
{css}
      </style>
      <div id="{cid}" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{dur_s}">
        {deco}
        <div class="stage">
{body}
        </div>
      </div>
      <script>
        (function () {{
          const root = document.getElementById("{cid}");
          const D = {dur_s};
{JS_LIB}
{js}
          ambient(D);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["{cid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""


def J(fn, sel, at, **o):
    def v(x):
        return x if isinstance(x, Raw) else json.dumps(x, ensure_ascii=False)
    opts = "{" + ",".join(f"{k}:{v(x)}" for k, x in o.items()) + "}"
    return f"{fn}({json.dumps(sel)},{at:.3f},{opts});"


class Raw(str):
    pass
