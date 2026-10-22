"""Map camera + labels/pins + B-roll reels + icons shared by the South Shore scenes.

Map layer: <div class="cam"> holds the base SVG (map units) plus an overlay SVG (REM line, territory) and HTML labels
positioned in map units. The camera is a GSAP tween on .cam (x, y, scale, transform-origin 0 0); views come from geo.view.
Labels are sized for the view they are shown in: font px = screen px / view scale.

Cue expressions in scene bodies use ⟦expr⟧ (resolved by build.py: T('phrase') -> seconds, then evaluated).
"""
import geo

CSS = """
R .cam{position:absolute;left:0;top:0;width:%dpx;height:%dpx}
R .cam svg{position:absolute;left:0;top:0}
R .mlab{position:absolute;white-space:nowrap;font-weight:900;color:#7A1B26;transform-origin:0 50%%}
R .mlab i{display:inline-block;border-radius:50%%;background:#C8102E;margin-right:.35em;vertical-align:.12em}
R .mtag{position:absolute;white-space:nowrap;font-weight:900;background:#fff;color:#C8102E;border:.12em solid #C8102E;border-radius:.6em;padding:.12em .55em}
R .water-lab{position:absolute;white-space:nowrap;font-weight:700;color:#6F8C9B;letter-spacing:.12em;font-style:italic}
R .pin{position:absolute}
R .broll{position:absolute;overflow:hidden;border-radius:26px;background:#2B2B2B;box-shadow:0 18px 40px rgba(122,27,38,.22)}
R .broll video{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
R .broll .cr{position:absolute;right:14px;bottom:10px;font-size:18px;font-weight:700;color:#fff;opacity:.85;text-shadow:0 1px 4px rgba(0,0,0,.6)}
R .broll .lb{position:absolute;left:16px;top:14px;font-size:24px;font-weight:900;color:#fff;background:#C8102E;border-radius:12px;padding:4px 14px}
""" % (geo.W, geo.H)

PIN = ('<svg viewBox="0 0 44 60" width="%(w).0f" height="%(h).0f"><path d="M22 58 C 8 38, 2 30, 2 22 A20 20 0 0 1 42 22 '
       'C 42 30, 36 38, 22 58 Z" fill="%(c)s"/><circle cx="22" cy="22" r="8" fill="#fff"/></svg>')


def cam_html(inner="", overlay="", south_hi=False):
    over = f'<svg class="ov" viewBox="0 0 {geo.W} {geo.H}" width="{geo.W}" height="{geo.H}">{overlay}</svg>' if overlay else ""
    return f'<div class="cam">{geo.svg_map(south_hi=south_hi)}{over}{inner}</div>'


def cam_set_js(v, at=0.0):
    return f"tl.set(q('.cam'),{{x:{v['x']},y:{v['y']},scale:{v['scale']},transformOrigin:'0 0'}},{at});"


def cam_move_js(v, at, d=2.2, ease="power2.inOut"):
    return f"tl.to(q('.cam'),{{x:{v['x']},y:{v['y']},scale:{v['scale']},duration:{d},ease:'{ease}'}},{at});"


def label(cls, text, lat, lon, v, px=34, dot=True, dx=0, dy=0, kind="mlab"):
    """HTML label in map units. Anchored left-middle at the point (dot first)."""
    x, y = geo.map_xy(lat, lon)
    f = px / v["scale"]
    d = f'<i style="width:{0.55 * f:.1f}px;height:{0.55 * f:.1f}px"></i>' if dot else ""
    return (f'<div class="{kind} {cls}" style="left:{x + dx / v["scale"]:.1f}px;top:{y - 0.62 * f + dy / v["scale"]:.1f}px;'
            f'font-size:{f:.1f}px">{d}{text}</div>')


def pin(cls, lat, lon, v, px=54, color="#C8102E"):
    x, y = geo.map_xy(lat, lon)
    w = px / v["scale"]
    h = w * 60 / 44
    return f'<div class="pin {cls}" style="left:{x - w / 2:.1f}px;top:{y - h:.1f}px">{PIN % dict(w=w, h=h, c=color)}</div>'


def reel(sid, cls, x, y, w, h, items, credit="영상: Riverside School Board", label_text=""):
    """A framed B-roll window. items: [(clip_name, start_expr, dur)] scene-local times (exprs may use T()).
    Each <video> carries its own data-start/duration (no timed ancestor)."""
    vids = []
    for k, (name, at, dur) in enumerate(items):
        vids.append(f'<video id="{sid}-{cls}-v{k}" class="clip" src="assets/clips/{name}.mp4" muted playsinline '
                    f'data-start="⟦{at}⟧" data-duration="⟦{dur}⟧" data-track-index="{40 + k % 2}"></video>')
    lb = f'<div class="lb">{label_text}</div>' if label_text else ""
    return (f'<div class="broll {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{"".join(vids)}'
            f'<div class="cr">{credit}</div>{lb}</div>')


def seq(names, start_expr, slot, dur_of):
    """Clips back to back from start_expr, each shown min(slot, clip length)."""
    out, t = [], 0.0
    for n in names:
        d = round(min(slot, dur_of(n) - 0.05), 3)
        out.append((n, f"{start_expr}+{t:.3f}", d))
        t += d
    return out, round(t, 3)


# ---- icons (simple, no faces) ---------------------------------------------------------------------------------
def icon(name, size=90, color="#C8102E"):
    p = {
        "house": '<path d="M10 46 L50 12 L90 46 L90 90 L10 90 Z" fill="C"/><rect x="40" y="60" width="20" height="30" fill="#fff"/>'
                 '<rect x="18" y="52" width="16" height="14" fill="#fff"/><rect x="66" y="52" width="16" height="14" fill="#fff"/>',
        "tree": '<circle cx="50" cy="36" r="28" fill="C"/><rect x="44" y="56" width="12" height="36" fill="C"/>',
        "school": '<path d="M6 40 L50 10 L94 40 Z" fill="C"/><rect x="14" y="40" width="72" height="50" fill="C"/>'
                  '<rect x="42" y="62" width="16" height="28" fill="#fff"/><rect x="22" y="50" width="12" height="12" fill="#fff"/>'
                  '<rect x="66" y="50" width="12" height="12" fill="#fff"/><circle cx="50" cy="28" r="6" fill="#fff"/>',
        "museum": '<path d="M8 32 L50 8 L92 32 Z" fill="C"/><rect x="10" y="84" width="80" height="8" fill="C"/>'
                  '<rect x="16" y="38" width="10" height="42" fill="C"/><rect x="36" y="38" width="10" height="42" fill="C"/>'
                  '<rect x="56" y="38" width="10" height="42" fill="C"/><rect x="76" y="38" width="10" height="42" fill="C"/>',
        "theatre": '<path d="M14 14 Q50 30 86 14 L86 50 Q86 86 50 90 Q14 86 14 50 Z" fill="C"/>'
                   '<circle cx="36" cy="44" r="6" fill="#fff"/><circle cx="64" cy="44" r="6" fill="#fff"/>'
                   '<path d="M34 64 Q50 78 66 64" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>',
        "train": '<rect x="20" y="8" width="60" height="70" rx="14" fill="C"/><rect x="28" y="18" width="44" height="24" rx="4" fill="#fff"/>'
                 '<circle cx="34" cy="60" r="6" fill="#fff"/><circle cx="66" cy="60" r="6" fill="#fff"/>'
                 '<path d="M30 80 L20 94 M70 80 L80 94" stroke="C" stroke-width="8" stroke-linecap="round"/>',
        "city": '<rect x="8" y="40" width="20" height="52" fill="C"/><rect x="32" y="14" width="22" height="78" fill="C"/>'
                '<rect x="58" y="30" width="16" height="62" fill="C"/><rect x="78" y="50" width="14" height="42" fill="C"/>',
        "shield": '<path d="M50 6 L88 20 L84 58 Q78 84 50 94 Q22 84 16 58 L12 20 Z" fill="C"/>'
                  '<path d="M34 50 L46 62 L68 38" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "bus": '<rect x="8" y="16" width="84" height="60" rx="12" fill="C"/><rect x="16" y="26" width="30" height="20" fill="#fff"/>'
               '<rect x="54" y="26" width="30" height="20" fill="#fff"/><circle cx="28" cy="80" r="9" fill="C"/><circle cx="72" cy="80" r="9" fill="C"/>',
        "ball": '<circle cx="50" cy="50" r="40" fill="C"/><path d="M10 50 H90 M50 10 V90 M22 22 Q50 50 22 78 M78 22 Q50 50 78 78" stroke="#fff" stroke-width="5" fill="none"/>',
        "meal": '<circle cx="50" cy="54" r="34" fill="C"/><circle cx="50" cy="54" r="20" fill="#fff"/>'
                '<path d="M12 10 V40 M6 10 V30 M18 10 V30 M88 10 Q74 24 88 44 V92" stroke="C" stroke-width="6" fill="none" stroke-linecap="round"/>',
        "plane": '<path d="M50 6 Q56 6 56 18 L56 40 L92 60 L92 70 L56 58 L56 80 L68 90 L68 96 L50 90 L32 96 L32 90 L44 80 L44 58 L8 70 L8 60 L44 40 L44 18 Q44 6 50 6 Z" fill="C"/>',
        "chat": '<path d="M10 20 Q10 10 20 10 L80 10 Q90 10 90 20 L90 62 Q90 72 80 72 L44 72 L24 90 L28 72 L20 72 Q10 72 10 62 Z" fill="C"/>'
                '<circle cx="32" cy="41" r="6" fill="#fff"/><circle cx="50" cy="41" r="6" fill="#fff"/><circle cx="68" cy="41" r="6" fill="#fff"/>',
    }[name].replace('"C"', f'"{color}"')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">{p}</svg>'


def clock(hh, mm, size=200, color="#C8102E"):
    import math
    ah = math.radians((hh % 12 + mm / 60) * 30)
    am = math.radians(mm * 6)
    hx, hy = 50 + 22 * math.sin(ah), 50 - 22 * math.cos(ah)
    mx, my = 50 + 32 * math.sin(am), 50 - 32 * math.cos(am)
    ticks = "".join(f'<rect x="48.5" y="8" width="3" height="8" fill="{color}" transform="rotate({k * 30} 50 50)"/>' for k in range(12))
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#fff" stroke="{color}" stroke-width="6"/>'
            f'{ticks}<line x1="50" y1="50" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#2B2B2B" stroke-width="6" stroke-linecap="round"/>'
            f'<line x1="50" y1="50" x2="{mx:.1f}" y2="{my:.1f}" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="50" cy="50" r="4" fill="{color}"/></svg>')
