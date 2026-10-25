"""Shared design system: palette, CSS, icons, JS motion helpers, skyline art."""

RED = "#C8102E"
INK = "#2B2B2B"
CREAM = "#FFF8F2"
HI = "#FFD6CF"
SUB = "#7A1B26"
YEL = "#F2B705"  # timetable "English" cells only (narration says yellow)
MUTE = "#D9B8B1"  # tinted neutral for non-focus bars
LINE = "#EAD3CB"

# --- icons: 64x64 line icons; each path gets class "ic" so draw() can trace it ---
ICONS = {
    "parent": ['<circle cx="32" cy="17" r="9"/>', '<path d="M14 58 C14 38 50 38 50 58"/>'],
    "child": ['<circle cx="32" cy="22" r="8"/>', '<path d="M18 58 C18 42 46 42 46 58"/>', '<path d="M24 12 L28 15 M40 12 L36 15"/>'],
    "school": ['<path d="M6 56 H58 M12 56 V28 L32 14 L52 28 V56"/>', '<path d="M26 56 V42 H38 V56"/>', '<path d="M32 14 V5 L43 8 L32 11"/>'],
    "bus": ['<path d="M6 16 H50 Q58 16 58 26 V46 H6 Z"/>', '<path d="M11 22 H23 V31 H11 Z M27 22 H39 V31 H27 Z"/>', '<circle cx="17" cy="48" r="5"/>', '<circle cx="47" cy="48" r="5"/>', '<path d="M50 20 L44 31 H51 L45 42"/>'],
    "printer": ['<path d="M8 8 H56 V56 H8 Z"/>', '<path d="M8 17 H56 M22 17 V25 H42 V17 M32 25 V31"/>', '<path d="M22 47 L32 41 L42 47 L32 53 Z"/>'],
    "board": ['<path d="M5 10 H59 V44 H5 Z"/>', '<path d="M20 58 L25 44 M44 58 L39 44"/>', '<path d="M13 36 L23 27 L32 31 L48 18"/>'],
    "book": ['<path d="M6 14 Q19 7 32 14 Q45 7 58 14 V52 Q45 45 32 52 Q19 45 6 52 Z"/>', '<path d="M32 14 V52"/>'],
    "bag": ['<path d="M12 22 H52 L47 58 H17 Z"/>', '<path d="M23 22 V17 Q32 4 41 17 V22"/>'],
    "music": ['<path d="M24 48 V14 L52 8 V42"/>', '<circle cx="17" cy="48" r="7"/>', '<circle cx="45" cy="42" r="7"/>'],
    "house": ['<path d="M6 30 L32 9 L58 30"/>', '<path d="M13 25 V56 H51 V25"/>', '<path d="M27 56 V40 H37 V56"/>'],
    "plane": ['<path d="M5 36 L59 13 L46 53 L34 41 L26 51 V38 Z"/>', '<path d="M34 41 L59 13"/>'],
    "doc": ['<path d="M15 5 H40 L50 15 V59 H15 Z"/>', '<path d="M40 5 V15 H50"/>', '<path d="M22 28 H43 M22 36 H43 M22 44 H35"/>'],
    "check": ['<circle cx="32" cy="32" r="26"/>', '<path d="M19 33 L28 42 L46 23"/>'],
    "clock": ['<circle cx="32" cy="32" r="25"/>', '<path d="M32 17 V32 L43 39"/>'],
    "chat": ['<path d="M7 11 H57 V42 H28 L15 55 V42 H7 Z"/>', '<path d="M18 23 H46 M18 31 H38"/>'],
    "coin": ['<circle cx="32" cy="32" r="24"/>', '<path d="M39 22 Q32 17 25 22 Q21 29 32 32 Q43 35 39 42 Q32 47 25 42 M32 13 V51"/>'],
    "star": ['<path d="M32 5 L39 24 L59 24 L43 36 L49 57 L32 45 L15 57 L21 36 L5 24 L25 24 Z"/>'],
    "pin": ['<path d="M32 59 C18 41 11 33 11 24 A21 21 0 1 1 53 24 C53 33 46 41 32 59 Z"/>', '<circle cx="32" cy="24" r="7"/>'],
    "heart": ['<path d="M32 55 C9 38 5 26 13 16 C21 7 30 11 32 18 C34 11 43 7 51 16 C59 26 55 38 32 55 Z"/>'],
    "gov": ['<path d="M6 56 H58 M11 56 V25 H53 V56"/>', '<path d="M6 25 L32 9 L58 25"/>', '<path d="M20 32 V49 M32 32 V49 M44 32 V49"/>'],
    "calendar": ['<path d="M9 13 H55 V55 H9 Z"/>', '<path d="M9 24 H55 M21 7 V18 M43 7 V18"/>', '<path d="M18 34 H26 M30 34 H38 M42 34 H48 M18 44 H26 M30 44 H38"/>'],
    "folder": ['<path d="M5 15 H26 L31 21 H59 V53 H5 Z"/>', '<path d="M5 28 H59"/>'],
    "trophy": ['<path d="M20 7 H44 V24 Q44 38 32 38 Q20 38 20 24 Z"/>', '<path d="M20 13 H9 Q9 27 20 27 M44 13 H55 Q55 27 44 27"/>', '<path d="M32 38 V48 M21 57 H43 V48 H21 Z"/>'],
    "smile": ['<circle cx="32" cy="32" r="25"/>', '<path d="M21 37 Q32 47 43 37"/>', '<path d="M24 25 V27 M40 25 V27"/>'],
    "globe": ['<circle cx="32" cy="32" r="25"/>', '<path d="M7 32 H57 M32 7 Q19 32 32 57 Q45 32 32 7"/>'],
    "mail": ['<path d="M6 15 H58 V51 H6 Z"/>', '<path d="M6 15 L32 36 L58 15"/>'],
    "phone": ['<path d="M18 6 H46 V58 H18 Z"/>', '<path d="M27 50 H37"/>'],
    "web": ['<circle cx="32" cy="32" r="25"/>', '<path d="M7 32 H57 M32 7 Q19 32 32 57 Q45 32 32 7 M12 19 H52 M12 45 H52"/>'],
    "flag": ['<path d="M14 58 V7"/>', '<path d="M14 9 H50 L42 20 L50 31 H14"/>'],
    "people": ['<circle cx="22" cy="20" r="7"/>', '<circle cx="44" cy="20" r="7"/>', '<path d="M8 54 C8 36 36 36 36 54 M30 40 C36 33 56 34 56 54"/>'],
}


def icon(name, size=96, color=INK, sw=4, cls="", extra=""):
    paths = "".join(p.replace("/>", ' class="ic"/>', 1) for p in ICONS[name])
    return (f'<svg class="icon {cls}" {extra} viewBox="0 0 64 64" width="{size}" height="{size}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


# simplified maple leaf (100x100), drawn symmetric
_R = [(50, 2), (57, 16), (64, 12), (61, 36), (74, 23), (77, 30), (91, 27), (86, 42), (94, 46), (74, 61), (77, 69), (54, 65), (53, 86), (52, 98)]
_L = [(100 - x, y) for x, y in reversed(_R)]
LEAF_D = "M" + " L".join(f"{x} {y}" for x, y in _R + _L) + " Z"


def leaf(size, color, sw=2.5, fill="none", cls="", style=""):
    return (f'<svg class="leaf {cls}" style="{style}" viewBox="0 0 100 100" width="{size}" height="{size}">'
            f'<path d="{LEAF_D}" fill="{fill}" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/></svg>')


def skyline():
    """Illustrated Montreal skyline (not a photo): Mount Royal + cross, downtown towers,
    Olympic Stadium tower, Jacques Cartier bridge. 1920x560 viewBox."""
    W, H = 1920, 560
    back = (f'<path class="sky-back" d="M-20 560 L-20 330 C220 300 360 120 640 110 C900 100 1040 260 1240 300 '
            f'C1460 340 1700 300 1940 320 L1940 560 Z" fill="#F7DCD5"/>'
            f'<path d="M620 112 V40 M600 62 H640" stroke="#E9B8AE" stroke-width="8" stroke-linecap="round"/>')
    # mid layer buildings
    mids = [(40, 300), (130, 250), (200, 330), (290, 210), (380, 280), (470, 190), (560, 300), (1300, 260), (1390, 220), (1490, 300), (1580, 240), (1680, 310), (1780, 270)]
    mid = ""
    for i, (x, h) in enumerate(mids):
        w = 70 + (i * 37) % 40
        mid += f'<rect x="{x}" y="{H - h}" width="{w}" height="{h}" fill="#EFC2B9"/>'
    # Olympic Stadium inclined tower (right)
    mid += '<path d="M1600 560 L1640 560 L1720 250 L1700 244 Z" fill="#E8AFA5"/><path d="M1540 560 Q1640 470 1760 560 Z" fill="#E8AFA5"/>'
    # front red skyline with landmarks
    front = ""
    blds = [(560, 70, 230), (640, 90, 330), (740, 60, 260), (812, 110, 420, "pvm"), (935, 80, 360), (1028, 70, 470, "spire"),
            (1110, 90, 300), (1212, 70, 380, "crown"), (1295, 100, 250), (1405, 60, 200), (460, 90, 180), (1475, 80, 150)]
    win = ""
    k = 0
    for b in blds:
        x, w, h = b[0], b[1], b[2]
        kind = b[3] if len(b) > 3 else ""
        y = H - h
        front += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{RED}"/>'
        if kind == "spire":
            front += f'<path d="M{x} {y} L{x + w / 2} {y - 70} L{x + w} {y} Z" fill="{RED}"/>'
        if kind == "pvm":
            front += f'<rect x="{x + 15}" y="{y - 22}" width="{w - 30}" height="24" fill="{RED}"/>'
        if kind == "crown":
            front += f'<path d="M{x} {y} L{x + 10} {y - 30} L{x + w - 10} {y - 30} L{x + w} {y} Z" fill="{RED}"/>'
        rows = int((h - 40) / 46)
        cols = max(1, int((w - 16) / 26))
        for r in range(rows):
            for c in range(cols):
                k += 1
                if (k * 7 + r * 3 + c) % 5 in (0, 2):
                    win += f'<rect class="win" x="{x + 12 + c * 26}" y="{y + 24 + r * 46}" width="12" height="20" rx="2" fill="{HI}"/>'
    # Jacques Cartier bridge (truss) across right
    bridge = ('<path class="bridge" d="M1180 470 L1920 430" stroke="#7A1B26" stroke-width="10" fill="none"/>'
              '<path class="bridge" d="M1300 466 Q1420 360 1540 455" stroke="#7A1B26" stroke-width="7" fill="none"/>'
              '<path class="bridge" d="M1560 452 Q1680 350 1800 440" stroke="#7A1B26" stroke-width="7" fill="none"/>'
              '<path class="bridge" d="M1330 440 L1360 410 L1390 448 L1420 392 L1450 446 L1480 400 L1510 452 '
              'M1590 425 L1620 395 L1650 435 L1680 380 L1710 432 L1740 392 L1770 438" stroke="#7A1B26" stroke-width="4" fill="none"/>')
    river = f'<rect x="-20" y="520" width="1960" height="60" fill="{HI}"/>'
    return (f'<svg class="skyline" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<g class="sk-back">{back}</g><g class="sk-mid">{mid}</g>'
            f'<g class="sk-front">{front}{win}</g><g class="sk-bridge">{bridge}</g>{river}</svg>')


CSS = r"""
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #FFF8F2; }
#root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Noto Sans KR", sans-serif; color: #2B2B2B; }
.basefill { position: absolute; inset: 0; background-color: #FFF8F2; }
.scene { position: absolute; inset: 0; overflow: hidden; background-color: #FFF8F2; }
.bgl { position: absolute; inset: 0; overflow: hidden; }
.dots { position: absolute; left: -60px; top: -60px; opacity: 0.8; }
.glow { position: absolute; width: 900px; height: 900px; border-radius: 50%; background-color: #FFE9E3; }
.ghost { position: absolute; font-family: "Black Han Sans"; font-size: 380px; line-height: 1; color: #F9E8E1; white-space: nowrap; }
.bgleaf { position: absolute; }
.stage { position: absolute; inset: 0; }
.abs { position: absolute; }
.bhs { font-family: "Black Han Sans"; font-weight: 400; }
.kick { font-weight: 900; font-size: 32px; letter-spacing: 0.14em; color: #C8102E; }
.h1 { font-family: "Black Han Sans"; font-size: 124px; line-height: 1.08; color: #2B2B2B; }
.h2 { font-family: "Black Han Sans"; font-size: 84px; line-height: 1.12; color: #2B2B2B; }
.h3 { font-family: "Black Han Sans"; font-size: 60px; line-height: 1.15; color: #2B2B2B; }
.red { color: #C8102E; }
.sub { color: #7A1B26; }
.body { font-weight: 700; font-size: 40px; line-height: 1.35; }
.small { font-weight: 700; font-size: 28px; line-height: 1.35; color: #7A1B26; }
.foot { position: absolute; left: 64px; bottom: 192px; font-weight: 500; font-size: 28px; color: #7A1B26; }
.chip { display: inline-block; font-weight: 900; font-size: 36px; padding: 12px 30px; border-radius: 999px; background: #C8102E; color: #FFFFFF; white-space: nowrap; }
.chip.o { background: #FFFFFF; color: #C8102E; border: 4px solid #C8102E; }
.chip.d { background: #2B2B2B; color: #FFFFFF; }
.card { position: absolute; background: #FFFFFF; border: 4px solid #2B2B2B; border-radius: 34px; box-shadow: 14px 14px 0 #FFD6CF; }
.mkw { position: relative; display: inline-block; isolation: isolate; }
.mk { position: absolute; left: -3%; width: 106%; bottom: 4%; height: 42%; background: #FFD6CF; z-index: -1; transform-origin: 0 50%; border-radius: 8px; }
.ring { position: absolute; border: 5px solid #C8102E; border-radius: 50%; }
.icon { display: block; overflow: visible; }
.win { position: absolute; overflow: hidden; border: 6px solid #C8102E; border-radius: 28px; background-color: #FFFFFF; box-shadow: 14px 14px 0 #FFD6CF; }
.pic { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
.pic img { position: absolute; display: block; }
.hl { position: absolute; border: 4px solid #C8102E; border-radius: 8px; }
.bdg { position: absolute; width: 64px; height: 64px; margin: -32px 0 0 -32px; border-radius: 50%; background-color: #C8102E; border: 4px solid #FFFFFF; color: #FFFFFF; font-family: "Black Han Sans"; font-size: 42px; line-height: 56px; text-align: center; box-shadow: 0 0 0 3px #C8102E; }
.num { font-family: "Black Han Sans"; font-variant-numeric: tabular-nums; }
.row { display: flex; align-items: center; }
.ctr { display: flex; align-items: center; justify-content: center; text-align: center; }
/* overlays */
.progress { position: absolute; left: 0; top: 0; width: 1920px; height: 8px; background: #C8102E; transform-origin: 0 50%; z-index: 400; }
.chap { position: absolute; left: 48px; top: 36px; z-index: 400; }
.chap span { display: inline-flex; align-items: center; gap: 14px; background: #2B2B2B; color: #FFFFFF; font-weight: 900; font-size: 27px; padding: 10px 26px 10px 20px; border-radius: 999px; }
.chap i { display: block; width: 14px; height: 14px; border-radius: 50%; background: #C8102E; }
.logo { position: absolute; right: 34px; bottom: 30px; width: 112px; height: 112px; z-index: 400; }
.cap { position: absolute; left: 0; right: 0; bottom: 34px; display: flex; justify-content: center; z-index: 410; }
.cap .t { display: inline-block; max-width: 1480px; background: #FFFFFF; border: 4px solid #2B2B2B; color: #2B2B2B; font-weight: 700; font-size: 42px; line-height: 1.38; padding: 10px 34px 12px; border-radius: 20px; text-align: center; word-break: keep-all; }
.cap .t b { color: #C8102E; font-weight: 900; }
"""

JS_HELPERS = r"""
const OFF = __OFF__;
// v2 audio: 283.00-286.45 (3.45 s) was cut from the narration. Scene cues are written in v1 narration
// time, so A() pulls every cue at/after the cut 3.45 s earlier. R() = already-final times (no shift).
const CUT = 283.0, CUTLEN = 3.45;
const A = (t) => t + OFF - (t >= CUT ? CUTLEN : 0);
const R = (t) => t + OFF;
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
function pop(sel, t, o = {}) {
  tl.fromTo(sel, { scale: o.from ?? 0.3, opacity: 0, rotation: o.rot ?? 0, y: o.y ?? 0 },
    { scale: 1, opacity: 1, rotation: 0, y: 0, duration: o.d ?? 0.55, ease: o.ease ?? "back.out(1.9)", stagger: o.st ?? 0 }, A(t));
}
function rise(sel, t, o = {}) {
  tl.fromTo(sel, { y: o.y ?? 70, opacity: 0 }, { y: 0, opacity: 1, duration: o.d ?? 0.6, ease: o.ease ?? "power3.out", stagger: o.st ?? 0.08 }, A(t));
}
function slide(sel, t, dx, o = {}) {
  tl.fromTo(sel, { x: dx, opacity: 0 }, { x: 0, opacity: 1, duration: o.d ?? 0.6, ease: o.ease ?? "power4.out", stagger: o.st ?? 0.08 }, A(t));
}
function drop(sel, t, o = {}) {
  tl.fromTo(sel, { y: o.y ?? -500, rotation: o.rot ?? -14, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: o.d ?? 0.75, ease: "bounce.out", stagger: o.st ?? 0 }, A(t));
}
function slam(sel, t, o = {}) {
  tl.fromTo(sel, { scale: o.from ?? 2.8, opacity: 0, rotation: o.rot ?? 0 }, { scale: 1, opacity: 1, rotation: o.to ?? 0, duration: o.d ?? 0.42, ease: "expo.out", stagger: o.st ?? 0 }, A(t));
}
function fade(sel, t, o = {}) { tl.fromTo(sel, { opacity: 0 }, { opacity: o.to ?? 1, duration: o.d ?? 0.5, ease: "power1.out", stagger: o.st ?? 0 }, A(t)); }
function flipIn(sel, t, o = {}) {
  tl.fromTo(sel, { rotationY: -90, opacity: 0, transformPerspective: 900 }, { rotationY: 0, opacity: 1, duration: o.d ?? 0.6, ease: "back.out(1.6)", stagger: o.st ?? 0.1 }, A(t));
}
function chars(sel, t, o = {}) {
  const split = (node) => {
    Array.from(node.childNodes).forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        for (const ch of n.textContent) { const s = document.createElement("span"); s.className = "chr"; s.style.display = "inline-block"; s.textContent = ch === " " ? "\u00a0" : ch; frag.appendChild(s); }
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && !n.classList.contains("mk")) split(n);
    });
  };
  $$(sel).forEach(split);
  tl.fromTo(sel + " .chr", { y: o.y ?? 120, opacity: 0, rotation: o.rot ?? 8, scale: o.from ?? 1 },
    { y: 0, opacity: 1, rotation: 0, scale: 1, duration: o.d ?? 0.5, ease: o.ease ?? "back.out(2)", stagger: o.st ?? 0.045 }, A(t));
}
function draw(sel, t, d = 1.1, o = {}) {
  $$(sel).forEach((p, i) => {
    const L = Math.ceil(p.getTotalLength() * 1.03) + 2;
    p.style.strokeDasharray = L + " " + L;
    tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease: o.ease ?? "power2.inOut" }, A(t) + i * (o.st ?? 0.06));
  });
}
function mark(sel, t, d = 0.45) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power2.out", stagger: 0.12 }, A(t)); }
function count(sel, t, d, from, to, fmt) {
  const el = $(sel); const o = { v: from }; const f = fmt || ((v) => Math.round(v).toLocaleString("en-US"));
  el.textContent = f(from);
  tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = f(o.v); } }, A(t));
}
function pulse(sel, t, o = {}) {
  tl.fromTo(sel, { scale: 1 }, { scale: o.s ?? 1.12, duration: o.d ?? 0.22, ease: "power2.out", yoyo: true, repeat: 1, stagger: o.st ?? 0 }, A(t));
}
function grow(sel, t, o = {}) {
  tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: o.d ?? 0.9, ease: o.ease ?? "power3.out", stagger: o.st ?? 0.1 }, A(t));
}
function growY(sel, t, o = {}) {
  tl.fromTo(sel, { scaleY: 0 }, { scaleY: 1, duration: o.d ?? 0.8, ease: o.ease ?? "back.out(1.4)", stagger: o.st ?? 0.1 }, A(t));
}
function view(sel, t, d, s, cx, cy, W, H, ease) {
  tl.to(sel, { x: W / 2 - cx * s, y: H / 2 - cy * s, scale: s, duration: d, ease: ease || "power3.inOut" }, A(t));
}
function setView(sel, t, s, cx, cy, W, H) {
  const v = { x: W / 2 - cx * s, y: H / 2 - cy * s, scale: s };
  tl.fromTo(sel, v, Object.assign({ duration: 0.01 }, v), A(t));
}
function cam(sel, t, d, to, ease) { tl.to(sel, Object.assign({ duration: d, ease: ease || "power2.inOut" }, to), A(t)); }
function dim(sel, t, v = 0.35) { tl.to(sel, { opacity: v, duration: 0.4, ease: "power1.out" }, A(t)); }
function burst(sel, t) {
  $$(sel).forEach((p, i) => {
    const a = (i / $$(sel).length) * Math.PI * 2 + (i % 3) * 0.3; const r = 160 + (i * 53) % 140;
    tl.fromTo(p, { x: 0, y: 0, scale: 0.2, opacity: 1 }, { x: Math.cos(a) * r, y: Math.sin(a) * r, scale: 1, opacity: 0, duration: 0.9, ease: "power3.out" }, A(t));
  });
}
"""
