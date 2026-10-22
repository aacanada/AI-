"""YouTube thumbnail 1280x720 -> thumbnail/thumbnail.html + thumbnail.jpg (+ thumbnail-b.jpg variant). Run from project root:
    python3 -I tools/thumbnail.py
Map + REM line only (brief: no student faces on the thumbnail)."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo  # noqa: E402
from common import MAPLE  # noqa: E402

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
fonts = open(os.path.join("assets", "fonts", "fonts.css"), encoding="utf-8").read().replace("url(assets/", "url(../assets/")
os.makedirs("thumbnail", exist_ok=True)

V = geo.view(45.468, -73.497, 24, frame_w=1280, frame_h=720, cx=960, cy=390)


def xy(la, lo):
    return geo.screen(la, lo, V)


st = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{12 / V["scale"] * V["scale"]:.0f}" fill="#fff" stroke="#C8102E" stroke-width="6"/>'
             for x, y in (xy(la, lo) for _, _, la, lo in geo.REM_STATIONS))
gx, gy = xy(*geo.REM_STATIONS[-1][2:])
bx, by = xy(*geo.REM_STATIONS[0][2:])


def page(t1, t2, band):
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8" />
<style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:900px;overflow:hidden;background:#FFF8F2;font-family:'Noto Sans KR',sans-serif;color:#2B2B2B}}
.map{{position:absolute;left:0;top:0;width:1280px;height:720px;overflow:hidden}}
.cam{{position:absolute;left:0;top:0;transform-origin:0 0;transform:translate({V["x"]}px,{V["y"]}px) scale({V["scale"]})}}
.fade{{position:absolute;left:0;top:0;width:1280px;height:720px;background:linear-gradient(90deg,rgba(255,248,242,.97) 0%,rgba(255,248,242,.93) 44%,rgba(255,248,242,0) 66%)}}
.top{{position:absolute;left:0;right:0;top:0;height:20px;background:#C8102E}}
.t1{{position:absolute;left:54px;top:96px;font-family:'Black Han Sans';font-size:92px;line-height:1.08}}
.t1 em{{font-style:normal;color:#C8102E}}
.t2{{position:absolute;left:50px;top:300px;font-family:'Black Han Sans';font-size:118px;line-height:1.02;color:#C8102E}}
.band{{position:absolute;left:40px;top:560px;height:110px;background:#2B2B2B;border-radius:24px;display:flex;align-items:center;padding:0 36px;gap:20px}}
.band .lf{{width:70px;height:70px}} .band .lf path{{fill:#C8102E}}
.band .t{{font-family:'Black Han Sans';font-size:58px;color:#fff;white-space:nowrap}}
.tag{{position:absolute;font-family:'Black Han Sans';font-size:34px;background:#fff;border:4px solid #C8102E;color:#C8102E;border-radius:14px;padding:2px 14px;white-space:nowrap}}
.min{{position:absolute;left:{(gx + bx) / 2 - 20:.0f}px;top:{(gy + by) / 2 + 40:.0f}px;font-family:'Black Han Sans';font-size:104px;color:#fff;background:#C8102E;border-radius:26px;padding:4px 26px;transform:rotate(-6deg);box-shadow:0 14px 30px rgba(122,27,38,.3)}}
.logo{{position:absolute;right:30px;bottom:24px;display:flex;align-items:center;gap:10px;font-weight:900;font-size:26px}}
.logo img{{width:56px;height:54px}}
</style></head><body>
<div class="map"><div class="cam">{geo.svg_map(south_hi=True)}</div>
<svg width="1280" height="720" style="position:absolute;left:0;top:0"><polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in (xy(*p) for p in geo.REM_LINE))}" fill="none" stroke="#C8102E" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>{st}</svg>
<div class="tag" style="left:{gx + 24:.0f}px;top:{gy - 24:.0f}px">다운타운 중앙역</div>
<div class="tag" style="left:{bx - 150:.0f}px;top:{by + 24:.0f}px">브로사드역</div>
<div class="min">18분</div></div>
<div class="fade"></div>
<div class="top"></div>
<div class="t1">{t1}</div>
<div class="t2">{t2}</div>
<div class="band"><svg class="lf" viewBox="0 0 100 100"><path d="{MAPLE}"/></svg><div class="t">{band}</div></div>
<div class="logo"><img src="../assets/img/aa-canada-logo-transparent.png" alt="" />AA Canada</div>
</body></html>
"""


def shot(name, html):
    hp = os.path.abspath(os.path.join("thumbnail", name + ".html"))
    open(hp, "w", encoding="utf-8").write(html)
    png = hp[:-5] + ".png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1280,900", "--virtual-time-budget=3000", "file://" + hp], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", png, "-vf", "crop=1280:720:0:0", "-q:v", "2", hp[:-5] + ".jpg"], check=True)
    os.remove(png)
    print(f"thumbnail/{name}.jpg")


shot("thumbnail", page("다운타운 <em>18분</em>인데", "한국인이<br/>없다?".replace("<br/>", " ").replace(" ", "<br>", 1), "몬트리올 영어 공립학교 동네"))
shot("thumbnail-b", page("몬트리올 남쪽", "영어 공립<br>학교 동네", "REM으로 다운타운 18분"))
