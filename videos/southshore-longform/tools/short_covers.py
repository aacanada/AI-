"""1080x1920 cover images for the shorts (title + brand only, so no scene text - e.g. 불어 - lands on a cover).
Run from the long-form project root after shorts.py:  python3 -I tools/short_covers.py
Writes ../southshore-shorts/short-<x>/cover.jpg"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MAPLE  # noqa: E402
from shorts import OUT, SHORTS  # noqa: E402

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
SUB = {"a": "REM 브로사드역 → 다운타운 중앙역", "b": "한국계 인구 · 2021 캐나다 인구조사", "c": "동네 고르는 법",
       "d": "리버사이드 교육청 학교 영상", "e": "2027-28 리버사이드 학비표"}

for key, sh in SHORTS.items():
    d = os.path.abspath(os.path.join(OUT, f"short-{key}"))
    fonts = open(os.path.join("assets", "fonts", "fonts.css"), encoding="utf-8").read().replace("url(assets/", "url(assets/")
    title = "".join(f"<div>{x}</div>" for x in sh["title"])
    html = f"""<!doctype html><html lang="ko"><head><meta charset="UTF-8" /><style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:2100px;overflow:hidden;background:#FFF8F2;font-family:'Noto Sans KR',sans-serif;color:#2B2B2B}}
.bar{{position:absolute;left:0;right:0;top:0;height:24px;background:#C8102E}}
.leaf{{position:absolute;opacity:.10}} .leaf svg{{width:100%;height:100%}}
.l1{{left:560px;top:120px;width:640px;height:640px}} .l2{{left:-140px;top:1200px;width:520px;height:520px}}
.chip{{position:absolute;left:0;right:0;top:470px;text-align:center}}
.chip span{{display:inline-block;padding:14px 40px;border-radius:99px;background:#C8102E;color:#fff;font-weight:900;font-size:44px}}
.title{{position:absolute;left:0;right:0;top:620px;text-align:center;font-family:'Black Han Sans';font-size:96px;line-height:1.18}}
.title em{{font-style:normal;color:#C8102E}}
.sub{{position:absolute;left:0;right:0;top:960px;text-align:center;font-weight:900;font-size:54px;color:#7A1B26}}
.big{{position:absolute;left:390px;top:1090px;width:300px;height:300px}} .big path{{fill:#C8102E}}
.logo{{position:absolute;left:0;right:0;top:1180px;display:flex;justify-content:center;align-items:center;gap:16px;font-weight:900;font-size:44px}}
.logo img{{width:96px;height:93px}}
</style></head><body><div class="bar"></div>
<div class="leaf l1"><svg viewBox="0 0 100 100"><path d="{MAPLE}" fill="#C8102E"/></svg></div>
<div class="leaf l2"><svg viewBox="0 0 100 100"><path d="{MAPLE}" fill="#C8102E"/></svg></div>
<div class="chip"><span>몬트리올 사우스쇼어</span></div>
<div class="title">{title}</div><div class="sub">{SUB[key]}</div>
<div class="logo"><img src="assets/img/aa-canada-logo-transparent.png" alt="" />AA Canada</div>
</body></html>"""
    hp = os.path.join(d, "cover.html")
    open(hp, "w", encoding="utf-8").write(html)
    png = os.path.join(d, "cover.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1080,2100", "--virtual-time-budget=3000", "file://" + hp],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", png, "-vf", "crop=1080:1920:0:0", "-q:v", "2", os.path.join(d, "cover.jpg")], check=True)
    os.remove(png)
    os.remove(hp)
    print(f"short-{key}/cover.jpg")
