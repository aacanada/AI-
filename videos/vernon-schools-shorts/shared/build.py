"""Build <short>/index.html (1080x1920 Shorts) from <short>/script.json + <short>/timing.json.

Usage: python3 shared/build.py <short-dir>

script.json  = narration chunks + per-scene visual spec (items).  Never edited by the timing tools.
timing.json  = scene windows + caption chunk windows.  Made by estimate_timing.py (temporary, no audio)
               or narration.py (from the owner's recordings).  Re-run build.py after either.
"""
import html, json, pathlib, re, shutil, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from icons import icon  # noqa: E402

SHARED = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
PHOTOS = SHARED.parent.parent.parent / "plans" / "vernon-schools-shorts" / "assets" / "photos"
SPEC = json.loads((ROOT / "script.json").read_text())
T = json.loads((ROOT / "timing.json").read_text())
TOTAL = T["total"]

ACC = SPEC["accent"]
GOLD, RED, GREEN, LAKE, NAVY, NAVY2 = "#ffd23f", "#e63946", "#2ec27e", "#1fb5c9", "#0b1730", "#132a52"
COLORS = {"acc": ACC, "gold": GOLD, "red": RED, "green": GREEN, "lake": LAKE, "white": "#ffffff"}
col = lambda c: COLORS.get(c, c) if c else ACC


def lum(h):
    h = h.lstrip("#")
    ch = [int(h[k:k + 2], 16) / 255 for k in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def txt(bg):
    """Text colour with the better contrast on a solid background."""
    L = lum(bg)
    return "#0b1730" if (L + 0.05) / (lum("#0b1730") + 0.05) > 1.05 / (L + 0.05) else "#ffffff"
E = html.escape


def r(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- assets
def sync_assets():
    a = ROOT / "assets"
    for sub in ("fonts", "vendor", "sfx", "photos", "audio"):
        (a / sub).mkdir(parents=True, exist_ok=True)
    for src, dst in ((SHARED / "fonts", a / "fonts"), (SHARED / "vendor", a / "vendor"), (SHARED / "sfx", a / "sfx")):
        for f in src.iterdir():
            if not (dst / f.name).exists() or (dst / f.name).stat().st_size != f.stat().st_size:
                shutil.copy2(f, dst / f.name)
    bgm = SHARED / "bgm" / SPEC.get("bgm", "bgm-a.mp3")
    if not (a / "audio" / "bgm.mp3").exists():
        shutil.copy2(bgm, a / "audio" / "bgm.mp3")
    used = set(re.findall(r'"([a-z]+-\d\d-[a-z0-9-]+)"', json.dumps(SPEC)))
    for name in used:
        f = PHOTOS / f"{name}.jpg"
        if f.exists() and not (a / "photos" / f.name).exists():
            shutil.copy2(f, a / "photos" / f.name)
    return used


def ph(name):
    return f"assets/photos/{name}.jpg"


# ---------------------------------------------------------------- map
# Stylised Vernon (relative positions only, per brief).  viewBox 0 0 400 440.
MAP_PINS = {"seaton": (196, 196), "vss": (262, 182), "fulton": (112, 236), "kal": (246, 318), "bloom": (378, 150)}
MAP_SVG = """
<path class="mp-draw mp-lake" d="M40 430 C60 380 52 330 70 290 C86 254 72 220 86 186 C98 156 84 120 70 86 C60 60 74 30 92 10 L106 14 C92 40 86 64 98 96 C112 132 112 164 102 196 C92 230 104 262 92 296 C78 336 86 384 70 430 Z"/>
<path class="mp-draw mp-lake" d="M232 440 C236 404 226 380 238 352 C246 334 240 312 252 296 L264 300 C256 318 262 336 254 356 C246 382 256 406 252 440 Z"/>
<path class="mp-draw mp-lake" d="M180 60 C196 46 222 48 230 64 C236 80 214 92 196 88 C180 84 170 74 180 60 Z"/>
<path class="mp-draw mp-city" d="M120 120 C160 96 230 100 300 130 C330 150 330 220 300 262 C280 300 250 336 220 340 C180 344 140 300 120 262 C104 230 100 150 120 120 Z"/>
<path class="mp-draw mp-road" d="M200 0 C200 80 196 140 196 196 C196 250 230 290 246 330 C256 360 262 400 262 440"/>
<path class="mp-draw mp-road" d="M196 196 C240 186 300 170 400 150"/>
<path class="mp-draw mp-road" d="M196 196 C160 206 130 220 100 240"/>
"""


def map_html(it):
    pins = MAP_PINS if it["pin"] == "all" else {it["pin"]: MAP_PINS[it["pin"]]}
    pin_svg = "".join(
        f'<g transform="translate({x} {y})"><g class="mp-pin"><circle class="mp-pulse" r="14" fill="{ACC}"/>'
        f'<path d="M0 0 C-11 -14 -14 -20 -14 -27 A14 14 0 0 1 14 -27 C14 -20 11 -14 0 0 Z" fill="{RED}" stroke="#fff" stroke-width="3"/>'
        f'<circle cy="-27" r="5" fill="#fff"/></g></g>' for k, (x, y) in pins.items())
    lbl = f'<div class="mp-label">{E(it.get("label", ""))}</div>' if it.get("label") else ""
    note = f'<div class="mp-note">{E(it["note"])}</div>' if it.get("note") else ""
    return (f'<div class="mapcard" style="{box(it, 600, 820, 420, 560)}">'
            f'<div class="mp-head">VERNON, BC</div>'
            f'<svg class="mp" viewBox="0 0 400 440" width="{340 if it.get("note") else 380}" height="{374 if it.get("note") else 418}">{MAP_SVG}{pin_svg}</svg>{lbl}{note}</div>')


def box(it, x=60, y=600, w=960, h=None):
    s = f"left:{it.get('x', x)}px;top:{it.get('y', y)}px;width:{it.get('w', w)}px;"
    hh = it.get("h", h)
    return s + (f"height:{hh}px;" if hh else "")


# ---------------------------------------------------------------- odometer
def odo(value, cls=""):
    out = []
    for ch in value:
        if ch.isdigit():
            digits = "".join(f"<b>{d % 10}</b>" for d in range(20))
            out.append(f'<span class="od-col" data-d="{ch}"><span class="od-strip">{digits}</span></span>')
        else:
            out.append(f'<span class="od-ch">{E(ch)}</span>')
    return f'<span class="odo {cls}">{"".join(out)}</span>'


def split_chars(text):
    return "".join(f'<span class="ch">{E(c) if c != " " else "&nbsp;"}</span>' for c in text)


# ---------------------------------------------------------------- item renderers
def R_bg(it, iid):
    dim = it.get("dim", 0.45)
    front = ""
    if it.get("parallax", True):
        front = f'<div class="bg-front" style="background-image:url({ph(it["src"])});background-position:{it.get("pos", "50% 50%")}"></div>'
    return (f'<div class="bgph" id="{iid}"><div class="bg-back" style="background-image:url({ph(it["src"])});background-position:{it.get("pos", "50% 50%")}"></div>{front}'
            f'<div class="bg-dim" style="background:linear-gradient(180deg, rgba(11,23,48,{min(1, dim + 0.25)}) 0%, rgba(11,23,48,{dim}) 32%, rgba(11,23,48,{dim}) 70%, rgba(11,23,48,0.92) 100%)"></div></div>')


def R_card(it, iid):
    lab = ""
    if it.get("label"):
        lab = f'<div class="card-label" style="background:{col(it.get("lc"))};color:{txt(col(it.get("lc")))}">{E(it["label"])}</div>'
    return (f'<div class="card3d" id="{iid}" style="{box(it, 60, 600, 960, 640)}">'
            f'<div class="card" style="border-color:{col(it.get("border", "acc"))}"><div class="card-img" style="background-image:url({ph(it["src"])});background-position:{it.get("pos", "50% 50%")}"></div>'
            f'<div class="sweep"></div>{lab}</div></div>')


def R_slam(it, iid):
    sub = f'<div class="slam-sub">{E(it["sub"])}</div>' if it.get("sub") else ""
    return (f'<div class="slam" id="{iid}" style="{box(it, 0, 820, 1080)}">'
            f'<div class="shock" style="border-color:{col(it.get("color", "gold"))}"></div>'
            f'<div class="slam-t" style="font-size:{it.get("size", 300)}px;color:{col(it.get("color", "gold"))}">{E(it["text"])}</div>{sub}</div>')


def R_odo(it, iid):
    ul = f'<div class="odo-ul" style="background:{col(it.get("underline", "red"))}"></div>' if it.get("underline") else ""
    lab = f'<div class="odo-label">{E(it["label"])}</div>' if it.get("label") else ""
    return (f'<div class="odobox" id="{iid}" style="{box(it, 0, 900, 1080)}">{lab}'
            f'<div class="odo-wrap" style="font-size:{it.get("size", 150)}px;color:{col(it.get("color", "gold"))}">{odo(it["value"])}</div>{ul}</div>')


def R_title(it, iid):
    return (f'<div class="title" id="{iid}" style="{box(it, 60, 600, 960)}">'
            f'<div class="t-bar" style="background:{ACC}"></div>'
            f'<div class="t-en" style="font-size:{it.get("size", 64)}px">{split_chars(it["en"])}</div>'
            f'<div class="t-ko"><span>{E(it["ko"])}</span></div></div>')


def R_stats(it, iid):
    rows = "".join(
        f'<div class="stat"><div class="st-l">{E(s["l"])}</div><div class="st-v">{odo(s["v"])}<span class="st-u">{E(s.get("u", ""))}</span></div></div>'
        for s in it["items"])
    return f'<div class="stats" id="{iid}" style="{box(it, 60, 820, 510)}"><div class="strip" style="background:{ACC}"></div>{rows}</div>'


def R_map(it, iid):
    return map_html(it).replace('class="mapcard"', f'class="mapcard" id="{iid}"', 1)


def R_chips(it, iid):
    chips = []
    for c in it["items"]:
        c = c if isinstance(c, dict) else {"t": c}
        bg = col(c.get("c", it.get("color", "acc")))
        ic = icon(c["i"], 44, txt(bg)) if c.get("i") else ""
        chips.append(f'<div class="chip" style="background:{bg};color:{txt(bg)};font-size:{it.get("size", 44)}px">{ic}<span>{E(c["t"])}</span></div>')
    align = it.get("align", "center")
    return f'<div class="chips" id="{iid}" style="{box(it, 60, 900, 960)}justify-content:{align}">{"".join(chips)}</div>'


def R_note(it, iid):
    return (f'<div class="note" id="{iid}" style="{box(it, 60, 1300, 960)}font-size:{it.get("size", 40)}px;color:{col(it.get("color", "white"))};text-align:{it.get("align", "center")}">'
            f'{E(it["text"])}</div>')


def R_quote(it, iid):
    return (f'<div class="quote" id="{iid}" style="{box(it, 60, 1020, 960)}"><div class="q-mark" style="color:{ACC}">&ldquo;</div>'
            f'<div class="q-text">{E(it["text"])}</div><div class="q-by">{E(it.get("by", ""))}</div>'
            f'<div class="strip" style="background:{ACC}"></div></div>')


def R_thumbs(it, iid):
    th = "".join(
        f'<div class="thumb"><div class="th-img" style="background-image:url({ph(s)});height:{it.get("ih", 250)}px"></div><div class="th-l">{E(l)}</div></div>'
        for s, l in zip(it["srcs"], it.get("labels", [""] * len(it["srcs"]))))
    return f'<div class="thumbs" id="{iid}" style="{box(it, 60, 1100, 960)}flex-direction:{it.get("dir", "row")}">{th}</div>'


def R_icons(it, iid):
    tiles = "".join(
        f'<div class="itile"><div class="ic-c" style="background:{col(t.get("c", "acc"))}">{icon(t["i"], 84)}</div><div class="it-l">{E(t["l"])}</div></div>'
        for t in it["items"])
    return f'<div class="icons" id="{iid}" style="{box(it, 60, 1080, 960)}">{tiles}</div>'


def R_split(it, iid):
    L, Rr = it["left"], it["right"]
    left_img = f'<div class="sp-img" style="background-image:url({ph(L["src"])})"></div>' if L.get("src") else ""
    right_img = f'<div class="sp-img" style="background-image:url({ph(Rr["src"])})"></div>' if Rr.get("src") else ""
    def side(S, img, c):
        return (f'<div class="sp-card"><div class="sp-tag" style="background:{col(c)};color:{txt(col(c))}">{E(S["tag"])}</div>{img}'
                f'<div class="sp-ic" style="background:{col(c)}">{icon(S.get("i", "check"), 70)}</div>'
                f'<div class="sp-t">{E(S["title"])}</div><div class="sp-s">{E(S.get("sub", ""))}</div></div>')
    return (f'<div class="split" id="{iid}" style="{box(it, 60, 600, 960, 800)}">'
            f'{side(L, left_img, L.get("c", "lake"))}{side(Rr, right_img, Rr.get("c", "acc"))}</div>')


def R_checks(it, iid):
    rows = "".join(
        f'<div class="ck"><svg class="ck-svg" viewBox="0 0 60 60" width="84" height="84"><circle cx="30" cy="30" r="27" fill="{GREEN}"/>'
        f'<path class="ck-path" d="M17 31 L26 40 L44 21" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
        f'<span>{E(t)}</span></div>' for t in it["items"])
    return f'<div class="checks" id="{iid}" style="{box(it, 60, 1100, 960)}">{rows}</div>'


def R_stamp(it, iid):
    c = col(it.get("color", "red"))
    return (f'<div class="stampwrap" id="{iid}" style="{box(it, 620, 640, 400)}"><div class="stamp" style="color:{c};border-color:{c};font-size:{it.get("size", 56)}px">'
            f'{E(it["text"])}</div></div>')


def R_people(it, iid):
    n, f = it.get("n", 10), it.get("filled", 9)
    figs = "".join(
        f'<div class="pp {"pp-f" if k < f else "pp-o"}"><svg viewBox="0 0 24 40" width="72" height="120"><circle cx="12" cy="7" r="6"/>'
        f'<path d="M3 40 V22 a9 9 0 0 1 18 0 V40 Z"/></svg></div>' for k in range(n))
    return (f'<div class="people" id="{iid}" style="{box(it, 60, 1060, 960)}"><div class="pp-row">{figs}</div>'
            f'<div class="pp-l">{E(it.get("label", ""))}</div></div>')


def R_fork(it, iid):
    return (f'<div class="fork" id="{iid}" style="{box(it, 60, 600, 960, 520)}">'
            f'<svg viewBox="0 0 960 520" width="960" height="520"><path class="fk" d="M480 500 L480 330 C480 250 230 260 230 150 L230 120" pathLength="1" stroke="{LAKE}"/>'
            f'<path class="fk" d="M480 330 C480 250 730 260 730 150 L730 120" pathLength="1" stroke="{ACC}"/></svg>'
            f'<div class="fk-node" style="left:40px;background:{LAKE};color:{txt(LAKE)}"><div class="fk-t">{E(it["left"])}</div><div class="fk-s">{E(it.get("ls", ""))}</div></div>'
            f'<div class="fk-node" style="left:540px;background:{ACC};color:{txt(ACC)}"><div class="fk-t">{E(it["right"])}</div><div class="fk-s">{E(it.get("rs", ""))}</div></div>'
            f'<div class="fk-root">{E(it.get("root", ""))}</div></div>')


def R_fan(it, iid):
    cards = "".join(f'<div class="fan-c" style="background-image:url({ph(s)})"></div>' for s in it["srcs"])
    return f'<div class="fan" id="{iid}" style="{box(it, 0, 640, 1080, 760)}">{cards}</div>'


def R_pick(it, iid):
    c = it["color"]
    return (f'<div class="pick" id="{iid}" style="{box(it, 60, 600, 960, 840)}"><div class="pk-card" style="border-color:{c}">'
            f'<div class="pk-img" style="background-image:url({ph(it["src"])})"></div><div class="pk-band" style="background:{c}"></div>'
            f'<div class="pk-ic" style="background:{c}">{"".join(icon(i, 72) for i in it["icons"])}</div>'
            f'<div class="pk-type">{E(it["type"])}</div>'
            f'<div class="pk-name">{E(it["name"])}</div><div class="pk-en">{E(it["en"])}</div>'
            f'<div class="pk-stat"><span class="pk-v" style="color:{GOLD}">{E(it["stat"])}</span></div></div></div>')


def R_notes(it, iid):
    return (f'<div class="notes" id="{iid}" style="{box(it, 0, 1120, 1080, 260)}"><svg viewBox="0 0 1080 260" width="1080" height="260">'
            + "".join(f'<path class="nl" d="M0 {60 + k * 36} C270 {20 + k * 36} 540 {120 + k * 36} 1080 {50 + k * 36}" pathLength="1"/>' for k in range(5))
            + "".join(f'<g class="nn" transform="translate({x} {y})"><ellipse rx="22" ry="16" transform="rotate(-20)" fill="{GOLD}"/><path d="M20 -6 V-90" stroke="{GOLD}" stroke-width="6"/></g>'
                      for x, y in ((180, 150), (360, 110), (560, 190), (760, 130), (930, 170)))
            + '</svg></div>')


def R_balance(it, iid):
    return (f'<div class="balance" id="{iid}" style="{box(it, 140, 1040, 800, 360)}">'
            f'<div class="bl-post"></div><div class="bl-beam"><div class="bl-pan bl-l" style="background:{GREEN};color:{txt(GREEN)}">{E(it.get("l", "장점?"))}</div>'
            f'<div class="bl-pan bl-r" style="background:{RED};color:{txt(RED)}">{E(it.get("r", "단점?"))}</div></div></div>')


def R_cta(it, iid):
    return (f'<div class="cta" id="{iid}">'
            f'<div class="cta-chip">8분 전체 영상 · 관련 동영상에서</div>'
            f'<div class="cta-logo">{split_chars("AA CANADA")}</div>'
            f'<div class="cta-sub">캐나다 관리형 조기유학 · 자녀무상교육 · 유학 후 이민</div>'
            f'<div class="cta-cities">버논 · 몬트리올 · 밴쿠버 · 토론토</div>'
            f'<div class="cta-btn">무료 상담 · 카톡 canlog</div></div>')


def R_particles(it, iid):
    return f'<div class="parts" id="{iid}" style="top:{it.get("y", 900)}px">' + '<i class="pt"></i>' * it.get("n", 100) + "</div>"


RENDER = {k[2:]: v for k, v in globals().items() if k.startswith("R_")}


# ---------------------------------------------------------------- captions
HL = SPEC.get("highlights", []) + ["AA Canada"]
HL_RE = re.compile("|".join(re.escape(h) for h in sorted(HL, key=len, reverse=True)))


def cap_html(text):
    out, pos = [], 0
    for m in HL_RE.finditer(text):
        out.append(E(text[pos:m.start()]))
        out.append(f'<span class="hl">{E(m.group(0))}</span>')
        pos = m.end()
    out.append(E(text[pos:]))
    return "".join(out)


# ---------------------------------------------------------------- assemble
def main():
    sync_assets()
    assert [s["id"] for s in SPEC["scenes"]] == [s["id"] for s in T["scenes"]], "script.json / timing.json scene mismatch"
    scenes, caps, sfx = [], [], []
    for i, (sc, tm) in enumerate(zip(SPEC["scenes"], T["scenes"])):
        items = []
        for k, it in enumerate(sc["items"]):
            items.append(RENDER[it["t"]](it, f'{sc["id"]}-i{k}'))
        foot = sc.get("foot")
        foot_html = f'<div class="foot">{E(foot)}</div>' if foot else ""
        vis = "" if i == 0 else "opacity:0;"
        scenes.append(
            f'<div id="{sc["id"]}" class="scene" style="background-color:{NAVY};{vis}">'
            f'<div class="sbg"><div class="blob b1" style="background:radial-gradient(closest-side, rgba(47,107,255,0.5), rgba(47,107,255,0))"></div>'
            f'<div class="blob b2" style="background:radial-gradient(closest-side, {hexa(ACC, 0.35)}, {hexa(ACC, 0)})"></div>'
            f'<div class="grid"></div></div>'
            f'<div class="cam" id="{sc["id"]}-cam">{"".join(items)}{foot_html}</div>'
            # brand, badge and captions live INSIDE each scene: the shader compositor only carries scene layers
            f'<div class="brand">{brand_html(SPEC["brand"])}</div><div class="badge">{E(SPEC.get("badge", ""))}</div>'
            + "".join(f'<div class="cap" id="cap-{i}-{j}"><div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{cap_html(c["text"])}</span></div></div>'
                      for j, c in enumerate(tm["captions"]))
            + '</div>')
    # ---- audio: narration (if recorded) + BGM bed with narration ducking + SFX
    audio = []
    if (ROOT / "assets" / "audio" / "narration.wav").exists():
        audio.append(f'<audio id="narration" src="assets/audio/narration.wav" data-start="0" data-duration="{r(TOTAL)}" data-track-index="5" data-volume="1"></audio>')
    pts = [{"t": 0, "v": 0}, {"t": 0.8, "v": 0.16}]
    for s in T["scenes"]:
        a0, a1 = s.get("audio_start", s["start"]), s.get("audio_start", s["start"]) + s.get("audio_dur", s["duration"])
        pts += [{"t": round(a0 - 0.15, 3), "v": 0.16}, {"t": round(a0 + 0.1, 3), "v": 0.07},
                {"t": round(a1, 3), "v": 0.07}, {"t": round(a1 + 0.25, 3), "v": 0.16}]
    pts += [{"t": round(TOTAL - 1.6, 3), "v": 0.16}, {"t": round(TOTAL, 3), "v": 0}]
    pts = sorted([p for p in pts if 0 <= p["t"] <= TOTAL], key=lambda p: p["t"])
    dedup = []
    for p in pts:
        if dedup and p["t"] <= dedup[-1]["t"]:
            p = {"t": round(dedup[-1]["t"] + 0.01, 3), "v": p["v"]}
        dedup.append(p)
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": dedup}]})
    audio.append(f'<audio id="bgm" src="assets/audio/bgm.mp3" data-start="0" data-duration="{r(TOTAL)}" data-track-index="6" data-volume="1" data-automation=\'{auto}\'></audio>')
    trans = []
    for i in range(len(T["scenes"]) - 1):
        b = T["scenes"][i + 1]["start"]
        sh = SPEC["scenes"][i + 1].get("shader")
        trans.append({"time": round(b - 0.28, 3), "shader": sh, "duration": 0.56} if sh else {"time": round(b - 0.28, 3), "duration": 0.56})
        sfx.append(("whoosh-cinematic.mp3" if i % 2 == 0 else "whoosh.mp3", b - 0.32, 0.25))
    # item-level SFX
    for i, (sc, tm) in enumerate(zip(SPEC["scenes"], T["scenes"])):
        for it in sc["items"]:
            kind = {"slam": "impact-bass-1.mp3", "stamp": "impact-bass-2.mp3", "chips": "pop.mp3", "icons": "pop.mp3",
                    "cta": "sparkle.mp3", "odo": "impact-bass-2.mp3"}.get(it["t"])
            if kind:
                t0 = at_time(tm, it)
                sfx.append((kind, t0 + (0.12 if it["t"] in ("slam", "stamp") else 0.05), 0.22 if kind == "pop.mp3" else 0.25))
    for k, (f, t0, vol) in enumerate(sfx):
        t0 = max(0, t0)
        audio.append(f'<audio id="sfx{k}" src="assets/sfx/{f}" data-start="{r(t0)}" data-duration="{r(min(2.0, TOTAL - t0))}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')

    page = (SHARED / "template.html").read_text()
    css = (SHARED / "style.css").read_text().replace("__ACCTXT__", txt(ACC)).replace("__ACC__", ACC)
    page = (page.replace("__TITLE__", E(SPEC["title"]))
                .replace("__CSS__", css)
                .replace("__TOTAL__", r(TOTAL))
                .replace("__BRAND__", brand_html(SPEC["brand"]))
                .replace("__BADGE__", E(SPEC.get("badge", "")))
                .replace("__ACC__", ACC)
                .replace("__SCENES__", "\n      ".join(scenes))
                .replace("__CAPTIONS__", "\n      ".join(caps))
                .replace("__AUDIO__", "\n      ".join(audio))
                .replace("__ENGINE__", (SHARED / "engine.js").read_text())
                .replace("__SPEC__", json.dumps(SPEC, ensure_ascii=False))
                .replace("__TRANS__", json.dumps(trans))
                .replace("__TIMING__", json.dumps(T, ensure_ascii=False)))
    (ROOT / "index.html").write_text(page)
    print("index.html written; total", TOTAL, "scenes", len(scenes), "captions", len(caps), "audio", len(audio))


def at_time(tm, it):
    a = it.get("at", 0)
    base = tm["start"] if a == -1 else tm["captions"][min(a, len(tm["captions"]) - 1)]["start"]
    return base + it.get("dt", 0)


def hexa(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


def bokeh(seed):
    import random
    rnd = random.Random(1000 + seed)
    out = []
    for k in range(4):
        s = rnd.randint(14, 34)
        out.append(f'<i class="bk" style="left:{rnd.randint(0, 1000)}px;top:{rnd.randint(200, 1800)}px;width:{s}px;height:{s}px;opacity:{rnd.uniform(0.25, 0.45):.2f}"></i>')
    return out


def brand_html(b):
    head, _, rest = b.partition(" · ")
    return f"<b>{E(head)}</b> · {E(rest)}"


if __name__ == "__main__":
    main()
