"""Subset the brand fonts to the characters the generated HTML uses. Run from project root after build.py:
    YV_FONTSRC=<dir with npm-packed @fontsource/black-han-sans and @fontsource/noto-sans-kr> python3 -I tools/fonts.py
(npm pack @fontsource/black-han-sans @fontsource/noto-sans-kr; Google Fonts is not reachable from the sandbox.)
Writes assets/fonts/*.woff2 + assets/fonts/fonts.css (@font-face with unicode-range, one rule per kept subset)."""
import glob
import html
import os
import re
import subprocess
import sys

SRC = os.environ.get("YV_FONTSRC", "")
OUT = os.path.join("assets", "fonts")
FACES = [("Black Han Sans", "fontsource-black-han-sans-*", "400"), ("Noto Sans KR", "fontsource-noto-sans-kr-*", "500"),
         ("Noto Sans KR", "fontsource-noto-sans-kr-*", "700"), ("Noto Sans KR", "fontsource-noto-sans-kr-*", "900")]


def used_chars(roots):
    chars = set(chr(c) for c in range(0x20, 0x7F))
    for r in roots:
        for p in glob.glob(r, recursive=True):
            t = open(p, encoding="utf-8").read()
            chars |= set(html.unescape(t))
    return chars


def ranges(spec):
    out = []
    for part in spec.split(","):
        part = part.strip().lower().replace("u+", "")
        a, _, b = part.partition("-")
        out.append((int(a, 16), int(b or a, 16)))
    return out


def main(roots):
    chars = used_chars(roots)
    cps = sorted(ord(c) for c in chars)
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "*.woff2")):
        os.remove(f)
    css = []
    for fam, pkg, wt in FACES:
        d = sorted(x for x in glob.glob(os.path.join(SRC, pkg)) if os.path.isdir(x))[-1]
        src_css = open(os.path.join(d, f"{wt}.css"), encoding="utf-8").read()
        for m in re.finditer(r"src: url\(\./files/([^)]+\.woff2)\)[^;]*;\s*unicode-range: ([^;]+);", src_css):
            fn, ur = m.group(1), m.group(2)
            rs = ranges(ur)
            need = [c for c in cps if any(a <= c <= b for a, b in rs)]
            if not need:
                continue
            out = os.path.join(OUT, fn)
            subprocess.run([sys.executable, "-m", "fontTools.subset", os.path.join(d, "files", fn),
                            "--unicodes=" + ",".join(f"{c:04x}" for c in need), "--flavor=woff2",
                            f"--output-file={out}", "--layout-features=*"], check=True, capture_output=True)
            css.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:block;"
                       f"src:url(assets/fonts/{fn}) format('woff2');unicode-range:{ur};}}")
    open(os.path.join(OUT, "fonts.css"), "w", encoding="utf-8").write("\n".join(css) + "\n")
    print(f"chars {len(chars)} faces {len(css)} size {sum(os.path.getsize(f) for f in glob.glob(os.path.join(OUT, '*.woff2'))) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:] or ["index.html", "compositions/*.html", "thumbnail/*.html", "../yeongyu-montreal-shorts/**/*.html"])
