"""YouTube thumbnail 1280x720 -> thumbnail/thumbnail.html + thumbnail.jpg. Run from project root:
    python3 -I tools/thumbnail.py
(No French in title/thumbnail - director's rule.)"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MAPLE, kid  # noqa: E402

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
fonts = open(os.path.join("assets", "fonts", "fonts.css"), encoding="utf-8").read().replace("url(assets/", "url(../assets/")
leaf = f'<svg viewBox="0 0 100 100"><path d="{MAPLE}" fill="#C8102E"/></svg>'
kids = kid("#7A1B26", 64) + kid("#7A1B26", 52)

html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8" />
<style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:900px;overflow:hidden;background:#FFF8F2;font-family:'Noto Sans KR',sans-serif;color:#2B2B2B}}
.top{{position:absolute;left:0;right:0;top:0;height:22px;background:#C8102E}}
.leaf{{position:absolute;opacity:.10}}
.leaf svg{{width:100%;height:100%}}
.l1{{left:930px;top:-60px;width:420px;height:420px}}
.l2{{left:-80px;top:470px;width:300px;height:300px}}
.k{{position:absolute;left:70px;top:58px;display:flex;align-items:flex-end;gap:10px}}
.t1{{position:absolute;left:66px;top:160px;font-family:'Black Han Sans';font-size:100px;line-height:1.08;letter-spacing:-.01em}}
.t2{{position:absolute;left:62px;top:276px;font-family:'Black Han Sans';font-size:190px;line-height:1;color:#C8102E;letter-spacing:-.02em}}
.t2 small{{font-size:110px}}
.vs{{position:absolute;left:1000px;top:230px;width:200px;height:200px;border-radius:50%;background:#2B2B2B;color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Black Han Sans';font-size:96px;transform:rotate(-8deg);box-shadow:0 12px 26px rgba(43,43,43,.3)}}
.band{{position:absolute;left:44px;top:518px;width:1192px;height:168px;background:#C8102E;border-radius:28px;display:flex;align-items:center;padding:0 44px;gap:30px;box-shadow:0 14px 30px rgba(122,27,38,.25)}}
.band .lf{{width:104px;height:104px;flex:none}}
.band .lf path{{fill:#fff}}
.band .t{{font-family:'Black Han Sans';font-size:96px;color:#fff;white-space:nowrap}}
.band .t b{{color:#FFD6CF;font-weight:400}}
.logo{{position:absolute;right:40px;top:52px;display:flex;align-items:center;gap:10px;font-weight:900;font-size:28px}}
.logo img{{width:60px;height:58px}}
</style></head><body>
<div class="top"></div>
<div class="leaf l1">{leaf}</div><div class="leaf l2">{leaf}</div>
<div class="k">{kids}</div>
<div class="t1">영유 아이 둘이면 1년</div>
<div class="t2">3,580<small>만원</small></div>
<div class="vs">VS</div>
<div class="band"><div class="lf">{leaf}</div><div class="t">캐나다에선 <b>아이 학비 0원</b></div></div>
<div class="logo"><img src="../assets/img/aa-canada-logo-transparent.png" alt="" />AA Canada</div>
</body></html>
"""
open(os.path.join("thumbnail", "thumbnail.html"), "w", encoding="utf-8").write(html)
png = os.path.abspath(os.path.join("thumbnail", "thumbnail.png"))
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1",
                f"--screenshot={png}", "--window-size=1280,900", "--virtual-time-budget=3000",
                "file://" + os.path.abspath(os.path.join("thumbnail", "thumbnail.html"))], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", png, "-vf", "crop=1280:720:0:0", "-q:v", "2", os.path.join("thumbnail", "thumbnail.jpg")], check=True)
os.remove(png)
print("thumbnail/thumbnail.jpg")
