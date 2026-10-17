"""Shared build helpers: kinetic text, odometers, layered backgrounds, captions, SFX tags, page assembly."""
import html, json, random, re, shutil, subprocess, pathlib

KIT = pathlib.Path(__file__).resolve().parent


def r(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def esc(s):
    return html.escape(s)


def kt(text, cls="kt"):
    """kinetic text: one inline-block span per glyph."""
    return f'<span class="{cls}">' + "".join(
        '<span class="ch">&nbsp;</span>' if c == " " else f'<span class="ch">{html.escape(c)}</span>' for c in text) + "</span>"


def odo(digits, cls):
    """odometer: each digit is a column with a 0-9,0-9 strip; other chars are static."""
    parts = []
    for i, d in enumerate(digits):
        if d.isdigit():
            strip = "".join(f"<b>{n % 10}</b>" for n in range(20))
            parts.append(f'<span class="odc"><span class="strip {cls}-d{i}">{strip}</span></span>')
        else:
            parts.append(f'<span class="ods">{html.escape(d)}</span>')
    return "".join(parts)


def bg(seed, W, H, mesh_css, dot_cols, speed_lines=0, n_dots=5):
    rnd = random.Random(seed)
    dots = []
    for _ in range(n_dots):
        s = rnd.randint(14, 70)
        col = rnd.choice(dot_cols)
        a = rnd.choice([0.22, 0.28, 0.35])
        dots.append(f'<i class="bk" data-sp="{rnd.uniform(0.4, 1.6):.2f}" style="left:{rnd.randint(-20, W - 20)}px;top:{rnd.randint(60, H)}px;'
                    f'width:{s}px;height:{s}px;background:radial-gradient(circle, rgba({col},{a}) 0%, rgba({col},0) 70%)"></i>')
    lines = []
    for _ in range(speed_lines):
        w = rnd.randint(120, 420)
        lines.append(f'<i class="spd" data-sp="{rnd.uniform(0.6, 2.2):.2f}" style="left:{rnd.randint(0, W * 3)}px;top:{rnd.randint(80, H - 40)}px;'
                     f'width:{w}px;opacity:{rnd.choice([0.05, 0.07, 0.1])}"></i>')
    gh = H + 500
    return (f'<div class="bgl"><div class="mesh" style="width:{W + 600}px;height:{H + 600}px;background:{mesh_css}"></div>'
            f'<svg class="gridl" width="{W}" height="{gh}" viewBox="0 0 {W} {gh}"><defs><pattern id="gp{seed}" width="90" height="90" patternUnits="userSpaceOnUse">'
            f'<path d="M90 0H0V90" fill="none" stroke="#ffffff" stroke-opacity="0.06" stroke-width="2"/></pattern></defs>'
            f'<rect width="{W}" height="{gh}" fill="url(#gp{seed})"/></svg>' + "".join(dots) + "".join(lines) + "</div>")


def hl_html(text, words):
    if not words:
        return esc(text)
    rx = re.compile("|".join(re.escape(h) for h in sorted(words, key=len, reverse=True)))
    out, pos = [], 0
    for m in rx.finditer(text):
        out.append(esc(text[pos:m.start()])); out.append(f'<span class="hl">{esc(m.group(0))}</span>'); pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def captions(T, words, track=2):
    divs = []
    for i, s in enumerate(T["scenes"]):
        for j, c in enumerate(s["captions"]):
            divs.append(f'<div id="cap-{i}-{j}" class="clip cap" data-start="{r(c["start"])}" data-duration="{r(c["end"] - c["start"])}" data-track-index="{track}">'
                        f'<div class="cap-box" id="cap-{i}-{j}-box"><span class="cap-text">{hl_html(c["text"], words)}</span></div></div>')
    return divs


_DUR = {}


def sfx_tags(root, sfx, total, base_track=11):
    tags, busy = [], []  # busy[lane] = end time of the last clip on that lane
    for k, (n, t, v) in enumerate(sorted(sfx, key=lambda x: x[1])):
        p = root / "assets" / "sfx" / f"{n}.mp3"
        if n not in _DUR:
            _DUR[n] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())
        t = max(0.0, t)
        d = min(_DUR[n], total - t)
        if d <= 0.05:
            continue
        lane = next((q for q, e in enumerate(busy) if e <= t), None)
        if lane is None:
            busy.append(0.0); lane = len(busy) - 1
        busy[lane] = t + d
        tags.append(f'<audio id="sfx-{k}" class="clip" src="assets/sfx/{n}.mp3" data-start="{r(t)}" data-duration="{r(d)}" data-track-index="{base_track + lane}" data-volume="{v}"></audio>')
    return tags


def install(root):
    d = root / "assets" / "kit"
    d.mkdir(parents=True, exist_ok=True)
    for f in ("kit.js", "base.css"):
        shutil.copy(KIT / f, d / f)


def page(root, template, **parts):
    s = (root / "tools" / template).read_text()
    for k, v in parts.items():
        s = s.replace(f"__{k}__", v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
    (root / "index.html").write_text(s)
