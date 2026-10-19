"""<short>/script.json "thumbnail" -> <short>/thumbnail/thumbnail.html, then renders PNG/JPG via the shorts skill.
Usage: python3 shared/thumbnail.py <short-dir>"""
import html, json, pathlib, subprocess, sys

SHARED = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
spec = json.loads((ROOT / "script.json").read_text())
th = spec["thumbnail"]
ACC = spec["accent"]
E = html.escape


def txt(bg):
    """Text colour with the better contrast on a solid background (same rule as build.py)."""
    def lum(h):
        h = h.lstrip("#")
        ch = [int(h[k:k + 2], 16) / 255 for k in (0, 2, 4)]
        ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    L = lum(bg)
    return "#0b1730" if (L + 0.05) / (lum("#0b1730") + 0.05) > 1.05 / (L + 0.05) else "#ffffff"


if "collage" in th:
    tiles = "".join(f'<div class="tile" style="background-image:url({"../assets/photos/" + s + ".jpg"})"></div>' for s in th["collage"])
    bg = f'<div class="collage">{tiles}</div>'
else:
    bg = f'<div class="bg" style="background-image:url({"../assets/photos/" + th["bg"] + ".jpg"})"></div>'
lines = "".join(f'<div class="ln{" gold" if k in th.get("gold", []) else ""}">{E(t)}</div>' for k, t in enumerate(th["lines"]))
chips = "".join(f'<div class="chip" style="background:{c};color:{txt(c)}">{E(t)}</div>'
                for t, c in zip(th["chips"], th.get("chip_colors", [ACC, "#132a52"] + ["#132a52"] * 8)))
fonts = "../assets/fonts"
page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@font-face {{ font-family: P; font-weight: 800; src: url({fonts}/Pretendard-ExtraBold.woff2); }}
@font-face {{ font-family: P; font-weight: 900; src: url({fonts}/Pretendard-Black.woff2); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b1730; font-family: P, sans-serif; color: #fff; word-break: keep-all; }}
.bg {{ position: absolute; inset: 0; background-size: cover; background-position: 50% 50%; }}
.collage {{ position: absolute; inset: 0; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(3, 1fr); }}
.tile {{ background-size: cover; background-position: 50% 50%; }}
.tile:first-child {{ grid-column: span 2; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(11,23,48,0.55) 0%, rgba(11,23,48,0.62) 30%, rgba(11,23,48,0.72) 70%, rgba(11,23,48,0.95) 100%); }}
.bar {{ position: absolute; left: 0; right: 0; top: 0; height: 16px; background: {ACC}; }}
.pill {{ position: absolute; top: 330px; left: 0; right: 0; margin: 0 auto; width: max-content; padding: 20px 46px; border-radius: 999px;
         background: #e63946; font-size: 52px; font-weight: 900; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
.big {{ position: absolute; top: 560px; left: 40px; right: 40px; text-align: center; }}
.ln {{ font-size: {th.get("size", 168)}px; font-weight: 900; line-height: 1.12; letter-spacing: -0.04em; white-space: nowrap;
       text-shadow: 0 8px 0 rgba(0,0,0,0.35), 0 14px 40px rgba(0,0,0,0.75); }}
.gold {{ color: #ffd23f; }}
.chips {{ position: absolute; top: 1250px; left: 40px; right: 40px; display: flex; flex-wrap: wrap; justify-content: center; gap: 18px; }}
.chip {{ padding: 16px 34px; border-radius: 999px; font-size: 48px; font-weight: 900; border: 4px solid rgba(255,255,255,0.85);
         box-shadow: 0 8px 24px rgba(0,0,0,0.45); }}
.brand {{ position: absolute; top: 1420px; left: 0; right: 0; text-align: center; font-size: 46px; font-weight: 900; letter-spacing: 0.16em; }}
.brand b {{ color: #ff5a66; }}
</style></head><body>{bg}<div class="shade"></div><div class="bar"></div>
<div class="pill">캐나다 버논 조기유학</div><div class="big">{lines}</div><div class="chips">{chips}</div>
<div class="brand"><b>AA</b> CANADA</div></body></html>"""
(ROOT / "thumbnail").mkdir(exist_ok=True)
(ROOT / "thumbnail" / "thumbnail.html").write_text(page)
skill = SHARED.parent.parent.parent / ".claude" / "skills" / "shorts-video" / "scripts" / "thumbnail.sh"
subprocess.run(["bash", str(skill), str(ROOT)], check=True)
